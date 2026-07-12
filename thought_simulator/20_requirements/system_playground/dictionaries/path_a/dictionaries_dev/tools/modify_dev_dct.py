#!/usr/bin/env python3
"""
modify_dev_dct.py

Developer-layer dictionary editor for Path A.

Supports:
    - add entries
    - modify entries
    - delete entries

Two modes:
    - normal mode (default)
    - batch mode (--batch)

Normal mode:
    - Loads highest manifest_revNN.json (or manifest.json)
    - Applies local edits
    - Writes new chunk files
    - Writes manifest_rev(NN+1).json
    - Enforces chunk size limits (2.5–3.0 MB)

Batch mode:
    - Requires user to manually increase CHUNK_COUNT in config.py
    - Re-chunks entire dictionary using WDP
    - Writes new chunk files
    - Writes manifest_rev(NN+1).json

This tool NEVER deletes dictionary files.
"""

import os
import sys
import json
import gzip
import argparse
from pathlib import Path

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
    """Return uncompressed JSON byte size."""
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

    # fallback
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
    """Validate TS developer entry structure."""
    for field in REQUIRED_FIELDS:
        if field not in entry:
            return False, f"Missing required field: {field}"
    return True, ""

# ---------------------------------------------------------------------
# Chunk selection
# ---------------------------------------------------------------------

def select_chunk(lemma, manifest):
    """
    Determine which chunk a lemma belongs to.
    """
    for chunk in manifest["chunks"]:
        if chunk["first_lemma"] <= lemma <= chunk["last_lemma"]:
            return chunk["chunk_id"]

    # If outside all ranges, find lexicographic position
    # Insert into the chunk whose range it should fall into
    for chunk in manifest["chunks"]:
        if lemma < chunk["first_lemma"]:
            return chunk["chunk_id"]

    # Otherwise last chunk
    return manifest["chunks"][-1]["chunk_id"]

# ---------------------------------------------------------------------
# Apply mutations
# ---------------------------------------------------------------------

def apply_mutations(directory, manifest, input_entries, revision_number):
    """
    Apply add/modify/delete operations in normal mode.
    """
    summary = {
        "added": [],
        "modified": [],
        "deleted": [],
        "skipped": []
    }

    # Load all chunks into memory
    chunks_data = {}
    for chunk in manifest["chunks"]:
        path = os.path.join(directory, chunk["filename"])
        chunks_data[chunk["chunk_id"]] = load_gzip_json(path)

    # Process each operation
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

        # add or modify
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

        # remove old version if exists
        chunk_entries = [e for e in chunk_entries if e["lemma"] != lemma]
        chunk_entries.append(entry)
        chunk_entries.sort(key=lambda x: x["lemma"])

        chunks_data[chunk_id] = chunk_entries

        if op == "add":
            summary["added"].append(lemma)
        else:
            summary["modified"].append(lemma)

    # Write new chunk files
    new_manifest = {
        "total_entries": 0,
        "chunks": []
    }

    for chunk in manifest["chunks"]:
        cid = chunk["chunk_id"]
        new_filename = f"meaning_dictionary_dev_rev{revision_number:02d}_{cid:02d}.json.gz"
        path = os.path.join(directory, new_filename)

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
# Chunk size enforcement
# ---------------------------------------------------------------------

def check_chunk_sizes(manifest):
    """
    Return True if any chunk exceeds 3 MB uncompressed.
    """
    for chunk in manifest["chunks"]:
        if chunk["uncompressed_size"] > 3_000_000:
            return True, chunk
    return False, None

# ---------------------------------------------------------------------
# Batch mode WDP re-chunking
# ---------------------------------------------------------------------

def batch_rechunk(directory, manifest, revision_number):
    """
    Full WDP re-chunking.
    Requires CHUNK_COUNT to be manually increased in config.py.
    """
    # Load config
    config = load_json(os.path.join(directory, "config.py.json"))
    chunk_count = config["CHUNK_COUNT"]

    # Load all entries
    all_entries = []
    for chunk in manifest["chunks"]:
        path = os.path.join(directory, chunk["filename"])
        all_entries.extend(load_gzip_json(path))

    # Sort by lemma
    all_entries.sort(key=lambda x: x["lemma"])

    # Compute WDP sizes
    sizes = [measure_uncompressed_size(e) for e in all_entries]
    total = sum(sizes)
    target = total / chunk_count

    # Split into chunks
    new_chunks = []
    current = []
    current_size = 0
    idx = 0

    for entry, size in zip(all_entries, sizes):
        if current_size + size > target and len(new_chunks) < chunk_count - 1:
            new_chunks.append(current)
            current = []
            current_size = 0
        current.append(entry)
        current_size += size

    new_chunks.append(current)

    # Write new chunks + manifest
    new_manifest = {
        "total_entries": len(all_entries),
        "chunks": []
    }

    for i, chunk_entries in enumerate(new_chunks, start=1):
        filename = f"meaning_dictionary_dev_rev{revision_number:02d}_{i:02d}.json.gz"
        path = os.path.join(directory, filename)
        write_gzip_json(path, chunk_entries)

        uncompressed_size = measure_uncompressed_size(chunk_entries)
        compressed_size = os.path.getsize(path)

        new_manifest["chunks"].append({
            "chunk_id": i,
            "filename": filename,
            "first_lemma": chunk_entries[0]["lemma"] if chunk_entries else "",
            "last_lemma": chunk_entries[-1]["lemma"] if chunk_entries else "",
            "entry_count": len(chunk_entries),
            "uncompressed_size": uncompressed_size,
            "compressed_size": compressed_size
        })

    return new_manifest

# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="dictionaries_dev")
    parser.add_argument("--input", default=None)
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()

    directory = args.dir
    input_file = args.input or os.path.join(directory, "modify_entries.json")

    manifest_path, current_rev = find_manifest(directory)
    manifest = load_json(manifest_path)

    next_rev = current_rev + 1

    if args.batch:
        # Batch mode
        config_path = os.path.join(directory, "config.py.json")
        if not os.path.exists(config_path):
            print("ERROR: config.py.json not found.")
            sys.exit(1)

        config = load_json(config_path)
        if config["CHUNK_COUNT"] <= len(manifest["chunks"]):
            print("ERROR: CHUNK_COUNT must be manually increased before batch mode.")
            sys.exit(1)

        new_manifest = batch_rechunk(directory, manifest, next_rev)
        manifest_out = os.path.join(directory, f"manifest_rev{next_rev:02d}.json")
        write_json(manifest_out, new_manifest)

        print(f"Batch mode complete. New manifest: {manifest_out}")
        return

    # Normal mode
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)

    input_entries = load_json(input_file)

    new_manifest, summary = apply_mutations(directory, manifest, input_entries, next_rev)

    # Check chunk sizes
    too_big, chunk = check_chunk_sizes(new_manifest)
    if too_big:
        print(f"Chunk {chunk['chunk_id']} exceeds 3 MB limit.")
        print("Normal mode cannot continue.")
        print("Please increase CHUNK_COUNT in config.py and run batch mode.")
        sys.exit(1)

    manifest_out = os.path.join(directory, f"manifest_rev{next_rev:02d}.json")
    write_json(manifest_out, new_manifest)

    print("Normal mode complete.")
    print("Summary:")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
