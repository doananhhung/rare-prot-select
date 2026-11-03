# -*- coding: utf-8 -*-
with open(r"d:\programing\project\Topic 2\GEMINI.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Line 82 is index 81 (0-based)
cutoff_idx = -1
for i, line in enumerate(lines):
    if line.startswith("### 7. QUY CHUẨN SOẠN THẢO BÁO CÁO LATEX"):
        cutoff_idx = i
        break

if cutoff_idx != -1:
    new_content = "".join(lines[:cutoff_idx])
    new_content += """### 7. QUY CHUẨN SOẠN THẢO BÁO CÁO LATEX (SSOT ĐỘC QUYỀN)
Toàn bộ quy chuẩn soạn thảo báo cáo LaTeX, cấu trúc văn bản, thuật ngữ học thuật, ma trận chỉ số và quy tắc bảng biểu được quản lý tập trung và duy nhất tại:
👉 [**`report_latex/GEMINI.md`**](./report_latex/GEMINI.md)

Mọi tác vụ liên quan đến tài liệu trong `report_latex/` bắt buộc phải đọc và tuân thủ các quy tắc trong tệp trên cùng các catalog chuyên biệt tại `report_latex/qa/rules/`. Tệp `GEMINI.md` ở thư mục gốc này chỉ chi phối mã nguồn Python và quy trình nghiên cứu khoa học tổng thể của dự án.
"""
    with open(r"d:\programing\project\Topic 2\GEMINI.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS: Cleaned GEMINI.md, new length:", len(new_content.splitlines()))
else:
    print("ERROR: Cutoff heading not found!")
