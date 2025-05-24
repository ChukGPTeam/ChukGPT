# utils.py
import re

def extract_num(text):
    match = re.search(r"\d+", text)
    return match.group() if match else None
