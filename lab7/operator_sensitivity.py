from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from unixcoder_intro import UniXcoderEmbedder

print("Loading UniXcoder...")
embedder = UniXcoderEmbedder()

# Original function
original = """def validate_age(age):
    '''Check if age meets minimum requirement.'''
    if age < 18:
        return False
    return True"""

# Test cases: progressively change operators
test_cases = {
    "original": {
        "code": """def validate_age(age):
    '''Check if age meets minimum requirement.'''
    if age < 18:
        return False
    return True""",
        "changes": "None (baseline)",
        "description": "Original: age < 18"
    },
    
    "one_operator": {
        "code": """def validate_age(age):
    '''Check if age meets minimum requirement.'''
    if age > 18:
        return False
    return True""",
        "changes": "1 operator: < → >",
        "description": "Changed: age > 18 (completely different logic)"
    },
    
    "two_operators": {
        "code": """def validate_age(age):
    '''Check if age meets minimum requirement.'''
    if age > 18:
        return True
    return False""",
        "changes": "2 operators: < → >, flip returns",
        "description": "Changed: age > 18, swapped True/False"
    },
    
    "three_operators": {
        "code": """def validate_age(age):
    '''Check if age meets minimum requirement.'''
    if age >= 21:
        return True
    return False""",
        "changes": "3 operators: < → >=, 18 → 21, flip returns",
        "description": "Changed: age >= 21, swapped True/False"
    },
    
    "cosmetic_only": {
        "code": """def validate_age(user_age):
    '''Check if age meets minimum requirement.'''
    if user_age < 18:
        return False
    return True""",
        "changes": "0 operators (cosmetic: age → user_age)",
        "description": "Only variable name changed"
    },
    
    "comment_only": {
        "code": """def validate_age(age):
    '''Check if age meets minimum requirement.'''
    # Checking minimum age limit
    if age < 18:
        return False
    return True""",
        "changes": "0 operators (added comment)",
        "description": "Only added comment"
    }
}

print("\n" + "="*70)
print("UniXcoder Operator Sensitivity Test")
print("="*70)
print("\nOriginal Function:")
print(original)
print("\n" + "="*70)

# Generate embeddings
embeddings = {}
for name, test in test_cases.items():
    embeddings[name] = embedder.encode(test['code']).reshape(1, -1)

# Calculate similarities to original
base = embeddings["original"]
results = []

for name, test in test_cases.items():
    if name != "original":
        sim = cosine_similarity(base, embeddings[name])[0][0]
        results.append({
            'name': name,
            'similarity': sim,
            'changes': test['changes'],
            'description': test['description']
        })

# Sort by similarity (highest first)
results.sort(key=lambda x: x['similarity'], reverse=True)

print("\nSimilarity to Original (sorted high to low):")
print("="*70)
print(f"{'Test Case':<20} {'Similarity':<12} {'Changes':<30}")
print("-"*70)

for r in results:
    print(f"{r['name']:<20} {r['similarity']:<12.4f} {r['changes']:<30}")

print("\n" + "="*70)
print("Detailed Analysis")
print("="*70)

for r in results:
    print(f"\n{r['name']}:")
    print(f"  Similarity: {r['similarity']:.4f}")
    print(f"  Changes: {r['changes']}")
    print(f"  Description: {r['description']}")


# import ollama

# ollama_client = ollama.Client(host='http://ollama.cs.wallawalla.edu:11434')

# def get_ollama_embedding(text):
#     response = ollama_client.embeddings(
#         model='nomic-embed-text',
#         prompt=text
#     )
#     return response['embedding']

# # Compare UniXcoder vs Generic for one operator change
# original_unix = embedder.encode(original).reshape(1, -1)
# one_op_unix = embedder.encode(test_cases["one_operator"]["code"]).reshape(1, -1)

# original_gen = [get_ollama_embedding(original)]
# one_op_gen = [get_ollama_embedding(test_cases["one_operator"]["code"])]

# unix_sim = cosine_similarity(original_unix, one_op_unix)[0][0]
# gen_sim = cosine_similarity(original_gen, one_op_gen)[0][0]

# print("\n" + "="*70)
# print("UniXcoder vs Generic Embedding Comparison")
# print("="*70)
# print(f"UniXcoder similarity (< → >): {unix_sim:.4f}")
# print(f"Generic similarity (< → >):   {gen_sim:.4f}")
# print(f"Difference:                   {abs(unix_sim - gen_sim):.4f}")
# print("\nWhich model better recognizes the logical change?")