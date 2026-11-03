# QUY CHUẨN SOẠN THẢO BÁO CÁO LATEX ĐỒ ÁN LIÊN NGÀNH (GEMINI.MD)
## Đề tài 2: Chọn tập protein đại diện có ưu tiên nhóm hiếm bằng tối ưu hóa submodular (RareProtSelect)

Tài liệu này là **Nguồn Sự Thật Duy Nhất (SSOT)** chi phối 100% mã nguồn LaTeX, phong cách học thuật, cấu trúc văn bản, công thức toán học và bảng biểu thực nghiệm trong thư mục [`report_latex/`](./). Mọi lượt soạn thảo, cập nhật nội dung các chương hoặc tinh chỉnh định dạng bắt buộc phải tuân thủ nghiêm ngặt các nguyên tắc dưới đây.

---

## 1. QUY TẮC ĐỊNH DẠNG ĐOẠN VĂN & THỤT LỀ (INDENTATION & TYPOGRAPHY)

1. **Quy tắc đoạn văn đầu tiên sau tiêu đề mục (First Paragraph Rule - BẮT BUỘC):**
   - Đoạn văn đầu tiên nằm ngay sau mọi tiêu đề mục (`\chapter`, `\section`, `\subsection`, `\subsubsection`...) **TUYỆT ĐỐI KHÔNG lùi đầu dòng (không thụt lề / `no indent`)**. Đoạn này phải luôn bắt đầu sát lề trái.
   - **CẤM NẠP GÓI `indentfirst`:** Tuyệt đối không nạp `\usepackage{indentfirst}` vào preamble. Giữ nguyên hành vi mặc định của LaTeX (`@afterindentfalse`).
   - Chỉ các đoạn văn thứ hai trở đi trong cùng một mục mới được tự động thụt lề đầu dòng $1{,}0\text{ cm}$ theo thiết lập `\setlength{\parindent}{1.0cm}`.

2. **Khoảng cách, cỡ chữ và căn lề trang chuẩn mực:**
   - **Cỡ chữ**: Chuẩn $12\text{ pt}$ thiết lập qua `\documentclass[12pt,a4paper]{report}` (chuẩn mực cho đồ án kỹ thuật và luận văn, giúp văn bản trang nhã và bảng biểu không bị tràn lề).
   - **Giãn dòng**: Chuẩn $1{,}3$ qua gói `setspace` (`\usepackage{setspace}` kèm `\setstretch{1.3}`).
   - **Khoảng cách giữa các đoạn văn**: $2{,}5\text{ pt}$ (`\setlength{\parskip}{2.5pt}`).
   - **Căn lề trang giấy (chuẩn A4)**:
     - Lề trái (*Left*): $3{,}5\text{ cm}$ (dành khoảng trống đóng gáy đồ án).
     - Lề phải (*Right*): $2{,}5\text{ cm}$.
     - Lề trên (*Top*): $2{,}5\text{ cm}$.
     - Lề dưới (*Bottom*): $2{,}5\text{ cm}$.
     - Thiết lập chuẩn qua `geometry`: `\usepackage[top=2.5cm, bottom=2.5cm, left=3.5cm, right=2.5cm]{geometry}`.

3. **Chống mồ côi dòng và từ đơn lẻ (No Widows, Orphans & No Orphan Words):**
   - Đảm bảo tiêu đề mục vừa vặn trên 1 dòng, không để rớt 1 từ đơn lẻ xuống dòng thứ hai.
   - Ngăn chặn triệt để hiện tượng 1 dòng đơn lẻ bị đẩy sang đầu trang mới hoặc rớt lại cuối trang bằng thiết lập chống mồ côi dòng trong preamble:
     ```latex
     \widowpenalty=10000
     \clubpenalty=10000
     ```

4. **Quy chuẩn định dạng tiêu đề chương tối giản một dòng (One-Line Minimalist Chapter Styling):**
   - Không dùng chữ "CHƯƠNG" cồng kềnh, đưa số thứ tự và tên chương lên cùng một hàng ngang: `\thechapter.\quad <Tên chương>`.
   - Đối với các phần không đánh số (`\chapter*` như Mở đầu, Tài liệu tham khảo): In hoa đậm trực tiếp tên phần `\Large\bfseries`.
   - Triệt tiêu hoàn toàn khoảng trắng thừa của LaTeX và phần đệm `\headsep`, thiết lập khoảng cách trên `-30pt` (kéo sát cách đường kẻ Header $\approx 0{,}8\text{ cm}$) và khoảng cách dưới $15\text{ pt}$ qua gói `titlesec`:
     ```latex
     \titleformat{\chapter}[hang]{\normalfont\Large\bfseries}{\thechapter.\quad}{0pt}{}
     \titlespacing*{\chapter}{0pt}{-30pt}{15pt}
     ```
   - Định dạng phân cấp tương thích cho `\section` (`\large\bfseries`, cách trên $12\text{ pt}$, cách dưới $6\text{ pt}$) và `\subsection` (`\normalsize\bfseries`, cách trên $10\text{ pt}$, cách dưới $4\text{ pt}$).

---

## 2. CẤU TRÚC PREAMBLE & MÔI TRƯỜNG BIÊN DỊCH XELATEX

1. **Trình biên dịch & Phông chữ hệ thống:**
   - Biên dịch độc quyền bằng **`XeLaTeX`** (trên VS Code LaTeX Workshop, MiKTeX, TeX Live hoặc Overleaf).
   - Sử dụng gói `fontspec` với phông chữ chính **Times New Roman** và phông mã nguồn **Consolas**:
     ```latex
     \usepackage{fontspec}
     \setmainfont{Times New Roman}
     \setmonofont{Consolas}[Scale=MatchLowercase]
     ```

2. **Đồng bộ Header & Chiều cao Header (Headheight Hygiene):**
   - Thiết lập `\setlength{\headheight}{16.5pt}` để triệt tiêu hoàn toàn cảnh báo `Package fancyhdr Warning: \headheight is too small`.
   - Header & Footer trang hiển thị:
     - Header trái: `\fancyhead[L]{Đồ án liên ngành - RareProtSelect}` kèm đường kẻ mỏng $0{,}4\text{ pt}$ phân cách.
     - Header phải: để trống.
     - Footer giữa: `\fancyfoot[C]{\thepage}` (số trang nằm chính giữa đáy trang).

---

## 3. NGUYÊN TẮC LIÊM CHÍNH HỌC THUẬT & TRÌNH BÀY (ACADEMIC WRITING)

1. **Quy tắc Whitelist dấu ngoặc đơn (Ironclad Parentheses Whitelist):**
   - **TUYỆT ĐỐI KHÔNG** dùng dấu ngoặc đơn để kẹp văn bản hoặc chữ tiếng Việt thông thường (như `(ví dụ là ...)`, `(biến cao nhất là ...)`, `(chúng ta thấy rằng ...)`). Viết diễn giải trực tiếp vào câu văn bằng dấu phẩy hoặc mệnh đề quan hệ.
   - Dấu ngoặc đơn `(...)` **CHỈ ĐƯỢC PHÉP** sử dụng trong 4 trường hợp cụ thể:
     1. Trích dẫn tài liệu tham khảo: `\cite{...}` (ví dụ: `\cite{nguyen2025}`).
     2. Ký hiệu toán học, tham số và biến mô hình (ví dụ: $S_k$, $w_v^{(\alpha)}$, $F_\alpha(S)$, $\beta = 0{,}70$).
     3. Các chỉ số thống kê và số đo thực nghiệm định lượng (ví dụ: `($N = 4.120$)`, `($p < 0{,}001$)`, `($\text{Sens} = 94{,}13\%$)`, `($k = 115$)`).
     4. Tên viết tắt tiếng Anh đi kèm ở lần đầu xuất hiện (ví dụ: *Mô hình ngôn ngữ protein (Protein Language Model -- PLM)*).

2. **Chống văn mẫu rập khuôn (Anti-Robotic Lead-ins & BLUF):**
   - Tuyệt đối không dùng các câu dẫn học vẹt sáo rỗng: *"nhóm em nhận thấy bài làm vẫn còn một số hạn chế nội tại"*, *"dưới đây là kết quả thực nghiệm..."*, *"sau đây chúng ta cùng tìm hiểu..."*.
   - Áp dụng nguyên tắc **Kết luận cốt lõi lên đầu (BLUF - Bottom Line Up Front)**: Nêu ngay bản chất hiện tượng sinh học/toán học và con số đo đạc cụ thể trước khi giải thích chi tiết.
   - Giữ ngôi kể khách quan khoa học: Tuyệt đối không dùng *"em"*, *"chúng em"*, *"nhóm em"* trong thân bài các chương (chỉ dùng trong Lời cam đoan và Lời cảm ơn). Thay bằng: *"đồ án"*, *"nghiên cứu"*, *"phương pháp đề xuất"*, *"thuật toán"*.
   - **Cấm câu mở đầu rập khuôn tự quy chiếu**: Tuyệt đối không bắt đầu đoạn văn hoặc tiểu mục bằng các cụm từ sáo rỗng tự quy chiếu như *"Nội dung này..."*, *"Nội dung tiếp theo tập trung vào..."*, *"Phần này sẽ trình bày..."*. Đi thẳng vào phát hiện khoa học, bản chất cơ chế hoặc nhận định dữ liệu cụ thể (BLUF).

3. **Nguyên tắc Liêm chính Dữ liệu Thực nghiệm (100% Verbatim):**
   - Mọi con số đo đạc trích dẫn trong văn bản (độ nhạy, độ bao phủ, số phân họ hiếm, tỷ lệ dư thừa) bắt buộc phải đối soát chính xác $100\%$ nguyên văn với 6 tệp kết quả CSV gốc trong `RareProtSelect/outputs/tables/`:
     - Thử nghiệm 1: `exp1_baseline_a1a_calibration.csv`
     - Thử nghiệm 2: `exp2_rare_weighted_a1a.csv`
     - Thử nghiệm 3: `exp3_esm_coverage_a1a.csv`
     - Thử nghiệm 4: `exp4_cross_eval_a1a.csv`
     - Thử nghiệm 5: `exp5_subfamily_allocation_a1a.csv`
     - Thử nghiệm 6: `exp6_budget_scaling_a1a.csv`
   - Tuyệt đối không làm tròn tùy tiện hoặc tự ý nội suy số liệu chưa đo đạc thật.

4. **Cấm tuyệt đối ẩn dụ tu từ văn học & hình tượng báo chí (Zero Literary Metaphors & Journalistic Imagery):**
   - Nghiêm cấm sử dụng các ẩn dụ văn học, hình tượng báo chí tu từ như *"bệ phóng"*, *"trụ cột"*, *"ngọn hải đăng"*, *"cú hích"*, *"đòn bẩy"*, *"bức tranh toàn cảnh"* để mô tả các chương mục hoặc nội dung khoa học.
   - Bắt buộc dùng thuật ngữ khoa học chuẩn xác, trung tính:
     - Thay *"bệ phóng lý thuyết / bệ phóng nền tảng"* bằng *"cơ sở lý thuyết nền tảng"* hoặc *"thiết lập cơ sở lý thuyết"*.
     - Thay *"bốn trụ cột kiến thức"* bằng *"bốn nội dung khoa học liên ngành trọng tâm"* hoặc *"bốn nội dung nghiên cứu"*.
     - Thay *"bức tranh toàn cảnh"* bằng *"tổng quan toàn diện"*.
   - Tuyệt đối không lặp nghĩa (*pleonasm*) và không chồng chéo các hình ảnh tu từ trong cùng một câu văn.

5. **Chuẩn hóa thuật ngữ phân cấp phân loại MEROPS & Độ chính xác cấp độ Họ vs. Phân họ (MEROPS Taxonomic Hierarchy & Family-Subfamily Precision):**
   - Bắt buộc sử dụng thống nhất 100% thuật ngữ tiếng Anh gốc cho bốn cấp độ phân loại sinh học trong MEROPS: `Clan`, `Family`, `Subfamily`, và `Peptidase` (hoặc `Peptidase ID`).
   - Tuyệt đối CẤM dịch pha tạp kiểu 'ở trên ghi định nghĩa tiếng Việt: Lớp, Họ, Phân họ... ở dưới viết tiếng Anh: Clan AA, Family A1'.
   - Khi đề cập đến các đơn vị phân loại MEROPS, sử dụng thống nhất: `Clan AA`, `Family A1`, `Subfamily` (ví dụ: `115 Subfamily chính thức`, `45 Subfamily hiếm`, `Subfamily đơn độc`, `ranh giới Subfamily`).
   - **Phân biệt rạch ròi giữa cấp độ Họ (Family) đa dạng và Phân họ (Subfamily) biến dị nội nhóm**: Tuyệt đối CẤM viết gộp sai bản chất sinh học thành *"các phân họ đa dạng cao đòi hỏi nhiều chuỗi đại diện"*. Phải diễn đạt chính xác theo hai cấp độ: (1) **Một họ protein có độ đa dạng cao và phân tách thành nhiều phân họ** (như `Family A1` gồm $115$ `Subfamily` chính thức), và (2) **Các phân họ quy mô lớn bên trong họ đó có mức độ biến dị trình tự nội nhóm rộng** (như `A01.009` gồm $329$ chuỗi) nên đòi hỏi nhiều hơn một chuỗi đại diện để bao phủ hết các nhánh tiến hóa phụ.

6. **Phân định rạch ròi ngữ cảnh sử dụng từ "Chuỗi protein" và "Trình tự axit amin" (Monomer Order vs. Molecular Entity):**
   - Dùng **"chuỗi protein"** hoặc **"chuỗi"** (*sequence*) khi đề cập đến một cá thể phân tử, thực thể sinh học cụ thể trong tập dữ liệu (ví dụ: *"chọn tập chuỗi protein đại diện"*, *"loại bỏ các chuỗi chưa phân loại"*, *"$4.120$ chuỗi protein"*).
   - Dùng **"trình tự axit amin"** hoặc **"trình tự nucleotide"** (*primary sequence / amino acid sequence*) khi bàn về cấu trúc trật tự sắp xếp các ký tự monomer trong chuỗi; tuyệt đối không dùng từ *"trình tự"* đứng trơ trọi như một danh từ chỉ cá thể phân tử.

