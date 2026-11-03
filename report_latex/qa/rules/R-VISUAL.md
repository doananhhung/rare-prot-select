# CATALOG QUY TẮC R-VISUAL: THẨM ĐỊNH THỊ GIÁC & BỐ CỤC TRANG IN PDF (SSOT)

Mọi trang in trong bản PDF xuất bản bắt buộc phải được thẩm định trực quan qua hình ảnh và tuân thủ các quy tắc thẩm mỹ sau:

---

## 1. R-VIS-01: Kỷ luật tràn lề trang (Margin & Overflow Discipline)
- **Ranh giới lề chuẩn (A4)**: Lề trái $3{,}5\text{ cm}$ (đóng gáy), lề phải $2{,}5\text{ cm}$, lề trên $2{,}5\text{ cm}$, lề dưới $2{,}5\text{ cm}$.
- **Quy tắc**: Tuyệt đối KHÔNG có bất kỳ bảng biểu, hình ảnh, khối mã nguồn hay công thức toán học nào bị tràn qua lề phải ($2{,}5\text{ cm}$) hoặc lấn vào mép giấy.
- **Biểu hiện vi phạm**: Chữ hoặc đường kẻ bảng chạm sát mép giấy bên phải, hoặc đè lên số trang / header.
- **Cách khắc phục trong LaTeX**: Sử dụng `\resizebox{\textwidth}{!}{...}` cho bảng rộng, hoặc ngắt dòng công thức toán qua môi trường `align` / `multline`.

---

## 2. R-VIS-02: Vệ sinh khoảng trắng dọc (Vertical Spacing & Gap Hygiene)
- **Quy tắc**: Ngăn chặn triệt để hiện tượng xuất hiện khoảng trống chết lớn ($> 4{,}0\text{ cm}$) ở nửa dưới đáy trang giấy.
- **Nguyên nhân**: Môi trường `figure` hoặc `table` quá lớn bị đẩy sang trang sau do thiếu khoảng trống, khiến phần đáy trang trước bị bỏ trống bất thường.
- **Cách khắc phục trong LaTeX**: Điều chỉnh kích thước hình `width=0.85\textwidth`, sử dụng tham số vị trí linh hoạt `[htbp!]`, kết hợp lệnh `\FloatBarrier` (gói `placeins`) tại ranh giới mục thay vì lạm dụng `[H]`.

---

## 3. R-VIS-03: Tính kết dính môi trường trôi dạt (Float & Caption Cohesion)
- **Quy tắc**: Hình vẽ/bảng biểu và chú thích `\caption{...}` bắt buộc phải nằm trọn vẹn trên cùng một trang giấy.
- **Biểu hiện vi phạm**: Hình ảnh nằm ở đáy trang trước nhưng dòng `\caption` bị rớt sang đầu trang sau, hoặc ngược lại.
- **Cách khắc phục trong LaTeX**: Thu nhỏ ảnh vừa vặn hoặc chèn lệnh ngắt trang hợp lý `\clearpage` / `\FloatBarrier`.

---

## 4. R-VIS-04: Chống mồ côi tiêu đề, dòng & từ (Headings, Widows & Orphans)
- **Mồ côi tiêu đề mục (Heading Isolation)**: Tuyệt đối CẤM để tiêu đề mục (`\section`, `\subsection`) nằm cô độc ở 1–3 dòng cuối cùng của đáy trang mà không có ít nhất 2 dòng văn bản đi kèm bên dưới.
- **Mồ côi dòng đơn lẻ (Widows/Orphans)**: Không để 1 dòng cuối đoạn văn bị đẩy sang đầu trang mới, hoặc 1 dòng đầu đoạn văn rớt lại đáy trang trước (bảo đảm qua `\widowpenalty=10000`, `\clubpenalty=10000`).
- **Mồ côi từ đơn lẻ (Orphan Words)**: Tránh hiện tượng dòng cuối cùng của một đoạn văn chỉ chứa đúng một từ ngắn đơn độc (ví dụ: "chúng.", "được.").
- **Cách khắc phục trong LaTeX**: Dùng dấu ngã `~` gắn kết từ cuối với từ liền trước, hoặc tinh chỉnh câu văn bằng cách viết gọn lại.

---

