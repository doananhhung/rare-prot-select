import os, sys

sys.stdout.reconfigure(encoding='utf-8')

large_files = []
ignored_dirs = {'.git', '.venv', '.gemini'}

for root, dirs, files in os.walk('.'):
    # prune ignored dirs
    dirs[:] = [d for d in dirs if d not in ignored_dirs]
    for f in files:
        fpath = os.path.join(root, f)
        try:
            sz = os.path.getsize(fpath)
            if sz > 5 * 1024 * 1024:  # > 5 MB
                large_files.append((sz, fpath))
        except Exception:
            pass

large_files.sort(reverse=True)
print(f"=== Files > 5 MB (Total: {len(large_files)}) ===")
for sz, p in large_files:
    print(f"{sz / (1024*1024):8.2f} MB  {p}")
