"""Characterization package for milestone-1 integration."""

from dataclasses import dataclass


@dataclass
class CharacterizationError(Exception):
    """Raised when characterization processing fails after CLI validation."""

    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


