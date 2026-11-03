# CATALOG QUY TẮC R-DATA: LIÊM CHÍNH DỮ LIỆU & ĐỐI SOÁT CSV (SSOT)

Mọi khẳng định số liệu, bảng biểu và diễn giải định lượng trong báo cáo LaTeX bắt buộc phải tuân thủ nghiêm ngặt các quy tắc sau:

## 1. R-DATA-01: Nguyên tắc đối soát 100% nguyên văn (100% Verbatim Match)
- Mọi con số trích dẫn trong văn bản (độ nhạy, độ bao phủ, số phân họ hiếm, số chuỗi Hit, tỷ lệ phần trăm) bắt buộc phải đối soát chính xác 100% nguyên văn với 6 tệp CSV gốc trong `RareProtSelect/outputs/tables/`:
  * Thử nghiệm 1: `exp1_baseline_a1a_calibration.csv`
  * Thử nghiệm 2: `exp2_rare_weighted_a1a.csv`
  * Thử nghiệm 3: `exp3_esm_coverage_a1a.csv`
  * Thử nghiệm 4: `exp4_cross_eval_a1a.csv`
  * Thử nghiệm 5: `exp5_subfamily_allocation_a1a.csv`
  * Thử nghiệm 6: `exp6_budget_scaling_a1a.csv`
- Tuyệt đối CẤM làm tròn tùy tiện (ví dụ: $94{,}13\%$ không được làm tròn thành $94\%$ hoặc $94{,}1\%$).
- Tuyệt đối CẤM tự ý nội suy hoặc bịa đặt các con số chưa đo đạc thực tế.

## 2. R-DATA-02: Dữ liệu kiểm chuẩn tái hiện bài báo nền (Thử nghiệm 1 - exp1)
- Tập dữ liệu tái hiện bài báo nền của Nguyen et al. (2025) thực hiện trên toàn bộ $13.307$ chuỗi thô của siêu họ Peptidase A1 (`MEROPS_A1A.fasta`), sử dụng hàm mục tiêu Facility Location không trọng số ($\alpha = 0{,}0$) và giải thuật Pruned Greedy 90%.
- Bảng đối chuẩn 11 mốc ngân sách $k \in \{11, 22, 33, 44, 55, 66, 77, 88, 99, 110, 115\}$:
  * $k = 11$: Đề tài đạt $94{,}13\%$ ($12.526/13.307$ chuỗi Hit); Công bố hình 8A đạt $94{,}20\%$; Độ lệch tuyệt đối là $0{,}07\%$.
  * $k = 22$: Đề tài đạt $97{,}64\%$ ($12.993/13.307$ chuỗi Hit); Công bố hình 8A đạt $97{,}50\%$; Độ lệch tuyệt đối là $0{,}14\%$.
  * $k = 33$: Đề tài đạt $98{,}54\%$ ($13.113/13.307$ chuỗi Hit); Công bố hình 8A đạt $98{,}40\%$; Độ lệch tuyệt đối là $0{,}14\%$.
  * $k = 44$: Đề tài đạt $98{,}96\%$ ($13.169/13.307$ chuỗi Hit); Công bố hình 8A đạt $98{,}90\%$; Độ lệch tuyệt đối là $0{,}06\%$.
  * $k = 55$: Đề tài đạt $99{,}21\%$ ($13.202/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}20\%$; Độ lệch tuyệt đối là $0{,}01\%$.
  * $k = 66$: Đề tài đạt $99{,}41\%$ ($13.228/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}40\%$; Độ lệch tuyệt đối là $0{,}01\%$.
  * $k = 77$: Đề tài đạt $99{,}56\%$ ($13.248/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}50\%$; Độ lệch tuyệt đối là $0{,}06\%$.
  * $k = 88$: Đề tài đạt $99{,}66\%$ ($13.262/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}60\%$; Độ lệch tuyệt đối là $0{,}06\%$.
  * $k = 99$: Đề tài đạt $99{,}74\%$ ($13.272/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}70\%$; Độ lệch tuyệt đối là $0{,}04\%$.
  * $k = 110$: Đề tài đạt $99{,}80\%$ ($13.280/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}80\%$; Độ lệch tuyệt đối là $0{,}00\%$.
  * $k = 115$: Đề tài đạt $99{,}82\%$ ($13.283/13.307$ chuỗi Hit); Công bố hình 8A đạt $99{,}80\%$; Độ lệch tuyệt đối là $0{,}02\%$.
- Độ lệch tuyệt đối trung bình trên toàn bộ 11 mốc là $0{,}055\%$ ($\le 0{,}14\%$), khẳng định pipeline tính toán tái hiện thành công bài báo nền với độ chuẩn xác cao.

## 3. R-DATA-03: Kỷ luật số liệu mẫu $V_{\text{curated}}$ vs. Tập thô $13.307$
- Thử nghiệm 1 chạy trên toàn bộ $13.307$ chuỗi thô của Peptidase A1 (để đối chuẩn với hình 8A của bài báo nền).
- Các thử nghiệm từ 2 đến 6 chạy trên tập nền phân họ chính thức $V_{\text{curated}}$ gồm $4.120$ chuỗi thuộc $115$ Subfamily chính thức.
- Tuyệt đối CẤM nhầm lẫn mẫu số giữa $13.307$ chuỗi (thử nghiệm 1) và $4.120$ chuỗi (thử nghiệm 2..6).