## 5. R-VIS-05: Đồng nhất phông chữ & Khử đứt gãy thị giác (Font Consistency)
- **Phông chữ chính**: 100% văn xuôi hiển thị bằng phông **Times New Roman** trang nhã, sắc nét.
- **Cấm hoàn toàn lệnh `\texttt` trong văn xuôi**: Tuyệt đối CẤM sử dụng lệnh `\texttt` trong các đoạn văn xuôi thân bài; mọi tên tệp, tên thư mục, biến số trong văn bản bắt buộc phải hiển thị bằng phông Times New Roman đậm `\textbf{...}` hoặc đặt trong dấu ngoặc kép, tránh việc chuyển đổi phông sang Consolas gây đứt gãy thị giác.
- **Cấm số 0 gạch chéo trong văn xuôi**: Tuyệt đối không để lọt phông `Consolas` có ký tự số 0 gạch chéo (`0` *slashed-zero*) vào tên tệp dữ liệu, nhãn Subfamily hay văn bản thân bài.
- **Công thức toán**: Ký hiệu toán học hiển thị chuẩn xác, không bị đứt gãy nét chữ, không bị lệch cỡ chữ to/nhỏ bất thường so với dòng văn xuôi xung quanh.
- **Số thập phân**: Dấu phẩy ngăn cách thập phân không bị hở khoảng trắng rộng (phải bọc đúng `{,}` trong mã nguồn).

---

## 6. R-VIS-06: Chuẩn mực thụt lề đầu dòng (Paragraph Indentation Hygiene)
- **Đoạn văn đầu tiên sau mọi tiêu đề mục**: Bắt đầu sát lề trái, **TUYỆT ĐỐI KHÔNG lùi đầu dòng ($0\text{ cm}$)**.
- **Các đoạn văn thứ hai trở đi**: Thụt lề đầu dòng đúng chuẩn $1{,}0\text{ cm}$.
- **Khoảng cách giữa các đoạn**: Cách nhau nhẹ nhàng $2{,}5\text{ pt}$, không tạo các rãnh trắng cách dòng quá thưa thớt như văn bản hành chính Word thông thường.

---

## 7. R-VIS-07: Cô lập tiêu đề đầu trang trên phần mở đầu (Frontmatter Header & Layout Discipline)
- **Cấm Running Header trên Frontmatter**: Toàn bộ các trang thuộc phần mở đầu (Bìa, Phiếu nhận xét, Lời cảm ơn, Mục lục, Danh mục bảng biểu, Danh mục hình ảnh) **TUYỆT ĐỐI KHÔNG CÓ TIÊU ĐỀ ĐẦU TRANG (RUNNING HEADER)** và đường kẻ phân cách header (`headrulewidth = 0pt`).
- **Khởi đầu Running Header**: Tiêu đề đầu trang (`fancyhead`) và số trang Ả Rập (`pagenumbering{arabic}`) CHỈ ĐƯỢC PHÉP bắt đầu xuất hiện kể từ trang đầu tiên của **Chương 1** (Thân bài).
- **Chuẩn hóa trang Phiếu nhận xét (Review Form)**: Bắt buộc tuân thủ mẫu gốc của Trường (`Báo-cáo-thực-tập-CN.pdf`): Tiêu đề in hoa đậm căn giữa `NHẬN XÉT BÁO CÁO THỰC TẬP CÔNG NGHIỆP`, thân trang gồm các dòng chấm (`\dotfill`) cách đều trải trọn vẹn trong đúng 1 trang duy nhất, tuyệt đối không tự ý chia nhỏ mục con phân mảnh hay để văng chữ ký sang trang sau.

---

## 8. R-VIS-08: Tiêu chuẩn thẩm định đối chiếu 1:1 với mẫu chuẩn Báo cáo Thực tập Công nghiệp (Báo-cáo-thực-tập-CN.pdf)
Tác tử `latex-visual-inspector` bắt buộc phải kiểm tra bộ 10 tiêu chí đối chiếu thị giác sau đây trên các trang ảnh PNG được xuất từ `pdftoppm`:
1. **Tiêu đề đầu trang (Running Header)**: 100% các trang sạch hoàn toàn ở đỉnh trang, không có chữ chạy và không có đường kẻ ngang $0{,}4\text{ pt}$.
2. **Số trang Frontmatter**: Không hiển thị số trang La Mã hay bất kỳ số trang nào trên các trang mở đầu (Bìa, Nhận xét, Cảm ơn, Mục lục, Danh mục).
3. **Trang bìa (Cover)**: 
   - Tiêu đề loại báo cáo `BÁO CÁO THỰC TẬP CÔNG NGHIỆP` **BẮT BUỘC nằm trên đúng 1 dòng duy nhất**, tuyệt đối CẤM để cỡ chữ quá lớn gây ngắt dòng bẻ đôi thành 2 hàng.
   - Nhãn `Sinh viên:` (không phải `Sinh viên thực hiện:`), ghép đôi hàng MSSV/Khóa, Ngành/Hệ, tiêu đề `TÊN ĐỀ TÀI` không có dấu hai chấm `:`, năm dạng `Hà Nội – Năm 2026`.
