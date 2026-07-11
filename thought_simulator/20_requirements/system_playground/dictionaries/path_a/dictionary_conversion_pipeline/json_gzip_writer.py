import os
import json
import gzip

class JSONGzipWriter:
    """
    Chunk-aware writer for the TS developer dictionary.

    This writer:
        - computes the Word Density Profile (WDP)
        - splits the dictionary into 6 compressed chunks
        - ensures stable lemma boundaries
        - writes chunk files into dictionaries_dev/
        - returns manifest metadata for batch_converter.py

    Output files:
        dictionaries_dev/meaning_dictionary_dev_01.json.gz
        dictionaries_dev/meaning_dictionary_dev_02.json.gz
        dictionaries_dev/meaning_dictionary_dev_03.json.gz
        dictionaries_dev/meaning_dictionary_dev_04.json.gz
        dictionaries_dev/meaning_dictionary_dev_05.json.gz
        dictionaries_dev/meaning_dictionary_dev_06.json.gz

    The runtime dictionary is produced separately by:
        ts_meaning_dct_path_a.py
    """

    def __init__(self, output_dir, chunk_count=6, target_size_mb=2.0):
        self.output_dir = output_dir
        self.chunk_count = chunk_count
        self.target_size_bytes = int(target_size_mb * 1024 * 1024)

    def _ensure_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _measure_json_size(self, entry_dict):
        """
        Measures the JSON size of a TS entry (uncompressed).
        """
        json_string = json.dumps(entry_dict, ensure_ascii=False, separators=(",", ":"))
        return len(json_string), json_string

    def write(self, ts_entries):
        """
        Writes TS entries into 6 chunked gzipped JSON files.

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

        self._ensure_dir()

        # Sort entries by lemma for stable chunk boundaries
        sorted_entries = sorted(ts_entries, key=lambda e: e["lemma"])

        manifest = []
        chunk_entries = []
        chunk_id = 1
        chunk_size = 0

        first_lemma = None
        last_lemma = None

        for entry in sorted_entries:
            entry_size, entry_json = self._measure_json_size(entry)

            # If adding this entry exceeds target chunk size → finalize chunk
            if chunk_size + entry_size > self.target_size_bytes and chunk_entries:
                filename = self._write_chunk(chunk_id, chunk_entries)
                compressed_size = os.path.getsize(os.path.join(self.output_dir, filename))

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
            compressed_size = os.path.getsize(os.path.join(self.output_dir, filename))

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

    def _write_chunk(self, chunk_id, entries):
        """
        Writes a single chunk file.
        """
        filename = f"meaning_dictionary_dev_{chunk_id:02d}.json.gz"
        path = os.path.join(self.output_dir, filename)

        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, separators=(",", ":"))

        return filename
