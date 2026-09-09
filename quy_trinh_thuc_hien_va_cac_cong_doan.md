# TÀI LIỆU 1: QUY TRÌNH THỰC HIỆN & CÁC CÔNG ĐOẠN NGHIÊN CỨU KHOA HỌC
## Đề tài: Chọn tập protein đại diện có ưu tiên nhóm hiếm bằng tối ưu hóa submodular (RareProtSelect)

> 📌 **VAI TRÒ CỦA TÀI LIỆU NÀY (NGUỒN SỰ THẬT DUY NHẤT - SINGLE SOURCE OF TRUTH - SSOT)**:
> * Đây là tài liệu quy định **toàn bộ các công đoạn nghiên cứu khoa học thuần túy** (tư duy sinh học, mô hình toán học, đầu vào, các bước xử lý logic, đầu ra và tiêu chí đánh giá), **hoàn toàn độc lập với chi tiết mã nguồn**.
> * Mọi triển khai kỹ thuật hoặc thay đổi code trong tương lai **bắt buộc phải đối chiếu và tuân thủ đúng quy trình trong tài liệu này**.
> * 🔗 **Liên kết kỹ thuật**: Mỗi công đoạn đều có liên kết trực tiếp sang [**Tài liệu 2: Thiết kế Codebase & Kiến trúc Hệ thống**](./thiet_ke_codebase_va_kien_truc_he_thong.md) để xác định module code chịu trách nhiệm hiện thực hóa.

---

## MỤC LỤC CÁC CÔNG ĐOẠN NGHIÊN CỨU

