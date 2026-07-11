# wordnet_loader_diag.py
# Standalone diagnostics for WordNet 2.1 data.* files.
# Compares DIAG parsing vs REAL parsing logic (embedded here).
# Logs detailed differences to a file, prints only summaries to terminal.

from pathlib import Path
import os

MAX_DIFFERENCES = 10
LOG_FILE = "wordnet_diag.log"


def log(msg: str) -> None:
    """Append a single line to the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        lf.write(msg + "\n")


# ------------------------------------------------------------
# REAL PARSER LOGIC (embedded copy from your wordnet_loader.py)
# ------------------------------------------------------------
def real_parse(fields, gloss):
    """
    This is a copy of your real parsing logic.
    It returns a dict describing what the real parser thinks the synset contains.
    """

    offset = int(fields[0])
    lex_filenum = int(fields[1])
    pos_code = fields[2]

    lemma_count = int(fields[3])
    lemma_start = 4

    lemmas = []
    lex_ids = []

    # WordNet 2.1 alternates lemma and lex_id
    for i in range(lemma_count):
        lemma = fields[lemma_start + 2 * i]
        lex_id = int(fields[lemma_start + 2 * i + 1])
        lemmas.append(lemma)
        lex_ids.append(lex_id)

    # Pointer count index
    ptr_count_index = lemma_start + 2 * lemma_count
    ptr_count = int(fields[ptr_count_index])

    ptr_start = ptr_count_index + 1
    ptr_end = ptr_start + ptr_count * 4

    pointers_raw = fields[ptr_start:ptr_end]
    pointers = []
    for i in range(0, len(pointers_raw), 4):
        pointers.append(
            {
                "symbol": pointers_raw[i],
                "offset": int(pointers_raw[i + 1]),
                "pos": pointers_raw[i + 2],
                "src_tgt": pointers_raw[i + 3],
            }
        )

    return {
        "offset": offset,
        "pos": pos_code,
        "lex_filenum": lex_filenum,
        "lemmas": lemmas,
        "lex_ids": lex_ids,
        "ptr_count": ptr_count,
        "pointers": pointers,
        "gloss": gloss,
    }


# ------------------------------------------------------------
# DIAGNOSTIC PARSER (raw fields only)
# ------------------------------------------------------------
def diag_parse(fields, gloss):
    """
    The diagnostic parser simply returns the raw fields and gloss.
    """
    return {
        "fields": fields,
        "gloss": gloss,
    }


# ------------------------------------------------------------
# FIELD CLASSIFIER (Option 1 structural mapping)
# ------------------------------------------------------------
def classify_field(f):
    # Basic categories
    if f.isdigit():
        return "INT"

    # Offset (8-digit)
    if len(f) == 8 and f.isdigit():
        return "OFFSET"

    # POS
    if f in {"n", "v", "a", "s", "r"}:
        return "POS"

    # Pointer symbols
    if f in {"@", "~", "+", "-", "%p", "&", "!", "^", "$", ">", "*", "\\"}:
        return "POINTER_SYMBOL"

    # Morph / domain markers
    if f in {";c", ";u", "#m"}:
        return "MORPH_MARKER"

    # Satellite / sense markers (single letters)
    if len(f) == 1 and f.isalpha():
        return "SENSE_MARKER"

    # Lex_id-like (single digit)
    if len(f) == 1 and f.isdigit():
        return "LEX_ID"

    # Zero-prefixed class markers like 0a, 0b, 0c, 0d, 0f
    if len(f) == 2 and f[0] == "0" and f[1].isalpha():
        return "CLASS_MARKER"

    # Frame codes like 0101, 0202, 0301, etc.
    if len(f) == 4 and f.isdigit():
        return "FRAME_CODE"

    # Everything else: lemma or unknown
    return "LEMMA_OR_OTHER"


def classify_line(fields):
    return [(i, f, classify_field(f)) for i, f in enumerate(fields)]


# ------------------------------------------------------------
# DIFF ENGINE
# ------------------------------------------------------------
def diff(real, diag):
    """
    Compare real parser output vs diag parser output.
    Return a list of differences.
    """

    differences = []

    # Compare lemma list
    if "lemmas" in real:
        if real["lemmas"] != diag["fields"][4 : 4 + 2 * len(real["lemmas"]) : 2]:
            differences.append(("lemmas", real["lemmas"], diag["fields"]))

    # Compare lex_ids
    if "lex_ids" in real:
        if real["lex_ids"] != [
            int(x) for x in diag["fields"][5 : 5 + 2 * len(real["lex_ids"]) : 2]
        ]:
            differences.append(("lex_ids", real["lex_ids"], diag["fields"]))

    # Compare pointer count
    if "ptr_count" in real:
        lemma_count = len(real["lemmas"])
        diag_ptr_count = diag["fields"][4 + 2 * lemma_count]
        # Normalize diag pointer count (strip leading zeros)
        diag_ptr_norm = diag_ptr_count.lstrip("0") or "0"

        if str(real["ptr_count"]) != diag_ptr_norm:
            differences.append(("ptr_count", real["ptr_count"], diag_ptr_count))

    return differences


# ------------------------------------------------------------
# MAIN DIAGNOSTIC LOOP
# ------------------------------------------------------------
def diag_data_file(file_path: Path):
    print("\n====================================================")
    print("DIAGNOSTICS FOR:", file_path)
    print("====================================================\n")

    diff_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Skip header lines
            if len(line) < 8 or not line[:8].isdigit():
                continue

            # Split gloss
            if " | " in line:
                data_part, gloss = line.split(" | ", 1)
            else:
                data_part, gloss = line, ""

            fields = data_part.split()

            # Run both parsers
            diag_result = diag_parse(fields, gloss)

            try:
                real_result = real_parse(fields, gloss)
            except Exception as e:
                log("----------------------------------------------------")
                log("REAL PARSER ERROR")
                log("Raw line:")
                log(line)
                log(f"Exception: {e}")
                log("")
                log("Classified fields:")
                for i, fval, kind in classify_line(fields):
                    log(f"  [{i}] {fval:20} -> {kind}")
                log("----------------------------------------------------\n")

                diff_count += 1
                if diff_count >= MAX_DIFFERENCES:
                    print(
                        f">>> Reached {MAX_DIFFERENCES} differences in {file_path}. "
                        f"Full details in {LOG_FILE}."
                    )
                    return
                continue

            # Compare
            differences = diff(real_result, diag_result)

            if not differences:
                # Line parsed cleanly; no logging needed
                continue

            # Log differences
            log("----------------------------------------------------")
            log("DIFFERENCE DETECTED")
            log("Raw line:")
            log(line)
            log("")
            log("Differences:")
            for d in differences:
                log(f"  Field: {d[0]}")
                log(f"  Real:  {d[1]}")
                log(f"  Diag:  {d[2]}")
                log("")
            log("----------------------------------------------------\n")

            diff_count += 1
            if diff_count >= MAX_DIFFERENCES:
                print(
                    f">>> Reached {MAX_DIFFERENCES} differences in {file_path}. "
                    f"Full details in {LOG_FILE}."
                )
                return

    # Terminal summary per file
    if diff_count == 0:
        print(f"No differences found for {file_path}.")
    else:
        print(
            f"{diff_count} differences found for {file_path}. "
            f"See {LOG_FILE} for details."
        )


def run_diag(base_dir="wordnet_raw"):
    # Reset log at start of run
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    base = Path(base_dir)

    data_files = {
        "noun": base / "data.noun",
        "verb": base / "data.verb",
        "adj": base / "data.adj",
        "adv": base / "data.adv",
    }

    for pos, file_path in data_files.items():
        diag_data_file(file_path)

    print("\nDiagnostics complete.")
    print(f"Full detailed output written to {LOG_FILE}.")


if __name__ == "__main__":
    run_diag()
