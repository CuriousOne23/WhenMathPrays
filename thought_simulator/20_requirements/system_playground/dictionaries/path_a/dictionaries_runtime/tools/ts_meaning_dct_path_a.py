"""
ts_meaning_dct_path_a.py
------------------------

Creates the TS-efficient runtime dictionary for Path A by stripping
developer-only metadata from the developer dictionary chunks.

Input:
    dictionaries_dev/
        meaning_dictionary_dev_01.json.gz
        meaning_dictionary_dev_02.json.gz
        meaning_dictionary_dev_03.json.gz
        meaning_dictionary_dev_04.json.gz
        meaning_dictionary_dev_05.json.gz
        meaning_dictionary_dev_06.json.gz
        manifest.json

Output (written to the SAME directory as this script):
    ts_meaning_dictionary_01.json.gz
    ts_meaning_dictionary_02.json.gz
    ts_meaning_dictionary_03.json.gz
    ts_meaning_dictionary_04.json.gz
    ts_meaning_dictionary_05.json.gz
    ts_meaning_dictionary_06.json.gz
    manifest.json

The user must manually move the runtime files into:
    dictionaries_runtime/

This prevents accidental overwrites.
"""

import os
import json
import gzip
from pathlib import Path


class TSMeaningDctPathA:
    """
    Runtime dictionary stripper for TS Path A.
    Converts developer dictionary chunks into runtime-efficient chunks.
    """

    def __init__(self, dev_dir="dictionaries_dev", output_dir=None):
        script_dir = Path(__file__).parent

        # Developer dictionary directory
        self.dev_dir = (script_dir / dev_dir).resolve()

        # Runtime output directory (same directory as this script)
        if output_dir is None:
            self.output_dir = script_dir.resolve()
        else:
            self.output_dir = (script_dir / output_dir).resolve()

        os.makedirs(self.output_dir, exist_ok=True)

    def _load_dev_chunk(self, filename):
        """
        Loads a single developer chunk.
        """
        path = self.dev_dir / filename
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)

    def _strip_entry(self, entry):
        """
        Removes developer-only fields from a TS entry.
        Keeps only runtime-essential fields.
        """
        keep = {
            "lemma",
            "alternates",
            "primitive",
            "invariants",
            "cue_envelope",
            "routing_signature",
            "identity_anchor"
        }

        return {k: v for k, v in entry.items() if k in keep}

    def _write_runtime_chunk(self, chunk_id, entries):
        """
        Writes a single runtime chunk.
        """
        filename = f"ts_meaning_dictionary_{chunk_id:02d}.json.gz"
        path = self.output_dir / filename

        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

        return filename

    def run(self):
        """
        Executes the full runtime dictionary conversion.
        """
        print(f"[ts_meaning_dct_path_a] Loading developer manifest from {self.dev_dir}...")

        manifest_path = self.dev_dir / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            dev_manifest = json.load(f)

        runtime_manifest = []

        print("[ts_meaning_dct_path_a] Processing developer chunks...")

        for chunk in dev_manifest["chunks"]:
            chunk_id = chunk["chunk_id"]
            filename = chunk["filename"]

            print(f"  - Loading developer chunk {filename}...")
            dev_entries = self._load_dev_chunk(filename)

            print(f"  - Stripping developer metadata for chunk {chunk_id}...")
            runtime_entries = [self._strip_entry(e) for e in dev_entries]

            print(f"    • runtime entry count: {len(runtime_entries)}")

            print(f"  - Writing runtime chunk {chunk_id}...")
            runtime_filename = self._write_runtime_chunk(chunk_id, runtime_entries)

            compressed_size = os.path.getsize(self.output_dir / runtime_filename)

            runtime_manifest.append({
                "chunk_id": chunk_id,
                "filename": runtime_filename,
                "first_lemma": chunk["first_lemma"],
                "last_lemma": chunk["last_lemma"],
                "entry_count": len(runtime_entries),
                "compressed_size": compressed_size
            })

        # Write runtime manifest
        runtime_manifest_path = self.output_dir / "manifest.json"
        with open(runtime_manifest_path, "w", encoding="utf-8") as f:
            json.dump(runtime_manifest, f, indent=2, ensure_ascii=False)

        print(f"[ts_meaning_dct_path_a] Runtime manifest written to {runtime_manifest_path}")
        print("[ts_meaning_dct_path_a] Runtime dictionary chunks created successfully.")
        print(">>> Please move the ts_meaning_dictionary_XX.json.gz files into dictionaries_runtime/")
        print(">>> This prevents accidental overwrites and keeps versions self-contained.")


if __name__ == "__main__":
    TSMeaningDctPathA().run()
