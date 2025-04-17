from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import List, Optional

console = Console()

def display_menu(title: str, options: List[str], exit_option: bool = True) -> int:
    """Display a menu and return user's choice."""
    while True:
        console.print(Panel.fit(title, style="bold blue"))
        for i, option in enumerate(options, 1):
            console.print(f"[cyan]{i}.[/cyan] {option}")
        
        if exit_option:
            console.print(f"[cyan]0.[/cyan] Exit")
        
        try:
            choice = console.input("[bold]Enter your choice: [/bold]")
            if not choice.strip():  # Handle empty input
                console.print("[red]Please enter a number.[/red]")
                continue
                
            choice = int(choice)
            if exit_option and choice == 0:
                return -1
            if 1 <= choice <= len(options):
                return choice
            console.print("[red]Invalid choice. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")

def display_conversation_history(history: List[dict]):
    """Display conversation history in a readable format."""
    for message in history:
        role = message['role'].capitalize()
        content = message['content']
        timestamp = message.get('timestamp', '')
        
        if role == 'User':
            console.print(Panel.fit(content, title=f"{role} ({timestamp})", style="green"))
        else:
            console.print(Panel.fit(content, title=f"{role} ({timestamp})", style="blue"))