import typer
import readchar
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from typing import Optional


from .models import Crosshair
from .utils import validate_crosshair_code, validate_name, name_exists, find_by_name, find_by_id

from .database import db 

app = typer.Typer()
console = Console()


@app.command()
def add(name: str, code: str):
    
    valid_code = validate_crosshair_code(code)
    
    #Checks if the name is correct
    
    if not validate_name(name):
        console.print("[bold red]Invalid name[/bold red]")
        console.print("[yellow]Lenght of the name must be lower than 16 letters and higher than 1[/yellow]")
        raise typer.Exit()
    
    # Check if the code is the correct for our crosshair
    
    if not valid_code:
        console.print("[bold red]Invalid Code![/bold red]")
        console.print("[yellow]Must follow format: [bold]CSGO-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX[/bold][/yellow]")
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
    
    #Adds the crosshair to our small "db"
    
    doc_id = db.insert(new_crosshair.to_dict())
    
    console.print(f"[green]✔ Saved '[bold]{new_crosshair.name}[/bold]' (ID: {doc_id})[/green]")
    
@app.command()
def list(
    show_all: bool = typer.Option(False, "--all", help="Show all crosshairs even deleted ones."),
    page_size: int = typer.Option(
        10, "--page-size", "-p", 
        help="Number of crosshairs to show per page."
    )
):
    # Get request for all crosshairs
    
    all_data = db.all()
    
    if not show_all:
        records = [r for r in all_data if r.get("is_active", True)]
    else:
        records = all_data

    if not records:
        console.print("[yellow]Vault is empty.[/yellow]")
        return

    total_pages = (len(records) - 1) // page_size + 1
    current_page = 0

    while True:
        console.clear() # Clears the terminal
        
        
        # Creates the pagination
        start = current_page * page_size
        end = start + page_size
        chunk = records[start:end]

        # Table creation for the crosshairs
        
        table = Table(
            title=f"CS2 Vault [bold cyan](Page {current_page + 1}/{total_pages})[/bold cyan]",
            caption="[dim]Use ← → Arrows to Navigate | 'q' to Exit[/dim]"
        )
        
        
        table.add_column("ID", style="sky_blue3")
        table.add_column("Name", style="grey70")
        table.add_column("Code", style="pale_green3")
        table.add_column("Status", style="medium_purple3")
        
        for item in chunk:
            status = "[green]Active[/green]" if item.get("is_active", True) else "[red]Archived[/red]"
            table.add_row(str(item.doc_id), item["name"], item["code"], item["created_at"])

        console.print(table)

        # This handles the arrow keys 
        key = readchar.readkey()

        if key == readchar.key.RIGHT:
            if current_page < total_pages - 1:
                current_page += 1
        elif key == readchar.key.LEFT:
            if current_page > 0:
                current_page -= 1
        elif key.lower() == 'q':
            console.clear()
            console.print("[yellow]Exited Vault list.[/yellow]")
            break

@app.command()
def find(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Search by crosshair name"),
    id: Optional[int] = typer.Option(None, "--id", help="Search by crosshair ID")
):
    # Check for command arguments
    
    if name:
        res = find_by_name(db, name)
        item = res[0] if res else None
    elif id:
        item = find_by_id(db, id)
    else:
        console.print("[yellow]Please provide either --name (-n) or --id.[/yellow]")
        raise typer.Exit()

    # Handle no results
    if not item:
        console.print("[bold red]No crosshair found.[/bold red]")
        return

    # Display results
    
    status = "[bold green]ACTIVE[/bold green]" if item.get("is_active", True) else "[bold red]ARCHIVED[/bold red]"
    
    print(f"{item["name"]} - {item["code"]}")


    
    
@app.command()
def edit():
    
    print("Editing...")
@app.command()
def delete():
    print("Deleting..")
if __name__ == "__main__":
    app()
    