7. **Nguyên lý văn phong học thuật nghiêm cẩn & Chống từ ngữ giật gân, khẩu ngữ (Scholarly Temperance & Zero Colloquialism):**
   - **Cấm tuyệt đối khẩu ngữ / tiếng lóng tin sinh (Zero Colloquial Slang)**: Nghiêm cấm sử dụng các từ ngữ bình dân, khẩu ngữ phòng lab hoặc khẩu ngữ đời thường như *"cơ chế bắn BLAST"*, *"bắn chuỗi"*, *"chạy bừa"*, *"chọn nốt"*, *"làm nốt"*. Bắt buộc thay bằng thuật ngữ học thuật chuẩn xác: *"quy trình truy vấn Live BLASTp"*, *"phép tìm kiếm tương đồng Live BLASTp"*, *"thao tác so khớp chuỗi All-vs-All"*, *"lựa chọn các phân họ hiếm còn lại"*.
   - **Cấm tuyệt đối kịch tính hóa / văn phong báo chí giật gân & mở đầu tán dương cảm tính (Zero Sensationalism / Pompous Openers)**: Nghiêm cấm các từ ngữ cảm tính, phóng đại, giật gân như *"cốt tử"*, *"chết người"*, *"tai hại"*, *"vô phương cứu chữa"*, hoặc các cụm từ mở đầu tán dương hoa mỹ như *"xác nhận quy luật sinh học sâu sắc"*, *"minh chứng hùng hồn"*. Bắt buộc thay bằng từ ngữ đánh giá khoa học trung tính, chuẩn mực: *"điểm mù phương pháp luận trọng yếu"*, *"hạn chế phương pháp luận then chốt"*, *"Số liệu tại bảng~\ref{...} cho thấy rõ cơ chế..."*.

8. **Nguyên lý khiêm tốn nhận thức & Chống tuyên ngôn dứt điểm / bão hòa chủ quan (Epistemic Humility & Prohibition of Subjective Saturation Claims):**
   - Tuyệt đối CẤM sử dụng các từ ngữ mang tính khẳng định hoàn tất tuyệt đối hoặc áp đặt chủ quan trước khi xét số liệu: *"hoàn hảo"*, *"sửa triệt để"*, *"triệt tiêu hoàn toàn sai số"*, *"lần sửa cuối cùng"*, *"bảo đảm không còn lỗi phát sinh"*, *"hoàn toàn giải quyết dứt điểm"*, *"xác lập trạng thái bão hòa trên toàn siêu họ"*.
   - Bắt buộc giới hạn phát biểu trong phạm vi khoa học đo đạc khách quan: *"giảm thiểu tối đa sai lệch"*, *"ngăn chặn nguy cơ sai lệch bao phủ chéo"*, *"đánh giá mức độ hội tụ của độ bao phủ ở vùng ngân sách cao"*, *"tiệm cận ngưỡng bão hòa bao phủ với 104 trên 115 Subfamily đạt tỷ lệ nhận diện 100% Sensitivity"*. Mọi kết luận chỉ có giá trị trong không gian kiểm chứng thực nghiệm cụ thể.

---

## 4. KỶ LUẬT TRÌNH BÀY BẢNG BIỂU KHOA HỌC (BOOKTABS & DATA TABLES)

1. **Tiêu chuẩn Booktabs 3 đường kẻ ngang (Strict Booktabs Rule):**
   - **TUYỆT ĐỐI CẤM** kẻ các đường dọc (`|`) trong bảng.
   - Chỉ sử dụng 3 đường kẻ ngang chuẩn mực từ gói `booktabs`:
     - `\toprule`: Đường kẻ đầu bảng (dày).
     - `\midrule`: Đường kẻ phân cách giữa tiêu đề cột và dòng dữ liệu đầu tiên.
     - `\bottomrule`: Đường kẻ chân bảng (dày).
   - Nếu cần phân tách các nhóm hàng, chỉ sử dụng lệnh `\addlinespace` hoặc `\cmidrule(lr){...}`.

2. **Quy tắc căn lề dữ liệu trong bảng:**
   - **Cột văn bản mô tả**: Căn trái (`L{...}` hoặc `l`).
   - **Cột ký hiệu, nhãn phân họ, hệ số**: Căn giữa (`c`).
   - **Cột số liệu thực nghiệm, phần trăm, giá trị đo đạc**: Căn phải (`r`) để các hàng đơn vị thẳng cột trực quan.

3. **Cấu trúc Cặp dẫn - luận & Kết luận tự chứa (Lead-in, Post-Analysis & Self-Contained Conclusion Discipline):**
   - Mọi bảng biểu xuất hiện trong văn bản **bắt buộc phải có câu dẫn nhập (Lead-in)** trước bảng giới thiệu mục đích so sánh (tách bạch rõ với đoạn văn giải thích thiết kế tham số phía trên).
   - Ngay sau bảng **bắt buộc phải có đoạn văn phân tích các điểm mốc (Key Landmarks)**, cực trị và khoảng lệch (Gaps), không được để bảng nằm trơ trọi thiếu lời giải thích.
   - **Câu kết luận của đoạn phân tích bảng bắt buộc phải tự chứa (Self-Contained)**: Phải tổng kết trực diện từ chính các con số vừa phân tích trong đoạn đó; tuyệt đối cấm viết câu kết sáo rỗng, tự mâu thuẫn với số liệu trong bảng, hoặc gán ghép vô căn cứ cho bài báo nền đối với các phép đo mở rộng mà bài báo nền không thực hiện.

4. **Ký tự thoát hiểm (Escaped Characters in Tables):**
   - Các ký tự đặc biệt trong nội dung ô bảng bắt buộc phải escape cẩn trọng: `\%` (phần trăm), `\_` (gạch dưới), `\&` (và).

---

## 5. QUY CHUẨN CÔNG THỨC TOÁN HỌC & KÝ HIỆU (MATHEMATICAL RIGOR)

1. **Môi trường công thức có đánh số:**
   - Mọi công thức toán lý thuyết cần tham chiếu trong văn bản bắt buộc đặt trong môi trường `equation` có `\label{eq:...}`:
     ```latex
     \begin{equation}
         F_\alpha(S) = \sum_{v \in V} w_v^{(\alpha)} \max_{s \in S} \mathbf{S}(v, s)
         \label{eq:weighted_facility_location}
     \end{equation}
     ```
   - Công thức giải thích biến trung gian không cần đánh số đặt trong `\[ ... \]`.

2. **Ký hiệu chuẩn hóa của đề tài RareProtSelect:**
   - Ma trận tương đồng in đậm: $\mathbf{S}_{\text{BLAST}}$, $\mathbf{S}_{\text{ESM}}^{(\beta=0{,}70)}$.
   - Vector nhúng ngữ nghĩa in đậm: $\mathbf{z}_v \in \mathbb{R}^{480}$.
   - Tập hợp in hoa nghiêng: Tập toàn thể $V$, tập đại diện $S_k$, phân họ $V_g$, tập phân họ hiếm $G_{\text{rare}}$.
   - Tên biến có chỉ số dưới trong toán học dùng ký hiệu chỉ số dưới: $w_v^{(\alpha)}$, $n_g$, $\text{sim}_{\text{PLM}}$. (Lưu ý: trong tệp Markdown thì escape $\text{sim}\_\text{PLM}$ để tránh vỡ cú pháp markdown, nhưng trong mã nguồn LaTeX .tex bắt buộc dùng cú pháp chỉ số dưới chuẩn $w_v, n_g$).

3. **Định dạng số thập phân trong tiếng Việt:**
   - Trong khối toán học LaTeX, dấu phẩy ngăn cách phần thập phân của tiếng Việt bắt buộc phải bọc trong cặp ngoặc nhọn `{,}` để LaTeX không hiểu nhầm là dấu phẩy phân cách danh sách và tự ý chèn khoảng trắng:
     - Đúng: `$94{,}13\%$`, `$0{,}51\%$`, `$1{,}0\text{ cm}$`, `$\beta = 0{,}70$`.
     - Sai: `$94,13\%$` (sẽ bị giãn cách thành $94, 13\%$).

4. **Chuẩn hóa thuật ngữ toán học tối ưu hóa & Cấm từ ngữ ước lệ đời thường, hành chính hoặc cơ học sai ngữ cảnh (Mathematical Rigor):**
   - Tuyệt đối CẤM sử dụng các từ ngữ đời thường, hành chính bao cấp (như *"bù đắp"*, *"bù trừ"*, *"gánh vác"*, *"cấp đại diện"*, *"cấp thêm đại diện"*, *"vừa cấp thêm đại diện"*), từ ngữ tâm lý học nhân hóa (như *"làm giảm động lực chọn"*), hoặc từ cơ học sai ngữ cảnh cho chỉ số thống kê (như *"nén mạnh độ dư thừa"*, *"ép độ dư thừa xuống"*) để diễn giải cơ chế mô hình toán học và giải thuật tối ưu.
   - Bắt buộc sử dụng các thuật ngữ tối ưu hóa và thống kê chuẩn xác: *"hiệu chỉnh trọng số"* (*weight adjustment/normalization*), *"tái cân bằng quy mô"* (*rebalancing*), *"phạt quy mô nhóm"* (*group size penalty*), *"phân bổ đại diện / phân bổ thêm các chuỗi đại diện"*, *"giảm đáng kể / cắt giảm độ dư thừa"*, *"khiến phần độ tăng cận biên còn lại bị thu hẹp và nhỏ hơn tổng độ tăng cận biên tích lũy trên các phân họ lớn"*.

5. **Quy chuẩn biểu diễn bội số và tỷ số trong văn xuôi (Multipliers & Dimensionless Ratios):**
   - Trong văn xuôi tiếng Việt học thuật, **TUYỆT ĐỐI CẤM** viết bội số dưới dạng ký hiệu tắt `$X\times$` (ví dụ: `$1{,}6\times$`, `$4{,}0\times$`, `$329{,}0\times$`).
   - **Bắt buộc viết bằng tiếng Việt tự nhiên**: `gấp $X$ lần` (ví dụ: `gấp $1{,}6$ đến $4{,}0$ lần`, `gấp $329{,}0$ lần`).
   - Khi thể hiện trong công thức toán học hoặc tỷ số vô thứ nguyên thuần túy, viết tỷ số trực tiếp không kèm đơn vị (ví dụ: $\frac{n_{\max}}{n_{\min}} = 329{,}0$).

---

## 6. QUY CHUẨN CHÈN HÌNH ẢNH & BIỂU ĐỒ THỰC NGHIỆM (FIGURES & LANDMARKS)

1. **Nguồn ảnh & Thư mục lưu trữ:**
   - Toàn bộ hình ảnh biểu đồ thực nghiệm của đề tài lưu trữ thống nhất tại [`Images/figures/`](./Images/figures/).
   - Ảnh biểu đồ sử dụng định dạng PNG độ phân giải cao ($\ge 300\text{ DPI}$) hoặc PDF vector xuất bản từ matplotlib/seaborn của pipeline.

2. **Môi trường hình vẽ chuẩn mực:**
   - Mọi hình ảnh phải đặt trong môi trường `figure` với tham số vị trí `[htbp!]` (kết hợp gói `placeins` qua lệnh `\FloatBarrier` ở đầu mỗi section để tránh trôi hình sang phần khác mà không tạo khoảng trắng lớn ở cuối trang như `[H]`), căn giữa `\centering`:
     ```latex
     \begin{figure}[htbp!]
         \centering
         \includegraphics[width=0.88\textwidth]{Images/figures/exp2_pareto_tradeoff.png}
         \caption{Tương quan đánh đổi giữa Overall Sensitivity và Rare Sensitivity tại $k = 11$ và $k = 115$ trên không gian BLASTp.}
         \label{fig:exp2_pareto}
     \end{figure}
     ```
   - Lệnh `\label{fig:...}` **bắt buộc phải đặt ngay sau** `\caption{...}` để số thứ tự hình được tham chiếu chính xác.

3. **Nguyên tắc phân tích biểu đồ (/report-result):**
   - **Triệt tiêu trùng lặp**: Đã có biểu đồ thì không lặp lại bảng số liệu thô đồ sộ.
   - **Chỉ ra các điểm mốc (Landmarks)**: Phải chỉ rõ điểm uốn bứt phá, ngưỡng bão hòa (plateau) gắn liền với giá trị ngân sách $k$ và hệ số $\alpha$.
   - **Khoảng lệch đa biểu đồ (Multi-Chart Gap)**: Chỉ ra khoảng cách giữa các đường cong (ví dụ: khoảng cách giữa $\alpha = 0{,}0$ và $\alpha = 0{,}5$) và giải thích nguyên nhân toán học tạo ra khoảng lệch đó.

---

## 7. KỶ LUẬT THAM CHIẾU CHÉO & DANH MỤC TRÍCH DẪN (CROSS-REFERENCING)

1. **Hệ thống tiền tố nhãn chuẩn hóa (`\label`):**
   - `chap:` cho Chương (ví dụ: `\label{chap:theory}`)
   - `sec:` cho Mục (ví dụ: `\label{sec:submodular_theory}`)
   - `subsec:` cho Tiểu mục (ví dụ: `\label{subsec:plm_anisotropy}`)
   - `fig:` cho Hình vẽ (ví dụ: `\label{fig:exp4_crossover}`)
   - `tab:` cho Bảng biểu (ví dụ: `\label{tab:milestone_k115}`)
   - `eq:` cho Công thức toán (ví dụ: `\label{eq:within_subfamily_query}`)

2. **Cấm tuyệt đối hard-code số thứ tự tĩnh:**
   - **TUYỆT ĐỐI CẤM** viết các câu như: *"như trong Hình 3.1"*, *"theo Bảng 2"*, *"ở Công thức 5"*.
   - **BẮT BUỘC** sử dụng lệnh `\ref{...}` kèm dấu ngã `~` chống ngắt dòng:
     - `như thể hiện trong hình~\ref{fig:exp4_crossover}` (giữa câu) hoặc `Hình~\ref{fig:exp4_crossover}` (đầu câu)
     - `kết quả đối chuẩn tại bảng~\ref{tab:milestone_k115}` (giữa câu) hoặc `Bảng~\ref{tab:milestone_k115}` (đầu câu)
     - `được định nghĩa qua công thức~\eqref{eq:weighted_facility_location}` (giữa câu) hoặc `Công thức~\eqref{eq:weighted_facility_location}` (đầu câu)

3. **Kỷ luật trích dẫn học thuật (`\cite`):**
   - Mọi khẳng định khoa học, thuật toán kế thừa hoặc công cụ bên ngoài bắt buộc phải có trích dẫn `\cite{...}` liên kết trực tiếp với mục tương ứng trong [`contents/references.tex`](./contents/references.tex):
     - Bài báo nền: `\cite{nguyen2025}`
     - Mô hình ESM-2: `\cite{esm2}`
     - Công cụ BLAST: `\cite{blast}`
     - Cơ sở dữ liệu MEROPS: `\cite{merops}`
     - Định lý Nemhauser $(1 - 1/e)$: `\cite{nemhauser1978}`
     - Giới hạn cận chặt $(1 - 1/e)$: `\cite{feige1998}`
     - Tối ưu hóa hàm submodular: `\cite{krause2014}`
     - Thuật toán Lazy Greedy: `\cite{minoux1978}`
     - Công cụ CD-HIT: `\cite{cdhit}` và MMseqs2: `\cite{mmseqs2}`

---

## 8. BẢO VỆ MÔI TRƯỜNG LÀM VIỆC SẠCH (ZERO BUILD ARTIFACTS)

1. **Vệ sinh không gian tệp (Workspace Hygiene):**
   - Thư mục [`report_latex/`](./) chỉ lưu trữ các tệp nguồn (`.tex`, `.bib`, `.jpg`, `.png`, `.md`).
   - Tuyệt đối không commit các tệp phụ sinh ra trong quá trình biên dịch (`.aux`, `.log`, `.out`, `.toc`, `.lof`, `.lot`) vào kho lưu trữ git.
   - Khi có sự cố biên dịch, chủ động xóa các tệp phụ auxiliary cũ trước khi biên dịch lại.

