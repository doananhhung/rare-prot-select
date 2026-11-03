# TÀI LIỆU 1: QUY TRÌNH THỰC HIỆN & CÁC CÔNG ĐOẠN NGHIÊN CỨU KHOA HỌC (SSOT)
## Đề tài 2: Chọn Tập Protein Đại Diện Có Ưu Tiên Nhóm Hiếm Bằng Tối Ưu Hóa Submodular (`RareProtSelect`) Trên Siêu Họ Peptidase A1 (`MEROPS_A1A`)

> 📌 **VAI TRÒ CỦA TÀI LIỆU NÀY (NGUỒN SỰ THẬT DUY NHẤT - SINGLE SOURCE OF TRUTH - SSOT)**:
> * Đây là tài liệu quy định **toàn bộ quy trình nghiên cứu khoa học thuần túy** xuyên suốt chuỗi thực nghiệm từ **Nhánh 1 đến Nhánh 6** trên siêu họ Peptidase A1 (`baseline_repo/MEROPS_A1A.fasta`).
> * **Tuân thủ triệt để nguyên tắc `/controlled-scientific-experiment` (*Ceteris Paribus*)**: Mỗi giai đoạn nghiên cứu chỉ thay đổi duy nhất một biến số độc lập hoặc bổ sung tầng phân tích trực tiếp trên tập đại diện cố định, giữ nguyên 100% các thành phần đối chứng trước đó.
> * 🔗 **Liên kết kỹ thuật**: Mỗi công đoạn đều có liên kết trực tiếp sang [**Tài liệu 2: Thiết kế Codebase & Kiến trúc Hệ thống**](./thiet_ke_codebase_va_kien_truc_he_thong.md) và [**Tổng hợp Hệ thống Chỉ số Đánh giá**](./tong_hop_cac_chi_so_danh_gia.md).

---

## MỤC LỤC CÁC CÔNG ĐOẠN NGHIÊN CỨU (NHÁNH 1 $\to$ NHÁNH 6)

