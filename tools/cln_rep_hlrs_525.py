import os
import re

INPUT_FILE = "thought_simulator/20_requirements/20.525.015_old_hlr_num_in_files.md"
OUTPUT_FILE = "thought_simulator/20_requirements/20.525.015.001_rep_hlrs_remvd.md"

# Matches lines like:
# - HLR-20.001-001
HLR_LINE = re.compile(r"-\s*(HLR-\d{2,3}\.\d{3}(?:\.\d{3})?-\d{3})", re.IGNORECASE)

def process_file():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output = []
    seen = set()
    current_file = None
    seen_in_file = set()

    for line in lines:
        # Detect file section header
        if line.startswith("## "):
            current_file = line.strip()
            seen_in_file = set()  # reset for each file
            output.append(line)
            continue

        # Try to match an HLR line
        m = HLR_LINE.search(line)
        if m:
            hlr = m.group(1)

            if hlr not in seen_in_file:
                # First time this HLR appears in this file → keep it
                seen_in_file.add(hlr)
                output.append(line)
            else:
                # Duplicate within same file → skip it
                continue
        else:
            # Non-HLR line → keep it
            output.append(line)

    # Write cleaned output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.writelines(output)

    print(f"Cleaned report written to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_file()
