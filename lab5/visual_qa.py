import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import analyze_image

def visual_qa(image_url, questions):
    """Answer multiple questions about an image."""
    
    results = []
    for question in questions:
        answer = analyze_image(image_url, question, temperature=0.2)
        results.append((question, answer))
    
    return results

# Test image
#image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons.jpg/360px-Tour_Eiffel_Wikimedia_Commons.jpg"
image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg"

questions = [
    "What landmark is shown in this image?",
    "What time of day is it?",
    "Are there people visible?",
    "What's the weather like?"
]

if __name__ == "__main__":
    print("Visual Question Answering\n" + "="*50)
    
    results = visual_qa(image_url, questions)
    
    for q, a in results:
        print(f"\nQ: {q}")
        print(f"A: {a}")