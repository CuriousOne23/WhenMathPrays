#!/usr/bin/env python3
"""
meaning_dct_add_entry.py
Starter tool for adding new entries to the Path A meaning dictionary.

Implements the field rules defined in meaning_dct_spec.md:
- primitive (required)
- invariants (required)
- cue_envelope (required)
- routing_signature (required)
- identity_anchor (required)
- id (required)
"""

import yaml
import sys
from pathlib import Path

DICT_PATH = Path("meaning_dictionary.yaml")


# -----------------------------
# Validation helpers
# -----------------------------

REQUIRED_FIELDS = [
    "id",
    "primitive",
    "invariants",
    "cue_envelope",
    "routing_signature",
    "identity_anchor"
]

def validate_entry(entry: dict):
    """Validate that the entry contains all required fields."""
    missing = [f for f in REQUIRED_FIELDS if f not in entry]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")


# -----------------------------
# Load dictionary
# -----------------------------

def load_dictionary():
    if not DICT_PATH.exists():
        return {"entries": {}, "metadata": {}}

    with open(DICT_PATH, "r") as f:
        return yaml.safe_load(f)


# -----------------------------
# Insert entry alphabetically
# -----------------------------

def insert_entry(dct: dict, word: str, entry: dict):
    """Insert entry under the given word, keeping alphabetical order."""
    validate_entry(entry)

    if "entries" not in dct:
        dct["entries"] = {}

    # Add or append
    if word not in dct["entries"]:
        dct["entries"][word] = []

    dct["entries"][word].append(entry)

    # Alphabetize top-level keys
    dct["entries"] = dict(sorted(dct["entries"].items(), key=lambda x: x[0]))

    return dct


# -----------------------------
# Save dictionary
# -----------------------------

def save_dictionary(dct: dict):
    with open(DICT_PATH, "w") as f:
        yaml.dump(dct, f, sort_keys=False)


# -----------------------------
# CLI interface
# -----------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: meaning_dct_add_entry.py <entry_file.yaml>")
        sys.exit(1)

    entry_file = Path(sys.argv[1])
    if not entry_file.exists():
        print(f"Entry file not found: {entry_file}")
        sys.exit(1)

    # Load entry YAML
    with open(entry_file, "r") as f:
        entry_data = yaml.safe_load(f)

    if "word" not in entry_data or "entry" not in entry_data:
        print("Entry file must contain 'word' and 'entry' fields.")
        sys.exit(1)

    word = entry_data["word"]
    entry = entry_data["entry"]

    # Load dictionary
    dct = load_dictionary()

    # Insert entry
    dct = insert_entry(dct, word, entry)

    # Save
    save_dictionary(dct)

    print(f"Added entry for word '{word}' with id '{entry['id']}'.")


if __name__ == "__main__":
    main()
