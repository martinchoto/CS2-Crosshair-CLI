import typer
from rich.console import Console
from .models import Crosshair
from .utils import validate_crosshair_code, validate_name, name_exists

from .database import db 

app = typer.Typer()
console = Console()


@app.command()
def add(name: str, code: str):
    
    valid_code = validate_crosshair_code(code)
    
    # Check if the code is the correct for our crosshair
    if not valid_code:
        console.print("[bold red]Invalid Code![/bold red]")
        console.print("[yellow]Must follow format: [bold]CSGO-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX[/bold][/yellow]")
        raise typer.Exit()

    #Checks if the name is correct
    if not validate_name(name):
        console.print("[bold red]Invalid name[/bold red]")
        console.print("[yellow]Lenght of the name must be lower than 16 letters and higher than 1[/yellow]")
        raise typer.Exit()

    
    if name_exists(db, name):
        console.print(f"[bold red]Error:[/bold red] A crosshair named '[yellow]{name}[/yellow]' already exists!")
        console.print("[dim]Use a different name or delete the old one first.[/dim]")
        raise typer.Exit()
        
    #Should check the db, we don't want to overflow it with crosshairs
    if len(db) >= 25:
        console.print("[bold red]File Full![/bold red] You can only store 25 crosshairs.")
        raise typer.Exit()

    new_crosshair = Crosshair(name=name, code=valid_code)
    
    doc_id = db.insert(new_crosshair.to_dict())
    
    console.print(f"[green]✔ Saved '[bold]{new_crosshair.name}[/bold]' (ID: {doc_id})[/green]")
    
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
    
