"""
batch_converter.py
------------------

Runs the full TS Path A dictionary conversion pipeline:

    WordNet → Synset → TS Entry → YAML Dictionary

This module orchestrates:
    • WordNetLoader
    • TSEntryBuilder
    • YAMLWriter

Produces:
    meaning_dictionary.yaml
"""

from pathlib import Path
from wordnet_loader import load_wordnet
from ts_entry_builder import TSEntryBuilder
from yaml_writer import write_yaml


class BatchConverter:
    """
    High-level orchestrator for TS dictionary generation.
    """

    def __init__(self, base_dir=None, output_file="meaning_dictionary.yaml"):
        # Always resolve paths relative to THIS file, not the working directory.
        script_dir = Path(__file__).parent

        if base_dir is None:
            # WordNet directory lives next to this script
            base_dir = script_dir / "wordnet_raw"
        else:
            # If user passes a relative path, resolve it relative to this script
            base_dir = script_dir / base_dir

        self.base_dir = base_dir.resolve()
        self.output_file = (script_dir / output_file).resolve()
        self.entry_builder = TSEntryBuilder()

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
            ts_entries.append(entry)

        print(f"Built {len(ts_entries)} TS entries.")

        print(f"Writing YAML dictionary to {self.output_file}...")
        write_yaml(ts_entries, self.output_file)

        print("File meaning_dictionary.yaml has been created.")
        print("Done.")


# Convenience function
def run_batch_conversion(base_dir="wordnet_raw", output_file="meaning_dictionary.yaml"):
    BatchConverter(base_dir, output_file).run()


if __name__ == "__main__":
    run_batch_conversion()
