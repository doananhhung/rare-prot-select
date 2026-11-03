# TỔNG HỢP & PHÂN TÍCH: BÀI BÁO NỀN (NGUYEN ET AL., 2025) VÀ ĐỀ TÀI 2 (RAREPROTSELECT)

> **Hướng dẫn điều hướng giữa 2 tệp trong VS Code**:
> * **Trong cửa sổ soạn thảo (Editor)**: Giữ phím **`Ctrl` + Click chuột trái** vào liên kết màu xanh để mở ngay file giải thích.
> * **Trong cửa sổ xem trước (Preview)**: Nhấn **`Ctrl + Shift + V`** để mở preview, sau đó **Click chuột trực tiếp** vào liên kết để chuyển file.

---

## 1. BỐI CẢNH VÀ BÀI TOÁN TỔNG QUÁT

* **Bài toán**: Cho một họ protein (Protein Family) gồm tập hợp $V = \{v_1, v_2, \dots, v_n\}$ chứa hàng nghìn đến hàng triệu chuỗi amino acid. Mục tiêu là chọn ra một tập con đại diện $S \subseteq V$ với kích thước ngân sách $|S| \le k$ ($k \ll n$) sao cho:
  1. **Bao phủ tối đa (Maximum Coverage)**: Đại diện đầy đủ không gian chuỗi, cấu trúc và chức năng của toàn bộ họ.
  2. **Hạn chế trùng lặp (Minimum Redundancy)**: Loại bỏ các chuỗi gần như giống hệt nhau.
  3. **Bảo tồn nhóm hiếm (Rare-Awareness)**: Không để các phân họ lớn lấn át các phân họ/nhánh tiến hóa nhỏ, hiếm (*long-tail groups*).
  4. **Kiểm soát ngân sách linh hoạt**: Người dùng chủ động khống chế kích thước $k$ theo nhu cầu lưu trữ/tính toán.

* **Hạn chế của phương pháp phân cụm truyền thống (CD-HIT, MMseqs2)**:
  * Phụ thuộc vào ngưỡng đồng nhất cố định (*hard threshold*). Nếu ngưỡng quá cao sẽ sinh ra quá nhiều cụm (hàng nghìn chuỗi đại diện); nếu ngưỡng quá thấp sẽ bỏ sót các mối quan hệ quan trọng.
  * Không cho phép ấn định trước số lượng đại diện $k$.

---

<a id="bang-so-sanh"></a>
## 2. SO SÁNH MÔ HÌNH TOÁN HỌC: BÀI BÁO NỀN vs. ĐỀ TÀI 2

*(Nhấp vào các thuật ngữ có gạch chân để mở tệp **giai_thich_khai_niem.md** tại đúng vị trí tương ứng)*

