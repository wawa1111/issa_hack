# Deploying to Render

This guide will help you deploy the Visa Consultant AI to Render.

## Prerequisites

1. A GitHub repository with your code
2. A Render account (sign up at https://render.com)
3. Supabase project set up with tables created (run `init_supabase.sql`)

## Deployment Steps

### 1. Push Code to GitHub

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Create New Web Service on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository containing this project

### 3. Configure the Service

Use these exact settings:

#### Basic Settings
- **Name**: `visa-consultant-ai` (or your preferred name)
- **Region**: **Singapore (Southeast Asia)**
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (Render uses repository root)

#### Build & Deploy
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

#### Environment Variables

Add these three environment variables in the Render dashboard:

1. **GEMINI_API_KEY**
   - Value: Your Gemini API key
   - Example: `AIzaSyBh2WrdSXTMW6Mrc0ZGz75sWOsgeP3GMa4`

2. **SUPABASE_URL**
   - Value: Your Supabase project URL
   - Example: `https://xxxxx.supabase.co`

3. **SUPABASE_ANON_KEY**
   - Value: Your Supabase anon/public key
   - Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Optional:**
- **FLASK_DEBUG**: `False` (recommended for production)

**Note:** Render automatically sets the `PORT` environment variable. The app will use this automatically.

### 4. Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your service
3. Monitor the build logs for any issues
4. Once deployed, your service will be available at: `https://your-service-name.onrender.com`

### 5. Verify Deployment

Test the health endpoint:

```bash
curl https://your-service-name.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "service": "visa-consultant-ai"}
```

## Using render.yaml (Alternative Method)

If you prefer, you can use the `render.yaml` file included in this project:

1. In Render dashboard, go to **"New +"** → **"Blueprint"**
2. Connect your GitHub repository
3. Render will automatically detect and use `render.yaml`
4. You'll still need to set the environment variables in the dashboard

## Important Notes

- **No .env file needed**: Render uses environment variables set in the dashboard
- **Port handling**: Render sets `PORT` automatically - the app uses this
- **Database**: Make sure Supabase tables are created before deploying
- **API endpoints**: All endpoints will be available at your Render URL

## Troubleshooting

### Build fails with "Module not found"
- Check that `requirements.txt` includes all dependencies
- Verify Python version compatibility

### "SUPABASE_URL and SUPABASE_ANON_KEY must be set"
- Verify environment variables are set in Render dashboard
- Check variable names match exactly (case-sensitive)
- Redeploy after adding environment variables

### Service crashes on startup
- Check Render logs for error messages
- Verify Supabase connection and table existence
- Ensure Gemini API key is valid

### Health check fails
- Verify the service is running (check status in dashboard)
- Check that port is correctly configured
- Review application logs in Render dashboard

## API Endpoints After Deployment

Once deployed, your endpoints will be:

- `https://your-service.onrender.com/health` - Health check
- `https://your-service.onrender.com/generate-reply` - Generate AI reply
- `https://your-service.onrender.com/improve-ai` - Self-learning endpoint
- `https://your-service.onrender.com/improve-ai-manually` - Manual prompt update
- `https://your-service.onrender.com/parse-conversations` - Parse conversations
- `https://your-service.onrender.com/load-training-data` - Bulk training

## Updating the Service

After making code changes:

1. Push changes to GitHub
2. Render will automatically detect and redeploy
3. Or manually trigger a deploy from the Render dashboard

