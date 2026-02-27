import re
from tinydb import where

# The standard CS2/CSGO share code pattern
CS2_REGEX = r"^CSGO(-[a-zA-Z0-9]{5}){5}$"

def validate_crosshair_code(code: str) -> str:

    cleaned_code = code.upper().strip()
    
    if re.match(CS2_REGEX, cleaned_code):
        return cleaned_code
    
    return None

def validate_name(name: str) -> bool:
    
    return 1 < len(name) < 16

def name_exists(db, name: str) -> bool:

    result = db.search(where('name').map(lambda x: x.lower()) == name.lower())
    return len(result) > 0