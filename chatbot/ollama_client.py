import ollama
from typing import Dict, List
from rich.console import Console
from rich.markdown import Markdown

class OllamaClient:
    def __init__(self, config):
        self.config = config
        self.console = Console()
    
    def generate_response(self, messages: List[Dict]) -> str:
        """Generate a response from Ollama API."""
        try:
            response = ollama.chat(
                model=self.config.get('model', 'llama3'),
                messages=messages,
                options={
                    'temperature': self.config.get('temperature', 0.7)
                }
            )
            return response['message']['content']
        except ollama.ResponseError as e:
            self.console.print(f"[red]Error: {e.error}[/red]")
            return None
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {str(e)}[/red]")
            return None
    
    def print_markdown(self, text: str):
        """Print text as formatted markdown."""
        if text:
            self.console.print(Markdown(text))
    
    def list_models(self) -> List[str]:
        """List available Ollama models."""
        try:
            return [model['model'] for model in ollama.list()['models']]
        except Exception as e:
            self.console.print(f"[red]Error fetching models: {str(e)}[/red]")
            return []
    
    def pull_model(self, model_name: str):
        """Pull a model from Ollama hub."""
        try:
            self.console.print(f"[yellow]Downloading model {model_name}...[/yellow]")
            for progress in ollama.pull(model_name, stream=True):
                if 'completed' in progress:
                    self.console.print(
                        f"[green]Progress: {progress['completed']}/{progress['total']}[/green]"
                    )
            self.console.print(f"[green]Model {model_name} downloaded successfully![/green]")
            return True
        except Exception as e:
            self.console.print(f"[red]Error downloading model: {str(e)}[/red]")
            return False