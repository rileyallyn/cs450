import ast

from code_kb import CodeKnowledgeBase

def parse_python_file(filepath):
    """Parse Python file and extract functions using AST."""
    with open(filepath, 'r') as f:
        code = f.read()
    
    tree = ast.parse(code)
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            docstring = ast.get_docstring(node)
            func_lines = code.split('\n')[node.lineno-1:node.end_lineno]
            func_code = '\n'.join(func_lines)
            
            functions.append({
                'name': node.name,
                'code': func_code,
                'docstring': docstring,
                'lineno': node.lineno,
                'args': [arg.arg for arg in node.args.args]
            })
    
    return functions

def index_codebase(kb, filepath='sample_codebase.py'):
    """Index the sample codebase into knowledge base."""
    print("\n" + "="*60)
    print("Indexing Codebase with AST Parsing")
    print("="*60 + "\n")
    
    functions = parse_python_file(filepath)
    
    for func in functions:
        kb.add_function(
            func['name'],
            func['code'],
            func['docstring'],
            metadata={
                'lineno': func['lineno'],
                'args': str(func['args']),
                'file': filepath
            }
        )
    
    print(f"\nIndexed {len(functions)} functions")
    return kb

if __name__ == "__main__":
    kb = CodeKnowledgeBase("codebase_index")
    index_codebase(kb)
    
    # Test with various natural language queries
    queries = [
        "How do I validate user input?",
        "How do I authenticate a user?",
        "How do I save data to the database?",
        "How do I generate a secure token?",
        "How do I log out a user?",
        "How do I format error messages?"
    ]
    
    print("\n" + "="*60)
    print("Testing Code Search with Natural Language")
    print("="*60)
    
    for query in queries:
        print(f"\n\nQuery: {query}")
        print("-" * 60)
        results = kb.search(query, top_k=2)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['metadata']['name']}")
            print(f"   {result['metadata']['docstring']}")
            print(f"   Distance: {result['distance']:.4f}")