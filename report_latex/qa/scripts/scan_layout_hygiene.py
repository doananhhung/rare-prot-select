#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mechanical Layout & Typography Linter for RareProtSelect Report
Part of RareProtSelect LaTeX Multi-Agent QA Framework

Checks:
1. Orphan words / runts (paragraph tail <= 2 words in body paragraphs and table cells)
2. Dangling hyphens (lines starting with '-' followed by digits in tables or text)
3. Underfilled / Dead Pages (body pages with < 1000 characters violating R-VIS-15)
4. Orphan Headings / Orphan Intros at page bottoms violating R-VIS-04 and R-VIS-16
5. Heading syntax errors in .tex source files (manual \\ breaks with stray spaces)
"""

import sys
import os
import re
import argparse
from typing import List, Dict, Any
import pypdf

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def parse_args():
    parser = argparse.ArgumentParser(description="Mechanical Layout & Typography Linter for LaTeX PDF")
    parser.add_argument('--pdf', default='report_latex/thuc_tap_cong_nghiep/main.pdf', help='Path to target PDF')
    parser.add_argument('--tex-dir', default='report_latex/thuc_tap_cong_nghiep/contents/chapters', help='Path to .tex chapters')
    return parser.parse_args()

def audit_layout():
    args = parse_args()
    pdf_path = args.pdf
    if not os.path.exists(pdf_path) and os.path.exists('main.pdf'):
        pdf_path = 'main.pdf'
        
    try:
        reader = pypdf.PdfReader(pdf_path)
    except Exception as e:
        print(f"ERROR: Cannot read PDF file at {pdf_path}: {e}")
        sys.exit(1)

    total_pages = len(reader.pages)
    findings = []
    
    # -------------------------------------------------------------
    # Check 1 & 2: Paragraph Tails (Runts) and Dangling Hyphens
    # -------------------------------------------------------------
    for page_idx, page in enumerate(reader.pages, 1):
        # Exclude bibliography pages from prose paragraph tail checks
        if page_idx >= 21:
            continue
            
        text = page.extract_text()
        if not text:
            continue
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        for line_idx, line in enumerate(lines):
            # Ignore page numbers
            if line.isdigit():
                continue
                
            # Ignore structural headings, document headers, table captions
            if any(line.startswith(h) for h in [
                'CHƯƠNG', 'BÁO CÁO', 'DANH MỤC', 'MỤC LỤC', 'TÊN ĐỀ TÀI',
                'Hà Nội', 'Hình ', 'Bảng ', 'Sinh viên', 'Giảng viên',
                'Cơ sở', 'Mã số', 'Ngành', 'Khóa', 'Hệ', 'Ký tên', 'Họ và tên', 'Trưởng phòng'
            ]):
                continue
            
            words = line.split()
            
            # Check: Dangling hyphen at line start (e.g. '- 21/09')
            if line.startswith('- ') and len(words) >= 2 and words[1][0].isdigit():
                findings.append({
                    "page": page_idx,
                    "type": "DANGLING_HYPHEN",
                    "line": line,
                    "context": lines[line_idx - 1] if line_idx > 0 else ""
                })
                
            # Check: Orphan words in body text / table cells
            if len(words) in [1, 2] and line_idx > 0:
                prev_line = lines[line_idx - 1]
                
                # Filter out math display fractions (like \frac{n_max}{n_min}) and equation variables
                if line in ['nmin', 'nmax', 'w(α)', 'wv(α)'] or line.startswith('w('):
                    continue
                # Filter out chapter subtitle wrapped in all-caps
                if line == 'RAREPROTSELECT':
                    continue
                # Filter out table column headers
                if line in ['Sens, %', 'Count']:
                    continue
                # Filter out section titles wrapping 1 word
                if prev_line.startswith('1.') or prev_line.startswith('2.') or prev_line.startswith('3.') or prev_line.startswith('4.') or prev_line.startswith('5.'):
                    continue
                    
                # If previous line is a long narrative sentence (>= 6 words)
                if len(prev_line.split()) >= 6:
                    if not line.startswith('\\') and not line.startswith('$') and not line.startswith('-'):
                        findings.append({
                            "page": page_idx,
                            "type": "ORPHAN_WORD",
                            "line": line,
                            "context": prev_line
                        })

    # -------------------------------------------------------------
    # Check 3: Underfilled / Dead Pages (R-VIS-15)
    # Body pages from Page 6 to Page (total_pages - 2) must have >= 1000 characters
    # -------------------------------------------------------------
    for page_idx in range(6, total_pages - 1):
        page_text = reader.pages[page_idx - 1].extract_text()
        text_len = len(page_text.strip()) if page_text else 0
        if text_len < 1000:
            findings.append({
                "page": page_idx,
                "type": "UNDERFILLED_PAGE",
                "line": f"Text length: {text_len} chars (< 1000 min limit)",
                "context": f"First 50 chars: '{page_text.strip()[:50]}...'" if page_text else "EMPTY PAGE"
            })

    # -------------------------------------------------------------
    # Check 4: Orphan Headings & Orphan Intro Clauses at Page Bottom (R-VIS-04, R-VIS-16)
    # Body pages only (page 6 to total_pages - 1)
    # -------------------------------------------------------------
    for page_idx in range(6, total_pages):
        page_text = reader.pages[page_idx - 1].extract_text()
        if not page_text:
            continue
        lines = [l.strip() for l in page_text.split('\n') if l.strip()]
        # Filter out trailing page number
        content_lines = [l for l in lines if not l.isdigit()]
        if not content_lines:
            continue
            
        last_line = content_lines[-1]
        
        # Check if any section heading appears in the last 3 content lines of the page
        for lookback in range(1, min(4, len(content_lines) + 1)):
            cand_line = content_lines[-lookback]
            is_heading = bool(re.match(r'^\d+\.\d+(\.\d+)?\.\s+', cand_line) or cand_line.startswith('CHƯƠNG'))
            if is_heading:
                # If it's a heading followed only by 1-2 lines ending in ':' or with fewer than 3 lines of text
                subsequent = content_lines[-lookback + 1:]
                if not subsequent or last_line.endswith(':') or len(subsequent) < 3:
                    findings.append({
                        "page": page_idx,
                        "type": "ORPHAN_HEADING",
                        "line": f"{cand_line} (followed by {len(subsequent)} lines ending in '{last_line[-25:]}')",
                        "context": "Heading stranded near bottom of page without sufficient body text or list items"
                    })
                break

    # -------------------------------------------------------------
    # Check 5, 6, 7, 8: Codebase Syntax & Consistency Audits in .tex Source Files
    # -------------------------------------------------------------
    tex_dir = args.tex_dir
    if os.path.exists(tex_dir):
        for root, _, files in os.walk(tex_dir):
            for file in files:
                if file.endswith('.tex'):
                    fpath = os.path.join(root, file)
                    with open(fpath, 'r', encoding='utf-8') as f:
                        for lno, line in enumerate(f, 1):
                            # Ignore commented lines
                            stripped = line.strip()
                            if stripped.startswith('%'):
                                continue
                                
                            # Check 5: Heading Syntax Errors (Stray space after \\)
                            if any(cmd in line for cmd in [r'\section', r'\subsection', r'\subsubsection']):
                                if re.search(r'\\\\\s+', line):
                                    findings.append({
                                        "page": 0,
                                        "type": "HEADING_SYNTAX_ERROR",
                                        "line": f"{file}:{lno} - {stripped}",
                                        "context": "Manual linebreak '\\\\' inside heading has trailing whitespace causing indentation flaws"
                                    })
                                    
                            # Check 6: Prose Font Consistency (No \texttt in prose chapters)
                            if r'\texttt{' in line:
                                findings.append({
                                    "page": 0,
                                    "type": "PROSE_FONT_CONSISTENCY",
                                    "line": f"{file}:{lno} - {stripped}",
                                    "context": "Monospace \\texttt font clashes with Times New Roman prose. Use \\textbf or quotes instead."
                                })
                                
                            # Check 7: Abbreviated Math Symbol (\mathbf{cov})
                            if r'\mathbf{cov}' in line or r'\mathbf{cov}_' in line:
                                findings.append({
                                    "page": 0,
                                    "type": "ABBREVIATED_MATH_SYMBOL",
                                    "line": f"{file}:{lno} - {stripped}",
                                    "context": "Abbreviated \\mathbf{cov} risks confusion with covariance. Use full \\mathbf{coverage} instead."
                                })
                                
                            # Check 8: Latin Phrase Hygiene (ceteris paribus)
                            if 'ceteris paribus' in line.lower():
                                findings.append({
                                    "page": 0,
                                    "type": "LATIN_PHRASE",
                                    "line": f"{file}:{lno} - {stripped}",
                                    "context": "Redundant Latin phrase 'ceteris paribus' clutters prose. Use pure Vietnamese instead."
                                })
                                
                            # Check 9: ORLab Brand & Capitalization Hygiene
                            if re.search(r'\bORlab\b', line):
                                findings.append({
                                    "page": 0,
                                    "type": "ORLAB_CAPITALIZATION",
                                    "line": f"{file}:{lno} - {stripped}",
                                    "context": "Inconsistent 'ORlab' lowercase 'l'. Must be standardized to 'ORLab'."
                                })
                            if 'large-scale systems optimization laboratory' in line.lower():
                                findings.append({
                                    "page": 0,
                                    "type": "FABRICATED_NAME",
                                    "line": f"{file}:{lno} - {stripped}",
                                    "context": "Fabricated English name 'Large-scale Systems Optimization Laboratory' not in official website."
                                })

    print(f"=== MECHANICAL LAYOUT HYGIENE AUDIT ({total_pages} PAGES) ===")
    if not findings:
        print("STATUS: PASSED (0 layout defects found across all body paragraphs, headings and tables)")
        sys.exit(0)
    else:
        print(f"STATUS: FAILED ({len(findings)} layout defects found)")
        for f in findings:
            p_str = f"Page {f['page']}" if f['page'] > 0 else "Source Code"
            print(f" - {p_str} [{f['type']}]: '{f['line']}' (Context: '{f['context'][:70]}...')")
        sys.exit(1)

if __name__ == '__main__':
    audit_layout()