| Thành phần | Bài báo nền (Nguyen et al., *Scientific Reports* 2025) | Đề tài 2 (RareProtSelect - Hướng phát triển) |
| :--- | :--- | :--- |
| **Không gian biểu diễn** | Chuỗi ký tự thô ([**FASTA**](./giai_thich_khai_niem.md#fasta)) | Đối chứng hai không gian: Căn chỉnh cục bộ **BLASTp** vs. Vector nhúng ngữ nghĩa $z(v) \in \mathbb{R}^d$ sinh bởi [**ESM-2 PLM**](./giai_thich_khai_niem.md#esm2-plm) |
| **Hàm tương đồng $\operatorname{sim}(u, v)$** | Tỷ lệ amino acid khớp nhau qua BLAST (% Identity) | BLASTp Identity ($\mathbf{S}_{\text{BLAST}}$) vs. Cosine similarity dịch tâm: $\max\{0, \cos(z'(u), z'(v))\}$ ($\mathbf{S}_{\text{ESM}}$) |
| **Cơ chế trọng số** | **Unweighted**: Mọi chuỗi có trọng số bằng nhau ($w_v = 1.0$, ứng với $\alpha = 0.0$) | **Rare-Aware**: Họ trọng số tần suất nghịch đảo $w_v^{(\alpha)} = (n_{g(v)})^{-\alpha}$ với $\alpha \in \{0.0, 0.5, 1.0\}$ (trọng tâm cân bằng Pareto $\alpha = 0.5 \implies w_v = \frac{1}{\sqrt{n_{g(v)}}}$) |
| **Hàm mục tiêu $F(S)$** | [**Facility Location**](./giai_thich_khai_niem.md#facility-location-unweighted): $F(S) = \sum_{v \in V} \max_{s \in S} \phi(v, s)$ | [**Weighted Facility Location**](./giai_thich_khai_niem.md#weighted-facility-location): $F_\alpha(S) = \sum_{v \in V} w_v^{(\alpha)} \max_{s \in S} \operatorname{sim}(v, s)$ |
| **Xử lý mất cân bằng** | Không xử lý; nhóm lớn áp đảo hoàn toàn nhóm nhỏ | Trọng số $w_v^{(\alpha)}$ nén quyền lực nhóm lớn, tăng lực kéo toán học cho nhóm hiếm |
| **Thuật toán tối ưu** | [**Pruned Greedy 90% (1,000-Shuffle Consensus)**](./giai_thich_khai_niem.md#standard-greedy) / [**Bidirectional Greedy**](./giai_thich_khai_niem.md#bidirectional-greedy) | Giữ nguyên bộ giải chuẩn của bài báo nền để cô lập biến số (*Ceteris Paribus*) / Mở rộng [**Lazy Greedy WFL**](./giai_thich_khai_niem.md#lazy-greedy) |
| **Nhiệm vụ kiểm chứng** | Đánh giá gộp toàn cục: Tái tạo cơ sở dữ liệu qua duy nhất chỉ số `Overall Sensitivity BLAST (%)` | Chuỗi 5 nhánh thực nghiệm tuần tự trả lời **5 Câu hỏi Nghiên cứu (`RQ1` $\to$ `RQ5`)**:<br>1. **Đánh giá thu hồi nội phân họ (`Within-Subfamily Representative Query`: $S_k \cap V_g \to V_g$)**.<br>2. **Kiểm tra chéo hai chiều ($2 \times 2$ Cross-Space Evaluation)** giữa `BLASTp` và `ESM-2`.<br>3. **Phân tích trực tiếp tỷ lệ đại diện phân họ & độ dư thừa ngân sách trong $S_k$**. |

### Chi tiết các điểm đột phá của Đề tài 2:

1. **Từ BLAST Sequence Identity $\rightarrow$ ESM-2 Embeddings**:
   * *BLAST* chỉ so sánh ký tự amino acid bề mặt. Hai protein có cùng cấu trúc 3D và chức năng nhưng đột biến nhiều chuỗi (*remote homology*) sẽ bị BLAST gán điểm tương đồng bằng $0$.
   * *ESM-2 PLM* nắm bắt thông tin cấu trúc bậc 3, vị trí tâm hoạt động và ngữ cảnh tiến hóa sâu, cho phép đo lường chính xác độ tương đồng chức năng.
2. **Từ Unweighted $\rightarrow$ Rare-Aware Weighting**:
   * Hàm Facility Location không trọng số của bài báo nền tối ưu hóa *Overall Coverage*. Do đó, nếu họ protein có 95% chuỗi nhóm A và 5% chuỗi nhóm B, thuật toán sẽ dồn đại diện cho nhóm A để tối đa hóa điểm trung bình.
   * Đề tài 2 đưa vào trọng số $w_v = \frac{1}{\sqrt{n_{g(v)}}}$ (với $n_{g(v)}$ là quy mô nhóm của chuỗi $v$). Nhóm càng hiếm thì $w_v$ càng lớn, tạo ra *Marginal Gain* cao, buộc Greedy phải chọn đại diện cho nhóm hiếm từ sớm.

---

## 3. KẾT QUẢ ĐÁNH GIÁ CỦA THUẬT TOÁN GREEDY TRONG BÀI BÁO NỀN

Bài báo nền đã thực nghiệm thuật toán [**Greedy**](./giai_thich_khai_niem.md#standard-greedy) trên 27 họ Thioesterase (TE - ThYme DB, 737 chuỗi), họ Carboxylesterase (CE - ESTHER DB, 12,277 chuỗi) và họ Peptidase A1 (A1A - MEROPS DB, 13,847 chuỗi), so sánh với [**Bidirectional Greedy**](./giai_thich_khai_niem.md#bidirectional-greedy), **CD-HIT**, **MMseqs2**, và chuẩn chuyên gia (**Ad hoc + Manual curation**):

### 3.1. Ý nghĩa các chỉ số và khía cạnh đánh giá (Evaluation Metrics kèm Ví Dụ & Tính Toán Chi Tiết)

> 📖 **CẨM NANG TOÀN DIỆN VỀ CÁC CHỈ SỐ ĐÁNH GIÁ (EVALUATION METRICS COMPENDIUM)**:
> Toàn bộ công thức toán học KaTeX, ý nghĩa sinh học, ví dụ tính toán số thực tế từng bước trên 3 bộ dữ liệu (TE, CE, A1A), phân tích bản chất và ma trận đối đầu 1-1 đã được tách và tổng hợp đầy đủ trong tài liệu chuyên đề độc lập:
> 👉 [**`tong_hop_cac_chi_so_danh_gia.md` (Tổng Hợp Toàn Diện Các Chỉ Số Đánh Giá)**](./tong_hop_cac_chi_so_danh_gia.md).

Bài báo nền thiết kế khung đánh giá gồm 5 khía cạnh/chỉ số thực nghiệm cụ thể:

---

#### 1. Độ nhạy (Sensitivity / Completeness) *(Hình 6 trong bài báo)*
* **Ý nghĩa sinh học**: Đo lường **Độ bao phủ trọn vẹn** — tỷ lệ phần trăm các chuỗi protein trong họ (*Ground set*) được tìm thấy lại khi dùng tập đại diện làm Query chạy thuật toán BLAST:
  $$\text{Sensitivity} = \frac{\text{Số chuỗi trong họ được BLAST tìm thấy}}{\text{Tổng số chuỗi thực tế của họ (Ground Set)}} \times 100\%$$

* **Ví dụ thực tế & Tính toán**:
  * Xét họ **TE4** (Thioesterase 4) có Ground set gồm $N = 29$ chuỗi protein đã được xác thực thực nghiệm.
  * Thuật toán Greedy chọn ra tập đại diện $R$ gồm $10$ chuỗi.
  * Khi lấy $10$ chuỗi này làm Query BLAST quét vào tập 29 chuỗi của TE4:
    * BLAST tìm thấy đủ cả $29$ chuỗi $\implies \text{Sensitivity} = \frac{29}{29} \times 100\% = \mathbf{100\%}$.
  * **Đặc biệt (Tốc độ bao phủ của Greedy)**:
    * Ngay ở ngân sách chỉ $k = 2$ chuỗi đại diện đầu tiên, BLAST đã tìm được $23/29$ chuỗi $\implies \text{Sensitivity} = \frac{23}{29} \approx \mathbf{79.3\%} \approx 80\%$.
    * Điều này chứng minh Greedy tối ưu hóa độ bao phủ cực nhanh ngay từ những bước đầu tiên.

---

#### 2. Độ đặc hiệu & Tỷ lệ sai số chéo họ (Specificity & Error Rate) *(Hình 7 trong bài báo)*
* **Ý nghĩa sinh học**: Đo lường **Độ tinh sạch** — khả năng nhận diện chính xác protein thuộc họ của mình mà **KHÔNG bị bắt nhầm** sang các protein thuộc 34 họ TE khác trong cơ sở dữ liệu:
  $$\text{Error Rate} = \frac{\text{Số chuỗi thuộc họ khác bị nhận diện nhầm}}{\text{Tổng số chuỗi của tất cả các họ khác trong DB}}$$
  $$\text{Specificity} = 1 - \text{Error Rate} = 1 - \frac{\text{Số chuỗi thuộc họ khác bị bắt nhầm}}{N_{\text{các họ khác}}}$$

* **Ví dụ thực tế & Tính toán**:
  * Trong ThYme DB có tổng cộng $737$ chuỗi thuộc 35 họ TE. Khi xét họ **TE1** (gồm $6$ chuỗi), thì tổng số chuỗi thuộc 34 họ TE còn lại là $N_{\text{khác}} = 737 - 6 = 731$ chuỗi.
  * Greedy chọn ra $k = 1$ chuỗi đại diện duy nhất cho TE1 là `P32316`.
  * Dùng `P32316` làm Query BLAST quét qua toàn bộ $731$ chuỗi của 34 họ TE khác:
    * Kết quả BLAST chỉ phát hiện nhầm đúng $1$ chuỗi thuộc họ TE khác có độ tương đồng vượt ngưỡng (False Positive = 1).
    * $\text{Error Rate} = \frac{1}{731} \approx 0.00137 = \mathbf{0.137\%}$.
    * $\text{Specificity} = 1 - 0.00137 = \mathbf{0.99863} \approx \mathbf{99.86\%} \approx \mathbf{1.0}$.
  * *(Trung bình trên toàn bộ 27 họ TE, sai số bắt nhầm của Greedy chỉ tối đa khoảng 0.02%, đảm bảo tính tinh sạch tuyệt đối)*.

---

#### 3. Kích thước tập đại diện & Khả năng giảm dư thừa (Representative Set Size / Redundancy) *(Bảng 1 trong bài báo)*
* **Ý nghĩa sinh học**: Đo lường **Tính tối giản** — số lượng chuỗi đại diện $|R|$ nhỏ nhất cần chọn để đạt $100\%$ độ bao phủ (tập càng ít chuỗi $\implies$ độ dư thừa càng thấp, tiết kiệm chi phí lưu trữ/tính toán).

* **Ví dụ thực tế & Tính toán đối đầu trên Siêu họ Carboxylesterase (CE)**:
  * Siêu họ **CE** có quy mô khổng lồ gồm $N = 12,277$ chuỗi protein.
  * So sánh số lượng chuỗi đại diện $|R|$ mà các phương pháp cần trích xuất để đạt $100\%$ độ bao phủ:
    * **Greedy (Submodular)**: Chỉ cần **$< 10$ chuỗi** đại diện đã đạt $100\%$ coverage $\implies$ Tỷ lệ nén dữ liệu đạt **$\approx 99.92\%$** (cực kỳ tinh gọn).
    * **MMseqs2**: Phân thành **$2,323$ cụm** $\implies$ cần $2,323$ chuỗi đại diện.
    * **CD-HIT**: Phân thành **$10,564$ cụm** $\implies$ giữ lại tới $10,564$ chuỗi (dư thừa tới $86\%$ dữ liệu, không có ý nghĩa chọn lọc đại diện).

---

#### 4. Độ tương đồng với Tập chuẩn của Chuyên gia (Sequence Identity with Benchmark) *(Hình 5 trong bài báo)*
* **Ý nghĩa sinh học**: Đo lường **Độ tin cậy sinh học** — so sánh mức độ trùng khớp giữa các chuỗi do thuật toán chọn tự động ($R_{\text{algo}}$) với tập đại diện "chuẩn vàng" do các chuyên gia sinh học hàng đầu chọn thủ công trong ThYme DB ($R_{\text{benchmark}}$):
  $$\text{Identity}(r) = \max_{b \in R_{\text{benchmark}}} \text{BLAST\_Identity}(r, b)$$

* **Ví dụ thực tế & Tính toán**:
  * **Tại họ TE1**: 
    * Chuyên gia ThYme chọn thủ công chuỗi: `P32316`.
    * Thuật toán Greedy tự động chọn đúng chuỗi: `P32316`.
    * $\implies \text{Độ khớp tuyệt đối} = \mathbf{100\%}$.
  * **Tại họ phức tạp TE16** ($79$ chuỗi):
    * Chuyên gia chọn 4 chuỗi: `{P12276, Q45563, Q03149, A5YV76}`.
    * Greedy tự động chọn 4 chuỗi: `{A0A0S2E7W7, B3FWS8, Q0UI00, P0DUV3}`.
    * Khi so sánh chéo từng cặp chuỗi qua BLAST: Các chuỗi của Greedy khớp với các chuỗi của chuyên gia với tỷ lệ amino acid đồng nhất đạt **$> 80\% - 95\%$**, chứng minh thuật toán tìm ra các tâm cụm tương đương chuyên gia sinh học mà không cần tốn hàng tháng trời giám định thủ công.

---

#### 5. Độ bao phủ theo ngân sách trên Siêu họ lớn (Coverage vs. Budget $k$) *(Hình 8 trong bài báo)*
* **Ý nghĩa sinh học**: Đánh giá **Hiệu quả biên theo từng đồng ngân sách $k$** — biểu diễn đường cong tích lũy độ bao phủ khi ta tăng dần số lượng chuỗi đại diện $k$ từ $1, 2, \dots, 11$.

* **Ví dụ thực tế & Tính toán trên Siêu họ Peptidase A1 (A1A - 13,847 chuỗi)**:
  * Khi thay đổi ngân sách $k$, độ bao phủ của Greedy tăng trưởng vượt bậc theo quy luật lợi ích biên giảm dần (*Diminishing Returns*):
    * Đồ thị Hình 8 Panel A (trang 12) khảo sát thực tế trên đúng 11 mốc ngân sách ($k = 1, 2, \dots, 11$). Đo tọa độ tâm điểm trực tiếp trên đồ thị Hình 8A (tỉ lệ trục tung $31.10\text{ px} = 1.0\%$, làm tròn 1 chữ số thập phân, lưu tại [`RareProtSelect/outputs/tables/nguyen2025_fig8a_benchmark.csv`](./RareProtSelect/outputs/tables/nguyen2025_fig8a_benchmark.csv)) cho thấy:
      - Tại $k = 1, 2, 3, 4$: Pruned Greedy 90% (1,000-Shuffle) đạt lần lượt **$\sim 80.5\%$**, **$\sim 83.5\%$**, **$\sim 85.7\%$**, **$\sim 86.7\%$** (trong khi Bidirectional Greedy xuất phát tại $k=1$ từ **$\sim 71.0\%$**).
      - Tại $k = 5, 6, 7, 8$: Độ bao phủ đạt lần lượt **$\sim 88.0\%$**, **$\sim 88.1\%$**, **$\sim 88.4\%$**, **$\sim 89.0\%$**.
      - Tại $k = 9, 10, 11$: Độ bao phủ vượt ngưỡng $90\%$ ngay từ $k = 9$ (**$\sim 90.7\%$**, khớp với khẳng định *"achieve over 90% coverage with less than 10 representative sequences"* tại trang 11), tiếp tục đạt **$\sim 90.8\%$** tại $k = 10$ và **$\sim 90.9\%$** tại $k = 11$.
  * **Kết luận**: Người dùng có thể linh hoạt chọn $k=10$ hoặc $k=11$ nếu muốn tiết kiệm tài nguyên tối đa (giữ được $>90\%$ thông tin), thay vì bị động nhận về $8,774$ chuỗi cứng nhắc như CD-HIT.

---

### 3.2. Bảng Tổng hợp Hiệu năng Toàn diện & Các phát hiện thực nghiệm cốt lõi

| Phương pháp | Kích thước tập TE (Giảm dư thừa) | Sensitivity (Độ nhạy TE) | Specificity (Độ đặc hiệu) | % Identity với Chuẩn chuyên gia | Hiệu năng trên Siêu họ lớn (CE & A1A) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Greedy (Paper nền)** | **Rất nhỏ (Tối ưu nhất)** | **100% (Đạt 80% chỉ với $k=2$)** | **~ 1.0 (Sai số bắt nhầm ~0.02%)** | **Cao nhất (>80% ở đa số họ)** | **Chỉ cần $<10$ chuỗi đạt 100% CE; 11 chuỗi đạt >90% A1A** |
| **Bidirectional Greedy** | Trung bình – Lớn | 100% (Chậm hơn, cần $k=4$) | ~ 1.0 | Khá | Đạt độ phủ cao nhưng kích thước tập lớn hơn Greedy |
| **CD-HIT** | Rất lớn (Dư thừa ở 19 họ) | Biến động theo ngưỡng | Phụ thuộc ngưỡng | Biến động mạnh (<50% ở nhiều họ) | 10,564 chuỗi (CE) và 8,774 chuỗi (A1A) (Dư thừa nghiêm trọng) |
| **MMseqs2** | Lớn (Dư thừa ở đa số họ) | Biến động theo ngưỡng | Phụ thuộc ngưỡng | Biến động mạnh | 2,323 chuỗi (CE) và 1,701 chuỗi (A1A) (Dư thừa lớn) |
| **Ad hoc (Chuyên gia ThYme)** | Chuẩn tham chiếu (Gold Standard) | 100% | 1.0 | 100% (Chính là tập chuẩn) | Không khả thi (quá tốn nhân lực để làm thủ công) |

#### Các phát hiện thực nghiệm cốt lõi:

1. **Giảm thiểu tối đa tính dư thừa (Tập đại diện nhỏ gọn nhất)**:
   * Trên 27 họ TE: Greedy cho kích thước tương đồng với chuyên gia ở 12 họ, nhỏ gọn hơn ở 6 họ, và lớn hơn ở 9 họ.
   * Vượt trội so với CD-HIT và MMseqs2 vốn luôn tạo ra tập đại diện quá lớn do cơ chế phân cụm tĩnh.
2. **Độ nhạy và Tốc độ bao phủ tuyệt đối (Sensitivity = 100%)**:
   * Khi dùng tập đại diện làm Query để BLAST tìm lại dữ liệu trong họ, Greedy đạt **Sensitivity = 100%** trên toàn bộ các họ TE.
   * **Tốc độ bao phủ vượt bậc**: Greedy đạt trung bình **80% Sensitivity chỉ với $k = 2$ chuỗi**, trong khi Bidirectional Greedy cần trung bình $k = 4$ chuỗi.
3. **Độ đặc hiệu và Độ tinh sạch cao (Specificity $\approx 1.0$)**:
   * Greedy đạt Specificity xấp xỉ 1.0 trên tất cả các họ. Tỷ lệ nhận diện nhầm chuỗi thuộc họ khác (*False Positive*) tối đa chỉ khoảng **0.02%**.
4. **Hiệu quả vượt bậc trên các siêu họ protein (CE và A1A)**:
   * **Họ CE (12,277 chuỗi)**: Greedy đạt **100% coverage với chỉ dưới 10 chuỗi**. Trong khi đó, CD-HIT sinh ra **10,564 chuỗi**, MMseqs2 sinh ra **2,323 chuỗi**.
   * **Họ A1A (13,847 chuỗi)**: Greedy đạt **> 90% coverage với 10-11 chuỗi**. Ngược lại, CD-HIT sinh ra **8,774 chuỗi** và MMseqs2 sinh ra **1,701 chuỗi**.

---

## 4. HỆ THỐNG 5 CÂU HỎI NGHIÊN CỨU (RQ1 $\to$ RQ5) & KHUNG CHỈ SỐ ĐÁNH GIÁ ĐỐI ĐẦU

> 💡 **TRA CỨU TOÀN BỘ CÔNG THỨC & VÍ DỤ TÍNH TOÁN**:
> Bảng tổng hợp công thức, phân loại 3 nhóm thước đo và số liệu đối đầu thực nghiệm 1-1 chi tiết được trình bày tập trung tại [**`tong_hop_cac_chi_so_danh_gia.md`**](./tong_hop_cac_chi_so_danh_gia.md), và kết quả trả lời chi tiết cho từng câu hỏi nghiên cứu nằm tại [**`bao_cao_ket_qua_chi_tiet_topic2.md`**](./bao_cao_ket_qua_chi_tiet_topic2.md).

---

<a id="he-thong-5-rq"></a>
### 4.1. Hệ thống 5 Câu hỏi Nghiên cứu Trọng tâm (Từ Nhánh 1, Nhánh 2 đến Cụm Liên hoàn Nhánh 3 – 4 – 5)

Dựa trên đề cương gốc ([`topic2.md` Mục 3.2](./topic2.md)) và nguyên tắc **Thực nghiệm Cô lập Biến số (*Ceteris Paribus*)**, đề tài thiết lập **5 Câu hỏi Nghiên cứu (`RQ1` $\to$ `RQ5`)** chia làm 2 cụm logic:

#### Cụm I — Khởi đầu & Khảo sát Cơ sở (Giải quyết tuần tự tại Nhánh 1 và Nhánh 2)
* **RQ1 (Trả lời tại Nhánh 1 — Tái lập Đường cơ sở Bài báo nền & Kiểm định Điểm mù Nhóm hiếm):**
  *Phương pháp tối ưu hóa submodular không trọng số (`Unweighted Facility Location`, $\alpha = 0.0$) trên tương đồng trình tự `BLASTp` của bài báo nền tái lập độ nhạy toàn cục (`Overall Sensitivity`) theo ngân sách $k$ như thế nào, và bộc lộ những điểm mù gì khi hoàn toàn thiếu các chỉ số đánh giá phân họ hiếm?*
* **RQ2 (Khảo sát bước đầu tại Nhánh 2 — Đề xuất Hàm trọng số & Bộ chỉ số Nội phân họ trên `BLASTp`):**
  *Khi đề xuất bộ chỉ số nhóm hiếm dưới cơ chế **Truy vấn Ngược Nội Phân Họ ($S_k \cap V_g \to V_g$)** và hàm mục tiêu có trọng số $w_v^{(\alpha)} = (n_{g(v)})^{-\alpha}$ ($\alpha \in \{0.0, 0.5, 1.0\}$) khảo sát bước đầu trên `BLASTp`, độ nhạy nhóm hiếm cải thiện ra sao mà không làm suy giảm đáng kể `Overall Sensitivity`? (Và tại sao kết quả trên `BLASTp` mới chỉ là bước đệm, chưa đủ cơ sở kết luận toàn diện do `BLASTp` chưa biểu diễn được tương đồng ngữ nghĩa – cấu trúc sâu?)*

#### Cụm II — Trọng tâm Liên hoàn: Kết hợp Cả 3 Nhánh (Nhánh 3 + Nhánh 4 + Nhánh 5) để Trả lời 3 Câu hỏi Chung
*(Từng nhánh riêng lẻ không thể tự trả lời trọn vẹn, mà phải kết hợp cả 3 nhánh: **Nhánh 3** đưa bài toán sang không gian ngữ nghĩa `ESM-2`; **Nhánh 4** tái kiểm định chéo $2 \times 2$ để đưa ra cái nhìn đầy đủ và tổng quan nhất về kết quả chung; **Nhánh 5** phân tích sâu kết quả trực tiếp của các nhóm hiếm và độ dư thừa trong tập đại diện $S_k$ nhằm chỉ ra phương pháp nào có tập đại diện thực sự tốt hơn)*:
* **RQ3 (Kết hợp Nhánh 3, 4, 5 — Hiệu quả của Không gian Biểu diễn `ESM-2` vs. `BLASTp`):**
  *Sử dụng không gian nhúng ngữ nghĩa `ESM-2` có tạo ra được tập đại diện $S_k$ tốt hơn `BLASTp` hay không?*
* **RQ4 (Kết hợp Nhánh 3, 4, 5 — Kiểm định Giá trị Thực sự của Hàm Mục tiêu Có Trọng số $w_v^{(\alpha)}$):**
  *Vượt qua hạn chế biểu diễn cục bộ của `BLASTp` ở Nhánh 2, hàm mục tiêu có trọng số ưu tiên nhóm hiếm thực sự có tốt hơn hàm không trọng số trên mọi không gian biểu diễn, hệ quy chiếu đánh giá và cấu trúc tập đại diện $S_k$ hay không?*
* **RQ5 (Kết hợp Nhánh 3, 4, 5 — Sự Đột phá của Tổ hợp `ESM-2 + Hàm Trọng số` vs. Sử dụng Riêng lẻ):**
  *Khi sử dụng `ESM-2` cộng với `Hàm trọng số` ($\alpha \in \{0.5, 1.0\}$) thì kết quả tạo ra sự đột phá như thế nào cho nhóm hiếm, và nếu chỉ sử dụng riêng lẻ từng thành phần (chỉ dùng `ESM-2` không trọng số hoặc chỉ dùng `Hàm trọng số` trên `BLASTp`) thì có đạt được kết quả tương tự hay không?*

> 📌 **Lý giải Phương pháp luận: Tại sao chuyển hóa bài toán `Annotation Transfer` (trong đề cương sơ bộ `topic2.md`) thành `Truy vấn Ngược Nội Phân Họ ($S_k \cap V_g \to V_g$)` và `Tỷ lệ Đại diện Trực tiếp Phân họ ($S_k \cap V_g \ne \emptyset$)`?**
> 1. **Nhiễu chưa định danh `[A01.UPA]` và 18 phân họ đơn độc (*singleton*, $n_g = 1$)**: Tập dữ liệu chuẩn hóa Phương án 3B ($4,120$ chuỗi sau khi lọc $9,187$ chuỗi `[A01.UPA]`) gồm $115$ phân họ và $45$ phân họ hiếm ($n_g \le 5$), trong đó có **$18$ phân họ hiếm chỉ chứa đúng $1$ chuỗi duy nhất ($n_g = 1$)**. Nếu chia tập kiểm tra $V \setminus S_k$ để tính `1-NN Annotation Transfer F1`: khi chuỗi duy nhất đó được chọn vào $S_k$ thì tập kiểm tra rỗng ($V_g \setminus S_k = \emptyset$); ngược lại nếu không được chọn thì thư viện $S_k$ mất hoàn toàn nhãn phân họ đó ($\text{F1} = 0\%$).
> 2. **Khử "Ảo giác Bắn tràn Liên phân họ"**: Phép truy vấn toàn cục không phân biệt phân họ (Nhánh 1) cho phép đại diện của họ lớn bắn tràn (*cross-hit*) sang họ hiếm ở ngưỡng $E \le 10^{-7}$, gây ảo giác bao phủ dù họ hiếm không hề có mặt trong $S_k$. Do đó, việc kết hợp **Truy vấn Ngược Nội Phân Họ ($S_k \cap V_g \to V_g$, Nhánh 2–4)** và **Đếm Trực tiếp Tỷ lệ Đại diện Phân họ & Độ dư thừa Ngân sách (Nhánh 5)** là thước đo chính xác và trực diện nhất.

---

### 4.2. Phân loại chi tiết các Chỉ số Đánh giá (Metrics)

#### PHẦN A: Các chỉ số ĐÃ CÓ ở Bài báo nền (Phương pháp mới cần DUY TRÌ TƯƠNG ĐƯƠNG)
Đây là các chỉ số mà bài báo nền (*Nguyen et al., 2025*) đã sử dụng để đánh giá trên toàn thể họ protein (coi họ protein như một khối phẳng đồng nhất):

1. **Overall Sensitivity / Completeness (Độ nhạy toàn thể qua BLAST)**:
   * *Bản chất*: Tỷ lệ phần trăm chuỗi trong toàn bộ Ground Set $V$ được tìm thấy lại khi dùng tập đại diện $S$ làm Query BLAST.
   * *Vai trò kiểm chứng*: Đối chuẩn tái lập ở Nhánh 1 và theo dõi mức độ bảo toàn độ bao phủ tổng thể khi bật trọng số ưu tiên nhóm hiếm ($\alpha \in \{0.5, 1.0\}$) ở Nhánh 2, 3, 4.
2. **Overall Specificity / Error Rate (Độ đặc hiệu & Tỷ lệ sai số chéo họ)**:
   * *Bản chất*: Khả năng nhận diện chính xác protein trong họ mà không bị bắt nhầm sang các họ khác trong cơ sở dữ liệu (đã được bài báo nền chứng minh trên 27 họ TE).
3. **Kích thước tập đại diện & Đường cong ngân sách (Set Size & Coverage vs. Budget $k$ Curve)**:
   * *Bản chất*: Tốc độ tích lũy độ bao phủ khi tăng dần ngân sách $k$ (từ $k \in [1..11]$ trong bài báo nền mở rộng lên 20 mốc $k \in [1..115]$ tiến tới tổng số phân họ $G = 115$).
4. **Độ tương đồng với Chuẩn chuyên gia (Sequence Identity with Benchmark)**:
   * *Bản chất*: Mức độ tương đồng về chuỗi giữa tập thuật toán chọn và tập do chuyên gia sinh học giám định thủ công trong ThYme DB.

---

<a id="phan-b-cac-chi-so-danh-gia-moi"></a>
#### PHẦN B: Các chỉ số ĐÁNH GIÁ MỚI BỔ SUNG (Bài báo nền HOÀN TOÀN CHƯA CÓ — Trả lời RQ2 $\to$ RQ5)
*(Tra cứu công thức toán học và ví dụ tính tay từng bước tại [**`tong_hop_cac_chi_so_danh_gia.md`**](./tong_hop_cac_chi_so_danh_gia.md))*:

1. **Rare Subfamily Sensitivity / Coverage (Độ nhạy / Độ bao phủ nội phân họ trung bình trên các phân họ hiếm $n_g \le 5$)**:
   * *Công thức*: $\operatorname{Rare\_Cov}(S_k) = \frac{1}{|G_{\text{rare}}|} \sum_{g \in G_{\text{rare}}} \operatorname{Cov}_g^{\text{within}}(S_k)$ (với $|G_{\text{rare}}| = 45$ phân họ hiếm trên `MEROPS_A1A_curated`).
   * *Bản chất & Vai trò*: Đo lường trực tiếp khả năng thu hồi nội phân họ dành riêng cho nhóm các phân họ hiếm ($\le 5$ chuỗi) dưới cả hai hệ quy chiếu `Live BLASTp Sensitivity (%)` (Nhánh 2, 4) và `Coverage ESM (%)` (Nhánh 3, 4).
2. **Macro Sensitivity / Coverage (Độ nhạy / Độ bao phủ nội phân họ trung bình bình đẳng trên toàn bộ $G = 115$ phân họ)**:
   * *Công thức*: $\operatorname{Macro\_Cov}(S_k) = \frac{1}{G} \sum_{g=1}^{G} \operatorname{Cov}_g^{\text{within}}(S_k)$.
   * *Bản chất & Vai trò*: Đo lường **mặt bằng chung phân bố qua các phân họ** bằng cách cấp quyền biểu quyết bình đẳng $1/G$ cho mỗi phân họ, bất kể phân họ đó có $329$ chuỗi hay chỉ có $1$ chuỗi.
3. **Worst-Group Sensitivity / Coverage & Zero-Coverage Subfamilies Count (Độ bao phủ nhóm thiệt thòi nhất & Số phân họ bị bỏ rơi $0\%$)**:
   * *Công thức*: $\operatorname{Worst\_Cov}(S_k) = \min_{g \in \{1..G\}} \operatorname{Cov}_g^{\text{within}}(S_k)$ và $\operatorname{Zero\_Count}(S_k) = |\{g \in \{1..G\} \mid \operatorname{Sens}_g^{\text{within}}(S_k) = 0.0\%\}|$.
   * *Bản chất & Vai trò*: Kiểm tra chốt chặn công bằng cực tiểu và đếm chính xác số lượng phân họ bị bỏ trống hoàn toàn tại mỗi mức ngân sách $k$.
4. **Subfamily & Rare Group Representation Rate (Tỷ lệ phân họ trên $115$ họ và họ hiếm trên $45$ họ có đại diện trực tiếp trong $S_k$ — Nhánh 5)**:
   * *Công thức*: $\operatorname{Subfamily\_Repr}(S_k) = \frac{|\mathcal{G}(S_k)|}{115} \times 100\%$ và $\operatorname{Rare\_Repr}(S_k) = \frac{|\mathcal{G}_{\text{rare}}(S_k)|}{45} \times 100\%$.
   * *Bản chất & Vai trò*: Đếm trực tiếp số phân họ có ít nhất 1 chuỗi đại diện góp mặt trong thư viện $S_k$ ($S_k \cap V_g \ne \emptyset$).
5. **Subfamily Allocation Redundancy & Dominant Group Share (Độ dư thừa phân bổ phân họ & Tỷ trọng độc chiếm của họ lớn nhất `A01.009` — Nhánh 5)**:
   * *Công thức*: $\operatorname{Subfamily\_Redundancy}(S_k) = \frac{k - |\mathcal{G}(S_k)|}{k} \times 100\%$ và $\operatorname{Dominant\_Share}(S_k) = \frac{|S_k \cap V_{\text{A01.009}}|}{k} \times 100\%$.
   * *Bản chất & Vai trò*: Định lượng tỷ lệ ngân sách bị tiêu tốn vào việc chọn lặp lại nhiều đại diện trong cùng một phân họ lớn để trả lời trực diện câu hỏi **RQ5**.

---

### 4.3. Bảng Tổng hợp Đối đầu các Chỉ số: Bài báo nền vs. RareProtSelect

| Nhóm chỉ số | Tên chỉ số cụ thể | Trạng thái ở Bài báo nền | Vai trò Kiểm chứng trong Chuỗi Thực nghiệm Nhánh 1 $\to$ Nhánh 5 |
| :--- | :--- | :---: | :--- |
| **1. Nhóm Chỉ số BẢO TỒN NHÓM HIẾM (Trả lời RQ2, RQ3, RQ4)** | **`rare_sensitivity_blast_pct` & `rare_coverage_esm_pct`** | ❌ Chưa có | Đo độ thu hồi và bao phủ nội phân họ trung bình trên $45$ phân họ hiếm ($n_g \le 5$) |
| | **`worst_group_sensitivity_blast_pct` & `worst_group_coverage_esm_pct`** | ❌ Chưa có | Đo cận dưới bao phủ của phân họ thiệt thòi nhất trong $115$ phân họ |
| | **`zero_cov_subfamilies_count`** | ❌ Chưa có | Đếm số phân họ bị bỏ rơi hoàn toàn ($\operatorname{Sens}_g^{\text{within}} = 0.0\%$) |
| **2. Nhóm Chỉ số ĐO MẶT BẰNG CHUNG & TOÀN CỤC (Trả lời RQ1, RQ2, RQ3, RQ4)** | **`macro_sensitivity_blast_pct` & `macro_coverage_esm_pct`** | ❌ Chưa có | Đo mặt bằng chung bình đẳng ($1/115$) qua toàn bộ các phân họ |
| | **`overall_sensitivity_blast_pct` & `overall_coverage_esm_pct`** | ✅ Đã có *(bản BLAST toàn cục)* | Đối chuẩn Hình 8A (Nhánh 1) và kiểm tra mức độ đánh đổi toàn cục khi ưu tiên nhóm hiếm (Nhánh 2, 3, 4) |
| **3. Nhóm Chỉ số CẤU TRÚC ĐẠI DIỆN & ĐỘ DƯ THỪA NGÂN SÁCH (Trả lời RQ5)** | **`subfamily_repr_rate_pct` & `rare_repr_rate_pct`** | ❌ Chưa có | Đo tỷ lệ `%` phân họ ($/115$) và họ hiếm ($/45$) có đại diện trực tiếp trong $S_k$ |
| | **`subfamily_redundancy_pct` & `dominant_a01_009_share_pct`** | ❌ Chưa có | Đo tỷ lệ `%` ghế ngân sách bị chọn trùng phân họ và mức độ lấn át của họ lớn nhất `A01.009` |

---

### 4.4. Thiết kế Chuỗi Thực nghiệm Cô lập Biến số (*Ceteris Paribus* — Nhánh 1 $\to$ Nhánh 5)

Quy trình thực nghiệm được thiết kế chặt chẽ thành 5 nhánh nhằm giải quyết trọn vẹn 2 cụm câu hỏi nghiên cứu:

1. **Nhánh 1 (Trả lời `RQ1` — Đối chuẩn Bài báo nền & Phát hiện Điểm mù Nhóm hiếm)**:
   * Chạy **Unweighted Facility Location ($\alpha = 0.0$)** trên $\mathbf{S}_{\text{BLAST}}$ với $13,307$ chuỗi tại $k \in [1..11]$ để tái lập Hình 8 Panel A (*Nguyen et al., 2025*) và chỉ ra việc thiếu hoàn toàn các thước đo nhóm hiếm.
2. **Nhánh 2 (Trả lời `RQ2` — Khảo sát Bước đầu Hàm trọng số & Bộ chỉ số Nội phân họ trên `BLASTp`)**:
   * Đề xuất bộ chỉ số nhóm hiếm dưới cơ chế **Truy vấn Ngược Nội Phân Họ ($S_k \cap V_g \to V_g$)** trên tập chuẩn hóa Phương án 3B ($4,120$ chuỗi, $115$ họ, $45$ họ hiếm) và khảo sát hàm trọng số $w_v^{(\alpha)} = n_g^{-\alpha}$ ($\alpha \in \{0.0, 0.5, 1.0\}$) trên $\mathbf{S}_{\text{BLAST}}$. Do `BLASTp` chỉ đo tương đồng chuỗi cục bộ bề mặt nên Nhánh 2 mới dừng ở khảo sát bước đầu, chưa đủ cơ sở để kết luận toàn diện.
3. **Cụm Liên hoàn Nhánh 3 + Nhánh 4 + Nhánh 5 (Cùng kết hợp để trả lời dứt điểm `RQ3`, `RQ4`, `RQ5`)**:
   * **Nhánh 3 (Đưa vào Không gian Ngữ nghĩa `ESM-2`)**: Thay $\mathbf{S}_{\text{BLAST}}$ bằng $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$ và khảo sát $\alpha \in \{0.0, 0.5, 1.0\}$ trên thước đo nội tại `Within-Subfamily Coverage ESM (%)`.
   * **Nhánh 4 (Tái kiểm định chéo $2 \times 2$ — Bức tranh Tổng quan Toàn diện)**: Đánh giá chéo cả 6 tập đại diện (`BLASTp-Selected` và `ESM2-Selected`) đồng thời trên cả 2 mặt trận (`Live BLASTp Sensitivity %` & `Coverage ESM %`) để có cái nhìn đầy đủ và khách quan nhất về kết quả chung.
   * **Nhánh 5 (Phân tích sâu Nhóm hiếm & Độ dư thừa trực tiếp trong Tập $S_k$)**: Đi sâu kiểm đếm trực tiếp số phân họ (`/115`), số phân họ hiếm (`/45`) có đại diện trong $S_k$ và độ dư thừa ngân sách (`Redundancy`), từ đó kết hợp với Nhánh 3 và Nhánh 4 để trả lời trực diện 3 câu hỏi chung: **(1) `RQ3`: `ESM-2` có tạo tập $S_k$ tốt hơn `BLASTp` không?** **(2) `RQ4`: Hàm trọng số thực sự tốt hơn không?** **(3) `RQ5`: Tổ hợp `ESM-2 + Hàm trọng số` đột phá như thế nào so với dùng riêng lẻ?**

---

## 5. MÔ HÌNH TOÁN HỌC CỦA PHƯƠNG PHÁP ĐỀ XUẤT (RAREPROTSELECT)

Mô hình cốt lõi **RareProtSelect** định nghĩa bài toán chọn tập protein đại diện ưu tiên nhóm hiếm qua 5 thành phần toán học:

### 5.1. Không gian Dữ liệu & Biểu diễn (Data & Representation)
* **Tập protein đầu vào**: $V = \{v_1, v_2, \dots, v_n\}$.
* **Cấu trúc phân nhóm**: Mỗi protein $v$ thuộc một phân họ/nhóm phân loại $g(v)$ có quy mô là $n_{g(v)}$ chuỗi.
* **Vector đặc trưng**: Mỗi protein $v$ được biểu diễn bằng vector nhúng ngữ nghĩa $z(v) \in \mathbb{R}^d$ sinh bởi mô hình ngôn ngữ protein **ESM-2**.

### 5.2. Độ tương đồng Ngữ nghĩa (Semantic Similarity)
Độ tương đồng giữa 2 protein $u$ và $v$ được tính bằng khoảng cách Cosine không âm trong không gian vector:
$$\operatorname{sim}_{PLM}(u, v) = \max\{0, \cos(z(u), z(v))\} = \max\left\{0, \frac{z(u) \cdot z(v)}{\|z(u)\| \|z(v)\|}\right\}$$

### 5.3. Trọng số Thích ứng Nhóm Hiếm (Rare-Aware Weighting)
Gán trọng số $w_v$ cho từng protein $v$ nghịch đảo theo căn bậc hai quy mô nhóm $n_{g(v)}$ của nó:
$$w_v = \frac{1}{\sqrt{n_{g(v)}}}$$
*(Nhóm càng hiếm thì trọng số mỗi cá thể càng cao, giúp khuếch đại tiếng nói của nhóm hiếm trước nhóm lớn).*

### 5.4. Hàm Mục tiêu Weighted Facility Location (WFL)
Với tập đại diện $S \subseteq V$, tổng độ bao phủ có trọng số của toàn bộ họ protein được đo bằng:
$$F(S) = \sum_{v \in V} w_v \max_{s \in S} \operatorname{sim}_{PLM}(v, s)$$

### 5.5. Bài toán Tối ưu hóa & Thuật toán Giải (Optimization & Algorithm)
* **Bài toán tối ưu**: Tìm tập đại diện $S \subseteq V$ không vượt quá ngân sách $k$ chuỗi ($|S| \le k$) sao cho $F(S)$ đạt cực đại:
  $$\max_{S \subseteq V, |S| \le k} F(S)$$

* **Hai thuật toán giải (cùng đạt bảo đảm lý thuyết $\ge 1 - 1/e \approx 63.2\%$):**
  1. [**Standard Greedy (Greedy thuần)**](./giai_thich_khai_niem.md#standard-greedy): Dùng làm thuật toán chuẩn để đối chiếu và so sánh kết quả trực diện, công bằng nhất với bài báo nền (Nguyen et al., 2025).
  2. [**Lazy Greedy (Biến thể tăng tốc)**](./giai_thich_khai_niem.md#lazy-greedy): Sử dụng Hàng đợi ưu tiên (Max-Heap) để tăng tốc thực thi trên dữ liệu lớn, cho ra kết quả nghiệm chính xác 100% giống hệt Standard Greedy.



