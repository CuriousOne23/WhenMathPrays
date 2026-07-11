import os
import json
import gzip

class JSONGzipWriter:
    """
    Writes the full TS developer dictionary (including gloss, pointers,
    and all TS semantic products) into a gzipped JSON file.

    Output:
        dictionaries_dev/meaning_dictionary_dev.json.gz

    This file is intended for engineers, not TS runtime. It contains:
        - lemma
        - alternates
        - gloss
        - WordNet pointers
        - raw WordNet metadata
        - primitives
        - invariants
        - cue envelopes
        - routing signatures
        - identity anchors

    The runtime dictionary is produced separately by:
        ts_meaning_dct_path_a.py
    """

    def __init__(self, output_path):
        self.output_path = output_path

    def write(self, ts_entries):
        """
        Writes the full TS entries to a gzipped JSON file.

        Parameters:
            ts_entries (list or dict):
                The full TS dictionary entries produced by ts_entry_builder.py.
        """

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # Write gzipped JSON
        with gzip.open(self.output_path, "wt", encoding="utf-8") as f:
            json.dump(
                ts_entries,
                f,
                ensure_ascii=False,
                separators=(",", ":")  # compact JSON
            )

        print(f"[json_gzip_writer] Developer dictionary written to: {self.output_path}")
