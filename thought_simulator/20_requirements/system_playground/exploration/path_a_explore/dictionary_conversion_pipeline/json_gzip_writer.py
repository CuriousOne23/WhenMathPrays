import os
import json
import gzip
from pathlib import Path

from config import (
    CHUNK_COUNT,
    DEV_OUTPUT_DIR,
)
from utils import (
    measure_json_size,
    write_gzip_json,
    ensure_dir,
)


class JSONGzipWriter:
    """
    Chunk-aware writer for the TS developer dictionary using
    Word Density Profile (WDP) bucket splitting.

    Responsibilities:
        • compute Word Density Profile (WDP)
        • split dictionary into CHUNK_COUNT equal-density buckets
        • ensure stable lemma boundaries
        • write chunk files into dictionaries_dev/
        • return manifest metadata to batch_converter.py

    Output files:
        dictionaries_dev/meaning_dictionary_dev_01.json.gz
        ...
        dictionaries_dev/meaning_dictionary_dev_06.json.gz
    """

    def __init__(self, output_dir=DEV_OUTPUT_DIR, chunk_count=CHUNK_COUNT):
        self.output_dir = Path(output_dir)
        self.chunk_count = chunk_count

    # ------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------

    def _write_chunk(self, chunk_id, entries):
        filename = f"meaning_dictionary_dev_{chunk_id:02d}.json.gz"
        path = self.output_dir / filename
        write_gzip_json(path, entries)
        return filename

    # ------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------

    def write(self, ts_entries):
        """
        Writes TS entries into CHUNK_COUNT WDP-balanced gzipped JSON files.

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
                    - entry_count
                    - uncompressed_size
                    - compressed_size
        """

        ensure_dir(self.output_dir)
        # Clean existing developer dictionary files
        for f in self.output_dir.glob("meaning_dictionary_dev_*.json.gz"):
            try:
                f.unlink()
            except Exception as e:
                print(f"[json_gzip_writer] Warning: could not delete {f}: {e}")

        # Remove old manifest if present
        manifest_path = self.output_dir / "manifest.json"
        if manifest_path.exists():
            try:
                manifest_path.unlink()
            except Exception as e:
                print(f"[json_gzip_writer] Warning: could not delete manifest.json: {e}")

        # Sort entries by lemma for stable boundaries
        sorted_entries = sorted(ts_entries, key=lambda e: e["lemma"])

        # Compute WDP: uncompressed size for each entry
        sizes = []
        for entry in sorted_entries:
            entry_size, _json_string = measure_json_size(entry)
            sizes.append(entry_size)

        total_size = sum(sizes)
        target_bucket_size = total_size / self.chunk_count

        manifest = []
        chunk_entries = []
        chunk_id = 1
        bucket_accum = 0

        first_lemma = None
        last_lemma = None

        for entry, entry_size in zip(sorted_entries, sizes):

            # Start new chunk if bucket target reached
            if bucket_accum >= target_bucket_size and chunk_entries:
                filename = self._write_chunk(chunk_id, chunk_entries)
                compressed_size = os.path.getsize(self.output_dir / filename)

                manifest.append({
                    "chunk_id": chunk_id,
                    "filename": filename,
                    "first_lemma": first_lemma,
                    "last_lemma": last_lemma,
                    "entry_count": len(chunk_entries),
                    "uncompressed_size": bucket_accum,
                    "compressed_size": compressed_size
                })

                # Reset for next bucket
                chunk_id += 1
                chunk_entries = []
                bucket_accum = 0
                first_lemma = None
                last_lemma = None

            # Add entry to current bucket
            if first_lemma is None:
                first_lemma = entry["lemma"]
            last_lemma = entry["lemma"]

            chunk_entries.append(entry)
            bucket_accum += entry_size

        # Write final chunk
        if chunk_entries:
            filename = self._write_chunk(chunk_id, chunk_entries)
            compressed_size = os.path.getsize(self.output_dir / filename)

            manifest.append({
                "chunk_id": chunk_id,
                "filename": filename,
                "first_lemma": first_lemma,
                "last_lemma": last_lemma,
                "entry_count": len(chunk_entries),
                "uncompressed_size": bucket_accum,
                "compressed_size": compressed_size
            })

        print(f"[json_gzip_writer] Wrote {len(manifest)} developer chunks to {self.output_dir}")

        # Add total number of entries to manifest
        return {
            "total_entries": len(sorted_entries),
            "chunks": manifest
        }
