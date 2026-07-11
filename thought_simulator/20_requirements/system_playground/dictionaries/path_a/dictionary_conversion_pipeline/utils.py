"""
utils.py
--------

Shared utility functions for the TS Path A dictionary conversion pipeline.

This module provides:
    • JSON size measurement
    • GZIP compression helpers
    • manifest writing
    • directory helpers
    • safe JSON loading/writing

All functions are deterministic and side‑effect free.
"""

import os
import json
import gzip
from pathlib import Path


# ============================================================
# JSON / GZIP Helpers
# ============================================================

def measure_json_size(entry_dict):
    """
    Returns:
        (uncompressed_size_bytes, json_string)

    Used by json_gzip_writer.py to compute the Word Density Profile (WDP).
    """
    json_string = json.dumps(entry_dict, ensure_ascii=False, separators=(",", ":"))
    return len(json_string), json_string


def write_gzip_json(path, data):
    """
    Writes JSON data to a gzipped file.

    Parameters:
        path (Path or str): output file path
        data (object): JSON‑serializable Python object
    """
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def load_gzip_json(path):
    """
    Loads JSON data from a gzipped file.

    Returns:
        Python object (list or dict)
    """
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Manifest Helpers
# ============================================================

def write_manifest(manifest, output_dir, filename="manifest.json"):
    """
    Writes manifest.json into the specified directory.

    Parameters:
        manifest (list of dict): chunk metadata
        output_dir (Path or str): directory to write into
        filename (str): manifest filename (default: manifest.json)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    path = output_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return path


# ============================================================
# Directory Helpers
# ============================================================

def ensure_dir(path):
    """
    Ensures a directory exists.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def list_dev_chunks(dev_dir):
    """
    Returns a sorted list of developer chunk filenames.

    Example:
        [
            "meaning_dictionary_dev_01.json.gz",
            "meaning_dictionary_dev_02.json.gz",
            ...
        ]
    """
    dev_dir = Path(dev_dir)
    return sorted(
        [p.name for p in dev_dir.glob("meaning_dictionary_dev_*.json.gz")]
    )


# ============================================================
# Runtime Stripping Helpers
# ============================================================

def strip_runtime_fields(entry, keep_fields):
    """
    Removes developer-only fields from a TS entry.

    Parameters:
        entry (dict): full developer TS entry
        keep_fields (set): fields to preserve for runtime

    Returns:
        dict: stripped runtime entry
    """
    return {k: v for k, v in entry.items() if k in keep_fields}
