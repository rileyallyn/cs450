import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import analyze_image

def ask_about_image(image_url, question):
    """Ask specific questions about an image."""
    response = analyze_image(image_url, question, temperature=0.1)
    return response


test_image = "https://upload.wikimedia.org/wikipedia/commons/9/95/Man_biking_on_Recife_city.jpg"

questions = [
    # "What is the main subject of this image?",
    # "What colors are prominent in this image?",
    # "Is this a photograph or a drawing?",
    # "Describe the person's appearance."
    "What is the architecture of the buildings in the background?",
    "Is the bike electric?",
    "What river is he riding over?"
]

if __name__ == "__main__":
    print("Question-Answering with Images\n" + "="*50)
    
    for question in questions:
        answer = ask_about_image(test_image, question)
        print(f"\nQ: {question}")
        print(f"A: {answer}")