# Project: RareProtSelect
## Đề tài 2: Tái hiện Đối chuẩn Bài báo nền trên Siêu họ Peptidase A1 (MEROPS A1A)

## Architecture
RareProtSelect trong giai đoạn hiện tại được thiết kế theo cấu trúc khoa học tinh gọn tập trung độc quyền vào việc tái hiện bài báo nền (*Nguyen et al., Nature Scientific Reports 2025*):
- **Tầng 1 (Data & Config & Utils)**: Xử lý tệp FASTA (`fasta_parser.py`), lọc kiểm soát chất lượng (`quality_filter.py`), trích xuất cấu trúc phân họ (`annotation_mapper.py`), bộ nạp tích hợp (`dataset_loader.py`), cấu hình YAML (`settings.py`), bấm giờ (`timer.py`) và xuất báo cáo (`exporter.py`).
- **Tầng 2 (Sequence Similarity)**: Căn chỉnh cục bộ All-vs-All bằng NCBI BLASTp (`blast_similarity.py`), chuẩn hóa ma trận nhận dạng chuỗi Identity không âm $\mathbf{S} \in \mathbb{R}^{13,307 \times 13,307}$.
- **Tầng 3 (Submodular Selection)**: Thuật toán tham lam cắt tỉa 90% kết hợp 1,000 lần xáo trộn ngẫu nhiên (`Pruned Greedy 90% (1,000-Shuffle Consensus Ranking)`) theo đúng Algorithm 1 và mã nguồn R `Greedy.R` của tác giả.
- **Tầng 4 (Live BLAST Evaluation & Experiments)**: Kịch bản thực nghiệm `exp1_baseline_a1a_calibration.py` đo lường duy nhất chỉ số chính thống `Overall Sensitivity BLAST (%)` trên đúng 11 mốc ngân sách $k \in [1..11]$ đối chiếu 1-1 với Hình 8 Panel A.

## Code Layout
```
RareProtSelect/
├── pyproject.toml
├── configs/
│   └── config_exp1_baseline_a1a_calibration.yaml # Cấu hình duy nhất cho Nhánh 1
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
│   ├── similarity/
│   │   ├── __init__.py
│   │   └── blast_similarity.py
│   ├── selection/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── standard_greedy.py
│   │   └── unweighted_selector.py
│   └── utils/
│       ├── __init__.py
│       ├── timer.py
│       └── exporter.py
├── experiments/
│   ├── __init__.py
│   └── exp1_baseline_a1a_calibration.py # Kịch bản tái hiện Hình 8 A1A (k in [1..11])
└── outputs/
    ├── similarity_cache/
    ├── figures/
    └── tables/
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Configuration & Settings | Dataclass config loader cho YAML | M1 | Doc 2 (Module 3.1) |
| 2 | FASTA Parsing | Parser đọc FASTA, khử wrapping | M1 | Doc 1 (CĐ 1), Doc 2 (Module 3.2) |
| 3 | Quality Control Filter | Lọc độ dài [30, 2000], lọc ký tự lạ <= 5%, khử trùng | M1 | Doc 1 (CĐ 1), Doc 2 (Module 3.2) |
| 4 | Annotation Mapper | Bóc tách nhãn phân họ MEROPS | M1 | Doc 1 (CĐ 1), Doc 2 (Module 3.2) |
| 5 | Dataset Loader | Pipeline tích hợp parser + QC + mapping | M1 | Doc 1 (CĐ 1), Doc 2 (Module 3.2) |
| 6 | System Utilities | Timer, Exporter (CSV, JSON, Markdown) | M1 | Doc 2 (Module 3.5) |
| 7 | BLASTp Similarity Matrix | Ma trận nhận dạng chuỗi NCBI BLASTp All-vs-All | M2 | Doc 1 (CĐ 2), Doc 2 (Module 3.3) |
| 8 | Pruned Greedy Selection | Thuật toán tham lam cắt tỉa 90% (Greedy.R) | M3 | Doc 1 (CĐ 3), Doc 2 (Module 3.4) |
| 9 | 1,000-Shuffle Consensus | Bầu chọn tần suất đồng thuận qua 1,000 lần xáo trộn | M3 | Doc 1 (CĐ 3), Doc 2 (Module 4) |
| 10 | Live BLAST Sensitivity | Đo đạc độ nhạy Live BLAST (E <= 1e-7) trên 11 mốc ngân sách k | M4 | Doc 1 (CĐ 4), Doc 2 (Module 4) |
| 11 | Figure 8 Calibration | Đối chiếu trực diện với Hình 8 Panel A của bài báo gốc | M5 | Doc 1 (CĐ 5), Doc 2 (Module 4) |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Data, Config & Utils | `settings.py`, `dataset_loader.py`, `exporter.py` | None | DONE |
| M2 | BLASTp Sequence Identity Matrix | `blast_similarity.py`, All-vs-All $13,307 \times 13,307$ | M1 | DONE |
| M3 | Pruned Greedy & 1,000 Shuffles | `standard_greedy.py`, `run_pruned_greedy_1000_shuffles()` | M2 | DONE |
| M4 | Live BLAST Sensitivity Evaluation | Đánh giá 11 mốc ngân sách $k \in [1..11]$ qua Live BLAST | M3 | DONE |
| M5 | Figure 8 Verification & Reporting | Đối chuẩn định lượng Hình 8 Panel A, xuất bản đồ thị 1 panel và bảng CSV | M4 | DONE |
