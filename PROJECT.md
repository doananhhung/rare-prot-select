# Project: RareProtSelect (Chọn tập protein đại diện có ưu tiên nhóm hiếm bằng tối ưu hóa submodular)

## Architecture
RareProtSelect là hệ thống khoa học tích hợp 4 tầng phụ thuộc theo kiến trúc Clean Architecture:
- **Tầng 1 (Data & Config & Utils)**: Xử lý tệp FASTA, lọc kiểm soát chất lượng (QC), trích xuất phân họ sinh học, nạp dataset, cấu hình YAML, theo dõi thời gian/bộ nhớ và xuất kết quả.
- **Tầng 2 (ESM-2 Embeddings & Similarity)**: Khai thác mô hình ngôn ngữ protein tiền huấn luyện ESM-2 trên GPU NVIDIA RTX 5060 (CUDA 13.0, PyTorch cu130), trích xuất vector nhúng Mean Pooling chuẩn hóa $\ell_2$, quản lý lưu đệm cache, và xây dựng không gian tương đồng ngữ nghĩa Cosine không âm $\operatorname{sim}(u, v) = \max(0, \hat{z}(u)^\top \hat{z}(v))$.
- **Tầng 3 (Rare Weighting & Submodular Optimization)**: Tính toán trọng số Rare-Aware $w_v = 1/\sqrt{n_g}$ (kèm các hàm đối chứng Uniform, Inverse Frequency, Power), thuật toán tối ưu Lazy Greedy sử dụng Hàng đợi ưu tiên (Max-Heap) với cơ chế kiểm tra tính hợp lệ và dừng sớm, thuật toán Standard Greedy và các bộ chọn baseline (Random, K-Medoids, Farthest First).
- **Tầng 4 (Multi-tier Evaluation & Experiments)**: Đánh giá nội tại 3 tầng (Overall, Macro, Worst-Group Coverage, Rare Rep Rate, Redundancy), đánh giá hạ nguồn (1-NN Annotation Transfer Macro-F1 & Accuracy), đối chuẩn chuẩn vàng ThYme DB Expert Benchmark, và 4 kịch bản thực nghiệm độc lập (Pilot, Core, Scalability, Ablation).

