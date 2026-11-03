# TỔNG HỢP HỆ THỐNG CHỈ SỐ ĐÁNH GIÁ KHOA HỌC (SSOT METRIC COMPENDIUM)
## Đề tài 2: Chọn Tập Protein Đại Diện Có Ưu Tiên Nhóm Hiếm Bằng Tối Ưu Hóa Submodular (`RareProtSelect`)
### Phạm Vi Chuẩn Hóa: Chuỗi Thực Nghiệm Nhánh 1 $\to$ Nhánh 5 Trên Siêu Họ Peptidase A1 (`MEROPS_A1A` — Phương Án 3B & Truy Vấn Ngược Nội Phân Họ)

---

> 📌 **QUY CHUẨN THƯỚC ĐO KHOA HỌC & LIÊM CHÍNH DỮ LIỆU (SSOT NOTICE)**:
> 1. **Hai thiết lập dữ liệu và đánh giá chuẩn mực**:
>    - **Nhánh 1 (Tái hiện Hình 8A bài báo gốc *Nguyen et al., 2025*)**: Đánh giá trên toàn tập $13,307$ chuỗi sạch (`exclude_unknown_subfamilies: false`) với thước đo `Overall Sensitivity BLAST (%)` toàn cục tại $k \in [1..11]$.
>    - **Nhánh 2 $\to$ Nhánh 5 (Bài toán Chọn tập đại diện đa phân họ có ưu tiên nhóm hiếm)**:
>      - **Tập dữ liệu chuẩn hóa Phương án 3B (`MEROPS_A1A_curated`, `exclude_unknown_subfamilies: true`)**: Gồm **$|V| = 4,120$ chuỗi sạch** có nhãn phân họ chính thức ($0\%$ Unknown), phân bố trên **$G = 115$ phân họ định danh** (`75` phân họ mã số `A01.001`..`A01.971` + `40` phân họ mã chữ-số `A01.A02`..`A01.P02`), trong đó có **$|G_{\text{rare}}| = 45$ phân họ hiếm** ($n_g \le 5$ chuỗi, gồm $18$ họ đơn độc $n_g = 1$), và phân họ lớn nhất là **`A01.009` (Cathepsin D, $329$ chuỗi sạch / $339$ chuỗi thô)**.
>      - **Cơ chế Truy vấn ngược nội phân họ (`Within-Subfamily Representative Query`: $S_{k,g} = S_k \cap V_g \to V_g$)**: Khi đánh giá từng phân họ $g \in \{1..115\}$, **chỉ những chuỗi đại diện trong $S_k$ thực sự thuộc về phân họ $g$ ($S_{k,g} = S_k \cap V_g$)** mới được phép truy vấn ngược lại các thành viên $V_g$ của chính phân họ đó. Nếu $S_k \cap V_g = \emptyset$ thì phân họ $g$ có độ nhạy và độ bao phủ nội phân họ bằng đúng **$0.0\%$**.
> 2. **Cấu trúc giải thích thống nhất 4 phần cho từng chỉ số**:
>    - **(1) Công thức toán học & Giải nghĩa từng ký hiệu**
>    - **(2) Ý nghĩa sinh học & Thực tiễn**
>    - **(3) Ví dụ tính tay từng bước (`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`)**
>    - **(4) Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Số liệu đo đạc thực tế tại $k = 11$ và $k = 115$)**

---

## BẢNG TỔNG QUAN PHÂN LOẠI 13 CHỈ SỐ ĐÁNH GIÁ CHÍNH & 4 CỘT ĐẾM NGUYÊN (NHÁNH 1 $\to$ NHÁNH 5)

| Nhóm Thước Đo | STT | Tên Cột CSV / Ký Hiệu | Tên Chỉ Số Tiếng Việt | Phạm Vi Áp Dụng | Chiều Tối Ưu |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **Nhóm 1: Độ nhạy căn chỉnh rời rạc nội phân họ (`Live BLASTp Sensitivity %`, $E \le 10^{-7}$)** | 1 | `overall_sensitivity_blast_pct` | Độ nhạy toàn tập ($13,307$ chuỗi ở Nhánh 1; $4,120$ chuỗi nội phân họ ở Nhánh 2, 4) | Nhánh 1, 2, 4 | Càng cao càng tốt ($\uparrow$) |
| | 2 | `worst_group_sensitivity_blast_pct` | Độ nhạy nội phân họ của phân họ thiệt thòi nhất (trên $115$ họ) | Nhánh 2, 4 | Càng cao càng tốt ($\uparrow$) |
| | 3 | `rare_sensitivity_blast_pct` | Độ nhạy nội phân họ trung bình trên $45$ phân họ hiếm ($\le 5$ chuỗi) | Nhánh 2, 4 | Càng cao càng tốt ($\uparrow$) |
| | 4 | `macro_sensitivity_blast_pct` | Độ nhạy nội phân họ trung bình bình đẳng trên $115$ phân họ | Nhánh 2, 4 | Càng cao càng tốt ($\uparrow$) |
| | 5 | `zero_cov_subfamilies_count` | Số phân họ bị bỏ rơi hoàn toàn ($\operatorname{Sens}_g^{\text{within}} = 0\%$, trên $115$ họ) | Nhánh 2, 4 | Càng thấp càng tốt ($\downarrow \to 0$) |
| **Nhóm 2: Độ bao phủ ngữ nghĩa liên tục nội phân họ (`Coverage ESM %`, $\beta = 0.70$)** | 6 | `overall_coverage_esm_pct` | Độ bao phủ ngữ nghĩa nội phân họ toàn tập ($4,120$ chuỗi) | Nhánh 3, 4 | Càng cao càng tốt ($\uparrow$) |
| | 7 | `worst_group_coverage_esm_pct` | Độ bao phủ ngữ nghĩa nội phân họ của phân họ thấp nhất (trên $115$ họ) | Nhánh 3, 4 | Càng cao càng tốt ($\uparrow$) |
| | 8 | `rare_coverage_esm_pct` | Độ bao phủ ngữ nghĩa nội phân họ trung bình $45$ phân họ hiếm | Nhánh 3, 4 | Càng cao càng tốt ($\uparrow$) |
| | 9 | `macro_coverage_esm_pct` | Độ bao phủ ngữ nghĩa nội phân họ trung bình bình đẳng $115$ phân họ | Nhánh 3, 4 | Càng cao càng tốt ($\uparrow$) |
| **Nhóm 3: Cấu trúc đại diện trực tiếp & Độ dư thừa phân họ trong $S_k$** | 10 | `subfamily_repr_rate_pct`<br>*(kèm `subfamilies_represented_count`)* | Tỷ lệ `%` (và số lượng) phân họ trên $115$ họ có đại diện trực tiếp trong $S_k$ | Nhánh 5 | Càng cao càng tốt ($\uparrow$) |
| | 11 | `rare_repr_rate_pct`<br>*(kèm `rare_subfamilies_represented_count`)* | Tỷ lệ `%` (và số lượng) phân họ hiếm trên $45$ họ hiếm có đại diện trực tiếp trong $S_k$ | Nhánh 5 | Càng cao càng tốt ($\uparrow$) |
| | 12 | `subfamily_redundancy_pct`<br>*(kèm `redundant_slots_count`)* | Độ dư thừa phân bổ phân họ (`%` và số ghế trong $k$ bị lặp lại phân họ) | Nhánh 5 | Càng thấp càng tốt ($\downarrow \to 0\%$) |
| | 13 | `dominant_a01_009_share_pct`<br>*(kèm `dominant_a01_009_count`)* | Tỷ trọng `%` (và số ghế) độc chiếm ngân sách của họ lớn nhất `A01.009` ($329$ chuỗi) | Nhánh 5 | Càng thấp càng tốt ($\downarrow$) |

