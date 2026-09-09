# GIẢI THÍCH CHI TIẾT CÁC KHÁI NIỆM & CƠ CHẾ HOẠT ĐỘNG
### (Tài liệu Chuyên sâu dành cho Đề tài 2 & Bài báo nền)

> **Điều hướng nhanh**: [Quay lại Tệp Tổng hợp & Bảng so sánh](./doc_hieu_topic2_va_bai_bao_nen.md#bang-so-sanh)

---

<a id="cau-hoi-1-va-2"></a>
## I. GIẢI ĐÁP 2 THẮC MẮC CỐT LÕI VỀ PHƯƠNG PHÁP & ĐÁNH GIÁ

### 1. Tại sao dùng biến thể Lazy Greedy thay vì Standard Greedy? Dùng chung 1 thuật toán có thấy rõ sự vượt trội của hàm mục tiêu mới không?
* **Bản chất toán học quan trọng**: **Lazy Greedy và Standard Greedy cho ra kết quả nghiệm CHÍNH XÁC 100% GIỐNG NHAU** (cùng chọn ra tập các chuỗi $S$ giống hệt nhau với cùng một giá trị hàm mục tiêu). 
  * Lazy Greedy **không phải là một thuật toán đổi bản chất logic tối ưu**, mà là một **kỹ thuật tối ưu hóa cài đặt (Computational Acceleration)** dựa trên Hàng đợi ưu tiên (Max-Heap) và tính chất *Lợi ích biên giảm dần (Submodularity)*.
* **Tại sao bắt buộc phải dùng Lazy Greedy trong thực tế?**:
  * Khi số lượng protein $n = 10,000 - 100,000$ chuỗi, Standard Greedy có độ phức tạp $O(k \cdot n^2)$ sẽ mất nhiều giờ hoặc nhiều ngày để chạy xong.
  * Lazy Greedy cắt giảm 90% – 99% số phép tính thừa, chạy trong vài giây đến vài phút mà **không làm suy giảm bất kỳ 0.001% chất lượng nghiệm nào**.
* **Thực nghiệm chứng minh hàm mục tiêu mới (Ablation Study)**:
  * Khi làm bài báo, chúng ta giữ nguyên cùng 1 thuật toán (chạy Lazy Greedy cho tất cả) và so sánh trực diện:
    $$\text{Unweighted FL (Cũ)} \quad \text{vs.} \quad \text{Weighted FL (Mới)}$$
  * Nhờ nghiệm toán học không đổi, mọi sự cải thiện về độ bao phủ nhóm hiếm đều **100% đến từ Hàm mục tiêu mới và Độ đo tương đồng mới**, hoàn toàn minh bạch và chặt chẽ về mặt khoa học!

---

### 2. Bản chất nhiệm vụ đánh giá của Phương pháp mới trong Bảng so sánh
Đúng như bạn đã nhận định, nhiệm vụ kiểm chứng của đề tài được chia làm 2 tầng rõ rệt:
1. **Đánh giá Nội tại (Intrinsic Ablation - Bóc tách thành phần)**:
   * Chạy đối đầu trực tiếp trên cùng một tập dữ liệu để trả lời:
     * *Độ đo mới (ESM-2) có tốt hơn độ đo cũ (BLAST) khi giữ nguyên hàm mục tiêu?*
     * *Hàm mục tiêu mới (Weighted FL) có cải thiện Macro Coverage và Worst-group Coverage so với hàm cũ (Unweighted FL) khi giữ nguyên độ đo?*
2. **Đánh giá Hạ nguồn (Extrinsic / Downstream Task - Ứng dụng thực tế)**:
   * **Annotation Transfer (Chuyển giao nhãn chức năng)**: Dùng tập đại diện được chọn để gán nhãn chức năng/phân họ cho các chuỗi chưa biết (đo bằng **Macro-F1** và **Worst-group F1**).
   * Điều này chứng minh tập đại diện không chỉ đẹp về mặt điểm số toán học, mà thực sự giúp các nhà sinh học **chú giải chính xác các protein thuộc phân họ hiếm** trong thực tế.

---

<a id="fasta"></a>
## II. GIẢI THÍCH CHI TIẾT 4 KHÁI NIỆM NỀN TẢNG

## 1. ĐỊNH DẠNG FASTA

### a. Khái niệm đơn giản
* **FASTA** là định dạng văn bản (*text*) tiêu chuẩn và phổ biến nhất trong tin sinh học dùng để lưu trữ chuỗi **axit amin của protein**.

### b. Cấu trúc một tệp FASTA
Một chuỗi FASTA luôn bao gồm 2 phần:
1. **Dòng tiêu đề (Header line)**: Bắt đầu bằng dấu lớn hơn (`>`), chứa mã định danh (Protein ID), tên sinh vật, phân họ hoặc thông tin mô tả.
2. **Dòng chuỗi (Sequence lines)**: Các dòng tiếp theo chứa chuỗi ký tự viết tắt của 20 loại axit amin tiêu chuẩn (ví dụ: `M` = Methionine, `A` = Alanine, `K` = Lysine...).

```text
>sp|P32316|TES1_YEAST Acyl-CoA thioesterase 1 OS=Saccharomyces cerevisiae
MPPTLNLQEKQLLAKRRNKLIKKL... (chuỗi axit amin tiếp diễn) ...VKL
```

### c. Vai trò trong bài toán
* Là **dữ liệu đầu vào thô (Raw Input)** của toàn bộ pipeline.
* Trong bài báo nền: FASTA được đưa trực tiếp vào BLAST để đo tỷ lệ phần trăm khớp chữ.
* Trong Topic 2: FASTA được đưa qua mô hình ESM-2 để biến thành các vector số học (Embeddings).

[Quay lại Bảng so sánh](./doc_hieu_topic2_va_bai_bao_nen.md#bang-so-sanh)

---

<a id="esm2-plm"></a>
## 2. ESM-2 PLM (PROTEIN LANGUAGE MODEL)

### a. Khái niệm đơn giản
* **PLM (Protein Language Model)** là mô hình trí tuệ nhân tạo (kiến trúc Transformer tương tự BERT/GPT) được huấn luyện trên **hàng trăm triệu chuỗi protein** trong tự nhiên.
* **ESM-2 (Evolutionary Scale Modeling 2)**: Là mô hình PLM tiên tiến nhất do Meta AI phát triển.

### b. Cách ESM-2 hoạt động (Ẩn dụ câu văn)
* Trong ngôn ngữ tự nhiên: GPT đọc *"Con mèo đang trèo lên ... cây"* và hiểu từ tiếp theo phải là "ngọn" hoặc "cái" nhờ hiểu ngữ pháp và ngữ cảnh.
* Trong sinh học: ESM-2 đọc chuỗi amino acid `M - A - K - ... - V` và học được quy luật gấp cuộn 3D, liên kết hóa lý và vị trí tâm hoạt động sinh học.

```
Chuỗi FASTA (Ký tự thô) ──> [ ESM-2 Transformer ] ──> Vector Embedding z(v)
"MPPTLNLQEK..."                                       [ 0.24, -1.52, 0.88, ..., 0.05 ]
                                                      (Biểu diễn cấu trúc & chức năng 3D)
```

### c. Tại sao Topic 2 lại dùng ESM-2 thay vì BLAST?
* **BLAST (So sánh bề mặt)**: Hai protein có thể có chuỗi ký tự khác nhau nhiều (>70% đột biến) $\rightarrow$ BLAST đáznh giá là không liên quan ($\text{similarity} \approx 0$).
* **ESM-2 (Hiểu bản chất sâu)**: Dù ký tự khác nhau, nhưng vector nhúng $z(v)$ của 2 protein vẫn nằm rất gần nhau trong không gian vector vì chúng có chung cấu trúc 3D và cùng chức năng xúc tác enzyme (**Remote Homology**).

[Quay lại Bảng so sánh](./doc_hieu_topic2_va_bai_bao_nen.md#bang-so-sanh)

---

<a id="facility-location"></a>
## 3. CƠ CHẾ HOẠT ĐỘNG CỦA 2 HÀM MỤC TIÊU KHI KẾT HỢP VỚI GREEDY

<a id="facility-location-unweighted"></a>
<a id="weighted-facility-location"></a>

Để hiểu cách hoạt động và tại sao Hàm mục tiêu mới lại bảo vệ được nhóm hiếm, thầy trò mình cùng xét một **Ví dụ thực tế bằng số** cụ thể:

### VÍ DỤ THỰC TẾ BẰNG SỐ:
Giả sử ta có 1 họ protein gồm **4 chuỗi**: $V = \{v_1, v_2, v_3, v_4\}$.
* **Nhóm 1 (Nhóm lớn - 3 chuỗi)**: $\{v_1, v_2, v_3\} \implies n_1 = 3 \implies \text{Trọng số } w_1 = w_2 = w_3 = \frac{1}{\sqrt{3}} \approx 0.577$.
* **Nhóm 2 (Nhóm hiếm - 1 chuỗi)**: $\{v_4\} \implies n_2 = 1 \implies \text{Trọng số } w_4 = \frac{1}{\sqrt{1}} = 1.0$.

**Ma trận độ tương đồng $\operatorname{sim}(u, v)$ giữa các chuỗi**:
* Các chuỗi trong Nhóm 1 rất giống nhau: $\operatorname{sim}(v_1, v_2) = 0.9$, $\operatorname{sim}(v_1, v_3) = 0.8$, $\operatorname{sim}(v_2, v_3) = 0.85$.
* Chuỗi $v_4$ (nhóm hiếm) rất khác Nhóm 1: $\operatorname{sim}(v_4, v_1) = 0.1$, $\operatorname{sim}(v_4, v_2) = 0.1$, $\operatorname{sim}(v_4, v_3) = 0.1$.
* Độ tương đồng với chính mình: $\operatorname{sim}(v_i, v_i) = 1.0$.

Mục tiêu: Cần chọn ra **$k = 2$ chuỗi đại diện**.

---

### VÒNG LẶP 1 ($k = 1$): Bắt đầu từ tập rỗng $S_0 = \emptyset$

Thuật toán Greedy sẽ tính điểm số đạt được nếu chọn thử từng chuỗi:

| Chuỗi được chọn | Hàm Unweighted FL (Bài báo nền) | Hàm Weighted FL (Đề tài 2) |
| :---: | :--- | :--- |
| **Chọn thử $\{v_1\}$** | $F = \frac{1}{4}(1.0 + 0.9 + 0.8 + 0.1) = \mathbf{0.700}$ | $F = 0.577(1.0 + 0.9 + 0.8) + 1.0(0.1) = \mathbf{1.658}$ |
| **Chọn thử $\{v_2\}$** | $F = \frac{1}{4}(0.9 + 1.0 + 0.85 + 0.1) = 0.712$ | $F = 0.577(0.9 + 1.0 + 0.85) + 1.0(0.1) = 1.687$ |
| **Chọn thử $\{v_4\}$ (Hiếm)** | $F = \frac{1}{4}(0.1 + 0.1 + 0.1 + 1.0) = 0.325$ | $F = 0.577(0.1 + 0.1 + 0.1) + 1.0(1.0) = 1.173$ |

$\implies$ Ở vòng 1, cả 2 phương pháp đều chọn **$v_2$** (hoặc $v_1$) làm đại diện đầu tiên vì nó bao phủ tốt cho số đông ban đầu: $S_1 = \{v_2\}$.

---

### VÒNG LẶP 2 ($k = 2$): Đã có $S_1 = \{v_2\}$, chọn tiếp phần tử thứ hai

Bây giờ ta tính **Marginal Gain (Lợi ích biên)** $\Delta(v \mid S_1)$ khi chọn thêm một chuỗi $v \notin S_1$ vào tập đại diện.

#### Công thức toán học tổng quát của Marginal Gain:
$$\Delta(v \mid S_1) = F(S_1 \cup \{v\}) - F(S_1) = \frac{1}{|V|} \sum_{u \in V} \underbrace{\left[ \max_{s \in S_1 \cup \{v\}} \operatorname{sim}(u, s) - \max_{s \in S_1} \operatorname{sim}(u, s) \right]}_{\text{Mức tăng độ tương đồng của từng chuỗi } u}$$

Với $S_1 = \{v_2\}$, độ tương đồng ban đầu của từng chuỗi $u$ với tập $S_1$ là:
* Chuỗi $v_1$: $\operatorname{sim}(v_1, v_2) = \mathbf{0.90}$
* Chuỗi $v_2$: $\operatorname{sim}(v_2, v_2) = \mathbf{1.00}$
* Chuỗi $v_3$: $\operatorname{sim}(v_3, v_2) = \mathbf{0.85}$
* Chuỗi $v_4$: $\operatorname{sim}(v_4, v_2) = \mathbf{0.10}$
$$\implies F(\{v_2\}) = \frac{1}{4}(0.90 + 1.00 + 0.85 + 0.10) = \frac{2.85}{4} = \mathbf{0.7125}$$

---

#### 1. Tính toán chi tiết với Hàm Unweighted FL (Bài báo nền):

##### A. Trường hợp xét chọn thêm $v_3$ (tập mới $S = \{v_2, v_3\}$):
Ta so sánh độ bao phủ của từng chuỗi $u \in V$ khi có thêm $v_3$:
* Với $u = v_1$: $\max(\operatorname{sim}(v_1, v_2), \operatorname{sim}(v_1, v_3)) = \max(0.9, 0.8) = 0.9 \implies \text{Mức tăng } = 0.9 - 0.9 = \mathbf{0}$
* Với $u = v_2$: $\max(\operatorname{sim}(v_2, v_2), \operatorname{sim}(v_2, v_3)) = \max(1.0, 0.85) = 1.0 \implies \text{Mức tăng } = 1.0 - 1.0 = \mathbf{0}$
* Với $u = v_3$: $\max(\operatorname{sim}(v_3, v_2), \operatorname{sim}(v_3, v_3)) = \max(0.85, 1.0) = 1.0 \implies \text{Mức tăng } = 1.0 - 0.85 = \mathbf{0.15}$
* Với $u = v_4$: $\max(\operatorname{sim}(v_4, v_2), \operatorname{sim}(v_4, v_3)) = \max(0.1, 0.1) = 0.1 \implies \text{Mức tăng } = 0.1 - 0.1 = \mathbf{0}$

$$\Delta(v_3 \mid \{v_2\}) = \frac{1}{4} \Big( \underbrace{0}_{v_1} + \underbrace{0}_{v_2} + \underbrace{0.15}_{v_3} + \underbrace{0}_{v_4} \Big) = \frac{0.15}{4} = \mathbf{0.0375}$$
*(Hoặc tính bằng $F(\{v_2, v_3\}) - F(\{v_2\}) = \frac{0.9 + 1.0 + 1.0 + 0.1}{4} - 0.7125 = 0.75 - 0.7125 = \mathbf{0.0375}$)*

##### B. Trường hợp xét chọn thêm $v_4$ (Hiếm) (tập mới $S = \{v_2, v_4\}$):
Ta so sánh độ bao phủ của từng chuỗi $u \in V$ khi có thêm $v_4$:
* Với $u = v_1$: $\max(\operatorname{sim}(v_1, v_2), \operatorname{sim}(v_1, v_4)) = \max(0.9, 0.1) = 0.9 \implies \text{Mức tăng } = 0.9 - 0.9 = \mathbf{0}$
* Với $u = v_2$: $\max(\operatorname{sim}(v_2, v_2), \operatorname{sim}(v_2, v_4)) = \max(1.0, 0.1) = 1.0 \implies \text{Mức tăng } = 1.0 - 1.0 = \mathbf{0}$
* Với $u = v_3$: $\max(\operatorname{sim}(v_3, v_2), \operatorname{sim}(v_3, v_4)) = \max(0.85, 0.1) = 0.85 \implies \text{Mức tăng } = 0.85 - 0.85 = \mathbf{0}$
* Với $u = v_4$: $\max(\operatorname{sim}(v_4, v_2), \operatorname{sim}(v_4, v_4)) = \max(0.1, 1.0) = 1.0 \implies \text{Mức tăng } = 1.0 - 0.1 = \mathbf{0.90}$

$$\Delta(v_4 \mid \{v_2\}) = \frac{1}{4} \Big( \underbrace{0}_{v_1} + \underbrace{0}_{v_2} + \underbrace{0}_{v_3} + \underbrace{0.90}_{v_4} \Big) = \frac{0.90}{4} = \mathbf{0.2250}$$
*(Hoặc tính bằng $F(\{v_2, v_4\}) - F(\{v_2\}) = \frac{0.9 + 1.0 + 0.85 + 1.0}{4} - 0.7125 = 0.9375 - 0.7125 = \mathbf{0.2250}$)*

---

#### 2. Tính toán chi tiết với Hàm Weighted FL (Topic 2):
$$\Delta(v \mid S_1) = \sum_{u \in V} w_u \cdot \left[ \max_{s \in S_1 \cup \{v\}} \operatorname{sim}(u, s) - \max_{s \in S_1} \operatorname{sim}(u, s) \right]$$

* **Khi chọn thêm $v_3$**: Chỉ có $v_3$ tăng thêm $0.15$, với trọng số $w_3 = 0.577$:
  $$\Delta(v_3) = w_3 \times 0.15 = 0.577 \times 0.15 = \mathbf{0.0865}$$
* **Khi chọn thêm $v_4$ (Hiếm)**: Chỉ có $v_4$ tăng thêm $0.90$, với trọng số $w_4 = 1.0$:
  $$\Delta(v_4) = w_4 \times 0.90 = 1.0 \times 0.90 = \mathbf{0.9000}$$

$\implies \Delta(v_4) = 0.9000$ **lớn gấp hơn 10 lần** so với $\Delta(v_3) = 0.0865$. 
$\implies$ **Thuật toán Weighted Greedy lập tức chọn ngay chuỗi hiếm $v_4$ vào tập đại diện: $S_2 = \{v_2, v_4\}$!**

* **Ý nghĩa cốt lõi**: Trọng số $w_4 = 1.0$ (cao hơn $w_{1,2,3} = 0.577$) đã khuếch đại mức đóng góp của nhóm hiếm, đảm bảo nhóm hiếm không bị bỏ rơi.

---

### PHÂN TÍCH CHUYÊN SÂU: NẾU $n$ RẤT LỚN ($n = 1.000$ CHUỖI), $v_4$ CÓ BỊ LU MỜ KHÔNG?

> **Câu hỏi mấu chốt**: Trong ví dụ trên $n = 4$ thì $v_4$ có Marginal Gain cao ($0.225$). Nhưng nếu họ protein thực tế rất lớn ($n = 1.000$ chuỗi) và cực kỳ mất cân bằng, liệu $v_4$ có bị nhóm lớn "nuốt chửng" không?

#### Giả sử bối cảnh thực tế:
* **Nhóm 1 (Nhóm siêu lớn - 999 chuỗi)**: $\{v_1, v_2, \dots, v_{999}\}$.
* **Nhóm 2 (Nhóm siêu hiếm - 1 chuỗi)**: duy nhất chuỗi $\{v_4\}$.
* Ở vòng 1, đã chọn 1 đại diện $v_1$ cho nhóm lớn.
* Ở vòng 2, ta cân nhắc giữa:
  * **Ứng viên $v_4$ (Hiếm)**: Nếu chọn $v_4$, chỉ riêng 1 mình $v_4$ được tăng độ bao phủ $+0.90$.
  * **Ứng viên $v_{khác}$ (Nhóm lớn)**: Nếu chọn thêm $v_{khác}$ trong nhóm lớn, có **200 chuỗi** trong nhóm lớn được tăng nhẹ độ tương đồng $+0.05$ (từ $0.80 \rightarrow 0.85$).

---

#### 1. Với Hàm Unweighted FL (Bài báo nền) $\rightarrow$ $v_4$ BỊ LU MỜ HOÀN TOÀN:
Điểm Marginal Gain chia đều cho $n = 1.000$:

* **Mức tăng điểm khi chọn chuỗi hiếm $v_4$**:
  $$\Delta(v_4) = \frac{1}{1.000} \Big( 1 \text{ chuỗi} \times 0.90 \Big) = \frac{0.90}{1.000} = \mathbf{0.0009}$$
* **Mức tăng điểm khi chọn thêm chuỗi nhóm lớn $v_{khác}$**:
  $$\Delta(v_{khác}) = \frac{1}{1.000} \Big( 200 \text{ chuỗi} \times 0.05 \Big) = \frac{10.00}{1.000} = \mathbf{0.0100}$$

> **HIỆN TƯỢNG "TÍCH TIỂU THÀNH ĐẠI" CỦA SỐ ĐÔNG**:
> So sánh: $\Delta(v_{khác}) = 0.0100 \gg \Delta(v_4) = 0.0009$ (**lớn hơn gấp 11 lần!**).
> 
> $\implies$ Thuật toán Greedy của bài báo nền sẽ **tiếp tục chọn $v_{khác}$ và bỏ rơi chuỗi hiếm $v_4$**. Chuỗi hiếm hoàn toàn bị "chết chìm trong biển số đông".

---

#### 2. Với Hàm Weighted FL (Đề tài 2) $\rightarrow$ $v_4$ ĐƯỢC CỨU BỞI TRỌNG SỐ RARE-AWARE:
Trọng số nghịch đảo kích thước nhóm:
* Nhóm lớn ($n_1 = 999$): $w_{lớn} = \frac{1}{\sqrt{999}} \approx \mathbf{0.0316}$
* Nhóm hiếm ($n_2 = 1$): $w_{hiếm} = \frac{1}{\sqrt{1}} = \mathbf{1.0000}$ *(Gấp **31.6 lần** trọng số nhóm lớn)*

Tính lại Marginal Gain:
* **Mức tăng điểm khi chọn chuỗi hiếm $v_4$**:
  $$\Delta(v_4) = w_{hiếm} \times 0.90 = 1.0000 \times 0.90 = \mathbf{0.900}$$
* **Mức tăng điểm khi chọn thêm chuỗi nhóm lớn $v_{khác}$**:
  $$\Delta(v_{khác}) = 200 \times w_{lớn} \times 0.05 = 200 \times 0.0316 \times 0.05 = \mathbf{0.316}$$

> **CHIẾN THẮNG CỦA NHÓM HIẾM**:
> So sánh: $\Delta(v_4) = 0.900 \gg \Delta(v_{khác}) = 0.316$ (**lớn hơn gần 3 lần!**).
> 
> $\implies$ **Thuật toán Weighted Greedy dứt khoát chọn ngay chuỗi hiếm $v_4$ vào tập đại diện!** Trọng số $1/\sqrt{n}$ đã đóng vai trò như một **"chiếc loa phóng thanh"** khuếch đại tiếng nói của nhóm hiếm, ngăn chặn hiện tượng bị nhóm lớn áp đảo.

[Quay lại Bảng so sánh](./doc_hieu_topic2_va_bai_bao_nen.md#bang-so-sanh)

---

<a id="greedy-algorithms"></a>
<a id="lazy-greedy"></a>
<a id="standard-greedy"></a>
<a id="bidirectional-greedy"></a>
## 4. GIẢI THÍCH CHI TIẾT THUẬT TOÁN LAZY GREEDY (VÍ DỤ & VÒNG LẶP)

### a. Cơ sở toán học: Tính chất Submodular (Lợi ích biên giảm dần)
Khi tập đại diện $S$ ngày càng lớn lên, mức đóng góp thêm $\Delta(v \mid S)$ của bất kỳ chuỗi $v$ nào chỉ có thể **giảm đi hoặc giữ nguyên, KHÔNG BAO GIỜ TĂNG LÊN**:
$$A \subseteq B \implies \Delta(v \mid A) \ge \Delta(v \mid B)$$

### b. Cách Lazy Greedy sử dụng Max-Heap để tăng tốc
* Thay vì mỗi bước phải tính lại Marginal Gain cho toàn bộ hàng nghìn chuỗi ($O(n)$ phép tính mỗi bước):
* Ta lưu Marginal Gain của các chuỗi trong một **Hàng đợi ưu tiên (Max-Heap)** (phần tử có Gain lớn nhất luôn nằm ở đỉnh).

---

### VÍ DỤ TRIỂN KHAI 1 VÒNG LẶP CỦA LAZY GREEDY:

Giả sử ta đang có 4 ứng viên chưa chọn: $\{A, B, C, D\}$. 
Tập hiện tại đã có 1 phần tử: $S_1$.

* **Trạng thái Max-Heap ban đầu (lưu Gain cũ ước lượng)**:
  1. **Đỉnh Heap**: Chuỗi $A$ (Gain cũ = $0.80$, tính từ vòng trước)
  2. Vị trí 2: Chuỗi $B$ (Gain cũ = $0.75$)
  3. Vị trí 3: Chuỗi $C$ (Gain cũ = $0.60$)
  4. Vị trí 4: Chuỗi $D$ (Gain cũ = $0.40$)

```
          [ ĐỈNH HEAP: Chuỗi A (Gain cũ = 0.80) ]
                     /              \
         [ Chuỗi B (0.75) ]      [ Chuỗi C (0.60) ]
                /
        [ Chuỗi D (0.40) ]
```

#### Các bước thực thi trong 1 vòng lặp:
* **Bước 1**: Lấy phần tử đỉnh heap là **Chuỗi $A$** ra để kiểm tra.
* **Bước 2**: Tính lại Marginal Gain thực tế mới của riêng chuỗi $A$ với tập hiện tại $S_1$:
  * Giả sử tính ra: $\Delta_{new}(A \mid S_1) = \mathbf{0.78}$.
* **Bước 3**: So sánh $\Delta_{new}(A) = 0.78$ với Gain của phần tử đứng thứ 2 trong Heap là **Chuỗi $B$** (đang có Gain cũ là $0.75$):
  * Ta thấy: $0.78 \ge 0.75$.
  * **Lập luận toán học then chốt**: Vì Gain thực tế của $B$ chỉ có thể $\le 0.75$ (do tính chất Submodular không bao giờ tăng), chắc chắn rằng:
    $$\Delta_{new}(A) = 0.78 \ge \Delta_{thực}(B) \ge \Delta_{thực}(C) \ge \Delta_{thực}(D)$$
* **Bước 4 (CHỐT NGAY LẬP TỨC)**:
  * Ta kết luận ngay **Chuỗi $A$ là chuỗi tốt nhất toàn cục** và thêm $A$ vào tập đại diện!
  * **TIẾT KIỆM TÍNH TOÁN**: Ta hoàn toàn **KHÔNG CẦN** tính lại Gain cho chuỗi $B, C, D$.

*(Trong trường hợp nếu $\Delta_{new}(A)$ bị tụt xuống $0.70 < 0.75$, ta chỉ việc cập nhật $A = 0.70$, đẩy $A$ trở lại Heap để nó tự tụt xuống vị trí 2, và lấy $B$ ra kiểm tra tiếp).*

* **Hiệu năng thực tế**: Trên tập dữ liệu $n = 10,000$ protein, ở mỗi bước Greedy thường chỉ cần tính lại 1 đến 3 chuỗi ở đỉnh heap là đã tìm ra chuỗi tối ưu, **bỏ qua 9,997 phép tính ma trận tốn kém** $\rightarrow$ Tốc độ nhanh gấp hàng trăm lần mà kết quả giống Standard Greedy 100%!

[Quay lại Bảng so sánh](./doc_hieu_topic2_va_bai_bao_nen.md#bang-so-sanh)

---

<a id="cac-chi-so-danh-gia-moi"></a>
## III. CHI TIẾT CÁC CHỈ SỐ ĐÁNH GIÁ MỚI & VÍ DỤ TÍNH TOÁN
### (Khung Đánh Giá Đột Phá Cho Dữ Liệu Mất Cân Bằng / Long-Tail Subfamilies)

> **Điều hướng nhanh**: [Quay lại Mục 4 của Tệp Đọc hiểu & Đối chiếu](./doc_hieu_topic2_va_bai_bao_nen.md#phan-b-cac-chi-so-danh-gia-moi)

---

### 📌 BẢNG QUY ƯỚC KÝ HIỆU TOÁN HỌC & SINH HỌC THỐNG NHẤT:
Để đảm bảo tính nhất quán 100% xuyên suốt toàn bộ tài liệu và mã nguồn, các ký hiệu được định nghĩa chuẩn xác như sau:
* **$V = \{v_1, v_2, \dots, v_n\}$**: **Ground Set** — Tập hợp toàn bộ $n$ chuỗi protein của **Một Họ Protein (Protein Family)** đang xét (ví dụ: Họ TE4 có $n=29$, Họ CE có $n=12,277$).
* **$G = \{g_1, g_2, \dots, g_m\}$**: Tập hợp tất cả $m$ **Phân họ (Subfamilies)** hoặc các **Nhóm phân loại/chức năng (Taxon/Functional Groups)** nằm trong họ protein $V$ ($|G| = m$).
* **$g \in G$**: Một **Phân họ (Subfamily)** cụ thể trong tập $G$. Kích thước của phân họ $g$ là $|g| = n_g$ chuỗi ($n_g = |\{v \in V \mid y(v) = g\}|$).
* **$v \in V$**: Một chuỗi protein bất kỳ trong họ.
* **$S \subseteq V$**: Tập các chuỗi protein đại diện được chọn bởi thuật toán ($|S| \le k$).
* **$s \in S$**: Một chuỗi protein đại diện nằm trong tập $S$.
* **$v \in V \setminus S$**: Một chuỗi protein chưa được chọn vào tập đại diện (cần được bao phủ hoặc cần gán nhãn dự đoán).
* **$y(v) \in G$**: Nhãn phân họ thực tế (Ground-truth label) của protein $v$.
* **$\hat{y}(v) \in G$**: Nhãn phân họ dự đoán (Predicted label) của protein $v \in V \setminus S$.

---

<a id="coverage-g"></a>
### 1. CÔNG THỨC VÀ CÁCH TÍNH ĐỘ BAO PHỦ CỦA MỘT PHÂN HỌ $\operatorname{Coverage}(g)$

#### a. Ý nghĩa bản chất
Với một phân họ cụ thể $g \in G$ có quy mô $|g| = n_g$ chuỗi, chỉ số $\operatorname{Coverage}(g)$ đo lường: **"Tập đại diện $S$ được chọn bao phủ được bao nhiêu phần trăm chất lượng/thông tin của riêng phân họ $g$?"**.

#### b. Công thức toán học
1. **Theo độ tương đồng liên tục (Facility Location Coverage - Độ đo chính)**:
   $$\operatorname{Coverage}(g) = \frac{1}{|g|} \sum_{v \in g} \max_{s \in S} \operatorname{sim}_{PLM}(v, s)$$
   * Với mỗi protein $v \in g$, ta tìm đại diện $s \in S$ gần nó nhất trong không gian vector ESM-2 ($\max_{s \in S} \operatorname{sim}(v, s)$).
   * Lấy trung bình cộng mức độ tương đồng này trên toàn bộ $|g|$ chuỗi của nhóm. Giá trị nằm trong khoảng $[0, 1]$ (tương ứng $0\% - 100\%$).
2. **Theo ngưỡng tương đồng (Thresholded / Retrieval Coverage)**:
   $$\operatorname{Coverage}_{\tau}(g) = \frac{|\{v \in g \mid \max_{s \in S} \operatorname{sim}_{PLM}(v, s) \ge \tau\}|}{|g|} \times 100\%$$
   *(Tỷ lệ phần trăm chuỗi trong $g$ có ít nhất 1 đại diện trong $S$ đạt độ tương đồng $\ge \tau$, ví dụ $\tau = 0.6$)*.

---

<a id="macro-coverage"></a>
### 2. CHỈ SỐ MACRO COVERAGE (ĐỘ BAO PHỦ TRUNG BÌNH ĐỀU QUA CÁC PHÂN HỌ)

#### a. Ý nghĩa sinh học & toán học
* Đo lường **mặt bằng chung phân bố qua các phân họ (Balanced Central Tendency)** — gán trọng số bình đẳng $1/|G|$ cho mỗi phân họ (bất kể phân họ đó có nhiều hay ít chuỗi).
* **Vai trò quan trọng**: Phản ánh xu hướng trung tâm công bằng của toàn bộ phổ phân họ, đồng thời làm đối trọng kiểm chứng chất lượng toàn diện (giúp tránh việc đánh giá bị méo mó nếu chỉ dựa vào Worst-case khi gặp phải 1-2 chuỗi rác/outlier).
* **Giới hạn toán học**: Vì là phép tính trung bình cộng $\frac{1}{|G|}$, nếu số lượng phân họ phổ biến quá nhiều so với số phân họ hiếm (ví dụ 18 nhóm lớn vs. 2 nhóm hiếm), điểm Macro Coverage vẫn có thể bị các nhóm lớn làm loãng. Do đó, **Macro Coverage luôn phải đi kèm song song với Worst-Group Coverage** để tạo nên khung đánh giá toàn diện (Macro đo mặt bằng chung, Worst-Group đo cận dưới bảo vệ nhóm hiếm).

#### b. Công thức toán học
$$\text{Macro Coverage} = \frac{1}{|G|} \sum_{g \in G} \operatorname{Coverage}(g) = \frac{\operatorname{Coverage}(g_1) + \operatorname{Coverage}(g_2) + \dots + \operatorname{Coverage}(g_m)}{m}$$

---

<a id="worst-group-coverage"></a>
### 3. CHỈ SỐ WORST-GROUP COVERAGE (ĐỘ BAO PHỦ CỦA NHÓM THIỆT THÒI NHẤT)

#### a. Ý nghĩa sinh học & toán học
* Đo lường **mức độ an toàn tối thiểu (Safety Floor)** — kiểm tra xem phân họ chịu thiệt thòi nhất (nhóm hiếm nhất, xa nhất) đạt độ bao phủ bao nhiêu điểm.
* Nếu chỉ số này bằng $0\%$, nghĩa là hệ thống tồn tại ít nhất một phân họ hoàn toàn bị "mù thông tin".

#### b. Công thức toán học
$$\text{Worst-Group Coverage} = \min_{g \in G} \operatorname{Coverage}(g)$$

---

<a id="rare-group-representation"></a>
### 4. CHỈ SỐ RARE GROUP REPRESENTATION RATE (TỶ LỆ NHÓM HIẾM CÓ ĐẠI DIỆN TRỰC TIẾP)

#### a. Ý nghĩa sinh học & toán học
* Đo lường **tính hiện diện thực thể mẫu vật** — trong số các nhóm hiếm ($G_{rare} \subseteq G$), có bao nhiêu nhóm đã thực sự có ít nhất một chuỗi của chính nó được chọn vào tập đại diện $S$.
* Phục vụ trực tiếp cho các nhà sinh học thực nghiệm trong phòng lab (Wet-lab): Đảm bảo không bị thất thoát mẫu vật của phân họ hiếm khi đem tập $S$ đi giải cấu trúc 3D hoặc tổng hợp enzyme.

#### b. Công thức toán học
$$\text{Rare Group Representation Rate} = \frac{|\{g \in G_{rare} \mid S \cap g \neq \emptyset\}|}{|G_{rare}|} \times 100\%$$

---

<a id="annotation-transfer"></a>
### 5. NHIỆM VỤ HẠ NGUỒN: ANNOTATION TRANSFER (MACRO-F1 & WORST-GROUP F1)

#### a. Ý nghĩa ứng dụng thực tế & Cơ chế 1-NN
Lấy tập đại diện $S$ đã biết nhãn làm "cơ sở tri thức mẫu", dùng thuật toán $1$-Nearest Neighbor ($1$-NN) trong không gian ESM-2 để dự đoán nhãn phân họ $\hat{y}(v)$ cho toàn bộ các chuỗi chưa biết $v \in V \setminus S$:
$$\hat{y}(v) = y\left(\arg\max_{s \in S} \operatorname{sim}_{PLM}(v, s)\right) \quad \forall v \in V \setminus S$$

#### b. Cách tính chi tiết $\operatorname{Precision}_g$, $\operatorname{Recall}_g$ và $F1_g$ cho từng phân họ $g \in G$:
Với mỗi phân họ $g \in G$, ta phân loại các kết quả dự đoán trên tập $V \setminus S$ thành 3 thành phần:
1. **$TP_g$ (True Positives - Đúng đích thực)**: Số chuỗi thực tế thuộc phân họ $g$ và được thuật toán dự đoán chính xác là $g$:
   $$TP_g = |\{v \in V \setminus S \mid y(v) = g \text{ và } \hat{y}(v) = g\}|$$
2. **$FP_g$ (False Positives - Dương tính giả / Bắt nhầm)**: Số chuỗi thực tế KHÔNG thuộc phân họ $g$ nhưng bị thuật toán dự đoán nhầm thành $g$:
   $$FP_g = |\{v \in V \setminus S \mid y(v) \neq g \text{ và } \hat{y}(v) = g\}|$$
3. **$FN_g$ (False Negatives - Âm tính giả / Bỏ sót)**: Số chuỗi thực tế thuộc phân họ $g$ nhưng bị thuật toán dự đoán nhầm sang phân họ khác:
   $$FN_g = |\{v \in V \setminus S \mid y(v) = g \text{ và } \hat{y}(v) \neq g\}|$$

Từ đó, ta tính các chỉ số:
* **Độ chính xác của phân họ $g$ ($\operatorname{Precision}_g$)**:
  $$\operatorname{Precision}_g = \frac{TP_g}{TP_g + FP_g} = \frac{\text{Số chuỗi đoán trúng phân họ } g}{\text{Tổng số chuỗi bị thuật toán gán nhãn là phân họ } g}$$
* **Độ thu hồi của phân họ $g$ ($\operatorname{Recall}_g$)**:
  $$\operatorname{Recall}_g = \frac{TP_g}{TP_g + FN_g} = \frac{\text{Số chuỗi đoán trúng phân họ } g}{\text{Tổng số chuỗi thực tế thuộc phân họ } g \text{ trong } V \setminus S}$$
* **Điểm F1 của phân họ $g$ ($F1_g$)**:
  $$F1_g = 2 \cdot \frac{\operatorname{Precision}_g \cdot \operatorname{Recall}_g}{\operatorname{Precision}_g + \operatorname{Recall}_g}$$
* **Macro-F1 (Trung bình đều qua tất cả các phân họ)**:
  $$\text{Macro-F1} = \frac{1}{|G|} \sum_{g \in G} F1_g$$
* **Worst-Group F1 (F1 của phân họ phân loại kém nhất)**:
  $$\text{Worst-Group F1} = \min_{g \in G} F1_g$$


---

<a id="vi-du-tinh-toan-chi-tiet"></a>
### 6. VÍ DỤ BẰNG SỐ CỤ THỂ TÍNH TOÁN CẢ 4 CHỈ SỐ MỚI

> 🧪 **BỐI CẢNH THỰC NGHIỆM MẪU**:
> Xét họ protein $V$ gồm **100 chuỗi**, phân thành **3 phân họ**:
> * **Nhóm 1 ($g_1$)**: $90$ chuỗi (chiếm $90\%$).
> * **Nhóm 2 ($g_2$)**: $8$ chuỗi (chiếm $8\%$).
> * **Nhóm 3 ($g_3$ - Hiếm)**: $2$ chuỗi $\{v_{99}, v_{100}\}$ (chiếm $2\%$).
>
> 🎯 **Ngân sách chọn**: $k = 3$ chuỗi đại diện.
> * **Thuật toán Cũ (Bài báo nền - Unweighted FL)**: Chọn 3 đại diện đều thuộc $g_1$: $S_{\text{cũ}} = \{v_1, v_2, v_3\} \subset g_1$.
> * **Thuật toán Mới (Đề tài 2 - Rare-Aware WFL)**: Chọn 2 đại diện $g_1$ và 1 đại diện $g_3$: $S_{\text{mới}} = \{v_1, v_2, v_{99}\}$.

#### Bảng so sánh tính toán chi tiết từng chỉ số:

| Chỉ số | Cách tính Thuật toán Cũ ($S_{\text{cũ}}$) | Cách tính Thuật toán Mới ($S_{\text{mới}}$) | Đánh giá & Kết luận |
| :--- | :--- | :--- | :--- |
| **Độ bao phủ từng nhóm** | $\operatorname{Cov}(g_1) = 0.95$<br>$\operatorname{Cov}(g_2) = 0.60$<br>$\operatorname{Cov}(g_3) = \mathbf{0.10}$ *(bỏ rơi)* | $\operatorname{Cov}(g_1) = 0.93$<br>$\operatorname{Cov}(g_2) = 0.60$<br>$\operatorname{Cov}(g_3) = \mathbf{0.98}$ *(phủ trọn vẹn)* | Nhóm hiếm $g_3$ tăng từ $10\% \rightarrow 98\%$ |
| **Overall Coverage** | $\frac{90(0.95) + 8(0.60) + 2(0.10)}{100} = \mathbf{90.50\%}$ | $\frac{90(0.93) + 8(0.60) + 2(0.98)}{100} = \mathbf{90.46\%}$ | Điểm tổng thể **chỉ giảm $0.04\%$** (hoàn hảo) |
| **Macro Coverage** | $\frac{0.95 + 0.60 + 0.10}{3} = \mathbf{55.00\%}$ | $\frac{0.93 + 0.60 + 0.98}{3} = \mathbf{83.67\%}$ | **Tăng vọt $+28.67\%$** nhờ tính công bằng |
| **Worst-Group Coverage** | $\min(0.95, 0.60, 0.10) = \mathbf{10.00\%}$ | $\min(0.93, 0.60, 0.98) = \mathbf{60.00\%}$ | **Tăng vọt $+50.00\%$**, xóa sổ vùng tối dữ liệu |
| **Rare Representation Rate** | Nhóm $g_3$ không có đại diện trong $S \implies \mathbf{0\%}$ | Nhóm $g_3$ có $v_{99} \in S \implies \mathbf{100\%}$ | Giữ được mẫu vật phân họ hiếm cho phòng lab |
| **Annotation Transfer Macro-F1** | Chuỗi $v_{100}$ bị gán nhầm sang $g_1 \implies F1_{g_3} = 0 \implies \mathbf{Macro\text{-}F1 \approx 0.55}$ | Chuỗi $v_{100}$ gán đúng sang $g_3$ nhờ $v_{99} \implies \mathbf{Macro\text{-}F1 \approx 0.88}$ | Tăng độ chính xác chú giải phân họ hiếm |

---

<a id="so-sanh-worst-va-representation"></a>
### 7. PHÂN BIỆT RẠCH RÒI: `Worst-Group Coverage` vs. `Rare Group Representation Rate`

| Tiêu chí | Worst-Group Coverage | Rare Group Representation Rate |
| :--- | :--- | :--- |
| **Bản chất đo lường** | **Độ đo liên tục (Continuous Score)**: Từ $0.0$ đến $1.0$ ($0\% - 100\%$). | **Độ đo nhị phân (Binary Inclusion)**: Có ($1$) hoặc Không ($0$) cho mỗi nhóm. |
| **Câu hỏi cốt lõi** | *"Phân họ chịu thiệt thòi nhất được bao phủ ở **mức độ tương đồng** bao nhiêu điểm?"* | *"Phân họ hiếm có **cá thể nào lọt vào danh sách** đại diện $S$ hay không?"* |
| **Cơ chế phủ sóng** | Cho phép **bao phủ gián tiếp (Proxy Coverage)**: Nhóm $g$ không có đại diện trong $S$, nhưng nhóm lân cận $g'$ có đại diện tương đồng $65\% \implies \operatorname{Coverage}(g) = 65\%$. | Bắt buộc phải là **hiện diện thực thể trực tiếp**: Bắt buộc phải có ít nhất 1 phần tử của $S$ thực sự thuộc nhóm $g$ ($S \cap g \neq \emptyset$). |
| **Ý nghĩa thực tiễn** | **Tìm kiếm cơ sở dữ liệu (Database Search / Retrieval)**: Đảm bảo không góc nào của họ protein bị mù hoàn toàn. | **Bảo tồn mẫu vật phòng lab (Wet-lab Experimental Validation)**: Đảm bảo có mẫu vật thật để đem làm thí nghiệm kết tinh 3D hoặc tổng hợp enzyme. |
| **Ẩn dụ trực quan** | **Đo cường độ sóng điện thoại** tại xã vùng sâu (dù chưa có trạm phát sóng riêng, bắt ké sóng huyện bên vẫn được 2 vạch = $40\%$). | **Kiểm tra xã đó đã có trạm phát sóng riêng hay chưa** (chưa có = $0\%$, đã xây trạm riêng = $100\%$). |

[Quay lại Mục 4 của Tệp Đọc hiểu & Đối chiếu](./doc_hieu_topic2_va_bai_bao_nen.md#phan-b-cac-chi-so-danh-gia-moi)

