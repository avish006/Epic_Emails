# date_utils.py - Enhanced version
import dateutil.parser
from email.utils import parsedate_to_datetime
from datetime import datetime

def parse_email_date(date_header):
    """
    Robustly parse an email date string from the 'Date' header.
    Returns a datetime object or None if parsing fails.
    """
    if not date_header:
        return None
    
    try:
        # Method 1: Use the standard library's email utility (recommended)
        dt_object = parsedate_to_datetime(date_header)
        return dt_object
    except (ValueError, TypeError) as e:
        print(f"Standard parser failed for '{date_header}': {e}. Trying fallback...")
        try:
            # Method 2: Fallback to dateutil.parser for non-standard formats
            dt_object = dateutil.parser.parse(date_header)
            return dt_object
        except Exception as e:
            print(f"All parsers failed for date string: '{date_header}'. Error: {e}")
            return None

def format_date_for_display(dt_object):
    """
    Format a datetime object into a user-friendly string.
    Example: 'Tue, Aug 28, 2012 at 1:19 PM'
    """
    if dt_object:
        return dt_object.strftime('%a, %b %d, %Y at %I:%M %p')
    return "Date not available"