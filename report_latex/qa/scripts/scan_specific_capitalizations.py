import glob, os, sys, unicodedata, re

sys.stdout.reconfigure(encoding='utf-8')

tex_files = [
    'report_latex/thuc_tap_cong_nghiep/contents/frontmatter/acknowledgement.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/frontmatter/review_form.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/frontmatter/cover.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/chapters/01_gioi_thieu_orlab.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/chapters/02_muc_tieu_ke_hoach_lich_trinh.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/chapters/03_tinh_hinh_thuc_tap_du_an.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/chapters/04_tu_danh_gia.tex',
    'report_latex/thuc_tap_cong_nghiep/contents/chapters/05_ket_luan_kien_nghi.tex',
]

# Common Vietnamese words that should NOT be capitalized mid-sentence or in common nouns
# Unless at the very beginning of a sentence.
common_vn_words_often_wrongly_capitalized = [
    'Tối', 'Ưu', 'Hóa', 'Trí', 'Tuệ', 'Nhân', 'Tạo', 'Học', 'Máy', 'Sâu', 
    'Mô', 'Hình', 'Ngôn', 'Ngữ', 'Lớn', 'Hệ', 'Thống', 'Đa', 'Tác', 'Tử',
    'Thực', 'Tập', 'Công', 'Nghiệp', 'Ban', 'Giám', 'Hiệu', 'Khoa',
    'Toán', 'Tin', 'Dữ', 'Liệu', 'Sinh', 'Học', 'Định', 'Tuyến', 'Lập', 'Lịch',
    'Tổ', 'Hợp', 'Thuật', 'Toán', 'Đại', 'Học', 'Trường', 'Phòng', 'Thí', 'Nghiệm',
    'Cán', 'Bộ', 'Hướng', 'Dẫn', 'Nghiên', 'Cứu', 'Sinh', 'Viên', 'Giảng', 'Viên'
]

for tf in tex_files:
    fname = os.path.basename(tf)
    with open(tf, encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n==================== {fname} ====================")
    for idx, line in enumerate(lines, 1):
        clean = re.sub(r'(?<!\\)%.*$', '', line).strip()
        if not clean:
            continue
        # Find any of these capitalized words
        for target in common_vn_words_often_wrongly_capitalized:
            # Match word boundary
            matches = list(re.finditer(rf'(?<![a-zA-ZÀ-ỹ0-9_]){target}(?![a-zA-ZÀ-ỹ0-9_])', clean))
            for m in matches:
                pos = m.start()
                # Check character before pos
                before = clean[:pos].strip()
                # If before is empty, it's start of line
                if not before:
                    continue
                # If before ends with '.', '!', '?', then it is start of sentence
                if before.endswith(('.', '!', '?')):
                    continue
                # If before is a section or chapter command: \chapter{, \section{, \subsection{
                # Or \item \textbf{...
                # Let's print out context
                start = max(0, pos - 25)
                end = min(len(clean), pos + len(target) + 25)
                snippet = clean[start:end]
                print(f"  L{idx:3d} [{target}]: ...{snippet}...")
