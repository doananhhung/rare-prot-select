# -*- coding: utf-8 -*-
"""
Cổng 1: Linter kiểm tra tĩnh mã nguồn LaTeX (report_latex/qa/lint_report.py)
Thực hiện kiểm tra tất định các quy chuẩn hình thức, Master Blacklist, chính tả và định dạng.
"""
import sys
import os
import re
import json
import argparse
from typing import List, Dict, Any

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Master Blacklist rules (Rule ID, Pattern, Message, Severity)
BLACKLIST_RULES = [
    ("R-TERM-01A", r"(?:bắn|quét)\s+(?:Live\s+)?BLAST|bắn\s+chuỗi|chạy\s+bừa", "Khẩu ngữ/tiếng lóng tin sinh; thay bằng 'truy vấn Live BLASTp' hoặc 'đối soát chuỗi'"),
    ("R-TERM-01B", r"căn\s+chỉnh(?:\s+chuỗi|\s+cục\s+bộ)?", "Dịch thô từ alignment; thay bằng 'so khớp chuỗi', 'đối soát chuỗi' hoặc 'gióng hàng'"),
    ("R-TERM-01C", r"tinh\s+tuyển(?:\s+tập\s+dữ\s+liệu)?", "Từ hoa mỹ; thay bằng 'sàng lọc và thẩm định dữ liệu' hoặc 'chuẩn bị dữ liệu'"),
    ("R-TERM-01D", r"vạch\s+trần|bóc\s+trần|phơi\s+bày|dưới\s+vỏ\s+bọc", "Văn phong giật gân; thay bằng 'làm sáng tỏ', 'chỉ ra', 'phát hiện'"),
    ("R-TERM-01E", r"áp\s+đảo(?:\s+hoàn\s+toàn)?|đối\s+đầu\s+trực\s+diện", "Từ thể thao/võ thuật; thay bằng 'vượt trội hơn', 'đạt giá trị cao hơn'"),
    ("R-TERM-01F", r"giải\s+cứu(?:\s+thành\s+công)?|bị\s+bỏ\s+rơi|bỏ\s+rơi\s+nhóm\s+hiếm", "Nhân hóa ủy mị; thay bằng 'khôi phục tính đại diện', 'chưa có đại diện'"),
    ("R-TERM-01G", r"(?:sự\s+)?độc\s+quyền(?:\s+của\s+nhóm\s+lớn)?|hóa\s+giải(?:\s+sự)?\s+độc\s+quyền", "Thuật ngữ kinh tế; thay bằng 'thiên lệch quy mô mẫu', 'tập trung đại diện quá mức'"),
    ("R-TERM-01H", r"(?:tổng\s+|chênh\s+lệch\s+)?quyền\s+lực|giành\s+ghế|thâu\s+tóm", "Nhân hóa chính trị; thay bằng 'tổng trọng số trong hàm mục tiêu', 'tiềm năng đóng góp cận biên'"),
    ("R-TERM-01I", r"bù\s+đắp|bù\s+trừ|gánh\s+vác|cấp\s+đại\s+diện", "Từ hành chính bao cấp; thay bằng 'hiệu chỉnh trọng số', 'tái cân bằng quy mô', 'phạt quy mô nhóm'"),
    ("R-TERM-01J", r"nén\s+mạnh\s+độ\s+dư\s+thừa|ép\s+độ\s+dư\s+thừa", "Từ cơ học sai ngữ cảnh; thay bằng 'giảm đáng kể độ dư thừa'"),
    ("R-TERM-01K", r"hoàn\s+hảo|sửa\s+triệt\s+để|triệt\s+tiêu\s+hoàn\s+toàn\s+sai\s+số|giải\s+quyết\s+dứt\s+điểm", "Vi phạm khiêm tốn nhận thức; thay bằng 'giảm thiểu tối đa sai lệch', 'ngăn chặn nguy cơ'"),
    ("R-TERM-01L", r"cốt\s+tử|chết\s+người|tai\s+hại|vô\s+phương\s+cứu\s+chữa", "Kịch tính hóa giật gân; thay bằng 'điểm mù phương pháp luận trọng yếu', 'hạn chế then chốt'"),
    ("R-TERM-01M", r"bệ\s+phóng(?:\s+lý\s+thuyết|\s+nền\s+tảng)?|bốn\s+trụ\s+cột|ngọn\s+hải\s+đăng", "Ẩn dụ tu từ văn học; thay bằng 'cơ sở lý thuyết nền tảng', 'nội dung nghiên cứu trọng tâm'"),
    ("R-TERM-01N", r"phương\s+pháp\s+hiện\s+hành", "Từ pháp lý - hành chính; thay bằng 'các phương pháp hiện có' hoặc 'truyền thống'"),
    ("R-TERM-01O", r"chứng\s+minh\s+hình\s+thức", "Hàm ý tiêu cực làm màu; thay bằng 'chứng minh toán học chặt chẽ / giải tích'"),
    ("R-TERM-01P", r"dải\s+ngân\s+sách\s+sâu", "Dịch thô gây hiểu nhầm sang tài chính; thay bằng 'khi mở rộng quy mô tập đại diện'"),
    ("R-TERM-01Q", r"truy\s+vấn\s+ngược", "Dịch thô tối nghĩa; thay bằng 'cơ chế bao phủ Within-Subfamily Coverage'"),
    ("R-TERM-01R", r"chú\s+ý\s+tự\s+thân", "Dịch máy thô; thay bằng 'cơ chế tự chú ý Self-Attention'"),
    ("R-STYLE-01", r"\b(?:chúng\s+)?em\b|\bnhóm\s+em\b", "Ngôi kể xưng hô không phù hợp thân bài; thay bằng 'đồ án', 'nghiên cứu', 'phương pháp'"),
    ("R-STYLE-02", r"Nội\s+dung\s+này|Nội\s+dung\s+tiếp\s+theo|Phần\s+này\s+sẽ\s+trình\s+bày", "Câu dẫn sáo rỗng tự quy chiếu; đi thẳng vào phát hiện khoa học (BLUF)"),
]