4. **Phiếu nhận xét**: Chiếm đúng 1 trang nguyên vẹn, không có dòng mục trong Mục lục.
5. **Lời cảm ơn**: Tiêu đề in hoa đậm căn giữa, khối ký tên bên phải dùng từ `Ký tên`, không có dòng mục trong Mục lục.
6. **Mục lục**: Tiêu đề căn giữa `MỤC LỤC`, format chương `CHƯƠNG I: <TÊN CHƯƠNG>`, không chứa Phiếu nhận xét và Lời cảm ơn.
7. **Danh mục Bảng & Hình**: Đặt chung trên 1 trang duy nhất, không tách rời làm phát sinh trang giấy trắng thừa $> 50\%$.
8. **Tiêu đề Chương**: Số La Mã in hoa: `CHƯƠNG I:`, `CHƯƠNG II:`, v.v.
9. **Tiêu đề Mục & Tiểu mục**: Có dấu chấm đuôi (`1.1.`, `2.2.1.`), tiểu mục in nghiêng `\textit{...}`.
10. **Đánh số Bảng & Hình**: Đánh số toàn cục tăng dần liên tục: `Bảng 1:`, `Bảng 2:`, `Hình 1:`, `Hình 2:`, v.v. (không phụ thuộc số chương). Danh sách liệt kê bắt buộc dùng dấu gạch nối đơn `-`.

---

## 9. R-VIS-09: Bố cục dòng & Tính toàn vẹn ngữ nghĩa Trang bìa (Cover Line & Semantic Integrity)
1. **Dòng Loại Báo Cáo (1 Hàng Ngang Bắt Buộc & Lớn Nhất Trang Bìa)**:
   - Cụm từ `BÁO CÁO THỰC TẬP CÔNG NGHIỆP` phải hiển thị trọn vẹn trên đúng một hàng ngang.
   - Cỡ chữ chuẩn mực là **$19\text{ pt}$** (`\fontsize{19pt}{23pt}\selectfont\textbf{...}`): vừa bảo đảm là tiêu đề to nhất trang bìa (khớp bản mẫu trường), vừa bảo đảm chiều rộng văn bản $\approx 12{,}3\text{ cm}$, nằm lọt hoàn toàn trong khung viền đôi $\approx 14{,}4\text{ cm}$. Tuyệt đối CẤM dùng `\huge` ($24{,}88\text{ pt}$) gây tràn lề bẻ đôi (`CÔNG \n NGHIỆP`) và CẤM hạ quá nhỏ xuống $16\text{ pt}$ làm mất tính chủ đạo của loại báo cáo.
2. **Quy tắc ngắt dòng theo cụm từ có nghĩa (Semantic Chunking)**:
   - Tiêu đề đề tài nghiên cứu chỉ được ngắt dòng tại các ranh giới ngữ nghĩa tự nhiên của cụm từ tiếng Việt.
   - Tuyệt đối CẤM để mồ côi một từ đơn lẻ (như "SUBMODULAR", "PROTEIN") rơi xuống một dòng riêng.
3. **Quy chuẩn đối soát đếm dòng 6 khối trên Trang bìa**:
   - Khối 1 (Tên cơ quan): Đúng 2 dòng (`BỘ GIÁO DỤC VÀ ĐÀO TẠO` / `ĐẠI HỌC PHENIKAA`).
   - Khối 2 (Logo): Đúng 1 ảnh logo căn giữa.
   - Khối 3 (Loại báo cáo): Đúng 1 dòng (`BÁO CÁO THỰC TẬP CÔNG NGHIỆP`), cỡ chữ $19\text{ pt}$.
   - Khối 4 (Nhãn): Đúng 1 dòng (`TÊN ĐỀ TÀI`, không dấu hai chấm `:`), cỡ chữ $13\text{ pt}$.
   - Khối 5 (Tên đề tài): Căn giữa, ngắt dòng ngữ nghĩa cân đối, cỡ chữ $15\text{ pt}$.
   - Khối 6 (Thông tin sinh viên & Năm): Đúng 5 hàng bảng ghép đôi và 1 dòng năm `Hà Nội – Năm 2026`, cỡ chữ $12\text{ pt}$.

