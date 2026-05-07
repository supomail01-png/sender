# 🌐 SK PRO Server — Railway Deployment Guide

## 📋 Ach kayn f had l'folder

```
server/
├── server.py          ← FastAPI backend
├── requirements.txt   ← Python deps
├── railway.json       ← Railway config
├── Dockerfile         ← Backup deployment
└── DEPLOY_GUIDE.md   ← had l'fichier
```

---

## 🚀 KIFASH NDIRO DEPLOY (Railway — FREE)

### Step 1️⃣: Cr3a account f Railway

1. Mchi l: https://railway.app
2. Click "Login" → Login b GitHub (free)
3. Confirm email

### Step 2️⃣: Push code l GitHub

**Option A — b Git CLI:**
```bash
cd server
git init
git add .
git commit -m "Initial SK PRO server"
git branch -M main

# Cr3a repo new f GitHub.com (private)
# Mn ba3d:
git remote add origin https://github.com/USERNAME/skpro-server.git
git push -u origin main
```

**Option B — Upload manual:**
1. Mchi l https://github.com/new
2. Cr3a private repo "skpro-server"
3. Click "Upload files"
4. Drag les 4 fichiers (server.py, requirements.txt, railway.json, Dockerfile)
5. Commit

### Step 3️⃣: Deploy f Railway

1. F Railway dashboard: **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. Khtar repo "skpro-server"
4. Railway ki-y-detect kolchi automatique → ki-bda deployment

### Step 4️⃣: Set environment variables (MUHIM!)

Dial security, khasna n-bdlu API keys default:

1. F Railway project → Click "Variables"
2. Add 2 variables:
   ```
   ADMIN_API_KEY = <gen random string 32+ chars>
   USER_API_KEY  = <gen random string 32+ chars>
   ```

**Generate random keys:**

Python:
```python
import secrets
print("ADMIN:", secrets.token_urlsafe(32))
print("USER: ", secrets.token_urlsafe(32))
```

Wla online: https://www.random.org/strings/?num=2&len=32&digits=on&loweralpha=on&upperalpha=on

Save 2 keys f endroit safe — ghadi nsta3lhom mn 9bel!

### Step 5️⃣: Get your URL

1. F Railway → Settings → "Generate Domain"
2. Ki-3tini URL b7al: `skpro-server-production.up.railway.app`
3. **Test:**
   ```
   https://YOUR-URL.up.railway.app/health
   ```
   Khasso y-return: `{"status": "ok", ...}`

---

## 🔐 SECURITY CHECKLIST

- [ ] Bdl ADMIN_API_KEY mn default
- [ ] Bdl USER_API_KEY mn default
- [ ] Ma t-share-ch had l'keys f code public
- [ ] Repo dyal GitHub khssh ykon **PRIVATE**
- [ ] Backup keys f password manager

---

## 📊 ENDPOINTS (l'documentation)

### User endpoints (b USER_API_KEY):
```
POST /heartbeat              → I'm alive
POST /log                    → Send activity log
GET  /commands/{username}    → Get pending commands
POST /command-ack            → Confirm command done
GET  /check-expiration/{username}  → Check ila expired
```

### Admin endpoints (b ADMIN_API_KEY):
```
GET    /admin/users           → List all users
GET    /admin/logs            → Get logs (filter b user/since)
POST   /admin/extend          → Extend user expiration
POST   /admin/disconnect      → Force disconnect
POST   /admin/block           → Block/unblock user
DELETE /admin/clear-disconnect/{username}
```

---

## 🧪 TEST RAPIDE

```bash
# Replace YOUR_URL + ADMIN_KEY
curl https://YOUR-URL.up.railway.app/health

# List users (admin)
curl -H "x-api-key: YOUR_ADMIN_KEY" \
     https://YOUR-URL.up.railway.app/admin/users

# Send heartbeat (user)
curl -X POST https://YOUR-URL.up.railway.app/heartbeat \
     -H "x-api-key: YOUR_USER_KEY" \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser"}'
```

---

## 💰 RAILWAY PRICING

- **Free tier**: $5 credit/month (kheddam ~500 hours/month — enough l'app sghir)
- Ila bghiti more → $5/month plan

L'app dyalna ki-7tah ~1-2 GB RAM + minimal CPU = environ $2-3/month.

---

## 🐛 TROUBLESHOOTING

### "Build failed"
- Check logs f Railway → Deployments → View logs
- Probably requirements.txt issue

### "Healthcheck failed"
- Server ki-bda walakin endpoint /health ma kheddamch
- Check logs

### "Database errors"
- SQLite ki-stocker f filesystem dyal Railway (NB: volatile!)
- L production a7sen tsta3ml PostgreSQL (ana ndiha lik ila bghiti)

---

## 🔄 UPDATE SERVER

Ila baddati f code:
```bash
git add .
git commit -m "Update"
git push
```

Railway ki-redeploy automatique 🚀