def lint_line(line_num: int, line_text: str) -> List[Dict[str, Any]]:
    findings = []
    
    # Check lint-allow marker
    if "% lint-allow:" in line_text:
        return findings

    # 1. Master Blacklist Checks
    for rule_id, pattern, msg in BLACKLIST_RULES:
        matches = list(re.finditer(pattern, line_text, re.IGNORECASE))
        for m in matches:
            findings.append({
                "rule_id": rule_id,
                "severity": "MAJOR",
                "line": line_num,
                "quote": m.group(0),
                "message": msg
            })

    # 2. Multipliers in prose ($X\times$)
    m_mult = re.search(r'\$[0-9]+(?:\{,\}[0-9]+)?\\times\$', line_text)
    if m_mult:
        findings.append({
            "rule_id": "R-FMT-03",
            "severity": "MAJOR",
            "line": line_num,
            "quote": m_mult.group(0),
            "message": "Bội số trong văn xuôi phải viết 'gấp X lần', cấm viết '$X\\times$'"
        })

    # 3. Monospace font violations on MEROPS / Subfamily / Fasta
    m_tt = re.search(r'\\texttt\{[^\}]*(?:MEROPS|A01|\.fasta|ESM)[^\}]*\}', line_text)
    if m_tt:
        findings.append({
            "rule_id": "R-FMT-05",
            "severity": "MAJOR",
            "line": line_num,
            "quote": m_tt.group(0),
            "message": "Cấm dùng \\texttt cho tên tệp dữ liệu, nhãn Subfamily hoặc mô hình ESM"
        })

    # 4. Vertical lines in tabular
    if re.search(r'\\begin\{tabular\}\{[^\}]*\|[^\}]*\}', line_text):
        findings.append({
            "rule_id": "R-FMT-01",
            "severity": "BLOCKER",
            "line": line_num,
            "quote": line_text.strip(),
            "message": "Cấm tuyệt đối kẻ đường dọc (|) trong bảng; tuân thủ chuẩn booktabs"
        })

    # 5. Decimal formatting in math ($94,13%$)
    m_dec = re.search(r'\$[^\$]*\b([0-9]+),([0-9]+)\b[^\$]*\$', line_text)
    if m_dec:
        findings.append({
            "rule_id": "R-FMT-02",
            "severity": "MAJOR",
            "line": line_num,
            "quote": f"{m_dec.group(1)},{m_dec.group(2)}",
            "message": "Số thập phân tiếng Việt trong math mode phải bọc trong ngoặc nhọn: '{,}'"
        })

    # 6. Dangling $ (odd number of unescaped $)
    # Count unescaped $
    unescaped_dollar_count = len(re.findall(r'(?<!\\)\$', line_text))
    if unescaped_dollar_count % 2 != 0:
        findings.append({
            "rule_id": "R-FMT-07",
            "severity": "BLOCKER",
            "line": line_num,
            "quote": line_text.strip()[:60],
            "message": f"Số lượng ký tự '$' lẻ ({unescaped_dollar_count}), có nguy cơ thiếu/thừa đóng mở math mode"
        })

    # 7. Over-capitalization in middle of sentence (e.g. "tại Bảng~\ref", "trong Hình~\ref")
    m_mid_cap = re.search(r'\b(?:tại|ở|trong|theo|vào|của|cho)\s+(Bảng|Hình|Công\s+thức)~\s*\\ref', line_text)
    if m_mid_cap:
        findings.append({
            "rule_id": "R-TERM-05",
            "severity": "MINOR",
            "line": line_num,
            "quote": m_mid_cap.group(0),
            "message": f"Từ '{m_mid_cap.group(1)}' đứng giữa câu phải viết thường ('{m_mid_cap.group(1).lower()}')"
        })

    # 8. Parentheses Whitelist Enforcement (R-FMT-08 / Mục 3.1 SSOT)
    # Cấm dùng dấu ngoặc đơn kẹp chữ thông thường (như '(Family A1)', '(ví dụ ...)')
    paren_matches = re.finditer(r'\(([^()]+)\)', line_text)
    for pm in paren_matches:
        inside = pm.group(1).strip()
        # Skip allowed patterns:
        # - Math mode inside: '$...$'
        # - Pure numbers/enumeration: '1', '2', '3', '4', 'a', 'b', 'i', 'ii', 'iii', '1..6'
        # - Acronyms in all-caps: 'PLM', 'MSA', 'BLAST', 'QC', 'BLASTp', 'NCBI', 'PDB'
        # - Table/Figure sub-labels: 'A', 'B', 'C', 'hình~\ref{...}A'
        if '$' in inside or '\\' in inside:
            continue
        if re.match(r'^(?:[0-9]+(?:\.\.[0-9]+)?|[a-z]|[ivxIVX]+|[A-Z])$', inside):
            continue
        if re.match(r'^[A-Z0-9_\-]+(?:\s*--\s*[A-Z0-9_\-]+)?$', inside):
            continue
        # If it contains regular words like "Family A1", "ví dụ", "tức là"
        if re.search(r'[a-zA-ZÀ-ỹ]{2,}', inside):
            # Check if it's an expanded acronym definition: e.g. "Protein Language Model -- PLM"
            if '--' in inside and re.search(r'[A-Z]{2,}', inside):
                continue
            findings.append({
                "rule_id": "R-FMT-08",
                "severity": "MAJOR",
                "line": line_num,
                "quote": pm.group(0),
                "message": "Vi phạm Whitelist dấu ngoặc đơn (Mục 3.1 SSOT); cấm kẹp văn bản thông thường trong ngoặc đơn, hãy viết trực tiếp vào câu văn"
            })

    return findings

def main():
    parser = argparse.ArgumentParser(description="LaTeX Report Linter (Gate 1)")
    parser.add_argument("--file", required=True, help="Path to .tex file")
    parser.add_argument("--start-line", type=int, default=1, help="Start line to check (1-based)")
    parser.add_argument("--end-line", type=int, default=None, help="End line to check (1-based)")
    parser.add_argument("--json", help="Path to output JSON file")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start = max(1, args.start_line)
    end = min(len(lines), args.end_line) if args.end_line else len(lines)

    all_findings = []
    for line_idx in range(start - 1, end):
        line_num = line_idx + 1
        line_findings = lint_line(line_num, lines[line_idx])
        all_findings.extend(line_findings)

    print(f"Linting {args.file} (lines {start} to {end}): Found {len(all_findings)} issue(s).")
    for f in all_findings:
        print(f"  [{f['severity']}] {f['rule_id']} at L{f['line']}: {f['message']} | Quote: \"{f['quote']}\"")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as jf:
            json.dump({"file": args.file, "line_range": [start, end], "total": len(all_findings), "findings": all_findings}, jf, ensure_ascii=False, indent=2)

    return 0 if len(all_findings) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
