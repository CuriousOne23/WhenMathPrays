import gzip
import json
import argparse
from pathlib import Path
from pprint import pprint


def load_chunk(chunk_path: Path):
    """
    Load a gzipped JSON developer dictionary chunk.

    Returns:
        list of dict: TS developer dictionary entries.
    """
    with gzip.open(chunk_path, "rt", encoding="utf-8") as f:
        return json.load(f)


def inspect_entries(entries, lemma=None, fields=None, limit=None):
    """
    Pretty-print entries with optional filtering.

    Parameters:
        lemma (str): substring filter on entry["lemma"]
        fields (list[str]): only show these fields
        limit (int): show only first N entries
    """
    count = 0

    for entry in entries:
        # Lemma substring filter
        if lemma and lemma.lower() not in entry["lemma"].lower():
            continue

        # Field filtering
        if fields:
            filtered = {k: entry.get(k) for k in fields}
            pprint(filtered)
        else:
            pprint(entry)

        print("-" * 60)
        count += 1

        if limit and count >= limit:
            break


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a TS developer dictionary chunk (meaning_dictionary_dev_XX.json.gz)."
    )

    parser.add_argument(
        "chunk",
        type=str,
        help="Path to meaning_dictionary_dev_XX.json.gz"
    )

    parser.add_argument(
        "--lemma",
        type=str,
        default=None,
        help="Filter entries by lemma substring"
    )

    parser.add_argument(
        "--fields",
        type=str,
        nargs="+",
        default=None,
        help="Only show these fields (e.g., --fields lemma gloss primitives)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Show only the first N entries"
    )

    args = parser.parse_args()

    chunk_path = Path(args.chunk)

    if not chunk_path.exists():
        print(f"[inspect_chunk] Error: file not found: {chunk_path}")
        return

    print(f"[inspect_chunk] Loading {chunk_path} ...")
    entries = load_chunk(chunk_path)

    print(f"[inspect_chunk] Loaded {len(entries)} entries.")
    print("=" * 60)

    inspect_entries(
        entries,
        lemma=args.lemma,
        fields=args.fields,
        limit=args.limit
    )


if __name__ == "__main__":
    main()
