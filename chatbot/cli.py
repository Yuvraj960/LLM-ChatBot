import os
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from typing import Optional

from .config import Config
from .conversation import Conversation
from .ollama_client import OllamaClient
from .utils import display_menu, display_conversation_history

console = Console()

class ChatbotCLI:
    def __init__(self):
        self.config = Config()
        self.conversation = Conversation(self.config)
        self.ollama = OllamaClient(self.config)
        self.running = True
    
    def run(self):
        """Main entry point for the CLI application."""
        self._check_ollama_installation()
        self._welcome_message()
        
        while self.running:
            self._main_menu()
    
    def _check_ollama_installation(self):
        """Check if Ollama is installed and running."""
        try:
            import ollama
            ollama.list()  # Test connection
        except ImportError:
            console.print("[red]Error: Ollama Python package not installed.[/red]")
            console.print("Please install it with: pip install ollama")
            sys.exit(1)
        except Exception as e:
            console.print("[red]Error: Could not connect to Ollama.[/red]")
            console.print("Please ensure Ollama is installed and running.")
            console.print("Download from https://ollama.ai")
            sys.exit(1)
    
    def _welcome_message(self):
        """Display welcome message and current configuration."""
        console.print(Panel.fit(
            "Ollama Chatbot - CLI Version",
            style="bold blue"
        ))
        console.print(f"Current model: [green]{self.config.get('model')}[/green]")
        console.print(f"Temperature: [green]{self.config.get('temperature')}[/green]")
        console.print("\n")
    
    def _main_menu(self):
        """Display the main menu and handle user choice."""
        options = [
            "Start new conversation",
            "Continue previous conversation",
            "Change settings",
            "List available models",
            "Download new model"
        ]
        
        choice = display_menu("Main Menu", options)
        
        if choice == -1:
            self.running = False
        elif choice == 1:
            self._start_new_conversation()
        elif choice == 2:
            self._continue_conversation()
        elif choice == 3:
            self._change_settings()
        elif choice == 4:
            self._list_models()
        elif choice == 5:
            self._download_model()
    
    def _start_new_conversation(self):
        """Start a new conversation."""
        self.conversation.start_new_conversation()
        console.print("[green]New conversation started.[/green]\n")
        self._chat_loop()
    
    def _continue_conversation(self):
        """Continue a previous conversation."""
        conversations = self.conversation.list_conversations()
        if not conversations:
            console.print("[yellow]No previous conversations found.[/yellow]")
            return
        
        options = [Path(conv).name for conv in conversations]
        choice = display_menu("Select Conversation", options)
        
        if choice > 0:
            if self.conversation.load_conversation(conversations[choice-1]):
                console.print("[green]Conversation loaded successfully.[/green]")
                display_conversation_history(self.conversation.get_history())
                self._chat_loop()
            else:
                console.print("[red]Failed to load conversation.[/red]")
    
    def _chat_loop(self):
        """Main chat loop for user interaction."""
        console.print("\n[bold]Chat with the AI (type 'exit' to end)[/bold]\n")
        
        while True:
            try:
                user_input = Prompt.ask("[bold green]You[/bold green]")
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                if not user_input.strip():
                    continue
                
                # Add user message to conversation
                self.conversation.add_message("user", user_input)
                
                # Get AI response
                console.print("[bold blue]AI[/bold blue] is thinking...")
                response = self.ollama.generate_response(
                    self.conversation.get_history()
                )
                
                if response:
                    # Add AI response to conversation
                    self.conversation.add_message("assistant", response)
                    self.ollama.print_markdown(response)
                else:
                    console.print("[red]No response received from AI.[/red]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Conversation interrupted.[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
                break
    
    def _change_settings(self):
        """Change application settings."""
        options = [
            f"Change model (current: {self.config.get('model')})",
            f"Change temperature (current: {self.config.get('temperature')})",
            f"Change max history length (current: {self.config.get('max_history')})",
            f"Toggle conversation saving (current: {'ON' if self.config.get('save_conversations') else 'OFF'})"
        ]
        
        choice = display_menu("Settings", options)
        
        if choice == 1:
            self._change_model()
        elif choice == 2:
            self._change_temperature()
        elif choice == 3:
            self._change_max_history()
        elif choice == 4:
            current = self.config.get('save_conversations')
            self.config.set('save_conversations', not current)
            console.print(f"[green]Conversation saving is now {'ON' if not current else 'OFF'}[/green]")
    
    def _change_model(self):
        """Change the model used for generation."""
        available_models = self.config.get_available_models()
        if not available_models:
            console.print("[red]No models available. Please download one first.[/red]")
            return
        
        options = available_models
        choice = display_menu("Select Model", options, exit_option=False)
        
        if choice > 0:
            self.config.set('model', available_models[choice-1])
            console.print(f"[green]Model changed to {available_models[choice-1]}[/green]")
    
    def _change_temperature(self):
        """Change the temperature parameter."""
        try:
            temp = float(Prompt.ask(
                "Enter temperature (0.1-1.0)",
                default=str(self.config.get('temperature'))
            ))
            if 0.1 <= temp <= 1.0:
                self.config.set('temperature', temp)
                console.print(f"[green]Temperature set to {temp}[/green]")
            else:
                console.print("[red]Temperature must be between 0.1 and 1.0[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
    
    def _change_max_history(self):
        """Change the maximum history length."""
        try:
            max_hist = int(Prompt.ask(
                "Enter max history length (1-20)",
                default=str(self.config.get('max_history'))
            ))
            if 1 <= max_hist <= 20:
                self.config.set('max_history', max_hist)
                console.print(f"[green]Max history set to {max_hist}[/green]")
            else:
                console.print("[red]Max history must be between 1 and 20[/red]")
        except ValueError:
            console.print("[red]Please enter a valid integer[/red]")
    
    def _list_models(self):
        """List available models."""
        models = self.ollama.list_models()
        if models:
            console.print(Panel.fit(
                "Available Models",
                style="bold blue"
            ))
            for model in models:
                console.print(f"- {model}")
        else:
            console.print("[yellow]No models available. Please download one first.[/yellow]")
    
    def _download_model(self):
        """Download a new model from Ollama hub."""
        model_name = Prompt.ask("Enter model name to download (e.g., 'llama3')")
        if model_name:
            if Confirm.ask(f"Download model '{model_name}'?"):
                self.ollama.pull_model(model_name)

def main():
    """Entry point for the CLI application."""
    try:
        chatbot = ChatbotCLI()
        chatbot.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/red]")

if __name__ == "__main__":
    main()