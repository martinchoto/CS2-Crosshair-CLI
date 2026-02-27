import re
from tinydb import where

# The standard CS2/CSGO share code pattern
CS2_REGEX = r"^CSGO(-[a-zA-Z0-9]{5}){5}$"

#Crosshair validation

def validate_crosshair_code(code: str) -> str:

    cleaned_code = code.strip()
    
    if re.match(CS2_REGEX, cleaned_code):
        return cleaned_code
    
    return None
# Crosshair validation for name

def validate_name(name: str) -> bool:
    
    return 1 < len(name) < 16

# Checks the db if name exists already

def name_exists(db, name: str) -> bool:

    result = db.search(where('name').map(lambda x: x.lower()) == name.lower())
    return len(result) > 0

# finds the name of the crosshair
def find_by_name(db, name: str):
    return db.get(where('name').map(lambda x: x.lower()) == name.lower())
# finds it by the id
def find_by_id(db, doc_id: int):
    return db.get(doc_id=doc_id)