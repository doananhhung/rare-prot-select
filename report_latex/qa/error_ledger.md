# SỔ GHI NHẬN LỖI LỌT & PHÂN TÍCH NGUYÊN NHÂN (ERROR LEDGER)
## Đề tài 2: RareProtSelect

Mỗi khi người dùng phát hiện một lỗi lọt qua tại Cổng 3, bản ghi bắt buộc phải được tạo trong tệp này, phân loại nguyên nhân và liên kết với một Detector chạy lại được.

---

### [ESC-01] Lỗi đóng mở ngoặc đơn kẹp tên phân loại MEROPS
- **Thời gian**: 27/10/2026.
- **Vị trí**: `report_latex/contents/sections/03_chapter_3_experiments.tex` dòng 15.
- **Câu sai nguyên văn**:
  > `Tập dữ liệu thực nghiệm trọng tâm của đề tài là họ Peptidase A1 (Family A1) trích xuất từ cơ sở dữ liệu MEROPS...`
- **Câu chuẩn hóa**:
  > `Tập dữ liệu thực nghiệm trọng tâm của đề tài là Family Peptidase A1 trích xuất từ cơ sở dữ liệu MEROPS...`
- **Phân loại nguyên nhân (Escape Analysis)**:
  * Lớp lỗi: **Lớp E/F (Reviewer gợi ý sai / Linter thiếu luật)**.
  * *Tại Cổng 2*: Reviewer Terminology bắt lỗi "siêu họ" nhưng lại gợi ý Writer ghép tiếng Việt và tiếng Anh kèm ngoặc đơn `(Family A1)`.
  * *Tại Cổng 1*: Script `lint_report.py` chưa có detector kiểm tra Whitelist dấu ngoặc đơn.
- **Hành động chuyển đổi thành Detector**:
  * Mã luật mới: **`R-FMT-08`** (Parentheses Whitelist Enforcement) trong `report_latex/qa/lint_report.py`.
  * Mã quy chuẩn bổ sung: **`R-TERM-02B`** trong `report_latex/qa/rules/R-TERM.md`.
  * Kết quả probe: Script đã bắt thành công `('R-FMT-08', '(Family A1)')` trên chuỗi thử nghiệm.
