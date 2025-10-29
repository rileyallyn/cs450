import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import analyze_image

def detect_objects(image_url):
    """Detect and list objects in an image."""
    
    prompt = """List all objects you can identify in this image.
Format: Return a comma-separated list of objects."""
    
    response = analyze_image(image_url, prompt, temperature=0.2)
    return response

def count_objects(image_url, object_type):
    """Count specific objects in an image."""
    
    prompt = f"How many {object_type} are in this image? Return only a number."
    response = analyze_image(image_url, prompt, temperature=0.1)
    return response

if __name__ == "__main__":
    # Using a simple test image
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Small_terracotta_figurines%2C_Ancient_toys%2C_Dice%2C_Spinning_tops%2C_AM_of_Corinth%2C_202929x.jpg/640px-Small_terracotta_figurines%2C_Ancient_toys%2C_Dice%2C_Spinning_tops%2C_AM_of_Corinth%2C_202929x.jpg"
    
    print("Object Detection\n" + "="*50)
    
    # List objects
    objects = detect_objects(image_url)
    print(f"\nDetected objects: {objects}")
    
    # Count specific objects
    count = count_objects(image_url, "stone creations")
    print(f"count: {count}")