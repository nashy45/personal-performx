"""Utility helpers for the application"""

def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return "Not set"
    return dt.strftime('%Y-%m-%d')