2. **Quy trình biên dịch 2 lượt chuẩn xác:**
   - Mọi lần kiểm thử chất lượng tài liệu phải chạy tối thiểu 2 lượt lệnh `xelatex`:
     - Lượt 1: Ghi nhận cấu trúc nhãn, số trang và mục lục vào `main.aux` và `main.toc`.
     - Lượt 2: Đồng bộ hóa toàn bộ tham chiếu chéo `\ref`, danh mục hình/bảng và số trang hoàn chỉnh.

3. **Kỷ luật an toàn khi dùng Script chỉnh sửa mã nguồn LaTeX (LaTeX Script Safety):**
   - **Tuyệt đối CẤM** chạy lệnh inline `python -c "..."` trên PowerShell chứa chuỗi có ký tự `$` của LaTeX, vì PowerShell sẽ hiểu nhầm `$V`, `$0` là biến môi trường và nuốt mất ký tự toán học (dẫn đến lỗi cú pháp nghiêm trọng như mất dấu mở/đóng math mode).
   - **Bắt buộc** sử dụng công cụ `edit_file` hoặc ghi script Python độc lập ra tệp `.py` với mã hóa UTF-8 rồi mới thực thi.
   - Sau mọi thao tác sửa mã nguồn `.tex`, bắt buộc kiểm tra tính cân bằng chẵn lẻ của ký tự `$` và biên dịch 2 lượt qua terminal để kiểm chứng không có lỗi `Missing $ inserted` hay `Missing character in font cmmi12`.

---

## 9. KỶ LUẬT PHÂN ĐỊNH PHÔNG CHỮ MONOSPACE (\texttt) VÀ PHÔNG CHỮ CHÍNH

1. **Bản chất cơ chế phông chữ trong LaTeX:**
   - Trong `main.tex`, phông chữ đơn không gian (monospace) được gán cố định cho phông **Consolas** qua lệnh `\setmonofont{Consolas}[Scale=MatchLowercase]`.
   - Phông Consolas có đặc trưng thị giác phục vụ lập trình: chiều rộng ký tự cố định (*fixed-pitch*), số 0 có dấu gạch chéo (`0` *slashed-zero*), và nét chữ slab/sans-serif thô.
   - Khi sử dụng `\texttt{...}` trong thân bài văn xuôi, các từ ngữ này bị đứt gãy thị giác hoàn toàn (*visual disruption/nhảy font*) so với phông chữ chính Times New Roman.

2. **Đối tượng CẤM TUYỆT ĐỐI sử dụng `\texttt` và `\verb`:**
   - **Tên tệp dữ liệu sinh học trong thân bài**: `MEROPS\_A1A.fasta`, `Thioesterases\_Sequences.fasta`, `CE.fasta`.
   - **Mã định danh phân loại sinh học & nhãn Subfamily**: `[A01.UPA]`, `A01.001`, `A01.009`, `A01.098`.
   - **Tên mô hình học máy & Checkpoint trong văn bản**: `facebook/esm2\_t12\_35M\_UR50D`, `ESM-2-35M`.
   - **Tên chỉ số kỹ thuật & biến toán học**: Sử dụng chế độ toán học (`$k$`, `$\text{Overall Sensitivity}$`, `$w_v$`), không bọc bằng `\texttt`.
   - **Biểu thức chính quy (Regex) và mẫu chuỗi mô tả trong văn xuôi**: Tuyệt đối không dùng `\verb` hoặc `\texttt` vì sẽ kéo phông Consolas vào tạo ra số 0 gạch chéo (`0` slashed-zero) và nét chữ monospace thô cứng làm đứt gãy thị giác. Bắt buộc hiển thị bằng phông chữ chính Times New Roman chữ đứng, escape các ký tự đặc biệt trong LaTeX (ví dụ: `\textbackslash [([A-Z]\textbackslash d\{2\}\textbackslash .(?!UPA)[A-Z0-9]\{3\})\textbackslash ]`).

3. **Phạm vi DUY NHẤT được phép sử dụng `\texttt`:**
   - **Lệnh thực thi dòng lệnh (CLI / Terminal)**: `uv run python main.py`, `git clone`.
   - **Đường dẫn tệp mã nguồn và cấu hình lập trình trong codebase**: `configs/config.yaml`, `src/facility_location.py`.
   - **Tên hàm, class, phương thức hoặc biến lập trình trực tiếp**: `compute_submodular_gain()`, `class GreedyOptimizer`.

4. **Quy chuẩn hiển thị tên tệp dữ liệu và mã phân họ**:
   - Toàn bộ tên tệp dữ liệu sinh học và mã phân loại trong văn xuôi phải được hiển thị bằng **phông chữ chính (Times New Roman)** ở dạng chữ đứng (*upright Roman*) thông thường, escape ký tự gạch dưới bằng `\_` (ví dụ: `MEROPS\_A1A.fasta`, `[A01.UPA]`, `A01.009`).

---

## 10. NGUYÊN TẮC CẤM NHÂN HÓA / CHÍNH TRỊ HÓA & DANH MỤC THUẬT NGỮ CẤM KỴ TOÀN BỘ ĐỒ ÁN (ZERO ANTHROPOMORPHISM & MASTER BLACKLIST)

1. **Bản chất khoa học & Triết học mô hình hóa:**
   - Trong toán học tối ưu hóa tổ hợp submodular và sinh học phân tử, protein là các đại phân tử hóa sinh vô tri, Subfamily là các đơn vị phân loại học tiến hóa, và hàm mục tiêu Facility Location là một hàm số thực xác định trên không gian metric.
   - Các thực thể này **hoàn toàn không có ý thức xã hội, thể chế, hay quan hệ quyền lực chính trị**. Mọi hành vi gán ghép từ ngữ chính trị - xã hội vào mô hình toán học đều là lỗi ngụy biện nhân hóa (*anthropomorphism*), làm suy thoái tính nghiêm cẩn học thuật của đồ án khoa học.

2. **Bảng danh mục đối chiếu cấm kỵ và thay thế bắt buộc (Master Blacklist & Mandatory Lexicon):**

