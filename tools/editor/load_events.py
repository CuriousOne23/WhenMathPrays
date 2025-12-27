# Sample function to load events from CSV and create Event/Marker objects
import csv
from .event import Event
from .debug_config import get_logger

_logger = get_logger('load_events')

PRIMITIVE_NAMES = ['v', 'r', 'f', 'a', 'S']

def load_events_from_csv(filepath, start_id=0):
    """
    Loads scenario events from a CSV file and returns a list of Event objects.
    
    Args:
        filepath (str): Path to CSV file.
        start_id (int): Starting ID for event assignment (default 0).
    
    Returns:
        tuple: (List[Event], dict, int) - List of Event objects, metadata dict with 
               'gamma_self_0', 'time_unit', 'name', and next_event_id to use for new events.
    
    Note: Events are assigned sequential IDs starting from start_id in file order.
          The returned next_event_id is start_id + len(events).
    """
    events = []
    metadata = {'gamma_self_0': 0+0j, 'time_unit': 'days', 'name': ''}
    event_id = start_id
    
    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        # Find the actual header row
        lines = csvfile.readlines()
        header_idx = None
        for idx, line in enumerate(lines):
            if line.lower().startswith('step,') or line.lower().startswith('day,'):
                header_idx = idx
                break
        if header_idx is None:
            _logger.debug("No valid header found in CSV!")
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
                        _logger.debug(f"Parsed gamma_self_0 = {metadata['gamma_self_0']}")
                    except Exception as e:
                        _logger.debug(f"Failed to parse gamma_self_0: {e}")
                elif key == 'time_unit':
                    metadata['time_unit'] = value
                elif key == 'name':
                    metadata['name'] = value
        
        header = [h.strip() for h in lines[header_idx].strip().split(',')]
        _logger.debug(f"Using header: {header}")
        # Read data rows after header
        reader = csv.DictReader(lines[header_idx+1:], fieldnames=header)
        for row in reader:
            _logger.debug(f"load_events_from_csv: row = {row}")
            # Skip rows missing any primitive columns
            missing = [prim for prim in PRIMITIVE_NAMES if prim not in row or row[prim] in (None, '')]
            if missing:
                _logger.debug(f"Skipping row, missing columns: {missing}")
                continue
            try:
                time = float(row.get('step', row.get('day', 0)))
                primitives = {prim: float(row[prim]) for prim in PRIMITIVE_NAMES}
                notes = row.get('notes', '')
                marker = row.get('marker', '')
                locked = row.get('locked', '')
                event = Event(time, primitives, notes=notes, marker=marker, locked=locked, event_id=event_id)
                events.append(event)
                _logger.debug(f"Accepted event: id={event_id}, time={time}, primitives={primitives}")
                event_id += 1
            except Exception as e:
                _logger.debug(f"Skipping row due to error: {e}")
    
    next_event_id = event_id
    _logger.debug(f"Loaded {len(events)} events, next_event_id={next_event_id}")
    return events, metadata, next_event_id
