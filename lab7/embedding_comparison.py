from sklearn.metrics.pairwise import cosine_similarity
import ollama

from unixcoder_intro import UniXcoderEmbedder

# Initialize models
print("Loading models...")
unixcoder = UniXcoderEmbedder()
ollama_client = ollama.Client(host='http://ollama.cs.wallawalla.edu:11434')

def get_ollama_embedding(text):
    """Get generic text embedding from Ollama."""
    response = ollama_client.embeddings(
        model='nomic-embed-text',
        prompt=text
    )
    return response['embedding']

# Test with clearly different code snippets
code_snippets = {
    'email_val_1': """def validate_email(email):
    '''Check if email is valid.'''
    return '@' in email and '.' in email.split('@')[1]""",
    
    'email_val_2': """def check_email(address):
    '''Verify email format.'''
    if '@' not in address:
        return False
    return '.' in address.split('@')[1]""",
    
    'math_calc': """def calculate_compound_interest(principal, rate, years):
    '''Calculate compound interest.'''
    return principal * ((1 + rate) ** years)""",
    
    'string_op': """def reverse_string(text):
    '''Reverse a string.'''
    return text[::-1]"""
}

print("\n" + "="*60)
print("Comparing Generic vs Code-Specific Embeddings")
print("="*60)

# Generate embeddings
print("\nGenerating UniXcoder embeddings...")
unix_embeddings = {}
for name, code in code_snippets.items():
    unix_embeddings[name] = unixcoder.encode(code).reshape(1, -1)

print("Generating generic embeddings...")
generic_embeddings = {}
for name, code in code_snippets.items():
    generic_embeddings[name] = [get_ollama_embedding(code)]

# Compare similar code (both email validation)
print("\n" + "="*60)
print("Test 1: Similar Functions (both email validation)")
print("="*60)
print("email_val_1 vs email_val_2")

unix_sim = cosine_similarity(
    unix_embeddings['email_val_1'], 
    unix_embeddings['email_val_2']
)[0][0]

generic_sim = cosine_similarity(
    generic_embeddings['email_val_1'], 
    generic_embeddings['email_val_2']
)[0][0]

print(f"UniXcoder:      {unix_sim:.4f}")
print(f"Generic model:  {generic_sim:.4f}")
print(f"Difference:     {unix_sim - generic_sim:+.4f}")

# Compare different code (email vs math)
print("\n" + "="*60)
print("Test 2: Different Functions (email vs math)")
print("="*60)
print("email_val_1 vs math_calc")

unix_diff = cosine_similarity(
    unix_embeddings['email_val_1'], 
    unix_embeddings['math_calc']
)[0][0]

generic_diff = cosine_similarity(
    generic_embeddings['email_val_1'], 
    generic_embeddings['math_calc']
)[0][0]

print(f"UniXcoder:      {unix_diff:.4f}")
print(f"Generic model:  {generic_diff:.4f}")
print(f"Difference:     {unix_diff - generic_diff:+.4f}")

# Compare very different code (email vs string)
print("\n" + "="*60)
print("Test 3: Very Different Functions (email vs string reversal)")
print("="*60)
print("email_val_1 vs string_op")

unix_very_diff = cosine_similarity(
    unix_embeddings['email_val_1'], 
    unix_embeddings['string_op']
)[0][0]

generic_very_diff = cosine_similarity(
    generic_embeddings['email_val_1'], 
    generic_embeddings['string_op']
)[0][0]

print(f"UniXcoder:      {unix_very_diff:.4f}")
print(f"Generic model:  {generic_very_diff:.4f}")
print(f"Difference:     {unix_very_diff - generic_very_diff:+.4f}")

# Summary
print("\n" + "="*60)
print("Analysis")
print("="*60)
print("A good code embedding model should:")
print("  - Give HIGH similarity for functionally similar code")
print("  - Give LOW similarity for functionally different code")
print(f"\nUniXcoder discrimination (similar - different): {unix_sim - unix_diff:.4f}")
print(f"Generic discrimination (similar - different):   {generic_sim - generic_diff:.4f}")