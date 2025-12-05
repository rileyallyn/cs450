from code_kb import CodeKnowledgeBase
from index_codebase import index_codebase

kb = CodeKnowledgeBase("query_test")
index_codebase(kb)

# Test various query formulations
query_tests = {
    "Natural Language": [
        "How do I check if an email is valid?",
        "What's the best way to store passwords securely?",
        "How can I verify a user's identity?",
        "How do I record what happens in the system?"
    ],
    "Technical Terms": [
        "email validation function",
        "password hashing algorithm",
        "user authentication logic",
        "database CRUD operations"
    ],
    "Use Cases": [
        "I need to create a new user account",
        "I want to log in a user",
        "I need to verify session is valid",
        "I want to save user data"
    ],
    "Incomplete/Vague": [
        "email",
        "password",
        "database",
        "user"
    ]
}

print("="*60)
print("Testing Query Types with UniXcoder")
print("="*60)

for query_type, query_list in query_tests.items():
    print(f"\n\n{'='*60}")
    print(f"Query Type: {query_type}")
    print('='*60)
    
    for query in query_list:
        print(f"\n\nQuery: '{query}'")
        print("-" * 60)
        
        results = kb.search(query, top_k=3)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['metadata']['name']:25} (distance: {result['distance']:.3f})")

print("\n\n" + "="*60)
print("Summary")
print("="*60)
print("Observe which query types work best:")
print("- Natural language queries")
print("- Technical terminology")
print("- Use case descriptions")
print("- Single keywords")