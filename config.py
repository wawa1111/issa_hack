"""
Configuration and environment variables.

SECURITY: Never hardcode API keys in this file!
- For local development: Use .env file (not committed to git)
- For Render deployment: Set environment variables in Render dashboard
- .env file is in .gitignore and .renderignore, so it's never deployed

How it works:
1. First tries to load from .env file (if exists) - for local development
2. Then reads from os.getenv() - works for both local and Render
3. On Render: .env doesn't exist, so it uses environment variables from dashboard
4. On local: .env exists, loads it, then os.getenv() reads the loaded values
"""
import os
from pathlib import Path

# Load .env file for local development ONLY (optional - only if file exists)
# On Render: .env file doesn't exist, so this is skipped and we use os.getenv() directly
# .env is in .gitignore, so it's never committed to GitHub
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # dotenv not installed (shouldn't happen, but skip gracefully)
        pass

# Gemini Configuration
# API key MUST be set as environment variable - never hardcode it
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is required.\n"
        "For local development: Create a .env file or export it: export GEMINI_API_KEY=your_key\n"
        "For Render: Set it in the dashboard under Environment Variables"
    )

GEMINI_MODEL = "gemini-2.5-flash"
# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Flask Configuration
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