| Khái niệm khoa học | Thuật ngữ cấm sử dụng (`BLACKLIST`) | Thuật ngữ chuẩn mực khoa học (`MANDATORY`) | Bản chất khoa học & Cơ chế giải thích |
| :--- | :--- | :--- | :--- |
| **Đại lượng $W_g^{(\alpha)}$** | Quyền lực của Subfamily, tổng quyền lực | **Tổng trọng số trong hàm mục tiêu của Subfamily** / **Tiềm năng đóng góp cận biên tích lũy** | $W_g^{(\alpha)} = (n_g)^{1-\alpha}$ là tổng trọng số của các chuỗi thành viên trong hàm mục tiêu; không phải quyền lực biểu quyết. |
| **Tỷ số giữa các nhóm** | Chênh lệch quyền lực, quyền lực tương đối | **Tỷ số đóng góp trong hàm mục tiêu** / **Tỷ lệ ưu tiên phân bổ tương đối** | Đại lượng đo lường tỷ lệ đóng góp tối đa giữa Subfamily lớn nhất và Subfamily đơn độc: $(n_{\max} / n_{\min})^{1-\alpha}$. |
| **Hiệu chỉnh $\alpha$** | Trao quyền lực cho nhóm hiếm, tái phân bổ quyền lực | **Tái cân bằng mức ưu tiên tối ưu hóa** / **Tái cân bằng trọng số trong hàm mục tiêu** | Thay đổi $\alpha$ từ $0{,}0 \to 1{,}0$ là kỹ thuật nén hàm số mũ để san phẳng độ dốc đóng góp cận biên của các nhóm. |
| **Lựa chọn tham lam** | Giành ghế đại diện bằng quyền lực, thâu tóm quyền lực | **Chiếm ưu thế độ tăng cận biên** / **Được ưu tiên lựa chọn trong giải thuật tham lam** | Chuỗi được chọn vì mang lại độ tăng cận biên lớn nhất $\Delta(e \mid S)$, là kết quả của phép so sánh số thực cực đại. |
| **Mục tiêu nhóm hiếm** | Đòi quyền lợi đại diện, bình đẳng xã hội | **Bảo tồn tính đại diện nhóm hiếm** / **Khắc phục sự thiên lệch quy mô mẫu** | Bản chất là mục tiêu tối ưu hóa bao phủ bảo toàn đa dạng sinh học trong phân bố đuôi dài Long-Tail. |
| **Thuật toán đồng thuận** | Bầu chọn đồng thuận, quy trình bầu chọn | **Cơ chế xác lập thứ hạng đồng thuận** / **Tổng hợp thứ hạng đồng thuận** | Sắp xếp danh sách dựa trên tần suất đếm $\text{Count}$ và tổng thứ hạng $\text{RankSum}$ qua $M$ lần chạy; không phải bầu cử hay bỏ phiếu xã hội. |
| **Phần độ tăng bao phủ** | Vector gia số (dùng trơ trọi) | **Vector độ tăng tương đồng** ($\boldsymbol{\delta}_u$) / **Cập nhật vector bao phủ lũy tích** | $\delta_{u, v} = \max(0, \mathbf{S}(u, v) - m_v)$ là độ cải thiện bao phủ của chuỗi; tránh dùng từ "gia số" vi phân gây tối nghĩa. |
| **So khớp ngoài phân họ** | Bắt chéo, bắt dính chéo | **So khớp chéo ngoài ranh giới Subfamily** / **Bảo tồn cục bộ xuyên ranh giới phân loại** | "Bắt" là khẩu ngữ cơ học phòng lab; bản chất là hai chuỗi thuộc Subfamily khác nhau cùng chia sẻ motif xúc tác bảo tồn. |
| **Bảo toàn ranh giới phân loại** | Bảo toàn tính đặc hiệu của từng Subfamily | **Duy trì ranh giới phân loại của từng Subfamily** / **Ngăn chặn sai lệch bao phủ chéo ngoài ranh giới phân họ** | Cụm từ "bảo toàn tính đặc hiệu" mang tính trừu tượng tối nghĩa; bản chất sinh học là bảo đảm các chuỗi đại diện chỉ bao phủ các thành viên cùng Subfamily, ngăn chặn hiện tượng bao phủ chéo sang các phân họ khác. |
| **Sai lệch bao phủ chéo** | Dương tính giả, dương tính giả giữa các Subfamily, quy gán đại diện chéo | **Sai lệch bao phủ chéo ngoài ranh giới phân họ (Cross-Subfamily Misattribution)** / **Ảo giác bảo tồn ngụy tạo** | Tránh dùng từ chẩn đoán y tế ("dương tính giả") hoặc từ Hán-Việt khiên cưỡng ("quy gán"); bản chất ở đây là sai lệch đo lường khi chuỗi đại diện nhóm lớn bao phủ chéo sang nhóm hiếm tạo ảo giác bảo tồn ngụy tạo. |
| **Thao tác đối soát BLAST** | Quét Live BLASTp, quét BLAST, bắn BLAST, bắn chuỗi, chạy bừa | **Thực hiện phép tìm kiếm tương đồng Live BLASTp** / **Quy trình đối soát chuỗi Live BLASTp** | "Quét", "bắn" là khẩu ngữ / tiếng lóng phòng lab; văn bản học thuật bắt buộc dùng danh từ/động từ chuẩn xác của thao tác tin sinh học. |
| **So khớp chuỗi** | Căn chỉnh, căn chỉnh chuỗi, căn chỉnh cục bộ, ma trận căn chỉnh | **So khớp chuỗi / Đối soát chuỗi / Gióng hàng chuỗi / Tìm kiếm tương đồng Live BLASTp** | "Căn chỉnh" là dịch máy thô từ *alignment* (dễ nhầm với căn lề trang Word/LaTeX); trong tin sinh học phải dùng "so khớp chuỗi", "gióng hàng" hoặc "đối soát chuỗi". |
| **Quy trình xử lý dữ liệu** | Tinh tuyển, tinh tuyển tập dữ liệu | **Sàng lọc và thẩm định dữ liệu** / **Kiểm soát chất lượng và chuẩn bị dữ liệu** | "Tinh tuyển" là từ hoa mỹ/văn học, không chuẩn mực khoa học; bản chất là quy trình kiểm tra chất lượng (QC) và phân loại. |
| **Bản chất Subfamily** | Subfamily sinh học thực thụ, phân họ thực thụ | **Subfamily có định danh chính thức trong MEROPS** / **Subfamily chính thức** | "Thực thụ" là cách dịch máy thô ("true biological subfamilies"); bản chất là các phân họ đã được phân loại chính thức theo chuẩn quốc tế. |
| **Tập nền $V$** | Tập nền sạch, tập dữ liệu sạch | **Tập nền phân họ chính thức** / **Chuỗi protein đã qua kiểm soát chất lượng** | "Sạch" là khẩu ngữ đời thường; văn bản khoa học phải dùng thuật ngữ phản ánh đúng quy trình tiền xử lý dữ liệu. |
| **Tạo dựng tập nền** | Xác lập tập nền, xác lập tập dữ liệu | **Xây dựng tập nền** / **Thiết lập tập nền phân họ chính thức** | "Xác lập" mang nặng tính hành chính/pháp lý; tạo dựng tập hợp dữ liệu phải dùng động từ "xây dựng" hoặc "thiết lập". |
| **Chỉ số Sensitivity** | Độ nhạy, độ nhạy toàn thể, 0% độ nhạy | **Overall Sensitivity / Rare Sensitivity / Tỷ lệ nhận diện chuỗi qua Live BLASTp** | "Độ nhạy" gây liên tưởng cảm biến vật lý/y tế; bắt buộc dùng danh xưng tiếng Anh chuẩn cho chỉ số và giải nghĩa "tỷ lệ nhận diện chuỗi" trong văn xuôi. |
| **Chỉ số Coverage** | Độ phủ (dùng cộc lốc) | **Độ bao phủ / Tính đại diện / Within-Subfamily Coverage** | "Độ phủ" là cách nói tắt dân dã; văn bản khoa học bắt buộc dùng "độ bao phủ" hoặc thuật ngữ chuẩn hóa. |
| **Cá thể phân tử** | Trình tự (đứng trơ trọi) | **Chuỗi protein / Chuỗi** | "Trình tự" là danh từ trừu tượng chỉ trật tự sắp xếp monomer; cá thể phân tử bắt buộc phải gọi là "chuỗi protein" hoặc "chuỗi". |
| **Chuỗi chưa phân loại** | Trình tự chưa định danh | **Chuỗi chưa được phân loại phân họ** | Tránh hiểu nhầm là chuỗi lạ hoặc mất mã ID; thực tế chuỗi có ID đầy đủ nhưng chưa được gán vào phân họ chính thức trong MEROPS. |
| **Phương pháp so sánh** | Phương pháp hiện hành | **Các phương pháp hiện có / truyền thống** | "Hiện hành" là thuật ngữ hành chính — pháp lý (áp dụng cho luật pháp/văn bản); cấm dùng cho thuật toán và phương pháp khoa học. |
| **Chứng minh toán học** | Chứng minh hình thức | **Chứng minh toán học chặt chẽ / giải tích** | "Hình thức" trong tiếng Việt mang hàm ý tiêu cực là chiếu lệ, làm màu, không có thực chất; bản chất là chứng minh toán học giải tích chặt chẽ. |
| **Biểu diễn ngữ nghĩa** | Suy biến dị hướng (trơ trọi) | **Hiện tượng co cụm vector (Anisotropy)** | "Dị hướng" là từ Hán-Việt tối nghĩa; bản chất hình học là các vector bị co cụm về một góc nón hẹp trong không gian embedding. |
| **Kỹ thuật dịch tâm** | Kỹ thuật khử suy biến dị hướng | **Kỹ thuật dịch tâm Mean-Centering** | Gọi đúng tên hàm toán học đã lập trình (`compute_mean_centered_cosine_matrix`) để trừ vector kỳ vọng trung bình toàn thể. |
| **Mở rộng kích thước $k$** | Dải ngân sách sâu | **Khi mở rộng quy mô tập đại diện** | "Dải ngân sách sâu" gây hiểu nhầm sang tài chính hoặc địa chất; bản chất là khảo sát hành vi mô hình khi tăng số lượng đại diện $k$ lớn. |
| **Cơ chế bao phủ nội nhóm** | Truy vấn ngược | **Cơ chế bao phủ Within-Subfamily Coverage** | Tránh dịch thô "truy vấn ngược"; bản chất là cơ chế chỉ cho phép đại diện bảo vệ và tính độ bao phủ cho chuỗi cùng phân họ. |
| **Cơ chế Attention** | Chú ý tự thân / Cơ chế chú ý tự thân | **Cơ chế tự chú ý Self-Attention / Cơ chế Self-Attention** | "Tự thân" là dịch máy thô thiển; bản chất là tính toán trọng số tương quan giữa các vị trí trong cùng chuỗi, dùng theo chuẩn mực AI/NLP. |
| **Mức độ nghiêm trọng** | Cốt tử, chết người, tai hại, vô phương cứu chữa | **Điểm mù phương pháp luận trọng yếu / Hạn chế then chốt** | Từ ngữ kịch tính hóa, giật gân theo lối báo chí; bắt buộc sử dụng văn phong đánh giá khoa học khách quan, trung tính. |
| **Đánh giá hiệu quả** | Triệt tiêu hoàn toàn sai số / Hoàn hảo / Giải quyết dứt điểm | **Giảm thiểu tối đa sai lệch / Ngăn chặn nguy cơ sai lệch bao phủ chéo** | Tuyên ngôn dứt điểm giả tạo vi phạm nguyên tắc khiêm tốn nhận thức (Epistemic Humility); khoa học thực nghiệm chỉ đo lường sự giảm thiểu. |
| **Cơ chế điều chỉnh hàm** | Bù đắp, bù trừ, gánh vác | **Hiệu chỉnh trọng số / Tái cân bằng quy mô / Phạt quy mô nhóm** | Từ ngữ đời thường, hành chính; mô hình toán tối ưu submodular bắt buộc sử dụng các thuật ngữ giải tích chuẩn xác. |
| **Cấu trúc phân loại** | Nhãn phân họ chuẩn mực | **Cấu trúc phân loại phân họ chính thức** | "Chuẩn mực" mang tính đạo đức xã hội; phải dùng "phân loại chính thức" theo MEROPS. |
| **Ma trận tương đồng** | Ma trận căn chỉnh / Ma trận căn chỉnh cục bộ | **Ma trận tương đồng BLASTp / Ma trận tương đồng chuỗi** | Tránh hiểu nhầm sang ma trận điểm thay thế (BLOSUM/PAM) hoặc bảng gióng hàng MSA; bản chất là ma trận số thực chứa độ tương đồng/tỷ lệ nhận dạng chuỗi. |
| **Khung lý thuyết** | Bệ phóng lý thuyết / Bệ phóng nền tảng | **Cơ sở lý thuyết nền tảng / Khung lý thuyết** | "Bệ phóng" là ẩn dụ văn học/báo chí, lặp nghĩa với "nền tảng"; văn bản khoa học phải dùng thuật ngữ trung tính, chuẩn xác. |
| **Nội dung nghiên cứu** | Trụ cột kiến thức / Các trụ cột | **Nội dung khoa học trọng tâm / Các nội dung nghiên cứu** | Tránh ẩn dụ tu từ hình tượng "trụ cột"; dùng từ ngữ khoa học phản ánh đúng các phần nội dung nghiên cứu. |
| **Cấp độ phân loại** | Lớp, Họ, Phân họ, Peptidase cụ thể (dịch pha tạp) | **Clan, Family, Subfamily, Peptidase ID** | Bắt buộc dùng thống nhất 4 cấp độ tiếng Anh gốc để đồng bộ với Family A1 và Clan AA. |
| **Định danh Subfamily** | Phân họ (khi đứng cạnh Family A1 gây đá nhau) | **Subfamily (thống nhất trong ngữ cảnh MEROPS)** | Đảm bảo tính nhất quán tuyệt đối với Family A1 và các chỉ số đo lường Within-Subfamily Coverage/Sensitivity; tránh tiền hậu bất nhất. |
| **Chuỗi truy vấn BLAST** | Dùng làm mồi, chuỗi mồi, làm mồi | **Chuỗi truy vấn / Làm chuỗi truy vấn để đối soát (Query sequence)** | "Mồi" là khẩu ngữ câu cá hoặc nhầm sang mồi sinh học phân tử (PCR primer); trong tin sinh học phân tử bắt buộc dùng "chuỗi truy vấn" (query). |
| **Hệ quy chiếu đo đạc** | Mặt trận, Mặt trận 1, Mặt trận 2, hai mặt trận | **Hệ quy chiếu đo đạc / Không gian đánh giá / Nhóm thước đo** | "Mặt trận" là ẩn dụ quân sự, chiến tranh; văn bản học thuật bắt buộc dùng thuật ngữ đo lường khoa học trung tính. |
| **Đối sánh thực nghiệm** | Đối đầu, đối đầu trực diện, áp đảo, áp đảo hoàn toàn, dẫn trước áp đảo, vượt lên dẫn trước | **Đối sánh hai chiều / So sánh tương quan / Vượt trội hơn / Đạt giá trị cao hơn** | Từ ngữ thể thao đối kháng, võ thuật, đua xe; nghiên cứu khoa học bắt buộc dùng thuật ngữ so sánh thống kê khách quan. |
| **Phân tích cơ chế** | Vạch trần, bóc trần, phơi bày (dùng giật gân), dưới vỏ bọc | **Làm sáng tỏ / Chỉ ra / Phát hiện / Ẩn giấu đằng sau / Bị che khuất bởi** | Từ ngữ báo chí giật gân, điều tra tố tụng, trinh thám; văn phong khoa học phải giữ thái độ điềm tĩnh, trung lập. |
| **Bảo tồn nhóm hiếm** | Giải cứu, giải cứu thành công, bỏ rơi, bị bỏ rơi (dùng ủy mị) | **Khôi phục tính đại diện / Bổ sung đại diện / Để sót / Chưa có đại diện / Không có chuỗi nào được nhận diện** | Nhân hóa tình cảm, cứu trợ ủy mị; Subfamily là đơn vị phân loại phân tử, không phải nạn nhân cần cứu nạn. |
| **Khắc phục mất cân bằng** | Độc quyền, sự độc quyền của nhóm lớn, hóa giải sự độc quyền | **Sự thiên lệch quy mô mẫu / Sự tập trung đại diện quá mức vào nhóm lớn** | "Độc quyền" là thuật ngữ kinh tế - thị trường; phân bố số lượng chuỗi là thuộc tính sinh học tự nhiên, không phải hành vi độc quyền thương mại. |
| **Mô tả đồ thị & Động học** | Nằm sát đáy, tăng dốc đứng, tăng vọt, nhảy trực tiếp sang, mở khóa, mở khóa thành công | **Duy trì ở mức 0,0% / Tăng trưởng nhanh / Đạt mức tăng trưởng / Chuyển dịch tối ưu sang / Bắt đầu có đại diện** | Khẩu ngữ đời thường, hình tượng hóa bình dân và thuật ngữ game (unlock); báo cáo khoa học bắt buộc dùng ngôn ngữ giải tích hàm số. |
| **Mở rộng ngân sách** | Bão hòa sâu, dải ngân sách sâu, động học bão hòa, động học tích lũy | **Khi mở rộng quy mô tập đại diện / Quá trình bão hòa độ bao phủ / Sự tích lũy số lượng đại diện** | "Bão hòa sâu", "dải ngân sách sâu" gây hiểu nhầm sang địa chất/tài chính; "động học" là từ lai căng thiếu tự nhiên trong ngữ cảnh tập hợp đại diện. |
| **Đánh giá & Dẫn nhập** | Tính ưu việt, chứng minh tính đúng đắn, mang tính cảm tính, các tác giả đi trước | **Tính hiệu quả / Giải quyết sự đánh đổi / Dựa trên phương pháp heuristic / Công trình nền tảng, nghiên cứu trước đây** | Tránh văn phong tự mãn tiếp thị, tránh khẩu ngữ đời thường; giữ văn phong học thuật nghiêm cẩn và khiêm tốn nhận thức. |
| **Mã phương án nội bộ** | Phương án 1, Phương án 2, Phương án 3A, Phương án 3B | **Quy trình sàng lọc và thẩm định dữ liệu phân họ chính thức Curated Subfamilies / Chiến lược thẩm định phân họ chính thức** | Tên mã kịch bản thử nghiệm code nội bộ, cấm đưa vào báo cáo học thuật; bắt buộc mô tả bằng danh xưng phương pháp luận chính thức. |
| **Ngưỡng đo lường BLAST** | Ngưỡng khắt khe, ở ngưỡng khắt khe E | **Ở ngưỡng E / Với ngưỡng thống kê sinh học E** | "Khắt khe" mang tính định tính cảm xúc đời thường; giá trị E-value ($E \le 10^{-7}$) là tham số xác suất/thống kê chuẩn mực. |
| **Lỗi lặp nghĩa chỉ số** | Chỉ số Overall Sensitivity toàn thể / Rare Sensitivity của nhóm hiếm | **Chỉ số Overall Sensitivity / Thước đo Rare Sensitivity** | "Overall" đã mang nghĩa toàn thể/tổng thể, "Rare" đã mang nghĩa nhóm hiếm; ghép thêm "toàn thể" hay "của nhóm hiếm" là lỗi lặp nghĩa (pleonasm). |
| **Lạm dụng thuật ngữ Pareto** | Điểm cân bằng Pareto, chế độ cân bằng Pareto, mối quan hệ đánh đổi Pareto, đường cong đánh đổi Pareto | **Điểm cân bằng tối ưu / Cấu hình cân bằng tối ưu / Mối quan hệ đánh đổi đa mục tiêu / Tương quan đánh đổi** | Cấm ghép từ Pareto khi chỉ có 3 điểm alpha rời rạc; bắt buộc dùng "điểm cân bằng tối ưu" hoặc "tương quan đánh đổi đa mục tiêu". |
| **Đồ thị và tham số** | Diễn tiến của đồ thị, diễn tiến bốn chỉ số, diễn tiến của thước đo | **Xu hướng biến thiên / Sự biến thiên / Đường cong biến thiên theo ngân sách k** | "Diễn tiến" là thuật ngữ y học lâm sàng hoặc sự kiện thời sự; với đồ thị hàm số theo tham số k bắt buộc dùng "biến thiên / xu hướng biến thiên". |
| **Dẫn nhập phân đoạn** | Hợp phần này, hợp phần khoa học, bốn hợp phần | **Nội dung này, phần này, mục này, bốn nội dung nghiên cứu** | "Hợp phần" mang văn phong hành chính/dự án đầu tư ODA; phân đoạn trong luận văn bắt buộc dùng "nội dung này", "mục này". |
| **Phân tích nhãn nghiệm** | Giải phẫu trực tiếp nhãn Subfamily, giải phẫu nhãn | **Phân tích cơ cấu nhãn Subfamily / Xác định nhãn Subfamily** | Tránh ẩn dụ y học/sinh học giải phẫu gượng gạo; dùng thuật ngữ phân tích dữ liệu chuẩn xác. |
| **Hiện tượng co cụm PLM** | Khử Hiện tượng co cụm vector (Representation Anisotropy) | **Khắc phục hiện tượng co cụm vector** | Vi phạm Whitelist ngoặc đơn kẹp cụm tiếng Anh; viết hoa sai ngữ pháp giữa câu; "khử" mang nghĩa hóa học, thay bằng "khắc phục hiện tượng co cụm vector". |
| **Kiểm chứng chéo không gian** | Sai lệch thiên vị không gian biểu diễn nội tại (in-domain evaluation bias) | **Hiện tượng thiên lệch khi đánh giá nội không gian** | Vi phạm Whitelist ngoặc đơn; "sai lệch thiên vị" lặp nghĩa pleonasm; "thiên vị" là nhân hóa cảm tính, bắt buộc dùng "thiên lệch" (statistical bias). |
| **Liên từ mở đầu rập khuôn** | Tuy nhiên (khi mở đầu đoạn phân tích sau hình/bảng) | **Áp dụng nguyên tắc BLUF: Nêu trực diện phát hiện/hạn chế phương pháp luận** | Tránh văn mẫu robot liên từ "Tuy nhiên, ..."; mở đầu câu trực tiếp bằng chủ ngữ khoa học hoặc hành động phân tích khách quan. |
| **Hiện tượng đảo chiều** | Giao cắt hiệu năng, quy luật động học Crossover Dynamics | **Sự đảo chiều về hiệu năng giữa hai không gian khi tăng ngân sách $k$** | "Giao cắt hiệu năng", "Crossover Dynamics" là dịch máy thô thiển; bản chất là sự hoán đổi ưu thế bao phủ giữa hai không gian khi mở rộng $k$. |
| **Mốc ngân sách** | Mốc neo, mốc neo cơ sở, mốc chuyển pha | **Ngưỡng ngân sách cơ sở, mốc ngân sách chiến lược** | "Mốc neo", "chuyển pha" là ẩn dụ hàng hải và vật lý nhiệt động học; trong tối ưu hóa tập hợp dùng thuật ngữ ngân sách chuẩn xác. |
| **Từ đệm sáo rỗng** | Năng lực nội tại, chuẩn tắc, liên nhánh | **Khả năng bao phủ, đặc tính giải thuật, chuẩn mực, giữa các cấu hình thực nghiệm** | "Nội tại", "chuẩn tắc", "liên nhánh" là từ ngữ đệm sáo rỗng, mang hơi hướng triết học/hành chính; dùng từ ngữ khoa học chuẩn xác. |
| **Khẩu ngữ & Từ sai ngữ cảnh** | Chọn nốt, làm nốt, nén mạnh độ dư thừa, ép độ dư thừa, giảm động lực chọn, cấp đại diện, vừa cấp thêm đại diện | **Lựa chọn các phân họ hiếm còn lại, giảm đáng kể / cắt giảm độ dư thừa, khiến phần độ tăng cận biên còn lại bị thu hẹp, phân bổ thêm các chuỗi đại diện** | "Chọn nốt" là khẩu ngữ đời thường; "nén mạnh/ép" là từ cơ học dùng sai cho tỷ lệ phần trăm; "cấp đại diện" mang âm hưởng hành chính bao cấp; giải thuật submodular không có "động lực" tâm lý. |
| **Nhầm lẫn phân cấp sinh học** | Các phân họ đa dạng cao, quy luật sinh học sâu sắc | **Một họ protein có độ đa dạng cao và phân tách thành nhiều phân họ; các phân họ quy mô lớn có biến dị trình tự nội nhóm rộng** | Phân biệt rõ cấp độ Họ (Family A1 đa dạng gồm 115 Subfamily) và cấp độ Phân họ lớn (như A01.009 có biến dị nội nhóm rộng); khử cụm từ hoa mỹ "quy luật sinh học sâu sắc". |
| **Tuyên ngôn bão hòa chủ quan & Kết luận sáo rỗng** | Xác lập trạng thái bão hòa, tái khẳng định hoàn toàn quan sát thực nghiệm trong công trình nền tảng (cho phép đo mở rộng), hiệu năng không phụ thuộc vào hệ quy chiếu | **Đánh giá mức độ hội tụ độ bao phủ ở vùng ngân sách cao / Tiệm cận ngưỡng bão hòa bao phủ / Tổng kết trực diện số liệu thực nghiệm** | Không áp đặt chủ quan trạng thái bão hòa trước khi xét số liệu; không gán ghép kết quả của A01.009 hay ESM-2 cho bài báo nền vốn không khảo sát các thành phần này. |

