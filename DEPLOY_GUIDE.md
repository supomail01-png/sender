# Railway Deployment Guide

## Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Code pushed to GitHub

## Step 1: Prepare Files

Ensure these files are in your GitHub repo:
- `server.py` (API backend)
- `requirements.txt` (dependencies)
- `Dockerfile` (container config)
- `railway.json` (Railway config)
- `server.json` (config file)

**DO NOT include** `Project_Sender_2027_To_2040.py` in Railway deployment.

## Step 2: Connect to Railway

1. Go to https://railway.app
2. Sign in (GitHub auth recommended)
3. Click "Start a New Project"
4. Select "Deploy from GitHub repo"
5. Authorize GitHub access
6. Select your repository
7. Click "Deploy"

Railway auto-detects Dockerfile and deploys automatically.

## Step 3: Configure Environment

In Railway Dashboard:

1. Go to your project
2. Click the environment
3. Go to Variables tab
4. Add:
   ```
   ADMIN_KEY=your_secret_admin_key_12345
   ```
5. Save

## Step 4: Verify Deployment

1. Find your app in Dashboard
2. Copy the public domain URL
3. Test health endpoint:
   ```bash
   curl https://your-app.up.railway.app/health
   ```

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "users_count": 0,
  "clients_online": 0
}
```

## Step 5: Connect Panel to API

In Panel (`Project_Sender_2027_To_2040.py`):

1. Go to Users tab
2. Set Server URL: `https://your-app.up.railway.app`
3. Set Admin Key: `your_secret_admin_key_12345`
4. Click "Test API"
5. Should show 🟢 Connected

## Troubleshooting

### App won't deploy
- Check build logs in Railway
- Verify Dockerfile syntax
- Check requirements.txt

### Health endpoint fails
- App still building (wait 2-3 minutes)
- Check error logs
- Verify environment variables set

### Panel can't connect
- Verify Railway domain is correct
- Verify Admin Key matches
- Check panel logs for errors

## API Test

```bash
# Get users
curl https://your-app.up.railway.app/api/admin/users \
  -H "Authorization: Bearer your_secret_admin_key_12345"

# Create user
curl -X POST https://your-app.up.railway.app/api/admin/create-user \
  -H "Authorization: Bearer your_secret_admin_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "email": "test@example.com",
    "password": "secure123",
    "expiry_days": 30
  }'
```

## Monitoring

Railway Dashboard shows:
- Real-time logs
- CPU/Memory usage
- Network stats
- Request metrics

## Custom Domain

In Railway Settings:
1. Add custom domain
2. Point DNS to Railway
3. SSL auto-configured

---

✅ Deployed! Your API is live! 🚀
