# NGUYÊN TẮC HOẠT ĐỘNG & QUY CHUẨN DỰ ÁN (GEMINI.MD)
## Đề tài 2: Chọn tập protein đại diện có ưu tiên nhóm hiếm bằng tối ưu hóa submodular (RareProtSelect)

---

### 1. NGUỒN SỰ THẬT DUY NHẤT (SINGLE SOURCE OF TRUTH - SSOT)
Toàn bộ dự án được quản lý và định hướng bởi **2 tệp tài liệu trung tâm**:
1. [**`quy_trinh_thuc_hien_va_cac_cong_doan.md`**](./quy_trinh_thuc_hien_va_cac_cong_doan.md): Mô tả tuần tự các công đoạn nghiên cứu khoa học thuần túy (tư duy sinh học, mô hình toán học, đầu vào, logic xử lý, đầu ra, tiêu chí đánh giá), KHÔNG đề cập chi tiết code.
2. [**`thiet_ke_codebase_va_kien_truc_he_thong.md`**](./thiet_ke_codebase_va_kien_truc_he_thong.md): Bản thiết kế kỹ thuật chi tiết của codebase (cấu trúc thư mục, từng file code, class, hàm, tham số, luồng dữ liệu và ma trận truy vết).

> ⚠️ **QUY TẮC BẮT BUỘC KHI SỬA CODE / THAY ĐỔI THIẾT KẾ**:
> * Khi cần thay đổi thuật toán, thêm chức năng hoặc sửa code, **BẮT BUỘC PHẢI CẬP NHẬT TRƯỚC VÀO 2 TỆP MARKDOWN NÀY**.
> * Trong mỗi file code, phần chú thích (Docstring) đầu file **bắt buộc phải ghi rõ: "Thực hiện Công đoạn X.X trong Tài liệu 1 và Module Y trong Tài liệu 2"**.

---

### 2. QUY CHUẨN CẤU TRÚC THƯ MỤC & ĐÓNG GÓI CODE
* **Thư mục gốc `Topic 2/`**: Chỉ lưu trữ các tệp tài liệu nghiên cứu (`.md`, `.pdf`), repo đối chuẩn gốc (`baseline_repo/`) và thư mục dự án con.
* **Thư mục dự án code `RareProtSelect/`**: Toàn bộ codebase Python, môi trường ảo `.venv`, tệp cấu hình `configs/`, mã nguồn `src/`, kịch bản chạy `experiments/`, kết quả `outputs/` và kiểm thử `tests/` **bắt buộc phải nằm gọn bên trong thư mục `RareProtSelect/`**.

---

### 3. QUY CHUẨN PHONG CÁCH GIAO TIẾP & GIẢI THÍCH (BẮT BUỘC)
* **Tuyệt đối KHÔNG kết luận vắn tắt, cụt lủn hay gạch đầu dòng khô khan thiếu bối cảnh**.
* **Luôn giải thích cặn kẽ, trực quan, có ví dụ số liệu và phân tích bản chất cơ chế hoạt động**:
  * *Tại sao phải làm bước này?* (Động lực khoa học & sinh học).
  * *Đầu vào dữ liệu là gì?* (Định dạng, số lượng, nhãn phân họ).
  * *Thuật toán xử lý cụ thể như thế nào từng bước?* (Công thức toán học, cơ chế cập nhật).
  * *Đầu ra và các chỉ số đo lường là gì?* (Ý nghĩa các con số, bảng đối đầu).
* Duy trì văn phong sư phạm, dễ hiểu, logic chặt chẽ tương tự như trong tài liệu `giai_thich_khai_niem.md` và `doc_hieu_topic2_va_bai_bao_nen.md`.

---

### 4. QUY CHUẨN KỸ THUẬT & QUẢN LÝ MÔI TRƯỜNG
* **Trình quản lý gói Python**: Luôn sử dụng công cụ **`uv`** (`D:\uv\bin\uv.exe` hoặc `uv` từ PATH ổ D) trong thư mục `RareProtSelect/` để khởi tạo virtual environment (`.venv`), cài đặt thư viện (`uv pip install`) và chạy mã nguồn (`uv run`).
* **Phiên bản Python**: Sử dụng Python 3.12 (`D:\uv\python\cpython-3.12.13-windows-x86_64-none\python.exe`).
* **Phần cứng GPU & PyTorch**: Sử dụng **`torch==2.11.0+cu130`** và **`torchvision==0.26.0+cu130`** (bản build CUDA 13.0 tương thích tối đa với card đồ họa **NVIDIA GeForce RTX 5060 Laptop GPU** kiến trúc Blackwell sm_120, Driver 595.97 / CUDA 13.2).
* **Thư mục UV Master**: Toàn bộ `bin`, `cache`, `python`, `tools` được quản lý thống nhất tại **`D:\uv\`** (`UV_CACHE_DIR=D:\uv\cache`, `UV_PYTHON_INSTALL_DIR=D:\uv\python`).

* **Thư viện cốt lõi**:
  * Biểu diễn phân tử: `torch`, `fair-esm`, `transformers` để sinh vector nhúng ESM-2.
  * Xử lý sinh học: `biopython` để đọc ghi FASTA, phân tích header.
  * Tối ưu hóa & Đánh giá: `numpy`, `scipy`, `scikit-learn`, `heapq` (Max-Heap cho Lazy Greedy).
  * Trực quan hóa & Báo cáo: `pandas`, `matplotlib`, `seaborn`, `pyyaml`, `tqdm`.

---

### 5. PHÂN ĐỊNH VAI TRÒ ĐỘC LẬP CỦA 3 BỘ DỮ LIỆU THỰC NGHIỆM
**TUYỆT ĐỐI KHÔNG GỘP CHUNG 3 TỆP DỮ LIỆU VÀO NHAU**. Mỗi tệp đóng một vai trò riêng biệt trong bài báo:

1. **`Thioesterases_Sequences.fasta` (737 chuỗi - 27 họ ThYme)**:
   * *Vai trò*: Chạy thử nghiệm nhanh (Pilot) để kiểm tra pipeline, và đối chứng độ khớp với tập đại diện do Chuyên gia sinh học chọn thủ công trong ThYme DB (*Gold Standard Benchmark*).
2. **`MEROPS_A1A.fasta` (13,847 chuỗi - 76 phân họ A01.001 đến A01.098)**:
   * *Vai trò*: **Vũ khí thực nghiệm chủ lực** để chứng minh tính đóng góp của đề tài. Mức độ mất cân bằng cực đoan (từ 339 chuỗi xuống 1 chuỗi) dùng để đo lường bước nhảy vọt của **Worst-Group Coverage**, **Rare Representation Rate**, và **Annotation Transfer Macro-F1**.
3. **`CE.fasta` (12,277 chuỗi - 12 nhóm phụ từ ESTHER)**:
   * *Vai trò*: Kiểm chứng tính tổng quát hóa trên siêu họ enzyme khác và đo đạc chi phí tính toán (**Runtime**, **Peak Memory**) giữa Lazy Greedy và Standard Greedy trên quy mô lớn.