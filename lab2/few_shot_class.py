import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from util import call_ollama

def classify_email_fewshot(email_body):
    """Classify emails as SPAM, IMPORTANT, or NORMAL using few-shot."""
    
    prompt = f"""Classify emails as SPAM, IMPORTANT, or NORMAL.

Example 1:
Email: "Congratulations! You've won $1,000,000! Click here now!"
Classification: SPAM

Example 1.5:
Email: "Urgent: Your Account Will Be Closed!" 
Classification: SPAM

Example 2:
Email: "Meeting with CEO rescheduled to tomorrow 9am. Please confirm."
Classification: IMPORTANT

Example 3:
Email: "Weekly newsletter: Here are this week's top articles."
Classification: NORMAL

Now classify this email:
Email: {email_body}
Classification:"""
    
    response = call_ollama(
        prompt, 
        temperature=0.1, 
        num_predict=10
    )
    return response.strip()

# Test cases
emails = [
    "URGENT: Your account will be closed unless you verify now!",
    "Board meeting agenda attached. Review before Friday's meeting.",
    "Thanks for signing up for our service. Welcome!",
    "You are the lucky winner! Claim your prize within 24 hours!",
    "Quarterly results are in. Please review the attached report ASAP."
]

print("Few-Shot Email Classification\n" + "="*50)
for email in emails:
    classification = classify_email_fewshot(email)
    print(f"\nEmail: {email[:60]}...")
    print(f"Classification: {classification}")