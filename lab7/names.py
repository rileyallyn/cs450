from sklearn.metrics.pairwise import cosine_similarity

from unixcoder_intro import UniXcoderEmbedder

embedder = UniXcoderEmbedder()

print("="*70)
print("Why Variable Names Matter to UniXcoder")
print("="*70)

# Test: Same logic, different variable name lengths
test_cases = {
    "original": "def check(x):\n    return x < 10",
    "short_rename": "def check(y):\n    return y < 10",
    "long_rename": "def check(value):\n    return value < 10",
    "very_long_rename": "def check(input_value):\n    return input_value < 10",
    "semantic_rename": "def check(threshold):\n    return threshold < 10",
}

print("\nOriginal: def check(x): return x < 10")
print("\nComparing variable name changes:")
print("-"*70)

base = embedder.encode(test_cases["original"]).reshape(1, -1)

for name, code in test_cases.items():
    if name != "original":
        emb = embedder.encode(code).reshape(1, -1)
        sim = cosine_similarity(base, emb)[0][0]
        var_name = code.split('(')[1].split(')')[0]
        print(f"{name:20} (var={var_name:15}) similarity: {sim:.4f}")

print("\n" + "="*70)
print("Insight: Variable Names Carry Semantic Information!")
print("="*70)
print("""
UniXcoder doesn't just see variables as placeholders. It recognizes:
- 'age' suggests age-related logic
- 'user_age' suggests user-specific age handling
- 'threshold' suggests boundary checking
- 'x' is generic

When you change variable names, you're potentially changing the
*semantic context* of the code, which UniXcoder picks up on!
""")