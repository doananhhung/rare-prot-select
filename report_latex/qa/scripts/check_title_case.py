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

for tf in tex_files:
    fname = os.path.basename(tf)
    with open(tf, encoding='utf-8') as f:
        text = f.read()
    
    # remove comments
    lines = [re.sub(r'(?<!\\)%.*$', '', l) for l in text.splitlines()]
    
    print(f"\n==================== {fname} ====================")
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        # Find all words with initial capital
        # We look for patterns where a capitalized word appears after:
        # 1. A colon ":" -> check if it's common noun
        # 2. Inside bullet headings or text
        
        # Check after colon
        colons = re.finditer(r':\s*([A-ZÀ-Ỹa-zà-ỹ0-9_]+)', line)
        for c in colons:
            w = c.group(1)
            if w and w[0].isupper() and w not in ['TS', 'PGS', 'GS', 'AMD', 'NVIDIA', 'CUDA', 'Python', 'ORLab', 'https', 'RareProtSelect']:
                print(f"  [After Colon] L{idx:3d}: {line.strip()[:100]}")
        
        # Check Title Case in Vietnamese phrases: Two capitalized words in a row that are common nouns
        # e.g., "Học Sâu", "Đa Tác Tử", "Trí Tuệ Nhân Tạo", "Tối Ưu Hóa", "Thực Tập Công Nghiệp"
        title_case_patterns = [
            r'Học\s+Sâu',
            r'Hệ\s+[Tt]hống\s+[Đđ]a\s+[Tt]ác\s+[Tt]ử',
            r'Trí\s+Tuệ\s+Nhân\s+Tạo',
            r'Tối\s+Ưu\s+Hóa',
            r'Thực\s+Tập\s+Công\s+Nghiệp',
            r'Ban\s+Giám\s+Hiệu',
            r'Khoa\s+Khoa\s+học',
            r'Tối\s+ưu\s+hóa\s+và\s+Trí',
            r'Học\s+máy\s+và\s+Học',
            r'Mô\s+hình\s+ngôn\s+ngữ\s+lớn\s+và\s+Hệ',
            r'học\s+phần\s+Thực\s+tập',
            r'Phòng\s+thí\s+nghiệm\s+Tối\s+ưu',
        ]
        for p in title_case_patterns:
            if re.search(p, line):
                print(f"  [Pattern Match: {p}] L{idx:3d}: {line.strip()[:100]}")
