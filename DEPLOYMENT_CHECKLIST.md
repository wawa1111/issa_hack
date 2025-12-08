# Render Deployment Checklist

## Pre-Deployment Checklist

- [x] Code uses environment variables (no hardcoded paths)
- [x] `app.py` is the main entry point
- [x] `requirements.txt` includes all dependencies
- [x] Port configuration uses Render's `PORT` env var
- [x] App binds to `0.0.0.0` (not localhost)
- [x] No local machine paths in code
- [x] Supabase tables created (run `init_supabase.sql`)

## Render Configuration

### Build Command
```
pip install -r requirements.txt
```

### Start Command
```
python app.py
```

### Root Directory
Leave empty (uses repository root)

### Region
Singapore (Southeast Asia)

### Environment Variables (Set in Render Dashboard)

1. **GEMINI_API_KEY**
   - Your Gemini API key

2. **SUPABASE_URL**
   - Your Supabase project URL
   - Format: `https://xxxxx.supabase.co`

3. **SUPABASE_ANON_KEY**
   - Your Supabase anon/public key
   - Found in Supabase Settings > API

### Optional Environment Variables

- **FLASK_DEBUG**: `False` (recommended for production)

## Post-Deployment Verification

1. [ ] Health endpoint works: `https://your-service.onrender.com/health`
2. [ ] Test `/generate-reply` endpoint
3. [ ] Verify Supabase connection (check logs)
4. [ ] Verify Gemini API connection (test endpoint)

## Files Included for Deployment

- ✅ `app.py` - Main Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `config.py` - Configuration (uses env vars)
- ✅ `supabase_client.py` - Supabase operations
- ✅ `prompt_manager.py` - Prompt management
- ✅ `gemini_client.py` - Gemini API client
- ✅ `conversation_parser.py` - Conversation parsing
- ✅ `render.yaml` - Optional Render blueprint

## Files Excluded (via .gitignore/.renderignore)

- `.env` - Not needed (use Render env vars)
- `__pycache__/` - Python cache
- `*.db`, `*.sqlite` - Local databases
- `venv/` - Virtual environment

## Notes

- Render automatically sets `PORT` environment variable
- The app will use `PORT` if available, otherwise falls back to `FLASK_PORT` or default `5001`
- No `.env` file needed on Render - all config via environment variables
- Make sure Supabase tables exist before deploying

