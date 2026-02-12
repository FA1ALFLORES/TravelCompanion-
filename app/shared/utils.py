import re
from datetime import datetime
from typing import Optional
import random
import string

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def generate_random_string(length: int = 8) -> str:
    
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    return dt.strftime(format)


def parse_datetime(date_str: str, format: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    try:
        return datetime.strptime(date_str, format)
    except ValueError:
        return None


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def validate_phone(phone: str) -> bool:
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    return cleaned.isdigit() and len(cleaned) >= 10


def normalize_email(email: str) -> str:
    return email.lower().strip()


def now() -> str:
    return datetime.now().isoformat()