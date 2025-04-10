"""
Security utilities for the application.
"""
import re
import string
import random
from django.utils.text import slugify


def generate_secure_password(length=12):
    """
    Generate a secure random password with letters, digits, and special characters.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def sanitize_input(input_text):
    """
    Sanitize user input to prevent XSS and injection attacks.
    """
    if not input_text:
        return ""
    
    # Convert to string if not already
    if not isinstance(input_text, str):
        input_text = str(input_text)
    
    # Remove potentially dangerous HTML tags
    sanitized = re.sub(r'<[^>]*>', '', input_text)
    
    return sanitized


def generate_slug(text, max_length=50):
    """
    Generate a URL-safe slug from a text string.
    """
    return slugify(text)[:max_length]


def secure_content(content_dict):
    """
    Recursively sanitize all string values in a dictionary or list.
    """
    if isinstance(content_dict, dict):
        return {k: secure_content(v) for k, v in content_dict.items()}
    elif isinstance(content_dict, list):
        return [secure_content(i) for i in content_dict]
    elif isinstance(content_dict, str):
        return sanitize_input(content_dict)
    else:
        return content_dict
