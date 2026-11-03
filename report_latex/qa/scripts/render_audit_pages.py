import fitz, os

doc = fitz.open('report_latex/thuc_tap_cong_nghiep/main.pdf')
out_dir = r'C:\Users\doana\.gemini\antigravity\brain\bd72b510-ed36-43f3-ad24-508b34f34938'

pages_to_render = [2, 6, 8, 12, 16, 19]

for p_num in pages_to_render:
    page = doc.load_page(p_num - 1)
    pix = page.get_pixmap(dpi=150)
    out_path = os.path.join(out_dir, f'audit_cap_p{p_num:02d}.png')
    pix.save(out_path)
    print(f'Rendered Page {p_num} -> {out_path}')