---

## 1. NHÓM 1: BỘ 5 CHỈ SỐ ĐỘ NHẠY CĂN CHỈNH RỜI RẠC NỘI PHÂN HỌ (`LIVE BLASTP SENSITIVITY %`, $E \le 10^{-7}$)
*(Hiện thực hóa tại [`src/similarity/blast_similarity.py`](./RareProtSelect/src/similarity/blast_similarity.py), [`experiments/exp2_rare_weighted_a1a.py`](./RareProtSelect/experiments/exp2_rare_weighted_a1a.py) và [`experiments/exp4_cross_eval_a1a.py`](./RareProtSelect/experiments/exp4_cross_eval_a1a.py))*

### Thiết lập toán học chung của Nhóm 1 (Nhánh 2 & Nhánh 4):
- **Tập dữ liệu chuẩn hóa Phương án 3B (Ground Set $V$)**: Gồm $|V| = 4,120$ chuỗi protein sạch có nhãn phân họ chính thức thuộc siêu họ Peptidase A1 (`MEROPS_A1A_curated`), được phân hoạch thành $G = 115$ phân họ không giao nhau:
  $$V = \bigcup_{g=1}^{115} V_g, \qquad n_g = |V_g|$$
- **Tập các phân họ hiếm ($G_{\text{rare}}$)**: Gồm các phân họ có quy mô từ $1$ đến $5$ chuỗi:
  $$G_{\text{rare}} = \{g \in \{1..115\} \mid n_g \le 5\}, \qquad |G_{\text{rare}}| = 45 \text{ phân họ hiếm}$$
- **Tập đại diện nội phân họ ($S_{k,g}$) và Tập chuỗi được tìm thấy nội phân họ qua `Live BLASTp` ($C_{k,g}^{\text{within}}$)**:
  Khi trích xuất $k$ chuỗi đại diện đầu tiên $S_k = \{s_1, \dots, s_k\}$ ($k \in [1..115]$), với mỗi phân họ $g \in \{1..115\}$, ta xét tập con các đại diện thuộc chính phân họ $g$:
  $$S_{k,g} = S_k \cap V_g$$
  Khi chạy công cụ NCBI `blastp` ($E\text{-value} \le 10^{-7}$), một chuỗi thành viên $v \in V_g$ chỉ được tính là thu hồi thành công nếu nó có hit từ một đại diện **cùng phân họ $g$** ($s \in S_{k,g}$):
  $$C_{k,g}^{\text{within}} = \left\{v \in V_g \;\middle|\; \exists s \in (S_k \cap V_g) : \operatorname{BLASTp}(s, v) \text{ có Hit thỏa } E \le 10^{-7}\right\}$$
- **Độ nhạy nội phân họ trên từng phân họ thứ $g$ ($\operatorname{Sens}_g^{\text{within}}(S_k)$)**:
  $$\operatorname{Sens}_g^{\text{within}}(S_k) = \frac{|C_{k,g}^{\text{within}}|}{|V_g|} \times 100\%$$
  Hệ quả trực tiếp: Nếu $S_k \cap V_g = \emptyset$ (phân họ $g$ chưa có đại diện trong $S_k$) thì $C_{k,g}^{\text{within}} = \emptyset \implies \operatorname{Sens}_g^{\text{within}}(S_k) = \mathbf{0.0\%}$.

---

