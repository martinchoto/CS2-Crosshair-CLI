import typer
from pathlib import Path
from datetime import datetime
from tinydb import TinyDB, Query
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

APP_DIR = Path(__file__).parent.resolve()
DB_PATH = APP_DIR / "crosshairs.json"
db = TinyDB(DB_PATH)

@app.command()
def add(name: str, code: str):
    
    
    entry = {
        "name": name, 
        "code": code, 
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    doc_id = db.insert(entry)
    console.print(f"[green]✔ Saved '[bold]{name}[/bold]' (ID: {doc_id}) to {DB_PATH}[/green]")
    
@app.command()
def list():
    print("Listing...")

@app.command()
def edit():
    
    print("asdasd")
@app.command()
def delete():
    print("deleting..")

if __name__ == "__main__":
    app()
    
