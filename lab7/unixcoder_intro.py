import torch
from transformers import AutoTokenizer, AutoModel

class UniXcoderEmbedder:
    """Wrapper for UniXcoder embeddings - a modern code understanding model."""
    
    def __init__(self):
        print("Loading UniXcoder model (this may take a minute on first run)...")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/unixcoder-base")
        self.model = AutoModel.from_pretrained("microsoft/unixcoder-base")
        self.model.eval()
        print("UniXcoder loaded successfully!")
        print("UniXcoder is a 2022 model trained on code from 5+ languages.")
    
    def encode(self, text):
        """Generate embedding for text using mean pooling."""
        # Tokenize
        inputs = self.tokenizer(text, return_tensors="pt", 
                               truncation=True, max_length=512,
                               padding=True)
        
        # Generate embedding
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Mean pooling over all tokens (best practice for embeddings)
        attention_mask = inputs['attention_mask']
        token_embeddings = outputs.last_hidden_state
        
        # Weighted average using attention mask
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        embedding = (sum_embeddings / sum_mask).squeeze().numpy()
        
        return embedding

# Test the embedder
if __name__ == "__main__":
    embedder = UniXcoderEmbedder()
    
    code = "def validate_email(email):\n    return '@' in email and '.' in email"
    
    print("\n" + "="*60)
    print("Testing UniXcoder Embeddings")
    print("="*60)
    print(f"\nCode: {code}")
    
    embedding = embedder.encode(code)
    print(f"\nEmbedding shape: {embedding.shape}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")