#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Candidate Terminology Harvester for LaTeX Scientific Reports
Part of RareProtSelect LaTeX Multi-Agent QA Framework

Extracts candidate technical terminology from LaTeX files across 4 filters:
1. English words, uppercase acronyms, and hyphenated terms.
2. Formatted phrases inside \\textbf{}, \\textit{}, \\emph{}.
3. Technical N-grams triggered by specialized Vietnamese headwords:
   - thuật toán, giải thuật, cơ chế, mô hình, bài toán, hàm, phương pháp,
     chỉ số, thước đo, không gian, kỹ thuật, hiện tượng, nguyên tắc, tỷ lệ, độ.
4. Math-adjacent noun phrases preceding or following $...$.

Cross-references with R-TERM.md to classify candidates as:
- [CATALOGED]: Already defined in R-TERM.md (whitelist or blacklist).
- [UNCATALOGED]: Potential new terms or unverified translations requiring web research.
"""

import os
import re
import sys
import json
import argparse
from typing import Dict, List, Set, Any

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Trigger keywords for specialized Vietnamese technical phrases
TECHNICAL_TRIGGERS = [
    'thuật toán', 'giải thuật', 'cơ chế', 'mô hình', 'bài toán',
    'hàm mục tiêu', 'hàm', 'phương pháp', 'chỉ số', 'thước đo',
    'không gian', 'kỹ thuật', 'hiện tượng', 'nguyên tắc', 'tỷ lệ', 'độ'
]

def load_rterm_catalog(rterm_path: str) -> Dict[str, Set[str]]:
    """Loads known terms from R-TERM.md to separate cataloged from uncataloged."""
    cataloged_terms = set()
    forbidden_terms = set()
    
    if not os.path.exists(rterm_path):
        return {"cataloged": cataloged_terms, "forbidden": forbidden_terms}
        
    with open(rterm_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    def add_terms_from_cell(cell_str: str, target_set: Set[str]):
        # Clean markdown bold/backticks
        cleaned = re.sub(r'[*`]', '', cell_str).strip()
        # Split by comma or slash
        for chunk in re.split(r'[,/]', cleaned):
            c = chunk.strip().lower()
            if c and len(c) > 2 and not c.startswith('r-term') and not c.startswith(':-'):
                target_set.add(c)

    for line in content.split('\n'):
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                col1 = parts[1]
                col2 = parts[2]
                col3 = parts[3]
                
                # Check if this is Section 1 (Master Blacklist) where col1 is R-TERM-01x
                if 'R-TERM-01' in col1:
                    add_terms_from_cell(col2, forbidden_terms)
                    add_terms_from_cell(col3, cataloged_terms)
                # Check if this is Section 14 (Extended Catalog) where col2 is Mandatory and col3 is Forbidden
                elif not col1.startswith(':-') and not col1.startswith('Khái niệm') and not col1.startswith('Mã'):
                    add_terms_from_cell(col1, cataloged_terms)
                    add_terms_from_cell(col2, cataloged_terms)
                    add_terms_from_cell(col3, forbidden_terms)
                        
    # Also extract bold terms in text
    for m in re.finditer(r'\*\*([^*]+)\*\*', content):
        term = m.group(1).strip().lower()
        if len(term) > 3 and not term.startswith('r-term') and not term.startswith('lưu ý') and not term.startswith('chú ý'):
            cataloged_terms.add(term)
            
    return {"cataloged": cataloged_terms, "forbidden": forbidden_terms}

def clean_latex(text: str) -> str:
    """Removes comments and normalizes whitespace."""
    lines = []
    for line in text.split('\n'):
        # Strip comments
        line = re.sub(r'(?<!\\)%.*$', '', line)
        lines.append(line)
    return '\n'.join(lines)

def extract_candidates_from_file(file_path: str) -> Dict[str, Any]:
    """Extracts candidate technical terminology from a single .tex file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    clean_content = clean_latex(raw_content)
    file_candidates = {
        "file": os.path.basename(file_path),
        "path": file_path,
        "english_entities": set(),
        "formatted_entities": set(),
        "triggered_phrases": set(),
        "math_adjacent": set()
    }
    
    # Filter 1: Formatted entities inside \textbf{}, \textit{}, \emph{}
    for m in re.finditer(r'\\(?:textbf|textit|emph)\{([^}]+)\}', clean_content):
        val = m.group(1).strip()
        # Exclude math mode only or trivial numbers
        if val and not val.startswith('$') and len(val) > 2 and not val.isdigit():
            file_candidates["formatted_entities"].add(val)
            
    # Filter 2: Uppercase English acronyms & technical words
    for m in re.finditer(r'\b[A-Z][A-Za-z0-9_\-]*(?:\s+[A-Z][A-Za-z0-9_\-]*)*\b', clean_content):
        val = m.group(0).strip()
        if len(val) > 2 and not val.isdigit() and val not in ['CHƯƠNG', 'BẢNG', 'HÌNH', 'MỤC']:
            # Check if ASCII / English
            if re.match(r'^[A-Za-z0-9_\-\s]+$', val):
                file_candidates["english_entities"].add(val)
                
    # Filter 3: Vietnamese Technical N-grams triggered by headwords
    for line in clean_content.split('\n'):
        line_clean = line.strip()
        if not line_clean:
            continue
        for trig in TECHNICAL_TRIGGERS:
            # Match trigger followed by 1 to 5 words
            pattern = rf'\b({trig}\s+[\w\d\-_~]+(?:\s+[\w\d\-_~]+){{1,4}})'
            for m in re.finditer(pattern, line_clean, re.IGNORECASE):
                phrase = m.group(1).replace('~', ' ').strip()
                # Clean punctuation at end
                phrase = re.sub(r'[,.:;?()]+$', '', phrase)
                if len(phrase.split()) >= 2:
                    file_candidates["triggered_phrases"].add(phrase)
                    
    # Filter 4: Math-adjacent noun phrases
    # (e.g. "hàm mục tiêu $F_\alpha$", "ngưỡng cắt tỉa $\theta$")
    for m in re.finditer(r'([\w\d\-_~]+(?:\s+[\w\d\-_~]+){1,3})\s+\$[^\$]+\$', clean_content):
        phrase = m.group(1).replace('~', ' ').strip()
        if len(phrase.split()) >= 2 and any(t in phrase.lower() for t in ['hàm', 'ngưỡng', 'độ', 'tập', 'vector', 'ma trận', 'hệ số']):
            file_candidates["math_adjacent"].add(phrase)

    return file_candidates

