# wordnet_loader_diag.py
# Incremental diagnostics for WordNet 2.1 data.* files.
# Prints only 10 NEW field layouts, then exits.

from pathlib import Path

MAX_NEW_LAYOUTS = 10

# Start with an empty whitelist; you will add shapes here as you learn them.
KNOWN_LAYOUTS = set()

def layout_signature(fields):
    """
    Create a signature based on the *shape* of the fields,
    not the exact content. This helps detect structural differences.
    """
    sig = []
    for f in fields:
        if f.isdigit():
            sig.append("INT")
        elif f.isalpha():
            sig.append("ALPHA")
        elif f.replace("_", "").isalnum():
            sig.append("ALNUM")
        else:
            sig.append("OTHER")
    return tuple(sig)


def diag_data_file(file_path, known_shapes):
    print("\n====================================================")
    print("DIAGNOSTICS FOR:", file_path)
    print("====================================================\n")

    new_count = 0

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
            sig = layout_signature(fields)

            # Skip known shapes
            if sig in known_shapes:
                continue

            # New shape detected
            known_shapes.add(sig)
            new_count += 1

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

            if new_count >= MAX_NEW_LAYOUTS:
                print(">>> Reached limit of 10 new layouts. Exiting diagnostics.")
                return True  # signal to stop

    return False  # continue


def run_diag(base_dir="wordnet_raw"):
    base = Path(base_dir)

    data_files = {
        "noun": base / "data.noun",
        "verb": base / "data.verb",
        "adj":  base / "data.adj",
        "adv":  base / "data.adv",
    }

    known_shapes = set(KNOWN_LAYOUTS)

    for pos, file_path in data_files.items():
        stop = diag_data_file(file_path, known_shapes)
        if stop:
            break

    print("\n>>> FINAL KNOWN SHAPES (add these to KNOWN_LAYOUTS):")
    for shape in known_shapes:
        print(shape)


if __name__ == "__main__":
    run_diag()
