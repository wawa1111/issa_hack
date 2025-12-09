# Security Guidelines

## API Keys and Secrets

**IMPORTANT: Never commit API keys or secrets to GitHub!**

### Current Setup ✅

1. **`.env` file is in `.gitignore`**
   - Your local `.env` file will NOT be committed to GitHub
   - Verify: `git status` should NOT show `.env`

2. **`.env` file is in `.renderignore`**
   - Your local `.env` file will NOT be deployed to Render
   - Render uses environment variables from the dashboard instead

3. **No hardcoded keys in code**
   - All API keys come from environment variables
   - Code uses `os.getenv()` which reads from:
     - `.env` file (local development only, if file exists)
     - Environment variables (Render dashboard or system)

### How It Works

**Local Development:**
```bash
# Create .env file (not committed to git)
echo "GEMINI_API_KEY=your_key_here" > .env
echo "SUPABASE_URL=your_url_here" >> .env
echo "SUPABASE_ANON_KEY=your_key_here" >> .env

# Run locally
python app.py
```

**Render Deployment:**
1. Go to Render dashboard → Your service → Environment
2. Add environment variables:
   - `GEMINI_API_KEY` = your_key_here
   - `SUPABASE_URL` = your_url_here
   - `SUPABASE_ANON_KEY` = your_key_here
3. Deploy - code automatically uses these variables

### Verification

**Check if .env is ignored by git:**
```bash
git check-ignore .env
# Should output: .env
```

**Check if any API keys are in code:**
```bash
grep -r "AIzaSy" . --exclude-dir=.git
# Should output nothing (no matches)
```

**Verify environment variables are set (Render):**
- Go to Render dashboard → Environment
- You should see your variables listed (values are masked)

### If You Accidentally Committed .env

If you accidentally committed `.env` to git:

1. **Remove it from git history:**
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from git"
   ```

2. **Rotate your API keys:**
   - Generate new keys in Google AI Studio / Supabase
   - Update them in Render dashboard
   - Update your local `.env` file

3. **Verify it's in .gitignore:**
   ```bash
   echo ".env" >> .gitignore
   git add .gitignore
   git commit -m "Ensure .env is ignored"
   ```

### Best Practices

✅ **DO:**
- Use `.env` file for local development
- Set environment variables in Render dashboard for production
- Keep `.env` in `.gitignore`
- Rotate keys if they're ever exposed

❌ **DON'T:**
- Commit `.env` to git
- Hardcode API keys in source code
- Share API keys in screenshots or documentation
- Use the same keys for development and production

