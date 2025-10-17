import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import call_ollama

def generate_function_fewshot(description):
    """Generate Python functions using few-shot prompting."""
    
    prompt = f"""Generate Python functions based on descriptions.

Now generate:
Description: {description}
Code:"""
    
    response = call_ollama(
        prompt, 
        model="cs450", 
        temperature=0.2, 
        num_predict=250
    )
    return response

# Test
descriptions = [
    "A function that finds the maximum value in a list",
    "A function that counts vowels in a string",
    "A function that calculates factorial"
]

print("\n\nFew-Shot Code Generation\n" + "="*50)
for desc in descriptions:
    code = generate_function_fewshot(desc)
    print(f"\nDescription: {desc}")
    print(f"Generated Code:\n{code}\n")