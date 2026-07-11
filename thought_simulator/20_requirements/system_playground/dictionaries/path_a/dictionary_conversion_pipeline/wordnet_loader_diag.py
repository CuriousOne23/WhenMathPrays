# wordnet_loader_diag.py
# Standalone diagnostics for WordNet 2.1 data.* files
# Does NOT build synsets — only prints field structure differences.

from pathlib import Path

def diag_data_file(file_path):
    print("\n====================================================")
    print("DIAGNOSTICS FOR:", file_path)
    print("====================================================\n")

    seen_layouts = set()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Skip header lines — real synset lines always begin with 8-digit offset
            if len(line) < 8 or not line[:8].isdigit():
                continue

            # Split gloss
            if " | " in line:
                data_part, gloss = line.split(" | ", 1)
            else:
                data_part, gloss = line, ""

            fields = data_part.split()

            # Record the layout signature
            layout_sig = tuple(fields)

            if layout_sig not in seen_layouts:
                seen_layouts.add(layout_sig)

                print("----------------------------------------------------")
                print("NEW FIELD LAYOUT DETECTED")
                print("Raw line:")
                print(line)
                print("\nFields:")
                for i, f in enumerate(fields):
                    print(f"  [{i}] {f}")

                print("\nGloss:")
                print(gloss)

                print("----------------------------------------------------\n")

def run_diag(base_dir="wordnet_raw"):
    base = Path(base_dir)

    data_files = {
        "noun": base / "data.noun",
        "verb": base / "data.verb",
        "adj":  base / "data.adj",
        "adv":  base / "data.adv",
    }

    for pos, file_path in data_files.items():
        diag_data_file(file_path)

if __name__ == "__main__":
    run_diag()
