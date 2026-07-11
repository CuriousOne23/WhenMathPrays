# wordnet_parser.py
# Final WordNet 2.1 data.* parser (robust to hex counts and markers)

from pathlib import Path

import os

# ------------------------------------------------------------
# FIELD CLASSIFIER (same spirit as your diag)
# ------------------------------------------------------------
def classify_field(f):
    if len(f) == 8 and f.isdigit():
        return "OFFSET"

    if f.isdigit():
        return "INT"

    if f in {"n", "v", "a", "s", "r"}:
        return "POS"

    if f in {"@", "~", "+", "-", "%p", "&", "!", "^", "$", ">", "*", "\\"}:
        return "POINTER_SYMBOL"

    if f in {";c", ";u", "#m"}:
        return "MORPH_MARKER"

    if len(f) == 2 and f[0] == "0" and f[1].isalpha():
        return "CLASS_MARKER"

    if len(f) == 1 and f.isalpha():
        return "SENSE_MARKER"

    if len(f) == 4 and f.isdigit():
        return "FRAME_CODE"

    return "LEMMA_OR_OTHER"


# ------------------------------------------------------------
# CORE LINE PARSER
# ------------------------------------------------------------
def parse_wordnet_line(line):
    """
    Parse a single WordNet 2.1 data.* line into a structured dict.
    Handles:
      - hex word counts (0a, 0b, 0c, 0d, ...)
      - extra markers (class markers, morph markers, etc.)
      - pointers
      - leaves any trailing structural stuff in 'extra_fields'
    """

    # Split gloss
    if " | " in line:
        data_part, gloss = line.split(" | ", 1)
    else:
        data_part, gloss = line, ""

    fields = data_part.split()
    if len(fields) < 4:
        return None  # header or malformed

    # Offset, lex_filenum, POS
    offset = int(fields[0])
    lex_filenum = int(fields[1])
    pos = fields[2]

    # Word count is hex (e.g., 0b -> 11)
    w_cnt_raw = fields[3]
    try:
        w_cnt = int(w_cnt_raw, 16)
    except ValueError:
        # Fallback: if it's not hex, try decimal
        w_cnt = int(w_cnt_raw)

    lemmas = []
    lex_ids = []

    idx = 4
    # Collect lemmas + lex_ids using classifier, until we reach w_cnt lemmas
    while idx < len(fields) and len(lemmas) < w_cnt:
        kind = classify_field(fields[idx])

        if kind == "LEMMA_OR_OTHER":
            lemma = fields[idx]
            lex_id = 0

            # Try to read a following INT as lex_id
            if idx + 1 < len(fields) and classify_field(fields[idx + 1]) == "INT":
                lex_id = int(fields[idx + 1])
                idx += 2
            else:
                idx += 1

            lemmas.append(lemma)
            lex_ids.append(lex_id)

        else:
            # Skip markers that appear between count and lemmas (rare)
            idx += 1

    # Pointer count
    if idx >= len(fields):
        ptr_count = 0
        pointers = []
        extra_fields = []
    else:
        ptr_count_raw = fields[idx]
        try:
            ptr_count = int(ptr_count_raw)
        except ValueError:
            # If something weird is here, treat as 0 and push into extras
            ptr_count = 0

        idx += 1

        pointers = []
        for _ in range(ptr_count):
            if idx + 3 >= len(fields):
                break
            symbol = fields[idx]
            offset_p = int(fields[idx + 1])
            pos_p = fields[idx + 2]
            src_tgt = fields[idx + 3]
            pointers.append({
                "symbol": symbol,
                "offset": offset_p,
                "pos": pos_p,
                "src_tgt": src_tgt,
            })
            idx += 4

        # Anything left is structural stuff we’re not fully decoding yet
        extra_fields = fields[idx:]

    return {
        "offset": offset,
        "lex_filenum": lex_filenum,
        "pos": pos,
        "w_cnt_raw": w_cnt_raw,
        "w_cnt": w_cnt,
        "lemmas": lemmas,
        "lex_ids": lex_ids,
        "ptr_count": ptr_count,
        "pointers": pointers,
        "extra_fields": extra_fields,
        "gloss": gloss,
        "raw_fields": fields,
    }


# ------------------------------------------------------------
# FILE PARSER
# ------------------------------------------------------------
def parse_wordnet_file(path):
    """
    Parse an entire WordNet data.* file.
    Returns a list of synset dicts.
    """
    synsets = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Skip header lines (non-digit at start)
            if len(line) < 8 or not line[:8].isdigit():
                continue

            syn = parse_wordnet_line(line)
            if syn is not None:
                synsets.append(syn)
    return synsets


# ------------------------------------------------------------
# EXAMPLE DRIVER
# ------------------------------------------------------------
def parse_all_wordnet(base_dir="wordnet_raw"):
    base = Path(base_dir)
    files = {
        "noun": base / "data.noun",
        "verb": base / "data.verb",
        "adj":  base / "data.adj",
        "adv":  base / "data.adv",
    }

    all_data = {}
    for pos, fp in files.items():
        all_data[pos] = parse_wordnet_file(fp)
    return all_data


if __name__ == "__main__":
    data = parse_all_wordnet()
    # Minimal summary
    for pos, synsets in data.items():
        print(f"{pos}: {len(synsets)} synsets parsed.")
