import subprocess, sys, os
os.chdir(r"c:\Users\monoc\Documents\Projects\Quilombo\quilombo_site")
result = subprocess.run(
    [r"c:\Users\monoc\Documents\Projects\Quilombo\.venv\Scripts\python.exe", "manage.py", "test", "--verbosity", "2"],
    capture_output=True, text=True
)
with open(r"c:\Users\monoc\Documents\Projects\Quilombo\test_output.txt", "w", encoding="utf-8") as f:
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n=== STDERR ===\n")
    f.write(result.stderr)
    f.write(f"\n=== RETURN CODE: {result.returncode} ===\n")
print("DONE")
