import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import chat_ollama

class ConversationManager:
    """Manage conversation context efficiently."""
    
    def __init__(self, system_prompt="", max_history=10):
        self.system_prompt = system_prompt
        self.messages = []
        self.max_history = max_history
        
        if system_prompt:
            self.messages.append({
                'role': 'system',
                'content': system_prompt
            })
    
    def add_user_message(self, content):
        """Add user message to history."""
        self.messages.append({
            'role': 'user',
            'content': content
        })
        self._trim_history()
    
    def get_response(self, temperature=0.7):
        """Get model response and add to history."""
        response = chat_ollama(self.messages, temperature=temperature)
        self.messages.append({
            'role': 'assistant',
            'content': response
        })
        self._trim_history()
        return response
    
    def _trim_history(self):
        """Keep only recent messages."""
        # Keep system prompt + last N messages
        if len(self.messages) > self.max_history + 1:
            system = self.messages[0] if self.messages[0]['role'] == 'system' else None
            recent = self.messages[-(self.max_history):]
            self.messages = ([system] if system else []) + recent
    
    def get_summary(self):
        """Summarize conversation so far."""
        convo = "\n".join([
            f"{m['role']}: {m['content']}" 
            for m in self.messages if m['role'] != 'system'
        ])
        return convo

conversation = ConversationManager(
    system_prompt="You are a software building tool, with knowledge in python games. Especially the library pygame",
    max_history=6
)

conversation.add_user_message("Create a Python snake game in Pygame in under 400 lines of code")
print("Create a Python snake game in Pygame in under 400 lines of code")
response = conversation.get_response()
print(f"Assistant {response}")

conversation.add_user_message("Based on popular implementations of the classic game Snake, what are 2 of the best customizations for this game? Do not provide any examples.")
print("User: Based on popular implementations of the classic game Snake, what are 2 of the best customizations for this game? Do not provide any examples.")
response = conversation.get_response()
print(f"Assistant {response}")

conversation.add_user_message("Create a Python snake game which implements those features in Pygame in under 500 lines of code")
print("User: Create a Python snake game which implements those features in Pygame in under 500 lines of code")
response = conversation.get_response()
print(f"Assistant {response}")