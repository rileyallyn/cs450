import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import call_ollama

def classify_sentiment(review):
    """Classify movie review sentiment using zero-shot prompting."""
    prompt = f"""Classify this movie review as POSITIVE, NEGATIVE, or NEUTRAL.
Return only the classification label.

Review: {review}

Classification:"""
    
    response = call_ollama(
        prompt, 
        temperature=0.1, 
        num_predict=5
    )
    return response.strip()

# Test cases
reviews = [
    "This movie was absolutely amazing! Best film of the year!",
    "Terrible waste of time. I want my money back.",
    "It was okay. Nothing special but not bad either.",
    "A masterpiece of cinema. Brilliantly directed and acted.",
    "Boring and predictable. Fell asleep halfway through."
]

print("Zero-Shot Sentiment Classification\n" + "="*50)
for review in reviews:
    sentiment = classify_sentiment(review)
    print(f"\nReview: {review[:50]}...")
    print(f"Sentiment: {sentiment}")