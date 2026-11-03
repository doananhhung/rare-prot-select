import glob, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

tex_files = glob.glob('report_latex/thuc_tap_cong_nghiep/contents/**/*.tex', recursive=True)
tex_files.append('report_latex/thuc_tap_cong_nghiep/main.tex')

vn_upper = r'[A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]'
vn_lower = r'[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]'

proper_nouns = {
    'Hà', 'Nội', 'Việt', 'Nam', 'Phenikaa', 'Cảnh', 'Tân', 'Hùng', 'Trác', 'Dương', 
    'Phạm', 'Trần', 'Nguyễn', 'Nemhauser', 'Minoux', 'Ethayarajh', 'Lin', 'Altschul', 
    'Camacho', 'Rawlings', 'Wei', 'Cui', 'Li', 'Godzik', 'Steinegger', 'Söding',
    'Thứ', 'Hai', 'Ba', 'Tư', 'Năm', 'Sáu', 'Bảy', 'Chủ', 'Nhật', 'ORLab', 'Lab',
    'Đoàn', 'Thị', 'Kim', 'Huyền', 'Dung', 'Tạ', 'Thúy', 'Anh', 'Bảng', 'Hình',
    'Chương', 'Mục', 'Công', 'thức', 'STT', 'TOC', 'LOT', 'LOF', 'ISI', 'Scopus'
}

for tf in sorted(tex_files):
    fname = os.path.basename(tf)
    print(f'=== {fname} ===')
    with open(tf, encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str or line_str.startswith('%'):
                continue
            if '%' in line_str:
                line_str = line_str.split('%')[0].strip()
            
            # Find any capitalized word that is preceded by a lowercase letter or space after lowercase letter
            matches = list(re.finditer(rf'([a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ,;:\s])({vn_upper}[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+)', line_str))
            for m in matches:
                word = m.group(2)
                if word in proper_nouns:
                    continue
                # check if word is at start of sentence or after label/ref
                pos = m.start(2)
                prefix = line_str[:pos].strip()
                if not prefix or prefix.endswith(('.', ':', '!', '?', '{', '[', '\\item', '\\textbf{', '\\textit{')):
                    continue
                # Print suspicious capitalization
                print(f'  L{idx}: [{word}] in: ...{line_str[max(0, pos-25):min(len(line_str), pos+35)]}...')
