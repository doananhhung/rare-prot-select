# CATALOG QUY TẮC R-LOGIC: MẠCH LUẬN CỨ & KẾT LUẬN TỰ CHỨA (SSOT)

Mọi cấu trúc lập luận trong báo cáo LaTeX bắt buộc phải tuân thủ nghiêm ngặt các quy tắc sau:

## 1. R-LOGIC-01: Nguyên tắc kết luận thực nghiệm tự chứa (Self-Contained Conclusions)
- Đoạn văn phân tích sau bảng/hình bắt buộc phải tự chứa, tổng kết trực diện từ chính các con số vừa phân tích trong đoạn đó.
- Tuyệt đối CẤM viết câu kết luận sáo rỗng, tự mâu thuẫn với số liệu trong bảng, hoặc gán ghép vô căn cứ cho bài báo nền đối với các phép đo mà bài báo nền không thực hiện.
- Ví dụ: Trong thử nghiệm 1, bài báo nền của Nguyen et al. (2025) chỉ công bố chỉ số `Overall Sensitivity` trên đồ thị hình 8A; bài báo nền KHÔNG công bố `Rare Sensitivity` hay `Within-Subfamily Coverage` tại thử nghiệm 1. Vì vậy tuyệt đối CẤM viết: *"kết quả này chứng minh bài báo nền bỏ rơi nhóm hiếm tại thử nghiệm 1"*.

## 2. R-LOGIC-02: Cặp dẫn - luận xung quanh bảng biểu và hình vẽ
- Mọi bảng biểu và hình vẽ bắt buộc phải có **Câu dẫn nhập (Lead-in)** trước bảng/hình, giới thiệu mục đích đối sánh (tách riêng thành đoạn độc lập).
- Ngay sau bảng/hình bắt buộc phải có đoạn văn **Phân tích các điểm mốc (Landmarks)**, cực trị và khoảng lệch (Gaps), không được để bảng/hình nằm trơ trọi.

## 3. R-LOGIC-03: Chuẩn xác cấp độ phân loại sinh học (Family vs. Subfamily)
- Phân biệt rạch ròi giữa 2 cấp độ:
  1. **Một họ protein có độ đa dạng cao và phân tách thành nhiều phân họ** (như `Family A1` gồm $115$ `Subfamily` chính thức).
  2. **Các phân họ quy mô lớn bên trong họ đó có mức độ biến dị trình tự nội nhóm rộng** (như `A01.009` gồm $329$ chuỗi) nên đòi hỏi nhiều hơn một chuỗi đại diện để bao phủ hết các nhánh phụ.
- Tuyệt đối CẤM viết gộp sai bản chất sinh học thành *"các phân họ đa dạng cao đòi hỏi nhiều chuỗi đại diện"*.

## 4. R-LOGIC-04: Giải thích cơ chế toán học thuần khiết
- Mọi hành vi chọn chuỗi của giải thuật tham lam phải được giải thích bằng cơ chế cực đại hóa độ tăng cận biên: $\Delta(e \mid S) = F(S \cup \{e\}) - F(S)$.
- Không được dùng các cách nhân hóa xã hội như "được bầu chọn", "giành ghế", "thâu tóm".