### 1.1. `overall_sensitivity_blast_pct` (Độ nhạy toàn tập)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   - **Ở Nhánh 1 (Tái hiện Hình 8A trên $13,307$ chuỗi toàn cục)**:
     $$\operatorname{Overall\_Sens}_{\text{BLAST}}^{\text{global}}(S_k) = \frac{|C_k|}{|V_{\text{all}}|} \times 100\%, \qquad |V_{\text{all}}| = 13,307$$
   - **Ở Nhánh 2 & Nhánh 4 (Truy vấn ngược nội phân họ trên $4,120$ chuỗi của $115$ phân họ)**:
     $$\operatorname{Overall\_Sens}_{\text{BLAST}}^{\text{within}}(S_k) = \frac{\sum_{g=1}^{115} |C_{k,g}^{\text{within}}|}{|V|} \times 100\%, \qquad |V| = 4,120$$
   *(Đi kèm cột đếm nguyên `retrieved_hits_count` $= \sum_{g=1}^{115} |C_{k,g}^{\text{within}}|$ và `total_cleaned_sequences` $= 4,120$).*
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đo lường tỷ lệ phần trăm tổng số protein trong toàn bộ $4,120$ chuỗi được thu hồi hợp lệ bởi các chuỗi đại diện xuất thân từ chính phân họ của chúng.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Giả sử tập dữ liệu có $|V| = 100$ chuỗi gồm Họ lớn $g_1$ ($90$ chuỗi) và 2 Họ hiếm $g_2$ ($5$ chuỗi), $g_3$ ($5$ chuỗi). Nếu $S_k$ có đại diện ở $g_1$ (thu hồi $88/90$ chuỗi) và ở $g_2$ (thu hồi $4/5$ chuỗi), nhưng chưa chọn đại diện nào ở $g_3$ ($S_k \cap V_{g_3} = \emptyset \implies |C_{k,g_3}^{\text{within}}| = 0$), thì tổng số chuỗi thu hồi hợp lệ là $88 + 4 + 0 = 92 \implies \operatorname{Overall\_Sens}_{\text{BLAST}}^{\text{within}} = 92.0\%$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` đạt `38.06%` ($\alpha=0.0$), `32.6%` ($\alpha=0.5$), `26.07%` ($\alpha=1.0$); `ESM-2` đạt `32.18%` ($\alpha=0.0$), `20.36%` ($\alpha=0.5$), `16.33%` ($\alpha=1.0$).
   - Tại **$k = 115$**: Trên `BLASTp`, mức trọng số cân bằng **$\alpha = 0.5$ đạt đỉnh toàn cục `94.13%` (`3,878 / 4,120` chuỗi)**, vượt qua cả phương pháp gốc không trọng số $\alpha = 0.0$ (`93.57%`, `3,855` chuỗi), trong khi $\alpha = 1.0$ đạt `79.08%` (`3,258` chuỗi). Trên `ESM-2`, chỉ số này đạt `90.7%` ($\alpha=0.0$), `89.98%` ($\alpha=0.5$), và `87.79%` ($\alpha=1.0$).

---

### 1.2. `worst_group_sensitivity_blast_pct` (Độ nhạy nội phân họ của phân họ thiệt thòi nhất)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Worst\_Sens}_{\text{BLAST}}^{\text{within}}(S_k) = \min_{g \in \{1..115\}} \operatorname{Sens}_g^{\text{within}}(S_k)$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đóng vai trò là **chốt chặn công bằng Rawlsian (Max-Min Fairness)** trên 115 phân họ: với mọi ngân sách $k < 115$, theo Nguyên lý Chuồng bồ câu chắc chắn tồn tại ít nhất $115 - k$ phân họ chưa có đại diện ($S_k \cap V_g = \emptyset$), nên chỉ số này bằng đúng $0.0\%$ tại mọi $k < 115$. Tại mốc $k = 115$, chỉ số này chỉ dương ($> 0\%$) khi và chỉ khi **cả 115/115 phân họ đều có ít nhất 1 đại diện** (`redundant_slots_count = 0`).
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Với $3$ phân họ có độ nhạy nội phân họ lần lượt là $\operatorname{Sens}_{g_1}^{\text{within}} = 97.78\%$, $\operatorname{Sens}_{g_2}^{\text{within}} = 80.0\%$, $\operatorname{Sens}_{g_3}^{\text{within}} = 0.0\%$, ta có $\operatorname{Worst\_Sens}_{\text{BLAST}}^{\text{within}} = \min(97.78\%, 80.0\%, 0.0\%) = 0.0\%$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại cả **$k = 11$** và **$k = 115$**, do giải thuật tham lam không có ràng buộc ép buộc phân vùng cứng (partition matroid constraint) nên ở $k = 115$ vẫn còn một số suất trùng lặp ở các phân họ lớn (tối thiểu `18` suất tại `BLASTp` $\alpha=1.0$), làm cho ít nhất `18` phân họ chưa có đại diện và giữ `worst_group_sensitivity_blast_pct = 0.0%` trên cả 6 cấu hình. Do đó, cần kết hợp với `zero_cov_subfamilies_count` và `rare_sensitivity_blast_pct` để thấy rõ tiến độ giải cứu từng phân họ.

---

### 1.3. `rare_sensitivity_blast_pct` (Độ nhạy nội phân họ trung bình trên 45 phân họ hiếm $\le 5$ chuỗi)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Rare\_Sens}_{\text{BLAST}}^{\text{within}}(S_k) = \frac{1}{|G_{\text{rare}}|} \sum_{g \in G_{\text{rare}}} \operatorname{Sens}_g^{\text{within}}(S_k) = \frac{1}{45} \sum_{g \in G_{\text{rare}}} \left(\frac{|C_{k,g}^{\text{within}}|}{|V_g|} \times 100\%\right)$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Cô lập riêng nhóm $45$ phân họ hiếm ($n_g \le 5$ chuỗi). Nhờ cơ chế truy vấn ngược nội phân họ, một phân họ hiếm chưa có đại diện trong $S_k$ sẽ nhận đúng $0.0\%$ (không được phép tính gộp hit chéo từ phân họ lớn), phản ánh trung thực năng lực bảo vệ nhóm hiếm của từng mức $\alpha$.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Giả sử có $|G_{\text{rare}}| = 45$ phân họ hiếm. Tại $k = 1$, nếu chọn 1 đại diện thuộc một phân họ hiếm đơn độc $g^*$ ($n_{g^*} = 1$), thì $\operatorname{Sens}_{g^*}^{\text{within}} = 100.0\%$ và $44$ phân họ hiếm còn lại có $\operatorname{Sens}_g^{\text{within}} = 0.0\% \implies \operatorname{Rare\_Sens}_{\text{BLAST}}^{\text{within}} = \frac{100.0\%}{45} \approx \mathbf{2.22\%}$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: Phương pháp không trọng số $\alpha = 0.0$ đạt **`0.0%`** trên cả `BLASTp` và `ESM-2`. Khi bật $\alpha = 1.0$, cả `BLASTp` và `ESM-2` đều nâng chỉ số này lên **`4.44%`** (đại diện sớm 2 phân họ hiếm ngay trong 11 bước đầu).
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Tăng nhảy vọt từ **`2.22%`** ($\alpha = 0.0$, chỉ $1/45$ họ hiếm) $\to$ **`59.11%`** ($\alpha = 0.5$, gấp $26.6\times$) $\to$ **`91.11%`** ($\alpha = 1.0$, cứu sống $41/45$ phân họ hiếm, gấp $41.0\times$ so với $\alpha=0.0$).
     - Trên `ESM-2`: Tăng từ **`13.33%`** ($\alpha = 0.0$) $\to$ **`43.11%`** ($\alpha = 0.5$) $\to$ **`41.33%`** ($\alpha = 1.0$).

---

### 1.4. `macro_sensitivity_blast_pct` (Độ nhạy nội phân họ trung bình bình đẳng trên toàn bộ 115 phân họ)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Macro\_Sens}_{\text{BLAST}}^{\text{within}}(S_k) = \frac{1}{115} \sum_{g=1}^{115} \operatorname{Sens}_g^{\text{within}}(S_k)$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đặt mỗi phân họ trong $115$ phân họ ngang hàng nhau với quyền biểu quyết $\frac{1}{115} \approx 0.87\%$, bất kể phân họ đó có $329$ chuỗi (`A01.009`) hay chỉ có $1$ chuỗi đơn độc.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Tại $k = 1$, nếu chọn 1 đại diện thuộc phân họ `A01.009` ($329$ chuỗi) và đại diện này bắt trúng cả $329/329$ chuỗi của `A01.009` ($\operatorname{Sens}_{\text{A01.009}}^{\text{within}} = 100.0\%$), trong khi $114$ phân họ còn lại bằng $0.0\%$, thì $\operatorname{Macro\_Sens}_{\text{BLAST}}^{\text{within}} = \frac{100.0\% + 114 \times 0.0\%}{115} \approx \mathbf{0.87\%}$ (khớp chính xác dòng 22 và dòng 42 của `exp2_rare_weighted_a1a.csv`).
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` tăng từ `8.68%` ($\alpha=0.0$) lên `9.56%` ($\alpha=0.5$) và `9.57%` ($\alpha=1.0$); `ESM-2` đạt `9.45%` ($\alpha=0.0$), `9.49%` ($\alpha=0.5$), `9.45%` ($\alpha=1.0$).
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Tăng mạnh từ **`49.28%`** ($\alpha = 0.0$) $\to$ **`78.87%`** ($\alpha = 0.5$, `+29.59%`) $\to$ **`83.44%`** ($\alpha = 1.0$, `+34.16%`).
     - Trên `ESM-2`: Tăng từ **`50.95%`** ($\alpha = 0.0$) $\to$ **`66.05%`** ($\alpha = 0.5$, `+15.10%`) $\to$ **`63.15%`** ($\alpha = 1.0$).

