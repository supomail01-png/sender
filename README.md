# SK PRO 4.2 - Complete Remote Control Panel

Professional email sender with live monitoring, remote control, and client management.

## Features

- **Users Management**: Create, edit, delete users with expiry dates
- **Build EXE**: Generate client EXE for each user
- **Live Monitor**: Real-time client status from Railway
- **Remote View**: Live screenshots + mouse/keyboard control
- **Client Heartbeat**: Auto-register + keep-alive system
- **Railway Deployment**: Auto-deploy from GitHub

## Quick Start

```bash
# Install requirements
pip install -r requirements.txt

# Run server (local)
python server.py

# Run admin panel (local)
python panel.py

# Or use batch files (Windows)
run_server.bat
run_panel.bat
```

## Deployment

Push to GitHub → Railway auto-deploys from main branch.

### Environment Variables (Railway Settings)
- ADMIN_API_KEY=skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR
- USER_API_KEY=skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV
- PORT=8080

## Repository
https://github.com/supomail01-png/sender

## Version
SK PRO 4.2 - Clean Rebuild
