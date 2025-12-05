import chromadb

from unixcoder_intro import UniXcoderEmbedder

class CodeKnowledgeBase:
    """Knowledge base for code using UniXcoder and Chroma."""
    
    def __init__(self, collection_name="code_kb"):
        print("Initializing Code Knowledge Base...")
        self.client = chromadb.Client()
        self.embedder = UniXcoderEmbedder()
        
        # Create or reset collection
        try:
            self.client.delete_collection(collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"description": "Code KB with UniXcoder embeddings"}
        )
        print(f"Created collection: {collection_name}")
        self.counter = 0
    
    def _create_searchable_text(self, func_name, func_code, docstring=None):
        """Create rich text representation for embedding."""
        parts = [f"Function name: {func_name}"]
        if docstring:
            parts.append(f"Description: {docstring}")
        parts.append(f"Implementation:\n{func_code}")
        return "\n".join(parts)
    
    def add_function(self, func_name, func_code, docstring=None, metadata=None):
        """Add a function to the knowledge base."""
        # Create searchable text with context
        searchable = self._create_searchable_text(func_name, func_code, docstring)
        
        # Generate embedding
        embedding = self.embedder.encode(searchable).tolist()
        
        # Prepare metadata
        meta = {
            'name': func_name,
            'docstring': docstring or '',
            'type': 'function'
        }
        if metadata:
            meta.update(metadata)
        
        # Add to collection
        doc_id = f"func_{self.counter}"
        self.collection.add(
            embeddings=[embedding],
            documents=[func_code],
            metadatas=[meta],
            ids=[doc_id]
        )
        
        self.counter += 1
        print(f"Added: {func_name}")
    
    def search(self, query, top_k=3):
        """Search for relevant code snippets."""
        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                'id': results['ids'][0][i],
                'code': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted
    
    def get_count(self):
        """Get number of items in KB."""
        return self.collection.count()

# Test
if __name__ == "__main__":
    kb = CodeKnowledgeBase("test_kb")
    
    print("\n" + "="*60)
    print("Building Code Knowledge Base")
    print("="*60 + "\n")
    
    # Add various functions
    kb.add_function(
        "validate_email",
        """def validate_email(email):
    return '@' in email and '.' in email.split('@')[1]""",
        "Check if email format is valid"
    )
    
    kb.add_function(
        "validate_password",
        """def validate_password(pwd):
    return len(pwd) >= 8 and any(c.isdigit() for c in pwd)""",
        "Check if password meets requirements"
    )
    
    kb.add_function(
        "hash_password",
        """def hash_password(pwd):
    import hashlib
    return hashlib.sha256(pwd.encode()).hexdigest()""",
        "Hash password for secure storage"
    )
    
    kb.add_function(
        "send_email",
        """def send_email(to, subject, body):
    print(f"Sending to {to}: {subject}")
    return True""",
        "Send email to recipient"
    )
    
    print(f"\nTotal functions: {kb.get_count()}")
    
    # Test search with different query types
    queries = [
        "How do I validate user email addresses?",
        "email format validation",
        "check if email is correct format"
    ]
    
    for query in queries:
        print(f"\n" + "="*60)
        print(f"Search: {query}")
        print("="*60 + "\n")
        
        results = kb.search(query, top_k=2)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['metadata']['name']}")
            print(f"   {result['metadata']['docstring']}")
            print(f"   Distance: {result['distance']:.4f}")
            print()