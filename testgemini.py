"""
Test script for Gemini API.
IMPORTANT: Never hardcode API keys. Always use environment variables.

This script uses the same API as gemini_client.py for consistency.

To use this script:
- Option 1: Create a .env file with: GEMINI_API_KEY=your_key_here
- Option 2: Export it: export GEMINI_API_KEY=your_key_here
- Option 3: Set inline: GEMINI_API_KEY=your_key_here python testgemini.py
"""
import os
from pathlib import Path
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# Try to load from .env file for local development (config.py handles this)
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        pass  # dotenv not installed, skip

# Use config which handles .env loading
# Re-import after potential .env load
import importlib
import config
importlib.reload(config)
from config import GEMINI_API_KEY, GEMINI_MODEL

if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY environment variable is not set!")
    print("\nTo fix this, choose one of the following:")
    print("\n  1. Create a .env file in the project root:")
    print("     echo 'GEMINI_API_KEY=your_key_here' > .env")
    print("     python testgemini.py")
    print("\n  2. Export it in your terminal:")
    print("     export GEMINI_API_KEY=your_key_here")
    print("     python testgemini.py")
    print("\n  3. Or set it inline when running:")
    print("     GEMINI_API_KEY=your_key_here python testgemini.py")
    raise ValueError("GEMINI_API_KEY environment variable is required")

# Use the same API as gemini_client.py
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

print(f"Testing with model: {GEMINI_MODEL}")
print(f"API Key loaded: {'Yes' if GEMINI_API_KEY else 'No'} (length: {len(GEMINI_API_KEY) if GEMINI_API_KEY else 0})")
print()

response = model.generate_content("Explain how AI works in a few words")
print("✅ Success! Response:")
print(response.text)