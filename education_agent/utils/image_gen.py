import requests
import os
import base64
import time
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

def generate_image(prompt: str):
    """
    Generate an image using Pollinations.ai with Retry Logic and Timeout.
    """
    # Max retries if request fails
    max_retries = 3
    
    try:
        # Clean and encode the prompt
        clean_prompt = prompt.strip().replace("\n", " ")
        encoded_prompt = urllib.parse.quote(clean_prompt)
        
        # Unique seed to avoid cache issues
        seed = os.urandom(4).hex()
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
        
        print(f"--- [DEBUG] Fetching image: {clean_prompt[:40]}... ---")

        for attempt in range(max_retries):
            try:
                # Increased timeout to 30 seconds for image generation
                response = requests.get(image_url, timeout=30)
                
                if response.status_code == 200:
                    print(f"--- [DEBUG] Success on attempt {attempt + 1} ---")
                    return base64.b64encode(response.content).decode('utf-8')
                else:
                    print(f"Attempt {attempt + 1} failed with status {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} error: {e}")
            
            # Wait a bit before retrying
            if attempt < max_retries - 1:
                time.sleep(2)
                
        return None
            
    except Exception as e:
        print(f"Image generation exception: {e}")
        return None
