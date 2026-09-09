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
| **Không gian biểu diễn** | Chuỗi ký tự thô ([**FASTA**](./giai_thich_khai_niem.md#fasta)) | Vector nhúng ngữ nghĩa $z(v) \in \mathbb{R}^d$ sinh bởi [**ESM-2 PLM**](./giai_thich_khai_niem.md#esm2-plm) |
| **Hàm tương đồng $\operatorname{sim}(u, v)$** | Tỷ lệ amino acid khớp nhau qua BLAST (% Identity) | Cosine similarity: $\max\{0, \cos(z(u), z(v))\}$ |
| **Cơ chế trọng số** | **Unweighted**: Mọi chuỗi có trọng số bằng nhau ($w = 1/\|V\|$) | **Rare-Aware**: Ưu tiên nhóm hiếm $w_v = \frac{1}{\sqrt{n_{g(v)}}}$ |
| **Hàm mục tiêu $F(S)$** | [**Facility Location**](./giai_thich_khai_niem.md#facility-location-unweighted): $F(S) = \frac{1}{\|V\|} \sum_{v \in V} \max_{s \in S} \phi(v, s)$ | [**Weighted Facility Location**](./giai_thich_khai_niem.md#weighted-facility-location): $F(S) = \sum_{v \in V} w_v \max_{s \in S} \operatorname{sim}_{PLM}(v, s)$ |
| **Xử lý mất cân bằng** | Không xử lý; nhóm lớn áp đảo hoàn toàn nhóm nhỏ | Trọng số $w_v$ tăng lực kéo toán học cho nhóm hiếm |
| **Thuật toán tối ưu** | [**Greedy**](./giai_thich_khai_niem.md#standard-greedy) / [**Bidirectional Greedy**](./giai_thich_khai_niem.md#bidirectional-greedy) (Bảo đảm $\ge 1 - 1/e$) | [**Lazy Greedy WFL**](./giai_thich_khai_niem.md#lazy-greedy) (Nghiệm giống 100% Greedy chuẩn, tăng tốc qua Max-Heap) |
| **Nhiệm vụ kiểm chứng** | Đánh giá nội tại: Tái tạo cơ sở dữ liệu qua BLAST query | 1. **Bóc tách (Ablation)**: Chứng minh Hàm mục tiêu mới và Độ đo ESM-2 vượt trội hơn cũ trên cùng thuật toán Greedy.<br>2. **Đánh giá hạ nguồn**: **Annotation Transfer** (Macro-F1 cho nhóm hiếm). |

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
* **Ý nghĩa sinh học**: Đánh giá **Hiệu quả biên theo từng đồng ngân sách $k$** — biểu diễn đường cong tích lũy độ bao phủ khi ta tăng dần số lượng chuỗi đại diện $k$ từ $1, 2, 5, 10, \dots, 600$.

* **Ví dụ thực tế & Tính toán trên Siêu họ Peptidase A1 (A1A - 13,847 chuỗi)**:
  * Khi thay đổi ngân sách $k$, độ bao phủ của Greedy tăng trưởng vượt bậc theo quy luật lợi ích biên giảm dần (*Diminishing Returns*):
    * Tại $k = 1$: Độ bao phủ đạt **$42\%$** (chỉ 1 chuỗi đã đại diện được gần nửa siêu họ).
    * Tại $k = 10$: Độ bao phủ tăng vọt lên **$> 90\%$** ($12,460 / 13,847$ chuỗi được bao phủ).
    * Tại $k = 100$: Độ bao phủ đạt **$97.5\%$**.
    * Tại $k = 600$: Độ bao phủ chạm mốc tuyệt đối **$100\%$**.
  * **Kết luận**: Người dùng có thể linh hoạt chọn $k=10$ nếu muốn tiết kiệm tài nguyên tối đa (giữ được 90% thông tin), hoặc chọn $k=600$ nếu muốn trọn vẹn 100%, thay vì bị động nhận về $8,774$ chuỗi cứng nhắc như CD-HIT.

---

### 3.2. Bảng Tổng hợp Hiệu năng Toàn diện & Các phát hiện thực nghiệm cốt lõi

| Phương pháp | Kích thước tập TE (Giảm dư thừa) | Sensitivity (Độ nhạy TE) | Specificity (Độ đặc hiệu) | % Identity với Chuẩn chuyên gia | Hiệu năng trên Siêu họ lớn (CE & A1A) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Greedy (Paper nền)** | **Rất nhỏ (Tối ưu nhất)** | **100% (Đạt 80% chỉ với $k=2$)** | **~ 1.0 (Sai số bắt nhầm ~0.02%)** | **Cao nhất (>80% ở đa số họ)** | **Chỉ cần $<10$ chuỗi đạt 100% CE; ~600 chuỗi đạt 100% A1A** |
| **Bidirectional Greedy** | Trung bình – Lớn | 100% (Chậm hơn, cần $k=4$) | ~ 1.0 | Khá | Đạt 100% nhưng kích thước tập lớn hơn Greedy |
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
   * **Họ A1A (13,847 chuỗi)**: Greedy đạt **> 90% coverage với dưới 10 chuỗi** và đạt 100% với khoảng 600 chuỗi. Ngược lại, CD-HIT sinh ra **8,774 chuỗi** và MMseqs2 sinh ra **1,701 chuỗi**.

---

## 4. CÁC HẠNG MỤC ĐÁNH GIÁ: PHƯƠNG PHÁP MỚI vs. BÀI BÁO NỀN (VÀ CÁC THỰC NGHIỆM BẮT BUỘC)

Để chứng minh tính đóng góp khoa học và bảo đảm bài báo đạt độ chặt chẽ tuyệt đối, khung đánh giá thực nghiệm được chia thành 3 phần rõ rệt:

### 4.1. Phân loại chi tiết các Chỉ số Đánh giá (Metrics)

#### PHẦN A: Các chỉ số ĐÃ CÓ ở Bài báo nền (Phương pháp mới cần DUY TRÌ TƯƠNG ĐƯƠNG)
Đây là các chỉ số mà bài báo nền (*Nguyen et al., 2025*) đã sử dụng để đánh giá trên toàn thể họ protein (coi họ protein như một khối phẳng đồng nhất):

1. **Overall Sensitivity / Completeness (Độ nhạy toàn thể qua BLAST)**:
   * *Bản chất*: Tỷ lệ phần trăm chuỗi trong toàn bộ Ground Set $V$ được tìm thấy lại khi dùng tập đại diện $S$ làm Query BLAST.
   * *Mục tiêu phương pháp mới*: Duy trì ở mức cao ($\ge 98\% - 100\%$), **không được suy giảm quá $1\% - 2\%$** so với bài báo nền.
2. **Overall Specificity / Error Rate (Độ đặc hiệu & Tỷ lệ sai số chéo họ)**:
   * *Bản chất*: Khả năng nhận diện chính xác protein trong họ mà không bị bắt nhầm sang các họ khác trong cơ sở dữ liệu.
   * *Mục tiêu phương pháp mới*: Duy trì Specificity xấp xỉ $1.0$, tỷ lệ sai số bắt nhầm $\le 0.02\%$.
3. **Kích thước tập đại diện & Tính giảm dư thừa (Set Size / Redundancy)**:
   * *Bản chất*: Số lượng chuỗi cần chọn để đạt độ bao phủ mong muốn ở ngân sách $k$, và mức độ trùng lặp giữa các chuỗi bên trong tập $S$ ($\text{Pairwise Redundancy}$).
   * *Mục tiêu phương pháp mới*: Tập $S$ giữ được tính tinh gọn cao, không chọn các chuỗi "sinh đôi" dư thừa.
4. **Độ tương đồng với Chuẩn chuyên gia (Sequence Identity with Benchmark)**:
   * *Bản chất*: Mức độ tương đồng về chuỗi/cấu trúc giữa tập thuật toán chọn và tập do chuyên gia sinh học giám định thủ công (ví dụ ThYme DB).
   * *Mục tiêu phương pháp mới*: Đạt độ tương đồng cao ($>80\% - 95\%$) ở các họ chuẩn.
5. **Đường cong ngân sách (Coverage vs. Budget $k$ Curve)**:
   * *Bản chất*: Tốc độ tích lũy độ bao phủ khi tăng dần ngân sách $k$ từ $1, 2, 5, \dots, k$.
   * *Mục tiêu phương pháp mới*: Tốc độ bao phủ nhanh ngay từ những giá trị $k$ rất nhỏ ($k=2$ đạt $\approx 80\%$).

---

<a id="phan-b-cac-chi-so-danh-gia-moi"></a>
#### PHẦN B: Các chỉ số ĐÁNH GIÁ MỚI BỔ SUNG (Bài báo nền HOÀN TOÀN CHƯA CÓ)
*(Nhấp vào tên các chỉ số có gạch chân bên dưới để mở [**tệp giai_thich_khai_niem.md**](./giai_thich_khai_niem.md#cac-chi-so-danh-gia-moi) xem công thức chi tiết, [**cách tính Coverage(g)**](./giai_thich_khai_niem.md#coverage-g), [**ví dụ thực tế bằng số từng bước**](./giai_thich_khai_niem.md#vi-du-tinh-toan-chi-tiet) và [**bản chất phân biệt Worst Coverage vs. Representation Rate**](./giai_thich_khai_niem.md#so-sanh-worst-va-representation))*:

1. [**Macro Coverage (Độ bao phủ trung bình đều qua các phân họ)**](./giai_thich_khai_niem.md#macro-coverage):
   * *Công thức*: $\text{Macro Coverage} = \frac{1}{|G|} \sum_{g \in G} \text{Coverage}(g)$ (với $|G|$ là tổng số phân họ/nhóm; xem [cách tính Coverage(g)](./giai_thich_khai_niem.md#coverage-g)).
   * *Bản chất & Vai trò*: Đo lường **mặt bằng chung phân bố qua các phân họ (Balanced Central Tendency)** bằng cách gán trọng số bình đẳng $1/|G|$ cho mỗi phân họ. Chỉ số này phản ánh chất lượng đại diện tổng quan trên toàn bộ phổ phân họ, đồng thời đóng vai trò làm đối trọng kiểm chứng chất lượng toàn diện (giúp phát hiện thuật toán tốt toàn cục, tránh việc chỉ số bị méo mó bởi 1-2 chuỗi rác/outlier như khi chỉ nhìn vào Worst-case).
2. [**Worst-Group Coverage (Độ bao phủ của nhóm hiếm nhất / thiệt thòi nhất — Chỉ số trọng tâm cho nhóm hiếm)**](./giai_thich_khai_niem.md#worst-group-coverage):
   * *Công thức*: $\text{Worst-Group Coverage} = \min_{g \in G} \text{Coverage}(g)$.
   * *Mục tiêu phương pháp mới*: **Vượt trội hoàn toàn so với bài báo nền** (trong khi bài báo nền thường bỏ rơi nhóm hiếm dẫn đến Worst-Group Coverage $= 0\%$, phương pháp mới đảm bảo nhóm hiếm nhất vẫn đạt độ bao phủ cao, xóa bỏ vùng tối dữ liệu).
3. [**Rare Group Representation Rate (Tỷ lệ nhóm hiếm có đại diện trực tiếp)**](./giai_thich_khai_niem.md#rare-group-representation):
   * *Bản chất*: Tỷ lệ phần trăm các phân họ hiếm có ít nhất 1 chuỗi lọt vào tập đại diện $S$ ($S \cap g \neq \emptyset$).
   * *Mục tiêu phương pháp mới*: Đạt tỷ lệ tối đa ($80\% - 100\%$ các nhóm hiếm có đại diện trong top $k$ để giữ mẫu vật thực tế cho phòng lab).
   * 🔍 *Xem thêm*: [So sánh sự khác biệt bản chất và mục tiêu giữa Worst-Group Coverage và Rare Group Representation Rate](./giai_thich_khai_niem.md#so-sanh-worst-va-representation).
4. [**Annotation Transfer Macro-F1 & Worst-Group F1 (Độ chính xác gán nhãn hạ nguồn)**](./giai_thich_khai_niem.md#annotation-transfer):
   * *Bản chất*: Lấy tập đại diện $S$ đã có nhãn làm "cơ sở tri thức", dùng Nearest Neighbor phân loại nhãn phân họ/chức năng cho các chuỗi còn lại trong Ground Set $V \setminus S$.
   * *Mục tiêu phương pháp mới*: **Macro-F1 toàn cục và F1 riêng của các nhóm hiếm phải vượt trội rõ rệt** so với khi dùng tập đại diện của bài báo nền.

---

### 4.2. Bảng Tổng hợp Đối đầu các Chỉ số: Bài báo nền vs. RareProtSelect

| Nhóm chỉ số | Tên chỉ số cụ thể | Trạng thái ở Bài báo nền | Vai trò & Yêu cầu đối với Phương pháp mới (RareProtSelect) |
| :--- | :--- | :---: | :--- |
| **1. Chỉ số ĐỘT PHÁ CHO NHÓM HIẾM (Core Rare Improvements)** | **Worst-Group Coverage** | ❌ Chưa có | **$\uparrow$ Vượt trội hoàn toàn (Bài báo nền $\approx 0\%$, phương pháp mới đảm bảo cận dưới an toàn)** |
| | **Rare Group Representation Rate** | ❌ Chưa có | **$\uparrow$ Bao phủ $\ge 80\% - 100\%$ các nhóm hiếm (giữ mẫu vật thực tế cho phòng lab)** |
| | **Worst-Group F1 (Annotation Transfer)** | ❌ Chưa có | **$\uparrow$ Nâng cao vượt bậc độ chính xác gán nhãn cho các phân họ hiếm** |
| **2. Chỉ số ĐO MẶT BẰNG CHUNG (Central Tendency & Scale)** | **Macro Coverage** | ❌ Chưa có | **Đo mặt bằng chung phân bố qua các phân họ (đối trọng chống outlier, kỳ vọng cải thiện ở dữ liệu mất cân bằng)** |
| | **Overall Coverage / Sensitivity** | ✅ Đã có | **$\approx$ Đo quy mô tổng thể theo đầu chuỗi, duy trì tương đương (giảm không quá $1\% - 2\%$)** |
| | **Annotation Transfer Macro-F1** | ❌ Chưa có | **$\uparrow$ Đo độ chính xác gán nhãn trung bình qua tất cả các lớp** |
| **3. Chỉ số KIỂM SOÁT CHẤT LƯỢNG & TINH GỌN (Quality & Parity)** | **Overall Specificity** | ✅ Đã có | **$\approx$ Duy trì độ tinh sạch cao, sai số bắt nhầm $\le 0.02\%$** |
| | **Tính tinh gọn (Redundancy / Size $k$)** | ✅ Đã có | **$\approx$ Kích thước tập nhỏ gọn, không chọn các chuỗi sinh đôi dư thừa** |


---

### 4.3. Các chỉ số CẦN ĐÁNH GIÁ THÊM để bài báo chặt chẽ tuyệt đối (Ablation & Efficiency)

Để ban giám khảo hoặc người phản biện (reviewer) không thể bắt bẻ, đề tài bắt buộc thực hiện 3 thực nghiệm bóc tách (*Ablation Study*) và đo lường hiệu năng:

1. **Bóc tách vai trò của ESM-2 vs. BLAST**:
   * *Cách thực hiện*: Chạy **Unweighted FL với BLAST** (Bài báo nền) **vs.** **Unweighted FL với ESM-2**.
   * *Mục đích*: Chứng minh riêng việc chuyển đổi từ ký tự thô sang vector nhúng ESM-2 đã giúp nắm bắt mối quan hệ sinh học sâu (*Remote Homology* — cùng cấu trúc 3D/chức năng dù đột biến chuỗi) vượt trội hơn BLAST ra sao.
2. **Bóc tách vai trò của Hàm trọng số (Weighting Function)**:
   * *Cách thực hiện*: So sánh trực diện 3 lựa chọn trọng số trên cùng mô hình ESM-2 WFL:
     * **Không trọng số**: $w = 1$ (hoặc $1/|V|$)
     * **Căn bậc hai nghịch đảo (Rare-Aware)**: $w_v = 1/\sqrt{n_{g(v)}}$
     * **Nghịch đảo thuần**: $w_v = 1/n_{g(v)}$
   * *Mục đích*: Chứng minh vì sao trọng số $1/\sqrt{n_g}$ là **điểm cân bằng toán học tối ưu nhất** (vừa đủ mạnh để cứu nhóm hiếm mà không làm sụp đổ Overall Coverage như $1/n_g$).
3. **Đo lường chi phí tính toán (Computational Efficiency)**:
   * *Cách thực hiện*: Đo lường thời gian chạy (**Runtime**) và bộ nhớ đỉnh (**Peak Memory**).
   * *Mục đích*: Chứng minh thuật toán **Lazy Greedy (dùng Max-Heap)** chạy nhanh gấp hàng chục đến hàng trăm lần so với Standard Greedy trên các siêu họ protein lớn (như CE 12,277 chuỗi hay A1A 13,847 chuỗi), đáp ứng hoàn hảo yêu cầu tính toán thực tế.

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



