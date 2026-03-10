from datetime import datetime

def get_current_date_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def is_same_day(date_str: str) -> bool:
    return date_str == get_current_date_str() 