## Code Layout
```
RareProtSelect/
├── pyproject.toml
├── requirements.txt
├── configs/
│   ├── config_pilot_thyme.yaml
│   ├── config_core_merops.yaml
│   ├── config_scalability_ce.yaml
│   └── config_ablation.yaml
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fasta_parser.py
│   │   ├── quality_filter.py
│   │   ├── annotation_mapper.py
│   │   └── dataset_loader.py
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── esm_embedder.py
│   │   └── cache_manager.py
│   ├── similarity/
│   │   ├── __init__.py
│   │   ├── dense_similarity.py
│   │   └── sparse_knn.py
│   ├── weighting/
│   │   ├── __init__.py
│   │   └── rare_weighting.py
│   ├── selection/
│   │   ├── __init__.py
│   │   ├── lazy_greedy.py
│   │   ├── standard_greedy.py
│   │   └── baseline_selectors.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── intrinsic_metrics.py
│   │   ├── annotation_transfer.py
│   │   └── benchmark_comparator.py
│   └── utils/
│       ├── __init__.py
│       ├── timer.py
│       ├── memory_tracker.py
│       ├── visualizer.py
│       └── exporter.py
├── experiments/
│   ├── __init__.py
│   ├── run_pilot_thyme.py
│   ├── run_core_merops.py
│   ├── run_scalability_ce.py
│   └── run_ablation_all.py
├── outputs/
│   ├── embeddings_cache/
│   ├── similarity_cache/
│   ├── logs/
│   ├── figures/
│   └── tables/
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Configuration & Settings | Pydantic/Dataclass config loader cho YAML | M1 | Doc 2 (Module 1) |
| 2 | FASTA Parsing | Parser đọc FASTA, khử wrapping, loại bỏ gaps | M1 | Doc 1 (CĐ 1.1), Doc 2 (Module 2) |
| 3 | Quality Control Filter | Lọc độ dài [30, 2000], lọc ký tự lạ >5%, khử trùng | M1 | Doc 1 (CĐ 1.2), Doc 2 (Module 2) |
| 4 | Annotation Mapper | Bóc tách nhãn phân họ MEROPS, CE, ThYme | M1 | Doc 1 (CĐ 1.3), Doc 2 (Module 2) |
| 5 | Dataset Loader | Pipeline tích hợp parser + QC + mapping | M1 | Doc 1 (GĐ 1), Doc 2 (Module 2) |
| 6 | System Utilities | Timer, MemoryTracker (RAM/VRAM), Visualizer, Exporter | M1 | Doc 2 (Module 7) |
| 7 | ESM-2 Embedder | Inference mô hình ESM-2 (35M/150M) trên GPU RTX 5060 | M2 | Doc 1 (CĐ 2.1), Doc 2 (Module 3) |
| 8 | Mean Pooling & L2 Norm | Pooling nén chuỗi và chuẩn hóa $\|\hat{z}(v)\|_2 = 1.0$ | M2 | Doc 1 (CĐ 2.2), Doc 2 (Module 3) |
| 9 | Cache Manager | Lưu và nạp vector nhúng định dạng .npy/.pt | M2 | Doc 1 (CĐ 2.3), Doc 2 (Module 3) |
| 10 | Non-negative Cosine Similarity | Ma trận tương đồng $\operatorname{sim}(u, v) = \max(0, \hat{z}(u)^\top \hat{z}(v))$ | M2 | Doc 1 (CĐ 3.1), Doc 2 (Module 4) |
| 11 | Sparse k-NN Similarity | Cấu trúc ma trận thưa cho tập dữ liệu siêu lớn | M2 | Doc 2 (Module 4) |
| 12 | Rare-Aware Weighting | Trọng số $w_v = 1/\sqrt{n_g}$ ưu tiên nhóm hiếm | M3 | Doc 1 (CĐ 3.2), Doc 2 (Module 5) |
| 13 | Comparison Weighting Schemes | Trọng số Uniform ($1.0$), Inverse ($1/n_g$), Power ($1/n_g^\alpha$) | M3 | Doc 1 (CĐ 3.2), Doc 2 (Module 5) |
| 14 | Marginal Gain Computation | $\Delta(e \mid S) = \sum_{v \in V} w_v \max(0, \operatorname{sim}(v, e) - \text{curr\_max}_v)$ | M3 | Doc 1 (CĐ 4.1), Doc 2 (Module 5) |
| 15 | Lazy Greedy Optimization | Max-Heap với Validity Check & Early Stopping ($>100\times$) | M3 | Doc 1 (CĐ 4.2), Doc 2 (Module 5) |
| 16 | Standard Greedy Optimization | Thuật toán quét vét cạn chuẩn làm mốc đối chứng 1-1 | M3 | Doc 1 (CĐ 4.3), Doc 2 (Module 5) |
| 17 | Baseline Selectors | Random, K-Medoids (PAM), Farthest First Traversal | M3 | Doc 1 (GĐ 6), Doc 2 (Module 5) |
| 18 | Intrinsic Coverage Metrics | Subfamily, Overall, Macro, Worst-Group Coverage | M4 | Doc 1 (CĐ 5.1), Doc 2 (Module 6) |
| 19 | Intrinsic Diversity Metrics | Rare Group Representation Rate, Pairwise Redundancy | M4 | Doc 1 (CĐ 5.1), Doc 2 (Module 6) |
| 20 | Downstream Annotation Transfer | 1-NN Classifier chuyển giao nhãn từ tập $S$ sang $V \setminus S$ | M4 | Doc 1 (CĐ 5.2), Doc 2 (Module 6) |
| 21 | Downstream Transfer Metrics | Macro-F1, Per-class F1, Accuracy | M4 | Doc 1 (CĐ 5.2), Doc 2 (Module 6) |
| 22 | ThYme Expert Comparator | Benchmark đối chuẩn độ khớp $>80\%-95\%$ với ThYme DB | M4 | Doc 1 (CĐ 7.1), Doc 2 (Module 6) |
| 23 | Static Logic & Direct Verification | Đối chiếu logic tĩnh với bản thiết kế và chạy trực tiếp module qua terminal | M5 | GEMINI.md, Doc 2 |
| 24 | Static Code Audit | 100% 1-1 đối chiếu signature, type hints, docstrings | M5 | GEMINI.md, Doc 2 |
| 25 | Pilot Experiment (Thioesterases) | Chạy run_pilot_thyme.py xác thực pipeline & ThYme benchmark | M6 | Doc 1 (GĐ 7), Doc 2 (Module 7) |
| 26 | Full Experiment Scripts | run_core_merops.py, run_scalability_ce.py, run_ablation_all.py | M6 | Doc 1 (GĐ 7), Doc 2 (Module 7) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Layer 1: Data, Config & Utils | `settings.py`, YAML configs, `fasta_parser.py`, `quality_filter.py`, `annotation_mapper.py`, `dataset_loader.py`, `timer.py`, `memory_tracker.py`, `visualizer.py`, `exporter.py` | None | DONE |
| M2 | Layer 2: ESM-2 Embeddings & Similarity | `esm_embedder.py`, `cache_manager.py`, `dense_similarity.py`, `sparse_knn.py` | M1 | DONE |
| M3 | Layer 3: Rare Weighting & Submodular Selection | `rare_weighting.py`, `lazy_greedy.py`, `standard_greedy.py`, `baseline_selectors.py` | M2 | DONE |
| M4 | Layer 4: Multi-tier Evaluation & Benchmark | `intrinsic_metrics.py`, `annotation_transfer.py`, `benchmark_comparator.py` | M3 | DONE |
| M5 | Static Logic & Direct Verification | 100% 1-1 đối chiếu thiết kế, xác minh trực tiếp đầu ra từng module | M1, M2, M3, M4 | DONE |
| M6 | Experiment Scripts & Pilot Validation | `experiments/` (4 scripts), thực thi pilot ThYme validation đạt >80%-95% khớp | M5 | DONE |

## Interface Contracts
### Data Layer ↔ Embeddings Layer
- `ProteinRecord`: `id: str`, `sequence: str`, `header: str`, `length: int`
- `DatasetBundle`: `records: list[ProteinRecord]`, `id_to_seq: dict[str, str]`, `id_to_family: dict[str, str]`, `family_counts: dict[str, int]`, `rare_families: list[str]`, `cleaned_ids: list[str]`
- `ESMEmbedder.embed_sequences(sequences: list[str], batch_size: int = 16) -> np.ndarray` (shape: `(N, d)`, $\ell_2$-normalized).

### Embeddings Layer ↔ Similarity Layer
- `DenseSimilarity.compute_similarity_matrix(embeddings: np.ndarray) -> np.ndarray` (shape: `(N, N)`, values in $[0, 1]$, non-negative cosine).

### Similarity & Weighting ↔ Selection Layer
- `RareWeighting.compute_weights(family_labels: list[str], scheme: str = "inverse_sqrt", alpha: float = 0.5) -> np.ndarray` (shape: `(N,)`, $w_v > 0$).
- `LazyGreedySelector.select(similarity_matrix: np.ndarray, weights: np.ndarray, k: int) -> SelectionResult` (`selected_indices: list[int]`, `marginal_gains: list[float]`, `objective_history: list[float]`, `total_evaluations: int`).
- `StandardGreedySelector.select(...) -> SelectionResult` (Đảm bảo $S_{\text{lazy}} == S_{\text{standard}}$ và $F(S_{\text{lazy}}) == F(S_{\text{standard}})$ $100\%$).

### Selection Layer ↔ Evaluation Layer
- `IntrinsicEvaluator.evaluate_all(similarity_matrix: np.ndarray, selected_indices: list[int], family_labels: list[str], rare_threshold: int = 5) -> dict[str, float]`
- `AnnotationTransferEvaluator.evaluate(similarity_matrix: np.ndarray, selected_indices: list[int], true_labels: list[str]) -> dict[str, Any]`
- `BenchmarkComparator.compare_with_expert(selected_ids: list[str], expert_ids: list[str], similarity_matrix: np.ndarray = None, id_to_index: dict[str, int] = None) -> dict[str, float]`
