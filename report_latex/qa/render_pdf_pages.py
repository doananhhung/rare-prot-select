# -*- coding: utf-8 -*-
"""
Script kết nối tự động render trang PDF sang ảnh PNG (report_latex/qa/render_pdf_pages.py)
Sử dụng công cụ pdftoppm (Poppler/MiKTeX) để phục vụ Agent Thẩm định Thị giác (Visual Inspector).
"""
import sys
import os
import subprocess
import argparse
import json
import glob
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def find_pdftoppm() -> str:
    # 1. Check default MiKTeX path
    miktex_path = r"D:\app\Miktex\miktex\bin\x64\pdftoppm.exe"
    if os.path.exists(miktex_path):
        return miktex_path
    
    # 2. Check PATH
    import shutil
    cmd = shutil.which("pdftoppm")
    if cmd:
        return cmd
        
    raise FileNotFoundError("Không tìm thấy công cụ pdftoppm.exe trên hệ thống!")

def find_default_pdf() -> str:
    candidates = [
        r"d:\programing\project\Topic 2\report_latex\do_an_lien_nganh\main.pdf",
        r"d:\programing\project\Topic 2\report_latex\main.pdf"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("Không tìm thấy tệp main.pdf trong thư mục report_latex!")

def render_pages(pdf_path: str, start_page: int, end_page: int, output_dir: str, dpi: int = 150) -> list:
    pdftoppm = find_pdftoppm()
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean previous snapshots in that range
    prefix = "page"
    
    # pdftoppm arguments
    cmd = [
        pdftoppm,
        "-png",
        "-r", str(dpi),
        "-f", str(start_page),
        "-l", str(end_page),
        pdf_path,
        os.path.join(output_dir, prefix)
    ]
    
    print(f"Đang thực thi: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Lỗi khi chạy pdftoppm:\n{res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
        
    # Collect generated files
    images = []
    for p in range(start_page, end_page + 1):
        # pdftoppm formats names as prefix-01.png or prefix-1.png or prefix-001.png depending on total pages
        matches = glob.glob(os.path.join(output_dir, f"{prefix}*{p}.png"))
        if not matches:
            # Try zero-padded patterns
            matches = glob.glob(os.path.join(output_dir, f"{prefix}*-{p:02d}.png"))
        if not matches:
            matches = glob.glob(os.path.join(output_dir, f"{prefix}*-{p:03d}.png"))
        if matches:
            images.append(matches[0])
            
    return sorted(images)

def main():
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG for Visual Inspector")
    parser.add_argument("--pdf", default=None, help="Đường dẫn tới tệp PDF")
    parser.add_argument("--start-page", type=int, required=True, help="Trang bắt đầu (1-based)")
    parser.add_argument("--end-page", type=int, required=True, help="Trang kết thúc (1-based)")
    parser.add_argument("--dpi", type=int, default=150, help="Độ phân giải DPI (mặc định: 150)")
    parser.add_argument("--output-dir", default=r"d:\programing\project\Topic 2\report_latex\qa\runs\pdf_snapshots", help="Thư mục lưu ảnh")
    parser.add_argument("--json", default=None, help="Tệp JSON lưu danh sách ảnh xuất ra")
    args = parser.parse_args()

    pdf_path = args.pdf if args.pdf else find_default_pdf()
    print(f"Sử dụng PDF: {pdf_path}")
    
    images = render_pages(pdf_path, args.start_page, args.end_page, args.output_dir, args.dpi)
    print(f"Đã xuất bản thành công {len(images)} ảnh trang PDF vào: {args.output_dir}")
    for img in images:
        print(f"  - {img} ({os.path.getsize(img)} bytes)")
        
    if args.json:
        with open(args.json, "w", encoding="utf-8") as jf:
            json.dump({
                "pdf": pdf_path,
                "start_page": args.start_page,
                "end_page": args.end_page,
                "total_images": len(images),
                "images": images
            }, jf, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
