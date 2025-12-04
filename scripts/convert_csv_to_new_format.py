#!/usr/bin/env python3
"""
Convert old CSV format to new simplified format.
Removes metadata headers (name, time_unit) and renames 'day' column to 'step'.
"""

import csv
from pathlib import Path

def convert_csv(input_path: Path, output_path: Path = None):
    """Convert a single CSV file to new format."""
    if output_path is None:
        output_path = input_path
    
    # Read the file
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    # Skip metadata lines (lines that contain ',' but start with 'name' or 'time_unit')
    data_lines = []
    found_header = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Skip metadata lines
        if stripped.startswith('name,') or stripped.startswith('time_unit,'):
            continue
        
        # Check if this is the header line
        if not found_header and (stripped.startswith('day,') or stripped.startswith('step,')):
            # Replace 'day' with 'step' if needed
            header = stripped.replace('day,', 'step,', 1)
            data_lines.append(header + '\n')
            found_header = True
        elif found_header:
            # Data line
            data_lines.append(line)
    
    # Write back
    with open(output_path, 'w', newline='') as f:
        f.writelines(data_lines)
    
    return len(data_lines) - 1  # Subtract header line

if __name__ == "__main__":
    # Convert all template files
    templates_dir = Path(__file__).parent.parent / "data" / "templates"
    
    if not templates_dir.exists():
        print(f"Templates directory not found: {templates_dir}")
        exit(1)
    
    csv_files = list(templates_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {templates_dir}")
        exit(1)
    
    print(f"Converting {len(csv_files)} CSV files...\n")
    
    for csv_file in csv_files:
        try:
            num_rows = convert_csv(csv_file)
            print(f"✓ {csv_file.name}: {num_rows} data rows")
        except Exception as e:
            print(f"✗ {csv_file.name}: ERROR - {e}")
    
    print(f"\nConversion complete!")
