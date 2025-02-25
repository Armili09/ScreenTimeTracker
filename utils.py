from datetime import datetime, timedelta

def format_time(seconds):
    """Format seconds into hours and minutes"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"

def get_date_range(days):
    """Get list of dates for the last n days"""
    dates = []
    today = datetime.now()
    for i in range(days):
        date = today - timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d"))
    return dates

def calculate_percentage(value, total):
    """Calculate percentage with safe division"""
    return (value / total * 100) if total > 0 else 0