def harvest_directory(target_dir: str, rterm_path: str, output_path: str):
    """Harvests all candidates across target .tex files and compiles JSON report."""
    catalog = load_rterm_catalog(rterm_path)
    cataloged_terms = catalog["cataloged"]
    forbidden_terms = catalog["forbidden"]
    
    all_english = set()
    all_formatted = set()
    all_triggered = set()
    all_math_adj = set()
    
    file_summaries = []
    
    for root, dirs, files in os.walk(target_dir):
        for f in files:
            if f.endswith('.tex'):
                full_path = os.path.join(root, f)
                file_res = extract_candidates_from_file(full_path)
                
                all_english.update(file_res["english_entities"])
                all_formatted.update(file_res["formatted_entities"])
                all_triggered.update(file_res["triggered_phrases"])
                all_math_adj.update(file_res["math_adjacent"])
                
                file_summaries.append({
                    "file": file_res["file"],
                    "english_count": len(file_res["english_entities"]),
                    "formatted_count": len(file_res["formatted_entities"]),
                    "triggered_count": len(file_res["triggered_phrases"])
                })
                
    # Consolidate candidates
    consolidated_candidates = []
    
    # Helper to classify term
    def classify_term(term_str: str, category: str):
        term_lower = term_str.lower().strip()
        
        # Word-boundary or exact phrase match for forbidden terms
        is_forbidden = False
        forbidden_match = ""
        for f in forbidden_terms:
            if len(f) > 2 and (f == term_lower or re.search(rf'(?:\b|^){re.escape(f)}(?:\b|$)', term_lower)):
                is_forbidden = True
                forbidden_match = f
                break
                
        # Cataloged check
        is_cataloged = False
        for c in cataloged_terms:
            if len(c) > 2 and (c in term_lower or term_lower in c):
                is_cataloged = True
                break
        
        status = "CATALOGED"
        if is_forbidden:
            status = "FORBIDDEN_DETECTED"
        elif not is_cataloged:
            status = "UNCATALOGED_TERM"
            
        res = {
            "term": term_str,
            "category": category,
            "status": status,
            "requires_web_research": (status == "UNCATALOGED_TERM")
        }
        if is_forbidden:
            res["matched_forbidden_rule"] = forbidden_match
        return res

    for item in sorted(all_english):
        consolidated_candidates.append(classify_term(item, "English_Acronym_Entity"))
    for item in sorted(all_formatted):
        consolidated_candidates.append(classify_term(item, "Formatted_Entity"))
    for item in sorted(all_triggered):
        consolidated_candidates.append(classify_term(item, "Triggered_Technical_Phrase"))
    for item in sorted(all_math_adj):
        consolidated_candidates.append(classify_term(item, "Math_Adjacent_Phrase"))

    uncataloged_count = sum(1 for c in consolidated_candidates if c["status"] == "UNCATALOGED_TERM")
    forbidden_count = sum(1 for c in consolidated_candidates if c["status"] == "FORBIDDEN_DETECTED")
    cataloged_count = sum(1 for c in consolidated_candidates if c["status"] == "CATALOGED")

    report = {
        "metadata": {
            "target_dir": target_dir,
            "total_candidates": len(consolidated_candidates),
            "cataloged_count": cataloged_count,
            "uncataloged_count": uncataloged_count,
            "forbidden_count": forbidden_count
        },
        "file_summaries": file_summaries,
        "candidates": consolidated_candidates
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"=== CANDIDATE TERMINOLOGY HARVEST COMPLETE ===")
    print(f"Target Directory: {target_dir}")
    print(f"Total Extracted Candidates: {len(consolidated_candidates)}")
    print(f" - Cataloged in R-TERM.md: {cataloged_count}")
    print(f" - Uncataloged (Requiring Web Research): {uncataloged_count}")
    print(f" - Forbidden Detected: {forbidden_count}")
    print(f"Report Output: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Harvest candidate terminology from LaTeX files.")
    parser.add_argument("--dir", default="report_latex/thuc_tap_cong_nghiep/contents", help="Directory of .tex files")
    parser.add_argument("--rterm", default="report_latex/qa/rules/R-TERM.md", help="Path to R-TERM.md catalog")
    parser.add_argument("--output", default="report_latex/qa/runs/candidate_terms.json", help="Path to output JSON")
    
    args = parser.parse_args()
    harvest_directory(args.dir, args.rterm, args.output)
