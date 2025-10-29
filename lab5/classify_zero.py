import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import analyze_image

def classify_image_zeroshot(image_url, categories):
    """Classify image into one of the given categories."""
    
    categories_str = ", ".join(categories)
    prompt = f"""Classify this image into ONE of these categories: {categories_str}
Return ONLY the category name, nothing else."""
    
    response = analyze_image(image_url, prompt, temperature=0.1)
    return response.strip()

# Test with various Wikipedia Commons images
test_cases = [
    # {
    #     "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/481px-Cat03.jpg",
    #     "categories": ["dog", "cat", "bird", "other animal"]
    # },
    # {
    #     "url": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg",
    #     "categories": ["building", "vehicle", "nature", "animal"]
    # }

    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Gotland_Grand_National_October_2023_61.jpg/500px-Gotland_Grand_National_October_2023_61.jpg",
        "categories": ["race", "van", "book"]
    }
]

if __name__ == "__main__":
    print("Zero-Shot Image Classification\n" + "="*50)
    
    for test in test_cases:
        result = classify_image_zeroshot(test["url"], test["categories"])
        print(f"\nImage: {test['url']}")
        print(f"Categories: {test['categories']}")
        print(f"Classification: {result}")