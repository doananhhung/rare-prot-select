# Bảng Thực Nghiệm Nhánh 1: Tái Hiện Hình 8 Bài Báo Gốc Trên Peptidase A1 (MEROPS A1A)

*(Thực hiện Công đoạn 1 trong Tài liệu 1 và Module 1 trong Tài liệu 2)*

### 1. Bảng Số Liệu Đo Đạc Thực Nghiệm (1,000-Shuffle Consensus Ranking)

|   budget_k |   num_selected |   overall_sensitivity_blast_pct |   retrieved_hits_count |   total_cleaned_sequences |   published_fig8_sensitivity_pct |   deviation_pct |
|-----------:|---------------:|--------------------------------:|-----------------------:|--------------------------:|---------------------------------:|----------------:|
|          1 |              1 |                           82.36 |                  10959 |                     13307 |                             80.5 |            1.86 |
|          2 |              2 |                           83.55 |                  11118 |                     13307 |                             83.5 |            0.05 |
|          3 |              3 |                           85.85 |                  11424 |                     13307 |                             85.7 |            0.15 |
|          4 |              4 |                           86.88 |                  11561 |                     13307 |                             86.7 |            0.18 |
|          5 |              5 |                           88.1  |                  11723 |                     13307 |                             88   |            0.1  |
|          6 |              6 |                           88.17 |                  11733 |                     13307 |                             88.1 |            0.07 |
|          7 |              7 |                           88.77 |                  11813 |                     13307 |                             88.4 |            0.37 |
|          8 |              8 |                           90.51 |                  12044 |                     13307 |                             89   |            1.51 |
|          9 |              9 |                           90.66 |                  12064 |                     13307 |                             90.7 |           -0.04 |
|         10 |             10 |                           91.43 |                  12167 |                     13307 |                             90.8 |            0.63 |
|         11 |             11 |                           91.59 |                  12188 |                     13307 |                             90.9 |            0.69 |

### 2. Đối Chiếu Định Lượng Trực Diện Với 11 Mốc Hình 8 Panel A (Nguyen et al., 2025)

- Nguồn sự thật 11 mốc ước lượng từ Hình 8 Panel A: `outputs/tables/nguyen2025_fig8a_benchmark.csv`
- **Mốc $k = 1$**: Đạt **82.36%** (Hình 8A: $\approx 80.5\%$, lệch: +1.86%)
- **Mốc $k = 5$**: Đạt **88.1%** (Hình 8A: $\approx 88.0\%$, lệch: +0.10%)
- **Mốc $k = 10$**: Đạt **91.43%** (Hình 8A: $\approx 90.8\%$, lệch: +0.63%)
- **Mốc $k = 11$**: Đạt **91.59%** (Hình 8A: $\approx 90.9\%$, lệch: +0.69%)
