# Đề tài 2: Chọn tập protein đại diện có ưu tiên nhóm hiếm bằng tối ưu hóa submodular

## 1. Bài toán, định nghĩa, đầu vào, đầu ra

### 1.1. Bài toán

Một protein family có thể chứa hàng nghìn hoặc hàng triệu sequence. Nhiều
sequence gần như trùng lặp, trong khi một số subfamily, taxon hoặc chức năng
hiếm chỉ có rất ít đại diện. Lưu và phân tích toàn bộ tập sequence làm tăng chi
phí tính toán, annotation và manual curation.

Bài toán là chọn một tập nhỏ các protein sequence đại diện sao cho:

- bao phủ tốt không gian sequence/chức năng của toàn bộ family;
- hạn chế redundancy giữa các sequence được chọn;
- không để các nhóm lớn lấn át subfamily hoặc taxon hiếm;
- giữ khả năng annotation transfer cho sequence chưa được chọn;
- cho phép người dùng kiểm soát trực tiếp kích thước tập đại diện.

Đề tài dùng embedding của protein language model (PLM) thay cho chỉ dựa vào
sequence identity, sau đó dùng weighted facility location để ưu tiên nhóm
hiếm.

### 1.2. Định nghĩa và mô hình toán học

Cho tập protein sequence

\[
V=\{v_1,v_2,\ldots,v_n\}.
\]

Mỗi sequence (v) có:

- chuỗi amino acid;
- embedding (z(v)) sinh bởi PLM pretrained, ví dụ ESM-2;
- nhãn family, subfamily, taxon hoặc functional class nếu có;
- thông tin chất lượng để tiền xử lý như độ dài, ký tự bất thường và mức độ
  đầy đủ của annotation.

Độ tương đồng PLM có thể được định nghĩa bởi

\[
\operatorname{sim}_{PLM}(u,v)
=\max\{0,\cos(z(u),z(v))\}.
\]

Nếu (g(v)) là nhóm của sequence (v), (n_{g(v)}) là số sequence trong
nhóm đó, một trọng số rare-aware đơn giản là

\[
w_v=\frac{1}{\sqrt{n_{g(v)}}}.
\]

Căn bậc hai được dùng thay cho nghịch đảo trực tiếp để tránh cho nhóm rất nhỏ
trọng số quá lớn. Các lựa chọn trọng số khác phải được kiểm tra bằng
sensitivity analysis.

Với tập đại diện (S), hàm mục tiêu weighted facility location là

\[
F(S)=\sum_{v\in V}w_v
\max_{s\in S}\operatorname{sim}_{PLM}(v,s).
\]

Bài toán tối ưu là

\[
\max_{S\subseteq V,\ |S|\leq k}F(S),
\]

trong đó (k) là số protein tối đa được phép đưa vào tập đại diện.

Khi similarity và trọng số không âm, (F) là monotone submodular. Standard
greedy hoặc lazy greedy đạt bảo đảm

\[
F(S_{greedy})\geq(1-1/e)F(S^*).
\]

### 1.3. Đầu vào

- Tập protein sequence dạng FASTA.
- Nhãn protein family và, nếu có, subfamily/taxonomy/function.
- Ngân sách (k), hoặc danh sách các ngân sách cần đánh giá.
- Mô hình PLM pretrained và cách pooling embedding.
- Hàm xác định trọng số rare-aware.

Nếu dữ liệu không có subfamily, có thể dùng taxonomy, functional label hoặc
cluster từ sequence identity làm nhóm đánh giá.

### 1.4. Đầu ra

- Danh sách (k) protein sequence đại diện.
- Sequence ID, group label và marginal gain của từng protein được chọn.
- Overall coverage, macro coverage, worst-group coverage và redundancy.
- Kết quả annotation transfer hoặc nearest-representative classification.
- Thời gian chạy, bộ nhớ và chi phí sinh embedding.

## 2. Paper nền

### 2.1. Paper chính

**Identifying representative sequences of protein families using submodular
optimization**, Nguyen et al., Scientific Reports, 2025.

Tài liệu trong repo:

- `papers/submodular/2025-nguyen-representative-protein-sequences-submodular/summary.md`
- `papers/submodular/2025-nguyen-representative-protein-sequences-submodular/metadata.md`
- `papers/submodular/2025-nguyen-representative-protein-sequences-submodular/paper.pdf`

