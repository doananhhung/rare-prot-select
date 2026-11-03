# CATALOG QUY TẮC R-FMT: ĐỊNH DẠNG BẢNG, TOÁN HỌC & TRÍCH DẪN (SSOT)

Mọi định dạng mã nguồn LaTeX bắt buộc phải tuân thủ nghiêm ngặt các quy tắc sau:

## 1. R-FMT-01: Tiêu chuẩn Booktabs 3 đường kẻ ngang
- Tuyệt đối CẤM kẻ các đường dọc (`|`) trong mọi bảng (`tabular`).
- Bắt buộc dùng 3 đường kẻ chuẩn từ gói `booktabs`:
  * `\toprule`: Đường kẻ đầu bảng.
  * `\midrule`: Đường kẻ phân cách giữa dòng tiêu đề cột và dòng dữ liệu đầu tiên.
  * `\bottomrule`: Đường kẻ chân bảng.
- Căn lề: Cột mô tả văn bản căn trái (`l`), cột nhãn/hệ số căn giữa (`c`), cột số liệu đo đạc định lượng căn phải (`r`).

## 2. R-FMT-02: Số thập phân tiếng Việt `{,}`
- Trong math mode, dấu phẩy ngăn cách phần thập phân bắt buộc phải bọc trong ngoặc nhọn `{,}`:
  * Đúng: `$94{,}13\%$`, `$0{,}07\%$`, `$1{,}0\text{ cm}$`, `$\alpha = 0{,}0$`.
  * Sai: `$94,13\%$` (LaTeX hiểu nhầm là dấu phẩy phân cách danh sách và tự ý chèn khoảng trắng).

## 3. R-FMT-03: Biểu diễn bội số trong văn xuôi (`gấp X lần`)
- Trong văn xuôi tiếng Việt học thuật, tuyệt đối CẤM viết bội số dưới dạng ký hiệu tắt `$X\times$` (ví dụ: `$1{,}6\times$`, `$4{,}0\times$`).
- Bắt buộc viết bằng tiếng Việt tự nhiên: **`gấp $X$ lần`** (ví dụ: `gấp $1{,}6$ đến $4{,}0$ lần`, `gấp $329{,}0$ lần`).
- Ngoại lệ: Ký hiệu thiết kế tích Descartes (như "Ma trận chọn $\times$ Thước đo đánh giá") được phép dùng `\times`, nhưng phải thêm chú thích `% lint-allow: R-FMT-03`.

## 4. R-FMT-04: Kỷ luật tham chiếu chéo (`\ref`, `\cite`)
- Tuyệt đối CẤM hard-code số thứ tự tĩnh trong văn bản (như *"theo Bảng 1"*, *"ở Hình 2"*, *"trong Công thức 3"*).
- Bắt buộc dùng `\ref{...}` hoặc `\eqref{...}` kèm dấu ngã `~` chống ngắt dòng: `bảng~\ref{tab:...}`, `hình~\ref{fig:...}`, `công thức~\eqref{eq:...}`.
- Ngoại lệ: Khi tham chiếu đến hình ảnh hoặc bảng biểu của bài báo ngoài (ví dụ: "công bố hình 8A của bài báo nền"), được phép ghi rõ tên nguồn ngoài kèm trích dẫn `\cite{...}` (như `hình 8A của Nguyen và cộng sự~\cite{nguyen2025}`).

## 5. R-FMT-05: Kỷ luật phân định phông chữ monospace (`\texttt`)
- Tuyệt đối CẤM dùng `\texttt` hoặc `\verb` cho:
  * Tên tệp dữ liệu sinh học: `MEROPS\_A1A.fasta`, `Thioesterases\_Sequences.fasta`.
  * Nhãn phân loại và mã Subfamily: `[A01.UPA]`, `A01.001`, `A01.009`.
  * Tên mô hình học máy: `ESM-2-35M`.
  * Tên chỉ số kỹ thuật: sử dụng math mode (`$k$`, `$\text{Overall Sensitivity}$`).
- Phạm vi DUY NHẤT được phép dùng `\texttt`: Lệnh CLI terminal (`\texttt{uv run python ...}`), đường dẫn mã nguồn lập trình (`\texttt{src/...}`), tên hàm/biến code (`\texttt{compute_submodular_gain()}`).

## 6. R-FMT-06: Môi trường hình ảnh và bảng biểu
- Đặt trong môi trường `figure[htbp!]` hoặc `table[htbp!]`, kết hợp `\centering`, `\caption{...}` và `\label{...}` đặt ngay sau caption.
- Đầu mỗi section có lệnh `\FloatBarrier` (từ gói `placeins`) để giữ các float nằm gọn trong section tương ứng.

## 7. R-FMT-07: Quy chuẩn cấu trúc & Định dạng Báo cáo Thực tập Công nghiệp (Mẫu sample.pdf)
- **Header & Footer**: Tuyệt đối CẤM Running Header và đường kẻ phân cách trên 100% các trang tài liệu. Phần thân bài chỉ hiển thị số trang Ả Rập tại chính giữa đáy trang (`\pagestyle{plain}`).
- **Số trang Frontmatter**: Tuyệt đối KHÔNG in số trang trên bất kỳ trang mở đầu nào (Bìa, Phiếu nhận xét, Lời cảm ơn, Mục lục, Danh mục bảng/hình). Sử dụng `\pagenumbering{gobble}` cho đến trước Chương I.
- **Phân cấp tiêu đề (Headings Hierarchy)**:
  * Chương: Bắt buộc định dạng số La Mã có tiền tố và dấu hai chấm: `CHƯƠNG \Roman{chapter}: <TÊN CHƯƠNG IN HOA>`.
  * Section: Bắt buộc có dấu chấm đuôi sau số thứ tự: `\thesection.\quad <Tên mục>`.
  * Subsection: Bắt buộc có dấu chấm đuôi và in nghiêng: `\textit{\thesubsection.\quad <Tên tiểu mục>}`.
- **Bộ đếm toàn cục cho Bảng & Hình (Global Numbering)**:
  * Bắt buộc dùng `\counterwithout{table}{chapter}` và `\counterwithout{figure}{chapter}` để đánh số liên tục toàn tài liệu: `Bảng 1:`, `Bảng 2:`, `Hình 1:`, `Hình 2:`.
  * Bảng: Chú thích đặt PHÍA TRÊN bảng.
  * Hình: Chú thích đặt PHÍA DƯỚI hình.
- **Ký hiệu danh sách liệt kê (Itemize Bullets)**: Bắt buộc cấu hình `\setlist[itemize]{label={--}}` để sử dụng dấu gạch ngang đầu dòng theo chuẩn văn bản hành chính Việt Nam.
- **Cấu trúc Mục lục (TOC)**:
  * Tiêu đề căn giữa: `\renewcommand{\contentsname}{\centering MỤC LỤC}`.
  * Tuyệt đối KHÔNG đưa Phiếu nhận xét và Lời cảm ơn vào Mục lục.
- **Gộp Danh mục Bảng & Hình**: Đặt Danh mục Bảng biểu và Danh mục Hình ảnh nằm gọn trên cùng 1 trang duy nhất (nối tiếp nhau), triệt tiêu hoàn toàn trang trắng thừa thãi.
