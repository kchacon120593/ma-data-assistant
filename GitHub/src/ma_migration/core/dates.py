from __future__ import annotations
from dateutil.parser import parse

def format_date(x):
    try:
        return parse(str(x), dayfirst=False).strftime('%Y-%m-%d')
    except (ValueError, OverflowError, TypeError):
        return str(x)