---

## 11. CHUẨN HÓA THUẬT NGỮ TẬP NỀN & QUY TRÌNH SÀNG LỌC VÀ THẨM ĐỊNH DỮ LIỆU (CURATION VS. NORMALIZATION)

1. **Phân định rạch ròi giữa Sàng lọc & Thẩm định dữ liệu (Data Curation / Screening) và Chuẩn hóa (Normalization):**
   - **Chuẩn hóa (*Normalization / Standardization*)**: Dành riêng cho các thao tác biến đổi toán học trên giá trị số, vector đặc trưng hoặc phân phối thống kê (ví dụ: chuẩn hóa vector độ dài đơn vị $L_2$ $\|z\|_2 = 1$, chuẩn hóa Min-Max về $[0, 1]$, chuẩn hóa phân phối $Z$-score, chuẩn hóa Z-score ma trận).
   - **Sàng lọc & Thẩm định dữ liệu (*Data Curation / Screening & Quality Control*)**: Dành riêng cho quy trình thẩm định sinh học, kiểm soát chất lượng (QC), bóc tách nhãn phân loại chính thức và loại bỏ các chuỗi chưa xác định danh tính sinh học (như việc loại bỏ $9.187$ chuỗi `[A01.UPA]` để giữ lại $4.120$ chuỗi thuộc $115$ Subfamily chính thức).

2. **Quy chuẩn gọi tên cho tập nền $V_{\text{curated}}$:**
   - **CẤM DÙNG**: *"Tập nền chuẩn hóa"* (dễ gây ngộ nhận là các chuỗi protein đã bị biến đổi số học/vector hoặc chuẩn hóa thang đo), *"Tập nền tinh tuyển"* (từ "tinh tuyển" mang tính văn học/hoa mỹ, không chuẩn mực khoa học), *"Tập nền sạch"* (khẩu ngữ), *"Subfamily sinh học thực thụ"* (dịch thô).
   - **BẮT BUỘC DÙNG**: **"Tập nền phân họ chính thức"** (*Curated Subfamily Ground Set* / *Official Subfamily Ground Set*). Thuật ngữ này gắn liền trực tiếp với bản chất sinh học của $115$ Subfamily MEROPS và khớp hoàn toàn với ký hiệu giải tích $V_{\text{curated}}$.

3. **Cấm tuyệt đối tên mã phương án kỹ thuật nội bộ (Zero Work-Package Jargon):**
   - **CẤM DÙNG**: Các tên mã phương án phát triển kỹ thuật cục bộ như `Phương án 1`, `Phương án 2`, `Phương án 3A`, `Phương án 3B` trong thân bài báo cáo.
   - **BẮT BUỘC DÙNG**: **"Quy trình sàng lọc và thẩm định dữ liệu phân họ chính thức Curated Subfamilies"** hoặc **"chiến lược thẩm định phân họ chính thức"**.
   - **Bản chất khoa học**: Các tên mã phương án chỉ là công cụ quy ước nội bộ trong giai đoạn lập trình và chạy thực nghiệm; văn bản khoa học chính thức phải mô tả giải pháp dưới dạng một quy trình phương pháp luận hoàn chỉnh, phản ánh đúng thao tác sinh học và kiểm soát chất lượng dữ liệu.

---

## 12. NGUYÊN TẮC PHÂN ĐỊNH ĐÓNG GÓP CỐT LÕI (CORE METHOD) VÀ MODULE KHẢO SÁT MỞ RỘNG (EXPLORATORY MODULE)

1. **Bản chất đóng góp độc lập của RareProtSelect:**
   - Đóng góp phương pháp luận cốt lõi của đề tài là: **Mô hình hàm mục tiêu tối ưu hóa submodular có trọng số nghịch đảo quy mô Subfamily** $F_\alpha(S) = \sum_{v \in V} w_v^{(\alpha)} \max_{s \in S} \mathbf{S}(s, v)$ kết hợp giải thuật Pruned Greedy 90\% vector hóa trên GPU.
   - Về mặt toán học tối ưu hóa tổ hợp, hàm mục tiêu $F_\alpha$ hoàn toàn độc lập với nguồn gốc của ma trận tương đồng $\mathbf{S}$. Hàm mục tiêu này có thể nhận đầu vào là ma trận tương đồng chuỗi rời rạc (NCBI BLASTp), ma trận vector nhúng ngữ nghĩa (ESM-2), hoặc bất kỳ ma trận tương đồng phân tử nào khác.

2. **Định vị chính xác vai trò của mô hình ngôn ngữ protein ESM-2:**
   - ESM-2 **KHÔNG PHẢI** là thành phần bắt buộc của phương pháp RareProtSelect.
   - ESM-2 đóng vai trò là một **Module khảo sát mở rộng độc lập (Plug-and-Play Exploratory Module)** nhằm trả lời câu hỏi nghiên cứu: *"Liệu không gian biểu diễn ngữ nghĩa liên tục từ mô hình ngôn ngữ protein có mang lại lợi ích cộng hưởng nào so với không gian tương đồng chuỗi truyền thống trong bài toán chọn tập protein đại diện hay không?"*.
   - **CẤM TUYỆT ĐỐI**: Đồng nhất phương pháp RareProtSelect với việc bắt buộc phải dùng ESM-2; cấm viết các câu áp đặt thiếu chủ ngữ hoặc khẳng định cưỡng bức như *"RareProtSelect chuyển dịch không gian tương đồng sang ESM-2"*. Bắt buộc diễn đạt rõ: *"RareProtSelect thiết lập module khảo sát mở rộng trên không gian ESM-2..."*.

3. **Nguyên tắc phân định trong thiết kế thực nghiệm và đánh giá:**
   - **Nhóm thực nghiệm cốt lõi (thử nghiệm 1 và thử nghiệm 2)**: Chạy trên không gian tương đồng chuỗi cơ sở (NCBI BLASTp) để chứng minh độc lập năng lực của hàm mục tiêu có trọng số (\textit{ceteris paribus} --- chỉ đổi hàm mục tiêu).
   - **Nhóm thực nghiệm khảo sát mở rộng (thử nghiệm 3, 4, 5, 6)**: Đánh giá đa chiều, đối sánh kiểm tra chéo (ablation study) khi kết hợp với module biểu diễn ESM-2.
   - **Phân định hai bộ thước đo hiệu năng**: Bộ 5 chỉ số Live BLASTp ($E \le 10^{-7}$) là **thước đo sinh học thực nghiệm chuẩn mực**; Bộ 4 chỉ số Within-Subfamily Coverage ESM là **thước đo hình học bổ trợ phục vụ module khảo sát mở rộng**.

4. **Cấm sử dụng ký hiệu trung gian $RQ_1 \dots RQ_5$ chưa định nghĩa**:
   - Tuyệt đối không sử dụng các ký hiệu mã hóa trung gian dạng `$RQ_1 \dots RQ_5$` trong văn bản Chương 3 khi phần Mở đầu đã trình bày dưới dạng 5 Nhiệm vụ nghiên cứu, nhằm tránh trùng lặp nội dung hoặc xuất hiện ký hiệu đột ngột; trình bày trực tiếp theo tên nội dung kiểm chứng thực nghiệm.

5. **Quy chuẩn phân bổ nội dung kiểm chuẩn kỹ thuật dịch tâm Mean-Centering**:
   - Toàn bộ kết quả thực nghiệm kiểm chuẩn kỹ thuật dịch tâm Mean-Centering (hệ số $\beta = 0{,}70$ cân bằng phân phối giá trị tương đồng cosine) được trình bày gọn gàng dưới dạng văn xuôi tại Chương 2 (Mục 2.3.2) ngay sau Thuật toán 2.1.
   - Sang Chương 3, ma trận $\mathbf{S}_{\text{ESM}}^{(\beta=0{,}70)}$ được áp dụng trực tiếp như một tiền đề kỹ thuật đã được kiểm chứng; TUYỆT ĐỐI KHÔNG giải thích lại cơ chế dịch tâm gây trùng lặp nội dung giữa các chương.

6. **Quy chuẩn thiết kế nội dung thử nghiệm 5 và thử nghiệm 6**:
   - **Thử nghiệm 5 (phân bổ vị trí đại diện --- Subfamily Allocation)**: Tuyệt đối không trình bày thử nghiệm 5 dưới danh nghĩa "xác nhận tính nhất quán" hay "kiểm tra tính hợp lệ (Sanity Check)". Bản chất cốt lõi của thử nghiệm 5 là giải thích cơ chế vi mô: hàm mục tiêu có trọng số đã giải phóng sự thiên lệch quy mô của Subfamily lớn nhất (A01.009), tái phân bổ hợp lý các chuỗi đại diện và giảm đáng kể độ dư thừa Subfamily Redundancy từ $50{,}43\%$ xuống $20{,}00\%$ (không dùng từ *"nén mạnh"* hay *"ép độ dư thừa"*).
   - **Thử nghiệm 6 (mở rộng ngân sách đại diện --- Budget Scaling)**: Bắt buộc giải thích rõ cơ sở sinh học (một họ protein có độ đa dạng cao và phân tách thành nhiều phân họ như Family A1, trong đó các phân họ lớn có biến dị nội nhóm rộng cần nhiều chuỗi đại diện) và cấu trúc phân tầng quy mô $115$ Subfamily MEROPS ($45$ hiếm, $32$ trung bình, $38$ lớn) khi lựa chọn 6 mốc ngân sách $k \in \{115, 150, 200, 270, 340, 380\}$. Tách bạch rõ đoạn giải thích quy luật bước nhảy của 6 mốc $k$ với đoạn dẫn nhập số liệu bảng 3.7 tại $k = 380$. Không dùng từ ẩn dụ *"mốc neo"*, không dùng từ hành chính *"cấp thêm đại diện"*, và không gán ghép kết luận của A01.009 hay ESM-2 cho bài báo nền.

---

## 13. QUY CHUẨN 2 TẦNG CHO THUẬT NGỮ CHỈ SỐ ĐO LƯỜNG & MA TRẬN 13 CHỈ SỐ THỰC NGHIỆM ĐỒ ÁN (STANDARDIZED ENGLISH METRIC NOMENCLATURE & 13-METRIC MATRIX)

1. **Nguyên lý chuẩn hóa thuật ngữ 2 tầng (Two-Tier Metric Nomenclature Framework):**
   - **Tầng 1 (Danh xưng chính thức của thước đo - Headers, Labels, Formulas, Section Titles)**:
     - Mọi tên chỉ số kỹ thuật và thực nghiệm **BẮT BUỘC giữ nguyên thuật ngữ tiếng Anh gốc** viết hoa/in nghiêng học thuật chuẩn hóa trong bảng biểu, tiêu đề cột, nhãn đồ thị, chú thích hình và định nghĩa toán học.
     - Ví dụ: `Overall Sensitivity`, `Rare Sensitivity`, `Worst-Group Sensitivity`, `Macro-Average Sensitivity`, `Zero-Sensitivity Count`, `Within-Subfamily Coverage`, `Coverage ESM`, `Worst-Group Coverage ESM`, `Macro-Average Coverage ESM`, `Rare Representation Rate`, `Subfamily Redundancy`.
     - Tuyệt đối **CẤM** dịch tên cột trong bảng thành "Độ nhạy toàn thể", "Độ nhạy nhóm hiếm", "Độ phủ ESM", hay "Độ phủ nội phân họ".
   - **Tầng 2 (Văn phong diễn giải trong thân bài - Body Prose Text)**:
     - Tuyệt đối **CẤM** dịch thô cộc lốc hoặc dùng trơ trọi từ "độ nhạy", "độ phủ" (ví dụ: cấm viết "độ nhạy toàn thể", "đạt 0% độ nhạy", "độ phủ của nhóm hiếm").
     - **Bắt buộc** áp dụng một trong hai hình thức diễn giải sau:
       1. *Đi kèm từ định danh khoa học*: Sử dụng cụm từ định danh rõ ràng như *"chỉ số Overall Sensitivity"*, *"thước đo Rare Sensitivity"*, *"chỉ số Within-Subfamily Coverage"*, *"thước đo hình học Coverage ESM"*.
       2. *Diễn giải thoát ý theo bản chất thao tác thực nghiệm*: Nêu chính xác hành vi sinh học hoặc tính toán thực tế, chẳng hạn *"tỷ lệ nhận diện chuỗi qua Live BLASTp"*, *"tỷ lệ phát hiện chuỗi thành viên của phân họ"*, *"độ bao phủ hình học trong không gian nhúng ngữ nghĩa ESM"*, *"hoàn toàn không có chuỗi nào được nhận diện (đạt 0,0% Sensitivity)"*.

