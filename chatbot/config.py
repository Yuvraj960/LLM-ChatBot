import os
from dotenv import load_dotenv
from pathlib import Path
import json

class Config:
    def __init__(self):
        load_dotenv()
        self.config_path = Path.home() / ".ollama_chatbot"
        self.config_file = self.config_path / "config.json"
        
        # Create config directory if it doesn't exist
        self.config_path.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            "model": "llama3",
            "temperature": 0.7,
            "max_history": 10,
            "save_conversations": True
        }
        
        # Load or create config
        if not self.config_file.exists():
            self._create_default_config()
        self.config = self._load_config()
    
    def _create_default_config(self):
        """Create default configuration file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.default_config, f, indent=4)
    
    def _load_config(self):
        """Load configuration from file."""
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value and save to file."""
        self.config[key] = value
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get_available_models(self):
        """Get list of available Ollama models."""
        try:
            import ollama
            return [model['name'] for model in ollama.list()['models']]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return ["llama3", "mistral", "gemma"]  # Default fallback