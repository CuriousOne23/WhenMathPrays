# tests/debug_files.py
from pathlib import Path

print("=== DEBUG: Where are the files? ===\n")
print(f"Current working directory: {Path.cwd()}\n")

data_path = Path("../data")
print(f"Script looks for data folder here: {data_path.resolve()}")
print(f"Does this folder exist? → {data_path.exists()}\n")

if data_path.exists():
    print("Files inside data folder:")
    for f in data_path.iterdir():
        print("   →", f.name)
else:
    print("data folder NOT found!\n")

print("\nFiles in project root (WhenMathPrays):")
for f in Path(".").iterdir():
    if f.is_file():
        print("   →", f.name)

print("\nRun complete.")