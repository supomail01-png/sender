# FIX NOTES

Patched server.py for Railway/local API on port 8080:

- Fixed Authorization / X-API-Key header detection.
- Added CORS so panel/API calls do not fail from external frontends.
- Fixed create-user route with JSON payload.
- Added alias routes used by the panel: /api/users, /users, /admin/users, /api/admin/users/create, etc.
- Added safe Live Monitor endpoint: /api/admin/live and /api/admin/monitor.
- Users list now merges online client heartbeat info into the table.
- Kept port 8080 in Dockerfile, railway.json, and server.py.

Safety note: remote-control/screenshot/command execution actions are not implemented here. Users + Live Monitor + API status are implemented for legitimate administration/status tracking.