---

### 1.5. `zero_cov_subfamilies_count` (Số phân họ bị bỏ rơi hoàn toàn với độ nhạy nội phân họ $0.0\%$)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Zero\_Count}_{\text{BLAST}}^{\text{within}}(S_k) = \left|\left\{g \in \{1..115\} \;\middle|\; \operatorname{Sens}_g^{\text{within}}(S_k) = 0.0\%\right\}\right|$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đếm trực tiếp số phân họ trong $115$ phân họ không có đại diện trong $S_k$. Vì mỗi đại diện $s \in S_k \cap V_g$ luôn tự khớp chính nó trong `Live BLASTp` ($E \le 10^{-7}$), chỉ số này thỏa mãn bất biến bù trừ tuyệt đối với Nhánh 5 tại mọi $k \in [1..115]$:
     $$\text{zero\_cov\_subfamilies\_count} + \text{subfamilies\_represented\_count} = 115$$
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Tại $k = 1$, chỉ có đúng $1$ phân họ có đại diện nên số phân họ bị bỏ rơi bằng đúng $115 - 1 = \mathbf{114}$ phân họ.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` ($\alpha=0.0$) còn bỏ sót `105` phân họ (do lãng phí 1 suất trùng lặp vào `A01.009`), trong khi 5 cấu hình còn lại giảm xuống `104` phân họ (mỗi suất trong 11 suất đều mở khóa 1 phân họ khác nhau).
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Giảm mạnh từ **`58` phân họ** bị bỏ rơi ($\alpha = 0.0$, tức bỏ rơi hơn nửa số phân họ!) xuống **`23` phân họ** ($\alpha = 0.5$) và xuống chỉ còn **`18` phân họ** ($\alpha = 1.0$, giải cứu thêm 40 phân họ).
     - Trên `ESM-2`: Giảm từ **`56` phân họ** ($\alpha = 0.0$) xuống **`38` phân họ** ($\alpha = 0.5$) và **`41` phân họ** ($\alpha = 1.0$).

---

## 2. NHÓM 2: BỘ 4 CHỈ SỐ ĐỘ BAO PHỦ NGỮ NGHĨA LIÊN TỤC NỘI PHÂN HỌ (`COVERAGE ESM %` TRÊN $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$)
*(Hiện thực hóa tại [`src/similarity/dense_similarity.py`](./RareProtSelect/src/similarity/dense_similarity.py), [`experiments/exp3_esm_coverage_a1a.py`](./RareProtSelect/experiments/exp3_esm_coverage_a1a.py) và [`experiments/exp4_cross_eval_a1a.py`](./RareProtSelect/experiments/exp4_cross_eval_a1a.py))*

### Thiết lập toán học chung của Nhóm 2:
- Trên tập chuẩn hóa Phương án 3B ($|V| = 4,120$ chuỗi), mỗi chuỗi protein $v \in V$ được trích xuất vector nhúng ngữ nghĩa $z_v \in \mathbb{R}^{480}$ từ mô hình **ESM-2** (`facebook/esm2_t12_35M_UR50D`), dịch tâm $\beta = 0.70$ và chuẩn hóa $\ell_2$:
  $$\mu = \frac{1}{|V|} \sum_{v \in V} z_v, \qquad z'_v = \frac{z_v - 0.70\mu}{\|z_v - 0.70\mu\|_2 + \epsilon}, \qquad \mathbf{S}_{\text{ESM}}^{(\beta=0.70)}(u, v) = \max\left(0.0, {z'_u}^\top z'_v\right) \in [0.0, 1.0]$$
- Với tập đại diện $S_k$, **điểm bao phủ ngữ nghĩa nội phân họ của từng chuỗi $v \in V_g$** chỉ được tính từ các đại diện cùng phân họ $g$ ($S_{k,g} = S_k \cap V_g$):
  $$c_v^{\text{within}}(S_k) = \begin{cases} 0.0 & \text{nếu } S_k \cap V_g = \emptyset \\ \max_{s \in S_k \cap V_g} \mathbf{S}_{\text{ESM}}^{(\beta=0.70)}(v, s) & \text{nếu } S_k \cap V_g \neq \emptyset \end{cases}$$
- **Độ bao phủ ngữ nghĩa nội phân họ của phân họ $g \in \{1..115\}$**:
  $$\operatorname{Cov}_g^{\text{within}}(S_k) = \frac{1}{|V_g|} \sum_{v \in V_g} c_v^{\text{within}}(S_k) \times 100\%$$

---

### 2.1. `overall_coverage_esm_pct` (Độ bao phủ ngữ nghĩa nội phân họ toàn tập $4,120$ chuỗi)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Overall\_Cov}_{\text{ESM}}^{\text{within}}(S_k) = \frac{1}{|V|} \sum_{v \in V} c_v^{\text{within}}(S_k) \times 100\%, \qquad |V| = 4,120$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đo mức độ tương đồng cấu trúc – ngữ nghĩa trung bình của toàn bộ $4,120$ chuỗi protein tới đại diện gần nhất nằm trong cùng phân họ của chúng trên không gian liên tục ESM-2 ($\beta = 0.70$).
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Nếu $|V| = 4$ chuỗi thuộc 2 phân họ $V_{g_1} = \{v_1, v_2\}$ (đã có đại diện $s_1 = v_1$ với $\mathbf{S}_{\text{ESM}}(v_1, s_1) = 1.00$, $\mathbf{S}_{\text{ESM}}(v_2, s_1) = 0.80$) và $V_{g_2} = \{v_3, v_4\}$ (chưa có đại diện nên $c_{v_3}^{\text{within}} = c_{v_4}^{\text{within}} = 0.0$), thì $\operatorname{Overall\_Cov}_{\text{ESM}}^{\text{within}} = \frac{1.00 + 0.80 + 0.0 + 0.0}{4} \times 100\% = 45.0\%$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` đạt `34.8%` ($\alpha=0.0$), `29.29%` ($\alpha=0.5$), `23.0%` ($\alpha=1.0$); `ESM-2` đạt `29.65%` ($\alpha=0.0$), `18.77%` ($\alpha=0.5$), `15.01%` ($\alpha=1.0$).
   - Tại **$k = 115$**: `BLASTp` đạt `87.47%` ($\alpha=0.0$), `86.88%` ($\alpha=0.5$), `72.75%` ($\alpha=1.0$); `ESM-2` đạt `84.2%` ($\alpha=0.0$), `82.8%` ($\alpha=0.5$), `82.38%` ($\alpha=1.0$).

---

