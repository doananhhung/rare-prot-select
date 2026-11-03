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

def clean_latex(text):
    # remove comments
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)
    return text

for tf in tex_files:
    fname = os.path.basename(tf)
    with open(tf, encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n==================================================")
    print(f"FILE: {fname}")
    print(f"==================================================")
    
    for l_idx, line in enumerate(lines, 1):
        l_clean = re.sub(r'(?<!\\)%.*$', '', line).strip()
        if not l_clean:
            continue
        
        # Split line into words
        # A word is a sequence of unicode letters
        # We want to identify any Vietnamese capitalized word that is NOT at sentence start
        # Let's tokenize by punctuation and spaces
        tokens = re.finditer(r'([A-ZÀ-Ỹa-zà-ỹ0-9_]+)', l_clean)
        prev_token = None
        for m in tokens:
            w = m.group(1)
            # check if w has uppercase
            if w and w[0].isupper():
                # check context
                pos = m.start()
                prefix = l_clean[:pos].rstrip()
                # If prefix is empty, it's line start
                is_start = False
                if not prefix or prefix.endswith(('.', '!', '?', '{', '[', '\\item', '\\section{', '\\subsection{', '\\chapter{', '\\textbf{', '\\textit{')):
                    is_start = True
                
                # We want to flag words that look Vietnamese (have diacritics or common vn syllables)
                # Syllables in Vietnamese:
                vn_syllables = {
                    'Tối', 'Ưu', 'Hóa', 'Trí', 'Tuệ', 'Nhân', 'Tạo', 'Học', 'Máy', 'Sâu', 
                    'Mô', 'Hình', 'Ngôn', 'Ngữ', 'Lớn', 'Hệ', 'Thống', 'Đa', 'Tác', 'Tử',
                    'Thực', 'Tập', 'Công', 'Nghiệp', 'Ban', 'Giám', 'Hiệu', 'Khoa',
                    'Toán', 'Tin', 'Dữ', 'Liệu', 'Sinh', 'Học', 'Định', 'Tuyến', 'Lập', 'Lịch',
                    'Tổ', 'Hợp', 'Thuật', 'Toán', 'Đại', 'Học', 'Trường', 'Phòng', 'Thí', 'Nghiệm',
                    'Cán', 'Bộ', 'Hướng', 'Dẫn', 'Nghiên', 'Cứu', 'Sinh', 'Viên', 'Giảng', 'Viên',
                    'Các', 'Những', 'Bộ', 'Đóng', 'Gói', 'Khắc', 'Phục', 'Đánh', 'Giá', 'Tích', 'Hợp',
                    'Thành', 'Viên', 'Nhóm', 'Lãnh', 'Đạo', 'Trưởng', 'Phát', 'Triển', 'Tiến', 'Trình'
                }
                
                if w in vn_syllables:
                    # check if it's legit proper noun context:
                    # e.g., "Trường Đại học Phenikaa" -> "Trường Đại học" before Phenikaa
                    # e.g., "Phạm Văn Cảnh", "Trần Đình Tân"
                    # e.g., "\textbf{Hướng nghiên cứu 01: Tối ưu hóa}" -> title of item
                    print(f"  Line {l_idx:3d} (is_start={is_start}): [{w}] -> context: ...{l_clean[max(0, pos-20):min(len(l_clean), pos+len(w)+25)]}...")
