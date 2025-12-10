# Sample function to load events from CSV and create Event/Marker objects
import csv
from .event import Event

PRIMITIVE_NAMES = ['v', 'r', 'f', 'a', 'S']

def load_events_from_csv(filepath):
    """
    Loads scenario events from a CSV file and returns a list of Event objects.
    Args:
        filepath (str): Path to CSV file.
    Returns:
        tuple: (List[Event], dict) - List of Event objects and metadata dict with 'gamma_self_0', 'time_unit', 'name'
    """
    events = []
    metadata = {'gamma_self_0': 0+0j, 'time_unit': 'days', 'name': ''}
    
    with open(filepath, 'r', newline='') as csvfile:
        # Find the actual header row
        lines = csvfile.readlines()
        header_idx = None
        for idx, line in enumerate(lines):
            if line.lower().startswith('step,') or line.lower().startswith('day,'):
                header_idx = idx
                break
        if header_idx is None:
            print("[DEBUG] No valid header found in CSV!")
            return events, metadata
        
        # Parse metadata rows before header
        for idx in range(header_idx):
            line = lines[idx].strip()
            if ',' in line:
                parts = line.split(',', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ''
                if key == 'gamma_self_0':
                    try:
                        metadata['gamma_self_0'] = complex(value.replace('+-', '-'))
                        print(f"[DEBUG] Parsed gamma_self_0 = {metadata['gamma_self_0']}")
                    except Exception as e:
                        print(f"[DEBUG] Failed to parse gamma_self_0: {e}")
                elif key == 'time_unit':
                    metadata['time_unit'] = value
                elif key == 'name':
                    metadata['name'] = value
        
        header = [h.strip() for h in lines[header_idx].strip().split(',')]
        print(f"[DEBUG] Using header: {header}")
        # Read data rows after header
        reader = csv.DictReader(lines[header_idx+1:], fieldnames=header)
        for row in reader:
            print(f"[DEBUG] load_events_from_csv: row = {row}")
            # Skip rows missing any primitive columns
            missing = [prim for prim in PRIMITIVE_NAMES if prim not in row or row[prim] in (None, '')]
            if missing:
                print(f"[DEBUG] Skipping row, missing columns: {missing}")
                continue
            try:
                time = float(row.get('step', row.get('day', 0)))
                primitives = {prim: float(row[prim]) for prim in PRIMITIVE_NAMES}
                notes = row.get('notes', '')
                marker = row.get('marker', '')
                locked = row.get('locked', '')
                event = Event(time, primitives, notes=notes, marker=marker, locked=locked)
                events.append(event)
                print(f"[DEBUG] Accepted event: time={time}, primitives={primitives}")
            except Exception as e:
                print(f"[DEBUG] Skipping row due to error: {e}")
    return events, metadata
