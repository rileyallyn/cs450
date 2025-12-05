import chromadb

from unixcoder_intro import UniXcoderEmbedder

# Initialize
print("Initializing Chroma and UniXcoder...")
client = chromadb.Client()
embedder = UniXcoderEmbedder()

# Create collection
collection = client.create_collection(
    name="code_snippets_test",
    metadata={"description": "Code snippets with UniXcoder embeddings"}
)

# Sample code functions
code_snippets = [
    {
        'code': """def validate_email(email):
    '''Check if email format is valid.'''
    return '@' in email and '.' in email.split('@')[1]""",
        'name': 'validate_email',
        'purpose': 'email validation'
    },
    {
        'code': """def validate_password(password):
    '''Check if password meets security requirements.'''
    return len(password) >= 8 and any(c.isupper() for c in password)""",
        'name': 'validate_password',
        'purpose': 'password validation'
    },
    {
        'code': """def hash_password(password):
    '''Hash password using SHA-256.'''
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()""",
        'name': 'hash_password',
        'purpose': 'password hashing'
    },
    {
        'code': """def calculate_discount(price, rate):
    '''Apply discount rate to price.'''
    return price * (1 - rate)""",
        'name': 'calculate_discount',
        'purpose': 'price calculation'
    }
]

print("\n" + "="*60)
print("Adding Code to Vector Store")
print("="*60)

# Add to collection
for i, snippet in enumerate(code_snippets):
    embedding = embedder.encode(snippet['code']).tolist()
    collection.add(
        embeddings=[embedding],
        documents=[snippet['code']],
        ids=[f"code_{i}"],
        metadatas=[{
            'function_name': snippet['name'],
            'purpose': snippet['purpose']
        }]
    )
    print(f"Added: {snippet['name']}")

# Test queries
queries = [
    "How do I check if an email is valid?",
    "How do I securely store passwords?",
    "How do I apply a discount to a price?"
]

print("\n" + "="*60)
print("Querying Vector Store")
print("="*60)

for query in queries:
    print(f"\nQuery: {query}")
    print("-" * 60)
    
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    
    for i, (doc, meta, dist) in enumerate(zip(
        results['documents'][0], 
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        print(f"{i}. {meta['function_name']} (distance: {dist:.4f})")
        print(f"   Purpose: {meta['purpose']}")