import typer 
from pathlib import Path
from datetime import datetime
from rich.console import Console

from .database import db 

app = typer.Typer()
console = Console()


@app.command()
def add(name: str, code: str):
    
    if len(db) >= 25:
        console.print("[red]❌ Vault Full![/red] You can only store 25 crosshairs. Delete one first.")
        raise typer.Exit()
    
    entry = {
        "name": name, 
        "code": code, 
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    doc_id = db.insert(entry)
    
    console.print(f"[green]✔ Saved '[bold]{name}[/bold]' (ID: {doc_id}) [/green]")
    
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
    
