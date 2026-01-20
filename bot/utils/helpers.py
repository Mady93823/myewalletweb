import re

def parse_time_string(time_str):
    """
    Parses a time string like '2h', '15m', '1d' into seconds.
    Returns None if invalid.
    """
    if not time_str:
        return None
        
    match = re.match(r"^(\d+)([smhd])$", time_str.lower())
    if not match:
        return None
        
    value, unit = match.groups()
    value = int(value)
    
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    elif unit == 'd':
        return value * 86400
    
    return None
