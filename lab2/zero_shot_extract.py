import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import call_ollama

def extract_info(text):
    """Extract structured information using zero-shot prompting."""
    prompt = f"""Extract the person's name, age, and occupation from this text.
Return as JSON.

Text: {text}

JSON:"""
    
    response = call_ollama(
        prompt, 
        temperature=0.1, 
        num_predict=100
    )
    return response

# Test
# text = "My name is Alice Johnson, I'm 28 years old, and I work as a software engineer."
# text = "Bob Smith, age 35, teacher"
text = "I'm Dave, 29, and I do marketing"
result = extract_info(text)
print("\n\nInformation Extraction\n" + "="*50)
print(f"Input: {text}")
print(f"Output: {result}")