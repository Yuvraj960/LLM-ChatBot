# Ollama Chatbot - CLI Version

A command-line chatbot interface for Ollama with conversation history and configuration options.

## Features

- Chat with various Ollama models
- Maintain conversation history
- Change model parameters (temperature, max history)
- Download new models
- Save and load previous conversations

## Installation

1. **Install Ollama**:
   - Download and install Ollama from [https://ollama.ai](https://ollama.ai)
   - Run `ollama pull llama3` to download a model (or any other model you prefer)

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the script**:
   ```bash
   python -m chatbot.cli
   ```