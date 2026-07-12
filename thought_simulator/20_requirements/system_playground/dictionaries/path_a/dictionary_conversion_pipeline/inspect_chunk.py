import gzip
import json
import argparse
from pathlib import Path
from pprint import pformat

# Import pipeline configuration
try:
    from config import BASE_DIR, DEV_OUTPUT_DIR
except ImportError:
    BASE_DIR = Path(__file__).parent.resolve()
    DEV_OUTPUT_DIR = BASE_DIR / "dictionaries_dev"


LOG_DIR = BASE_DIR / "inspection_logs"
LOG_DIR.mkdir(exist_ok=True)


def load_chunk(chunk_path: Path):
    with gzip.open(chunk_path, "rt", encoding="utf-8") as f:
        return json.load(f)


def resolve_chunk_path(chunk_name_or_path: str) -> Path:
    p = Path(chunk_name_or_path)

    if p.exists():
        return p

    candidate = DEV_OUTPUT_DIR / p.name
    if candidate.exists():
        return candidate

    raise FileNotFoundError(
        f"Chunk not found: {chunk_name_or_path}\n"
        f"Checked:\n"
        f"  - {p.resolve()}\n"
        f"  - {candidate.resolve()}"
    )


def filter_entries(entries, lemma=None):
    if lemma is None:
        return entries
    return [e for e in entries if lemma.lower() in e["lemma"].lower()]


def slice_entries(entries, limit):
    """
    limit can be:
        None → return all
        [N] → return first N
        [MIN, MAX] → return MIN..MAX inclusive
    """
    if limit is None:
        return entries

    if len(limit) == 1:
        n = limit[0]
        return entries[:n]

    if len(limit) == 2:
        lo, hi = limit
        return entries[lo:hi + 1]

    raise ValueError("limit must be N or MIN MAX")


def write_log(chunk_name, entries, fields):
    log_path = LOG_DIR / f"inspect_log_{chunk_name}.txt"

    with log_path.open("w", encoding="utf-8") as f:
        for entry in entries:
            if fields:
                filtered = {k: entry.get(k) for k in fields}
                f.write(pformat(filtered) + "\n")
            else:
                f.write(pformat(entry) + "\n")
            f.write("-" * 60 + "\n")

    return log_path


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a TS developer dictionary chunk."
    )

    parser.add_argument("chunk", type=str, help="Chunk filename or full path")
    parser.add_argument("--lemma", type=str, default=None,
                        help="Filter entries by lemma substring")
    parser.add_argument("--fields", type=str, nargs="+", default=None,
                        help="Only show these fields")
    parser.add_argument("--limit", type=int, nargs="+", default=None,
                        help="Show only first N entries or MIN MAX range")

    args = parser.parse_args()

    try:
        chunk_path = resolve_chunk_path(args.chunk)
    except FileNotFoundError as e:
        print(f"[inspect_chunk] {e}")
        return

    print(f"[inspect_chunk] Loading {chunk_path} ...")
    entries = load_chunk(chunk_path)
    chunk_name = chunk_path.name

    print(f"[inspect_chunk] Loaded {len(entries)} entries.")

    # Apply lemma filter
    filtered = filter_entries(entries, args.lemma)

    # Apply limit slicing
    sliced = slice_entries(filtered, args.limit)

    # Write log file
    log_path = write_log(chunk_name, sliced, args.fields)

    print("=" * 60)
    print(f"[inspect_chunk] Entries shown: {len(sliced)}")
    print(f"[inspect_chunk] Log file written to:")
    print(f"    {log_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
