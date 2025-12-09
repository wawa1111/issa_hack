"""
Configuration and environment variables.
Reads from environment variables (set by Render or system).
"""
import os

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBh2WrdSXTMW6Mrc0ZGz75sWOsgeP3GMa4")
#GEMINI_MODEL = "gemini-pro" # old model used
GEMINI_MODEL = "gemini-1.5-flash-latest"
# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Flask Configuration
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