Paper nghiên cứu bài toán maximum coverage with minimum redundancy, dùng
facility location và greedy/bidirectional greedy để chọn sequence đại diện.
Paper đánh giá trên các family trong ThYme, carboxylesterase và peptidase A1,
đồng thời so sánh với CD-HIT và MMseqs2.

### 2.2. Hạn chế tạo ra hướng phát triển

- Similarity chủ yếu dựa trên sequence similarity/identity truyền thống.
- Các nhóm lớn có thể chi phối giá trị facility location.
- Chưa tối ưu rõ macro hoặc worst-group coverage cho nhóm hiếm.
- Chưa đánh giá đầy đủ PLM embedding trong việc bảo toàn quan hệ chức năng hoặc
  cấu trúc xa.
- Chưa chứng minh tập đại diện giúp annotation transfer cho long-tail groups.

### 2.3. Công trình liên quan cần đọc

Sinh viên phải khảo sát tối thiểu:

- CD-HIT, MMseqs2 và các phương pháp clustering/de-redundancy;
- submodular selection dùng sequence hoặc structural similarity;
- protein language model embedding và remote-homology evaluation;
- weighted taxon/phylogeny representative selection;
- các công trình 2025-2026 về long-tail functional diversity.

Không được tuyên bố đây là công trình đầu tiên dùng trọng số cho nhóm hiếm.
Novelty phải nằm ở sự kết hợp giữa PLM similarity, rare-aware submodular
selection và đánh giá downstream trên protein family mất cân bằng.

Lưu ý: canonical record của paper nền trong repo đang ở tier
`processed-structured`. Công thức, số liệu và guarantee phải được đối chiếu lại
với PDF trước khi đưa vào bản thảo.

## 3. Hướng phát triển

### 3.1. Phương pháp đề xuất

Xây dựng phương pháp tạm gọi **RareProtSelect**:

1. Tiền xử lý và loại sequence lỗi, quá ngắn hoặc có quá nhiều ký tự không xác
   định.
2. Sinh embedding bằng ESM-2 35M hoặc 150M; chưa fine-tune trong giai đoạn đầu.
3. Tính PLM similarity; dùng approximate nearest neighbors nếu không thể lưu
   ma trận đầy đủ.
4. Tính trọng số rare-aware từ subfamily, taxon hoặc functional label.
5. Chạy lazy greedy cho weighted facility location.
6. Trả về tập đại diện và giải thích từng lựa chọn qua marginal coverage.

Phần lý thuyết tối thiểu:

- chứng minh weighted facility location là normalized monotone submodular;
- suy ra bảo đảm (1-1/e) của cardinality greedy;
- phân tích độ phức tạp khi dùng ma trận similarity đầy đủ;
- đề xuất và đánh giá biến thể sparse-kNN để mở rộng quy mô.

### 3.2. Câu hỏi nghiên cứu (Research Questions)

Chuỗi 5 Câu hỏi Nghiên cứu được chuẩn hóa theo nguyên tắc cô lập biến số (*Ceteris Paribus*) và chuỗi nhân quả kế thừa tuần tự ($RQ_1 \to RQ_5$):