### 2.2. `worst_group_coverage_esm_pct` (Độ bao phủ ngữ nghĩa nội phân họ của phân họ thấp nhất trên $115$ họ)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Worst\_Cov}_{\text{ESM}}^{\text{within}}(S_k) = \min_{g \in \{1..115\}} \operatorname{Cov}_g^{\text{within}}(S_k)$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Tương tự `worst_group_sensitivity_blast_pct`, dưới cơ chế truy vấn ngược nội phân họ, bất kỳ phân họ $g$ nào chưa có đại diện trực tiếp trong $S_k$ ($S_k \cap V_g = \emptyset$) đều có $\operatorname{Cov}_g^{\text{within}}(S_k) = 0.0\%$.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Với $\operatorname{Cov}_{g_1}^{\text{within}} = 90.0\%$ và $\operatorname{Cov}_{g_2}^{\text{within}} = 0.0\%$, ta có $\operatorname{Worst\_Cov}_{\text{ESM}}^{\text{within}} = \min(90.0\%, 0.0\%) = 0.0\%$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Bằng `0.0%` tại mọi $k < 115$ và giữ ở `0.0%` tại $k = 115$ khi vẫn còn ít nhất một phân họ chưa có đại diện trực tiếp trong $S_{115}$.

---

### 2.3. `rare_coverage_esm_pct` (Độ bao phủ ngữ nghĩa nội phân họ trung bình trên $45$ phân họ hiếm $\le 5$ chuỗi)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Rare\_Cov}_{\text{ESM}}^{\text{within}}(S_k) = \frac{1}{45} \sum_{g \in G_{\text{rare}}} \operatorname{Cov}_g^{\text{within}}(S_k)$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đo chất lượng đại diện cấu trúc – ngữ nghĩa nội phân họ trung bình trên $45$ phân họ hiếm ($n_g \le 5$).
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Nếu trong $45$ phân họ hiếm có $1$ phân họ đơn độc ($n_g=1$) được chọn làm đại diện ($\operatorname{Cov}_g^{\text{within}} = 100.0\%$) và $44$ phân họ hiếm còn lại chưa được chọn ($0.0\%$), thì $\operatorname{Rare\_Cov}_{\text{ESM}}^{\text{within}} = \frac{100.0\%}{45} \approx \mathbf{2.22\%}$. Nếu phân họ hiếm được chọn có $n_g = 2$ chuỗi với điểm bao phủ trung bình $92.25\%$, thì $\operatorname{Rare\_Cov}_{\text{ESM}}^{\text{within}} = \frac{92.25\%}{45} = \mathbf{2.05\%}$ (khớp chính xác dòng 14 của `exp3_esm_coverage_a1a.csv` và dòng 43 của `exp4_cross_eval_a1a.csv`).
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: Tăng từ `0.0%` ($\alpha=0.0$) lên `4.27%` (`BLASTp`, $\alpha=1.0$) và `4.44%` (`ESM-2`, $\alpha=1.0$).
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Tăng vọt từ **`2.05%`** ($\alpha = 0.0$) $\to$ **`58.29%`** ($\alpha = 0.5$) $\to$ **`89.69%`** ($\alpha = 1.0$).
     - Trên `ESM-2`: Tăng từ **`12.85%`** ($\alpha = 0.0$) $\to$ **`43.21%`** ($\alpha = 0.5$) $\to$ **`40.86%`** ($\alpha = 1.0$).

---

### 2.4. `macro_coverage_esm_pct` (Độ bao phủ ngữ nghĩa nội phân họ trung bình bình đẳng trên $115$ phân họ)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   $$\operatorname{Macro\_Cov}_{\text{ESM}}^{\text{within}}(S_k) = \frac{1}{115} \sum_{g=1}^{115} \operatorname{Cov}_g^{\text{within}}(S_k)$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Trung bình cộng không trọng số của độ bao phủ ngữ nghĩa nội phân họ trên toàn bộ $115$ phân họ.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Nếu tại $k = 1$, phân họ duy nhất được chọn có độ bao phủ nội phân họ bằng $83.95\%$ và $114$ phân họ còn lại bằng $0.0\%$, thì $\operatorname{Macro\_Cov}_{\text{ESM}}^{\text{within}} = \frac{83.95\%}{115} = \mathbf{0.73\%}$ (khớp chính xác dòng 2 của `exp3_esm_coverage_a1a.csv`).
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp4_cross_eval_a1a.csv`)**:
   - Tại **$k = 11$**: Đạt `7.97% -> 8.65% -> 8.66%` trên `BLASTp` và `8.73% -> 8.8% -> 8.87%` trên `ESM-2`.
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Tăng mạnh từ **`45.77%`** ($\alpha = 0.0$) $\to$ **`74.74%`** ($\alpha = 0.5$, `+28.97%`) $\to$ **`79.82%`** ($\alpha = 1.0$, `+34.05%`).
     - Trên `ESM-2`: Tăng từ **`47.24%`** ($\alpha = 0.0$) $\to$ **`62.36%`** ($\alpha = 0.5$, `+15.12%`) $\to$ **`59.85%`** ($\alpha = 1.0$).

---

## 3. NHÓM 3: BỘ 4 CHỈ SỐ ĐÁNH GIÁ CẤU TRÚC ĐẠI DIỆN TRỰC TIẾP & ĐỘ DƯ THỪA PHÂN HỌ TRONG TẬP $S_k$ (NHÁNH 5)
*(Hiện thực hóa tại [`experiments/exp5_subfamily_allocation_a1a.py`](./RareProtSelect/experiments/exp5_subfamily_allocation_a1a.py))*

### Thiết lập toán học chung của Nhóm 3:
Với tập đại diện $S_k = \{s_1, s_2, \dots, s_k\}$ gồm $k$ chuỗi đầu tiên trong danh sách đồng thuận ($k \in [1..115]$):
- Gọi $c_g(S_k) = |S_k \cap V_g|$ là **số lượng chuỗi đại diện trong $S_k$ thuộc về phân họ $g \in \{1..115\}$**:
  $$\sum_{g=1}^{115} c_g(S_k) = k$$
- Gọi $\mathcal{G}(S_k) = \{g \in \{1..115\} \mid c_g(S_k) \ge 1\}$ là **tập hợp các phân họ có ít nhất 1 đại diện trực tiếp trong $S_k$**.
- Gọi $\mathcal{G}_{\text{rare}}(S_k) = \mathcal{G}(S_k) \cap G_{\text{rare}}$ là **tập hợp các phân họ hiếm ($n_g \le 5$, $|G_{\text{rare}}| = 45$) có ít nhất 1 đại diện trực tiếp trong $S_k$**.

---

### 3.1. `subfamily_repr_rate_pct` (Tỷ lệ phân họ trên $115$ họ có đại diện trực tiếp trong $S_k$)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   *(Đi kèm cột đếm nguyên `subfamilies_represented_count` $= |\mathcal{G}(S_k)|$)*
   $$\operatorname{Subfamily\_Repr}(S_k) = \frac{|\mathcal{G}(S_k)|}{115} \times 100\%$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Cho biết trực tiếp có bao nhiêu phần trăm trong tổng số $115$ phân họ thực sự có ít nhất một "đại biểu" góp mặt trong tập đại diện $S_k$.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Tại $k = 115$, nếu tập $S_{115}$ có mặt đại diện của $|\mathcal{G}(S_{115})| = 97$ phân họ khác nhau, thì $\operatorname{Subfamily\_Repr}(S_{115}) = \frac{97}{115} \times 100\% \approx \mathbf{84.35\%}$ (khớp chính xác dòng 61 của `exp5_subfamily_allocation_a1a.csv`).
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp5_subfamily_allocation_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` ($\alpha=0.0$) chỉ đạt `10/115` (`8.7%`), trong khi cả 5 cấu hình còn lại đạt tuyệt đối `11/115` (`9.57%`).
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Tăng vọt từ **`57/115` (`49.57%`)** ở $\alpha = 0.0$ $\to$ **`92/115` (`80.0%`)** ở $\alpha = 0.5$ $\to$ **`97/115` (`84.35%`)** ở $\alpha = 1.0$.
     - Trên `ESM-2`: Tăng từ **`59/115` (`51.3%`)** ở $\alpha = 0.0$ $\to$ **`77/115` (`66.96%`)** ở $\alpha = 0.5$ $\to$ **`74/115` (`64.35%`)** ở $\alpha = 1.0$.