- **PHẦN I — GIAI ĐOẠN 1 (NHÁNH 1): Tái Hiện Đối Chuẩn Hình 8 Bài Báo Nền (*Nguyen et al., 2025*)**
  - [1. Đặt Vấn Đề & Mục Tiêu Khoa Học Cốt Lõi (Nhánh 1)](#sec-intro)
  - [2. Công Đoạn 1: Thu Thập & Kiểm Soát Chất Lượng Dữ Liệu (Quality Control)](#sec-cd1)
  - [3. Công Đoạn 2: Xây Dựng Ma Trận Tương Đồng Chuỗi Bằng NCBI BLASTp All-vs-All](#sec-cd2)
  - [4. Công Đoạn 3: Tối Ưu Hóa Tham Lam Cắt Tỉa & Bầu Chọn Đồng Thuận 1,000 Lần Xáo Trộn](#sec-cd3)
  - [5. Công Đoạn 4: Đánh Giá Thực Nghiệm Bằng Live BLAST Sensitivity Trên 11 Mốc Ngân Sách](#sec-cd4)
  - [6. Công Đoạn 5: Tiêu Chuẩn Nghiệm Thu & Đối Chiếu Trực Diện Với Hình 8 Bài Báo Gốc](#sec-cd5)
- **PHẦN II — GIAI ĐOẠN 2 (NHÁNH 2): Khảo Sát Hàm Mục Tiêu Có Trọng Số Ưu Tiên Nhóm Hiếm Trên Không Gian BLASTp (Phương Án 3B: 115 Phân Họ & Truy Vấn Ngược Nội Phân Họ)**
  - [7. Đặt Vấn Đề, Chuẩn Hóa Dữ Liệu Phương Án 3B & Mục Tiêu Khoa Học Cốt Lõi (Nhánh 2)](#sec-stage2-intro)
  - [8. Công Đoạn 2.1: Lọc Bỏ Khối Chưa Định Danh `A01.UPA` & Xây Dựng Họ Hàm Trọng Số Nghịch Đảo Quy Mô Phân Họ](#sec-stage2-cd1)
  - [9. Công Đoạn 2.2: Tối Ưu Hóa Pruned Greedy 90% (1,000-Shuffle, `budget_per_shuffle = 115`) Có Trọng Số Mẫu](#sec-stage2-cd2)
  - [10. Công Đoạn 2.3: Bộ 5 Thước Đo Phân Rã Nhóm Hiếm Bằng Truy Vấn Ngược Nội Phân Họ (`Within-Subfamily Live BLASTp`) Qua 20 Mốc Ngân Sách](#sec-stage2-cd3)
  - [11. Công Đoạn 2.4: Tiêu Chuẩn Nghiệm Thu Thực Nghiệm & Sản Phẩm Đầu Ra (Nhánh 2)](#sec-stage2-cd4)
- **PHẦN III — GIAI ĐOẠN 3 (NHÁNH 3): Khảo Sát Trong Không Gian Ngữ Nghĩa Liên Tục ESM-2 Với Độ Đo Bao Phủ Nội Phân Họ (`Within-Subfamily Coverage ESM %`)**
  - [12. Đặt Vấn Đề & Mục Tiêu Khoa Học Cốt Lõi (Nhánh 3)](#sec-stage3-intro)
  - [13. Công Đoạn 3.1: Biểu Diễn Phân Tử ESM-2 & Chuẩn Hóa Dịch Tâm Có Kiểm Soát ($\beta = 0.70$) Trên Tập 4,120 Chuỗi](#sec-stage3-cd1)
  - [14. Công Đoạn 3.2: Tối Ưu Hóa Pruned Greedy 90% (1,000-Shuffle, `budget_per_shuffle = 115`) Trên Không Gian ESM-2](#sec-stage3-cd2)
  - [15. Công Đoạn 3.3: Bộ 4 Thước Đo Độ Bao Phủ Ngữ Nghĩa Nội Phân Họ (`Within-Subfamily Coverage ESM %`) Qua 20 Mốc Ngân Sách](#sec-stage3-cd3)
  - [16. Công Đoạn 3.4: Tiêu Chuẩn Nghiệm Thu Thực Nghiệm & Sản Phẩm Đầu Ra (Nhánh 3)](#sec-stage3-cd4)
- **PHẦN IV — GIAI ĐOẠN 4 (NHÁNH 4): Kiểm Tra Chéo Hai Chiều ($2 \times 2$ Cross-Space Evaluation) Giữa `BLASTp` Và `ESM-2` Trên 115 Phân Họ**
  - [17. Đặt Vấn Đề & Mục Tiêu Khoa Học Cốt Lõi (Nhánh 4)](#sec-stage4-intro)
  - [18. Công Đoạn 4.1: Nạp Hai Bộ Đại Diện Đồng Thuận Cô Lập Từ Nhánh 2 Và Nhánh 3 (`budget_per_shuffle = 115`)](#sec-stage4-cd1)
  - [19. Công Đoạn 4.2: Đo Đạc Chéo Hai Chiều Trên Bộ 9 Chỉ Số Nội Phân Họ Chuẩn Hóa Qua 20 Mốc Ngân Sách](#sec-stage4-cd2)
  - [20. Công Đoạn 4.3: Tiêu Chuẩn Nghiệm Thu Thực Nghiệm & Sản Phẩm Đầu Ra (Nhánh 4)](#sec-stage4-cd3)
- **PHẦN V — GIAI ĐOẠN 5 (NHÁNH 5): Phân Tích Cấu Trúc Đại Diện Trực Tiếp & Độ Dư Thừa Phân Bổ Phân Họ Trong Tập $S_k$ Trên 115 Phân Họ**
  - [21. Đặt Vấn Đề, Bảng Tổng Hợp 6 Phương Pháp Đánh Giá & Mục Tiêu Khoa Học Cốt Lõi (Nhánh 5)](#sec-stage5-intro)
  - [22. Công Đoạn 5.1: Nạp Hai Bộ Đại Diện Đồng Thuận Cô Lập & Ánh Xạ Phân Bố 115 Phân Họ MEROPS A1A](#sec-stage5-cd1)
  - [23. Công Đoạn 5.2: Đo Đạc Bộ 4 Chỉ Số Cấu Trúc Đại Diện Trực Tiếp & Độ Dư Thừa Phân Họ Qua 20 Mốc Ngân Sách](#sec-stage5-cd2)
  - [24. Công Đoạn 5.3: Tiêu Chuẩn Nghiệm Thu Toán Học Bất Biến & Sản Phẩm Đầu Ra Bắt Buộc (Nhánh 5)](#sec-stage5-cd3)
- **PHẦN VI — GIAI ĐOẠN 6 (NHÁNH 6): Khảo Sát Động Học Bão Hòa Phân Họ Lớn & Dải Ngân Sách Sâu ($k \in [115..380]$) Trên 115 Phân Họ Peptidase A1**
  - [25. Đặt Vấn Đề, 6 Mốc Ngân Sách Chuyển Pha Sâu & Mục Tiêu Khoa Học Cốt Lõi (Nhánh 6)](#sec-stage6-intro)
  - [26. Công Đoạn 6.1: Tối Ưu Hóa Pruned Greedy 90% (1,000-Shuffle, `budget_per_shuffle = 380`) Trên Cả 2 Không Gian Tương Đồng](#sec-stage6-cd1)
  - [27. Công Đoạn 6.2: Đo Đạc Hệ Thống 18 Chỉ Số Phân Tầng Quy Mô Phân Họ & Độ Bão Hòa Nội Phân Họ Qua 6 Mốc Ngân Sách](#sec-stage6-cd2)
  - [28. Công Đoạn 6.3: Tiêu Chuẩn Nghiệm Thu Toán Học Bất Biến & Sản Phẩm Đầu Ra Bắt Buộc (Nhánh 6)](#sec-stage6-cd3)

---

<a id="sec-intro"></a>
## 1. ĐẶT VẤN ĐỀ & MỤC TIÊU KHOA HỌC CỐT LÕI

Trong bài báo nền tảng (*Nguyen et al., Nature Scientific Reports 2025*), các tác giả đã đề xuất phương pháp chọn tập protein đại diện cho các họ enzyme lớn bằng cách tối ưu hóa hàm Submodular Facility Location trên ma trận tương đồng chuỗi từ kết quả căn chỉnh cục bộ NCBI BLASTp.

Để chứng minh thuật toán có khả năng áp dụng trên các siêu họ protein có độ đa dạng cao, các tác giả đã thực nghiệm trên siêu họ **Peptidase A1 (MEROPS Family A1A)** và công bố kết quả tại **Hình 8 (Figure 8 Panel A, trang 12)**:
* **Bộ dữ liệu**: Siêu họ Peptidase A1 gồm $13,847$ chuỗi protein.
* **Dải ngân sách khảo sát**: Đúng **11 mốc ngân sách** trên trục hoành: $k \in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]$.
* **Thước đo duy nhất được công bố trên đồ thị**: **Độ nhạy toàn họ (Overall Sensitivity BLAST %)** đo bằng tỷ lệ phần trăm số chuỗi được tìm thấy khi dùng $k$ chuỗi đại diện làm mồi (Query) chạy Live BLAST với ngưỡng $E$-value $\le 10^{-7}$.
* **Khẳng định của tác giả**: Đạt trên $90\%$ độ nhạy chỉ với dưới 10 chuỗi đại diện (*"achieve over 90% coverage with less than 10 representative sequences"*), cụ thể đạt $\approx 90.8\%$ tại $k=10$ và $\approx 90.9\%$ tại $k=11$.

> 🎯 **Mục tiêu duy nhất của giai đoạn hiện tại**:
> Tái hiện độc lập $100\%$ quy trình thực nghiệm trên, chạy lại giải thuật gốc trên đúng bộ dữ liệu `MEROPS_A1A.fasta` qua đúng 11 mốc ngân sách $k \in [1..11]$, và đối chiếu đường cong `Overall Sensitivity BLAST (%)` thu được với Hình 8 Panel A của bài báo gốc.

---

<a id="sec-cd1"></a>
## 2. CÔNG ĐOẠN 1: THU THẬP & KIỂM SOÁT CHẤT LƯỢNG DỮ LIỆU (QUALITY CONTROL)

### 2.1. Nguồn dữ liệu:
* Tệp FASTA gốc: `baseline_repo/MEROPS_A1A.fasta` gồm **$13,847$ chuỗi protein** thuộc siêu họ Peptidase A1 từ cơ sở dữ liệu MEROPS.

### 2.2. Quy trình kiểm soát chất lượng (QC Filter):
Để đảm bảo ma trận tương đồng không bị sai lệch bởi các chuỗi rác hoặc phân mảnh giải trình tự lỗi, dữ liệu được quét qua bộ lọc chuẩn:
1. **Độ dài hợp lệ**: Giữ lại các chuỗi có độ dài $L \in [30, 2000]$ amino acid.
2. **Ký tự amino acid không xác định**: Tỷ lệ ký tự mơ hồ (`X, B, Z, J, *`) không vượt quá $5\%$.
3. **Khử trùng lặp**: Loại bỏ các chuỗi trùng lặp $100\%$ cả ID lẫn trình tự axit amin.

* **Kết quả đầu ra**: **$13,307$ chuỗi sạch** ($96.1\%$ tỷ lệ đạt chuẩn QC) tạo thành tập Ground Set $V$ phục vụ tính toán.
* 🔗 **Hiện thực hóa tại**: [Module `src/data/dataset_loader.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#sec-code-data).

---

<a id="sec-cd2"></a>
## 3. CÔNG ĐOẠN 2: XÂY DỰNG MA TRẬN TƯƠNG ĐỒNG CHUỖI BẰNG NCBI BLASTP ALL-VS-ALL

### 3.1. Đặc tả dòng lệnh căn chỉnh cục bộ (BLASTp All-vs-All):
Tái hiện trung thực $100\%$ phương pháp của bài báo nền (Greedy.R dòng 114–118) bằng công cụ dòng lệnh `blastp`:
$$\text{blastp -query fasta -subject fasta -evalue 0.05 -max\_target\_seqs 100 -word\_size 3 -outfmt '6 qseqid sseqid pident'}$$

### 3.2. Chuẩn hóa ma trận tương đồng:
1. **Chuẩn hóa tỷ lệ nhận dạng chuỗi**: $\operatorname{sim}_{\text{BLAST}}(u, v) = \frac{\text{pident}(u, v)}{100} \in [0.0, 1.0]$.
2. **Khử trùng lặp căn chỉnh (HSP)**: Với mỗi cặp $(u, v)$, giữ lại căn chỉnh có `pident` cao nhất (khớp dòng 125–127 trong `Greedy.R`).
3. **Xây dựng ma trận vuông $\mathbf{S} \in \mathbb{R}^{13,307 \times 13,307}$**:
   - Gán đường chéo $\mathbf{S}_{v, v} = 1.0$ (tự nhận dạng 100%).
   - Điền các vị trí không có căn chỉnh hợp lệ bằng $0.0$.
4. **Lưu đệm**: Lưu trữ ma trận dưới dạng tệp nén `MEROPS_A1A_blastp_sim_matrix.npz` để nạp tức thì trong các thực nghiệm tiếp theo.
* 🔗 **Hiện thực hóa tại**: [Module `src/similarity/blast_similarity.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#sec-code-sim).

---

<a id="sec-cd3"></a>
## 4. CÔNG ĐOẠN 3: TỐI ƯU HÓA THAM LAM CẮT TỈA & BẦU CHỌN ĐỒNG THUẬN 1,000 LẦN XÁO TRỘN

### 4.1. Hàm mục tiêu Submodular Facility Location không trọng số:
Bài báo gốc định nghĩa hàm mục tiêu độ bao phủ với trọng số đồng nhất ($w_v = 1.0, \forall v \in V$):
$$F(S) = \sum_{v \in V} \max_{s \in S} \operatorname{sim}_{\text{BLAST}}(v, s)$$

### 4.2. Thuật toán `Pruned Greedy 90% (1,000-Shuffle Consensus Ranking)`:
Để giải bài toán trên siêu họ lớn, bài báo gốc áp dụng thuật toán cắt tỉa kết hợp xáo trộn ngẫu nhiên (Greedy.R dòng 18–60 và 136–161):
1. **Cắt tỉa cứng 90% (Pruned Greedy)**:
   - Tại mỗi bước, chọn ứng viên $e^*$ có độ tăng biên $\Delta F(e \mid S) = F(S \cup \{e\}) - F(S)$ lớn nhất.
   - Ngay sau khi chọn $e^*$, loại bỏ toàn bộ các ứng viên $s$ còn lại có $\mathbf{S}(e^*, s) \ge 0.90$ ra khỏi tập xem xét tiếp theo.
2. **Xáo trộn ngẫu nhiên 1,000 lần (1,000-Shuffle Consensus Ranking)**:
   - Do có nhiều ứng viên có độ tăng biên bằng nhau (*ties*), thứ tự duyệt trong danh sách ban đầu sẽ ảnh hưởng đến quyết định chọn.
   - Thuật toán thực hiện hoán vị ngẫu nhiên danh sách ứng viên $1,000$ lần độc lập (`sample(allIDs)`).
   - Với mỗi vòng xáo trộn, chạy Pruned Greedy để ghi nhận danh sách chuỗi được chọn kèm thứ hạng (`repID`, `rank`).
   - Tổng hợp kết quả qua 1,000 vòng: tính tần suất xuất hiện `count = len(ranks)` và tổng thứ hạng `rank_sum = sum(ranks)`.
   - Sắp xếp giảm dần theo `count`, tăng dần theo `rank_sum` (`order(-count, rank_sum)`) để sinh ra **Danh sách Đại diện Đồng thuận Toàn cục (Consensus Ranking)**.
* 🔗 **Hiện thực hóa tại**: [Module `src/selection/standard_greedy.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#sec-code-sel) và kịch bản `experiments/exp1_baseline_a1a_calibration.py`.

---

<a id="sec-cd4"></a>
## 5. CÔNG ĐOẠN 4: ĐÁNH GIÁ THỰC NGHIỆM BẰNG LIVE BLAST SENSITIVITY TRÊN 11 MỐC NGÂN SÁCH

### 5.1. Dải ngân sách khảo sát:
Khảo sát chính xác **11 mốc ngân sách** của Hình 8:
$$k \in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]$$

### 5.2. Thước đo duy nhất: `Overall Sensitivity BLAST (%)`
Tại mỗi mốc $k$:
1. Trích xuất top $k$ chuỗi đại diện từ danh sách đồng thuận, ghi tệp `query_k.fasta`.
2. Tạo cơ sở dữ liệu `makeblastdb` từ toàn bộ tập protein sạch của họ A1A.
3. Chạy Live BLASTp tìm kiếm trực tiếp trên toàn bộ cơ sở dữ liệu:
   $$\text{blastp -query query\_k.fasta -db a1a\_db -evalue 1e-7 -max\_target\_seqs 999999}$$
4. Đếm số lượng chuỗi độc nhất trong họ có hit căn chỉnh hợp lệ và tính:
   $$\operatorname{Overall\_Sensitivity}_{\text{BLAST}}(k) = \frac{|\{v \in V \mid \text{BLAST}(S_k, v) \text{ có Hit}\}|}{|V|} \times 100\%$$
   *(với $|V| = 13,307$ chuỗi sạch)*.
* 🔗 **Hiện thực hóa tại**: Kịch bản `RareProtSelect/experiments/exp1_baseline_a1a_calibration.py`.

---

<a id="sec-cd5"></a>
## 6. TIÊU CHUẨN NGHIỆM THU & ĐỐI CHIẾU TRỰC DIỆN VỚI HÌNH 8 BÀI BÁO GỐC

### 6.1. Nguồn sự thật 11 mốc ước lượng từ đồ thị Hình 8 Panel A & Tiêu chuẩn nghiệm thu:
Do bài báo gốc (*Nguyen et al., 2025*, trang 12) công bố đường cong `Greedy` trên `A1A` tại **Hình 8 Panel A** dưới dạng đồ thị đường qua 11 điểm $k \in [1..11]$ mà không in bảng số chi tiết, toàn bộ 11 điểm trên đồ thị gốc đã được số hóa tọa độ tâm điểm (tỉ lệ trục tung $31.10\text{ px} = 1.0\%$, làm tròn 1 chữ số thập phân) và lưu trữ cố định tại tệp CSV Nguồn sự thật độc lập `outputs/tables/nguyen2025_fig8a_benchmark.csv`:
* Dãy 11 giá trị ước lượng từ Hình 8 Panel A ($k = 1 \dots 11$): **`[80.5%, 83.5%, 85.7%, 86.7%, 88.0%, 88.1%, 88.4%, 89.0%, 90.7%, 90.8%, 90.9%]`**.
* Kịch bản tái hiện được coi là nghiệm thu thành công khi đường cong thực nghiệm `Overall Sensitivity BLAST (%)` khớp sát toàn bộ 11 mốc của Hình 8 Panel A (độ lệch tuyệt đối trung bình $\le 1.0\%$, vượt ngưỡng $> 90\%$ trước $k = 10$).

### 6.2. Sản phẩm đầu ra bắt buộc:
1. **Tệp CSV Nguồn sự thật đối chuẩn bài báo gốc**: `outputs/tables/nguyen2025_fig8a_benchmark.csv` (lưu cố định 11 mốc $k=1 \dots 11$ ước lượng từ Hình 8 Panel A để tái sử dụng).
2. **Tệp cấu hình**: `configs/config_exp1_baseline_a1a_calibration.yaml` (chỉ chứa tham số thuật toán và đường dẫn `published_benchmark_csv`, tuyệt đối không gán cứng số liệu bài báo trong config).
3. **Kịch bản thực thi**: `experiments/exp1_baseline_a1a_calibration.py`.
4. **Bảng số liệu sạch**: `outputs/tables/exp1_baseline_a1a_calibration.csv` (đúng 11 dòng tương ứng $k=1 \dots 11$, điền đầy đủ cả 11 mốc tại cột `published_fig8_sensitivity_pct` và `deviation_pct`).
5. **Biểu đồ xuất bản sạch (1 panel)**: `outputs/figures/exp1_a1a_sensitivity_vs_k.png` (và `.svg`) thể hiện đường cong `Overall Sensitivity BLAST (%)` đối chiếu trực tiếp với đầy đủ 11 điểm của Hình 8 Panel A.

---

# PHẦN II: GIAI ĐOẠN 2 - KHẢO SÁT HÀM MỤC TIÊU CÓ TRỌNG SỐ ƯU TIÊN NHÓM HIẾM (RARE-AWARE WEIGHTED FACILITY LOCATION TRÊN 115 PHÂN HỌ ĐỊNH DANH & TRUY VẤN NGƯỢC NỘI PHÂN HỌ)

<a id="sec-stage2-intro"></a>
## 7. ĐẶT VẤN ĐỀ, CHUẨN HÓA DỮ LIỆU PHƯƠNG ÁN 3B & MỤC TIÊU KHOA HỌC CỐT LÕI (NHÁNH 2)

### 7.1. Lỗ hổng bỏ rơi nhóm hiếm của Baseline (Nhánh 1) & Bài toán Làm sạch Nhãn phân họ (Phương án 3B):
* Ở **Nhánh 1**, để tái lập trung thực $100\%$ Hình 8 Panel A của bài báo nền (*Nguyen et al., 2025*), thuật toán chạy trên toàn bộ $13,307$ chuỗi sạch của `MEROPS_A1A.fasta` mà không sử dụng nhãn phân họ. Tuy nhiên, khi giải phẫu cấu trúc tiêu đề (header) của $13,307$ chuỗi này, thực tế bao gồm:
  1. **$3,668$ chuỗi ($27.56\%$)** thuộc **75 phân họ chuẩn mã 3 chữ số (`[A01.001]` $\to$ `[A01.971]`)**.
  2. **$452$ chuỗi ($3.40\%$)** thuộc **40 phân họ chuẩn mã chữ-số (`[A01.A02]`, `[A01.A69]`, `[A01.P02]`...)**.
  3. **$9,187$ chuỗi ($69.04\%$)** mang thẻ **`[A01.UPA]`** (*Subfamily A1A Unassigned Peptidases* — các trình tự peptidase chưa được MEROPS phân loại vào bất kỳ phân họ Holotype cụ thể nào, chỉ ghi `[A01.UPA]#A01A#`).
* **Chuẩn hóa dữ liệu theo Phương án 3B (Curated Subfamilies Subset):**
  - Vì `[A01.UPA]` không phải là một phân họ sinh học mà là một rổ chứa tạm gồm các trình tự chưa định danh, từ **Nhánh 2 đến Nhánh 5**, hệ thống thực hiện:
    1. Mở rộng biểu thức chính quy trong `AnnotationMapper.extract_merops_subfamily()` thành `r"\[([A-Z]\d{2}\.(?!UPA)[A-Z0-9]{3})\]"` để thu nhận đầy đủ toàn bộ **$75 + 40 = 115$ phân họ định danh chính thức**, đồng thời gán `"A01.Unknown"` cho khối `[A01.UPA]`.
    2. Kích hoạt bộ lọc `exclude_unknown_subfamilies = true` để loại bỏ hoàn toàn $9,187$ chuỗi `[A01.UPA]` chưa định danh, thu được tập Ground Set chuẩn hóa **$V_{\text{curated}}$ gồm $|V| = 4,120$ chuỗi sạch** ($100\%$ có nhãn phân họ hợp lệ, $0\%$ Unknown).
  - **Cấu trúc mất cân bằng thực tế của $V_{\text{curated}}$ ($4,120$ chuỗi, $G = 115$ phân họ):**
    - Phân họ lớn nhất: **`A01.009` (Cathepsin D)** chứa **$329$ chuỗi sạch** ($339$ chuỗi trước lọc QC — khớp chính xác 100% với mô tả *"từ 339 chuỗi xuống 1 chuỗi"* tại `GEMINI.md` Mục 5.2), tiếp theo là `A01.089` ($217$ chuỗi), `A01.018` ($187$ chuỗi), `A01.019` ($185$ chuỗi), `A01.004` ($168$ chuỗi), `A01.001` (Pepsin A — $146$ chuỗi).
    - Phân bố nhóm: **$38$ phân họ lớn** ($n_g \ge 20$), **$32$ phân họ trung bình** ($6 \le n_g \le 19$), và **$|G_{\text{rare}}| = 45$ phân họ hiếm** ($n_g \le 5$ chuỗi, trong đó có **$18$ phân họ đơn độc / singleton** chỉ có đúng $1$ chuỗi).
    - Tỷ lệ mất cân bằng cực đoan: **$\text{Imbalance Ratio} = 329.0\times$** ($329 : 1$).

### 7.2. Mục tiêu nghiên cứu Nhánh 2 & Cơ chế Truy vấn ngược nội phân họ ($S_k \cap V_g \to V_g$):
* **Can thiệp trực tiếp vào toán học Submodular**: Đưa trọng số mẫu $w_v$ phụ thuộc nghịch đảo vào quy mô phân họ $n_{g(v)}$ để trao quyền lực đại diện cho $45$ phân họ hiếm.
* **Giải quyết giới hạn Nguyên lý Chuồng bồ câu ($k = 11 \ll G = 115$)**: Mở rộng dải ngân sách khảo sát từ 11 mốc bài báo gốc lên tới **$k_{\max} = G = 115$** (bằng đúng tổng số 115 phân họ định danh) qua **20 mốc chiến lược**:
  $$k \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115\}$$
* **Đánh giá bằng Truy vấn ngược nội phân họ (`Within-Subfamily Representative Query`: $S_k \cap V_g \to V_g$)**:
  - Đổ toàn bộ $|V| = 4,120$ chuỗi vào thuật toán để chọn ra tập đại diện $S_k$ ($|S_k| = k$).
  - Khi đánh giá độ nhạy trên từng phân họ $g \in \{1..115\}$, **chỉ những chuỗi đại diện trong $S_k$ thực sự thuộc về phân họ $g$ ($S_{k, g} = S_k \cap V_g$) mới được dùng để truy vấn ngược lại các thành viên trong phân họ $V_g$ của chính chuỗi đó**. Nếu một phân họ $g$ không có đại diện nào trong $S_k$ ($S_k \cap V_g = \emptyset$), độ nhạy của phân họ đó bắt buộc bằng **`0.0%`** (loại bỏ triệt để hiện tượng bắt dính chéo phân họ *cross-subfamily false positive*).
* **Nguyên tắc Cô lập Biến số (*Ceteris Paribus*)**:
  - Giữ nguyên 100%: Tập dữ liệu chuẩn hóa $V_{\text{curated}}$ ($4,120$ chuỗi, $115$ phân họ), ma trận tương đồng NCBI BLASTp All-vs-All ($4,120 \times 4,120$), thuật toán Pruned Greedy 90% (1,000-Shuffle Consensus Ranking với `budget_per_shuffle = 115`).
  - Biến số DUY NHẤT thay đổi: Hàm mục tiêu $F_\alpha(S) = \sum_{v \in V} w_v^{(\alpha)} \max_{u \in S} \mathbf{S}(u, v)$ qua 3 chế độ $\alpha \in \{0.0, 0.5, 1.0\}$.

---

<a id="sec-stage2-cd1"></a>
## 8. CÔNG ĐOẠN 2.1: LỌC BỎ KHỐI CHƯA ĐỊNH DANH `A01.UPA` & XÂY DỰNG HỌ HÀM TRỌNG SỐ NGHỊCH ĐẢO QUY MÔ PHÂN HỌ

### 8.1. Công thức tham số hóa toán học:
$$w_v^{(\alpha)} = \frac{1}{(n_{g(v)})^\alpha} \quad \text{với } \alpha \in \{0.0, 0.5, 1.0\}$$

* $n_{g(v)}$: Số lượng chuỗi thuộc phân họ của protein $v$ ($n_g \in [1, 329]$).
* $\alpha$: Hệ số phạt quy mô nhóm (Rareness Penalty Exponent).

### 8.2. Phân bố tổng trọng số của một phân họ $g$:
$$W_g^{(\alpha)} = \sum_{v \in V_g} w_v^{(\alpha)} = n_g \cdot \frac{1}{(n_g)^\alpha} = (n_g)^{1 - \alpha}$$

* $\alpha = 0.0$ (Baseline Unweighted): $W_g = n_g$. Phân họ lớn nhất `A01.009` ($329$ chuỗi) chiếm quyền lực gấp **$329.0\times$** phân họ hiếm $n=1$.
* $\alpha = 0.5$ (Cân bằng Pareto - Căn bậc hai nghịch đảo): $W_g = \sqrt{n_g}$. Phân họ `A01.009` được nén xuống gấp **$18.14\times$** phân họ hiếm $n=1$.
* $\alpha = 1.0$ (Công bằng nhóm tuyệt đối - Group-Equitable): $W_g = 1.0, \forall g \in \{1..115\}$. Mọi phân họ có tổng quyền lực hoàn toàn bình đẳng $1 : 1$.
* 🔗 **Hiện thực hóa tại**: Module `src/data/annotation_mapper.py`, `src/data/dataset_loader.py` và `src/selection/pruned_greedy.py` (hàm `compute_subfamily_weights`).

---

<a id="sec-stage2-cd2"></a>
## 9. CÔNG ĐOẠN 2.2: TỐI ƯU HÓA PRUNED GREEDY 90% (1,000-SHUFFLE, `budget_per_shuffle = 115`) CÓ TRỌNG SỐ MẪU & CẬP NHẬT CẬN BIÊN TRỰC TIẾP TRÊN GPU

### 9.1. Công thức độ tăng cận biên có trọng số & Cập nhật trực tiếp (Incremental Marginal Gain Update):
$$\Delta(u \mid S) = \sum_{v \in V} w_v^{(\alpha)} \max\left(0, \mathbf{S}(u, v) - \max_{s \in S} \mathbf{S}(s, v)\right)$$
* Tại bước khởi tạo $S = \emptyset$, tính sẵn vector lợi ích cận biên cơ sở $\mathbf{g}^{(0)} = \mathbf{w}^\top \mathbf{S}$ một lần duy nhất.
* Khi ứng viên $c^*$ được chọn vào $S$ tại bước $t$, chỉ cập nhật lại $\mathbf{g}^{(t+1)}$ trên tập các hàng $\mathcal{I}_{\text{changed}} = \{v \mid \mathbf{S}_{v, c^*} > m^{(t)}_v\}$ và phá hòa theo hoán vị ngẫu nhiên $\pi$ (`perm_t`), bảo toàn 100% kết quả toán học của `Greedy.R`.

### 9.2. Quy trình xáo trộn 1,000 lần tích hợp `tqdm`:
1. Vòng lặp ngoài quét qua 3 mức $\alpha \in \{0.0, 0.5, 1.0\}$.
2. Với mỗi $\alpha$, thực hiện 1,000 vòng xáo trộn ngẫu nhiên trên GPU PyTorch CUDA với `budget_per_shuffle = 115` (đảm bảo bầu chọn đủ 115 đại diện trong mỗi vòng).
3. Tổng hợp bảng xếp hạng đồng thuận toàn cục (Consensus Ranking) bằng `order(-count, rank_sum)` theo đúng `Greedy.R`.
4. Lưu đệm từng file riêng cho tập Curated: `MEROPS_A1A_curated_1000_shuffles_alpha_{alpha:.2f}.npz` kèm `metadata` lưu rõ `budget_per_shuffle = 115` (cô lập hoàn toàn với cache $13,307$ chuỗi của Nhánh 1).
* 🔗 **Hiện thực hóa tại**: Module `src/selection/pruned_greedy.py` và kịch bản `RareProtSelect/experiments/exp2_rare_weighted_a1a.py`.

---

<a id="sec-stage2-cd3"></a>
## 10. CÔNG ĐOẠN 2.3: BỘ 5 THƯỚC ĐO PHÂN RÃ NHÓM HIẾM BẰNG TRUY VẤN NGƯỢC NỘI PHÂN HỌ (`WITHIN-SUBFAMILY LIVE BLASTP`) QUA 20 MỐC NGÂN SÁCH (ĐẾN $k = 115$)

Tại mỗi mốc ngân sách $k \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115\}$ của từng $\alpha \in \{0.0, 0.5, 1.0\}$:
1. Gọi $S_k$ là tập $k$ chuỗi đại diện đầu tiên trong danh sách đồng thuận, và $S_{k, g} = S_k \cap V_g$ là tập các chuỗi đại diện thuộc phân họ $g \in \{1..115\}$.
2. Tạo file query top $k$ đại diện đồng thuận, thực thi Live `blastp` ($E \le 10^{-7}$) trên cơ sở dữ liệu `MEROPS_A1A_curated_live_db` và lọc các cặp hit `(qseqid, sseqid)` **cùng phân họ** (`id_to_family[qseqid] == id_to_family[sseqid]`):
   $$C_{k, g}^{\text{within}} = \left\{v \in V_g \;\middle|\; \exists s \in (S_k \cap V_g) : \operatorname{BLASTp}(s, v) \text{ có Hit } E \le 10^{-7}\right\}$$
   *(Nếu $S_k \cap V_g = \emptyset$, thì $C_{k, g}^{\text{within}} = \emptyset$).*
3. Tính toán chính xác 5 chỉ số nội phân họ độc lập:
   * **Overall Within-Subfamily Sensitivity BLAST (%)**:
     $$\operatorname{Overall\_Sens} = \frac{\sum_{g=1}^{115} |C_{k, g}^{\text{within}}|}{|V|} \times 100\% \quad (|V| = 4,120)$$
   * **Within-Subfamily Sensitivity của từng phân họ $g$**:
     $$\operatorname{Sens}_g = \frac{|C_{k, g}^{\text{within}}|}{|V_g|} \times 100\% \quad (g = 1 \dots 115)$$
   * **Worst-Group Sensitivity BLAST (%)**:
     $$\operatorname{Worst\_Sens} = \min_{g \in [1..115]} \operatorname{Sens}_g$$
   * **Rare Sensitivity BLAST (%)**: Trung bình độ nhạy của 45 phân họ hiếm có $|V_g| \le 5$ chuỗi:
     $$\operatorname{Rare\_Sens} = \frac{1}{|G_{\text{rare}}|} \sum_{g \in G_{\text{rare}}} \operatorname{Sens}_g \quad (|G_{\text{rare}}| = 45)$$
   * **Macro-Average Sensitivity BLAST (%)**:
     $$\operatorname{Macro\_Sens} = \frac{1}{115} \sum_{g=1}^{115} \operatorname{Sens}_g$$
   * **Zero-Sensitivity Subfamilies Count**:
     $$\operatorname{Zero\_Count} = |\{g \in [1..115] \mid \operatorname{Sens}_g = 0.0\%\}|$$
* 🔗 **Hiện thực hóa tại**: Kịch bản `RareProtSelect/experiments/exp2_rare_weighted_a1a.py`.

---

<a id="sec-stage2-cd4"></a>
## 11. CÔNG ĐOẠN 2.4: TIÊU CHUẨN NGHIỆM THU THỰC NGHIỆM & SẢN PHẨM ĐẦU RA

### 11.1. Tiêu chuẩn nghiệm thu khoa học:
1. **Kiểm định bất biến Truy vấn ngược nội phân họ tại $k = 1$**: Tại $k = 1$ (chỉ có 1 phân họ duy nhất có đại diện), bắt buộc đúng $114 / 115$ phân họ còn lại có $\operatorname{Sens}_g = 0.0\%$ (`zero_cov_subfamilies_count == 114`).
2. **Đánh giá xuyên suốt từ ngân sách nhỏ ($k=11$) đến ngân sách đủ 115 phân họ ($k=115$)**: So sánh sự biến thiên của 5 thước đo độ nhạy nội phân họ qua 20 mốc $k$ giữa $\alpha \in \{0.0, 0.5, 1.0\}$.

### 11.2. Sản phẩm đầu ra bắt buộc:
1. **Tệp cấu hình**: `configs/config_exp2_rare_weighted_a1a.yaml`.
2. **Kịch bản thực thi**: `experiments/exp2_rare_weighted_a1a.py`.
3. **Bảng số liệu sạch duy nhất**: `outputs/tables/exp2_rare_weighted_a1a.csv` (đúng $3 \times 20 = 60$ dòng dữ liệu thực nghiệm).
4. **Hệ thống 3 biểu đồ công bố khoa học**:
   - `outputs/figures/exp2_pareto_tradeoff.png` & `.svg`: Đối chiếu song song đường cong đánh đổi Pareto tại 2 mốc chiến lược $k = 11$ và $k = 115$.
   - `outputs/figures/exp2_metrics_vs_k.png` & `.svg`: Biến thiên của 4 chỉ số độ nhạy nội phân họ theo ngân sách $k \in [1..115]$ qua 3 mức $\alpha \in \{0.0, 0.5, 1.0\}$.
   - `outputs/figures/exp2_zero_cov_vs_alpha.png` & `.svg`: Đối chiếu song song số phân họ bị 0% độ nhạy theo hệ số $\alpha \in \{0.0, 0.5, 1.0\}$ tại $k = 11$ và $k = 115$.

---

# PHẦN III: GIAI ĐOẠN 3 - KHẢO SÁT TRONG KHÔNG GIAN BIỂU DIỄN NGỮ NGHĨA LIÊN TỤC ESM-2 VỚI ĐỘ ĐO BAO PHỦ NỘI PHÂN HỌ (`WITHIN-SUBFAMILY COVERAGE ESM %`)

<a id="sec-stage3-intro"></a>
## 12. ĐẶT VẤN ĐỀ & MỤC TIÊU KHOA HỌC CỐT LÕI (NHÁNH 3)

### 12.1. Giới hạn của không gian căn chỉnh cục bộ rời rạc (BLASTp) & bài toán Suy biến Dị hướng (Representation Anisotropy):
* Trong Nhánh 2, ma trận tương đồng $\mathbf{S}_{\text{BLAST}}$ trên tập $V_{\text{curated}}$ ($4,120 \times 4,120$) được xây dựng từ công cụ căn chỉnh cục bộ NCBI BLASTp (`-evalue 0.05 -max_target_seqs 100`). Do giới hạn cắt ngưỡng thống kê và chỉ giữ tối đa 100 mục tiêu cho mỗi chuỗi, ma trận BLASTp rất thưa, khiến các protein xa nhau trong cùng phân họ hoặc giữa các phân họ tiến hóa xa bị gán độ tương đồng bằng $0.0$ tuyệt đối.
* Khi chuyển sang mô hình ngôn ngữ protein tiền huấn luyện **ESM-2** (`facebook/esm2_t12_35M_UR50D`, vector nhúng 480 chiều), không gian biểu diễn trở nên liên tục và dày đặc, được chuẩn hóa bằng phép **Dịch tâm có kiểm soát ($\beta = 0.70$)** để khử hiệu ứng suy biến dị hướng hình nón hẹp (*Representation Anisotropy*).

### 12.2. Mục tiêu nghiên cứu Nhánh 3 (Nguyên tắc Cô lập Biến số - *Ceteris Paribus*):
* **Biến số độc lập duy nhất thay đổi so với Nhánh 2**: Thay thế ma trận tương đồng rời rạc $\mathbf{S}_{\text{BLAST}}$ bằng **Ma trận tương đồng ngữ nghĩa liên tục ESM-2 đã khử dị hướng ($\beta = 0.70$)** $\mathbf{S}_{\text{ESM}} \in [0, 1]^{4,120 \times 4,120}$, đồng thời đánh giá bằng **bộ 4 thước đo Độ bao phủ ngữ nghĩa nội phân họ (`Within-Subfamily Coverage ESM %`)**.
* **Các yếu tố đối chứng giữ nguyên 100% như Nhánh 2**:
  - Tập dữ liệu chuẩn hóa $V_{\text{curated}}$ (`MEROPS_A1A.fasta` sau lọc `UPA`: $4,120$ chuỗi sạch, $115$ phân họ định danh, $45$ phân họ hiếm $\le 5$ chuỗi).
  - Họ hàm trọng số ưu tiên nhóm hiếm $w_v^{(\alpha)} = (n_{g(v)})^{-\alpha}$ với 3 mức $\alpha \in \{0.0, 0.5, 1.0\}$.
  - Giải thuật `Pruned Greedy 90% (1,000-Shuffle Consensus Ranking)` với `prune_threshold = 0.90`, `num_shuffles = 1000`, `seed = 42`, `budget_per_shuffle = 115`.
  - Dải 20 mốc ngân sách chiến lược: $k \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115\}$.

---

<a id="sec-stage3-cd1"></a>
## 13. CÔNG ĐOẠN 3.1: BIỂU DIỄN PHÂN TỬ ESM-2 & CHUẨN HÓA DỊCH TÂM CÓ KIỂM SOÁT (PARTIAL MEAN-CENTERED COSINE SIMILARITY, $\beta = 0.70$) TRÊN TẬP 4,120 CHUỖI

### 13.1. Trích xuất vector nhúng mức chuỗi (Sequence-level Mean Pooling):
Với mỗi chuỗi protein sạch $v \in V_{\text{curated}}$ ($4,120$ chuỗi), mô hình `facebook/esm2_t12_35M_UR50D` sinh ra vector đặc trưng $z_v \in \mathbb{R}^{480}$ (lưu đệm tại `outputs/embeddings_cache/MEROPS_A1A_curated_facebook_esm2_t12_35M_UR50D.npy`).

### 13.2. Khử suy biến dị hướng bằng Dịch tâm có kiểm soát (Partial Mean-Centering với $\beta = 0.70$):
1. **Tính vector tâm đám mây toàn cục trên $V_{\text{curated}}$**:
   $$\mu = \frac{1}{|V|} \sum_{v \in V} z_v \in \mathbb{R}^{480} \quad (|V| = 4,120)$$
2. **Dịch tâm có kiểm soát với hệ số $\beta = 0.70$ và chuẩn hóa đơn vị $L_2$**:
   $$z'_v(\beta) = \frac{z_v - \beta \mu}{\|z_v - \beta \mu\|_2 + \epsilon} \quad \left(\beta = 0.70, \; \|z'_v(\beta)\|_2 = 1.0\right)$$
3. **Ma trận tương đồng Cosine không âm (Non-negative Partial Mean-Centered Cosine Matrix)**:
   $$\mathbf{S}_{\text{ESM}}^{(\beta)}(u, v) = \max\left(0.0, {z'_u(\beta)}^\top z'_v(\beta)\right) \in [0.0, 1.0], \quad \mathbf{S}_{\text{ESM}}^{(\beta)}(v, v) = 1.0$$
* 🔗 **Hiện thực hóa tại**: [Module `src/similarity/dense_similarity.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#module-similarity) (hàm `compute_mean_centered_cosine_matrix` và lớp `ESM2SimilarityMatrix`).

---

<a id="sec-stage3-cd2"></a>
## 14. CÔNG ĐOẠN 3.2: TỐI ƯU HÓA PRUNED GREEDY 90% (1,000-SHUFFLE, `budget_per_shuffle = 115`) TRÊN KHÔNG GIAN ESM-2

### 14.1. Hàm mục tiêu Facility Location có trọng số trên không gian ESM-2:
$$F_{\alpha}^{\text{ESM}}(S) = \sum_{v \in V} w_v^{(\alpha)} \max_{s \in S} \mathbf{S}_{\text{ESM}}(s, v), \quad w_v^{(\alpha)} = \frac{1}{(n_{g(v)})^\alpha}, \quad \alpha \in \{0.0, 0.5, 1.0\}$$

### 14.2. Thực thi và cô lập bộ nhớ đệm (Cache Isolation):
* Áp dụng chính xác hàm `run_pruned_greedy_1000_shuffles` trên GPU PyTorch CUDA (`budget_per_shuffle = 115`, `prune_threshold = 0.90`, `num_shuffles = 1000`, `seed = 42`).
* Lưu bảng xếp hạng đồng thuận của từng mức $\alpha$ vào tệp đệm riêng biệt:
  `outputs/similarity_cache/MEROPS_A1A_curated_esm2_1000_shuffles_alpha_{alpha:.2f}.npz`
  (tách biệt hoàn toàn với cache BLASTp của Nhánh 2 để phục vụ kiểm tra chéo ở Nhánh 4).
* 🔗 **Hiện thực hóa tại**: [Module `src/selection/pruned_greedy.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#module-selection) và kịch bản `RareProtSelect/experiments/exp3_esm_coverage_a1a.py`.

---

<a id="sec-stage3-cd3"></a>
## 15. CÔNG ĐOẠN 3.3: BỘ 4 THƯỚC ĐO ĐỘ BAO PHỦ NGỮ NGHĨA NỘI PHÂN HỌ (`WITHIN-SUBFAMILY COVERAGE ESM %`) QUA 20 MỐC NGÂN SÁCH

Tại mỗi mốc ngân sách $k \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115\}$ và mỗi $\alpha \in \{0.0, 0.5, 1.0\}$, gọi $S_k$ là tập $k$ chuỗi đại diện đầu tiên trong danh sách đồng thuận và $S_{k, g} = S_k \cap V_g$ là tập các chuỗi đại diện thuộc phân họ $g \in \{1..115\}$:
1. **Điểm bao phủ ngữ nghĩa nội phân họ của từng chuỗi protein $v \in V_g$**:
   $$c_v^{\text{within}}(S_k) = \begin{cases} 0.0 & \text{nếu } S_k \cap V_g = \emptyset \\ \max_{s \in S_k \cap V_g} \mathbf{S}_{\text{ESM}}^{(\beta=0.70)}(s, v) & \text{nếu } S_k \cap V_g \neq \emptyset \end{cases} \in [0.0, 1.0]$$
2. **Độ bao phủ ngữ nghĩa nội phân họ của từng phân họ $g \in \{1..115\}$**:
   $$\operatorname{Cov}_g(S_k) = \frac{1}{|V_g|} \sum_{v \in V_g} c_v^{\text{within}}(S_k) \times 100\%$$
3. **Bộ 4 chỉ số đánh giá chính thức**:
   * **Overall Within-Subfamily Coverage ESM (%)**:
     $$\operatorname{Overall\_Cov}_{\text{ESM}}(S_k) = \frac{1}{|V|} \sum_{v \in V} c_v^{\text{within}}(S_k) \times 100\% \quad (|V| = 4,120)$$
   * **Worst-Group Coverage ESM (%)**:
     $$\operatorname{Worst\_Cov}_{\text{ESM}}(S_k) = \min_{g \in [1..115]} \operatorname{Cov}_g(S_k)$$
   * **Rare Coverage ESM (%)** (Trung bình trên 45 phân họ hiếm có $|V_g| \le 5$ chuỗi):
     $$\operatorname{Rare\_Cov}_{\text{ESM}}(S_k) = \frac{1}{|G_{\text{rare}}|} \sum_{g \in G_{\text{rare}}} \operatorname{Cov}_g(S_k) \quad (|G_{\text{rare}}| = 45)$$
   * **Macro-Average Coverage ESM (%)** (Trung bình bình đẳng trên toàn bộ 115 phân họ):
     $$\operatorname{Macro\_Cov}_{\text{ESM}}(S_k) = \frac{1}{115} \sum_{g=1}^{115} \operatorname{Cov}_g(S_k)$$
* 🔗 **Hiện thực hóa tại**: Kịch bản `RareProtSelect/experiments/exp3_esm_coverage_a1a.py` (hàm `evaluate_esm_coverage_representatives`).

---

<a id="sec-stage3-cd4"></a>
## 16. CÔNG ĐOẠN 3.4: TIÊU CHUẨN NGHIỆM THU THỰC NGHIỆM & SẢN PHẨM ĐẦU RA (NHÁNH 3)

### 16.1. Tiêu chuẩn nghiệm thu khoa học:
1. **Kiểm chứng bất biến nội phân họ tại $k = 1$**: Tại $k = 1$, đúng $114 / 115$ phân họ không có đại diện phải có $\operatorname{Cov}_g(S_1) = 0.0\%$, do đó `worst_group_coverage_esm_pct == 0.0`.
2. **Đánh giá quy luật tăng trưởng theo $\alpha$ trên không gian ESM-2**: Đối chiếu sự gia tăng của `Overall Coverage ESM (%)`, `Rare Coverage ESM (%)` và `Macro Coverage ESM (%)` khi tăng $\alpha$ từ $0.0 \to 0.5 \to 1.0$ trên toàn dải 20 mốc ngân sách từ $k = 11$ đến $k = 115$.

### 16.2. Sản phẩm đầu ra bắt buộc:
1. **Tệp cấu hình**: `configs/config_exp3_esm_coverage_a1a.yaml`.
2. **Kịch bản thực thi**: `experiments/exp3_esm_coverage_a1a.py`.
3. **Bảng số liệu sạch duy nhất**: `outputs/tables/exp3_esm_coverage_a1a.csv` (đúng $3 \times 20 = 60$ dòng dữ liệu thực nghiệm với 4 cột chỉ số phần trăm `Coverage ESM (%)`).
4. **Hệ thống 2 biểu đồ công bố khoa học** (định dạng `.png` và `.svg`):
   - `outputs/figures/exp3_pareto_tradeoff.png` & `.svg`: Đối chiếu song song đường cong đánh đổi Pareto tại 2 mốc chiến lược $k = 11$ và $k = 115$.
   - `outputs/figures/exp3_metrics_vs_k.png` & `.svg`: Biểu đồ 4 ô ($2 \times 2$) diễn tiến của 4 chỉ số `Coverage ESM (%)` theo ngân sách $k \in [1..115]$ qua 3 mức $\alpha \in \{0.0, 0.5, 1.0\}$.

---

# PHẦN IV: GIAI ĐOẠN 4 - KIỂM TRA CHÉO HAI CHIỀU GIỮA KHÔNG GIAN CĂN CHỈNH RỜI RẠC (BLASTP) VÀ KHÔNG GIAN NGỮ NGHĨA LIÊN TỤC (ESM-2) TRÊN 115 PHÂN HỌ (CROSS-SPACE EVALUATION $2 \times 2$)

<a id="sec-stage4-intro"></a>
## 17. ĐẶT VẤN ĐỀ & MỤC TIÊU KHOA HỌC CỐT LÕI (NHÁNH 4)

### 17.1. Bài toán khử nhiễu biến giữa Không gian Chọn đại diện và Không gian Đánh giá:
* Ở Nhánh 2, tập đại diện $S_{\alpha, k}^{\text{BLASTp}}$ được tối ưu hóa trên ma trận căn chỉnh rời rạc $\mathbf{S}_{\text{BLAST}}$ ($4,120 \times 4,120$) và đánh giá bằng **bộ 5 chỉ số Truy vấn ngược nội phân họ `Within-Subfamily Live BLASTp Sensitivity (%)`** ($E \le 10^{-7}$).
* Ở Nhánh 3, tập đại diện $S_{\alpha, k}^{\text{ESM-2}}$ được tối ưu hóa trên ma trận ngữ nghĩa liên tục $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$ ($4,120 \times 4,120$) và đánh giá bằng **bộ 4 chỉ số Độ bao phủ ngữ nghĩa nội phân họ `Within-Subfamily Coverage ESM (%)`**.
* Để cô lập tuyệt đối biến số **Không gian Biểu diễn chọn đại diện** (`selection_space` $\in \{\text{"BLASTp"}, \text{"ESM-2"}\}$) theo nguyên tắc *Ceteris Paribus*, chúng ta đặt cả hai tập đại diện lên cùng một mặt trận thước đo thông qua **Ma trận Kiểm tra Chéo $2 \times 2$ (Full $2 \times 2$ Cross-Space Evaluation)**:
  1. **Mặt trận 1 — Đánh giá bằng `Within-Subfamily Live BLASTp Sensitivity (%)` (5 chỉ số nội phân họ, $E \le 10^{-7}$)**:
     - Ô đường chéo $(1, 1)$: Đại diện chọn bởi BLASTp (Nhánh 2) $\to$ đo bằng `Within-Subfamily Live BLASTp Sensitivity (%)`.
     - **Ô chéo $(2, 1)$ (`ESM-2 Selected` $\to$ `Within-Subfamily Live BLASTp Eval`)**: Đem các đại diện nội phân họ $S_k \cap V_g$ chọn bởi ESM-2 (Nhánh 3) truy vấn `blastp` ($E \le 10^{-7}$) vào chính phân họ $V_g$ của nó trên cơ sở dữ liệu `MEROPS_A1A_curated_live_db`.
  2. **Mặt trận 2 — Đánh giá bằng `Within-Subfamily Coverage ESM (%)` (4 chỉ số nội phân họ liên tục trên $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$)**:
     - **Ô chéo $(1, 2)$ (`BLASTp Selected` $\to$ `Within-Subfamily ESM-2 Coverage Eval`)**: Chiếu các đại diện nội phân họ $S_k \cap V_g$ chọn bởi BLASTp (Nhánh 2) lên ma trận ngữ nghĩa liên tục $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$ của chính phân họ $V_g$.
     - Ô đường chéo $(2, 2)$: Đại diện chọn bởi ESM-2 (Nhánh 3) $\to$ đo bằng `Within-Subfamily Coverage ESM (%)`.

---

<a id="sec-stage4-cd1"></a>
## 18. CÔNG ĐOẠN 4.1: NẠP HAI BỘ ĐẠI DIỆN ĐỒNG THUẬN CÔ LẬP TỪ NHÁNH 2 VÀ NHÁNH 3 (`budget_per_shuffle = 115`)

* Giữ nguyên 100% tập dữ liệu chuẩn hóa $V_{\text{curated}}$ ($4,120$ chuỗi, $115$ phân họ, $45$ phân họ hiếm $\le 5$ chuỗi), 3 mức trọng số $\alpha \in \{0.0, 0.5, 1.0\}$ và 20 mốc ngân sách $k \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115\}$.
* Nạp trực tiếp 2 bộ danh sách đại diện đồng thuận 1,000 lần xáo trộn (`budget_per_shuffle = 115`, `prune_threshold = 0.90`, `seed = 42`):
  1. **Đại diện `BLASTp`**: `outputs/similarity_cache/MEROPS_A1A_curated_1000_shuffles_alpha_{alpha:.2f}.npz`.
  2. **Đại diện `ESM-2`**: `outputs/similarity_cache/MEROPS_A1A_curated_esm2_1000_shuffles_alpha_{alpha:.2f}.npz`.
* 🔗 **Hiện thực hóa tại**: Kịch bản `RareProtSelect/experiments/exp4_cross_eval_a1a.py`.

---

<a id="sec-stage4-cd2"></a>
## 19. CÔNG ĐOẠN 4.2: ĐO ĐẠC CHÉO HAI CHIỀU TRÊN BỘ 9 CHỈ SỐ NỘI PHÂN HỌ CHUẨN HÓA QUA 20 MỐC NGÂN SÁCH

Tại mỗi tổ hợp $(\text{selection\_space}, \alpha, k)$ trong tổng số $2 \times 3 \times 20 = 120$ cấu hình thực nghiệm:
1. **Đo đạc bộ 5 chỉ số `Within-Subfamily Live BLASTp Sensitivity (%)` ($E \le 10^{-7}$)**:
   - `overall_sensitivity_blast_pct` ($\frac{\sum_{g=1}^{115} |C_{k, g}^{\text{within}}|}{4,120} \times 100\%$)
   - `worst_group_sensitivity_blast_pct` ($\min_{g \in [1..115]} \operatorname{Sens}_g$)
   - `rare_sensitivity_blast_pct` ($\frac{1}{45} \sum_{g \in G_{\text{rare}}} \operatorname{Sens}_g$)
   - `macro_sensitivity_blast_pct` ($\frac{1}{115} \sum_{g=1}^{115} \operatorname{Sens}_g$)
   - `zero_cov_subfamilies_count` ($|\{g \in [1..115] \mid \operatorname{Sens}_g = 0.0\%\}|$)
2. **Đo đạc bộ 4 chỉ số `Within-Subfamily Coverage ESM (%)` trên $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$**:
   - `overall_coverage_esm_pct` ($\frac{1}{4,120} \sum_{v \in V} c_v^{\text{within}}(S_k) \times 100\%$)
   - `worst_group_coverage_esm_pct` ($\min_{g \in [1..115]} \operatorname{Cov}_g(S_k)$)
   - `rare_coverage_esm_pct` ($\frac{1}{45} \sum_{g \in G_{\text{rare}}} \operatorname{Cov}_g(S_k)$)
   - `macro_coverage_esm_pct` ($\frac{1}{115} \sum_{g=1}^{115} \operatorname{Cov}_g(S_k)$)
* 🔗 **Hiện thực hóa tại**: Kịch bản `RareProtSelect/experiments/exp4_cross_eval_a1a.py`.

---

<a id="sec-stage4-cd3"></a>
## 20. CÔNG ĐOẠN 4.3: TIÊU CHUẨN NGHIỆM THU THỰC NGHIỆM & SẢN PHẨM ĐẦU RA (NHÁNH 4)

### 20.1. Tiêu chuẩn nghiệm thu khoa học:
1. **Kiểm định tính bất biến của 2 ô đường chéo chính**:
   - $60$ dòng có `selection_space == "BLASTp"` trong bảng Nhánh 4 phải khớp chính xác $100.00\%$ với `outputs/tables/exp2_rare_weighted_a1a.csv` trên cả 5 chỉ số `Live BLASTp Sensitivity (%)`.
   - $60$ dòng có `selection_space == "ESM-2"` trong bảng Nhánh 4 phải khớp chính xác $100.00\%$ với `outputs/tables/exp3_esm_coverage_a1a.csv` trên cả 4 chỉ số `Coverage ESM (%)`.
2. **Hoàn thiện đối chiếu chéo 2 chiều ($2 \times 2$)**: Đo đạc đầy đủ thực nghiệm 60 truy vấn Live BLASTp nội phân họ cho `selection_space == "ESM-2"` và 60 phép chiếu `Coverage ESM (%)` nội phân họ cho `selection_space == "BLASTp"`.

### 20.2. Sản phẩm đầu ra bắt buộc:
1. **Tệp cấu hình**: `configs/config_exp4_cross_eval_a1a.yaml`.
2. **Kịch bản thực thi**: `experiments/exp4_cross_eval_a1a.py`.
3. **Bảng số liệu sạch hợp nhất duy nhất**: `outputs/tables/exp4_cross_eval_a1a.csv` (đúng $2 \times 3 \times 20 = 120$ dòng dữ liệu thực nghiệm, chứa đầy đủ cả 5 chỉ số `Live BLASTp Sensitivity (%)` và 4 chỉ số `Coverage ESM (%)`).
4. **Hệ thống 3 biểu đồ đối đầu trực diện** (định dạng `.png` và `.svg`):
   - `outputs/figures/exp4_blast_eval_comparison_vs_k.png` & `.svg`: Biểu đồ 4 ô ($2 \times 2$) so sánh `ESM-2 Selected` (nét liền) vs. `BLASTp Selected` (nét đứt) trên mặt trận `Live BLASTp Sensitivity (%)` theo ngân sách $k \in [1..115]$.
   - `outputs/figures/exp4_esm_eval_comparison_vs_k.png` & `.svg`: Biểu đồ 4 ô ($2 \times 2$) so sánh `ESM-2 Selected` (nét liền) vs. `BLASTp Selected` (nét đứt) trên mặt trận `Coverage ESM (%)` theo ngân sách $k \in [1..115]$.
   - `outputs/figures/exp4_cross_space_summary_k11_k115.png` & `.svg`: Biểu đồ đối chiếu tổng hợp tại $k = 11$ và $k = 115$ giữa `BLASTp Selected` và `ESM-2 Selected`.

---

# PHẦN V: GIAI ĐOẠN 5 - PHÂN TÍCH CẤU TRÚC ĐẠI DIỆN TRỰC TIẾP & ĐỘ DƯ THỪA PHÂN BỔ PHÂN HỌ TRONG TẬP $S_k$ TRÊN 115 PHÂN HỌ (NHÁNH 5)

<a id="sec-stage5-intro"></a>
## 21. ĐẶT VẤN ĐỀ, BẢNG TỔNG HỢP 6 PHƯƠNG PHÁP ĐÁNH GIÁ & MỤC TIÊU KHOA HỌC CỐT LÕI (NHÁNH 5)

### 21.1. Mối liên hệ nhân quả giữa Cấu trúc phân bổ trong $S_k$ (Nhánh 5) và Độ phủ nội phân họ (Nhánh 2–4):
* Ở Nhánh 2, Nhánh 3 và Nhánh 4, bộ 9 chỉ số thực nghiệm đo lường độ nhạy và độ bao phủ khi lấy các chuỗi đại diện nội phân họ $S_k \cap V_g$ truy vấn ngược lại vào chính phân họ $V_g$ của nó.
* Để giải thích tận gốc tại sao độ phủ nội phân họ của $\alpha = 0.5$ và $\alpha = 1.0$ lại bứt phá mạnh mẽ so với $\alpha = 0.0$, **Nhánh 5** mổ xẻ trực tiếp cấu trúc phân bổ ghế bên trong danh sách $S_k$ qua 20 mốc ngân sách tiến tới $k = G = 115$: **Trong $k$ ghế đại diện đã được bầu chọn ra, có bao nhiêu phân họ (trên 115 họ) và bao nhiêu phân họ hiếm (trên 45 họ hiếm) thực sự có đại diện trực tiếp ngồi trong $S_k$? Có bao nhiêu phần trăm số ghế bị dùng lặp lại ở cùng một phân họ cũ, và riêng phân họ lớn nhất `A01.009` (Cathepsin D — $329$ chuỗi, gấp $329\times$ họ hiếm $n=1$) chiếm bao nhiêu phần trăm ngân sách?**

### 21.2. Bảng tổng hợp 6 phương pháp được đánh giá trong Nhánh 5:
Tuân thủ nghiêm ngặt nguyên tắc **Cô lập biến số (*Ceteris Paribus*)**, Nhánh 5 đánh giá chính xác **6 phương pháp chọn tập đại diện** ($2 \text{ không gian tương đồng} \times 3 \text{ chế độ trọng số } \alpha$) trên cùng tập dữ liệu chuẩn hóa $V_{\text{curated}} = 4,120$ chuỗi ($115$ phân họ, $45$ họ hiếm) và cùng 20 mốc ngân sách $k \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 20, 25, 30, 40, 50, 60, 75, 115\}$ ($6 \times 20 = 120$ cấu hình thực nghiệm):

| STT | Tên Phương Pháp (`selection_space` + `alpha`) | Không Gian Ma Trận Tương Đồng Đầu Vào | Hàm Mục Tiêu & Trọng Số Mẫu $w_v^{(\alpha)}$ | Thuật Toán Tối Ưu Hóa (`Solver` — Giữ Cố Định 100%) | Tổng Quyền Lực Phân Họ $W_g^{(\alpha)} = \sum_{v \in V_g} w_v^{(\alpha)}$ | Tệp Cache Đồng Thuận Đầu Vào (`outputs/similarity_cache/`) | Vai Trò Đối Chứng Trong Nhánh 5 |
| :-: | :--- | :--- | :---: | :--- | :---: | :--- | :--- |
| **1** | **`BLASTp` ($\alpha = 0.0$)** *(Baseline Unweighted)* | $\mathbf{S}_{\text{BLAST}} \in [0, 1]^{4,120 \times 4,120}$ | Unweighted FL ($w_v = 1.0$) | `Pruned Greedy 90%` (`1,000-Shuffle Consensus`, `prune_threshold = 0.90`, `budget_per_shuffle = 115`, `seed = 42`) | $W_g = n_g$ *(`A01.009` gấp **$329.0\times$** họ hiếm $n=1$)* | `MEROPS_A1A_curated_1000_shuffles_alpha_0.00.npz` | **Mốc đối chứng gốc:** Phơi bày mức độ các phân họ lớn gây dư thừa phân họ và bỏ rơi họ hiếm khi không có trọng số. |
| **2** | **`BLASTp` ($\alpha = 0.5$)** *(Rare-Aware Pareto — Nhánh 2)* | $\mathbf{S}_{\text{BLAST}} \in [0, 1]^{4,120 \times 4,120}$ | Weighted FL ($w_v = n_g^{-0.5}$) | `Pruned Greedy 90%` (`1,000-Shuffle Consensus`, `prune_threshold = 0.90`, `budget_per_shuffle = 115`, `seed = 42`) | $W_g = \sqrt{n_g}$ *(`A01.009` nén xuống **$18.14\times$** họ hiếm)* | `MEROPS_A1A_curated_1000_shuffles_alpha_0.50.npz` | **Cân bằng Pareto trên BLASTp:** Đo hiệu quả giảm trùng lặp phân họ và tăng số họ hiếm có mặt trực tiếp trong $S_k$. |
| **3** | **`BLASTp` ($\alpha = 1.0$)** *(Group-Equitable — Nhánh 2)* | $\mathbf{S}_{\text{BLAST}} \in [0, 1]^{4,120 \times 4,120}$ | Weighted FL ($w_v = n_g^{-1.0}$) | `Pruned Greedy 90%` (`1,000-Shuffle Consensus`, `prune_threshold = 0.90`, `budget_per_shuffle = 115`, `seed = 42`) | $W_g = 1.0$ *(Mọi phân họ bình đẳng **$1:1$**)* | `MEROPS_A1A_curated_1000_shuffles_alpha_1.00.npz` | **Bình đẳng nhóm tuyệt đối trên BLASTp:** Đo giới hạn tối đa số phân họ và họ hiếm được chọn trực tiếp trên BLASTp. |
| **4** | **`ESM-2` ($\alpha = 0.0$)** *(Unweighted ESM-2 — Nhánh 3)* | $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)} \in [0, 1]^{4,120 \times 4,120}$ | Unweighted FL ($w_v = 1.0$) | `Pruned Greedy 90%` (`1,000-Shuffle Consensus`, `prune_threshold = 0.90`, `budget_per_shuffle = 115`, `seed = 42`) | $W_g = n_g$ *(`A01.009` gấp **$329.0\times$** họ hiếm $n=1$)* | `MEROPS_A1A_curated_esm2_1000_shuffles_alpha_0.00.npz` | **Đối chứng không trọng số trên ESM-2:** Chứng minh nếu chỉ đổi sang `ESM-2` mà giữ $\alpha=0.0$, các họ lớn vẫn chiếm phần lớn ghế. |
| **5** | **`ESM-2` ($\alpha = 0.5$)** *(`RareProtSelect` Pareto — Nhánh 3 & 4)* | $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)} \in [0, 1]^{4,120 \times 4,120}$ | Weighted FL ($w_v = n_g^{-0.5}$) | `Pruned Greedy 90%` (`1,000-Shuffle Consensus`, `prune_threshold = 0.90`, `budget_per_shuffle = 115`, `seed = 42`) | $W_g = \sqrt{n_g}$ *(`A01.009` nén xuống **$18.14\times$** họ hiếm)* | `MEROPS_A1A_curated_esm2_1000_shuffles_alpha_0.50.npz` | **Phương pháp đề xuất chủ lực (`RareProtSelect`):** Đánh giá sự kết hợp `ESM-2` ($\beta=0.70$) + trọng số $\alpha=0.5$. |
| **6** | **`ESM-2` ($\alpha = 1.0$)** *(Group-Equitable ESM-2 — Nhánh 3 & 4)* | $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)} \in [0, 1]^{4,120 \times 4,120}$ | Weighted FL ($w_v = n_g^{-1.0}$) | `Pruned Greedy 90%` (`1,000-Shuffle Consensus`, `prune_threshold = 0.90`, `budget_per_shuffle = 115`, `seed = 42`) | $W_g = 1.0$ *(Mọi phân họ bình đẳng **$1:1$**)* | `MEROPS_A1A_curated_esm2_1000_shuffles_alpha_1.00.npz` | **Bình đẳng nhóm tuyệt đối trên ESM-2:** Đo mức độ ưu tiên tối đa cho 45 họ hiếm và 115 phân họ trên không gian ESM-2. |

---

<a id="sec-stage5-cd1"></a>
## 22. CÔNG ĐOẠN 5.1: NẠP HAI BỘ ĐẠI DIỆN ĐỒNG THUẬN CÔ LẬP & ÁNH XẠ PHÂN BỐ 115 PHÂN HỌ MEROPS A1A

1. **Giữ nguyên 100% Ground Set chuẩn hóa $V_{\text{curated}}$**:
   - Tập dữ liệu sạch có nhãn phân họ: $|V| = 4,120$ chuỗi protein thuộc siêu họ Peptidase A1 (`MEROPS_A1A.fasta` sau khi lọc `UPA`).
   - Tổng số phân họ định danh: $G = 115$ phân họ (`75` họ mã số `A01.001`..`A01.971` + `40` họ mã chữ-số `A01.A02`..`A01.P02`).
   - Tập các phân họ hiếm ($n_g \le 5$ chuỗi): $|G_{\text{rare}}| = 45$ phân họ hiếm.
   - Phân họ định danh lớn nhất: `A01.009` (Cathepsin D) chứa $n_{\text{A01.009}} = 329$ chuỗi sạch ($7.99\%$ tập Curated, gấp $329\times$ họ hiếm $n=1$).
2. **Nạp trực tiếp 6 tệp cache danh sách đại diện đồng thuận (`consensus_ids`)**:
   - Không gian `BLASTp` (Nhánh 2): `outputs/similarity_cache/MEROPS_A1A_curated_1000_shuffles_alpha_{0.00, 0.50, 1.00}.npz`.
   - Không gian `ESM-2` (Nhánh 3): `outputs/similarity_cache/MEROPS_A1A_curated_esm2_1000_shuffles_alpha_{0.00, 0.50, 1.00}.npz`.
   - Kiểm tra tính toàn vẹn metadata của từng tệp cache: `budget_per_shuffle >= 115` và `len(consensus_ids) >= 115`.
* 🔗 **Hiện thực hóa tại**: [Kịch bản `experiments/exp5_subfamily_allocation_a1a.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#sec-exp5-script).

---

<a id="sec-stage5-cd2"></a>
## 23. CÔNG ĐOẠN 5.2: ĐO ĐẠC BỘ 4 CHỈ SỐ CẤU TRÚC ĐẠI DIỆN TRỰC TIẾP & ĐỘ DƯ THỪA PHÂN HỌ QUA 20 MỐC NGÂN SÁCH

Tại mỗi tổ hợp $(\text{selection\_space}, \alpha, k)$ trong tổng số $2 \times 3 \times 20 = 120$ cấu hình thực nghiệm, gọi $S_k = \{s_1, \dots, s_k\}$ là tập $k$ chuỗi đại diện đầu tiên trong danh sách đồng thuận:
* Gọi $c_g(S_k) = |S_k \cap V_g|$ là số lượng chuỗi đại diện trong $S_k$ thuộc phân họ $g \in \{1..115\}$ (thỏa mãn $\sum_{g=1}^{115} c_g(S_k) = k$).
* Gọi $\mathcal{G}(S_k) = \{g \in \{1..115\} \mid c_g(S_k) \ge 1\}$ là tập các phân họ phân biệt có ít nhất 1 đại diện trực tiếp trong $S_k$.
* Gọi $\mathcal{G}_{\text{rare}}(S_k) = \{g \in G_{\text{rare}} \mid c_g(S_k) \ge 1\} = \mathcal{G}(S_k) \cap G_{\text{rare}}$ là tập các phân họ hiếm ($n_g \le 5$) có ít nhất 1 đại diện trực tiếp trong $S_k$.

Tính toán chính xác **4 chỉ số tỷ lệ phần trăm (`%`)** đi kèm **4 cột số đếm nguyên (`count`)**:
1. **Tỷ lệ phân họ trên 115 họ có đại diện trực tiếp trong $S_k$ (`subfamily_repr_rate_pct` & `subfamilies_represented_count`)**:
   $$\text{subfamilies\_represented\_count} = |\mathcal{G}(S_k)|, \qquad \operatorname{Subfamily\_Repr}(S_k) = \frac{|\mathcal{G}(S_k)|}{115} \times 100\%$$
2. **Tỷ lệ phân họ hiếm trên 45 họ hiếm ($\le 5$ chuỗi) có đại diện trực tiếp trong $S_k$ (`rare_repr_rate_pct` & `rare_subfamilies_represented_count`)**:
   $$\text{rare\_subfamilies\_represented\_count} = |\mathcal{G}_{\text{rare}}(S_k)|, \qquad \operatorname{Rare\_Repr}(S_k) = \frac{|\mathcal{G}_{\text{rare}}(S_k)|}{45} \times 100\%$$
3. **Độ dư thừa phân bổ phân họ (`subfamily_redundancy_pct` & `redundant_slots_count`)**:
   $$\text{redundant\_slots\_count} = \sum_{g \,:\, c_g(S_k) \ge 2} \left(c_g(S_k) - 1\right) = k - |\mathcal{G}(S_k)|$$
   $$\operatorname{Subfamily\_Redundancy}(S_k) = \frac{\sum_{g \,:\, c_g(S_k) \ge 2} \left(c_g(S_k) - 1\right)}{k} \times 100\% = \frac{k - |\mathcal{G}(S_k)|}{k} \times 100\%$$
4. **Tỷ trọng ngân sách phân bổ cho phân họ lớn nhất `A01.009` (`dominant_a01_009_share_pct` & `dominant_a01_009_count`)**:
   $$\text{dominant\_a01\_009\_count} = c_{\text{A01.009}}(S_k) = |S_k \cap V_{\text{A01.009}}|, \qquad \operatorname{Dominant\_Share}(S_k) = \frac{c_{\text{A01.009}}(S_k)}{k} \times 100\%$$
* 🔗 **Hiện thực hóa tại**: [Kịch bản `experiments/exp5_subfamily_allocation_a1a.py`](./thiet_ke_codebase_va_kien_truc_he_thong.md#sec-exp5-script) (hàm `evaluate_subfamily_allocation_metrics`).

---

<a id="sec-stage5-cd3"></a>
## 24. CÔNG ĐOẠN 5.3: TIÊU CHUẨN NGHIỆM THU TOÁN HỌC BẤT BIẾN & SẢN PHẨM ĐẦU RA BẮT BUỘC (NHÁNH 5)

### 24.1. Tiêu chuẩn nghiệm thu toán học (3 Bất biến Sanity Check bắt buộc):
Trên toàn bộ $120$ dòng dữ liệu thực nghiệm của Nhánh 5, chương trình bắt buộc tự động kiểm định 3 bất biến toán học:
1. **Bất biến bảo toàn tổng số ghế ngân sách $k$**:
   $$\text{subfamilies\_represented\_count} + \text{redundant\_slots\_count} = k, \quad \forall k \in \{1..115\}$$
2. **Bất biến bù $100.0\%$ tại mốc ngân sách đủ $k = G = 115$**:
   $$\operatorname{Subfamily\_Repr}(S_{115}) + \operatorname{Subfamily\_Redundancy}(S_{115}) = 100.0\%$$
3. **Bất biến ràng buộc tập con**:
   $$0 \le \text{rare\_subfamilies\_represented\_count} \le \min\left(45, \; \text{subfamilies\_represented\_count}\right)$$
   $$0 \le \text{dominant\_a01\_009\_count} \le 1 + \text{redundant\_slots\_count}$$

### 24.2. Sản phẩm đầu ra bắt buộc:
1. **Tệp cấu hình**: `configs/config_exp5_subfamily_allocation_a1a.yaml`.
2. **Kịch bản thực thi**: `experiments/exp5_subfamily_allocation_a1a.py`.
3. **Bảng số liệu sạch duy nhất**: `outputs/tables/exp5_subfamily_allocation_a1a.csv` (đúng $2 \times 3 \times 20 = 120$ dòng dữ liệu thực nghiệm và đúng **11 cột**: `selection_space`, `alpha`, `budget_k`, `subfamilies_represented_count`, `subfamily_repr_rate_pct`, `rare_subfamilies_represented_count`, `rare_repr_rate_pct`, `redundant_slots_count`, `subfamily_redundancy_pct`, `dominant_a01_009_count`, `dominant_a01_009_share_pct`).
4. **Hệ thống 2 biểu đồ công bố khoa học** (định dạng `.png` và `.svg`):
   - `outputs/figures/exp5_allocation_metrics_vs_k.png` & `.svg`: Biểu đồ 4 góc ($2 \times 2$) biểu diễn diễn tiến 4 chỉ số tỷ lệ `%` (`subfamily_repr_rate_pct`, `rare_repr_rate_pct`, `subfamily_redundancy_pct`, `dominant_a01_009_share_pct`) theo ngân sách $k \in [1..115]$ giữa `ESM-2 Selected` (nét liền) và `BLASTp Selected` (nét đứt) qua 3 mức $\alpha \in \{0.0, 0.5, 1.0\}$.
   - `outputs/figures/exp5_allocation_summary_k11_k115.png` & `.svg`: Biểu đồ cột ghép đối chiếu trực diện 4 chỉ số tại 2 mốc chiến lược $k = 11$ và $k = 115$ giữa `BLASTp Selected` và `ESM-2 Selected` qua 3 mức $\alpha \in \{0.0, 0.5, 1.0\}$, kèm nhãn số đếm nguyên và tỷ lệ `%` trên đỉnh cột.

---

# PHẦN VI: GIAI ĐOẠN 6 - KHẢO SÁT ĐỘNG HỌC BÃO HÒA PHÂN HỌ LỚN & DẢI NGÂN SÁCH SÂU ($k \in [115..380]$) TRÊN 115 PHÂN HỌ PEPTIDASE A1 (NHÁNH 6)

<a id="sec-stage6-intro"></a>
## 25. ĐẶT VẤN ĐỀ, 6 MỐC NGÂN SÁCH CHUYỂN PHA SÂU & MỤC TIÊU KHOA HỌC CỐT LÕI (NHÁNH 6)

### 25.1. Động lực khoa học từ quan sát Thioesterases (TE) của bài báo nền:
* Trong bài báo gốc (*Nguyen et al., 2025*), khi thực nghiệm trên bộ dữ liệu Thioesterases (TE — 737 chuỗi, 27 họ ThYme), các tác giả đã ghi nhận một số phân họ đa dạng cao cần tới **11 chuỗi đại diện** mới có thể bao phủ hoàn toàn cấu trúc nội họ ($100\%$ within-subfamily sensitivity).
* Trên siêu họ Peptidase A1 (`MEROPS_A1A_curated`: $4,120$ chuỗi sạch, $115$ phân họ định danh), phân họ lớn nhất **`A01.009` (Cathepsin D)** chứa tới **$329$ chuỗi sạch** ($7.99\%$ dữ liệu, gấp $329.0\times$ các phân họ đơn độc $n=1$), cùng với **$38$ phân họ lớn** ($n_g \ge 20$) chiếm đại đa số chuỗi trong siêu họ.
* Ở các Nhánh 1–5, ngân sách tối đa bị chặn tại $k \le G = 115$ (bình quân $1.0$ ghế/phân họ). Tại $k = 115$, thuật toán ưu tiên nhóm hiếm ($\alpha = 0.5$ và $\alpha = 1.0$) đã dành hầu hết số ghế để cứu $45$ phân họ hiếm, khiến `A01.009` chỉ nhận được $1$ ghế duy nhất (độ nhạy nội họ đạt $\approx 64.74\%$).
* Do đó, để trả lời câu hỏi khoa học then chốt: **"Cần thêm bao nhiêu ghế đại diện để các phân họ lớn ($n_g \ge 20$) và phân họ thống trị `A01.009` đạt bão hòa $100.0\%$ độ phủ nội họ?"**, Nhánh 6 thực hiện **Đường đua Ngân sách Sâu (True Deep Budget Track)**, giữ nguyên 100% các kết quả $k \le 115$ của Nhánh 1–5 và zoom trực tiếp vào dải bão hòa sâu $k \in [115..380]$.

### 25.2. Luận cứ toán học xác lập 6 mốc ngân sách chuyển pha chiến lược ($k \in [115, 150, 200, 270, 340, 380]$):
1. **$k = 115$ (Anchor Baseline)**: Mốc neo đối chuẩn chuẩn hóa ($k = G = 115$). Bình quân 1 ghế/phân họ. Tại đây, $\alpha=1.0$ đạt $100.0\%$ phân họ hiếm nhưng các họ lớn thiếu ghế trầm trọng.
2. **$k = 150$ ($\approx 115 + 38 \times 1$)**: Tầng đại diện thứ 2 cho 38 phân họ lớn. Dư $35$ ghế thừa sau khi phủ 115 họ, đủ để cấp ghế thứ 2 cho gần như toàn bộ 38 họ lớn.
3. **$k = 200$ ($\approx 115 + 38 \times 2$)**: Tầng đại diện thứ 3 cho 38 phân họ lớn. Dư $85$ ghế thừa ($85 \approx 38 \times 2.2$), cho phép các họ lớn tích lũy 3 đại diện.
4. **$k = 270$ ($\approx 115 + 32 \times 1 + 38 \times 3$)**: Ngưỡng chuyển tiếp bão hòa cho 32 phân họ trung bình ($6 \le n_g \le 19$) và tầng thứ 4 cho 38 họ lớn.
5. **$k = 340$ ($\approx 115 + 32 \times 2 + 38 \times 4$)**: Ngưỡng cận bão hòa toàn diện, các phân họ trung bình đã bão hòa 100%, các họ lớn đạt tầng đại diện thứ 5.
6. **$k = 380$ ($\approx 115 + 32 \times 2 + 38 \times 5$)**: Ngưỡng bão hòa sâu toàn siêu họ, trong đó `A01.009` tích lũy $8 \dots 11$ ghế đại diện, đối sánh trực tiếp với quan sát 11 đại diện trên TE của bài báo nền.

---

<a id="sec-stage6-cd1"></a>
## 26. CÔNG ĐOẠN 6.1: TỐI ƯU HÓA PRUNED GREEDY 90% (1,000-SHUFFLE, `budget_per_shuffle = 380`) TRÊN CẢ 2 KHÔNG GIAN TƯƠNG ĐỒNG

### 26.1. Nguyên tắc cô lập biến số (*Ceteris Paribus*):
* **Giữ nguyên 100%**: Tập dữ liệu chuẩn hóa Phương án 3B `MEROPS_A1A_curated` ($4,120$ chuỗi, $115$ phân họ định danh, $45$ họ hiếm), 2 ma trận tương đồng đã lưu đệm $\mathbf{S}_{\text{BLAST}}$ và $\mathbf{S}_{\text{ESM}}^{(\beta=0.70)}$, thuật toán `Pruned Greedy 90%` (1,000-Shuffle Consensus Ranking) và 3 mức trọng số $\alpha \in \{0.0, 0.5, 1.0\}$.
* **Biến số độc lập duy nhất thay đổi**: Nâng trần chọn tuần tự từ `budget_per_shuffle = 115` lên **`budget_per_shuffle = 380`** trên GPU PyTorch CUDA để mở rộng bảng xếp hạng đồng thuận sâu tới 380 đại diện.
* Lưu đệm độc lập: `outputs/similarity_cache/MEROPS_A1A_curated_{blastp,esm2}_deep_shuffles_alpha_{alpha:.2f}_b380.npz`.

---

<a id="sec-stage6-cd2"></a>
## 27. CÔNG ĐOẠN 6.2: ĐO ĐẠC HỆ THỐNG 18 CHỈ SỐ PHÂN TẦNG QUY MÔ PHÂN HỌ & ĐỘ BÃO HÒA NỘI PHÂN HỌ QUA 6 MỐC NGÂN SÁCH

Tại mỗi cấu hình $(\text{selection\_space}, \alpha, k)$ trong tổng số $2 \text{ không gian} \times 3 \ \alpha \times 6 \ k = 36$ cấu hình thực nghiệm:
1. **Phân tầng 115 phân họ thành 3 khối quy mô**:
   - **Khối Lớn ($38$ phân họ, $n_g \ge 20$)**: Chiếm $3,334 / 4,120$ chuỗi ($80.9\%$), trong đó `A01.009` ($n=329$) là Holotype lớn nhất.
   - **Khối Trung Bình ($32$ phân họ, $6 \le n_g \le 19$)**: Chiếm $341 / 4,120$ chuỗi ($8.3\%$).
   - **Khối Hiếm ($45$ phân họ, $n_g \le 5$)**: Chiếm $109 / 4,120$ chuỗi ($2.6\%$, gồm 18 singletons $n=1$).
2. **Bộ 18 chỉ số đo đạc phân tầng và bão hòa**:
   - `subfamilies_represented_count` & `subfamily_repr_rate_pct` (/115 phân họ).
   - `redundant_slots_count` & `subfamily_redundancy_pct` (% ghế thừa phục vụ bão hòa nội họ).
   - `dominant_a01_009_seats` & `dominant_a01_009_share_pct` (số ghế và % ngân sách của `A01.009`).
   - `dominant_a01_009_blast_sens_pct` & `dominant_a01_009_esm_cov_pct` (độ phủ nội họ riêng của `A01.009`).
   - `large_subfamilies_mean_blast_sens_pct` & `large_subfamilies_mean_esm_cov_pct` (trung bình 38 họ lớn).
   - `medium_subfamilies_mean_blast_sens_pct` (trung bình 32 họ trung bình).
   - `rare_subfamilies_mean_blast_sens_pct` (trung bình 45 họ hiếm).
   - `full_saturation_count_blast`: Số phân họ đạt đúng $100.0\%$ Live BLASTp Sensitivity (/115).
   - `full_saturation_count_esm`: Số phân họ đạt $\ge 99.5\%$ Within-Subfamily ESM Coverage (/115).
   - `overall_sensitivity_blast_pct`: Độ nhạy Live BLASTp toàn tập curated ($/4,120$).

---

<a id="sec-stage6-cd3"></a>
## 28. CÔNG ĐOẠN 6.3: TIÊU CHUẨN NGHIỆM THU TOÁN HỌC BẤT BIẾN & SẢN PHẨM ĐẦU RA BẮT BUỘC (NHÁNH 6)

### 28.1. Tiêu chuẩn nghiệm thu khoa học:
1. **Bất biến bảo toàn ghế ngân sách**: $\text{subfamilies\_represented\_count} + \text{redundant\_slots\_count} = k, \forall k \in [115..380]$.
2. **Đơn điệu không giảm của số ghế `A01.009`**: Số ghế của `A01.009` và độ nhạy nội họ không giảm khi $k$ tăng từ $115 \to 380$.
3. **Hiện tượng bão hòa đa đại diện**: Chứng minh định lượng tại $k=380$, `A01.009` thu nhận nhiều ghế đại diện (tương thích quy luật $\approx 11$ đại diện trên TE của bài báo gốc).

### 28.2. Sản phẩm đầu ra bắt buộc:
1. **Tệp cấu hình**: `configs/config_exp6_deep_budget_a1a.yaml`.
2. **Kịch bản thực thi**: `experiments/exp6_deep_budget_a1a.py`.
3. **Bảng số liệu sạch duy nhất**: `outputs/tables/exp6_deep_budget_a1a.csv` (đúng 36 dòng thực nghiệm $\times$ 18 cột).
4. **Hệ thống 3 biểu đồ công bố khoa học** (PNG 300 DPI và SVG vector, trục hoành zoom trực diện vào $k \in [115..380]$):
   - `outputs/figures/exp6_dominant_a01_009_saturation_vs_k.png` & `.svg`
   - `outputs/figures/exp6_stratified_coverage_vs_k.png` & `.svg`
   - `outputs/figures/exp6_full_saturation_count_vs_k.png` & `.svg`