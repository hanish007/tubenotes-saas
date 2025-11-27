from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit(1)

try:
    client = genai.Client(api_key=api_key)
    print("Listing available models...")
    count = 0
    for model in client.models.list():
        # Check if 'generateContent' is in supported_actions
        # Note: supported_actions might be a list of strings
        if "generateContent" in (model.supported_actions or []):
            print(f"- {model.name}")
            count += 1
    
    if count == 0:
        print("No models found with 'generateContent' capability.")

except Exception as e:
    print(f"Error listing models: {e}")
