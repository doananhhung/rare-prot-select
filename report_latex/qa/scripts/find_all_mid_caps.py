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

proper_nouns = {
    'Hà', 'Nội', 'Việt', 'Nam', 'Phenikaa', 'Cảnh', 'Tiến', 'Hùng', 'Trúc', 'Dũng',
    'Phạm', 'Trần', 'Nguyễn', 'Nemhauser', 'Minoux', 'Ethayarajh', 'Lin', 'Altschul',
    'Camacho', 'Rawlings', 'Wei', 'Cui', 'Li', 'Godzik', 'Steinegger', 'Söding',
    'Thứ', 'Hai', 'Ba', 'Tư', 'Năm', 'Sáu', 'Bảy', 'Chủ', 'Nhật', 'ORLab', 'Lab',
    'Đoàn', 'Thị', 'Kim', 'Huyền', 'Dung', 'Tô', 'Thúy', 'Anh', 'Bằng', 'Hình',
    'Bảng', 'Chương', 'Mục', 'Công', 'thức', 'STT', 'TOC', 'LOT', 'LOF', 'ISI', 'Scopus',
    'Python', 'PyTorch', 'CUDA', 'BLAST', 'BLAST+', 'MMseqs2', 'CD-HIT', 'FASTA', 'ESM', 'ESM-2',
    'MEROPS', 'ThYme', 'ESTHER', 'Greedy', 'Pruned', 'Lazy', 'Standard', 'Random', 'Facility',
    'Location', 'Sensitivity', 'Overall', 'Macro', 'Macro-Average', 'Rare', 'Within-Subfamily',
    'Coverage', 'Cosine', 'Shannon', 'Entropy', 'FL', 'Subfamily', 'Subfamilies', 'GPU', 'CPU',
    'RAM', 'VRAM', 'GB', 'MB', 'MD', 'PhD', 'TS', 'PGS', 'GS', 'NXB', 'ĐHQG', 'UBND', 'QĐ',
    'IEEE', 'ACM', 'Nature', 'Bioinformatics', 'Springer', 'BioMed', 'Central', 'BMC', 'PeerJ',
    'Kaggle', 'GitHub', 'Markdown', 'LaTeX', 'XeLaTeX', 'BibTeX', 'Overleaf', 'VS', 'Code',
    'Windows', 'Linux', 'Ubuntu', 'Intel', 'AMD', 'Ryzen', 'NVIDIA', 'GeForce', 'RTX', 'Blackwell',
    'DeepMind', 'OpenAI', 'Google', 'Meta', 'Microsoft', 'RareProtSelect'
}

for tf in tex_files:
    fname = os.path.basename(tf)
    with open(tf, encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n==================== {fname} ====================")
    for idx, line in enumerate(lines, 1):
        clean = re.sub(r'(?<!\\)%.*$', '', line).strip()
        if not clean:
            continue
        
        # 1. Check capitalized word right after a colon ": [A-ZÀ-Ỹ]"
        colon_matches = re.finditer(r':\s+([A-ZÀ-Ỹ][a-zA-ZÀ-ỹ0-9_]+)', clean)
        for m in colon_matches:
            w = m.group(1)
            if w not in proper_nouns:
                print(f"  [After Colon] L{idx:3d}: ': {w}' in: {clean[:100]}")
        
        # 2. Check capitalized word after a lowercase Vietnamese word without punctuation in between
        # e.g., "Học sâu" -> "Học Sâu"
        mid_matches = re.finditer(r'([a-zà-ỹ]+)\s+([A-ZÀ-Ỹ][a-zà-ỹ0-9_]+)', clean)
        for m in mid_matches:
            w1 = m.group(1)
            w2 = m.group(2)
            if w2 in proper_nouns:
                continue
            # Ignore if w1 is something like e.g. or etc
            print(f"  [Mid-sentence] L{idx:3d}: '{w1} {w2}' in: {clean[:100]}")
