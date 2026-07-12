"""
yaml_writer.py
--------------

Writes TS Path A dictionary entries to a YAML file.

Responsibilities:
    • Accept a list of TSEntry objects
    • Convert them into YAML-safe dictionaries
    • Write deterministic, stable YAML output
    • Ensure ordering and formatting are reviewer-friendly

This module performs no semantic work; it is purely structural.
"""

import yaml
from typing import List
from ts_entry_builder import TSEntry


class YAMLWriter:
    """
    Deterministic YAML writer for TS Path A dictionary entries.
    """

    def write(self, entries: List[TSEntry], filepath: str) -> None:
        """
        Write a list of TS entries to a YAML file.

        Parameters
        ----------
        entries : List[TSEntry]
            Fully constructed TS entries.
        filepath : str
            Output YAML file path.
        """
        data = [entry.to_dict() for entry in entries]

        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(
                data,
                f,
                sort_keys=False,      # preserve human-friendly ordering
                allow_unicode=True,   # support full Unicode
                default_flow_style=False,
            )


# Convenience function for pipeline modules
def write_yaml(entries: List[TSEntry], filepath: str) -> None:
    YAMLWriter().write(entries, filepath)
