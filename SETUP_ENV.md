# Setting Up Environment Variables

## For Local Development

### Option 1: Export in Current Terminal Session

```bash
export GEMINI_API_KEY=your_api_key_here
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_ANON_KEY=your_anon_key_here

# Then run your scripts
python testgemini.py
python app.py
```

**Note:** This only works for the current terminal session. When you close the terminal, you'll need to export again.

### Option 2: Add to Shell Profile (Permanent)

For **zsh** (macOS default):
```bash
echo 'export GEMINI_API_KEY=your_api_key_here' >> ~/.zshrc
echo 'export SUPABASE_URL=https://your-project.supabase.co' >> ~/.zshrc
echo 'export SUPABASE_ANON_KEY=your_anon_key_here' >> ~/.zshrc

# Reload your shell
source ~/.zshrc
```

For **bash**:
```bash
echo 'export GEMINI_API_KEY=your_api_key_here' >> ~/.bashrc
echo 'export SUPABASE_URL=https://your-project.supabase.co' >> ~/.bashrc
echo 'export SUPABASE_ANON_KEY=your_anon_key_here' >> ~/.bashrc

# Reload your shell
source ~/.bashrc
```

### Option 3: Set Inline When Running

```bash
GEMINI_API_KEY=your_key_here python testgemini.py
GEMINI_API_KEY=your_key_here SUPABASE_URL=... SUPABASE_ANON_KEY=... python app.py
```

## For Render Deployment

1. Go to your Render dashboard
2. Select your service
3. Go to **Environment** tab
4. Add/Edit environment variables:
   - `GEMINI_API_KEY` = your_api_key_here
   - `SUPABASE_URL` = https://your-project.supabase.co
   - `SUPABASE_ANON_KEY` = your_anon_key_here
5. Save and redeploy

## Verify Environment Variables Are Set

Check if variables are set:
```bash
echo $GEMINI_API_KEY
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY
```

Or test with Python:
```bash
python3 -c "import os; print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

## Troubleshooting

### "GEMINI_API_KEY environment variable is required"
- Make sure you exported it in the **same terminal** where you're running the script
- Check with: `echo $GEMINI_API_KEY`
- If empty, export it again: `export GEMINI_API_KEY=your_key`

### Variable works in one terminal but not another
- Each terminal session has its own environment
- Export it in each terminal, or add it to your shell profile (Option 2)

### IDE/Editor not picking up variables
- Some IDEs don't inherit terminal environment variables
- Restart your IDE after exporting
- Or set variables in your IDE's run configuration

