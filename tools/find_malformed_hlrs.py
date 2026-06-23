import os
import re

TARGET_DIR = "thought_simulator/20_requirements"
OUTPUT_FILE = os.path.join(TARGET_DIR, "20.525.016_old_malformed_hlrs.md")

# --- VALID PATTERNS ---------------------------------------------------------

# Correct forms:
#   HLR-20.xx-nnn
#   HLR-20.xxx-nnn
#   HLR-20.xx.yyy-nnn
#   HLR-20.xxx.yyy-nnn
VALID = re.compile(
    r"(HLR|LLR|INV)-20\.\d{2,3}(?:\.\d{3})?-\d{3}",
    re.IGNORECASE
)

# --- MALFORMED PATTERNS -----------------------------------------------------

# Wrong separator: dot instead of dash before final segment
MALFORMED_DOT = re.compile(
    r"(HLR|LLR|INV)[^\d]*20\.\d{2,3}(?:\.\d{3})\.\d{3}",
    re.IGNORECASE
)

# Wrong prefix separator: HLR.20.xx-nnn
MALFORMED_PREFIX_DOT = re.compile(
    r"(HLR|LLR|INV)\.20\.\d{2,3}(?:\.\d{3})?-\d{3}",
    re.IGNORECASE
)

# Wrong prefix separator: HLR_20.xx-nnn
MALFORMED_PREFIX_UNDERSCORE = re.compile(
    r"(HLR|LLR|INV)_20\.\d{2,3}(?:\.\d{3})?-\d{3}",
    re.IGNORECASE
)

# Wrong prefix separator: HLR 20.xx-nnn
MALFORMED_PREFIX_SPACE = re.compile(
    r"(HLR|LLR|INV)\s20\.\d{2,3}(?:\.\d{3})?-\d{3}",
    re.IGNORECASE
)

# Collect all malformed patterns
MALFORMED_PATTERNS = [
    MALFORMED_DOT,
    MALFORMED_PREFIX_DOT,
    MALFORMED_PREFIX_UNDERSCORE,
    MALFORMED_PREFIX_SPACE,
]

# --- YAML STRIPPER ----------------------------------------------------------

def strip_yaml(text):
    lines = text.splitlines()
    if not lines:
        return text

    # Only remove FIRST YAML block
    if lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i+1:])
        return text

    # Fenced YAML
    if lines[0].strip().lower().startswith("```yaml"):
        for i in range(1, len(lines)):
            if lines[i].strip().startswith("```"):
                return "\n".join(lines[i+1:])
        return text

    return text

# --- MAIN EXTRACTION --------------------------------------------------------

def find_malformed(text):
    body = strip_yaml(text)

    malformed = set()

    for pattern in MALFORMED_PATTERNS:
        for m in pattern.findall(body):
            malformed.add(m)

    # Remove any that are actually valid
    cleaned = set()
    for m in malformed:
        if not VALID.search(m):
            cleaned.add(m)

    return sorted(cleaned)


def main():
    files = [
        f for f in os.listdir(TARGET_DIR)
        if f.startswith("20.") and f.endswith(".md")
    ]

    results = {}

    for filename in sorted(files):
        full_path = os.path.join(TARGET_DIR, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read()

        malformed = find_malformed(text)
        results[filename] = malformed

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# 20.525.016 — Malformed HLR/LLR/INV Identifiers\n\n")
        out.write("This file lists malformed requirement identifiers found in the 20-series files.\n\n")

        for filename, malformed in results.items():
            out.write(f"## {filename}\n")
            if malformed:
                for m in malformed:
                    out.write(f"- {m}\n")
            else:
                out.write("- *(none found)*\n")
            out.write("\n")

    print(f"Done. Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
