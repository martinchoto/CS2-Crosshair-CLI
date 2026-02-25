# src/cs2_crosshair/database.py
import os
from pathlib import Path
from tinydb import TinyDB

def db_init():
    
    #This is for Windows
    if os.name == 'nt':
        
        base_dir = Path(os.environ.get('APPDATA')) / "CS2Crosshair"
    #This is for Linux
    else: 
        base_dir = Path.home() / ".config" / "CS2Crosshair"

    base_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = base_dir / "crosshairs.json"
    return TinyDB(db_path)

db = db_init()