# tests/debug_files.py
# Quick debug: show exactly what files exist and where

from pathlib import Path

# Where we are right now
print("Current folder:")
print(Path.cwd())
print()

# What the compute script thinks "data" folder is
data_folder = Path("../data")
print("Script expects data folder at:")
print(data_folder.resolve())
print()

# Does that folder exist?
if data_folder.exists():
    print("data folder FOUND")
else:
    print("data folder NOT FOUND")
    print()

# List everything in the project root
print("Files in project root (WhenMathPrays):")
for item in Path(".").iterdir():
    print("  ", item.name)
print()

# List everything in the data folder (if it exists)
if data_folder.exists():
    print("Files in data folder:")
    for item in data_folder.iterdir():
        print("  ", item.name)
else:
    print("No data folder — nothing to list")

print("\nRun this — then paste the output here.")