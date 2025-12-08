"""
Configuration and environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBh2WrdSXTMW6Mrc0ZGz75sWOsgeP3GMa4")
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp-01-21"

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Flask Configuration
# Render sets PORT environment variable automatically
# Use PORT if available (Render), otherwise use FLASK_PORT, default to 5001
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
FLASK_PORT = int(os.getenv("PORT", os.getenv("FLASK_PORT", "5001")))

