from sklearn.metrics.pairwise import cosine_similarity

from unixcoder_intro import UniXcoderEmbedder

embedder = UniXcoderEmbedder()

# Test how UniXcoder handles code variations
test_cases = {
    "original": """def add_numbers(a, b):
    '''Add two numbers together.'''
    return a + b""",
    
    "renamed_vars": """def add_numbers(x, y):
    '''Add two numbers together.'''
    return x + y""",
    
    "different_name": """def sum_values(a, b):
    '''Add two numbers together.'''
    return a + b""",
    
    "with_typing": """def add_numbers(a: int, b: int) -> int:
    '''Add two numbers together.'''
    return a + b""",
    
    "different_logic": """def multiply_numbers(a, b):
    '''Multiply two numbers together.'''
    return a * b""",
    
    "completely_different": """def send_email(recipient, message):
    '''Send an email to recipient.'''
    print(f"Sending to {recipient}: {message}")"""
}

print("\n" + "="*60)
print("Testing UniXcoder's Code Understanding")
print("="*60)

# Get embeddings
embeddings = {name: embedder.encode(code).reshape(1, -1) 
              for name, code in test_cases.items()}

# Compare all against original
base = embeddings["original"]
print(f"\nBase code:\n{test_cases['original']}\n")
print("="*60)
print("Similarity Scores:")
print("="*60)

results = []
for name, code in test_cases.items():
    if name != "original":
        sim = cosine_similarity(base, embeddings[name])[0][0]
        results.append((name, sim))

# Sort by similarity (highest first)
results.sort(key=lambda x: x[1], reverse=True)

for name, sim in results:
    print(f"{sim:.4f} - {name}")

print("\n" + "="*60)
print("Observations:")
print("="*60)
print("Higher scores = more similar to original")