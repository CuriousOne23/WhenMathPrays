"""
File path management for interactive editor.

Handles M1/M2 path resolution, perspective-based file naming,
and modified file tracking.
"""

from pathlib import Path
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class FileLoadResult:
    """Result of file path validation and resolution."""
    m1_path: Optional[Path]
    m2_path: Optional[Path]
    error_message: Optional[str]
    initial_perspective: str  # "M1" or "M2"
    
    @property
    def is_success(self) -> bool:
        """Check if file loading was successful."""
        return self.error_message is None
    
    @property
    def has_dual_perspective(self) -> bool:
        """Check if both M1 and M2 files are loaded."""
        return self.m1_path is not None and self.m2_path is not None and self.m1_path != self.m2_path


class FileManager:
    """
    Manages file paths for interactive editor.
    
    Responsibilities:
    - Validate input files
    - Resolve M1/M2 file pairs
    - Generate save paths with perspective awareness
    - Handle modified file naming conventions
    """
    
    def __init__(self, input_path: str):
        """
        Initialize file manager.
        
        Args:
            input_path: User-provided file path
        """
        self.input_path = Path(input_path)
        self._load_result: Optional[FileLoadResult] = None
    
    def validate_and_resolve(self) -> FileLoadResult:
        """
        Validate input file and resolve M1/M2 paths.
        
        Returns:
            FileLoadResult with resolved paths or error message
        
        Logic:
        - User loads M1 → looks for M2, loads M1 into both slots if not found
        - User loads M2 → looks for M1, loads M2 into both slots if not found
        - Invalid file → returns error
        - No M1/M2 suffix → treats as M1-only file
        """
        input_file = self.input_path
        
        # Check if file exists
        if not input_file.exists():
            return FileLoadResult(
                m1_path=None,
                m2_path=None,
                error_message=f"File not found: {input_file}",
                initial_perspective="M1"
            )
        
        # Check if file is CSV
        if input_file.suffix.lower() != '.csv':
            return FileLoadResult(
                m1_path=None,
                m2_path=None,
                error_message=f"Invalid file type: {input_file.suffix}. Must be a CSV file (.csv)",
                initial_perspective="M1"
            )
        
        # Determine if input is M1 or M2
        is_m1 = "_M1" in input_file.stem
        is_m2 = "_M2" in input_file.stem
        
        if not is_m1 and not is_m2:
            # File doesn't have M1 or M2 suffix - treat as M1 only
            self._load_result = FileLoadResult(
                m1_path=input_file,
                m2_path=None,
                error_message=None,
                initial_perspective="M1"
            )
            return self._load_result
        
        if is_m1:
            # User loaded M1 - look for M2
            m1_path = input_file
            m2_path_str = str(input_file).replace("_M1", "_M2", 1)
            m2_path = Path(m2_path_str)
            
            if m2_path.exists():
                # Both M1 and M2 exist - true dual perspective
                self._load_result = FileLoadResult(
                    m1_path=m1_path,
                    m2_path=m2_path,
                    error_message=None,
                    initial_perspective="M1"
                )
            else:
                # M1 exists but no M2 - load M1 into both slots
                print(f"[INFO] No M2 file found. Loading M1 file into both perspectives: {m1_path}")
                self._load_result = FileLoadResult(
                    m1_path=m1_path,
                    m2_path=m1_path,
                    error_message=None,
                    initial_perspective="M1"
                )
            return self._load_result
        
        else:  # is_m2
            # User loaded M2 - look for M1
            m2_path = input_file
            m1_path_str = str(input_file).replace("_M2", "_M1", 1)
            m1_path = Path(m1_path_str)
            
            if m1_path.exists():
                # Both M1 and M2 exist - true dual perspective
                self._load_result = FileLoadResult(
                    m1_path=m1_path,
                    m2_path=m2_path,
                    error_message=None,
                    initial_perspective="M1"  # Default to M1
                )
            else:
                # M2 exists but no M1 - load M2 into both slots, select M2
                print(f"[INFO] No M1 file found. Loading M2 file into both perspectives: {m2_path}")
                self._load_result = FileLoadResult(
                    m1_path=m2_path,
                    m2_path=m2_path,
                    error_message=None,
                    initial_perspective="M2"  # User intended M2
                )
            return self._load_result
    
    def get_save_path(self, perspective: str, save_to_data_dir: bool = True) -> Path:
        """
        Get save path for modified file based on current perspective.
        
        Args:
            perspective: "M1" or "M2"
            save_to_data_dir: If True, save to data/ directory
        
        Returns:
            Path for modified CSV file
        """
        if self._load_result is None:
            raise ValueError("Must call validate_and_resolve() first")
        
        # Get original file path
        original = self.input_path
        
        # Remove _modified suffix if present
        if original.stem.endswith('_modified'):
            base_name = original.stem[:-9]  # Remove '_modified'
        else:
            base_name = original.stem
        
        # Adjust base name for perspective
        if perspective == "M2":
            # Replace M1 with M2 in the base name
            base_name = base_name.replace("_M1", "_M2")
        elif perspective == "M1" and "_M2" in base_name:
            # Replace M2 with M1 (if user switched perspective)
            base_name = base_name.replace("_M2", "_M1")
        
        # Determine output directory
        if save_to_data_dir:
            if original.parent.name == 'data':
                output_dir = original.parent
            else:
                # Try to find data/ directory relative to original
                output_dir = original.parent.parent / 'data'
                if not output_dir.exists():
                    output_dir = original.parent  # Fallback to same directory
        else:
            output_dir = original.parent
        
        # Generate modified path
        return output_dir / f"{base_name}_modified.csv"
    
    def get_png_path(self, perspective: str, save_to_data_dir: bool = True) -> Path:
        """
        Get PNG export path for current perspective.
        
        Args:
            perspective: "M1" or "M2"
            save_to_data_dir: If True, save to data/ directory
        
        Returns:
            Path for PNG export
        """
        csv_path = self.get_save_path(perspective, save_to_data_dir)
        return csv_path.with_suffix('.png')
    
    def is_original_file(self) -> bool:
        """
        Check if current file is the original (not modified).
        
        Returns:
            True if file is in data/ and doesn't end with _modified.csv
        """
        return (
            self.input_path.parent.name == 'data' and
            not self.input_path.stem.endswith('_modified')
        )
    
    def get_m1_path(self) -> Optional[Path]:
        """Get resolved M1 file path."""
        if self._load_result is None:
            raise ValueError("Must call validate_and_resolve() first")
        return self._load_result.m1_path
    
    def get_m2_path(self) -> Optional[Path]:
        """Get resolved M2 file path."""
        if self._load_result is None:
            raise ValueError("Must call validate_and_resolve() first")
        return self._load_result.m2_path
    
    def get_initial_perspective(self) -> str:
        """Get initial perspective to display."""
        if self._load_result is None:
            raise ValueError("Must call validate_and_resolve() first")
        return self._load_result.initial_perspective
    
    def has_dual_perspective(self) -> bool:
        """Check if both M1 and M2 are loaded (different files)."""
        if self._load_result is None:
            raise ValueError("Must call validate_and_resolve() first")
        return self._load_result.has_dual_perspective
