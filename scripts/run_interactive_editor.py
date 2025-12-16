#!/usr/bin/env python
import sys
import subprocess
from pathlib import Path

# USAGE:
#   Edit CSV_FILE and DATA_DIR below, then run this script.
#
# Example:
#   python run_interactive_editor.py
#
# Or from command line:
#   python run_interactive_editor.py myfile.csv mydir

# --- EDIT THESE DEFAULTS ---
# CSV_FILE = "single_dating_to_love_M1.csv"  # Change to your CSV file
# DATA_DIR = "data/library/love"             # Change to your data directory
CSV_FILE = "entropy_calibration_M1_modified.csv"  # Change to your CSV file
DATA_DIR = "data/test_csv"             # Change to your data directory
# --------------------------
# --------------------------

if len(sys.argv) > 1:
    CSV_FILE = sys.argv[1]
if len(sys.argv) > 2:
    DATA_DIR = sys.argv[2]

csv_path = Path(DATA_DIR) / CSV_FILE

if not csv_path.exists():
    print(f"Error: File not found: {csv_path}")
    sys.exit(1)

cmd = [sys.executable, "tools/interactive_editor.py", str(csv_path)]
print(f"Running: {' '.join(cmd)}")
subprocess.run(cmd)

# Pause so user can see output/errors before window closes
input("\nPress Enter to exit...")
