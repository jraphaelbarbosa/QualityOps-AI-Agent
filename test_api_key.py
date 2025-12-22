import os
from dotenv import load_dotenv

load_dotenv()

# Test with google-generativeai directly
try:
    import google.generativeai as genai
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment")
        exit(1)
    
    print(f"API Key found: {api_key[:10]}...")
    
    genai.configure(api_key=api_key)
    
    # List available models
    print("\n=== Available Gemini Models ===")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    
    # Try a simple generation
    print("\n=== Testing simple generation ===")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello in one word")
    print(f"Response: {response.text}")
    print("\n✅ API key is valid and working!")
    
except ImportError:
    print("ERROR: google-generativeai not installed. Run: pip install google-generativeai")
except Exception as e:
    print(f"ERROR: {e}")
