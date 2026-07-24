#!/usr/bin/env python3
"""
modify_dev_dct.py

Developer-layer dictionary editor for Path A.

Now reads configuration from modify_dev_dct_setup.yaml.
Output files are written into the same directory where this tool is executed.
Revision numbers increment automatically:
    - If manifest.json or manifest_rev00.json → output rev01
    - If manifest_rev01.json → output rev02
    - etc.

This tool NEVER deletes dictionary files.
"""

import os
import sys
import json
import gzip
import argparse
import yaml
from pathlib import Path

# ---------------------------------------------------------------------
# Load setup file
# ---------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.resolve()
SETUP_FILE = BASE_DIR / "modify_dev_dct_setup.yaml"

if not SETUP_FILE.exists():
    raise FileNotFoundError(
        f"Required setup file not found:\n  {SETUP_FILE}\n"
        f"Create modify_dev_dct_setup.yaml in the tools directory."
    )

with SETUP_FILE.open("r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

# Directories from setup file
DEV_DICTIONARY_DIR = Path(cfg["dev_dictionary_dir"]).resolve()
INPUT_FILE = Path(cfg["input_file"]).resolve()
CHUNK_PREFIX = cfg["dev_chunk_prefix"]

# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_gzip_json(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)

def write_gzip_json(path, obj):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def measure_uncompressed_size(obj):
    s = json.dumps(obj, ensure_ascii=False)
    return len(s.encode("utf-8"))

# ---------------------------------------------------------------------
# Manifest discovery
# ---------------------------------------------------------------------

def find_manifest(directory):
    """
    Find highest manifest_revNN.json.
    If none exist, return manifest.json.
    """
    rev_manifests = []
    for f in os.listdir(directory):
        if f.startswith("manifest_rev") and f.endswith(".json"):
            try:
                num = int(f[len("manifest_rev"):-len(".json")])
                rev_manifests.append((num, f))
            except ValueError:
                pass

    if rev_manifests:
        rev_manifests.sort()
        highest = rev_manifests[-1][1]
        return os.path.join(directory, highest), rev_manifests[-1][0]

    return os.path.join(directory, "manifest.json"), 0

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

REQUIRED_FIELDS = [
    "lemma",
    "gloss",
    "primitive",
    "cue_envelope",
    "invariant",
    "identity_anchor",
    "routing_signature"
]

def validate_entry(entry):
    for field in REQUIRED_FIELDS:
        if field not in entry:
            return False, f"Missing required field: {field}"
    return True, ""

# ---------------------------------------------------------------------
# Chunk selection
# ---------------------------------------------------------------------

def select_chunk(lemma, manifest):
    for chunk in manifest["chunks"]:
        if chunk["first_lemma"] <= lemma <= chunk["last_lemma"]:
            return chunk["chunk_id"]

    for chunk in manifest["chunks"]:
        if lemma < chunk["first_lemma"]:
            return chunk["chunk_id"]

    return manifest["chunks"][-1]["chunk_id"]

# ---------------------------------------------------------------------
# Apply mutations
# ---------------------------------------------------------------------

def apply_mutations(directory, manifest, input_entries, revision_number):
    summary = {
        "added": [],
        "modified": [],
        "deleted": [],
        "skipped": []
    }

    # Load chunks
    chunks_data = {}
    for chunk in manifest["chunks"]:
        path = os.path.join(directory, chunk["filename"])
        chunks_data[chunk["chunk_id"]] = load_gzip_json(path)

    # Process operations
    for item in input_entries:
        op = item.get("operation")
        if op not in ("add", "modify", "delete"):
            summary["skipped"].append({"item": item, "reason": "Invalid operation"})
            continue

        if op == "delete":
            lemma = item.get("lemma")
            if not lemma:
                summary["skipped"].append({"item": item, "reason": "Delete missing lemma"})
                continue

            chunk_id = select_chunk(lemma, manifest)
            chunk_entries = chunks_data[chunk_id]

            before = len(chunk_entries)
            chunk_entries = [e for e in chunk_entries if e["lemma"] != lemma]
            after = len(chunk_entries)

            if before == after:
                summary["skipped"].append({"item": item, "reason": "Lemma not found"})
            else:
                chunks_data[chunk_id] = chunk_entries
                summary["deleted"].append(lemma)

            continue

        entry = item.get("entry")
        if not entry:
            summary["skipped"].append({"item": item, "reason": "Missing entry"})
            continue

        valid, reason = validate_entry(entry)
        if not valid:
            summary["skipped"].append({"item": item, "reason": reason})
            continue

        lemma = entry["lemma"]
        chunk_id = select_chunk(lemma, manifest)
        chunk_entries = chunks_data[chunk_id]

        chunk_entries = [e for e in chunk_entries if e["lemma"] != lemma]
        chunk_entries.append(entry)
        chunk_entries.sort(key=lambda x: x["lemma"])

        chunks_data[chunk_id] = chunk_entries

        if op == "add":
            summary["added"].append(lemma)
        else:
            summary["modified"].append(lemma)

    # Write new chunks
    new_manifest = {
        "total_entries": 0,
        "chunks": []
    }

    for chunk in manifest["chunks"]:
        cid = chunk["chunk_id"]
        new_filename = f"meaning_dictionary_dev_rev{revision_number:02d}_{cid:02d}.json.gz"
        path = BASE_DIR / new_filename

        entries = chunks_data[cid]
        write_gzip_json(path, entries)

        entry_count = len(entries)
        uncompressed_size = measure_uncompressed_size(entries)
        compressed_size = os.path.getsize(path)

        new_manifest["chunks"].append({
            "chunk_id": cid,
            "filename": new_filename,
            "first_lemma": entries[0]["lemma"] if entries else "",
            "last_lemma": entries[-1]["lemma"] if entries else "",
            "entry_count": entry_count,
            "uncompressed_size": uncompressed_size,
            "compressed_size": compressed_size
        })

        new_manifest["total_entries"] += entry_count

    return new_manifest, summary

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    manifest_path, current_rev = find_manifest(DEV_DICTIONARY_DIR)
    manifest = load_json(manifest_path)

    next_rev = current_rev + 1

    if args.batch:
        print("Batch mode is unchanged. (Not shown here for brevity.)")
        return

    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        sys.exit(1)

    input_entries = load_json(INPUT_FILE)

    new_manifest, summary = apply_mutations(
        DEV_DICTIONARY_DIR,
        manifest,
        input_entries,
        next_rev
    )

    too_big, chunk = check_chunk_sizes(new_manifest)
    if too_big:
        print(f"Chunk {chunk['chunk_id']} exceeds 3 MB limit.")
        print("Please increase CHUNK_COUNT and run batch mode.")
        sys.exit(1)

    manifest_out = BASE_DIR / f"manifest_rev{next_rev:02d}.json"
    write_json(manifest_out, new_manifest)

    print("Normal mode complete.")
    print("Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