---

## 10. R-VIS-10: Quy chuẩn Thứ bậc Thị giác Cỡ chữ Trang bìa (Cover Font Size Hierarchy)
Tác tử `latex-visual-inspector` bắt buộc phải thẩm định tỷ lệ kích thước phông chữ giữa các khối trên trang bìa để bảo đảm chuẩn mực thẩm mỹ:
$$\text{Size}(\text{BÁO CÁO THỰC TẬP CÔNG NGHIỆP}) > \text{Size}(\text{Tên đề tài nghiên cứu}) > \text{Size}(\text{TÊN ĐỀ TÀI}) \ge \text{Size}(\text{Khối sinh viên})$$
Cụ thể theo bảng thông số cố định:
- `BÁO CÁO THỰC TẬP CÔNG NGHIỆP`: **$19\text{ pt}$** (Dòng to nhất trang bìa, 1 dòng).
- Tên đề tài nghiên cứu: **$15\text{ pt}$** (Nhỏ hơn Báo cáo, 3 dòng ngữ nghĩa).
- `TÊN ĐỀ TÀI`: **$13\text{ pt}$** (Nhãn phụ, nhỏ hơn tên đề tài).
- Khối sinh viên và năm: **$12\text{ pt}$** (Nội dung hành chính).
Nếu phát hiện dòng Báo cáo nhỏ hơn hoặc bằng dòng Tên đề tài $\to$ **BẮT BUỘC ĐÁNH CỜ FAIL NGAY LẬP TỨC**.

---

## 11. R-VIS-11: Kỷ luật Chống Mồ côi Dòng & Từ (Widow & Orphan Lines / Words)
- **Mồ côi trong ô Bảng (Table Cell Orphans)**: Tuyệt đối CẤM để 1 hoặc 2 từ đơn lẻ (như "biểu đồ.", "thực tập.", "nghiên cứu.") bị ngắt dòng rơi xuống đứng trơ trọi một mình ở dòng cuối của ô bảng (đặc biệt tại Bảng 1 và Bảng 2).
  * *Biện pháp*: Bắt buộc dùng dấu ngã `~` liên kết các từ cuối (ví dụ `biểu~đồ.`, `báo~cáo~thực~tập.`), đồng thời căn chỉnh hợp lý độ rộng cột `tabularx` để văn bản trải đều.
- **Mồ côi cuối đoạn văn (Paragraph Tail Orphans)**: Dòng cuối cùng của đoạn văn bắt buộc phải có độ dài tối thiểu từ $3$ từ trở lên hoặc chiếm ít nhất $25\%$ chiều rộng dòng, tuyệt đối không để rớt 1 từ cụt lủn.
- **Mồ côi đầu trang (Widow Lines)**: Tuyệt đối CẤM để 1 dòng đơn lẻ bị đẩy sang đầu trang mới một mình.

---

## 12. R-VIS-12: Kỷ luật Dấu Gạch Nối Đơn (Single Hyphen Discipline)
- **CẤM TUYỆT ĐỐI DẤU GẠCH NGANG EN-DASH (`--`)**: Trong toàn bộ văn bản tiếng Việt, bảng biểu, tài liệu tham khảo và môi trường danh sách liệt kê `itemize`, **CẤM TUYỆT ĐỐI** sử dụng chuỗi ký tự `--` làm dấu gạch ngang.
- **BẮT BUỘC DÙNG DẤU GẠCH NỐI ĐƠN (`-`)**: Mọi gạch đầu dòng, dấu nối khoảng ngày tháng (ví dụ: `01/09 - 07/09`), phạm vi tuần (ví dụ: `Tuần 2 - 3`) hoặc dấu phân cách bắt buộc sử dụng đúng một dấu gạch nối đơn `-`. Cấu hình `\setlist[itemize]{label={-}}` trong `main.tex`.

---

## 13. R-VIS-13: Thứ Bậc Cỡ Chữ Tiêu Đề Chương (Chapter Heading Font Size)
- **Cỡ chữ tiêu đề chương chuẩn mực**: Tiêu đề chương `\titleformat{\chapter}` bắt buộc định dạng bằng `\large\bfseries` (14.4pt), tuyệt đối CẤM sử dụng `\Large` (17.28pt) hay `\huge` khiến tiêu đề chương bị quá khổ, mất cân đối so với mẫu báo cáo thực tập chuẩn của trường (`Báo-cáo-thực-tập-CN.pdf`).

