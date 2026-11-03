import subprocess, os, sys

sys.stdout.reconfigure(encoding='utf-8')

# Get list of files that would be tracked
res = subprocess.run(['git', 'status', '--porcelain', '-uall'], capture_output=True, text=True, encoding='utf-8')

large_files = []
for line in res.stdout.splitlines():
    if not line.strip():
        continue
    status = line[:2]
    filepath = line[3:].strip()
    if filepath.startswith('"') and filepath.endswith('"'):
        # handle unquoting escaped octal if git uses it
        import ast
        try:
            filepath = ast.literal_eval(filepath)
        except Exception:
            filepath = filepath.strip('"')
    
    if os.path.isfile(filepath):
        sz = os.path.getsize(filepath)
        if sz > 5 * 1024 * 1024:  # > 5 MB
            large_files.append((sz, filepath))

print(f"=== Files > 5 MB in prospective Git staging (Total: {len(large_files)}) ===")
for sz, p in sorted(large_files, reverse=True):
    print(f"{sz / (1024*1024):8.2f} MB  {p}")

if not large_files:
    print("ALL tracked files are < 5 MB!")
elif max(s[0] for s in large_files) < 50 * 1024 * 1024:
    print("\nSAFE: All files are well below GitHub's 100 MB hard limit (all < 50 MB)!")
