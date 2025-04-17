import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class Conversation:
    def __init__(self, config):
        self.config = config
        self.history_path = Path.home() / ".ollama_chatbot" / "conversations"
        self.history_path.mkdir(parents=True, exist_ok=True)
        self.current_conversation = []
        self.current_file = None
    
    def start_new_conversation(self):
        """Start a new conversation with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_file = self.history_path / f"conversation_{timestamp}.json"
        self.current_conversation = []
    
    def add_message(self, role: str, content: str):
        """Add a message to the current conversation."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.current_conversation.append(message)
        
        if self.config.get('save_conversations', True):
            self._save_conversation()
    
    def get_history(self, max_messages: int = None) -> List[Dict]:
        """Get conversation history."""
        if max_messages is None:
            max_messages = self.config.get('max_history', 10)
        return self.current_conversation[-max_messages:]
    
    def _save_conversation(self):
        """Save the current conversation to file."""
        if self.current_file:
            with open(self.current_file, 'w') as f:
                json.dump(self.current_conversation, f, indent=4)
    
    def load_conversation(self, file_path: str):
        """Load a conversation from file."""
        try:
            with open(file_path, 'r') as f:
                self.current_conversation = json.load(f)
            self.current_file = Path(file_path)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def list_conversations(self) -> List[str]:
        """List all saved conversations."""
        return sorted(
            [str(f) for f in self.history_path.glob("conversation_*.json")],
            reverse=True
        )