---

### 3.2. `rare_repr_rate_pct` (Tỷ lệ phân họ hiếm trên $45$ họ hiếm có đại diện trực tiếp trong $S_k$)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   *(Đi kèm cột đếm nguyên `rare_subfamilies_represented_count` $= |\mathcal{G}_{\text{rare}}(S_k)|$)*
   $$\operatorname{Rare\_Repr}(S_k) = \frac{|\mathcal{G}_{\text{rare}}(S_k)|}{45} \times 100\%$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Đếm trực tiếp số phân họ hiếm ($\le 5$ chuỗi) được chọn vào tập đại diện $S_k$.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Tại $k = 115$, nếu có $|\mathcal{G}_{\text{rare}}(S_{115})| = 41$ phân họ hiếm được chọn trong tổng số $45$ phân họ hiếm, thì $\operatorname{Rare\_Repr}(S_{115}) = \frac{41}{45} \times 100\% \approx \mathbf{91.11\%}$ (khớp chính xác dòng 61 của `exp5_subfamily_allocation_a1a.csv`).
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp5_subfamily_allocation_a1a.csv`)**:
   - Tại **$k = 11$**: Phương pháp không trọng số $\alpha = 0.0$ chọn **`0/45` (`0.0%`)** họ hiếm trên cả `BLASTp` và `ESM-2`; khi bật $\alpha = 1.0$, cả `BLASTp` và `ESM-2` chọn được **`2/45` (`4.44%`)** họ hiếm.
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Tăng gấp **`41.0x`** từ **`1/45` (`2.22%`)** ở $\alpha = 0.0$ $\to$ **`27/45` (`60.0%`)** ở $\alpha = 0.5$ $\to$ **`41/45` (`91.11%`)** ở $\alpha = 1.0$.
     - Trên `ESM-2`: Tăng từ **`6/45` (`13.33%`)** ở $\alpha = 0.0$ $\to$ **`20/45` (`44.44%`)** ở $\alpha = 0.5$ $\to$ **`19/45` (`42.22%`)** ở $\alpha = 1.0$.

---

### 3.3. `subfamily_redundancy_pct` (Độ dư thừa phân bổ phân họ — % số ghế trong $k$ bị trùng lặp phân họ)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   *(Đi kèm cột đếm nguyên `redundant_slots_count` $= k - |\mathcal{G}(S_k)|$)*
   $$\operatorname{Subfamily\_Redundancy}(S_k) = \frac{\sum_{g \,:\, c_g(S_k) \ge 2} \left(c_g(S_k) - 1\right)}{k} \times 100\% = \frac{k - |\mathcal{G}(S_k)|}{k} \times 100\%$$
   Tại mốc ngân sách $k = G = 115$, ta luôn có hằng đẳng thức bù:
   $$\operatorname{Subfamily\_Repr}(S_{115}) + \operatorname{Subfamily\_Redundancy}(S_{115}) = 100.00\%$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Định lượng tỷ lệ phần trăm ngân sách bị lãng phí vào việc chọn đại diện thứ 2, thứ 3... cho cùng một phân họ trong khi các phân họ khác chưa có nổi đại diện đầu tiên.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Tại $k = 115$, nếu $|\mathcal{G}(S_{115})| = 57$ phân họ có đại diện, thì số suất trùng lặp là $115 - 57 = 58$ suất $\implies \operatorname{Subfamily\_Redundancy}(S_{115}) = \frac{58}{115} \times 100\% \approx \mathbf{50.43\%}$, và $49.57\% + 50.43\% = 100.00\%$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp5_subfamily_allocation_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` ($\alpha=0.0$) đã sớm lãng phí `1/11` suất (`9.09%`), trong khi 5 cấu hình còn lại giữ mức dư thừa **`0.0%`** (`0` suất). Đặc biệt, `BLASTp` ($\alpha = 1.0$) duy trì **`0.0%` dư thừa suốt từ $k = 1$ đến $k = 30$**!
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Giảm mạnh từ **`58` suất (`50.43%`)** ở $\alpha = 0.0$ xuống **`23` suất (`20.0%`)** ở $\alpha = 0.5$ và xuống chỉ còn **`18` suất (`15.65%`)** ở $\alpha = 1.0$.
     - Trên `ESM-2`: Giảm từ **`56` suất (`48.7%`)** ở $\alpha = 0.0$ xuống **`38` suất (`33.04%`)** ở $\alpha = 0.5$ và **`41` suất (`35.65%`)** ở $\alpha = 1.0$.

---

### 3.4. `dominant_a01_009_share_pct` (Tỷ trọng độc chiếm ngân sách của phân họ lớn nhất `A01.009` — Cathepsin D, $329$ chuỗi)

1. **Công thức toán học & Giải nghĩa ký hiệu**:
   *(Đi kèm cột đếm nguyên `dominant_a01_009_count` $= c_{\text{A01.009}}(S_k)$)*
   $$\operatorname{Dominant\_Share}(S_k) = \frac{c_{\text{A01.009}}(S_k)}{k} \times 100\% = \frac{|S_k \cap V_{\text{A01.009}}|}{k} \times 100\%$$
2. **Ý nghĩa sinh học & Thực tiễn**:
   - Theo dõi trực tiếp mức độ lấn át ngân sách của phân họ lớn nhất `A01.009` ($329$ chuỗi, chiếm $7.99\%$ tập dữ liệu). Ở chế độ lý tưởng không dư thừa, `A01.009` chỉ cần đúng $1$ hoặc $2$ đại diện để bao phủ nội phân họ.
3. **`[Ví dụ Minh họa Toán học - Giả định tính tay từng bước]`**:
   - Tại $k = 115$, nếu `A01.009` chiếm $6$ suất trong $S_{115}$, thì $\operatorname{Dominant\_Share}(S_{115}) = \frac{6}{115} \times 100\% \approx \mathbf{5.22\%}$.
