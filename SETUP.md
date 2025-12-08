# Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Supabase

1. **Create Supabase Project**
   - Go to https://app.supabase.com
   - Create a new project
   - Wait for it to initialize

2. **Create Tables**
   - Go to SQL Editor in your Supabase dashboard
   - Copy and paste the contents of `init_supabase.sql`
   - Click "Run" to execute

3. **Get Credentials**
   - Go to Settings > API
   - Copy:
     - **Project URL** (looks like: `https://xxxxx.supabase.co`)
     - **anon/public key** (long string starting with `eyJ...`)

## Step 3: Configure Environment

1. Copy `env_template.txt` to `.env`:
   ```bash
   cp env_template.txt .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```
   GEMINI_API_KEY=AIzaSyBh2WrdSXTMW6Mrc0ZGz75sWOsgeP3GMa4
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   ```

## Step 4: Start the Server

```bash
python app.py
```

You should see:
```
✓ Initialized base system prompt
✓ Initialized base editor prompt
 * Running on http://0.0.0.0:5001
```

## Step 5: Test the API

In another terminal:

```bash
python test_api.py
```

Or test manually:

```bash
curl http://localhost:5001/health
```

## Step 6: Load Training Data (Optional)

If you have a `conversations.json` file:

```bash
python load_conversations.py conversations.json
```

## Troubleshooting

### "SUPABASE_URL and SUPABASE_ANON_KEY must be set"
- Make sure `.env` file exists in the project root
- Check that variable names match exactly (no typos)
- Restart the server after creating/editing `.env`

### "Table does not exist"
- Make sure you ran `init_supabase.sql` in Supabase SQL Editor
- Check that tables were created: Go to Table Editor in Supabase

### "Error generating reply with Gemini"
- Check that GEMINI_API_KEY is correct
- Verify internet connection
- Check Gemini API quota/limits

### Port already in use
- Change `FLASK_PORT` in `.env` to a different port (e.g., 5001)
- Or kill the process using port 5001

