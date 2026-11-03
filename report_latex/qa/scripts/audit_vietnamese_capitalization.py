import glob, os, sys, unicodedata, re

sys.stdout.reconfigure(encoding='utf-8')

tex_files = sorted(glob.glob('report_latex/thuc_tap_cong_nghiep/**/*.tex', recursive=True))

def is_vn_alpha(ch):
    cat = unicodedata.category(ch)
    return cat.startswith('L')

def is_upper(ch):
    return unicodedata.category(ch) == 'Lu'

# Whitelist of legitimate proper nouns, English terms, acronyms, or math/LaTeX
legit = {
    'Việt', 'Nam', 'Hà', 'Nội', 'Phenikaa', 'Cảnh', 'Tiến', 'Hùng', 'Trúc', 'Dũng',
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
    'DeepMind', 'OpenAI', 'Google', 'Meta', 'Microsoft'
}

for tf in tex_files:
    fname = os.path.relpath(tf, 'report_latex/thuc_tap_cong_nghiep')
    with open(tf, encoding='utf-8') as f:
        lines = f.readlines()
    
    suspicious = []
    for line_idx, line in enumerate(lines, 1):
        # strip comments
        clean_line = re.sub(r'(?<!\\)%.*$', '', line).strip()
        if not clean_line:
            continue
        
        # tokenize into words and latex commands
        # find all words
        words = re.findall(r'[a-zA-ZÀ-ỹ0-9_]+', clean_line)
        for w_idx, w in enumerate(words):
            if not w or w.isdigit() or len(w) == 1:
                continue
            if is_upper(w[0]):
                # If first char is uppercase
                # Check if it's in legit
                if w in legit:
                    continue
                # Check if all upper (acronym)
                if w.isupper():
                    continue
                # If it's the very first word in the line, could be start of sentence
                if w_idx == 0:
                    continue
                # Let's inspect context in the line
                # Find position
                pos = clean_line.find(w)
                before = clean_line[:pos].rstrip()
                # Check if preceding char ends a sentence: . ! ?
                if before.endswith(('.', '!', '?', ':', '---', '--', '``', '"', '(', '[')):
                    # Even after :, Vietnamese does NOT capitalize common nouns!
                    # After ., !, ? it is start of sentence
                    if not before.endswith((':', '---', '--', '``', '"', '(', '[')):
                        continue
                
                suspicious.append((line_idx, w, clean_line))
    
    if suspicious:
        print(f"=== {fname} ({len(suspicious)} items) ===")
        for lnum, w, ltext in suspicious:
            # show snippet
            pos = ltext.find(w)
            start = max(0, pos - 30)
            end = min(len(ltext), pos + len(w) + 30)
            snippet = ltext[start:end]
            print(f"  L{lnum:3d} [{w}]: ...{snippet}...")