2. **Bản chất khoa học phân biệt giữa Sensitivity (BLASTp) và Coverage (ESM-2):**
   - **Sensitivity (NCBI Live BLASTp, ngưỡng $E \le 10^{-7}$)**:
     - Đây là **thước đo sinh học thực nghiệm chuẩn mực** đo lường năng lực của tập đại diện $S_k$ trong việc "truy vấn tìm kiếm và nhận diện thành công" các chuỗi còn lại trong tập nền qua thuật toán gióng hàng cục bộ BLASTp.
     - Nếu dịch là "độ nhạy", người đọc sẽ liên tưởng sai lầm sang độ nhạy cảm biến vật lý/điện tử (*sensor sensitivity*) hoặc độ nhạy xét nghiệm y tế chẩn đoán bệnh (*diagnostic sensitivity*). Trong ngữ cảnh tin sinh học, bản chất cốt lõi của thước đo này là **tỷ lệ nhận diện chuỗi / tỷ lệ thu hồi chuỗi (recall/identification rate)**.
   - **Coverage (Không gian vector nhúng ngữ nghĩa ESM-2)**:
     - Đây là **thước đo hình học bổ trợ** đo lường mức độ bao bọc của các quả cầu siêu hình học (bán kính tương đồng cosine $\theta$) xung quanh các chuỗi đại diện trong không gian biểu diễn PLM.
     - Cấm dùng từ "độ phủ" đứng cộc lốc, dân dã; bắt buộc dùng **"độ bao phủ"** (*coverage*) hoặc **"tính đại diện hình học"**.

3. **Ma trận tra cứu 13 chỉ số đo lường thực nghiệm toàn đồ án:**
   - Bảng tra cứu dưới đây quy định thống nhất 100% danh xưng chính thức, ký hiệu toán học, bản chất đo lường và mẫu câu diễn giải tiếng Việt chuẩn mực:

| STT | Danh xưng chính thức (Tầng 1) | Ký hiệu / Phép đo | Bản chất đo lường tin sinh - toán học | Văn phong diễn giải chuẩn mực trong thân bài (Tầng 2) |
| :---: | :--- | :--- | :--- | :--- |
| **I** | **Nhóm thước đo sinh học thực nghiệm Live BLASTp ($E \le 10^{-7}$)** | | | |
| 1 | `Overall Sensitivity` / `Sensitivity` ($V_{\text{curated}}$) | $\text{Sens}(S_k, V) = \frac{\lvert \{v \in V \mid \max_{s \in S_k} \text{hit}(s, v) = 1\} \rvert}{\lvert V \rvert}$ | Tỷ lệ phần trăm tổng số chuỗi trong toàn bộ tập nền $V_{\text{curated}}$ được tìm thấy và nhận diện bởi ít nhất 1 chuỗi đại diện qua Live BLASTp. | "chỉ số Overall Sensitivity" / "tỷ lệ nhận diện chuỗi qua Live BLASTp trên toàn bộ tập nền" |
| 2 | `Common / Medium / Rare Subfamily Sensitivity` | $\text{Sens}(S_k, G_{\text{group}})$ với $G \in \{\text{Common}, \text{Medium}, \text{Rare}\}$ | Tỷ lệ nhận diện chuỗi phân tách theo từng tầng quy mô phân họ (Lớn $\ge 50$, Trung bình $10 - 49$, Hiếm $< 10$ chuỗi). | "thước đo Sensitivity trên nhóm phân họ lớn / trung bình / hiếm" / "tỷ lệ nhận diện chuỗi trong các phân họ hiếm" |
| 3 | `Worst-Group Sensitivity` | $\min_{g \in G} \text{Sens}(S_k, V_g)$ | Tỷ lệ nhận diện chuỗi của phân họ có kết quả thấp nhất trong toàn bộ 115 Subfamily chính thức. | "chỉ số Worst-Group Sensitivity của phân họ yếu nhất" / "tỷ lệ nhận diện của phân họ có độ bao phủ thấp nhất" |
| 4 | `Macro-Average Sensitivity` | $\frac{1}{\lvert G \rvert} \sum_{g \in G} \text{Sens}(S_k, V_g)$ | Trung bình cộng không trọng số của tỷ lệ nhận diện chuỗi trên toàn bộ 115 Subfamily (đối xử bình đẳng mọi phân họ bất kể quy mô). | "chỉ số trung bình vĩ mô Macro-Average Sensitivity" / "tỷ lệ nhận diện chuỗi trung bình giữa các phân họ" |
| 5 | `Zero-Sensitivity Count` | $\lvert \{g \in G \mid \text{Sens}(S_k, V_g) = 0\} \rvert$ | Số lượng phân họ hoàn toàn không có bất kỳ chuỗi nào được nhận diện bởi tập đại diện (bị bỏ sót $100\%$). | "số lượng phân họ có chỉ số Sensitivity bằng 0" / "số phân họ hoàn toàn không được nhận diện qua Live BLASTp" |
| **II** | **Nhóm thước đo hình học ngữ nghĩa ESM-2 (Module khảo sát mở rộng)** | | | |
| 6 | `Within-Subfamily Coverage` (ESM-2) | $\text{Cov}_{\text{within}}(S_k, V) = \frac{\lvert \{v \in V \mid \max_{s \in S_k \cap V_{g(v)}} \mathbf{S}(s, v) \ge \theta\} \rvert}{\lvert V \rvert}$ | Tỷ lệ chuỗi được bao phủ bởi đại diện thuộc đúng cùng phân họ trong không gian vector nhúng ESM-2 (ngăn chặn sai lệch bao phủ chéo). | "chỉ số Within-Subfamily Coverage nội phân họ" / "độ bao phủ chuỗi cùng phân họ trong không gian ESM-2" |
| 7 | `Coverage ESM` / `Overall Coverage` | $\text{Cov}(S_k, V) = \frac{\lvert \{v \in V \mid \max_{s \in S_k} \mathbf{S}(s, v) \ge \theta\} \rvert}{\lvert V \rvert}$ | Tỷ lệ bao phủ hình học toàn cục trong không gian biểu diễn ESM-2 (cho phép bao phủ chéo ngoài ranh giới phân họ). | "chỉ số Coverage ESM toàn cục" / "độ bao phủ hình học toàn thể trong không gian ngữ nghĩa ESM-2" |
| 8 | `Worst-Group Coverage ESM` | $\min_{g \in G} \text{Cov}_{\text{within}}(S_k, V_g)$ | Độ bao phủ nội phân họ của Subfamily có giá trị thấp nhất trong không gian vector nhúng ESM-2. | "chỉ số Worst-Group Coverage ESM" / "độ bao phủ nội phân họ của Subfamily thấp nhất trên không gian ESM-2" |
| 9 | `Macro-Average Coverage ESM` | $\frac{1}{\lvert G \rvert} \sum_{g \in G} \text{Cov}_{\text{within}}(S_k, V_g)$ | Trung bình cộng không trọng số của độ bao phủ nội phân họ trên toàn bộ 115 Subfamily trong không gian ESM-2. | "chỉ số trung bình vĩ mô Macro-Average Coverage ESM" / "độ bao phủ nội phân họ trung bình giữa các Subfamily trên không gian ESM-2" |
| **III** | **Nhóm thước đo phân bổ đại diện & tối ưu hóa tập hợp** | | | |
| 10 | `Rare Representation Rate` | $\frac{\lvert \{g \in G_{\text{rare}} \mid S_k \cap V_g \ne \emptyset\} \rvert}{\lvert G_{\text{rare}} \rvert}$ | Tỷ lệ phần trăm các phân họ hiếm ($n_g < 10$) sở hữu ít nhất 1 chuỗi đại diện được lựa chọn vào tập $S_k$. | "tỷ lệ hiện diện của nhóm hiếm Rare Representation Rate" / "tỷ lệ phân họ hiếm có đại diện trong tập tuyển chọn" |
| 11 | `Subfamily Redundancy` | $1 - \frac{\lvert \{g \in G \mid S_k \cap V_g \ne \emptyset\} \rvert}{k}$ | Mức độ dư thừa đại diện khi một phân họ có nhiều hơn 1 chuỗi đại diện trong tập $S_k$. | "chỉ số dư thừa phân họ Subfamily Redundancy" / "mức độ tập trung đại diện vào các phân họ lớn" |
| 12 | `Consensus Rank / Selection Count` | $\text{Count}(u) = \sum_{m=1}^M \mathbb{I}[u \in S_k^{(m)}]$ | Tần suất xuất hiện và tổng thứ hạng của chuỗi qua $M$ lần chạy lấy mẫu phụ (subsampling) để đánh giá độ bền vững thống kê. | "chỉ số đồng thuận Consensus Selection Count" / "tần suất được lựa chọn qua các lần chạy lấy mẫu phụ" |
| 13 | `Runtime & Peak Memory` | Thời gian chạy (giây) và bộ nhớ GPU/RAM đỉnh (MB) | Hiệu năng tính toán và mức độ tối ưu hóa tài nguyên phần cứng của giải thuật Pruned Greedy so với Standard Greedy. | "thời gian thực thi Runtime và mức tiêu thụ bộ nhớ đỉnh Peak Memory" |

---

## 14. KỶ LUẬT VĂN PHONG HỌC THUẬT: KHỬ TRIỆT ĐỂ ẨN DỤ QUÂN SỰ, THỂ THAO, BÁO CHÍ ĐIỀU TRA & KHẨU NGỮ PHÒNG LAB (SCHOLARLY RIGOR & ZERO SENSATIONALISM)

1. **Nguyên lý Khách quan Khoa học & Chống Kịch tính hóa (Objective Scholarly Neutrality):**
   - Đồ án khoa học liên ngành là bản báo cáo toán học tối ưu và tin sinh học chính xác, điềm tĩnh, trung lập và khiêm tốn nhận thức.
   - **TUYỆT ĐỐI CẤM** vay mượn từ ngữ, ẩn dụ hoặc khẩu ngữ từ 7 miền ngữ cảnh phi học thuật:
     1. *Ẩn dụ quân sự / chiến trường*: `mặt trận`, `Mặt trận 1`, `Mặt trận 2`, `vũ khí chủ lực`, `đối đầu trực diện`.
     2. *Ẩn dụ thể thao / trò chơi điện tử*: `áp đảo hoàn toàn`, `dẫn trước áp đảo`, `vượt lên dẫn trước`, `mở khóa thành công`.
     3. *Văn phong báo chí giật gân / điều tra tố tụng*: `vạch trần`, `bóc trần`, `dưới vỏ bọc`, `sự bứt phá mang tính bước ngoặt`, `nguyên nhân sâu xa bắt nguồn từ`.
     4. *Nhân hóa cứu trợ / ủy mị tình cảm*: `giải cứu thành công`, `giải cứu Subfamily`, `bỏ rơi` (dùng như trẻ em bị bỏ rơi).
     5. *Thuật ngữ kinh tế thị trường / luật chống độc quyền*: `sự độc quyền của nhóm lớn`, `hóa giải sự độc quyền`, `thâu tóm`.
     6. *Khẩu ngữ phòng lab / hình tượng hóa bình dân*: `dùng làm mồi` (để chỉ query BLAST), `nằm sát đáy`, `tăng dốc đứng`, `tăng vọt`, `nhảy trực tiếp sang`, `hàng chục`, `mang tính cảm tính`, `các tác giả đi trước`, `bão hòa sâu`.
     7. *Văn phong tự mãn tiếp thị / quảng bá*: `tính ưu việt`, `chứng minh tính đúng đắn`, `tuyệt đối`, `giải quyết dứt điểm`.

2. **Chuẩn hóa Thao tác Tin sinh học: Query Sequence vs. Primer (Chuỗi truy vấn vs. Mồi):**
   - Trong thuật toán BLASTp, `query sequence` là chuỗi trình tự protein được đưa vào làm mẫu để tìm kiếm các chuỗi tương đồng trong cơ sở dữ liệu (*subject / target database*).
   - Việc dịch `query sequence` thành *"chuỗi mồi"* hoặc *"dùng làm mồi để truy vấn"* là sai lệch kiến thức sinh học phân tử nghiêm trọng (gây ngộ nhận sang mồi PCR *primer* trong phản ứng khuếch đại DNA) và mang khẩu ngữ săn bắt, bẫy rập.
   - **BẮT BUỘC DÙNG**: **"chuỗi truy vấn"** (*query sequence*) hoặc **"sử dụng làm chuỗi truy vấn để đối soát"**.

3. **Kỷ luật Miêu tả Động học Đồ thị & Hàm số Thực nghiệm (Mathematical Graph Kinetics):**
   - Tuyệt đối cấm các từ ngữ hình tượng dân dã miêu tả đường cong: *"nằm sát đáy"*, *"tăng dốc đứng"*, *"tăng vọt"*, *"nhảy bước"*.
   - Bắt buộc sử dụng ngôn ngữ giải tích hàm số chuẩn xác: *"duy trì ở mức $0{,}0\%$ trên toàn bộ khoảng"*, *"tăng trưởng nhanh ngay từ mốc"*, *"đạt mức tăng trưởng"*, *"chuyển dịch tối ưu sang lựa chọn"*.

4. **Bảng Đối chiếu Cấm kỵ và Chuyển đổi Bắt buộc giữa Văn phong Tệ và Văn phong Chuẩn mực:**

