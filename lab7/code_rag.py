import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from code_kb import CodeKnowledgeBase
from util import call_ollama

class CodeRAG:
    """RAG system for code generation and understanding."""
    
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
    
    def generate_code(self, task_description, top_k=3):
        """Generate code based on task description using retrieved examples."""
        # Retrieve relevant examples
        results = self.kb.search(task_description, top_k=top_k)
        
        # Build context
        context_parts = ["Here are relevant code examples from the codebase:\n"]
        
        for i, result in enumerate(results, 1):
            meta = result['metadata']
            context_parts.append(f"\nExample {i}: {meta['name']}")
            if meta['docstring']:
                context_parts.append(f"Purpose: {meta['docstring']}")
            context_parts.append(f"Implementation:\n{result['code']}")
            context_parts.append("")
        
        context = "\n".join(context_parts)
        
        # Create prompt
        prompt = f"""You are a code generation assistant. Based on the example code from the codebase, generate a new function.

{context}

Task: {task_description}

Requirements:
1. Follow the coding style from the examples above
2. Include a clear docstring
3. Use similar naming conventions
4. Keep the function focused and simple

Generated Function:"""
        
        # Generate
        code = call_ollama(prompt, temperature=0.3, num_predict=400)
        
        return {
            'code': code,
            'examples': results
        }
    
    def explain_code(self, code_snippet, top_k=2):
        """Explain code using similar examples from codebase."""
        # Find similar code
        results = self.kb.search(code_snippet, top_k=top_k)
        
        # Build context
        context_parts = ["Similar functions from the codebase:\n"]
        
        for i, result in enumerate(results, 1):
            meta = result['metadata']
            context_parts.append(f"\n{i}. Function: {meta['name']}")
            context_parts.append(f"   Purpose: {meta['docstring']}")
            context_parts.append(f"   Code:\n{result['code']}")
            context_parts.append("")
        
        context = "\n".join(context_parts)
        
        # Create prompt
        prompt = f"""Based on these similar functions from the codebase:

{context}

Explain what this code does and how it works:

{code_snippet}

Provide a clear explanation covering:
1. What the code does (purpose)
2. How it works (logic)
3. How it relates to the similar examples above

Explanation:"""
        
        explanation = call_ollama(prompt, temperature=0.2, num_predict=300)
        
        return {
            'explanation': explanation,
            'similar_functions': results
        }
    
    def refactor_suggestion(self, code_snippet, top_k=3):
        """Suggest refactoring based on codebase patterns."""
        results = self.kb.search(code_snippet, top_k=top_k)
        
        context_parts = ["Best practices from the codebase:\n"]
        for i, result in enumerate(results, 1):
            meta = result['metadata']
            context_parts.append(f"\n{i}. {meta['name']}")
            context_parts.append(f"   {meta['docstring']}")
            context_parts.append(f"   Pattern:\n{result['code']}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""Based on these coding patterns from our codebase:

{context}

Review this code and suggest improvements:

{code_snippet}

Provide:
1. What could be improved
2. How to make it match our codebase patterns
3. Suggested refactored version

Analysis:"""
        
        suggestions = call_ollama(prompt, temperature=0.3, num_predict=400)
        
        return {
            'suggestions': suggestions,
            'reference_patterns': results
        }

if __name__ == "__main__":
    from index_codebase import index_codebase
    
    print("Building Knowledge Base...")
    kb = CodeKnowledgeBase("rag_test")
    index_codebase(kb)
    
    rag = CodeRAG(kb)
    
    # Test 1: Code Generation
    print("\n" + "="*60)
    print("Test 1: Code Generation")
    print("="*60)
    
    task = "Create a function to validate username: 3-20 characters, alphanumeric only, no spaces"
    print(f"\nTask: {task}\n")
    
    result = rag.generate_code(task)
    print("Generated Code:")
    print(result['code'])
    
    print("\n\nBased on these examples:")
    for ex in result['examples']:
        print(f"  - {ex['metadata']['name']} (distance: {ex['distance']:.3f})")
    
    # Test 2: Code Explanation
    print("\n\n" + "="*60)
    print("Test 2: Code Explanation")
    print("="*60)
    
    mystery_code = """def check_user(name, pwd):
    if len(name) < 3:
        return False
    import hashlib
    h = hashlib.sha256(pwd.encode()).hexdigest()
    return True"""
    
    print(f"\nMystery Code:\n{mystery_code}\n")
    
    result = rag.explain_code(mystery_code)
    print("Explanation:")
    print(result['explanation'])