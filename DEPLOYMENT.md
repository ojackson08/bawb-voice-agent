# BAWB Voice Chatbot — Production Deployment Guide

## Recommended: Railway (Fastest & Easiest)

### Step 1: Prepare Your Project
The folder `bawb-voice-agent` is already production-ready with:
- `requirements.txt`
- `Procfile`
- `railway.json`
- `.env.example`

### Step 2: Deploy to Railway (Two Options)

#### Option A: Deploy via GitHub (Recommended)
1. Create a new GitHub repo called `bawb-voice-agent`
2. Push this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial BAWB Voice Agent"
   git remote add origin https://github.com/YOUR_USERNAME/bawb-voice-agent.git
   git branch -M main
   git push -u origin main
   ```
3. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
4. Select the repo
5. Add environment variable:
   - `XAI_API_KEY` = your xAI API key

#### Option B: Deploy Directly from Folder (No Git)
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from current directory (or upload zip)
3. Add the same `XAI_API_KEY` variable

### Step 3: Get Your Production URL
Railway will give you a URL like:
```
https://bawb-voice-agent-production.up.railway.app
```

### Step 4: Update Frontend (index.html)
Open `frontend/index.html` and change this line:

```js
const BAWB_CONFIG = {
    backendUrl: "https://bawb-voice-agent-production.up.railway.app",  // ← Update this
    voiceEnabled: true,
    fallbackToSpeechSynthesis: true
};
```

### Step 5: Upload to Namecheap
You will upload the updated `index.html` to:
`https://merkabacreatives.org/BAWB/`

---

## Alternative: Render.com

1. Go to [render.com](https://render.com)
2. New Web Service → Connect GitHub repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn agent:app --host 0.0.0.0 --port $PORT`
5. Add environment variable `XAI_API_KEY`

---

## Environment Variables Required

| Variable       | Required | Description                  |
|----------------|----------|------------------------------|
| `XAI_API_KEY`  | Yes      | Your xAI Grok API key        |

---

## Verification Checklist

- [ ] Backend deployed and returns 200 on `/`
- [ ] `XAI_API_KEY` is set in the hosting platform
- [ ] Frontend `BAWB_CONFIG.backendUrl` points to production URL
- [ ] Voice mode connects successfully in browser
- [ ] Fallback to speech synthesis works if connection fails

---

## Need Help?

The voice agent is designed to be low-maintenance. Once deployed, it should run stably on Railway/Render.