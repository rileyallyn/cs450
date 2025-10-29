import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import analyze_image

def describe_image(image_url, detail_level="basic"):
    """Generate description of an image."""
    
    if detail_level == "basic":
        prompt = "Describe this image in one sentence."
    elif detail_level == "detailed":
        prompt = "Provide a detailed description of this image, including objects, colors, and context."
    else:
        prompt = "What do you see in this image?"
    
    response = analyze_image(image_url, prompt)
    return response

# Test with classic freely licensed images
test_images = [
    "https://upload.wikimedia.org/wikipedia/commons/3/37/Oryctolagus_cuniculus_Tasmania_2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/5f/Red_Kangaroos_at_Sturt_National_Park_NSW.jpg"
]

if __name__ == "__main__":
    print("Image Description\n" + "="*50)
    
    for img_url in test_images:
        print(f"\nImage: {img_url}")
        
        # Basic description
        basic = describe_image(img_url, "basic")
        print(f"Basic: {basic}")
        
        # Detailed description
        detailed = describe_image(img_url, "detailed")
        print(f"Detailed: {detailed[:100]}...")