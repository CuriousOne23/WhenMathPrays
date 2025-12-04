#!/usr/bin/env python3
"""
Time Unit Converter for WhenMathPrays Scenarios
Converts CSV scenario files between different time units (days/weeks/months/years).

Usage:
    python tools/convert_time_units.py input.csv output.csv weeks
"""

import sys
import csv
from pathlib import Path


# Conversion factors (all relative to days)
CONVERSION_FACTORS = {
    'days': 1.0,
    'weeks': 7.0,
    'months': 30.0,  # Approximate
    'years': 365.0
}


def convert_time_units(input_path: str, output_path: str, target_unit: str):
    """
    Convert time units in a scenario CSV file.
    
    Args:
        input_path: Path to source CSV
        output_path: Path to save converted CSV
        target_unit: Target time unit ('days', 'weeks', 'months', 'years')
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    # Validate target unit
    if target_unit.lower() not in CONVERSION_FACTORS:
        raise ValueError(f"Invalid target unit '{target_unit}'. Must be one of: {list(CONVERSION_FACTORS.keys())}")
    
    target_unit = target_unit.lower()
    
    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) == 0:
        raise ValueError("Input file is empty")
    
    # Parse metadata and find current time_unit
    metadata_lines = []
    data_start_idx = 0
    current_unit = 'days'  # Default
    name = None
    
    for i, line in enumerate(lines[:3]):  # Check first 3 lines for metadata
        line_stripped = line.strip()
        if line_stripped.startswith('name,'):
            name = line_stripped.split(',', 1)[1].strip()
            metadata_lines.append(('name', name))
            data_start_idx = i + 1
        elif line_stripped.startswith('time_unit,'):
            current_unit = line_stripped.split(',', 1)[1].strip().lower()
            if current_unit not in CONVERSION_FACTORS:
                print(f"Warning: Unknown current time_unit '{current_unit}', assuming 'days'")
                current_unit = 'days'
            metadata_lines.append(('time_unit', current_unit))
            data_start_idx = i + 1
        else:
            # Not metadata, data starts here
            break
    
    # Calculate conversion factor
    # Convert: current_unit -> days -> target_unit
    to_days = CONVERSION_FACTORS[current_unit]
    from_days = 1.0 / CONVERSION_FACTORS[target_unit]
    conversion_factor = to_days * from_days
    
    print(f"Converting from {current_unit} to {target_unit}")
    print(f"Conversion factor: {conversion_factor:.6f}")
    
    # Read CSV data (skip metadata rows)
    csv_reader = csv.DictReader(lines[data_start_idx:])
    fieldnames = csv_reader.fieldnames
    
    if 'day' not in fieldnames:
        raise ValueError("CSV missing required 'day' column")
    
    # Convert time values
    converted_rows = []
    for row in csv_reader:
        try:
            # Convert time value
            old_time = float(row['day'])
            new_time = old_time * conversion_factor
            
            # Determine precision based on target unit
            if target_unit == 'days':
                row['day'] = str(int(round(new_time)))  # Whole days
            else:
                row['day'] = f"{new_time:.1f}"  # 1 decimal for weeks/months/years
            
            converted_rows.append(row)
        except ValueError as e:
            print(f"Warning: Could not convert time value '{row['day']}': {e}")
            converted_rows.append(row)  # Keep original
    
    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        # Write metadata
        if name:
            f.write(f"name,{name}\n")
        f.write(f"time_unit,{target_unit}\n")
        
        # Write data
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(converted_rows)
    
    print(f"\nConversion complete!")
    print(f"Input:  {input_path} ({current_unit})")
    print(f"Output: {output_path} ({target_unit})")
    print(f"Rows converted: {len(converted_rows)}")


def main():
    """Command-line interface."""
    if len(sys.argv) != 4:
        print("Usage: python convert_time_units.py <input.csv> <output.csv> <target_unit>")
        print("\nTarget units: days, weeks, months, years")
        print("\nExample:")
        print("  python tools/convert_time_units.py data/scenario.csv data/scenario_weeks.csv weeks")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    target_unit = sys.argv[3]
    
    try:
        convert_time_units(input_path, output_path, target_unit)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
