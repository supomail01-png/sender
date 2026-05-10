# ProjectSender API Server

FastAPI backend for ProjectSender admin panel.

## Overview

- **Platform**: FastAPI on Railway
- **Port**: 8080
- **Database**: JSON file (or in-memory)
- **Authentication**: Admin API key
- **Routes**: All routes match panel exactly

## Local Testing

```bash
pip install -r requirements.txt
python server.py
```

Visit: http://localhost:8080/docs

## Railway Deployment

1. Push to GitHub
2. Connect to Railway
3. Railway auto-detects Dockerfile
4. Set env: `ADMIN_KEY=your_secret_key`
5. Deploy!

Server runs on port 8080 (panel expects this port)

## Environment Variables

- `ADMIN_KEY` - Admin API key
- `PORT` - Server port (default 8080)

## Routes

All routes with `/api/admin/` require Admin API key header:
- `Authorization: Bearer YOUR_KEY`
- or `X-API-Key: YOUR_KEY`

### Health
- `GET /health` - Health check
- `GET /` - Root info

### Admin
- `GET /api/admin/test` - Test auth
- `GET /api/admin/users` - List users
- `POST /api/admin/create-user` - Create user
- `POST /api/admin/delete-user` - Delete user
- `POST /api/admin/build` - Generate build

### Client
- `POST /api/client/register` - Client register
- `POST /api/client/heartbeat` - Keep alive
- `GET /api/client/screenshot/{username}` - Screenshot

### User
- `GET /api/user/commands` - Get commands
- `POST /api/user/command-ack` - Acknowledge

## Create User Payload

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secure123",
  "expiry_days": 30,
  "max_devices": 5,
  "is_active": true,
  "role": "user",
  "notes": "Optional notes"
}
```

## Files

- `server.py` - FastAPI application (PORT 8080)
- `requirements.txt` - Dependencies
- `Dockerfile` - Docker config (PORT 8080)
- `railway.json` - Railway config (PORT 8080)
- `server.json` - Runtime config
- `server.json.template` - Config template
- `Project_Sender_2027_To_2040.py` - Panel (local only, NOT deployed)

## Panel Configuration

The panel expects API on port 8080:

```
Server URL: http://localhost:8080 (local)
Server URL: https://your-app.up.railway.app (production)
Admin Key: your_secret_admin_key_12345
```

## Note

The `Project_Sender_2027_To_2040.py` file is the admin panel for local use only. 
Railway runs only `server.py` as an API server on port 8080.

---

Version 1.0.0
Production Ready ✅
Port: 8080
