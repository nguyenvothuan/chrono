from datetime import datetime


def date_field_from_date(date: str):
    """Generate a DateField from the format: YYYY-MM-DD"""
    date_object = datetime.strptime(date, '%Y-%m-%d')    
    return date_object.date()