4. **Quy luật biến thiên thực nghiệm theo $\alpha \in \{0.0, 0.5, 1.0\}$ và so sánh `BLASTp` vs. `ESM-2` (Trích từ `exp5_subfamily_allocation_a1a.csv`)**:
   - Tại **$k = 11$**: `BLASTp` ($\alpha=0.0$) lấy `2/11` suất (`18.18%`) cho `A01.009`; `BLASTp` ($\alpha=0.5, 1.0$) và `ESM-2` ($\alpha=0.0$) chỉ lấy `1/11` suất (`9.09%`); `ESM-2` ($\alpha=0.5, 1.0$) lấy `0` suất (`0.0%`).
   - Tại **$k = 115$**:
     - Trên `BLASTp`: Số ghế của `A01.009` giảm từ **`6` ghế (`5.22%`)** ở $\alpha = 0.0$ xuống **`3` ghế (`2.61%`)** ở $\alpha = 0.5$ và **`2` ghế (`1.74%`)** ở $\alpha = 1.0$.
     - Trên `ESM-2`: Số ghế của `A01.009` giảm từ **`7` ghế (`6.09%`)** ở $\alpha = 0.0$ xuống **`4` ghế (`3.48%`)** ở $\alpha = 0.5$ và chỉ còn đúng **`1` ghế (`0.87%`)** ở $\alpha = 1.0$.

---

## 4. CÁC BẢNG SỐ LIỆU ĐỐI CHUẨN NGUYÊN VĂN TỪ TỆP KẾT QUẢ CSV (NHÁNH 1 $\to$ NHÁNH 5)

### 4.1. Bảng Đối chuẩn Hình 8A Bài báo gốc (Nhánh 1 — Trích nguyên văn 100% từ [`exp1_baseline_a1a_calibration.csv`](./RareProtSelect/outputs/tables/exp1_baseline_a1a_calibration.csv))