| Nhóm vi phạm | Từ ngữ tệ / Cấm sử dụng (`BLACKLIST`) | Bản dịch & Văn phong chuẩn mực (`MANDATORY`) | Bản chất khoa học & Lý do cấm |
| :--- | :--- | :--- | :--- |
| **Ẩn dụ quân sự** | Mặt trận 1, Mặt trận 2, hai mặt trận, vũ khí thực nghiệm chủ lực | **Hệ quy chiếu đo đạc thứ nhất / thứ hai; hai nhóm không gian đánh giá; tập dữ liệu thực nghiệm trọng tâm** | Khoa học không phải là chiến trường; phân tích thực nghiệm là các phép đo trên các không gian metric khác nhau. |
| **Ẩn dụ thể thao** | Đối đầu trực diện, áp đảo hoàn toàn, dẫn trước áp đảo, vượt lên dẫn trước | **Đối sánh tương quan hai chiều, vượt trội hơn từ $1{,}6$ đến $4{,}0$ lần, đạt giá trị cao hơn** | Thuật toán tối ưu không phải trận đấu thể thao; đây là phép so sánh định lượng giữa hai phương pháp. |
| **Thuật ngữ game** | Mở khóa, mở khóa thành công, kích hoạt nhóm hiếm | **Bắt đầu lựa chọn được đại diện của nhóm hiếm, giúp nhóm hiếm có chuỗi đại diện** | Tránh lạm dụng thuật ngữ trò chơi điện tử (*unlock/activate*); bản chất là nghiệm tối ưu bắt đầu gán phần tử thuộc $V_g$. |
| **Báo chí giật gân** | Vạch trần, bóc trần, dưới vỏ bọc chỉ số toàn thể cao | **Làm sáng tỏ, chỉ ra, phát hiện; bị che khuất đằng sau chỉ số toàn thể** | "Vạch trần", "dưới vỏ bọc" mang văn phong tố tụng hình sự, đạo đức giả; nghiên cứu khoa học cần sự điềm tĩnh và trung lập. |
| **Cứu trợ ủy mị** | Giải cứu 35 Subfamily, bỏ rơi 58 Subfamily (dùng lặp lại) | **Khôi phục tính đại diện cho 35 Subfamily; để sót / không có chuỗi nào được nhận diện** | Protein và Subfamily là thực thể phân tử, không có tâm lý hay cảm xúc để được "giải cứu" hay bị "bỏ rơi". |
| **Kinh tế độc quyền** | Sự độc quyền của nhóm lớn, hóa giải sự độc quyền | **Sự thiên lệch quy mô mẫu, sự tập trung đại diện quá mức vào nhóm lớn** | Phân bố kích thước phân họ là đặc trưng sinh học tiến hóa, không phải hiện tượng lũng đoạn thị trường hay độc quyền thương mại. |
| **Khẩu ngữ truy vấn** | Dùng làm mồi, chuỗi mồi | **Chuỗi truy vấn (Query sequence), sử dụng làm chuỗi truy vấn để đối soát Live BLASTp** | "Mồi" gây nhầm lẫn với mồi PCR (*primer*) và mang khẩu ngữ câu cá; bắt buộc dùng thuật ngữ tin sinh học "chuỗi truy vấn". |
| **Hình tượng bình dân** | Nằm sát đáy, tăng dốc đứng, tăng vọt, nhảy trực tiếp sang | **Duy trì ở mức $0{,}0\%$, tăng trưởng nhanh ngay từ mốc, chuyển dịch tối ưu sang** | Dùng ngôn ngữ giải tích hàm số và tối ưu hóa tổ hợp chuẩn xác thay vì các từ ngữ tả cảnh cảm tính. |
| **Mở rộng ngân sách** | Khảo sát bão hòa sâu, dải ngân sách sâu, động học bão hòa | **Quá trình bão hòa độ bao phủ khi mở rộng quy mô ngân sách, khi mở rộng tập đại diện** | "Bão hòa sâu" là biến tướng của cụm từ cấm "dải ngân sách sâu"; "động học bão hòa" mượn thuật ngữ hóa lý/động học enzyme không tự nhiên trong ngữ cảnh tối ưu hóa tập hợp. |
| **Chủ quan cảm tính** | Mang tính cảm tính, các tác giả đi trước | **Dựa trên kinh nghiệm chủ quan (Heuristic), công trình nền tảng / nghiên cứu tiền đề** | Tránh khẩu ngữ đời thường; sử dụng thuật ngữ phương pháp luận chuẩn xác. |
| **Tự mãn quảng bá** | Tính ưu việt, chứng minh tính đúng đắn, tuyệt đối | **Tính hiệu quả thực nghiệm, giải quyết sự đánh đổi, minh chứng tính khả thi** | Tuân thủ nguyên tắc khiêm tốn nhận thức (Epistemic Humility); khoa học chỉ kiểm chứng trong phạm vi thực nghiệm cụ thể. |
| **Dịch máy thiếu tự nhiên** | Động học bão hòa, động học tích lũy, giao cắt hiệu năng, mốc chuyển pha | **Quá trình bão hòa độ bao phủ, sự tích lũy số lượng đại diện, sự đảo chiều về hiệu năng, mốc ngân sách chiến lược** | Mượn thuật ngữ vật lý/hóa học sai ngữ cảnh và dịch máy thô ráp; dùng ngôn ngữ giải tích hàm số và tối ưu hóa tổ hợp chuẩn xác. |
| **Từ đệm sáo rỗng** | Năng lực nội tại, chuẩn tắc, liên nhánh, mốc neo | **Khả năng bao phủ, chuẩn mực, giữa các cấu hình thực nghiệm, ngưỡng ngân sách cơ sở** | Khử các từ đệm sáo rỗng, lai căng triết học hoặc ẩn dụ hàng hải trong phân tích thực nghiệm. |
| **Khẩu ngữ & Từ sai ngữ cảnh** | Chọn nốt, nén mạnh, giảm động lực, xác lập trạng thái bão hòa, cấp đại diện | **Lựa chọn các phân họ còn lại, cắt giảm đáng kể, suy giảm ưu thế độ tăng cận biên, tiệm cận ngưỡng bão hòa, phân bổ thêm đại diện** | Khử khẩu ngữ, từ mượn cơ học/tâm lý sai ngữ cảnh, từ ngữ hành chính bao cấp và tuyên ngôn chủ quan. |
| **Nhầm lẫn phân cấp sinh học** | Các phân họ đa dạng cao, quy luật sinh học sâu sắc | **Một họ protein có độ đa dạng cao và gồm nhiều phân họ** | Gọi đúng thực thể sinh học: một họ protein đa dạng gồm nhiều phân họ. |

---

## 15. KỶ LUẬT MẠCH VĂN LIÊN ĐOẠN, KẾT LUẬN THỰC NGHIỆM TỰ CHỨA & CHUẨN XÁC CẤP ĐỘ PHÂN LOẠI SINH HỌC (INTER-PARAGRAPH FLOW, SELF-CONTAINED CONCLUSIONS & TAXONOMIC PRECISION)

Mục này hệ thống hóa các quy tắc bắt buộc về cấu trúc lập luận cấp đoạn văn (paragraph-level discourse) nhằm ngăn chặn triệt để tình trạng câu văn rời rạc, chuyển ý gãy khúc giữa các đoạn liền kề, hoặc kết luận tối nghĩa.

### 1. Nguyên tắc Kết luận Thực nghiệm Tự chứa & Cấm Gán ghép Vô căn cứ (Self-Contained & Data-Grounded Conclusions)
- **Định nghĩa**: Câu kết luận ở cuối mỗi đoạn văn phân tích bảng biểu hoặc cuối mỗi tiểu mục thực nghiệm bắt buộc phải **tự chứa (Self-Contained)** — tức là người đọc chỉ cần đọc câu kết đó cùng với các con số trong đoạn là hiểu trọn vẹn phát hiện khoa học mà không phải đoán ẩn ý.
- **Ba điều cấm tuyệt đối khi viết câu kết luận**:
  1. **Cấm viết câu kết tự mâu thuẫn với số liệu vừa nêu**: Ví dụ, ở thử nghiệm 4, sau khi phân tích rõ ESM-2 ưu thế ở $k \le 75$ còn BLASTp ưu thế ở $k = 115$, tuyệt đối CẤM kết luận rằng *"hiệu năng không phụ thuộc vào hệ quy chiếu hay không gian tối ưu hóa ban đầu"*. Phải kết luận đúng bản chất hai chiều: *"việc đưa trọng số $\alpha = 0{,}5$ vào hàm mục tiêu giúp cải thiện nhất quán độ bao phủ nhóm hiếm trên cả hai không gian biểu diễn, trong đó không gian ESM-2 phát huy ưu thế ở vùng ngân sách thấp ($k \le 75$) còn không gian BLASTp đạt hiệu quả bao phủ phân họ đầy đủ hơn khi ngân sách tiến tới quy mô phân họ ($k = 115$)"*.
  2. **Cấm gán ghép vô căn cứ cho công trình nền tảng**: Tuyệt đối CẤM viết các câu như *"tái khẳng định hoàn toàn quan sát thực nghiệm trong công trình nền tảng \cite{nguyen2025}"* ở cuối các đoạn phân tích riêng về phân họ `A01.009` hoặc không gian nhúng `ESM-2`, vì bài báo nền `nguyen2025` không khảo sát riêng phân họ `A01.009` hay mô hình `ESM-2`.
  3. **Cấm dùng mệnh đề trừu tượng chung chung không gắn với chỉ số**: Câu kết bắt buộc phải neo trực tiếp vào các chỉ số cốt lõi vừa phân tích (như tỷ lệ phân họ hiếm có đại diện đạt $93{,}33\%$, số lượng đại diện phân bổ cho `A01.009` tăng lên $6$ và $22$ chuỗi).

### 2. Nguyên tắc Liên kết Mạch văn Giữa Các Đoạn Liền kề & Tách bạch Thiết kế vs. Kết quả (Inter-Paragraph Flow & Design-Result Separation)
- **Quy tắc đọc ngữ cảnh 3 đoạn (Three-Paragraph Context Window)**: Khi chỉnh sửa bất kỳ một câu nào trong văn bản LaTeX, bắt buộc phải đọc xuyên suốt **đoạn liền trước, đoạn đang sửa và đoạn liền sau** để bảo đảm mạch văn trôi chảy, không bị lặp ý hoặc đứt gãy logic chuyển đoạn.
- **Tách bạch chức năng giữa Đoạn Thiết kế (Setup) và Đoạn Kết quả (Results)**:
  - **Đoạn giải thích thiết kế tham số / bước nhảy ngân sách**: Phải duy trì cấu trúc câu liệt kê song hành đồng nhất từ mốc đầu tiên đến mốc cuối cùng. Tại mốc cuối cùng (như $k = 380$), chỉ giải thích quy luật số học (bổ sung thêm $40$ vị trí để phân bổ đại diện thứ sáu cho khối $38$ phân họ lớn) và nêu **mục đích khảo sát** (*"nhằm đánh giá mức độ hội tụ của độ bao phủ ở vùng ngân sách cao"*). **TUYỆT ĐỐI KHÔNG** nhảy sang tuyên bố kết quả thực nghiệm (*"xác lập trạng thái bão hòa"* hay *"104/115 Subfamily đạt 100%"*) ngay trong đoạn thiết kế.
  - **Đoạn dẫn nhập và phân tích kết quả**: Nằm ngay sau đoạn thiết kế, mở đầu bằng câu dẫn nhập bảng/hình và trình bày trực tiếp số liệu thực nghiệm tại mốc đó (ví dụ: *"Tại mốc ngân sách $k = 380$, dữ liệu thực nghiệm tại bảng~\ref{tab:exp6\_k380} ghi nhận $104$ trên $115$ Subfamily chính thức đạt tỷ lệ nhận diện tuyệt đối $100\%$ Sensitivity..."*). Cách tổ chức này giúp hai đoạn nối tiếp nhau tự nhiên theo đúng trình tự *Mục đích thiết kế $\to$ Số liệu kết quả đạt được*, không bị lặp số liệu.

### 3. Nguyên tắc Chuẩn xác Cấp độ Phân loại Sinh học: Họ Đa dạng vs. Phân họ Lớn (Family vs. Subfamily Taxonomic Precision)
- **Bản chất sinh học trong MEROPS**:
  - Cấp độ **Họ (`Family`, như `Family A1`)**: Là một họ enzyme lớn có mức độ đa dạng tiến hóa cao và phân tách thành nhiều phân họ (`115 Subfamily` chính thức).
  - Cấp độ **Phân họ (`Subfamily`, như `A01.009`)**: Là một nhánh phân loại con nằm trong Họ; các phân họ có quy mô mẫu lớn (gồm hàng trăm chuỗi protein từ nhiều loài sinh vật) thường có mức độ biến dị trình tự nội nhóm rộng nên một chuỗi đại diện đơn lẻ không thể nhận diện hết toàn bộ thành viên trong phân họ đó.
- **Quy tắc diễn đạt bắt buộc**:
  - **CẤM VIẾT**: *"các phân họ đa dạng cao luôn đòi hỏi nhiều chuỗi đại diện"*.
  - **BẮT BUỘC VIẾT**: *"một họ protein có độ đa dạng cao và phân tách thành nhiều phân họ như Family A1 luôn đòi hỏi ngân sách đại diện lớn hơn số lượng phân họ"*, hoặc *"các phân họ quy mô lớn có mức độ biến dị trình tự nội nhóm rộng như A01.009 cần nhiều hơn một chuỗi đại diện"*.

### 4. Nguyên tắc Giải thích Cơ chế Toán học Thuần khiết — Khử Tâm lý học, Cơ học Sai chỗ & Hành chính Bao cấp
- **Giải thích sự suy giảm độ tăng cận biên trên ma trận đặc vs. ma trận thưa**:
  - Không dùng từ tâm lý học (*"làm giảm động lực chọn"*) hay khẩu ngữ (*"chọn nốt"*).
  - Phải giải thích rõ bằng cấu trúc toán học của hàm Facility Location $F_\alpha(S)$: Trong ma trận đặc $\mathbf{S}_{\text{ESM}}^{(\beta=0{,}70)}$ có nền tương đồng cơ sở dương, các phân họ hiếm đã nhận được một phần giá trị bao phủ nền từ đại diện của các nhóm khác, **khiến phần độ tăng cận biên còn lại khi chọn trực tiếp chuỗi thuộc phân họ hiếm bị thu hẹp và nhỏ hơn tổng độ tăng cận biên tích lũy khi chọn thêm đại diện thứ hai, thứ ba cho các phân họ quy mô lớn**. Ngược lại, trong ma trận thưa $\mathbf{S}_{\text{BLAST}}$, độ tương đồng giữa các phân họ khác nhau bằng $0$, nên một phân họ hiếm chưa có đại diện giữ nguyên toàn bộ độ tăng cận biên tối đa để giải thuật ưu tiên lựa chọn.

### 5. Bảng Đối chiếu Thực tế: Các Mẫu Câu Lỗi và Bản Chuẩn Hóa Mẫu Mực (Casebook)

