"""
batch_converter.py
------------------

Runs the full TS Path A dictionary conversion pipeline:

    WordNet → Synset → TS Entry → Chunked JSON Dictionary

This module orchestrates:
    • WordNetLoader
    • TSEntryBuilder
    • JSONGzipWriter (chunk-aware)

Produces:
    dictionaries_dev/
        meaning_dictionary_dev_01.json.gz
        meaning_dictionary_dev_02.json.gz
        meaning_dictionary_dev_03.json.gz
        meaning_dictionary_dev_04.json.gz
        meaning_dictionary_dev_05.json.gz
        meaning_dictionary_dev_06.json.gz
        manifest.json
"""

import json
from pathlib import Path
from wordnet_loader import load_wordnet
from ts_entry_builder import TSEntryBuilder
from json_gzip_writer import JSONGzipWriter


class BatchConverter:
    """
    High-level orchestrator for TS dictionary generation.
    """

    def __init__(self, base_dir=None, output_dir="dictionaries_dev"):
        # Resolve paths relative to this script
        script_dir = Path(__file__).parent

        if base_dir is None:
            base_dir = script_dir / "wordnet_raw"
        else:
            base_dir = script_dir / base_dir

        self.base_dir = base_dir.resolve()
        self.output_dir = (script_dir / output_dir).resolve()

        self.entry_builder = TSEntryBuilder()
        self.json_writer = JSONGzipWriter(self.output_dir)

    def run(self):
        """
        Execute the full conversion pipeline.
        """
        print("Loading WordNet...")
        print(f">>> Using WordNet directory: {self.base_dir}")

        index, synsets = load_wordnet(self.base_dir)
        print(f"Loaded {len(synsets)} synsets.")

        ts_entries = []

        print("Building TS entries...")
        for (pos, offset), synset in synsets.items():
            entry = self.entry_builder.build(synset)
            ts_entries.append(entry.to_dict())

        print(f"Built {len(ts_entries)} TS entries.")

        print(f"Writing chunked JSON GZIP developer dictionary to {self.output_dir}...")
        manifest = self.json_writer.write(ts_entries)

        # Write manifest.json
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"[batch_converter] Wrote manifest.json to {manifest_path}")
        print("[batch_converter] Developer dictionary chunks created successfully.")


# Convenience function
def run_batch_conversion(base_dir="wordnet_raw", output_dir="dictionaries_dev"):
    BatchConverter(base_dir, output_dir).run()


if __name__ == "__main__":
    run_batch_conversion()
