# TÀI LIỆU 2: THIẾT KẾ CODEBASE & KIẾN TRÚC HỆ THỐNG PHẦN MỀM
## Đề tài: Chọn tập protein đại diện có ưu tiên nhóm hiếm bằng tối ưu hóa submodular (RareProtSelect)

> 📌 **VAI TRÒ CỦA TÀI LIỆU NÀY (BẢN THIẾT KẾ KỸ THUẬT & NGUỒN SỰ THẬT DUY NHẤT - SSOT)**:
> * Đây là tài liệu quy định **kiến trúc phần mềm, cấu trúc thư mục, thiết kế chi tiết từng tệp mã nguồn (class, hàm, tham số, kiểu dữ liệu)** để hiện thực hóa toàn bộ các công đoạn nghiên cứu trong [**Tài liệu 1: Quy trình thực hiện & Các công đoạn nghiên cứu**](./quy_trinh_thuc_hien_va_cac_cong_doan.md).
> * **Quy định vị trí thư mục mã nguồn**: Toàn bộ codebase thực nghiệm, môi trường ảo `.venv`, cấu hình, module mã nguồn `src/`, kịch bản `experiments/` và kết quả `outputs/` được đóng gói độc lập và chuyên biệt bên trong thư mục con **`RareProtSelect/`** (nằm trong `Topic 2/`), tách biệt hoàn toàn với các tệp tài liệu nghiên cứu và repo gốc ở thư mục cha.
> * **Nguyên tắc bất di bất dịch**: Trước khi viết hoặc sửa bất kỳ dòng code nào, **bắt buộc phải cập nhật bản thiết kế trong tệp này trước**.
> * Trong mỗi tệp code thực tế, phần chú thích đầu tệp (Docstring) **bắt buộc phải ghi rõ: "Thực hiện Công đoạn X.X trong Tài liệu 1 và Module Y trong Tài liệu 2"**.

---

## MỤC LỤC BẢN THIẾT KẾ