| Ngữ cảnh thực nghiệm | Mẫu câu lỗi thực tế đã gặp (`BAD / PROHIBITED`) | Bản chuẩn hóa mẫu mực (`GOOD / MANDATORY`) | Phân tích lỗi & Bài học rút ra |
| :--- | :--- | :--- | :--- |
| **Giải thích cơ chế thử nghiệm 4 (ESM-2 vs BLASTp)** | "...làm giảm động lực chọn nốt 18 phân họ hiếm còn lại so với ma trận thưa..." | "...khiến phần độ tăng cận biên còn lại khi chọn trực tiếp chuỗi thuộc phân họ hiếm bị thu hẹp và nhỏ hơn tổng độ tăng cận biên tích lũy khi chọn thêm đại diện thứ hai, thứ ba cho các phân họ quy mô lớn..." | Khử khẩu ngữ *"chọn nốt"* và nhân hóa *"động lực"*; làm rõ phép so sánh độ tăng cận biên giữa việc chọn chuỗi nhóm hiếm với chọn thêm đại diện cho nhóm lớn. |
| **Câu kết luận thử nghiệm 4 (kiểm chứng chéo $2 \times 2$)** | "...khẳng định rằng hiệu năng của phương pháp đề xuất bắt nguồn từ cấu trúc toán học của hàm mục tiêu có trọng số chứ không phụ thuộc vào hệ quy chiếu hay không gian tối ưu hóa ban đầu." | "Kết quả kiểm chứng chéo $2 \times 2$ cho thấy việc đưa trọng số $\alpha = 0{,}5$ vào hàm mục tiêu giúp cải thiện nhất quán độ bao phủ nhóm hiếm trên cả hai không gian biểu diễn, trong đó không gian ESM-2 phát huy ưu thế ở vùng ngân sách thấp ($k \le 75$) còn không gian BLASTp đạt hiệu quả bao phủ phân họ đầy đủ hơn khi ngân sách tiến tới quy mô phân họ ($k = 115$)." | Mẫu câu cũ tối nghĩa và tự mâu thuẫn với số liệu bảng. Bản chuẩn hóa tổng kết trực diện, tự chứa và chính xác theo đúng hai vùng ngân sách. |
| **Mô tả giảm dư thừa thử nghiệm 5 (`Subfamily Redundancy`)** | "...nén mạnh độ dư thừa phân bổ từ 50,43% xuống chỉ còn 20,00%..." / "...ép độ dư thừa từ 50,43% xuống 20,00%..." | "...giảm đáng kể độ dư thừa phân bổ từ $50{,}43\%$ xuống còn $20{,}00\%$..." / "...cắt giảm chỉ số Subfamily Redundancy từ $50{,}43\%$ xuống $20{,}00\%$..." | Từ *"nén mạnh"*, *"ép"* là thuật ngữ cơ học/vật lý dùng sai ngữ cảnh cho tỷ lệ phần trăm thống kê. |
| **Mở đầu thử nghiệm 6 (bối cảnh sinh học)** | "...đối với các phân họ protein có mức độ đa dạng tiến hóa cao như Family A1..." | "...đối với một họ protein có độ đa dạng cao và phân tách thành nhiều phân họ như Family A1..." | `Family A1` là một **họ protein (Family)** gồm $115$ phân họ, không phải là *"các phân họ"*. |
| **Chuyển đoạn giữa Đoạn 2 và Đoạn 3 thử nghiệm 6 ($k = 380$)** | *Cuối đoạn 2*: "Mốc ngân sách cực đại $k = 380$ xác lập trạng thái bão hòa trên toàn siêu họ." $\to$ *Đầu đoạn 3*: "Tại mốc ngân sách cực đại $k = 380$, dữ liệu tại Bảng 3.7..." | *Cuối đoạn 2*: "Cuối cùng, mốc $k = 380$ bổ sung thêm $40$ vị trí để phân bổ đại diện thứ sáu cho khối phân họ lớn, nhằm đánh giá mức độ hội tụ của độ bao phủ ở vùng ngân sách cao." $\to$ *Đầu đoạn 3*: "Tại mốc ngân sách $k = 380$, dữ liệu thực nghiệm tại bảng~\ref{tab:exp6\_k380} ghi nhận $104$ trên $115$ Subfamily chính thức đạt tỷ lệ nhận diện tuyệt đối $100\%$ Sensitivity..." | Giữ cấu trúc liệt kê bước nhảy đồng nhất ở cuối đoạn 2, bỏ nhận định chủ quan *"xác lập trạng thái bão hòa"*, và nối mạch tự nhiên sang kết quả thực nghiệm ở đầu đoạn 3. |
| **Câu mở đầu và kết luận sau bảng 3.7 thử nghiệm 6** | "Kết quả tại Bảng 3.7 xác nhận quy luật sinh học sâu sắc: các phân họ đa dạng cao luôn đòi hỏi nhiều chuỗi đại diện. Việc mở rộng ngân sách... vừa cấp thêm đại diện... tái khẳng định hoàn toàn quan sát thực nghiệm trong công trình nền tảng." | "Số liệu tại bảng~\ref{tab:exp6\_k380} cho thấy rõ cơ chế phân bổ đại diện trên một họ protein đa dạng gồm nhiều phân họ: khi mở rộng ngân sách lên $k = 380$, hàm mục tiêu có trọng số ($\alpha = 0{,}5$) vừa duy trì được sự hiện diện của các phân họ hiếm ở mức $93{,}33\%$, vừa phân bổ thêm các chuỗi đại diện ($6$ chuỗi trên không gian BLASTp và $22$ chuỗi trên không gian ESM-2) để bao phủ toàn diện các phân họ quy mô lớn có biến dị nội nhóm rộng." | Khử câu mở đầu hoa mỹ *"quy luật sinh học sâu sắc"*, khử từ hành chính *"vừa cấp thêm đại diện"*, và xóa bỏ câu kết tối nghĩa gán ghép vô căn cứ cho công trình nền tảng. |

---

## 16. QUY CHUẨN CHÍNH TẢ VIẾT HOA TIẾNG VIỆT TRONG BÁO CÁO KHOA HỌC (VIETNAMESE CAPITALIZATION RIGOR)

1. **Nguyên tắc cốt lõi**:
   - Trong văn bản học thuật tiếng Việt, **chỉ viết hoa chữ cái đầu câu và danh từ riêng** (tên người, địa danh, tên riêng của mô hình/cơ sở dữ liệu như MEROPS, BLASTp, ESM-2, Nemhauser, RareProtSelect).
   - Tuyệt đối **CẤM** phong cách viết hoa từng từ (*Title Case*) của tiếng Anh trong mọi tiêu đề chương (`\chapter`), tiêu đề mục (`\section`, `\subsection`), chú thích bảng/hình (`\caption`), sau dấu hai chấm `:`, hoặc sau dấu gạch ngang giải thích `---`.

2. **Quy chuẩn danh từ chung đi kèm số thứ tự khi đứng giữa câu**:
   - Khi đứng giữa câu, các danh từ chung đi kèm số thứ tự hoặc số hiệu **bắt buộc viết thường**: `thử nghiệm 1..6`, `chương 1..4`, `mục 2.1`, `bảng 3.1`, `hình 3.1`, `thuật toán 2.1`, `định lý 2.1`, `bổ đề 2.1`, `hệ quả 2.1`, `công thức~\eqref{...}`, `bất đẳng thức`, `biểu thức`, `giảng viên hướng dẫn`, `khoa`, `hội đồng đánh giá`.
   - Chỉ viết hoa khi từ đó đứng ở đầu câu, đầu tiêu đề mục hoặc đầu ô bảng.

3. **Thuật ngữ toán học, thuật toán và phương pháp luận**:
   - Các từ như `submodular`, `cosine`, `\textit{ceteris paribus}` bắt buộc viết thường khi đứng giữa câu (trừ khi là danh xưng viết tắt chính thức như PLM, MSA, QC).
   - Không lạm dụng viết hoa các cụm từ tiếng Anh dịch nghĩa ở giữa câu.

4. **Ranh giới đầu câu / đầu đoạn văn vs. giữa câu (Chống lỗi Over-lowercasing)**:
   - Khi `Bảng~\ref{...}`, `Hình~\ref{...}`, `Công thức~\eqref{...}`, `Thử nghiệm 1..6`, `Chương 1..4`, `Mục 2.1` đứng ở **đầu câu mới** (ngay sau dấu chấm `. `) hoặc đứng ở **đầu đoạn văn mới** (ngay sau dòng trống `\n\n`, hoặc sau các khối môi trường đóng như `\end{equation}`, `\end{table}`, `\end{figure}`), chữ cái đầu tiên **bắt buộc phải viết hoa**.
   - Khi đứng sau bất kỳ từ nào khác trong câu (như `tại bảng~\ref{...}`, `ở hình~\ref{...}`, `trong hình~\ref{...}`, `theo công thức~\eqref{...}`, `kết quả thử nghiệm 2`), chữ cái đầu tiên **bắt buộc phải viết thường**.

5. **Quy tắc viết hoa trong tiêu đề bảng và ô bảng**:
   - Trong mỗi ô tiêu đề cột (`\textbf{...}`), chỉ viết hoa chữ cái đầu tiên của ô và danh từ riêng/thuật ngữ tiếng Anh gốc.
   - Các danh từ chung đứng giữa cụm từ trong ô bảng bắt buộc viết thường: ví dụ viết `\textbf{Công bố hình 8A (\%)}` (chữ "hình" viết thường), cấm viết `\textbf{Công bố Hình 8A (\%)}`.

6. **Nhắc lại và liên kết quy chuẩn phông chữ (Mục 9)**:
   - Tuyệt đối cấm sử dụng `\texttt` cho nhãn phân họ sinh học (`A01.009`, `[A01.UPA]`) và tên tệp dữ liệu (`MEROPS\_A1A.fasta`). Khi viết thêm đoạn văn mới hoặc cập nhật nội dung, phải kiểm tra để không vô tình đưa `\texttt` vào nhãn sinh học.

7. **Bảng Casebook đối chiếu 8 lỗi thực tế từ đợt kiểm toán đối kháng (Red Loop)**:

| STT | Vị trí / Ngữ cảnh | Mẫu câu lỗi thực tế (`BAD`) | Bản chuẩn hóa chính xác (`GOOD`) | Phân tích lỗi & Cơ chế phòng ngừa |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Sau dấu chấm kết thúc câu | `...tại $k = 115$. hình~\ref{fig:exp4_crossover} cho thấy...` | `...tại $k = 115$. Hình~\ref{fig:exp4_crossover} cho thấy...` | Lỗi Over-lowercasing: Danh từ chung đứng đầu câu mới sau dấu chấm bắt buộc viết hoa. |
| 2 | Mở đầu đoạn văn sau khối toán | `\end{equation}\n\ncông thức~\eqref{eq:sim_esm}...` | `\end{equation}\n\nCông thức~\eqref{eq:sim_esm}...` | Lỗi Over-lowercasing: Mở đầu đoạn văn mới sau môi trường `equation` bắt buộc viết hoa chữ cái đầu. |
| 3 | Sau dấu chấm kết thúc câu | `...tại $k = 380$. bảng~\ref{tab:exp6_k380} tổng hợp...` | `...tại $k = 380$. Bảng~\ref{tab:exp6_k380} tổng hợp...` | Lỗi Over-lowercasing: Danh từ chung đứng đầu câu mới bắt buộc viết hoa. |
| 4 | Ô tiêu đề cột trong bảng | `\textbf{Công bố Hình 8A (\%)}` | `\textbf{Công bố hình 8A (\%)}` | Danh từ chung `hình` nằm giữa cụm từ trong ô tiêu đề bảng bắt buộc viết thường. |
| 5 | Soạn thảo đoạn văn mới Mục 3.1 | `...như phân họ \texttt{A01.009}...` | `...như phân họ A01.009...` | Vi phạm quy chuẩn Mục 9: Cấm `\texttt` cho mã định danh phân loại sinh học; dùng Times New Roman chữ đứng. |
| 6 | Giữa câu văn thân bài | `...như thể hiện trong Bảng~\ref{tab:exp1}...` | `...như thể hiện trong bảng~\ref{tab:exp1}...` | Danh từ chung `bảng` đi kèm số thứ tự khi đứng giữa câu bắt buộc viết thường. |
| 7 | Giữa câu văn thân bài | `...được tính theo Công thức~\eqref{eq:facility}...` | `...được tính theo công thức~\eqref{eq:facility}...` | Danh từ chung `công thức` đi kèm số thứ tự khi đứng giữa câu bắt buộc viết thường. |
| 8 | Giữa câu văn thân bài | `...tuân theo quy trình tại Thuật toán 2.1...` | `...tuân theo quy trình tại thuật toán 2.1...` | Danh từ chung `thuật toán` đi kèm số thứ tự khi đứng giữa câu bắt buộc viết thường. |

---

## 17. CẬP NHẬT THÔNG SỐ CẤU HÌNH PHẦN CỨNG MÁY TRẠM THỰC NGHIỆM (HARDWARE SPECIFICATIONS)

1. **Bộ vi xử lý trung tâm (CPU)**:
   - Vi xử lý: **AMD Ryzen 9 8940HX** với $16$ nhân và $32$ luồng xử lý, hỗ trợ tập lệnh AVX-512.
   - Tuyệt đối không dùng thông tin cũ sai lệch (*Intel Core i7*).

2. **Bộ xử lý đồ họa (GPU)**:
   - Card đồ họa: **NVIDIA GeForce RTX 5060 Laptop GPU** kiến trúc Blackwell sm\_120, bộ nhớ $8\text{ GB}$ GDDR6, NVIDIA Driver $595.97$, hỗ trợ CUDA $13.2$.

---

## 18. CHUẨN HÓA THUẬT NGỮ CHUỖI THỰC NGHIỆM TUẦN TỰ (SEQUENTIAL EXPERIMENT NOMENCLATURE)

1. **Thay thế thuật ngữ quản lý dự án nội bộ `Nhánh 1..6`**:
   - Trong toàn bộ báo cáo đồ án LaTeX, thay thế toàn bộ từ quản lý dự án nội bộ `Nhánh 1..6` bằng thuật ngữ khoa học chuẩn mực: **`thử nghiệm 1..6`** (hoặc `Thử nghiệm 1..6` khi đứng đầu câu/đầu mục/đầu ô bảng).
   - Tuyệt đối không để sót từ `Nhánh 1..6` trong thân bài, tiêu đề, chú thích hoặc bảng biểu của báo cáo.

2. **Nguyên tắc cô lập biến số \textit{ceteris paribus} xuyên suốt 6 thử nghiệm tuần tự**:
   - Bắt buộc trình bày danh sách 6 gạch đầu dòng giới thiệu tường minh 6 thử nghiệm tuần tự tại cuối Mục 3.1 (trước Mục 3.2), nêu rõ biến số độc lập duy nhất thay đổi ở từng thử nghiệm theo nguyên tắc \textit{ceteris paribus}:
     - Thử nghiệm 1: Tái hiện mô hình cơ sở và kiểm chứng giới hạn đánh giá toàn cục.
     - Thử nghiệm 2: Đánh giá hàm mục tiêu có trọng số trên không gian BLASTp (biến số độc lập: hàm mục tiêu có trọng số $\alpha$).
     - Thử nghiệm 3: Khảo sát hàm mục tiêu có trọng số trên không gian ngữ nghĩa ESM-2 (biến số độc lập: ma trận biểu diễn ngữ nghĩa ESM-2).
     - Thử nghiệm 4: Kiểm chứng chéo hai chiều giữa hai không gian biểu diễn (biến số độc lập: kiểm chứng chéo $2 \times 2$ giữa không gian tối ưu hóa và không gian đánh giá).
     - Thử nghiệm 5: Phân tích cơ cấu phân bổ đại diện và độ dư thừa nội phân họ (biến số độc lập: cấu trúc phân bổ vi mô trên từng phân họ cụ thể).
     - Thử nghiệm 6: Khảo sát quá trình hội tụ độ bao phủ khi mở rộng ngân sách (biến số độc lập: quy mô ngân sách đại diện $k$).
   - Bắt buộc cập nhật đầy đủ cả 6 thử nghiệm vào Bảng 3.6 (`tab:rq_resolution`) để tổng kết toàn diện câu trả lời cho các câu hỏi nghiên cứu.

3. **Quy trình kiểm tra tự động trước khi xuất bản (Pre-Compile Hygiene Gate)**:
   - Trước khi biên dịch xuất bản báo cáo LaTeX, bắt buộc thực thi kịch bản kiểm tra tự động trên terminal để rà soát:
     1. Không có từ viết thường đứng ngay sau dấu chấm `. ` hoặc đứng đầu đoạn văn sau các khối môi trường đóng.
     2. Không có danh từ chung (`bảng`, `hình`, `công thức`, `thuật toán`, `thử nghiệm`) kèm `\ref`, `\eqref` viết hoa giữa câu.
     3. Không có lệnh `\texttt` bọc nhãn phân họ sinh học (`A01.009`, `[A01.UPA]`) hoặc tên tệp dữ liệu (`MEROPS\_A1A.fasta`).
     4. Không có từ cấm quản lý dự án `Nhánh 1..6` hoặc tên phần cứng cũ `Intel Core i7`.
     5. Cân bằng chẵn lẻ $100\%$ của ký tự toán học `$`.