- [GIAI ĐOẠN 0: Chuẩn bị Môi trường & Quản lý Thư viện Khoa học](#giai-doan-0)
- [GIAI ĐOẠN 1: Thu thập, Thẩm định & Tiền xử lý Dữ liệu Sinh học](#giai-doan-1)
  - [Công đoạn 1.1: Khảo sát & Đọc dữ liệu FASTA](#cong-doan-11)
  - [Công đoạn 1.2: Kiểm soát chất lượng chuỗi (Quality Control)](#cong-doan-12)
  - [Công đoạn 1.3: Trích xuất & Ánh xạ Cấu trúc Phân họ (Subfamily Mapping)](#cong-doan-13)
- [GIAI ĐOẠN 2: Biểu diễn Ngữ nghĩa Phân tử qua Protein Language Model (ESM-2)](#giai-doan-2)
  - [Công đoạn 2.1: Mã hóa Chuỗi Protein thành Vector Tiềm ẩn](#cong-doan-21)
  - [Công đoạn 2.2: Gộp Trung bình (Mean Pooling) & Chuẩn hóa Vector](#cong-doan-22)
  - [Công đoạn 2.3: Cơ chế Lưu đệm Vector (Embedding Caching)](#cong-doan-23)
- [GIAI ĐOẠN 3: Xây dựng Không gian Tương đồng & Trọng số Thích ứng Nhóm Hiếm](#giai-doan-3)
  - [Công đoạn 3.1: Đo lường Độ tương đồng Ngữ nghĩa Cosine không âm](#cong-doan-31)
  - [Công đoạn 3.2: Tính toán Trọng số Thích ứng Nhóm hiếm (Rare-Aware Weighting)](#cong-doan-32)
- [GIAI ĐOẠN 4: Tối ưu hóa Tập con Đại diện Submodular (RareProtSelect)](#giai-doan-4)
  - [Công đoạn 4.1: Xây dựng Hàm Mục tiêu Weighted Facility Location (WFL)](#cong-doan-41)
  - [Công đoạn 4.2: Tối ưu hóa Tham lam Tăng tốc (Lazy Greedy qua Max-Heap)](#cong-doan-42)
  - [Công đoạn 4.3: Tối ưu hóa Tham lam Chuẩn (Standard Greedy Baseline)](#cong-doan-43)
  - [Công đoạn 4.4: Thiết lập Dải Ngân sách Khảo sát (Budget Spectrum $k$)](#cong-doan-44)
- [GIAI ĐOẠN 5: Khung Đánh giá Thực nghiệm Đa tầng & Độc lập](#giai-doan-5)
  - [Công đoạn 5.1: Đánh giá Độ bao phủ & Tính Tinh gọn Nội tại (Intrinsic Metrics)](#cong-doan-51)
  - [Công đoạn 5.2: Đánh giá Tác vụ Chuyển giao Nhãn Hạ nguồn (1-NN Annotation Transfer)](#cong-doan-52)
  - [Công đoạn 5.3: Đo lường Chi phí Tài nguyên & Khả năng Mở rộng (Computational Scalability)](#cong-doan-53)
- [GIAI ĐOẠN 6: Khảo sát Bóc tách Thành phần (Ablation Studies)](#giai-doan-6)
- [GIAI ĐOẠN 7: Thực nghiệm Độc lập trên 3 Bộ Dữ liệu & Xuất Báo cáo Khoa học](#giai-doan-7)
  - [Công đoạn 7.1: Thử nghiệm Nhanh Pilot trên 27 họ Thioesterase (TE)](#cong-doan-71)
  - [Công đoạn 7.2: Thực nghiệm Trọng tâm Đột phá Nhóm hiếm trên Peptidase A1 (A1A)](#cong-doan-72)
  - [Công đoạn 7.3: Thực nghiệm Tổng quát hóa & Hiệu năng trên Carboxylesterase (CE)](#cong-doan-73)

---

<a id="giai-doan-0"></a>
## GIAI ĐOẠN 0: Chuẩn bị Môi trường & Quản lý Thư viện Khoa học

### Mục tiêu:
Thiết lập môi trường tính toán khoa học có khả năng tái lập 100%, bảo đảm tương thích với GPU/CPU, đồng bộ toàn bộ phiên bản thư viện lõi và quản lý phụ thuộc độc lập, không làm ảnh hưởng hệ điều hành.

* **Cơ sở kỹ thuật**:
  * Sử dụng công cụ quản lý gói thế hệ mới **`uv`** để tối ưu hóa tốc độ phân giải phụ thuộc và cô lập môi trường ảo `.venv`.
  * Phiên bản Python nền tảng: **Python 3.12**.
* **Đầu vào**: Tệp khai báo phụ thuộc `pyproject.toml` hoặc `requirements.txt`.
* **Đầu ra**: Môi trường `.venv` hoàn chỉnh chứa đầy đủ PyTorch, Transformers/Fair-ESM, BioPython, Scikit-learn, SciPy, Pandas, Matplotlib, Seaborn.
* 🔗 **Hiện thực hóa tại**: [Mục 2.1 - Quản lý Môi trường trong Tài liệu 2](./thiet_ke_codebase_va_kien_truc_he_thong.md#sec-env)

---

<a id="giai-doan-1"></a>
## GIAI ĐOẠN 1: Thu thập, Thẩm định & Tiền xử lý Dữ liệu Sinh học

```
[ Tệp FASTA Thô ] ──► [ 1.1 Đọc Chuỗi & Header ] ──► [ 1.2 Lọc Chuỗi Rác/Lỗi ] ──► [ 1.3 Tách & Ánh Xạ Nhóm Hiếm ]
```

<a id="cong-doan-11"></a>
### Công đoạn 1.1: Khảo sát & Đọc dữ liệu FASTA

#### a. Mục tiêu khoa học:
Nạp chính xác chuỗi amino acid và các thông tin sinh học trong dòng tiêu đề (*header*) của 3 bộ dữ liệu chuẩn (`Thioesterases`, `MEROPS_A1A`, `CE`), chuyển đổi từ dạng văn bản thô phân mảnh sang cấu trúc dữ liệu bộ nhớ có cấu trúc chuẩn hóa, phục vụ cho mô hình ngôn ngữ protein (ESM-2) và thuật toán tối ưu.

#### b. Dữ liệu thô thực tế trong tệp FASTA đang có dạng như thế nào?
Trong các tệp dữ liệu thực tế (`.fasta`), mỗi protein được biểu diễn dưới dạng văn bản gồm **2 phần hỗn độn**:
1. **Dòng Header (bắt đầu bằng `>`)**: Nhồi nhét rất nhiều thông tin phức tạp chưa được phân tách (Mã protein, Tên chức năng, Tên sinh vật, và Mã phân họ).
2. **Các dòng Sequence (chuỗi amino acid)**: Bị ngắt dòng tự động sau mỗi 60-80 ký tự (chứa các ký tự ngắt dòng `\n`, `\r`, khoảng trắng hoặc chữ thường).

##### 🧪 Ví dụ dữ liệu thực tế trích xuất từ 3 tệp của bài báo:

* **Từ tệp `MEROPS_A1A.fasta`**:
  ```text
  >MER0000885 - pepsin A (Homo sapiens) [A01.001]#A01A#{peptidase unit: 63-388}~source PEPA_HUMAN~
  MKWLLLLGLVALSECIMYKVPLIRKKSLRRTLSERGLLKDFLKKHNLNPARKYFPQWEAP
  TLVDEQPLENYLDMEYFGTIGIGTPAQDFTVIFDTGSSNLWVPSVYCSSLACTTNHNRFN
  PQDSSTYEETSRTLSITYGTGSMTGI...
  ```

* **Từ tệp `Thioesterases_Sequences.fasta`**:
  ```text
  >sp|G8JVR4| Ethanol acetyltransferase 1 OS=Eremothecium cymbalariae DBVPG#7215 OX=931890 GN=EAT1 PE=1 SV=1
  MPPTLNLQEKQLLAKRRNKLIKKLQIKLKKTKTTTTPTTAAPAAAPTATVTATVTATVTA
  SVATSSSTTVTSAPTSTVTTSPTTVSSAPTSTPTTSSPPTTTTTTTTTTTTTTTTTTTTT
  ...VKL
  ```

* **Từ tệp `CE.fasta`**:
  ```text
  >9acar-l7m799 /F12/ Rhipicephalus pulchellus (zebra tick); Rhipicephalus appendiculatus (Brown ear tick); Hyalomma excavatum Putative esterase
  MNKLLLLLLVGAAVCAESKEEETVRVQGPLTGIRGYKGYTINAKEKGPVFGFQGIPFAQP
  PVGELRFKAPEPPEPWKGVRDATTYGPICPQSEHLLGRLANVTLGGDEECLYLNIWVPPA
  ...
  ```

#### c. Tại sao BẮT BUỘC phải bóc tách thành `{id, sequence, header, length}`?
Việc chuyển đổi dữ liệu thô sang cấu trúc 4 trường thông tin chuẩn hóa xuất phát từ 4 yêu cầu kỹ thuật & khoa học cốt tử:

1. **Khắc phục hiện tượng phân mảnh chuỗi (De-wrapping Sequence)**:
   * Mô hình ESM-2 yêu cầu đầu vào là **một chuỗi amino acid duy nhất, liên tục và thuần khiết** (ví dụ: `"MKWLLLLGLVAL..."`).
   * Nếu không nối các dòng bị ngắt và không loại bỏ dấu xuống dòng `\n`, mô hình Transformer sẽ xử lý sai toàn bộ ngữ cảnh peptide.
2. **Tách riêng Định danh duy nhất (`id`) làm Khóa chính**:
   * Cần trích xuất mã ID duy nhất (như `"MER0000885"`, `"G8JVR4"`, `"9acar-l7m799"`) để làm định danh khóa chính truy vết xuyên suốt từ đầu vào, vector nhúng, chỉ số ma trận đến danh sách tập đại diện $S$.
3. **Lưu giữ Dòng tiêu đề gốc (`header`) để Khai phá Nhãn phân họ**:
   * Dòng header chứa thông tin phân loại quan trọng (ví dụ mã `[A01.001]` hay `/F12/`). Giữ lại `header` nguyên bản để chuyển giao cho [Công đoạn 1.3](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-13) bóc tách nhãn phân họ và phân nhóm hiếm.
4. **Xác định Độ dài Chuỗi (`length`) để Phục vụ Lọc QC & Tối ưu GPU**:
   * Biết chính xác số lượng amino acid $L_v$ giúp [Công đoạn 1.2](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-12) lọc bỏ chuỗi quá ngắn/quá dài.
   * Đồng thời giúp mô hình ESM-2 gom các chuỗi có độ dài tương đương vào cùng một Batch xử lý trên GPU RTX 5060 (*Dynamic Batching*), tránh lãng phí bộ nhớ VRAM.

#### d. Cấu trúc đối tượng chuẩn hóa đầu ra sau khi xử lý:
Mỗi chuỗi protein sau khi quét qua bộ Parser sẽ trở thành một đối tượng tiêu chuẩn:
```python
ProteinRecord(
    id = "MER0000885",
    sequence = "MKWLLLLGLVALSECIMYKVPLIRKKSLRRTLSERGLLKDFLKKHNLNPARKYFPQWEAPTLVDEQPL...",
    header = ">MER0000885 - pepsin A (Homo sapiens) [A01.001]#A01A#{peptidase unit: 63-388}~source PEPA_HUMAN~",
    length = 388
)
```

* 🔗 **Hiện thực hóa tại**: [Module `RareProtSelect/src/data/fasta_parser.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#fasta-parser)

---

<a id="cong-doan-12"></a>
### Công đoạn 1.2: Kiểm soát chất lượng chuỗi (Quality Control)
* **Mục tiêu khoa học**: Loại bỏ các chuỗi rác, đoạn phân mảnh quá ngắn, chuỗi quá dài bất thường hoặc chứa nhiều ký tự amino acid không xác định để tránh làm méo mó mô hình ngôn ngữ và thuật toán tối ưu.
* **Động lực sinh học**: Các ký tự mơ hồ như `X` (axit amin bất kỳ), `B` (Asp/Asn), `Z` (Glu/Gln), `J` (Leu/Ile) hoặc dấu `*` (mã dừng) xuất hiện với tỷ lệ cao phản ánh chất lượng giải trình tự kém.
* **Tiêu chí lọc chuẩn mực**:
  1. **Độ dài hợp lệ**: Giữ lại các chuỗi có độ dài $L \in [30, 2000]$ amino acid (loại bỏ peptide quá ngắn $<30$ hoặc chuỗi ngoại lai $>2000$).
  2. **Tỷ lệ ký tự không hợp lệ**: Tỷ lệ ký tự không thuộc 20 axit amin tiêu chuẩn (`A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y`) phải $\le 5\%$.
  3. **Khử trùng lặp hoàn toàn**: Nếu có 2 chuỗi trùng lặp $100\%$ cả ID lẫn chuỗi axit amin, chỉ giữ lại 1 bản ghi duy nhất.
* **Đầu ra**: Tập hợp protein sạch đã qua kiểm định (*Cleaned Ground Set $V$*) và Báo cáo kiểm định chất lượng (*QC Summary Report*).
* 🔗 **Hiện thực hóa tại**: [Module `src/data/quality_filter.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#quality-filter)

---

<a id="cong-doan-13"></a>
### Công đoạn 1.3: Trích xuất & Ánh xạ Cấu trúc Phân họ (Subfamily Mapping)
* **Mục tiêu khoa học**: Xác định chính xác nhãn phân loại/phân họ $g(v) \in G$ cho từng protein $v \in V$ và thống kê kích thước từng phân họ $n_g = |g|$ để phục vụ tính toán trọng số thích ứng nhóm hiếm.
* **Quy trình xử lý logic cho từng bộ dữ liệu**:
  1. **Bộ MEROPS A1A**: Phân tích biểu thức chính quy trích xuất mã phân họ trong ngoặc vuông (ví dụ `[A01.001]`, `[A01.002]`, ..., `[A01.098]`). Phân loại thành:
     * Nhóm lớn (*Major subfamilies*): $n_g \ge 20$ chuỗi.
     * Nhóm trung bình (*Medium subfamilies*): $5 < n_g < 20$ chuỗi.
     * Nhóm hiếm (*Rare/Long-tail subfamilies*): $n_g \le 5$ chuỗi (đặc biệt là các nhóm có $n_g = 1$).
  2. **Bộ CE (Carboxylesterase)**: Trích xuất mã nhóm phân loại phụ (ví dụ `/F85/`, `/F15/`, `/F12/`, ..., `/F208/`).
  3. **Bộ Thioesterase (TE)**: Đối chiếu mã UniProt Accession với bảng phân loại 27 họ TE chuẩn của ThYme Database.
* **Đầu ra**: Bảng ánh xạ nhãn `{protein_id -> subfamily_label}`, từ điển kích thước `{subfamily_label -> count}`, và danh sách định danh nhóm hiếm $G_{\text{rare}}$.
* 🔗 **Hiện thực hóa tại**: [Module `src/data/annotation_mapper.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#annotation-mapper)

---

<a id="giai-doan-2"></a>
## GIAI ĐOẠN 2: Biểu diễn Ngữ nghĩa Phân tử qua Protein Language Model (ESM-2)

```
Chuỗi Axit Amin (x) ──► [ ESM-2 Transformer ] ──► [ Hidden States H ] ──► [ Mean Pooling ] ──► [ Chuẩn Hóa L2 ] ──► Vector z(v)
```

<a id="cong-doan-21"></a>
### Công đoạn 2.1: Mã hóa Chuỗi Protein thành Vector Tiềm ẩn
* **Mục tiêu khoa học**: Chuyển đổi chuỗi ký tự amino acid thành các biểu diễn ngữ cảnh sinh học sâu (nắm bắt cấu trúc bậc 3, túi xúc tác và quan hệ tiến hóa xa mà BLAST không thể thấy).
* **Cơ sở mô hình**: Sử dụng mô hình ESM-2 tiền huấn luyện (`esm2_t12_35M_UR50D` với số chiều $d=480$, hoặc `esm2_t30_150M_UR50D` với $d=640$).
* **Quy trình xử lý logic**:
  1. Tokenize chuỗi protein, bổ sung các token đặc biệt `<cls>` ở đầu và `<eos>` ở cuối.
  2. Đưa qua các tầng Transformer Attention của ESM-2 ở chế độ Inference (`torch.no_grad()`).
  3. Trích xuất ma trận trạng thái ẩn ở tầng cuối cùng: $\mathbf{H}^{(v)} \in \mathbb{R}^{L_v \times d}$.
* **Đầu ra**: Tensor biểu diễn không gian tiềm ẩn của các residue trong chuỗi.
* 🔗 **Hiện thực hóa tại**: [Module `src/embeddings/esm_embedder.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#esm-embedder)

---

<a id="cong-doan-22"></a>
### Công đoạn 2.2: Gộp Trung bình (Mean Pooling) & Chuẩn hóa Vector
* **Mục tiêu khoa học**: Nén ma trận kích thước biến thiên $\mathbf{H}^{(v)} \in \mathbb{R}^{L_v \times d}$ thành một vector đặc trưng duy nhất có độ dài cố định $z(v) \in \mathbb{R}^d$ đại diện cho toàn bộ phân tử protein.
* **Công thức toán học**:
  1. **Mean Pooling** qua toàn bộ chiều dài chuỗi (loại bỏ vị trí của `<cls>` và `<eos>`):
     $$z(v) = \frac{1}{L_v} \sum_{i=1}^{L_v} \mathbf{H}^{(v)}_{i, :} \in \mathbb{R}^d$$
  2. **Chuẩn hóa $\ell_2$-norm**:
     $$\hat{z}(v) = \frac{z(v)}{\|z(v)\|_2} = \frac{z(v)}{\sqrt{\sum_{j=1}^d z_j(v)^2}}$$
* **Ý nghĩa toán học**: Sau khi chuẩn hóa $\ell_2$, tích vô hướng giữa hai vector $\hat{z}(u)^\top \hat{z}(v)$ chính là Cosine Similarity, giúp việc tính toán tương đồng trở nên cực kỳ nhanh chóng và ổn định.
* 🔗 **Hiện thực hóa tại**: [Module `src/embeddings/esm_embedder.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#esm-embedder)

---

<a id="cong-doan-23"></a>
### Công đoạn 2.3: Cơ chế Lưu đệm Vector (Embedding Caching)
* **Mục tiêu khoa học**: Đảm bảo tính tái lập và tối ưu hóa thời gian tính toán — chỉ sinh vector nhúng một lần duy nhất, lưu xuống đĩa để các thực nghiệm tối ưu và đánh giá sau này có thể tải lại tức thì trong $0.1$ giây.
* **Cơ chế lưu trữ**: Lưu trữ dưới dạng mảng nhị phân nén NumPy (`.npy`) hoặc PyTorch (`.pt`) kèm tệp JSON lưu danh sách ID và metadata tương ứng.
* **Đầu ra**: Tệp đệm `outputs/embeddings_cache/{dataset_name}_{model_name}.npy`.
* 🔗 **Hiện thực hóa tại**: [Module `src/embeddings/cache_manager.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#cache-manager)

---

<a id="giai-doan-3"></a>
## GIAI ĐOẠN 3: Xây dựng Không gian Tương đồng & Trọng số Thích ứng Nhóm Hiếm

<a id="cong-doan-31"></a>
### Công đoạn 3.1: Đo lường Độ tương đồng Ngữ nghĩa Cosine không âm
* **Mục tiêu khoa học**: Tạo ma trận đo lường khoảng cách sinh học/ngữ nghĩa $\mathbf{Sim} \in \mathbb{R}^{n \times n}$ giữa mọi cặp protein trong Ground Set $V$.
* **Công thức toán học**:
  $$\operatorname{sim}_{PLM}(u, v) = \max\left(0, \cos(z(u), z(v))\right) = \max\left(0, \hat{z}(u)^\top \hat{z}(v)\right)$$
* **Tính chất bắt buộc**:
  * Không âm: $\operatorname{sim}(u, v) \ge 0$ (điều kiện tiên quyết để hàm Facility Location giữ tính đơn điệu Monotone Submodular).
  * Đối xứng: $\operatorname{sim}(u, v) = \operatorname{sim}(v, u)$.
  * Đường chéo chính: $\operatorname{sim}(v, v) = 1.0$.
* 🔗 **Hiện thực hóa tại**: [Module `src/similarity/dense_similarity.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#dense-similarity)

---

<a id="cong-doan-32"></a>
### Công đoạn 3.2: Tính toán Trọng số Thích ứng Nhóm hiếm (Rare-Aware Weighting)
* **Mục tiêu khoa học**: Khuếch đại lực kéo toán học cho các phân họ nhỏ/hiếm, ngăn chặn việc thuật toán tối ưu dồn toàn bộ ngân sách đại diện cho nhóm chiếm số đông.
* **Hàm trọng số chuẩn của Đề tài (Inverse Square Root)**:
  $$w_v = \frac{1}{\sqrt{n_{g(v)}}}$$
* **Các biến thể trọng số dùng để bóc tách đối chứng (Ablation schemes)**:
  1. **Không trọng số (Unweighted - Baseline Nguyen et al., 2025)**: $w_v = 1$ (hoặc $1/|V|$).
  2. **Nghịch đảo quy mô thuần (Inverse Frequency)**: $w_v = \frac{1}{n_{g(v)}}$.
  3. **Dạng lũy thừa tổng quát**: $w_v = \frac{1}{(n_{g(v)})^\alpha}$ với $\alpha \in [0, 1]$.
* **Đầu ra**: Vector trọng số $\mathbf{w} \in \mathbb{R}^n$ gán cho từng phần tử $v_i \in V$.
* 🔗 **Hiện thực hóa tại**: [Module `src/weighting/rare_weighting.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#rare-weighting)

---

<a id="giai-doan-4"></a>
## GIAI ĐOẠN 4: Tối ưu hóa Tập con Đại diện Submodular (RareProtSelect)

```
Khởi tạo: S_0 = ∅, Max-Heap chứa Gain ban đầu
  │
  ▼
Vòng lặp t = 1 ... k:
  1. Rút đỉnh Max-Heap (protein e)
  2. Tính lại Gain mới: ΔF(e | S_{t-1})
  3. Nếu ΔF_mới >= đỉnh kế tiếp ──► CHỐT e vào S_t (Bỏ qua các ứng viên khác)
  4. Nếu không ──► Cập nhật Gain và đẩy lại vào Heap
  │
  ▼
Đầu ra: Tập đại diện S_k (Chính xác 100% giống Standard Greedy, tốc độ nhanh hơn hàng trăm lần)
```

<a id="cong-doan-41"></a>
### Công đoạn 4.1: Xây dựng Hàm Mục tiêu Weighted Facility Location (WFL)
* **Mục tiêu khoa học**: Định lượng hóa tổng độ bao phủ có trọng số của toàn bộ họ protein $V$ bởi tập đại diện $S \subseteq V$:
  $$F(S) = \sum_{v \in V} w_v \max_{s \in S} \operatorname{sim}_{PLM}(v, s)$$
* **Bảo đảm toán học**: Hàm $F(S)$ đã được chứng minh là chuẩn hóa $F(\emptyset)=0$, đơn điệu tăng và submodular, đảm bảo cận dưới nghiệm $(1 - 1/e) \approx 63.2\%$.
* 🔗 **Hiện thực hóa tại**: [Module `src/selection/lazy_greedy.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#lazy-greedy-code)

---

<a id="cong-doan-42"></a>
### Công đoạn 4.2: Tối ưu hóa Tham lam Tăng tốc (Lazy Greedy qua Max-Heap)
* **Mục tiêu khoa học**: Tìm tập đại diện $S$ kích thước $k$ tối ưu hóa $F(S)$ với thời gian thực thi nhanh nhất mà không làm giảm dù chỉ $0.001\%$ chất lượng nghiệm.
* **Cơ chế hoạt động**:
  1. Duy trì mảng `current_max_sim[v]` lưu khoảng cách lớn nhất hiện tại từ protein $v$ đến tập $S$.
  2. Sử dụng Hàng đợi ưu tiên cực đại (**Max-Heap**) lưu các bộ giá trị `(-marginal_gain, protein_id, last_updated_step)`.
  3. Ở mỗi bước, lấy đỉnh Heap ra kiểm tra. Dựa vào tính chất Lợi ích biên giảm dần (*Submodularity*), nếu Gain sau khi cập nhật của đỉnh vẫn lớn hơn hoặc bằng Gain cũ của phần tử thứ hai, kết luận ngay đây là phần tử tốt nhất toàn cục mà không cần tính lại hàng nghìn ứng viên còn lại.
* **Đầu ra**: Tập đại diện $S_{\text{lazy}} \subseteq V$ kèm nhật ký Lợi ích biên tích lũy qua từng bước.
* 🔗 **Hiện thực hóa tại**: [Module `src/selection/lazy_greedy.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#lazy-greedy-code)

---

<a id="cong-doan-43"></a>
### Công đoạn 4.3: Tối ưu hóa Tham lam Chuẩn (Standard Greedy Baseline)
* **Mục tiêu khoa học**: Cài đặt thuật toán Standard Greedy nguyên bản của bài báo nền (*Nguyen et al., 2025*) để làm mốc đối chứng $1-1$ về cả chất lượng nghiệm lẫn thời gian chạy.
* 🔗 **Hiện thực hóa tại**: [Module `src/selection/standard_greedy.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#standard-greedy-code)

---

<a id="cong-doan-44"></a>
### Công đoạn 4.4: Thiết lập Dải Ngân sách Khảo sát (Budget Spectrum $k$)
* **Mục tiêu khoa học**: Khảo sát đường cong hành vi của thuật toán khi ngân sách $k$ biến thiên từ rất nhỏ đến đủ lớn.
* **Các mốc ngân sách chuẩn mực**:
  * Tập TE ($737$ chuỗi): $k \in [1, 2, 4, 6, 8, 10, 15, 20]$.
  * Tập A1A ($13,847$ chuỗi): $k \in [5, 10, 20, 50, 100, 200, 400, 600]$.
  * Tập CE ($12,277$ chuỗi): $k \in [5, 10, 20, 50, 100, 200, 500]$.
* 🔗 **Hiện thực hóa tại**: [Module `experiments/run_core_merops.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#exp-merops)

---

<a id="giai-doan-5"></a>
## GIAI ĐOẠN 5: Khung Đánh giá Thực nghiệm Đa tầng & Độc lập

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        3 TẦNG ĐÁNH GIÁ KHOA HỌC CHẶT CHẼ                               │
├──────────────────────────────┬──────────────────────────────┬──────────────────────────┤
│ TẦNG 1: NỘI TẠI (Intrinsic)  │ TẦNG 2: HẠ NGUỒN (Extrinsic) │ TẦNG 3: HIỆU NĂNG TÍNH   │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────┤
│ • Overall Coverage           │ • 1-NN Annotation Transfer   │ • Thời gian chạy (s)     │
│ • Macro Coverage             │ • Macro-F1 (Tất cả các lớp)  │ • Bộ nhớ đỉnh (Peak RAM) │
│ • Worst-Group Coverage       │ • Per-Class Recall           │ • Tốc độ tăng tốc (Speed)│
│ • Rare Representation Rate   │                              │                          │
│ • Pairwise Redundancy        │                              │                          │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────┘
```

<a id="cong-doan-51"></a>
### Công đoạn 5.1: Đánh giá Độ bao phủ & Tính Tinh gọn Nội tại (Intrinsic Metrics)
* **Mục tiêu khoa học**: Đo lường khả năng đại diện không gian và mức độ công bằng giữa các nhóm:
  1. **Độ bao phủ của từng phân họ $g$**:
     $$\operatorname{Coverage}(g) = \frac{1}{|g|} \sum_{v \in g} \max_{s \in S} \operatorname{sim}(v, s)$$
  2. **Độ bao phủ toàn họ (Overall Coverage)**: $\text{Cov}_{\text{overall}} = \frac{1}{|V|} \sum_{v \in V} \max_{s \in S} \operatorname{sim}(v, s)$ (Kỳ vọng: Không giảm quá $1\% - 2\%$).
  3. **Độ bao phủ trung bình đều qua các phân họ (Macro Coverage)**: $\text{Cov}_{\text{macro}} = \frac{1}{|G|} \sum_{g \in G} \operatorname{Coverage}(g)$ (Kỳ vọng: Tăng $10\% - 25\%$).
  4. **Độ bao phủ của phân họ thiệt thòi nhất (Worst-Group Coverage - TRỌNG TÂM)**: $\text{Cov}_{\text{worst}} = \min_{g \in G} \operatorname{Coverage}(g)$ (Kỳ vọng: Tăng từ $0\% \rightarrow >60\%$).
  5. **Tỷ lệ nhóm hiếm có đại diện thực thể (Rare Group Representation Rate)**: $\text{RR}_{\text{rare}} = \frac{|\{g \in G_{\text{rare}} \mid S \cap g \neq \emptyset\}|}{|G_{\text{rare}}|}$ (Kỳ vọng: Đạt $\ge 80\% - 100\%$).
  6. **Độ dư thừa nội bộ (Pairwise Redundancy)**: $\text{Red}(S) = \frac{1}{\binom{k}{2}} \sum_{s_i, s_j \in S, i<j} \operatorname{sim}(s_i, s_j)$ (Kỳ vọng: Duy trì ở mức thấp).
* 🔗 **Hiện thực hóa tại**: [Module `src/evaluation/intrinsic_metrics.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#intrinsic-metrics)

---

<a id="cong-doan-52"></a>
### Công đoạn 5.2: Đánh giá Tác vụ Chuyển giao Nhãn Hạ nguồn (1-NN Annotation Transfer)
* **Mục tiêu khoa học**: Chứng minh giá trị ứng dụng sinh học thực tiễn — dùng tập $S$ để gán nhãn cho các protein chưa biết trong $V \setminus S$.
* **Quy trình logic**:
  1. Với mỗi $v \in V \setminus S$, tìm đại diện gần nhất $s^* = \arg\max_{s \in S} \operatorname{sim}(v, s)$ và gán nhãn dự đoán $\hat{y}(v) = y(s^*)$.
  2. Xây dựng ma trận nhầm lẫn đa lớp (*Confusion Matrix*), tính $F1_g$ cho từng phân họ $g$.
  3. Tính **Annotation Transfer Macro-F1** ($\frac{1}{|G|}\sum F1_g$).
* 🔗 **Hiện thực hóa tại**: [Module `src/evaluation/annotation_transfer.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#annotation-transfer-code)

---

<a id="cong-doan-53"></a>
### Công đoạn 5.3: Đo lường Chi phí Tài nguyên & Khả năng Mở rộng (Computational Scalability)
* **Mục tiêu khoa học**: Đo lường Thời gian thực thi (**Runtime**) bằng `time.perf_counter()` và Bộ nhớ đỉnh (**Peak Memory**) bằng `tracemalloc` / `torch.cuda.max_memory_allocated()`.
* 🔗 **Hiện thực hóa tại**: [Module `src/utils/timer.py` & `src/utils/memory_tracker.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#utils-code)

---

<a id="giai-doan-6"></a>
## GIAI ĐOẠN 6: Khảo sát Bóc tách Thành phần (Ablation Studies)

Để bảo đảm tính chặt chẽ tuyệt đối, tiến hành 4 thực nghiệm bóc tách:
1. **Ablation 1 (Biểu diễn phân tử)**: So sánh trực tiếp BLAST Sequence Identity vs. ESM-2 Embeddings trên cùng hàm mục tiêu Unweighted.
2. **Ablation 2 (Hàm trọng số)**: So sánh 3 lựa chọn $\alpha = 0$ (Unweighted), $\alpha = 0.5$ ($1/\sqrt{n_g}$), và $\alpha = 1.0$ ($1/n_g$).
3. **Ablation 3 (Kích thước PLM)**: So sánh ESM-2 35M vs. ESM-2 150M.
4. **Ablation 4 (Thuật toán đối chuẩn Baselines)**: So sánh đối đầu với Random Selection, CD-HIT, MMseqs2, K-Medoids, Unweighted BLAST FL (Paper 2025).
* 🔗 **Hiện thực hóa tại**: [Module `experiments/run_ablation_all.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#exp-ablation)

---

<a id="giai-doan-7"></a>
## GIAI ĐOẠN 7: Thực nghiệm Độc lập trên 3 Bộ Dữ liệu & Xuất Báo cáo Khoa học

<a id="cong-doan-71"></a>
### Công đoạn 7.1: Thử nghiệm Nhanh Pilot trên 27 họ Thioesterase (TE)
* **Mục tiêu**: Xác thực pipeline, tính toán độ trùng khớp $\text{Identity}(S_{\text{algo}}, S_{\text{expert}})$ với tập chuẩn chuyên gia ThYme.
* 🔗 **Hiện thực hóa tại**: [Module `experiments/run_pilot_thyme.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#exp-thyme)

<a id="cong-doan-72"></a>
### Công đoạn 7.2: Thực nghiệm Trọng tâm Đột phá Nhóm hiếm trên Peptidase A1 (A1A)
* **Mục tiêu**: Thu thập các bảng số liệu chính của bài báo về bước nhảy vọt của Worst-Group Coverage và Macro-F1 trên 76 phân họ MEROPS.
* 🔗 **Hiện thực hóa tại**: [Module `experiments/run_core_merops.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#exp-merops)

<a id="cong-doan-73"></a>
### Công đoạn 7.3: Thực nghiệm Tổng quát hóa & Hiệu năng trên Carboxylesterase (CE)
* **Mục tiêu**: Khẳng định tính tổng quát trên 12,277 chuỗi Esterase và chứng minh độ tăng tốc $>100\times - 500\times$ của Lazy Greedy.
* 🔗 **Hiện thực hóa tại**: [Module `experiments/run_scalability_ce.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#exp-ce)