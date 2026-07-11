import os
import json
import gzip
from pathlib import Path

from config import (
    CHUNK_COUNT,
    CHUNK_TARGET_SIZE_MB,
    DEV_OUTPUT_DIR,
)
from utils import (
    measure_json_size,
    write_gzip_json,
    ensure_dir,
)


class JSONGzipWriter:
    """
    Chunk-aware writer for the TS developer dictionary.

    Responsibilities:
        • compute Word Density Profile (WDP)
        • split dictionary into CHUNK_COUNT chunks
        • ensure stable lemma boundaries
        • write chunk files into dictionaries_dev/
        • return manifest metadata to batch_converter.py

    Output files:
        dictionaries_dev/meaning_dictionary_dev_01.json.gz
        ...
        dictionaries_dev/meaning_dictionary_dev_06.json.gz

    Runtime dictionary is produced separately by:
        ts_meaning_dct_path_a.py
    """

    def __init__(self, output_dir=DEV_OUTPUT_DIR,
                 chunk_count=CHUNK_COUNT,
                 target_size_mb=CHUNK_TARGET_SIZE_MB):

        self.output_dir = Path(output_dir)
        self.chunk_count = chunk_count
        self.target_size_bytes = int(target_size_mb * 1024 * 1024)

    # ------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------

    def _write_chunk(self, chunk_id, entries):
        """
        Writes a single chunk file.
        """
        filename = f"meaning_dictionary_dev_{chunk_id:02d}.json.gz"
        path = self.output_dir / filename

        write_gzip_json(path, entries)
        return filename

    # ------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------

    def write(self, ts_entries):
        """
        Writes TS entries into chunked gzipped JSON files.

        Parameters:
            ts_entries (list):
                Full TS developer entries produced by ts_entry_builder.py.

        Returns:
            manifest (list of dict):
                Metadata for each chunk:
                    - chunk_id
                    - filename
                    - first_lemma
                    - last_lemma
                    - uncompressed_size
                    - compressed_size
        """

        ensure_dir(self.output_dir)

        # Sort entries by lemma for stable chunk boundaries
        sorted_entries = sorted(ts_entries, key=lambda e: e["lemma"])

        manifest = []
        chunk_entries = []
        chunk_id = 1
        chunk_size = 0

        first_lemma = None
        last_lemma = None

        for entry in sorted_entries:
            entry_size, _json_string = measure_json_size(entry)

            # If adding this entry exceeds target chunk size → finalize chunk
            if chunk_size + entry_size > self.target_size_bytes and chunk_entries:
                filename = self._write_chunk(chunk_id, chunk_entries)
                compressed_size = os.path.getsize(self.output_dir / filename)

                manifest.append({
                    "chunk_id": chunk_id,
                    "filename": filename,
                    "first_lemma": first_lemma,
                    "last_lemma": last_lemma,
                    "uncompressed_size": chunk_size,
                    "compressed_size": compressed_size
                })

                # Reset for next chunk
                chunk_id += 1
                chunk_entries = []
                chunk_size = 0
                first_lemma = None
                last_lemma = None

            # Add entry to current chunk
            if first_lemma is None:
                first_lemma = entry["lemma"]
            last_lemma = entry["lemma"]

            chunk_entries.append(entry)
            chunk_size += entry_size

        # Write final chunk
        if chunk_entries:
            filename = self._write_chunk(chunk_id, chunk_entries)
            compressed_size = os.path.getsize(self.output_dir / filename)

            manifest.append({
                "chunk_id": chunk_id,
                "filename": filename,
                "first_lemma": first_lemma,
                "last_lemma": last_lemma,
                "uncompressed_size": chunk_size,
                "compressed_size": compressed_size
            })

        print(f"[json_gzip_writer] Wrote {len(manifest)} developer chunks to {self.output_dir}")
        return manifest