- [1. Cấu trúc Cây Thư mục Toàn dự án (Project Directory Structure)](#sec-tree)
- [2. Môi trường Thực thi & Quản lý Phụ thuộc (`uv`)](#sec-env)
- [3. Thiết kế Chi tiết Từng Module & Tệp Mã Nguồn](#sec-modules)
  - [3.1. Module Cấu hình (`RareProtSelect/src/config/`)](#module-config)
  - [3.2. Module Dữ liệu & Tiền xử lý (`RareProtSelect/src/data/`)](#module-data)
  - [3.3. Module Nhúng Ngữ nghĩa ESM-2 (`RareProtSelect/src/embeddings/`)](#module-embeddings)
  - [3.4. Module Ma trận Tương đồng (`RareProtSelect/src/similarity/`)](#module-similarity)
  - [3.5. Module Trọng số Thích ứng Nhóm hiếm (`RareProtSelect/src/weighting/`)](#module-weighting)
  - [3.6. Module Tối ưu hóa Submodular & Baselines (`RareProtSelect/src/selection/`)](#module-selection)
  - [3.7. Module Đánh giá Đa tầng (`RareProtSelect/src/evaluation/`)](#module-evaluation)
  - [3.8. Module Tiện ích, Đo lường & Trực quan hóa (`RareProtSelect/src/utils/`)](#module-utils)
- [4. Thiết kế Kịch bản Thực nghiệm Độc lập (`RareProtSelect/experiments/`)](#sec-experiments)
- [5. Sơ đồ Luồng Dữ liệu Toàn cục (Dataflow Pipeline)](#sec-dataflow)
- [6. Ma trận Truy vết 2 Chiều (Traceability Matrix: Công đoạn $\leftrightarrow$ File Code)](#sec-traceability)

---

<a id="sec-tree"></a>
## 1. CẤU TRÚC CÂY THƯ MỤC TOÀN DỰ ÁN

```
Topic 2/                                   # Thư mục gốc dự án
├── GEMINI.md                              # Quy chuẩn hoạt động & điều phối AI
├── quy_trinh_thuc_hien_va_cac_cong_doan.md # [TÀI LIỆU 1] Quy trình nghiên cứu khoa học (SSOT)
├── thiet_ke_codebase_va_kien_truc_he_thong.md # [TÀI LIỆU 2] Thiết kế codebase & kiến trúc (SSOT)
├── doc_hieu_topic2_va_bai_bao_nen.md      # Tài liệu phân tích đọc hiểu bài báo nền
├── giai_thich_khai_niem.md                # Tài liệu giải thích chi tiết khái niệm
├── topic2.md                              # Đề cương đề tài gốc
├── baseline_repo/                         # Thư mục lưu mã nguồn R gốc & 3 file FASTA chuẩn
│   ├── Greedy.R                           # Script R gốc của Nguyen et al. (2025)
│   ├── Bidirectional_Greedy.R             # Script R đối chứng gốc
│   ├── Thioesterases_Sequences.fasta      # 737 chuỗi TE
│   ├── MEROPS_A1A.fasta                   # 13,847 chuỗi Peptidase A1
│   └── CE.fasta                           # 12,277 chuỗi Carboxylesterase
│
└── RareProtSelect/                        # THƯ MỤC CODEBASE CHÍNH CỦA DỰ ÁN (ĐỘC LẬP & ĐÓNG GÓI)
    ├── .venv/                             # Môi trường ảo Python 3.12 tạo bởi uv
    ├── pyproject.toml                     # Cấu hình dự án và dependencies qua uv
    ├── requirements.txt                   # Danh sách dependencies phụ trợ
    │
    ├── configs/                           # Tệp cấu hình thực nghiệm YAML
    │   ├── config_pilot_thyme.yaml        # Cấu hình cho 27 họ Thioesterase
    │   ├── config_core_merops.yaml        # Cấu hình cho 76 phân họ MEROPS A1A
    │   ├── config_scalability_ce.yaml     # Cấu hình cho siêu họ CE
    │   └── config_ablation.yaml           # Cấu hình các kịch bản bóc tách
    │
    ├── src/                               # Mã nguồn lõi (Modularized Python Package)
    │   ├── __init__.py
    │   ├── config/                        # Module nạp và kiểm tra cấu hình
    │   │   ├── __init__.py
    │   │   └── settings.py
    │   ├── data/                          # Module đọc & tiền xử lý FASTA / Annotation
    │   │   ├── __init__.py
    │   │   ├── fasta_parser.py            # [Công đoạn 1.1] Đọc FASTA thô
    │   │   ├── quality_filter.py          # [Công đoạn 1.2] Lọc chuỗi lỗi/rác
    │   │   ├── annotation_mapper.py       # [Công đoạn 1.3] Trích xuất nhãn phân họ
    │   │   └── dataset_loader.py          # Bộ nạp dữ liệu tích hợp
    │   ├── embeddings/                    # Module trích xuất vector ESM-2
    │   │   ├── __init__.py
    │   │   ├── esm_embedder.py            # [Công đoạn 2.1 & 2.2] Inference ESM-2 & Mean Pooling
    │   │   └── cache_manager.py           # [Công đoạn 2.3] Quản lý lưu đệm .npy/.pt
    │   ├── similarity/                    # Module đo khoảng cách ngữ nghĩa
    │   │   ├── __init__.py
    │   │   ├── dense_similarity.py        # [Công đoạn 3.1] Cosine matrix không âm
    │   │   └── sparse_knn.py              # Biến thể Sparse k-NN cho tập siêu lớn
    │   ├── weighting/                     # Module tính trọng số Rare-aware
    │   │   ├── __init__.py
    │   │   └── rare_weighting.py          # [Công đoạn 3.2] Hàm w_v = 1/sqrt(n_g) & ablations
    │   ├── selection/                     # Module các thuật toán chọn tập đại diện
    │   │   ├── __init__.py
    │   │   ├── lazy_greedy.py             # [Công đoạn 4.2] WFL Lazy Greedy (Heapq - CỐT LÕI)
    │   │   ├── standard_greedy.py         # [Công đoạn 4.3] Standard Greedy (Baseline)
    │   │   └── baseline_selectors.py      # Random, K-Medoids, CD-HIT/MMseqs2 Wrappers
    │   ├── evaluation/                    # Module đo đạc và kiểm định khoa học
    │   │   ├── __init__.py
    │   │   ├── intrinsic_metrics.py       # [Công đoạn 5.1] Overall, Macro, Worst Coverage, Redundancy
    │   │   ├── annotation_transfer.py     # [Công đoạn 5.2] 1-NN Transfer, Macro-F1 & Accuracy
    │   │   └── benchmark_comparator.py    # [Công đoạn 7.1] So sánh với Chuẩn chuyên gia ThYme
    │   └── utils/                         # Module tiện ích hỗ trợ
    │       ├── __init__.py
    │       ├── timer.py                   # [Công đoạn 5.3] Bấm giờ chính xác cao
    │       ├── memory_tracker.py          # [Công đoạn 5.3] Theo dõi RAM / GPU VRAM
    │       ├── visualizer.py              # Vẽ đồ thị Coverage vs k, Confusion Matrix
    │       └── exporter.py                # Xuất bảng CSV, JSON, Markdown báo cáo
    │
    ├── experiments/                       # Scripts chạy thực nghiệm độc lập
    │   ├── run_pilot_thyme.py             # [Công đoạn 7.1] Thử nghiệm Pilot trên 27 họ TE
    │   ├── run_core_merops.py             # [Công đoạn 7.2] Thực nghiệm Trọng tâm trên MEROPS A1A
    │   ├── run_scalability_ce.py          # [Công đoạn 7.3] Thực nghiệm Tốc độ & Tổng quát trên CE
    │   └── run_ablation_all.py            # [Giai đoạn 6] Chạy toàn bộ Ma trận Ablation
    │
    ├── outputs/                           # Thư mục chứa kết quả sinh ra tự động
    │   ├── embeddings_cache/              # Lưu trữ vector nhúng .npy
    │   ├── similarity_cache/              # Lưu ma trận tương đồng
    │   ├── logs/                          # Log chi tiết quá trình chạy
    │   ├── figures/                       # Biểu đồ xuất bản (PNG, SVG, PDF)
    │   └── tables/                        # Bảng số liệu đối đầu (CSV, LaTeX)
    │
    └── tests/                             # Unit tests kiểm thử tính đúng đắn toán học
        ├── test_submodular_math.py        # Test tính chất đơn điệu & submodular
        ├── test_lazy_vs_standard.py       # Test chứng minh nghiệm giống nhau 100%
        └── test_metrics.py                # Test tính đúng đắn của Worst Coverage & Macro F1
```

---

<a id="sec-env"></a>
## 2. MÔI TRƯỜNG THỰC THI & QUẢN LÝ PHỤ THUỘC (`uv`)

Toàn bộ môi trường ảo và gói cài đặt được thiết lập và quản lý bên trong thư mục `RareProtSelect/`:
* **Trình quản lý gói**: `uv` (`C:\Users\doana\.local\bin\uv.exe`).
* **Phiên bản Python**: Python 3.12 (`C:\Users\doana\.local\bin\python3.12.exe`).
* **Phần cứng GPU chuyên dụng**: **NVIDIA GeForce RTX 5060 Laptop GPU** (Kiến trúc Blackwell, Compute Capability 12.0, Driver CUDA 13.2).
* **Phiên bản PyTorch chuẩn**: **`torch==2.13.0+cu130`** và **`torchvision==0.28.0+cu130`** (bản build CUDA 13.0 mới nhất hỗ trợ hoàn hảo kiến trúc GPU RTX 5060, lấy trực tiếp từ bộ đệm `uv` `D:\uv_cache`).
* **Lệnh thiết lập môi trường bằng `uv`**:
  ```powershell
  cd "c:\Users\doana\Downloads\Topic 2\RareProtSelect"
  uv venv --python "C:\Users\doana\.local\bin\python3.12.exe" .venv
  .venv\Scripts\activate
  uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu130
  uv pip install transformers fair-esm biopython scikit-learn scipy numpy pandas matplotlib seaborn pyyaml tqdm
  ```

---

<a id="sec-modules"></a>
## 3. THIẾT KẾ CHI TIẾT TỪNG MODULE & TỆP MÃ NGUỒN

---

<a id="module-config"></a>
### 3.1. Module Cấu hình (`RareProtSelect/src/config/`)

#### Tệp: `RareProtSelect/src/config/settings.py`
* **Mục đích**: Nạp và kiểm tra tính hợp lệ của tệp YAML cấu hình thực nghiệm.
* **Lớp chính**: `ExperimentConfig` (Dataclass).
* **Các hàm**:
  * `load_config(yaml_path: str) -> ExperimentConfig`
  * `validate_config(config: ExperimentConfig) -> bool`

---

<a id="module-data"></a>
### 3.2. Module Dữ liệu & Tiền xử lý (`RareProtSelect/src/data/`)

<a id="fasta-parser"></a>
#### Tệp: `RareProtSelect/src/data/fasta_parser.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 1.1 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-11).
* **Cấu trúc dữ liệu**:
  ```python
  from dataclasses import dataclass

  @dataclass
  class ProteinRecord:
      id: str
      sequence: str
      header: str
      length: int
  ```
* **Hàm chính**:
  ```python
  def parse_fasta(file_path: str) -> list[ProteinRecord]:
      """Đọc tệp FASTA thô và chuyển đổi thành danh sách ProteinRecord chuẩn hóa."""
      ...
  ```

---

<a id="quality-filter"></a>
#### Tệp: `RareProtSelect/src/data/quality_filter.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 1.2 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-12).
* **Hàm chính**:
  ```python
  def filter_proteins(
      records: list[ProteinRecord],
      min_len: int = 30,
      max_len: int = 2000,
      max_ambiguous_ratio: float = 0.05
  ) -> tuple[list[ProteinRecord], dict]:
      """Lọc bỏ các chuỗi rác, phân mảnh hoặc chứa quá nhiều ký tự lạ.
      Trả về: (Danh sách chuỗi sạch, Thống kê lọc QC)."""
      ...
  ```

---

<a id="annotation-mapper"></a>
#### Tệp: `RareProtSelect/src/data/annotation_mapper.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 1.3 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-13).
* **Hàm chính**:
  ```python
  def extract_merops_subfamilies(records: list[ProteinRecord]) -> dict[str, str]:
      """Trích xuất mã phân họ [A01.xxx] từ header MEROPS A1A."""
      ...

  def extract_ce_subgroups(records: list[ProteinRecord]) -> dict[str, str]:
      """Trích xuất mã nhóm /Fxx/ từ header Carboxylesterase."""
      ...

  def get_subfamily_statistics(label_map: dict[str, str]) -> dict[str, int]:
      """Đếm số lượng thành viên n_g của từng phân họ và xác định nhóm hiếm."""
      ...
  ```

---

<a id="module-embeddings"></a>
### 3.3. Module Nhúng Ngữ nghĩa ESM-2 (`RareProtSelect/src/embeddings/`)

<a id="esm-embedder"></a>
#### Tệp: `RareProtSelect/src/embeddings/esm_embedder.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 2.1 & 2.2 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-21).
* **Lớp chính**: `ESMEmbedder`
* **Các phương thức**:
  ```python
  class ESMEmbedder:
      def __init__(self, model_name: str = "facebook/esm2_t12_35M_UR50D", device: str = "auto"):
          ...

      def embed_sequences(self, sequences: list[str], batch_size: int = 16) -> np.ndarray:
          """Sinh vector nhúng cho danh sách chuỗi: Mean Pooling + Chuẩn hóa L2.
          Trả về: Mảng numpy shape (N, d) với chuẩn L2 mỗi hàng bằng 1.0."""
          ...
  ```

---

<a id="cache-manager"></a>
#### Tệp: `RareProtSelect/src/embeddings/cache_manager.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 2.3 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-23).
* **Hàm chính**:
  ```python
  def save_embeddings_cache(cache_path: str, embeddings: np.ndarray, seq_ids: list[str]):
      ...

  def load_embeddings_cache(cache_path: str) -> tuple[np.ndarray, list[str]]:
      ...
  ```

---

<a id="module-similarity"></a>
### 3.4. Module Ma trận Tương đồng (`RareProtSelect/src/similarity/`)

<a id="dense-similarity"></a>
#### Tệp: `RareProtSelect/src/similarity/dense_similarity.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 3.1 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-31).
* **Hàm chính**:
  ```python
  def compute_cosine_similarity_matrix(normalized_embeddings: np.ndarray) -> np.ndarray:
      """Tính ma trận Cosine Similarity không âm: Sim = max(0, Z @ Z.T).
      Đảm bảo Sim[i, j] in [0, 1] và Sim[i, i] = 1.0."""
      ...
  ```

---

<a id="module-weighting"></a>
### 3.5. Module Trọng số Thích ứng Nhóm hiếm (`RareProtSelect/src/weighting/`)

<a id="rare-weighting"></a>
#### Tệp: `RareProtSelect/src/weighting/rare_weighting.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 3.2 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-32).
* **Hàm chính**:
  ```python
  def compute_rare_aware_weights(
      seq_ids: list[str],
      label_map: dict[str, str],
      scheme: str = "inverse_sqrt",  # 'inverse_sqrt', 'uniform', 'inverse_freq', 'power'
      alpha: float = 0.5
  ) -> np.ndarray:
      """Tính vector trọng số w_v cho từng protein:
      - inverse_sqrt: w_v = 1 / sqrt(n_g) (MẶC ĐỊNH - RAREPROTSELECT)
      - uniform: w_v = 1.0 (BASELINE)
      - inverse_freq: w_v = 1 / n_g (ABLATION)
      - power: w_v = 1 / (n_g ** alpha)
      """
      ...
  ```

---

<a id="module-selection"></a>
### 3.6. Module Tối ưu hóa Submodular & Baselines (`RareProtSelect/src/selection/`)

<a id="lazy-greedy-code"></a>
#### Tệp: `RareProtSelect/src/selection/lazy_greedy.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 4.1 & 4.2 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-41).
* **Hàm chính**:
  ```python
  def lazy_greedy_facility_location(
      sim_matrix: np.ndarray,
      weights: np.ndarray,
      budget_k: int
  ) -> tuple[list[int], list[float], list[float]]:
      """Thuật toán Lazy Greedy tối ưu hóa Weighted Facility Location qua Max-Heap.
      Trả về:
      - selected_indices: Danh sách chỉ số protein đại diện được chọn [s_1, s_2, ..., s_k]
      - marginal_gains: Lợi ích biên thu được tại mỗi bước
      - objective_values: Giá trị hàm F(S) tích lũy
      """
      ...
  ```

---

<a id="standard-greedy-code"></a>
#### Tệp: `RareProtSelect/src/selection/standard_greedy.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 4.3 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-43).
* **Hàm chính**:
  ```python
  def standard_greedy_facility_location(
      sim_matrix: np.ndarray,
      weights: np.ndarray,
      budget_k: int
  ) -> tuple[list[int], list[float], list[float]]:
      """Thuật toán Standard Greedy gốc (quét vét cạn O(k*n^2) mỗi bước)."""
      ...
  ```

---



<a id="module-evaluation"></a>
### 3.7. Module Đánh giá Đa tầng (`RareProtSelect/src/evaluation/`)

<a id="intrinsic-metrics"></a>
#### Tệp: `RareProtSelect/src/evaluation/intrinsic_metrics.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 5.1 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-51).
* **Hàm chính**:
  ```python
  def compute_group_coverage(sim_matrix: np.ndarray, selected_indices: list[int], group_indices: list[int]) -> float:
      """Tính Coverage(g) cho một phân họ g."""
      ...

  def evaluate_intrinsic_metrics(
      sim_matrix: np.ndarray,
      selected_indices: list[int],
      labels: list[str],
      rare_threshold: int = 5
  ) -> dict[str, float]:
      """Tính toán toàn bộ bộ chỉ số nội tại:
      - overall_coverage: Độ bao phủ toàn họ
      - macro_coverage: Độ bao phủ trung bình đều qua các phân họ
      - worst_group_coverage: Độ bao phủ của phân họ thiệt thòi nhất
      - rare_group_representation_rate: Tỷ lệ phân họ hiếm có đại diện
      - pairwise_redundancy: Độ trùng lặp nội bộ tập S
      """
      ...
  ```

---

<a id="annotation-transfer-code"></a>
#### Tệp: `RareProtSelect/src/evaluation/annotation_transfer.py`
* **Mục đích**: Hiện thực hóa [**Công đoạn 5.2 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-52).
* **Hàm chính**:
  ```python
  def evaluate_annotation_transfer_1nn(
      sim_matrix: np.ndarray,
      selected_indices: list[int],
      labels: list[str]
  ) -> dict[str, float]:
      """Dùng tập S gán nhãn 1-NN cho V \ S và đo đạc:
      - macro_f1: Trung bình Macro-F1 qua tất cả các lớp
      - accuracy: Độ chính xác tổng thể
      """
      ...
  ```

---

<a id="module-utils"></a>
### 3.8. Module Tiện ích, Đo lường & Trực quan hóa (`RareProtSelect/src/utils/`)

<a id="utils-code"></a>
* `timer.py`: Đo thời gian thực thi chính xác cao bằng `time.perf_counter_ns()`.
* `memory_tracker.py`: Theo dõi Peak RAM và GPU VRAM qua `tracemalloc` và `torch.cuda`.
* `visualizer.py`: Vẽ biểu đồ đường cong *Coverage vs Budget $k$*, ma trận nhầm lẫn *Confusion Matrix*, và biểu đồ so sánh các thuật toán.
* `exporter.py`: Xuất bảng biểu kết quả ra định dạng CSV, JSON và Markdown.

---

<a id="sec-experiments"></a>
## 4. THIẾT KẾ KỊCH BẢN THỰC NGHIỆM ĐỘC LẬP (`RareProtSelect/experiments/`)

<a id="exp-thyme"></a>
### 4.1. Kịch bản Pilot: `RareProtSelect/experiments/run_pilot_thyme.py`
* **Mục tiêu**: Hiện thực hóa [**Công đoạn 7.1 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-71) trên $737$ chuỗi Thioesterase (27 họ ThYme).

<a id="exp-merops"></a>
### 4.2. Kịch bản Trọng tâm: `RareProtSelect/experiments/run_core_merops.py`
* **Mục tiêu**: Hiện thực hóa [**Công đoạn 7.2 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-72) trên $13,847$ chuỗi Peptidase A1 (76 phân họ MEROPS). Chạy đối đầu Unweighted vs. Rare-Aware WFL qua các dải $k \in [5, 10, 20, 50, 100, 200, 400, 600]$.

<a id="exp-ce"></a>
### 4.3. Kịch bản Hiệu năng & Tổng quát: `RareProtSelect/experiments/run_scalability_ce.py`
* **Mục tiêu**: Hiện thực hóa [**Công đoạn 7.3 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#cong-doan-73) trên $12,277$ chuỗi Carboxylesterase. So sánh Runtime & Memory của Lazy Greedy vs. Standard Greedy.

<a id="exp-ablation"></a>
### 4.4. Kịch bản Bóc tách: `RareProtSelect/experiments/run_ablation_all.py`
* **Mục tiêu**: Hiện thực hóa [**Giai đoạn 6 trong Tài liệu 1**](./quy_trinh_thuc_hien_va_cac_cong_doan.md#giai-doan-6).

---

<a id="sec-dataflow"></a>
## 5. SƠ ĐỒ LUỒNG DỮ LIỆU TOÀN CỤC (DATAFLOW PIPELINE)

```
[ ../baseline_repo/*.fasta ]
          │
          ▼
   fasta_parser.py ──► quality_filter.py ──► Clean Records
                                                  │
                   ┌──────────────────────────────┴──────────────────────────────┐
                   ▼                                                             ▼
           annotation_mapper.py                                            esm_embedder.py
                   │                                                             │
                   ▼                                                             ▼
          rare_weighting.py                                              cache_manager.py
                   │                                                             │
                   ▼                                                             ▼
            Vector Trọng Số w_v                                         dense_similarity.py
                   │                                                             │
                   │                                                             ▼
                   │                                                    Ma Trận Tương Đồng Sim
                   │                                                             │
                   └──────────────────────────────┬──────────────────────────────┘
                                                  ▼
                                        lazy_greedy.py (WFL)
                                                  │
                                                  ▼
                                      Tập Đại Diện Được Chọn S_k
                                                  │
                   ┌──────────────────────────────┴──────────────────────────────┐
                   ▼                                                             ▼
          intrinsic_metrics.py                                        annotation_transfer.py
                   │                                                             │
                   ▼                                                             ▼
     Overall / Macro / Worst Cov                                       Macro-F1 / Worst F1
                   │                                                             │
                   └──────────────────────────────┬──────────────────────────────┘
                                                  ▼
                                       exporter.py & visualizer.py
                                                  │
                                                  ▼
                                   Báo Cáo Thực Nghiệm & Biểu Đồ (outputs/)
```

---

<a id="sec-traceability"></a>
## 6. MA TRẬN TRUY VẾT 2 CHIỀU (TRACEABILITY MATRIX)

| Công đoạn trong [Tài liệu 1](./quy_trinh_thuc_hien_va_cac_cong_doan.md) | File Code đảm nhiệm (trong `RareProtSelect/`) | Hàm / Class chịu trách nhiệm chính |
| :--- | :--- | :--- |
| **Công đoạn 1.1: Đọc FASTA** | `src/data/fasta_parser.py` | `parse_fasta(file_path)` |
| **Công đoạn 1.2: Lọc QC chuỗi** | `src/data/quality_filter.py` | `filter_proteins(records, ...)` |
| **Công đoạn 1.3: Ánh xạ Phân họ** | `src/data/annotation_mapper.py` | `extract_merops_subfamilies()`, `extract_ce_subgroups()` |
| **Công đoạn 2.1 & 2.2: ESM-2 Embedding** | `src/embeddings/esm_embedder.py` | `ESMEmbedder.embed_sequences()` |
| **Công đoạn 2.3: Cache Vector** | `src/embeddings/cache_manager.py` | `save_embeddings_cache()`, `load_embeddings_cache()` |
| **Công đoạn 3.1: Cosine Similarity** | `src/similarity/dense_similarity.py` | `compute_cosine_similarity_matrix()` |
| **Công đoạn 3.2: Trọng số Rare-Aware** | `src/weighting/rare_weighting.py` | `compute_rare_aware_weights()` |
| **Công đoạn 4.1 & 4.2: Lazy Greedy WFL** | `src/selection/lazy_greedy.py` | `lazy_greedy_facility_location()` |
| **Công đoạn 4.3: Standard Greedy** | `src/selection/standard_greedy.py` | `standard_greedy_facility_location()` |
| **Công đoạn 5.1: Đánh giá Nội tại** | `src/evaluation/intrinsic_metrics.py` | `evaluate_intrinsic_metrics()` |
| **Công đoạn 5.2: Annotation Transfer** | `src/evaluation/annotation_transfer.py` | `evaluate_annotation_transfer_1nn()` |
| **Công đoạn 5.3: Đo Runtime & RAM** | `src/utils/timer.py`, `memory_tracker.py` | `Timer`, `MemoryTracker` |
| **Giai đoạn 6: Ma trận Ablation** | `experiments/run_ablation_all.py` | `main()` |
| **Công đoạn 7.1: Pilot Thioesterase** | `experiments/run_pilot_thyme.py` | `main()` |
| **Công đoạn 7.2: Trọng tâm MEROPS A1A** | `experiments/run_core_merops.py` | `main()` |
| **Công đoạn 7.3: Hiệu năng CE** | `experiments/run_scalability_ce.py` | `main()` |
---

<a id="sec-testing-qa"></a>
## 7. QUY CHUẨN KIỂM THỬ TĨNH (STATIC CODE VERIFICATION) & BỘ TEST SUITE CHUẨN

Để đảm bảo toàn bộ mã nguồn được xây dựng chuẩn xác $100\%$ theo bản thiết kế, đội ngũ kỹ sư QA / Test Agent thực hiện 2 quy trình kiểm định bắt buộc:

### 7.1. Quy trình Kiểm thử Tĩnh Đối chiếu 1-1 (Static Code Verification Protocol)
Trước khi nghiệm thu bất kỳ tệp mã nguồn nào, QA Agent phải rà soát qua bảng tiêu chí kiểm định tĩnh (Checklist):
1. **Kiểm tra Truy vết Docstring**: Tệp có chứa Docstring đầu file ghi rõ: *"Thực hiện Công đoạn X.X trong Tài liệu 1 và Module Y trong Tài liệu 2"* hay không?
2. **Kiểm tra Chữ ký & Kiểu dữ liệu (1-to-1 Signature Parity)**: Tên Class, Tên Hàm, Danh sách Tham số, Kiểu dữ liệu đầu vào (`type hints`) và Kiểu dữ liệu trả về (`return types`) có khớp $100\%$ với Bản thiết kế ở Mục 3 không?
3. **Kiểm tra Trường hợp Biên (Edge-case Hardening)**:
   * Xử lý trường hợp tập dữ liệu rỗng hoặc chuỗi có độ dài bất thường.
   * Xử lý chống chia cho $0$ trong hàm trọng số ($n_g \ge 1$) và trong tính F1-Score ($TP + FP = 0$).
   * Bảo đảm ma trận tương đồng Cosine luôn không âm ($\operatorname{sim} \ge 0$).
   * Xử lý khi ngân sách $k > n$ (ngân sách lớn hơn tổng số chuỗi).

---

### 7.2. Thiết kế Bộ Unit Test & Property Test Chuẩn mực (`RareProtSelect/tests/`)

Toàn bộ các tệp kiểm thử được đặt trong `RareProtSelect/tests/` và thực thi tự động qua `pytest`:

```
RareProtSelect/tests/
├── conftest.py                      # Fixtures sinh dữ liệu giả lập (Toy synthetic fasta & embeddings)
├── test_fasta_parser_qc.py          # [Test Công đoạn 1.1 & 1.2] Test đọc FASTA, khử ngắt dòng, lọc QC
├── test_annotation_mapper.py        # [Test Công đoạn 1.3] Test regex nhãn phân họ MEROPS / CE / TE
├── test_embeddings_similarity.py    # [Test Công đoạn 2.1, 2.2, 3.1] Test chuẩn L2=1.0, Cosine không âm
├── test_rare_weighting.py           # [Test Công đoạn 3.2] Test công thức w_v = 1/sqrt(n_g) & ablations
├── test_submodular_math.py          # [Test Công đoạn 4.1] Test tính đơn điệu & lợi ích biên giảm dần
├── test_lazy_vs_standard_greedy.py  # [Test Công đoạn 4.2 & 4.3] Test CHỨNG MINH Lazy Greedy == Standard Greedy 100%
└── test_evaluation_metrics.py       # [Test Công đoạn 5.1 & 5.2] Test Worst Coverage & Macro F1 calculation
```

#### Chi tiết các ca kiểm thử then chốt:

1. **`test_submodular_math.py`**:
   * **Test tính Đơn điệu (Monotonicity)**: Sinh ngẫu nhiên các tập con $A \subset B \subset V$, kiểm tra $F(A) \le F(B)$.
   * **Test tính Submodular (Diminishing Gains)**: Với mọi phần tử $e \notin B$, kiểm tra $\Delta F(e \mid A) \ge \Delta F(e \mid B)$.

2. **`test_lazy_vs_standard_greedy.py` (Bảo đảm tương đương nghiệm tuyệt đối)**:
   * Chạy song song `lazy_greedy_facility_location` và `standard_greedy_facility_location` trên cùng một ma trận tương đồng và vector trọng số.
   * So sánh:
     * `assert lazy_selected_indices == standard_selected_indices` (Thứ tự và danh sách phần tử chọn giống $100\%$).
     * `assert np.allclose(lazy_objective_values, standard_objective_values)` (Giá trị hàm mục tiêu khớp chính xác tuyệt đối).

3. **`test_evaluation_metrics.py`**:
   * Dùng ví dụ bằng số trong Tài liệu Đọc hiểu ($90$ chuỗi nhóm lớn, $8$ chuỗi nhóm vừa, $2$ chuỗi nhóm hiếm) để đối chiếu kết quả hàm tính `worst_group_coverage`, `macro_coverage`, và `annotation_transfer_macro_f1` với các giá trị lý thuyết đã tính tay.

---

### 7.3. Lệnh Thực thi Kiểm thử Toàn diện:
```powershell
cd "c:\Users\doana\Downloads\Topic 2\RareProtSelect"
& ".\.venv\Scripts\pytest" tests/ -v --cov=src --cov-report=term-missing
```