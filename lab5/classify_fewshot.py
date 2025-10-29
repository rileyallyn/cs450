import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import analyze_image

def classify_activity_basic(image_url):
    """Basic work vs leisure classification."""
    
    prompt = """Classify this image as WORK or LEISURE.

Return only: WORK or LEISURE"""
    
    response = analyze_image(image_url, prompt, temperature=0.1)
    return response.strip()

def classify_activity_guided(image_url):
    """Classification with specific guidelines for edge cases."""
    
    prompt = """Classify this image as WORK or LEISURE.

Guidelines:
- WORK: Any activity that could generate income or is done professionally:
  * Professional sports like running & track & field (even if enjoyable)
  * Content creation (photography, streaming)
  * Playing music (including street performers)
  * Fitness like a Yoga instructor
  * Competitive activities with prizes/sponsorships
  * Volunteer work or unpaid internships
  
- LEISURE: Activities purely for personal enjoyment:
  * Recreational sports without competition
  * Hobbies without monetization intent
  * Social gatherings
  * Personal fitness

Return only: WORK or LEISURE"""
    
    response = analyze_image(image_url, prompt, temperature=0.1)
    return response.strip()

# Ambiguous images where guidelines matter
test_images = [
    # Professional athlete training
    "https://upload.wikimedia.org/wikipedia/commons/1/19/Sergio_Ottolina_1964.jpg",
    
    # Street musician (could be work or hobby)
    "https://upload.wikimedia.org/wikipedia/commons/3/3d/Arles_Busker_IMG_8299.jpg",
    
    # Yoga class (fitness or instructor?)
    "https://upload.wikimedia.org/wikipedia/commons/8/87/Yoga_Class.jpg"
]

if __name__ == "__main__":
    print("Work vs Leisure Classification\n" + "="*50)
    
    for img_url in test_images:
        basic = classify_activity_basic(img_url)
        guided = classify_activity_guided(img_url)
        
        print(f"\nImage: {img_url.split('/')[-1]}")
        print(f"Basic classification:  {basic}")
        print(f"With guidelines:       {guided}")
        print(f"Different result:      {'YES ✓' if basic != guided else 'NO'}")