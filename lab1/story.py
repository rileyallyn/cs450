from ollama_client import call_ollama

prompt = "Tell me a cool story"

response = call_ollama(
    prompt, 
    temperature=0.9, 
    top_p=0.2,
    top_k=9,
    num_predict=40
)

print(f"Response: {response}\n")