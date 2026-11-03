# BẢN ĐỒ GIAO DIỆN & HỢP ĐỒNG KỸ THUẬT (LIVING INTERFACE INDEX)

> **Tự động sinh bởi GTD `sync-interfaces`**: Bản đồ chữ ký công khai (Public API Signatures & Types), loại bỏ 100% thân hàm (zero implementation body) để bảo toàn context window khi mở phiên chat mới.

- **Thư mục gốc:** `D:\programing\project\Topic 2`
- **Tổng số tệp mã nguồn:** 31

---

## MỤC LỤC TỆP MÃ NGUỒN

- [RareProtSelect/archive_legacy_code/memory_tracker.py](#rareprotselect-archive_legacy_code-memory_tracker-py) (`python`, 1 symbols)
- [RareProtSelect/archive_legacy_code/sparse_knn.py](#rareprotselect-archive_legacy_code-sparse_knn-py) (`python`, 2 symbols)
- [RareProtSelect/archive_legacy_code/src_evaluation/__init__.py](#rareprotselect-archive_legacy_code-src_evaluation-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/archive_legacy_code/src_evaluation/intrinsic_metrics.py](#rareprotselect-archive_legacy_code-src_evaluation-intrinsic_metrics-py) (`python`, 2 symbols)
- [RareProtSelect/archive_legacy_code/visualizer.py](#rareprotselect-archive_legacy_code-visualizer-py) (`python`, 8 symbols)
- [RareProtSelect/experiments/__init__.py](#rareprotselect-experiments-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/experiments/exp1_baseline_a1a_calibration.py](#rareprotselect-experiments-exp1_baseline_a1a_calibration-py) (`python`, 4 symbols)
- [RareProtSelect/experiments/exp2_rare_weighted_a1a.py](#rareprotselect-experiments-exp2_rare_weighted_a1a-py) (`python`, 3 symbols)
- [RareProtSelect/experiments/exp3_esm_coverage_a1a.py](#rareprotselect-experiments-exp3_esm_coverage_a1a-py) (`python`, 3 symbols)
- [RareProtSelect/experiments/exp4_cross_eval_a1a.py](#rareprotselect-experiments-exp4_cross_eval_a1a-py) (`python`, 7 symbols)
- [RareProtSelect/experiments/exp5_subfamily_allocation_a1a.py](#rareprotselect-experiments-exp5_subfamily_allocation_a1a-py) (`python`, 9 symbols)
- [RareProtSelect/src/__init__.py](#rareprotselect-src-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/src/config/__init__.py](#rareprotselect-src-config-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/src/config/settings.py](#rareprotselect-src-config-settings-py) (`python`, 9 symbols)
- [RareProtSelect/src/data/__init__.py](#rareprotselect-src-data-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/src/data/annotation_mapper.py](#rareprotselect-src-data-annotation_mapper-py) (`python`, 6 symbols)
- [RareProtSelect/src/data/dataset_loader.py](#rareprotselect-src-data-dataset_loader-py) (`python`, 3 symbols)
- [RareProtSelect/src/data/fasta_parser.py](#rareprotselect-src-data-fasta_parser-py) (`python`, 3 symbols)
- [RareProtSelect/src/data/quality_filter.py](#rareprotselect-src-data-quality_filter-py) (`python`, 3 symbols)
- [RareProtSelect/src/selection/__init__.py](#rareprotselect-src-selection-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/src/selection/base.py](#rareprotselect-src-selection-base-py) (`python`, 2 symbols)
- [RareProtSelect/src/selection/pruned_greedy.py](#rareprotselect-src-selection-pruned_greedy-py) (`python`, 2 symbols)
- [RareProtSelect/src/selection/standard_greedy.py](#rareprotselect-src-selection-standard_greedy-py) (`python`, 2 symbols)
- [RareProtSelect/src/selection/unweighted_selector.py](#rareprotselect-src-selection-unweighted_selector-py) (`python`, 1 symbols)
- [RareProtSelect/src/similarity/__init__.py](#rareprotselect-src-similarity-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/src/similarity/blast_similarity.py](#rareprotselect-src-similarity-blast_similarity-py) (`python`, 1 symbols)
- [RareProtSelect/src/similarity/dense_similarity.py](#rareprotselect-src-similarity-dense_similarity-py) (`python`, 4 symbols)
- [RareProtSelect/src/utils/__init__.py](#rareprotselect-src-utils-__init__-py) (`python`, 0 symbols)
- [RareProtSelect/src/utils/exporter.py](#rareprotselect-src-utils-exporter-py) (`python`, 6 symbols)
- [RareProtSelect/src/utils/timer.py](#rareprotselect-src-utils-timer-py) (`python`, 2 symbols)
- [RareProtSelect/tools/blast/bin/cleanup-blastdb-volumes.py](#rareprotselect-tools-blast-bin-cleanup-blastdb-volumes-py) (`python`, 5 symbols)

---

## CHI TIẾT GIAO DIỆN CÁC MODULE

### <a id="rareprotselect-archive_legacy_code-memory_tracker-py"></a> RareProtSelect/archive_legacy_code/memory_tracker.py
- **Đường dẫn:** [`RareProtSelect/archive_legacy_code/memory_tracker.py`](RareProtSelect/archive_legacy_code/memory_tracker.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 5.3 trong Tài liệu 1 và Module 3.8 (memory_tracker.py) trong Tài liệu 2."""

class MemoryTracker:
    """Bộ theo dõi mức sử dụng bộ nhớ đỉnh (Peak RAM qua tracemalloc và Peak VRAM qua torch.cuda)."""

    def __init__(self, name: str='MemoryTracker', auto_log: bool=False) -> None:
        pass

    def start(self) -> MemoryTracker:
        """Bắt đầu theo dõi bộ nhớ."""
        pass

    def stop(self) -> tuple[float, float]:
        """Dừng theo dõi và trả về bộ nhớ đỉnh (peak_ram_mb, peak_vram_mb)."""
        pass

    def get_peak_ram_mb(self) -> float:
        """Lấy mức RAM đỉnh hiện tại (MB)."""
        pass

    def get_peak_vram_mb(self) -> float:
        """Lấy mức VRAM GPU đỉnh hiện tại (MB)."""
        pass

    def reset(self) -> None:
        """Khởi tạo lại trạng thái theo dõi."""
        pass

    def __enter__(self) -> MemoryTracker:
        pass

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        pass
```

### <a id="rareprotselect-archive_legacy_code-sparse_knn-py"></a> RareProtSelect/archive_legacy_code/sparse_knn.py
- **Đường dẫn:** [`RareProtSelect/archive_legacy_code/sparse_knn.py`](RareProtSelect/archive_legacy_code/sparse_knn.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 3.1 (Sparse Variant) trong Tài liệu 1 và Module 3.4 (sparse_knn.py) trong Tài liệu 2."""

def compute_sparse_knn_similarity(normalized_embeddings: np.ndarray, k_neighbors: int=50, symmetric: bool=True) -> sp.csr_matrix:
    """Tính ma trận tương đồng Cosine thưa Sparse k-NN (CSR format) cho tập dữ liệu lớn."""
    pass

class SparseKNNSimilarity:
    """Bộ tính toán Không gian Tương đồng Thưa Sparse k-NN cho quy mô lớn."""

    def __init__(self, k_neighbors: int=50, symmetric: bool=True) -> None:
        pass

    def compute_sparse_knn_matrix(self, normalized_embeddings: np.ndarray) -> sp.csr_matrix:
        """Tính ma trận CSR k-NN từ tập vector nhúng L2-normalized."""
        pass
```

### <a id="rareprotselect-archive_legacy_code-src_evaluation-__init__-py"></a> RareProtSelect/archive_legacy_code/src_evaluation/__init__.py
- **Đường dẫn:** [`RareProtSelect/archive_legacy_code/src_evaluation/__init__.py`](RareProtSelect/archive_legacy_code/src_evaluation/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Module Đánh giá Đa tầng (Layer 4) trong Tài liệu 1 và Module 3.7 trong Tài liệu 2."""
```

### <a id="rareprotselect-archive_legacy_code-src_evaluation-intrinsic_metrics-py"></a> RareProtSelect/archive_legacy_code/src_evaluation/intrinsic_metrics.py
- **Đường dẫn:** [`RareProtSelect/archive_legacy_code/src_evaluation/intrinsic_metrics.py`](RareProtSelect/archive_legacy_code/src_evaluation/intrinsic_metrics.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 5.1 trong Tài liệu 1 và Module 3.7 (intrinsic_metrics.py) trong Tài liệu 2."""

def compute_group_coverage(sim_matrix: np.ndarray, selected_indices: list[int], group_indices: list[int]) -> float:
    """Tính toán độ bao phủ Coverage(g) cho một phân họ g cụ thể."""
    pass

def evaluate_intrinsic_metrics(sim_matrix: np.ndarray, selected_indices: list[int], labels: list[str], rare_threshold: int=5) -> dict[str, object]:
    """Tính toán toàn bộ bộ chỉ số nội tại:"""
    pass
```

### <a id="rareprotselect-archive_legacy_code-visualizer-py"></a> RareProtSelect/archive_legacy_code/visualizer.py
- **Đường dẫn:** [`RareProtSelect/archive_legacy_code/visualizer.py`](RareProtSelect/archive_legacy_code/visualizer.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Trực quan hóa Kết quả trong Tài liệu 1 và Module 3.8 (visualizer.py) trong Tài liệu 2."""

class Visualizer:
    """Bộ công cụ trực quan hóa kết quả thực nghiệm chuẩn công bố khoa học."""

    @classmethod
    def plot_coverage_vs_budget(cls, budget_k_list: list[int], metrics_by_method: dict[str, list[float]], output_path: str | Path, title: str='Worst-Group Coverage vs Budget k', metric_name: str='Worst-Group Coverage', dpi: int=300) -> None:
        """Vẽ biểu đồ đường cong độ bao phủ theo các mức ngân sách k."""
        pass

    @classmethod
    def plot_coverage_comparison(cls, budget_k_list: list[int], results_by_method: dict[str, dict[str, list[float]]], output_path: str | Path, dataset_name: str='', dpi: int=300) -> None:
        """Vẽ biểu đồ so sánh đa chỉ số: Overall Coverage, Macro Coverage, Worst-Group Coverage."""
        pass

    @classmethod
    def plot_rare_representation(cls, budget_k_list: list[int], rare_rep_by_method: dict[str, list[float]], output_path: str | Path, dpi: int=300) -> None:
        """Vẽ biểu đồ tỷ lệ nhóm hiếm có đại diện thực thể (Rare Representation Rate)."""
        pass

    @classmethod
    def plot_f1_distribution(cls, f1_scores_by_method: dict[str, list[float]], output_path: str | Path, dpi: int=300) -> None:
        """Vẽ biểu đồ phân bố F1-Score (Boxplot hoặc Violinplot) của các phân họ."""
        pass

    @classmethod
    def plot_runtime_scaling(cls, sizes: list[int], runtimes_by_method: dict[str, list[float]], output_path: str | Path, dpi: int=300) -> None:
        """Vẽ biểu đồ thang đo thời gian thực thi (Runtime Scalability) trên thang log-log hoặc semi-log."""
        pass

    @classmethod
    def plot_confusion_matrix(cls, y_true: list[str], y_pred: list[str], classes: list[str] | None=None, output_path: str | Path='confusion_matrix.png', title: str='Confusion Matrix', dpi: int=300) -> None:
        """Vẽ ma trận nhầm lẫn chuẩn hóa theo hàng."""
        pass

    @classmethod
    def plot_ablation_comparison(cls, results_df: pd.DataFrame, output_path: str | Path, dpi: int=300) -> None:
        """Vẽ biểu đồ bóc tách thành phần (Ablation Study) từ bảng kết quả DataFrame."""
        pass

def plot_coverage_vs_budget(budget_k_list: list[int], metrics_by_method: dict[str, list[float]], output_path: str | Path, title: str='Coverage vs Budget k', metric_name: str='Worst-Group Coverage') -> None:
    pass

def plot_coverage_comparison(budget_k_list: list[int], results_by_method: dict[str, dict[str, list[float]]], output_path: str | Path, dataset_name: str='') -> None:
    pass

def plot_rare_representation(budget_k_list: list[int], rare_rep_by_method: dict[str, list[float]], output_path: str | Path) -> None:
    pass

def plot_f1_distribution(f1_scores_by_method: dict[str, list[float]], output_path: str | Path) -> None:
    pass

def plot_runtime_scaling(sizes: list[int], runtimes_by_method: dict[str, list[float]], output_path: str | Path) -> None:
    pass

def plot_confusion_matrix(y_true: list[str], y_pred: list[str], classes: list[str] | None=None, output_path: str | Path='confusion_matrix.png', title: str='Confusion Matrix') -> None:
    pass

def plot_ablation_comparison(results_df: pd.DataFrame, output_path: str | Path) -> None:
    pass
```

### <a id="rareprotselect-experiments-__init__-py"></a> RareProtSelect/experiments/__init__.py
- **Đường dẫn:** [`RareProtSelect/experiments/__init__.py`](RareProtSelect/experiments/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Experiments module for RareProtSelect benchmarking and validation."""
```

### <a id="rareprotselect-experiments-exp1_baseline_a1a_calibration-py"></a> RareProtSelect/experiments/exp1_baseline_a1a_calibration.py
- **Đường dẫn:** [`RareProtSelect/experiments/exp1_baseline_a1a_calibration.py`](RareProtSelect/experiments/exp1_baseline_a1a_calibration.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 1 trong Tài liệu 1 và Module 1 trong Tài liệu 2:"""

def run_pruned_greedy_1000_shuffles(sim_matrix: np.ndarray, seq_ids: list[str], prune_threshold: float=0.9, num_shuffles: int=1000, seed: int=42, budget_per_shuffle: int=15, cache_path: Path | None=None, force_recompute: bool=False) -> tuple[list[str], pd.DataFrame]:
    """Cài đặt chính xác 100% thuật toán 1,000-Shuffle Consensus Ranking từ Greedy.R (Nguyen et al., 2025):"""
    pass

def load_published_fig8a_benchmark(csv_path: Path) -> dict[int, float]:
    """Đọc tệp CSV Nguồn sự thật (SSOT) chứa 11 mốc ước lượng từ Hình 8 Panel A (Nguyen et al., 2025)."""
    pass

def run_exp1_baseline_a1a_calibration(config_path: str='configs/config_exp1_baseline_a1a_calibration.yaml', force_recompute: bool=False, override_shuffles: int | None=None) -> dict[str, object]:
    """Thực thi kịch bản Nhánh 1: Tái hiện Hình 8 Bài báo gốc trên Peptidase A1 (MEROPS A1A)."""
    pass

def main() -> None:
    pass
```

### <a id="rareprotselect-experiments-exp2_rare_weighted_a1a-py"></a> RareProtSelect/experiments/exp2_rare_weighted_a1a.py
- **Đường dẫn:** [`RareProtSelect/experiments/exp2_rare_weighted_a1a.py`](RareProtSelect/experiments/exp2_rare_weighted_a1a.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 2.1, 2.2, 2.3, 2.4 trong Tài liệu 1 và Module 4.4 trong Tài liệu 2:"""

def evaluate_rare_aware_representatives(selected_ids: list[str], id_to_record: dict[str, ProteinRecord], seq_ids: list[str], id_to_family: dict[str, str], family_to_ids: dict[str, list[str]], rare_subfamilies: list[str], blast_calc: BLASTSimilarityMatrix, db_prefix: Path, tmpdir: Path, k_val: int, live_evalue: float=1e-07, live_max_targets: int=999999, live_threads: int=24, precomputed_hit_pairs: set[tuple[str, str]] | None=None) -> dict[str, int | float]:
    """Đo đạc Live BLASTp theo cơ chế Truy vấn ngược nội phân họ (Within-Subfamily Representative Query:"""
    pass

def run_exp2_rare_weighted_a1a(config_path: str='configs/config_exp2_rare_weighted_a1a.yaml', force_recompute: bool=False, override_shuffles: int | None=None) -> dict[str, object]:
    """Thực thi toàn bộ pipeline Nhánh 2: Khảo sát 3 mức alpha trên 20 mốc k (đến 115) với Pruned Greedy và Live BLASTp Nội Phân Họ."""
    pass

def main() -> None:
    pass
```

### <a id="rareprotselect-experiments-exp3_esm_coverage_a1a-py"></a> RareProtSelect/experiments/exp3_esm_coverage_a1a.py
- **Đường dẫn:** [`RareProtSelect/experiments/exp3_esm_coverage_a1a.py`](RareProtSelect/experiments/exp3_esm_coverage_a1a.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 3.1, 3.2, 3.3, 3.4 trong Tài liệu 1 và Module 4.6 trong Tài liệu 2:"""

def evaluate_esm_coverage_representatives(selected_indices: list[int], sim_matrix: np.ndarray, family_to_indices: dict[str, list[int]], rare_subfamilies: list[str], k_val: int, total_cleaned: int) -> dict[str, float | int]:
    """Đo đạc trực tiếp 4 chỉ số Độ bao phủ ngữ nghĩa liên tục nội phân họ (Within-Subfamily Coverage ESM %)"""
    pass

def run_exp3_esm_coverage_a1a(config_path: str='configs/config_exp3_esm_coverage_a1a.yaml', force_recompute: bool=False, override_shuffles: int | None=None) -> dict[str, object]:
    """Thực thi toàn bộ pipeline Nhánh 3: Khảo sát 3 mức alpha trên 20 mốc k (đến 115) trong không gian ESM-2 Mean-Centered Cosine."""
    pass

def main() -> None:
    pass
```

### <a id="rareprotselect-experiments-exp4_cross_eval_a1a-py"></a> RareProtSelect/experiments/exp4_cross_eval_a1a.py
- **Đường dẫn:** [`RareProtSelect/experiments/exp4_cross_eval_a1a.py`](RareProtSelect/experiments/exp4_cross_eval_a1a.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 4.1, 4.2, 4.3 trong Tài liệu 1 và Module 4.8 trong Tài liệu 2:"""

def load_cached_consensus_ids(cache_file: Path, expected_budget: int=115) -> list[str]:
    """Nạp danh sách đại diện đồng thuận 1,000 lần xáo trộn từ tệp cache .npz của Nhánh 2 hoặc Nhánh 3."""
    pass

def evaluate_rare_aware_representatives(selected_ids: list[str], id_to_record: dict[str, ProteinRecord], seq_ids: list[str], id_to_family: dict[str, str], family_to_ids: dict[str, list[str]], rare_subfamilies: list[str], blast_calc: BLASTSimilarityMatrix, db_prefix: Path, tmpdir: Path, k_val: int, live_evalue: float=1e-07, live_max_targets: int=999999, live_threads: int=24, precomputed_hit_pairs: set[tuple[str, str]] | None=None) -> dict[str, float | int]:
    """Đo đạc Live BLASTp thực tế (E <= 1e-7) theo cơ chế Truy vấn ngược nội phân họ (S_k cap V_g -> V_g)"""
    pass

def evaluate_esm_coverage_representatives(selected_indices: list[int], sim_matrix: np.ndarray, family_to_indices: dict[str, list[int]], rare_subfamilies: list[str], k_val: int, total_cleaned: int) -> dict[str, float | int]:
    """Đo đạc trực tiếp 4 chỉ số Độ bao phủ ngữ nghĩa liên tục nội phân họ (Within-Subfamily Coverage ESM %)"""
    pass

def verify_diagonal_consistency(df_exp4: pd.DataFrame, exp2_csv_path: Path, exp3_csv_path: Path) -> None:
    """Kiểm định tính toàn vẹn 100.00% của 2 ô đường chéo so với kết quả Nhánh 2 và Nhánh 3."""
    pass

def plot_exp4_figures(df_all: pd.DataFrame, alphas: list[float], budget_k_list: list[int], figures_dir: Path, total_subfamilies: int=115, total_rare: int=45) -> tuple[Path, Path, Path]:
    """Vẽ và xuất hệ thống 3 biểu đồ đối đầu trực diện giữa BLASTp-Selected và ESM2-Selected (PNG & SVG)."""
    pass

def run_exp4_cross_eval_a1a(config_path: str='configs/config_exp4_cross_eval_a1a.yaml', force_recompute: bool=False) -> dict[str, object]:
    """Thực thi toàn bộ pipeline Nhánh 4: Kiểm tra chéo 2x2 nội phân họ giữa BLASTp-Selected và ESM2-Selected trên 20 mốc k và 3 mức alpha."""
    pass

def main() -> None:
    pass
```

### <a id="rareprotselect-experiments-exp5_subfamily_allocation_a1a-py"></a> RareProtSelect/experiments/exp5_subfamily_allocation_a1a.py
- **Đường dẫn:** [`RareProtSelect/experiments/exp5_subfamily_allocation_a1a.py`](RareProtSelect/experiments/exp5_subfamily_allocation_a1a.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 5.1, 5.2, 5.3 trong Tài liệu 1 và Mục 4.10 trong Tài liệu 2:"""
EXPECTED_COLUMNS: list[str]

def load_cached_consensus_ids(cache_file: Path, expected_budget: int=115) -> list[str]:
    """Nạp danh sách đại diện đồng thuận 1,000 lần xáo trộn từ tệp cache .npz của Nhánh 2 hoặc Nhánh 3."""
    pass

def evaluate_subfamily_allocation_metrics(selected_ids: list[str], id_to_family: dict[str, str], total_subfamilies: int, rare_subfamilies_set: set[str], dominant_subfamily_id: str='A01.009') -> dict[str, int | float]:
    """Đo đạc trực tiếp Bộ 4 chỉ số tỷ lệ phần trăm (%) và 4 cột số đếm nguyên (count)"""
    pass

def verify_exp5_mathematical_invariants(df: pd.DataFrame, total_subfamilies: int=115, total_rare: int=45) -> None:
    """Kiểm định tự động (Sanity Check) 3 bất biến toán học trên toàn bộ 120 dòng của bảng kết quả Nhánh 5."""
    pass

def plot_exp5_allocation_metrics_vs_k(df: pd.DataFrame, alphas: list[float], budget_k_list: list[int], output_png: Path, output_svg: Path, total_subfamilies: int=115, total_rare: int=45) -> None:
    """Vẽ Hình 5.1 (1 ảnh 4 góc 2x2): Diễn tiến 4 chỉ số tỷ lệ % theo ngân sách k in [1..115]"""
    pass

def plot_exp5_allocation_summary_k11_k76(df: pd.DataFrame, alphas: list[float], output_png: Path, output_svg: Path, k_max: int=115, total_subfamilies: int=115, total_rare: int=45) -> None:
    """Vẽ Hình 5.2 (1 ảnh 4 góc 2x2): Biểu đồ cột ghép (4 cột tại mỗi mức alpha:"""
    pass

def log_strategic_milestone_summary(df: pd.DataFrame, milestones: tuple[int, ...]=(11, 115)) -> None:
    """In bảng đối chiếu tóm tắt toàn bộ 6 phương pháp tại các mốc ngân sách chiến lược (k=11 và k=115) ra màn hình console."""
    pass

def run_exp5_subfamily_allocation_a1a(config_path: str | Path='configs/config_exp5_subfamily_allocation_a1a.yaml') -> dict[str, object]:
    """Điều phối toàn bộ quy trình thực nghiệm Nhánh 5."""
    pass

def main() -> None:
    """Điểm vào CLI nhận tham số --config và kích hoạt run_exp5_subfamily_allocation_a1a."""
    pass
```

### <a id="rareprotselect-src-__init__-py"></a> RareProtSelect/src/__init__.py
- **Đường dẫn:** [`RareProtSelect/src/__init__.py`](RareProtSelect/src/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Cấu trúc Gói phần mềm trong Tài liệu 1 và Module 3 trong Tài liệu 2."""
```

### <a id="rareprotselect-src-config-__init__-py"></a> RareProtSelect/src/config/__init__.py
- **Đường dẫn:** [`RareProtSelect/src/config/__init__.py`](RareProtSelect/src/config/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Quản lý Cấu hình trong Tài liệu 1 và Module 3.1 trong Tài liệu 2."""
```

### <a id="rareprotselect-src-config-settings-py"></a> RareProtSelect/src/config/settings.py
- **Đường dẫn:** [`RareProtSelect/src/config/settings.py`](RareProtSelect/src/config/settings.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Quản lý Cấu hình trong Tài liệu 1 và Module 3.1 trong Tài liệu 2."""

@dataclass
class PathConfig:
    """Cấu hình đường dẫn tệp tin và thư mục dữ liệu/kết quả."""
    fasta_path: str
    benchmark_gold_path: str | None
    output_dir: str
    cache_dir: str
    similarity_cache_dir: str
    figures_dir: str
    tables_dir: str
    logs_dir: str

@dataclass
class QualityFilterConfig:
    """Cấu hình tiêu chí kiểm soát chất lượng chuỗi protein (QC)."""
    min_seq_len: int
    max_seq_len: int
    max_ambiguous_ratio: float
    deduplicate: bool

@dataclass
class ModelConfig:
    """Cấu hình mô hình ngôn ngữ protein (ESM-2) và phần cứng."""
    model_name: str
    device: str
    batch_size: int

@dataclass
class OptimizationConfig:
    """Cấu hình thuật toán chọn tập đại diện submodular và trọng số."""
    budget_k_list: list[int]
    weighting_scheme: str
    weighting_alpha: float

@dataclass
class EvaluationConfig:
    """Cấu hình đánh giá khoa học và phân định nhóm hiếm."""
    rare_threshold: int
    seed: int

@dataclass
class PlotConfig:
    """Cấu hình trực quan hóa đồ thị."""
    dpi: int
    fig_format: str
    style: str

@dataclass
class ExperimentConfig:
    """Cấu hình toàn diện cho một thực nghiệm của RareProtSelect."""
    dataset_name: str
    fasta_path: str
    benchmark_gold_path: str | None
    model_name: str
    device: str
    batch_size: int
    budget_k_list: list[int]
    weighting_scheme: str
    weighting_alpha: float
    rare_threshold: int
    min_seq_len: int
    max_seq_len: int
    max_ambiguous_ratio: float
    exclude_unknown_subfamilies: bool
    output_dir: str
    cache_dir: str
    seed: int
    extra_params: dict[str, object]

    def get_path_config(self) -> PathConfig:
        """Tạo đối tượng PathConfig từ cấu hình thực nghiệm."""
        pass

    def get_quality_config(self) -> QualityFilterConfig:
        """Tạo đối tượng QualityFilterConfig từ cấu hình thực nghiệm."""
        pass

    def get_model_config(self) -> ModelConfig:
        """Tạo đối tượng ModelConfig từ cấu hình thực nghiệm."""
        pass

    def get_optimization_config(self) -> OptimizationConfig:
        """Tạo đối tượng OptimizationConfig từ cấu hình thực nghiệm."""
        pass

    def get_evaluation_config(self) -> EvaluationConfig:
        """Tạo đối tượng EvaluationConfig từ cấu hình thực nghiệm."""
        pass

    def to_dict(self) -> dict[str, object]:
        """Chuyển đổi cấu hình thành từ điển."""
        pass

def load_config(yaml_path: str | Path) -> ExperimentConfig:
    """Nạp cấu hình từ tệp YAML và khởi tạo đối tượng ExperimentConfig."""
    pass

def validate_config(config: ExperimentConfig) -> bool:
    """Kiểm tra tính hợp lệ toán học và logic của các tham số cấu hình."""
    pass
```

### <a id="rareprotselect-src-data-__init__-py"></a> RareProtSelect/src/data/__init__.py
- **Đường dẫn:** [`RareProtSelect/src/data/__init__.py`](RareProtSelect/src/data/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Tiền xử lý Dữ liệu trong Tài liệu 1 và Module 3.2 trong Tài liệu 2."""
```

### <a id="rareprotselect-src-data-annotation_mapper-py"></a> RareProtSelect/src/data/annotation_mapper.py
- **Đường dẫn:** [`RareProtSelect/src/data/annotation_mapper.py`](RareProtSelect/src/data/annotation_mapper.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 1.3 trong Tài liệu 1 và Module 3.2 (annotation_mapper.py) trong Tài liệu 2."""

@dataclass
class AnnotationMapping:
    """Đối tượng chứa thông tin ánh xạ nhãn phân họ và thống kê kích thước nhóm."""
    label_map: dict[str, str]
    subfamily_counts: dict[str, int]
    rare_subfamilies: list[str]
    major_subfamilies: list[str]
    medium_subfamilies: list[str]
    singleton_subfamilies: list[str]
    imbalance_ratio: float

class AnnotationMapper:
    """Bộ trích xuất và ánh xạ nhãn phân loại học / phân họ protein."""
    UNKNOWN_LABELS: frozenset[str]

    @staticmethod
    def is_unknown_label(label: str) -> bool:
        """Kiểm tra xem nhãn phân họ có thuộc nhóm chưa định danh (Unknown / UPA) hay không."""
        pass

    @staticmethod
    def extract_merops_subfamily(header: str) -> str:
        """Trích xuất mã phân họ định danh [A01.xxx] từ header MEROPS A1A."""
        pass

    @staticmethod
    def extract_ce_subfamily(header: str) -> str:
        """Trích xuất mã nhóm phụ /Fxx/ từ header Carboxylesterase (ESTHER)."""
        pass

    @staticmethod
    def extract_thyme_family(header: str, seq_id: str, mapping_table: dict[str, str] | None=None) -> str:
        """Trích xuất họ Thioesterase (TE1-TE27) từ bảng ánh xạ hoặc header."""
        pass

    @classmethod
    def extract_merops_subfamilies(cls, records: list[ProteinRecord]) -> dict[str, str]:
        """Trích xuất toàn bộ nhãn phân họ cho tập bản ghi MEROPS."""
        pass

    @classmethod
    def extract_ce_subgroups(cls, records: list[ProteinRecord]) -> dict[str, str]:
        """Trích xuất toàn bộ nhãn nhóm phụ cho tập bản ghi Carboxylesterase."""
        pass

    @classmethod
    def extract_thyme_families(cls, records: list[ProteinRecord], mapping_table: dict[str, str] | None=None) -> dict[str, str]:
        """Trích xuất toàn bộ nhãn họ cho tập bản ghi Thioesterase."""
        pass

    @staticmethod
    def compute_family_statistics(label_map: dict[str, str]) -> dict[str, int]:
        """Đếm số lượng thành viên n_g của từng phân họ."""
        pass

    @staticmethod
    def identify_rare_families(subfamily_counts: dict[str, int], threshold: int=5) -> list[str]:
        """Xác định danh sách các phân họ hiếm (n_g <= threshold)."""
        pass

    @classmethod
    def get_subfamily_statistics(cls, label_map: dict[str, str], rare_threshold: int=5) -> dict[str, object]:
        """Tính toán thống kê chi tiết cấu trúc phân họ và độ mất cân bằng."""
        pass

    @classmethod
    def map_annotations(cls, records: list[ProteinRecord], dataset_name: str, mapping_table: dict[str, str] | None=None, rare_threshold: int=5) -> AnnotationMapping:
        """Ánh xạ nhãn tự động dựa trên tên tập dữ liệu."""
        pass

def extract_merops_subfamilies(records: list[ProteinRecord]) -> dict[str, str]:
    """Trích xuất mã phân họ [A01.xxx] từ header MEROPS A1A."""
    pass

def extract_ce_subgroups(records: list[ProteinRecord]) -> dict[str, str]:
    """Trích xuất mã nhóm /Fxx/ từ header Carboxylesterase."""
    pass

def extract_thyme_families(records: list[ProteinRecord], mapping_table: dict[str, str] | None=None) -> dict[str, str]:
    """Trích xuất họ TE từ header hoặc bảng ánh xạ."""
    pass

def get_subfamily_statistics(label_map: dict[str, str], rare_threshold: int=5) -> dict[str, object]:
    """Đếm số lượng thành viên n_g của từng phân họ và xác định nhóm hiếm."""
    pass
```

### <a id="rareprotselect-src-data-dataset_loader-py"></a> RareProtSelect/src/data/dataset_loader.py
- **Đường dẫn:** [`RareProtSelect/src/data/dataset_loader.py`](RareProtSelect/src/data/dataset_loader.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Tích hợp Giai đoạn 1 trong Tài liệu 1 và Module 3.2 (dataset_loader.py) trong Tài liệu 2."""

@dataclass
class DatasetBundle:
    """Tập hợp dữ liệu đã qua tiền xử lý, kiểm định chất lượng và ánh xạ nhãn."""
    records: list[ProteinRecord]
    cleaned_records: list[ProteinRecord]
    label_map: dict[str, str]
    subfamily_counts: dict[str, int]
    rare_subfamilies: list[str]
    qc_stats: dict[str, int | float | str | bool]

    @property
    def num_raw(self) -> int:
        pass

    @property
    def num_cleaned(self) -> int:
        pass

    @property
    def num_subfamilies(self) -> int:
        pass

    @property
    def num_rare_subfamilies(self) -> int:
        pass

class DatasetLoader:
    """Bộ nạp và tiền xử lý toàn diện cho dữ liệu protein."""

    @staticmethod
    def resolve_path(path_str: str) -> Path:
        """Chuẩn hóa và tìm kiếm đường dẫn tệp tin thực tế."""
        pass

    @classmethod
    def load_and_preprocess_dataset(cls, config: ExperimentConfig | Path | str, mapping_table: dict[str, str] | None=None, override_fasta: str | Path | None=None, override_dataset_name: str | None=None, exclude_unknown_subfamilies: bool | None=None) -> DatasetBundle:
        """Thực thi pipeline Giai đoạn 1: Đọc FASTA -> Lọc QC -> Ánh xạ phân họ (& lọc bỏ Unknown nếu Phương án 3B)."""
        pass

def load_dataset_pipeline(config: ExperimentConfig | Path | str, mapping_table: dict[str, str] | None=None, override_fasta: str | Path | None=None, override_dataset_name: str | None=None, exclude_unknown_subfamilies: bool | None=None) -> DatasetBundle:
    """Nạp và tiền xử lý toàn diện tập dữ liệu theo cấu hình ExperimentConfig."""
    pass
```

### <a id="rareprotselect-src-data-fasta_parser-py"></a> RareProtSelect/src/data/fasta_parser.py
- **Đường dẫn:** [`RareProtSelect/src/data/fasta_parser.py`](RareProtSelect/src/data/fasta_parser.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 1.1 trong Tài liệu 1 và Module 3.2 (fasta_parser.py) trong Tài liệu 2."""

@dataclass
class ProteinRecord:
    """Đối tượng biểu diễn một bản ghi protein chuẩn hóa từ tệp FASTA."""
    id: str
    sequence: str
    header: str
    length: int

    def __repr__(self) -> str:
        pass

class FastaParser:
    """Bộ phân tích cú pháp tệp FASTA sinh học."""

    @staticmethod
    def parse_header(header_line: str) -> tuple[str, str]:
        """Bóc tách định danh duy nhất (id) và phần mô tả từ dòng header FASTA."""
        pass

    @staticmethod
    def remove_gaps(sequence: str) -> str:
        """Loại bỏ ký tự khoảng trắng, dấu gạch ngang alignment (-), dấu chấm (.)."""
        pass

    @classmethod
    def dewrap(cls, sequence: str) -> str:
        """Nối các dòng chuỗi bị ngắt, khử khoảng trắng và chuẩn hóa thành chữ hoa."""
        pass

    @classmethod
    def read_fasta(cls, file_path: str | Path) -> list[ProteinRecord]:
        """Đọc tệp FASTA thô và chuyển đổi thành danh sách ProteinRecord chuẩn hóa."""
        pass

    @staticmethod
    def write_fasta(records: list[ProteinRecord], output_path: str | Path, line_wrap: int=60) -> None:
        """Ghi danh sách ProteinRecord ra tệp FASTA chuẩn."""
        pass

def parse_fasta(file_path: str | Path) -> list[ProteinRecord]:
    """Đọc tệp FASTA thô và chuyển đổi thành danh sách ProteinRecord chuẩn hóa."""
    pass
```

### <a id="rareprotselect-src-data-quality_filter-py"></a> RareProtSelect/src/data/quality_filter.py
- **Đường dẫn:** [`RareProtSelect/src/data/quality_filter.py`](RareProtSelect/src/data/quality_filter.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 1.2 trong Tài liệu 1 và Module 3.2 (quality_filter.py) trong Tài liệu 2."""

@dataclass
class QualityFilterResult:
    """Kết quả kiểm soát chất lượng (QC) cho tập protein."""
    cleaned_records: list[ProteinRecord]
    qc_stats: dict[str, int | float]

class QualityFilter:
    """Bộ kiểm soát chất lượng chuỗi protein (Quality Control)."""

    def __init__(self, min_len: int=30, max_len: int=2000, max_ambiguous_ratio: float=0.05, deduplicate: bool=True) -> None:
        pass

    def filter_sequences(self, records: list[ProteinRecord]) -> QualityFilterResult:
        """Lọc bỏ các chuỗi rác, phân mảnh hoặc chứa quá nhiều ký tự lạ."""
        pass

def filter_proteins(records: list[ProteinRecord], min_len: int=30, max_len: int=2000, max_ambiguous_ratio: float=0.05, deduplicate: bool=True) -> tuple[list[ProteinRecord], dict[str, int | float]]:
    """Lọc bỏ các chuỗi rác, phân mảnh hoặc chứa quá nhiều ký tự lạ."""
    pass
```

### <a id="rareprotselect-src-selection-__init__-py"></a> RareProtSelect/src/selection/__init__.py
- **Đường dẫn:** [`RareProtSelect/src/selection/__init__.py`](RareProtSelect/src/selection/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Module chọn tập đại diện Submodular cho Topic 2."""
```

### <a id="rareprotselect-src-selection-base-py"></a> RareProtSelect/src/selection/base.py
- **Đường dẫn:** [`RareProtSelect/src/selection/base.py`](RareProtSelect/src/selection/base.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 4.1 trong Tài liệu 1 và Module 3.6 (base.py) trong Tài liệu 2."""

@dataclass
class SelectionResult:
    """Cấu trúc dữ liệu chứa kết quả đầu ra chuẩn mực của thuật toán chọn tập đại diện Submodular."""
    selected_indices: list[int]
    selected_ids: list[str]
    marginal_gains: list[float]
    objective_history: list[float]
    total_evaluations: int
    runtime_seconds: float

    def to_dict(self) -> dict[str, object]:
        """Chuyển đổi kết quả sang từ điển Python."""
        pass

class BaseSubmodularSelector(ABC):
    """Lớp cơ sở trừu tượng quy định giao diện chuẩn cho mọi bộ chọn tập đại diện Submodular."""

    @abstractmethod
    def select(self, budget_k: int) -> SelectionResult:
        """Thực thi thuật toán chọn k protein đại diện tối ưu."""
        pass
```

### <a id="rareprotselect-src-selection-pruned_greedy-py"></a> RareProtSelect/src/selection/pruned_greedy.py
- **Đường dẫn:** [`RareProtSelect/src/selection/pruned_greedy.py`](RareProtSelect/src/selection/pruned_greedy.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 2.1, 2.2 trong Tài liệu 1 và Module 3.4 trong Tài liệu 2:"""

def compute_subfamily_weights(seq_ids: list[str], id_to_family: dict[str, str], alpha: float) -> np.ndarray:
    """Tính toán vector trọng số mẫu w_v = (n_{g(v)})^(-alpha) cho từng protein."""
    pass

def run_pruned_greedy_1000_shuffles(sim_matrix: np.ndarray, seq_ids: list[str], prune_threshold: float=0.9, num_shuffles: int=1000, sample_weights: np.ndarray | None=None, seed: int=42, budget_per_shuffle: int=76, cache_path: Path | None=None, force_recompute: bool=False, desc_label: str='Pruned Greedy', show_progress: bool=True) -> tuple[list[str], pd.DataFrame]:
    """Cài đặt thuật toán 1,000-Shuffle Consensus Ranking có trọng số mẫu:"""
    pass
```

### <a id="rareprotselect-src-selection-standard_greedy-py"></a> RareProtSelect/src/selection/standard_greedy.py
- **Đường dẫn:** [`RareProtSelect/src/selection/standard_greedy.py`](RareProtSelect/src/selection/standard_greedy.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 4.3 trong Tài liệu 1 và Module 3.6 (standard_greedy.py) trong Tài liệu 2."""

class StandardGreedySolver(BaseSubmodularSelector):
    """Bộ giải tối ưu hóa Submodular Facility Location bằng Standard Greedy (Vét cạn O(k*n^2))."""

    def __init__(self, sim_matrix: np.ndarray, weights: np.ndarray | None=None, seq_ids: list[str] | None=None, prune_threshold: float | None=None) -> None:
        """Khởi tạo StandardGreedySelector."""
        pass

    def select(self, budget_k: int) -> SelectionResult:
        """Thực thi thuật toán Standard Greedy (quét vét cạn O(k*n^2)) để chọn k protein đại diện."""
        pass

def standard_greedy_facility_location(sim_matrix: np.ndarray, weights: np.ndarray, budget_k: int, seq_ids: list[str] | None=None, prune_threshold: float | None=None) -> tuple[list[int], list[float], list[float]]:
    """Thuật toán Standard Greedy gốc (quét vét cạn O(k*n^2) mỗi bước)."""
    pass
```

### <a id="rareprotselect-src-selection-unweighted_selector-py"></a> RareProtSelect/src/selection/unweighted_selector.py
- **Đường dẫn:** [`RareProtSelect/src/selection/unweighted_selector.py`](RareProtSelect/src/selection/unweighted_selector.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Phương pháp Nền (Unweighted Facility Location - Nguyen et al., 2025)."""

class UnweightedFLSelector(BaseSubmodularSelector):
    """Bộ chọn tập đại diện Unweighted Facility Location (Mô hình nền - Nguyen et al., 2025)."""

    def __init__(self, sim_matrix: np.ndarray, seq_ids: list[str] | None=None, solver: Literal['standard', 'lazy']='standard') -> None:
        """Khởi tạo UnweightedFLSelector."""
        pass

    def select(self, budget_k: int) -> SelectionResult:
        """Thực thi chọn k protein đại diện theo mô hình Unweighted Facility Location."""
        pass
```

### <a id="rareprotselect-src-similarity-__init__-py"></a> RareProtSelect/src/similarity/__init__.py
- **Đường dẫn:** [`RareProtSelect/src/similarity/__init__.py`](RareProtSelect/src/similarity/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 2 và Công đoạn 3.1 trong Tài liệu 1 và Module 3.3 trong Tài liệu 2."""
```

### <a id="rareprotselect-src-similarity-blast_similarity-py"></a> RareProtSelect/src/similarity/blast_similarity.py
- **Đường dẫn:** [`RareProtSelect/src/similarity/blast_similarity.py`](RareProtSelect/src/similarity/blast_similarity.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 3.3 trong Tài liệu 1 và Module 3.4.2 (blast_similarity.py) trong Tài liệu 2."""

class BLASTSimilarityMatrix:
    """Xây dựng ma trận độ nhận dạng chuỗi (Sequence Identity) bằng NCBI BLASTp nguyên bản"""

    def __init__(self, blastp_bin_path: str | Path | None=None, evalue: float=0.05, max_target_seqs: int=100, word_size: int=3, num_threads: int=24, cache_dir: str | Path='outputs/similarity_cache') -> None:
        """Khởi tạo cấu hình bộ sinh ma trận BLASTp."""
        pass

    def find_blastp_binary(self) -> Path:
        """Tự động phát hiện vị trí của blastp executable."""
        pass

    def find_makeblastdb_binary(self) -> Path:
        """Tự động phát hiện vị trí của makeblastdb executable."""
        pass

    def run_all_vs_all_blastp(self, fasta_path: Path, output_tsv: Path, use_db: bool=True) -> Path:
        """Thực thi căn chỉnh All-vs-All bằng blastp."""
        pass

    def build_matrix_from_tsv(self, tsv_path: Path, seq_ids: list[str]) -> np.ndarray:
        """Đọc tệp kết quả TSV của blastp và xây dựng ma trận tương đồng vuông (N, N)."""
        pass

    def get_similarity_matrix(self, fasta_path: Path | str, seq_ids: list[str], dataset_name: str, force_recompute: bool=False, use_db: bool=True) -> np.ndarray:
        """Phương thức giao tiếp chính: Quản lý cache và sinh ma trận tương đồng BLASTp."""
        pass

    def build_blast_db(self, fasta_path: Path | str, db_prefix: Path | str | None=None) -> Path:
        """Tạo chỉ mục cơ sở dữ liệu protein bằng makeblastdb phục vụ tìm kiếm đa luồng."""
        pass

    def retrieve_blast_hits(self, query_fasta: Path | str, db_prefix: Path | str, evalue: float=1e-07, max_target_seqs: int=999999, num_threads: int | None=None) -> set[str]:
        """Thực thi blastp dùng query_fasta truy xuất trên indexed database, trả về tập ID có hit hợp lệ."""
        pass

    def retrieve_blast_hit_pairs(self, query_fasta: Path | str, db_prefix: Path | str, evalue: float=1e-07, max_target_seqs: int=999999, num_threads: int | None=None) -> set[tuple[str, str]]:
        """Thực thi blastp dùng query_fasta truy xuất trên indexed database, trả về tập cặp (qseqid, sseqid)"""
        pass
```

### <a id="rareprotselect-src-similarity-dense_similarity-py"></a> RareProtSelect/src/similarity/dense_similarity.py
- **Đường dẫn:** [`RareProtSelect/src/similarity/dense_similarity.py`](RareProtSelect/src/similarity/dense_similarity.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 3.1 trong Tài liệu 1 và Module 3.3 (dense_similarity.py) trong Tài liệu 2."""

def compute_cosine_similarity_matrix(normalized_embeddings: np.ndarray) -> np.ndarray:
    """Tính ma trận tương đồng Cosine không âm: Sim(u, v) = max(0, z(u)^T @ z(v))."""
    pass

def compute_mean_centered_cosine_matrix(raw_embeddings: np.ndarray, beta: float=0.7) -> np.ndarray:
    """Tính ma trận tương đồng Partial Mean-Centered Cosine không âm trên không gian ESM-2:"""
    pass

class DenseSimilarity:
    """Bộ tính toán Không gian Tương đồng Ngữ nghĩa Cosine Đầy đủ (Dense Similarity Space)."""

    def __init__(self) -> None:
        pass

    def compute_similarity_matrix(self, normalized_embeddings: np.ndarray) -> np.ndarray:
        """Tính ma trận tương đồng Cosine không âm từ tập vector nhúng L2-normalized."""
        pass

    def compute_pairwise_similarity(self, z1: np.ndarray, z2: np.ndarray) -> float:
        """Tính độ tương đồng Cosine không âm giữa hai vector protein đơn lẻ."""
        pass

class ESM2SimilarityMatrix:
    """Quản lý nạp vector nhúng ESM-2, chuẩn hóa Partial Mean-Centered Cosine và lưu đệm ma trận tương đồng."""

    def __init__(self, model_name: str='facebook/esm2_t12_35M_UR50D', embeddings_cache_dir: str | Path='outputs/embeddings_cache', similarity_cache_dir: str | Path='outputs/similarity_cache', batch_size: int=16, device: str='auto', center_shift_beta: float=0.7) -> None:
        pass

    def load_or_extract_embeddings(self, records: list[object], dataset_name: str, force_recompute: bool=False) -> np.ndarray:
        """Nạp ma trận nhúng (N, D) từ outputs/embeddings_cache/{dataset_name}_{model_slug}.npy"""
        pass

    def get_similarity_matrix(self, records: list[object], seq_ids: list[str], dataset_name: str, force_recompute: bool=False) -> np.ndarray:
        """Nạp hoặc tính toán ma trận tương đồng Partial Mean-Centered Cosine (N, N) kiểu float32,"""
        pass
```

### <a id="rareprotselect-src-utils-__init__-py"></a> RareProtSelect/src/utils/__init__.py
- **Đường dẫn:** [`RareProtSelect/src/utils/__init__.py`](RareProtSelect/src/utils/__init__.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Tiện ích Hệ thống trong Tài liệu 1 và Module 3.5 trong Tài liệu 2."""
```

### <a id="rareprotselect-src-utils-exporter-py"></a> RareProtSelect/src/utils/exporter.py
- **Đường dẫn:** [`RareProtSelect/src/utils/exporter.py`](RareProtSelect/src/utils/exporter.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Xuất Báo cáo Thực nghiệm trong Tài liệu 1 và Module 3.8 (exporter.py) trong Tài liệu 2."""

class NumpyJSONEncoder(json.JSONEncoder):
    """JSON Encoder hỗ trợ chuyển đổi các kiểu dữ liệu Numpy và Pandas."""

    def default(self, obj: object) -> object:
        pass

class ResultExporter:
    """Bộ công cụ xuất dữ liệu và báo cáo kết quả thực nghiệm đa định dạng (CSV, JSON, Markdown, LaTeX)."""

    @classmethod
    def export_to_csv(cls, data: list[dict[str, object]] | pd.DataFrame, output_path: str | Path) -> None:
        """Xuất kết quả ra tệp CSV."""
        pass

    @classmethod
    def export_to_json(cls, data: dict[str, object] | list[object], output_path: str | Path, indent: int=2) -> None:
        """Xuất kết quả ra tệp JSON."""
        pass

    @classmethod
    def export_to_markdown(cls, df: pd.DataFrame, output_path: str | Path, title: str='Experimental Results') -> None:
        """Xuất bảng kết quả ra tệp Markdown (.md) cho báo cáo khoa học."""
        pass

    @classmethod
    def export_summary_table(cls, results: list[dict[str, object]], output_base_path: str | Path, title: str='Summary Table') -> None:
        """Xuất đồng thời ra CSV, JSON và Markdown."""
        pass

    @classmethod
    def export_dataframe(cls, df: pd.DataFrame, csv_path: str | Path, json_path: str | Path, markdown_path: str | Path, title: str='Experimental Results') -> None:
        """Xuất đồng thời DataFrame ra cả 3 định dạng: CSV, JSON và Markdown."""
        pass

def export_results_to_csv(data: list[dict] | pd.DataFrame, output_path: str) -> None:
    """Xuất kết quả ra tệp CSV."""
    pass

def export_results_to_json(data: dict | list, output_path: str) -> None:
    """Xuất kết quả ra tệp JSON."""
    pass

def export_results_to_markdown(df: pd.DataFrame, output_path: str, title: str='Experimental Results') -> None:
    """Xuất bảng kết quả ra Markdown."""
    pass

def export_summary_table(results: list[dict], output_path: str, title: str='Summary Table') -> None:
    """Xuất bảng tổng hợp kết quả."""
    pass
```

### <a id="rareprotselect-src-utils-timer-py"></a> RareProtSelect/src/utils/timer.py
- **Đường dẫn:** [`RareProtSelect/src/utils/timer.py`](RareProtSelect/src/utils/timer.py)
- **Ngôn ngữ:** `python`

```python
"""Thực hiện Công đoạn 5.3 trong Tài liệu 1 và Module 3.8 (timer.py) trong Tài liệu 2."""

class Timer:
    """Công cụ bấm giờ có độ chính xác cao bằng time.perf_counter()."""

    def __init__(self, name: str='Task', auto_log: bool=False) -> None:
        pass

    def start(self) -> Timer:
        """Bắt đầu tính giờ."""
        pass

    def stop(self) -> float:
        """Dừng tính giờ và trả về thời gian thực thi (giây)."""
        pass

    @property
    def elapsed_seconds(self) -> float:
        """Thời gian trôi qua tính bằng giây."""
        pass

    @property
    def elapsed_ms(self) -> float:
        """Thời gian trôi qua tính bằng mili-giây (ms)."""
        pass

    def __enter__(self) -> Timer:
        pass

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None) -> None:
        pass

def timeit(name: str | None=None, auto_log: bool=True) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator đo thời gian chạy của hàm."""
    pass
```

### <a id="rareprotselect-tools-blast-bin-cleanup-blastdb-volumes-py"></a> RareProtSelect/tools/blast/bin/cleanup-blastdb-volumes.py
- **Đường dẫn:** [`RareProtSelect/tools/blast/bin/cleanup-blastdb-volumes.py`](RareProtSelect/tools/blast/bin/cleanup-blastdb-volumes.py)
- **Ngôn ngữ:** `python`

```python
"""# $Id: cleanup-blastdb-volumes.py 590894 2019-08-07 14:59:53Z camacho $"""

class Tester(unittest.TestCase):
    """Testing class for this script."""

    def test_blastdb_config_invalid(self):
        pass

    def test_blastdb_config(self):
        pass

    def test_blastdb_finder(self):
        pass

def find_blastdb(name: str, is_prot: bool) -> str:
    """Returns full path to BLAST database or None."""
    pass

def get_blastdb_from_ncbi_config(config_file: str) -> str:
    """Return the BLASTDB setting from the NCBI configuration file or None."""
    pass

def main():
    """Entry point into this program."""
    pass

def create_arg_parser():
    """Create the command line options parser object for this script."""
    pass
```
