import os
import re

TARGET_DIR = "thought_simulator/20_requirements"
OUTPUT_FILE = os.path.join(TARGET_DIR, "20.525.015_old_hlr_num_in_files.md")

# Regex for HLR numbers
HLR_PATTERN = re.compile(r"HLR[-_ ]?(\d{2}\.\d{3}\.\d{3})", re.IGNORECASE)

def strip_yaml(text):
    """
    Remove YAML front matter if present.
    YAML is defined as a block starting with '---' or '```yaml' and ending with '---' or '```'.
    """
    lines = text.splitlines()
    if not lines:
        return text

    # Case 1: --- YAML ---
    if lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i+1:])

    # Case 2: ```yaml ... ```
    if lines[0].strip().lower().startswith("```yaml"):
        for i in range(1, len(lines)):
            if lines[i].strip().startswith("```"):
                return "\n".join(lines[i+1:])

    return text


def extract_hlrs_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    body = strip_yaml(content)
    return sorted(set(HLR_PATTERN.findall(body)))


def main():
    files = [
        f for f in os.listdir(TARGET_DIR)
        if f.startswith("20.") and f.endswith(".md") and os.path.isfile(os.path.join(TARGET_DIR, f))
    ]

    results = []

    for filename in sorted(files):
        full_path = os.path.join(TARGET_DIR, filename)
        hlrs = extract_hlrs_from_file(full_path)

        results.append({
            "file": filename,
            "hlrs": hlrs
        })

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# 20.525.015 — Old HLR Numbers Found in 20-Series Files\n\n")
        out.write("This file is auto-generated. It lists all HLR numbers found in each 20.xx file.\n\n")

        for entry in results:
            out.write(f"## {entry['file']}\n")
            if entry["hlrs"]:
                for h in entry["hlrs"]:
                    out.write(f"- HLR-{h}\n")
            else:
                out.write("- *(No HLR numbers found)*\n")
            out.write("\n")

    print(f"Done. Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