| `budget_k` | `num_selected` | `overall_sensitivity_blast_pct` | `retrieved_hits_count` | `total_cleaned_sequences` | `published_fig8_sensitivity_pct` | `deviation_pct` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1` | `1` | `82.36` | `10959` | `13307` | `80.5` | `1.86` |
| `2` | `2` | `83.55` | `11118` | `13307` | `83.5` | `0.05` |
| `3` | `3` | `85.85` | `11424` | `13307` | `85.7` | `0.15` |
| `4` | `4` | `86.88` | `11561` | `13307` | `86.7` | `0.18` |
| `5` | `5` | `88.1` | `11723` | `13307` | `88.0` | `0.1` |
| `6` | `6` | `88.17` | `11733` | `13307` | `88.1` | `0.07` |
| `7` | `7` | `88.77` | `11813` | `13307` | `88.4` | `0.37` |
| `8` | `8` | `90.51` | `12044` | `13307` | `89.0` | `1.51` |
| `9` | `9` | `90.66` | `12064` | `13307` | `90.7` | `-0.04` |
| `10` | `10` | `91.43` | `12167` | `13307` | `90.8` | `0.63` |
| `11` | `11` | `91.59` | `12188` | `13307` | `90.9` | `0.69` |

---

### 4.2. Bảng Đối chiếu 9 Chỉ số Nhóm 1 & Nhóm 2 tại $k = 11$ và $k = 115$ (Nhánh 2, 3, 4 — Trích nguyên văn 100% từ [`exp4_cross_eval_a1a.csv`](./RareProtSelect/outputs/tables/exp4_cross_eval_a1a.csv), Dòng 12, 21, 32, 41, 52, 61, 72, 81, 92, 101, 112, 121)

| `selection_space` | `alpha` | `budget_k` | `overall_sensitivity_blast_pct` | `worst_group_sensitivity_blast_pct` | `rare_sensitivity_blast_pct` | `macro_sensitivity_blast_pct` | `zero_cov_subfamilies_count` | `overall_coverage_esm_pct` | `worst_group_coverage_esm_pct` | `rare_coverage_esm_pct` | `macro_coverage_esm_pct` | `retrieved_hits_count` | `total_cleaned_sequences` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `BLASTp` | `0.0` | `11` | `38.06` | `0.0` | `0.0` | `8.68` | `105` | `34.8` | `0.0` | `0.0` | `7.97` | `1568` | `4120` |
| `BLASTp` | `0.0` | `115` | `93.57` | `0.0` | `2.22` | `49.28` | `58` | `87.47` | `0.0` | `2.05` | `45.77` | `3855` | `4120` |
| `BLASTp` | `0.5` | `11` | `32.6` | `0.0` | `0.0` | `9.56` | `104` | `29.29` | `0.0` | `0.0` | `8.65` | `1343` | `4120` |
| `BLASTp` | `0.5` | `115` | `94.13` | `0.0` | `59.11` | `78.87` | `23` | `86.88` | `0.0` | `58.29` | `74.74` | `3878` | `4120` |
| `BLASTp` | `1.0` | `11` | `26.07` | `0.0` | `4.44` | `9.57` | `104` | `23.0` | `0.0` | `4.27` | `8.66` | `1074` | `4120` |
| `BLASTp` | `1.0` | `115` | `79.08` | `0.0` | `91.11` | `83.44` | `18` | `72.75` | `0.0` | `89.69` | `79.82` | `3258` | `4120` |
| `ESM-2` | `0.0` | `11` | `32.18` | `0.0` | `0.0` | `9.45` | `104` | `29.65` | `0.0` | `0.0` | `8.73` | `1326` | `4120` |
| `ESM-2` | `0.0` | `115` | `90.7` | `0.0` | `13.33` | `50.95` | `56` | `84.2` | `0.0` | `12.85` | `47.24` | `3737` | `4120` |
| `ESM-2` | `0.5` | `11` | `20.36` | `0.0` | `2.22` | `9.49` | `104` | `18.77` | `0.0` | `2.22` | `8.8` | `839` | `4120` |
| `ESM-2` | `0.5` | `115` | `89.98` | `0.0` | `43.11` | `66.05` | `38` | `82.8` | `0.0` | `43.21` | `62.36` | `3707` | `4120` |
| `ESM-2` | `1.0` | `11` | `16.33` | `0.0` | `4.44` | `9.45` | `104` | `15.01` | `0.0` | `4.44` | `8.87` | `673` | `4120` |
| `ESM-2` | `1.0` | `115` | `87.79` | `0.0` | `41.33` | `63.15` | `41` | `82.38` | `0.0` | `40.86` | `59.85` | `3617` | `4120` |

---

### 4.3. Bảng Đối chiếu 8 Cột Nhóm 3 tại $k = 11$ và $k = 115$ (Nhánh 5 — Trích nguyên văn 100% từ [`exp5_subfamily_allocation_a1a.csv`](./RareProtSelect/outputs/tables/exp5_subfamily_allocation_a1a.csv), Dòng 12, 21, 32, 41, 52, 61, 72, 81, 92, 101, 112, 121)

| `selection_space` | `alpha` | `budget_k` | `subfamilies_represented_count` | `subfamily_repr_rate_pct` | `rare_subfamilies_represented_count` | `rare_repr_rate_pct` | `redundant_slots_count` | `subfamily_redundancy_pct` | `dominant_a01_009_count` | `dominant_a01_009_share_pct` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `BLASTp` | `0.0` | `11` | `10` | `8.7` | `0` | `0.0` | `1` | `9.09` | `2` | `18.18` |
| `BLASTp` | `0.0` | `115` | `57` | `49.57` | `1` | `2.22` | `58` | `50.43` | `6` | `5.22` |
| `BLASTp` | `0.5` | `11` | `11` | `9.57` | `0` | `0.0` | `0` | `0.0` | `1` | `9.09` |
| `BLASTp` | `0.5` | `115` | `92` | `80.0` | `27` | `60.0` | `23` | `20.0` | `3` | `2.61` |
| `BLASTp` | `1.0` | `11` | `11` | `9.57` | `2` | `4.44` | `0` | `0.0` | `1` | `9.09` |
| `BLASTp` | `1.0` | `115` | `97` | `84.35` | `41` | `91.11` | `18` | `15.65` | `2` | `1.74` |
| `ESM-2` | `0.0` | `11` | `11` | `9.57` | `0` | `0.0` | `0` | `0.0` | `1` | `9.09` |
| `ESM-2` | `0.0` | `115` | `59` | `51.3` | `6` | `13.33` | `56` | `48.7` | `7` | `6.09` |
| `ESM-2` | `0.5` | `11` | `11` | `9.57` | `1` | `2.22` | `0` | `0.0` | `0` | `0.0` |
| `ESM-2` | `0.5` | `115` | `77` | `66.96` | `20` | `44.44` | `38` | `33.04` | `4` | `3.48` |
| `ESM-2` | `1.0` | `11` | `11` | `9.57` | `2` | `4.44` | `0` | `0.0` | `0` | `0.0` |
| `ESM-2` | `1.0` | `115` | `74` | `64.35` | `19` | `42.22` | `41` | `35.65` | `1` | `0.87` |

*(Xem trọn vẹn toàn bộ 60 dòng của Nhánh 2, 60 dòng của Nhánh 3, 120 dòng của Nhánh 4 và 120 dòng của Nhánh 5 tại [`bao_cao_ket_qua_chi_tiet_topic2.md`](./bao_cao_ket_qua_chi_tiet_topic2.md)).*

---

## 5. MA TRẬN TRUY VẾT MÃ NGUỒN & TỆP KẾT QUẢ QUA CÁC NHÁNH (CODEBASE TRACEABILITY)

| Nhánh Thực Nghiệm | Thành Phần Thước Đo / Thuật Toán | Tệp Mã Nguồn Hiện Thực | Hàm / Class Chịu Trách Nhiệm | Tệp CSV Đầu Ra Nguyên Bản |
| :--- | :--- | :--- | :--- | :--- |
| **Nhánh 1** | `overall_sensitivity_blast_pct` toàn cục ($13,307$ chuỗi, $k \in [1..11]$) | [`src/similarity/blast_similarity.py`](./RareProtSelect/src/similarity/blast_similarity.py) & [`experiments/exp1_baseline_a1a_calibration.py`](./RareProtSelect/experiments/exp1_baseline_a1a_calibration.py) | `BLASTSimilarityMatrix.retrieve_blast_hits()`, `run_exp1_baseline_a1a_calibration()` | [`exp1_baseline_a1a_calibration.csv`](./RareProtSelect/outputs/tables/exp1_baseline_a1a_calibration.csv) (`11` dòng, `7` cột) |
| **Nhánh 2** | Bộ 5 chỉ số `Live BLASTp Sensitivity (%)` nội phân họ ($4,120$ chuỗi, $115$ họ, $\alpha \in \{0.0, 0.5, 1.0\}$, $k \in [1..115]$) | [`src/selection/pruned_greedy.py`](./RareProtSelect/src/selection/pruned_greedy.py) & [`experiments/exp2_rare_weighted_a1a.py`](./RareProtSelect/experiments/exp2_rare_weighted_a1a.py) | `compute_subfamily_weights()`, `evaluate_rare_aware_representatives()` | [`exp2_rare_weighted_a1a.csv`](./RareProtSelect/outputs/tables/exp2_rare_weighted_a1a.csv) (`60` dòng, `10` cột) |
| **Nhánh 3** | Bộ 4 chỉ số `Coverage ESM (%)` nội phân họ trên $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$ ($4,120$ chuỗi, $115$ họ, $\alpha \in \{0.0, 0.5, 1.0\}$, $k \in [1..115]$) | [`src/similarity/dense_similarity.py`](./RareProtSelect/src/similarity/dense_similarity.py) & [`experiments/exp3_esm_coverage_a1a.py`](./RareProtSelect/experiments/exp3_esm_coverage_a1a.py) | `compute_mean_centered_cosine_matrix()`, `evaluate_esm_coverage_representatives()` | [`exp3_esm_coverage_a1a.csv`](./RareProtSelect/outputs/tables/exp3_esm_coverage_a1a.csv) (`60` dòng, `9` cột) |
| **Nhánh 4** | Kiểm tra chéo $2 \times 2$ nội phân họ trên toàn bộ **9 chỉ số** (5 `BLASTp Sens %` + 4 `Coverage ESM %`) | [`experiments/exp4_cross_eval_a1a.py`](./RareProtSelect/experiments/exp4_cross_eval_a1a.py) | `load_cached_consensus_ids()`, `run_exp4_cross_eval_a1a()` | [`exp4_cross_eval_a1a.csv`](./RareProtSelect/outputs/tables/exp4_cross_eval_a1a.csv) (`120` dòng, `14` cột) |
| **Nhánh 5** | Bộ 4 chỉ số Cấu trúc Đại diện Trực tiếp & Độ Dư thừa Phân họ trong $S_k$ (`subfamily_repr_rate_pct`, `rare_repr_rate_pct`, `subfamily_redundancy_pct`, `dominant_a01_009_share_pct`) kèm 4 cột đếm nguyên | [`configs/config_exp5_subfamily_allocation_a1a.yaml`](./RareProtSelect/configs/config_exp5_subfamily_allocation_a1a.yaml), [`experiments/exp5_subfamily_allocation_a1a.py`](./RareProtSelect/experiments/exp5_subfamily_allocation_a1a.py) | `load_cached_consensus_ids()`, `evaluate_subfamily_allocation_metrics()`, `verify_exp5_mathematical_invariants()`, `run_exp5_subfamily_allocation_a1a()` | [`exp5_subfamily_allocation_a1a.csv`](./RareProtSelect/outputs/tables/exp5_subfamily_allocation_a1a.csv) (`120` dòng, `11` cột) |

---
*Tài liệu được bảo chứng bởi Nhóm nghiên cứu Đề tài 2 © 2026. Mọi công thức và con số thực nghiệm đều được phân định cấp độ minh bạch tuyệt đối.*