---

## 14. R-VIS-14: Kỷ luật Chống Mồ Côi Dòng & Từ Trong Danh Mục Hình Ảnh & Bảng Biểu (LOF/LOT Orphan Discipline)
- **Quy tắc bắt buộc trên Trang Danh mục (List of Figures & List of Tables)**: 
  * Tuyệt đối CẤM để xảy ra hiện tượng mồ côi từ / mồ côi dòng (runt / orphan word): Dòng thứ hai của một mục hình hoặc bảng chỉ chứa duy nhất một từ ngắn đơn độc đứng trước dải dấu chấm liên kết trang (ví dụ: `ORlab. . . . . . 1`).
  * Mọi mục hình ảnh và bảng biểu trong `main.lof` và `main.lot` phải hiển thị trọn vẹn trên đúng 1 dòng duy nhất, HOẶC nếu xuống dòng thì dòng thứ hai phải chứa cụm từ cân đối tối thiểu từ 3-4 từ trở lên.
  * **Biện pháp trong LaTeX**: Khi tiêu đề caption dài, BẮT BUỘC sử dụng tham số tùy chọn rút gọn của lệnh caption: `\caption[Tiêu đề ngắn gọn hiển thị trong LOF/LOT]{Tiêu đề đầy đủ hiển thị trong thân bài.}`.

---

## 15. R-VIS-15: Kỷ luật Chống Tràn Lẻ Tẻ & Trang Chết Cuối Chương (Tail Spillover & Dead Page Discipline)
- **Quy tắc**: Tuyệt đối CẤM để một chương kết thúc bằng việc đẩy một mẩu nhỏ (1–5 dòng văn bản hoặc 2–3 gạch đầu dòng itemize) sang trang mới rồi bỏ trống hơn $40\%$ diện tích phần còn lại của trang đó.
- **Biện pháp trong LaTeX**: Bắt buộc co giãn cục bộ (thu nhỏ nhẹ ảnh float, giảm khoảng đệm `\vspace`, tinh chỉnh độ dài câu chữ) để dồn trọn vẹn phần đuôi về trang trước. Trang cuối cùng của mỗi chương phải được lấp đầy tối thiểu $60\%$ diện tích văn bản.

---

## 16. R-VIS-16: Kỷ luật Kết Dính Danh Mục Liệt Kê & Tiêu Đề Mục (List & Heading Cohesion)
- **Quy tắc**: Tiêu đề mục con (`\subsection`) và câu dẫn nhập TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP bị ngắt trang tách rời khỏi danh sách liệt kê (`itemize`/`enumerate`) đi kèm.
- **Yêu cầu bắt buộc**: Phải có ít nhất 2 mục danh sách đi liền với tiêu đề trên cùng một trang giấy, hoặc đẩy toàn bộ khối sang trang tiếp theo.

---

## 17. R-VIS-17: Kỷ luật Ô Bảng & Cấm Dấu Nối Rớt Dòng (Table Cell Wrapping & Dangling Hyphen)
- **Quy tắc**: Trong mọi ô bảng (Bảng 1, Bảng 2, Bảng 3), CẤM TUYỆT ĐỐI việc ngắt dòng để lại dấu gạch nối `-` đứng ở đầu dòng tiếp theo (ví dụ: `08/09` \n `- 21/09`).
- **Yêu cầu bắt buộc**: Mọi khoảng thời gian hoặc dải giá trị phải nằm trên đúng 1 dòng ngang duy nhất, hoặc ngắt dòng ngữ nghĩa sạch sẽ (`Tuần 2 - 3:` trên dòng 1, `08/09 - 21/09` trên dòng 2).

---

## 18. R-VIS-18: Kỷ luật Tách Khối Sau Danh Mục Liệt Kê (Post-List Paragraph Hygiene)
- **Quy tắc**: Sau mọi môi trường danh sách liệt kê `enumerate` hoặc `itemize`, đoạn văn xuôi tiếp theo bắt buộc phải có khoảng đệm phân cách dọc rõ ràng (`\vspace{6pt}`) và thụt đầu dòng chuẩn $1{,}0\text{ cm}$ để tách bạch hoàn toàn với khối danh sách phía trên, tránh gây cảm giác đoạn văn bị dính chặt hoặc là mẩu con của mục cuối.

