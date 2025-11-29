# tests/debug_csv.py
from pathlib import Path

filename = "Single_Dating_2_Love_M1_gamma_self_table.csv"
path = Path("data") / filename

print(f"Looking for file: {path.resolve()}")
print(f"File exists? → {path.exists()}\n")

if not path.exists():
    print("FILE NOT FOUND. STOP.")
else:
    print("FILE FOUND. Printing first 10 lines exactly as read:\n")
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            print(f"Line {i}: {repr(line)}")