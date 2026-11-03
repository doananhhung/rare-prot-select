import os, shutil

temp_patterns = [
    'preview_', 'visual_check_', 'updated_page_'
]

# 1. Clean files in report_latex/Images
images_dir = 'report_latex/Images'
if os.path.exists(images_dir):
    for f in os.listdir(images_dir):
        if any(f.startswith(p) for p in temp_patterns) and f.endswith('.png'):
            fpath = os.path.join(images_dir, f)
            os.remove(fpath)
            print(f"Removed: {fpath}")

# 2. Clean files in report_latex/thuc_tap_cong_nghiep
ttcn_dir = 'report_latex/thuc_tap_cong_nghiep'
if os.path.exists(ttcn_dir):
    for f in os.listdir(ttcn_dir):
        if any(f.startswith(p) for p in temp_patterns) and f.endswith('.png'):
            fpath = os.path.join(ttcn_dir, f)
            os.remove(fpath)
            print(f"Removed: {fpath}")

# 3. Clean rendered_pages folder
rp_dir = os.path.join(ttcn_dir, 'rendered_pages')
if os.path.exists(rp_dir):
    shutil.rmtree(rp_dir)
    print(f"Removed directory: {rp_dir}")

# 4. Clean sample.pdf
sample_pdf = 'report_latex/sample.pdf'
if os.path.exists(sample_pdf):
    os.remove(sample_pdf)
    print(f"Removed: {sample_pdf}")

print("Cleanup completed.")