- **$RQ_1$ (Baseline Flaw & Phantom Coverage):** *Khi tái hiện phương pháp Unweighted Submodular Facility Location của bài báo nền (Nguyen et al., 2025) trên siêu họ Peptidase A1, hiện tượng "đánh giá chéo phân họ" (cross-subfamily hits) ảnh hưởng như thế nào đến độ phủ thực sự của các phân họ hiếm?* (Tương ứng Nhánh 1 vs Nhánh 2 $\alpha=0.0$).
- **$RQ_2$ (Rare-Aware Weighting on BLASTp):** *Việc đưa hàm trọng số nghịch đảo quy mô phân họ $w_v = (n_g)^{-\alpha}$ vào hàm mục tiêu Facility Location trên ma trận BLASTp có thể giải quyết được sự thiên vị nhóm lớn và phục hồi độ phủ nội phân họ cho nhóm hiếm hay không, và sự đánh đổi (trade-off) với độ phủ toàn cục diễn ra như thế nào?* (Tương ứng Nhánh 2, $\alpha \in \{0.0, 0.5, 1.0\}$).
- **$RQ_3$ (Continuous Semantic Representation):** *Không gian biểu diễn ngữ nghĩa liên tục từ mô hình ngôn ngữ protein ESM-2 (sau khi khử suy biến dị hướng $\beta=0.70$) đem lại lợi thế gì so với ma trận căn chỉnh cục bộ rời rạc BLASTp trong việc duy trì độ bao phủ nội phân họ cho các nhóm hiếm?* (Tương ứng Nhánh 3).
- **$RQ_4$ (Cross-Space Evaluation Robustness):** *Khi thực hiện kiểm tra chéo hai chiều ($2 \times 2$ Cross-Space Evaluation), tập đại diện chọn trong không gian ngữ nghĩa ESM-2 có duy trì được độ nhạy trên mặt trận Live BLASTp truyền thống hay không, và ngược lại?* (Tương ứng Nhánh 4).
- **$RQ_5$ (Allocation Structure & Anti-Monopoly):** *Về mặt cấu trúc phân bổ đại diện trực tiếp trong $S_k$: Thuật toán đề xuất có thực sự tước bỏ sự thâu tóm ghế đại diện của phân họ lớn nhất A01.009 để phân bổ công bằng cho 45 phân họ hiếm hay không, và tỷ lệ dư thừa phân họ (redundancy %) biến thiên như thế nào theo ngân sách $k$?* (Tương ứng Nhánh 5).

### 3.3. Dữ liệu và thực nghiệm

Giai đoạn pilot chọn ba protein family có kích thước và mức mất cân bằng khác
nhau. Ưu tiên family đã được paper 2025 sử dụng để có baseline tái lập. Mỗi
family nên có ít nhất một nhóm lớn và một số nhóm hiếm.

Giai đoạn đầy đủ có thể mở rộng sang:

- ThYme;
- carboxylesterase và peptidase A1;
- Pfam/UniProt family có subfamily hoặc taxonomy label;
- SCOPe/remote-homology benchmark nếu đánh giá structural diversity.

Baselines:

- Random, CD-HIT và MMseqs2;
- k-medoids hoặc farthest-first;
- facility location dùng sequence identity;
- facility location dùng PLM nhưng không rare-aware;
- RareProtSelect đầy đủ.

Ablation bắt buộc:

- ESM-2 35M và 150M;
- không trọng số, inverse-square-root và inverse-frequency weighting;
- cosine PLM similarity và sequence identity;
- nhiều mức ngân sách (k);
- full similarity và sparse-kNN similarity.

### 3.4. Chỉ số đánh giá

- Overall weighted/unweighted coverage;
- macro coverage trung bình qua các nhóm;
- worst-group coverage;
- pairwise redundancy trong tập được chọn;
- tỷ lệ nhóm có ít nhất một đại diện;
- annotation-transfer accuracy, macro-F1 và worst-group F1;
- runtime, peak memory và chi phí sinh embedding.

Không được chỉ báo cáo chính objective mà thuật toán đang tối ưu. Cần ít nhất
một metric downstream độc lập, ví dụ annotation-transfer macro-F1.

### 3.5. Sản phẩm sinh viên phải bàn giao

- Pipeline đọc FASTA, sinh/cache embedding và chọn tập đại diện.
- File cấu hình để thay đổi PLM, family, group label và (k).
- Baseline, ablation và script đánh giá.
- Danh sách sequence được chọn kèm marginal gain và group label.
- Chứng minh tính submodular và phân tích độ phức tạp.
- Báo cáo kỹ thuật hoặc bản thảo paper 6-10 trang.
- Hướng dẫn tái lập và bảng threats to validity.

### 3.6. Tiêu chí go/no-go

Chỉ nên phát triển thành paper nếu:

- macro hoặc worst-group coverage cải thiện trên đa số family;
- overall coverage không giảm đáng kể;
- tập chọn không bị chi phối bởi outlier hoặc sequence lỗi;
- PLM-based selection có lợi so với sequence identity trên ít nhất một metric
  downstream;
- kết quả ổn định trên nhiều mức (k) và không chỉ đúng với một family.

Mức kỳ vọng cho pilot là macro hoặc worst-group coverage tăng khoảng 5%,
overall coverage giảm không quá 1-2%, và downstream macro-F1 không kém hơn
baseline. Đây là tiêu chí quyết định có tiếp tục hay không, không phải kết quả
được phép giả định trong paper.
