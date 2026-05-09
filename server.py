"""
═══════════════════════════════════════════════════════════════════
🌐 SK PRO — Backend Server (FIXED)
═══════════════════════════════════════════════════════════════════

Features:
✓ User heartbeat tracking (Online/Offline)
✓ Real-time Live Monitor updates
✓ Automatic offline after timeout
✓ Command routing
✓ Screenshot streaming
✓ Remote control (mouse, keyboard, clipboard)
═══════════════════════════════════════════════════════════════════
"""
import os
import time
import sqlite3
import secrets
from datetime import datetime
from typing import Optional, List
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ═══════════════════════════════════════════════════════════════════
# 🔐 API KEYS - FIXED CREDENTIALS
# ═══════════════════════════════════════════════════════════════════

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR")
USER_API_KEY = os.getenv("USER_API_KEY", "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV")

# Heartbeat timeout: user offline after 30 seconds of inactivity
HEARTBEAT_TIMEOUT = 30

# ═══════════════════════════════════════════════════════════════════
# 📦 DATABASE
# ═══════════════════════════════════════════════════════════════════

DB_PATH = os.getenv("DB_PATH", "skpro.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            last_seen INTEGER,
            ip_address TEXT,
            os_info TEXT,
            current_status TEXT,
            expires_at INTEGER,
            blocked INTEGER DEFAULT 0,
            disconnect_requested INTEGER DEFAULT 0,
            created_at INTEGER,
            updated_at INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp INTEGER,
            level TEXT,
            message TEXT,
            details TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_logs_user ON logs(username);
        CREATE INDEX IF NOT EXISTS idx_logs_ts ON logs(timestamp);
        
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            command TEXT,
            params TEXT,
            issued_at INTEGER,
            executed_at INTEGER,
            status TEXT DEFAULT 'pending'
        );
        
        CREATE INDEX IF NOT EXISTS idx_commands_user ON commands(username, status);
        """)

init_db()

# ═══════════════════════════════════════════════════════════════════
# 🚀 FASTAPI APP
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(title="SK PRO Server", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════════
# 🔐 AUTH
# ═══════════════════════════════════════════════════════════════════

def verify_admin_key(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin API key")
    return True

def verify_user_key(x_api_key: str = Header(...)):
    if x_api_key != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user API key")
    return True

# ═══════════════════════════════════════════════════════════════════
# 📊 MODELS
# ═══════════════════════════════════════════════════════════════════

class HeartbeatRequest(BaseModel):
    username: str
    os_info: Optional[str] = ""
    current_status: Optional[str] = "online"

class LogEntry(BaseModel):
    username: str
    level: str = "info"
    message: str
    details: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════
# 💓 USER HEARTBEAT - Keep track of ONLINE status
# ═══════════════════════════════════════════════════════════════════

def get_user_by_name(username: str):
    """Get user info, mark as OFFLINE if timeout"""
    with get_db() as db:
        row = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        
        if not row:
            return None
        
        # Check if offline (no heartbeat for 30 seconds)
        now = int(time.time())
        last_seen = row["last_seen"]
        is_offline = (now - last_seen) > HEARTBEAT_TIMEOUT
        
        return {
            "username": row["username"],
            "last_seen": row["last_seen"],
            "ip_address": row["ip_address"],
            "os_info": row["os_info"],
            "current_status": row["current_status"],
            "online": not is_offline,  # ✨ KEY: Online if heartbeat recent
            "offline_in_seconds": max(0, HEARTBEAT_TIMEOUT - (now - last_seen))
        }

@app.post("/heartbeat")
async def heartbeat(req: HeartbeatRequest, request: Request, _: bool = Depends(verify_user_key)):
    """
    User sends heartbeat to stay ONLINE.
    If no heartbeat for 30 seconds → marked OFFLINE in Live Monitor
    """
    now = int(time.time())
    ip = request.client.host
    
    with get_db() as db:
        # Check if blocked
        row = db.execute("SELECT blocked, disconnect_requested FROM users WHERE username=?",
                         (req.username,)).fetchone()
        
        if row and row["blocked"]:
            raise HTTPException(status_code=403, detail="User blocked by admin")
        
        # Upsert user (update last_seen = NOW)
        db.execute("""
            INSERT INTO users (username, last_seen, ip_address, os_info, current_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
                last_seen=excluded.last_seen,
                ip_address=excluded.ip_address,
                os_info=excluded.os_info,
                current_status=excluded.current_status,
                updated_at=excluded.updated_at
        """, (req.username, now, ip, req.os_info, req.current_status, now, now))
        
        # Return status
        return {
            "ok": True,
            "timestamp": now,
            "disconnect_requested": bool(row["disconnect_requested"]) if row else False,
            "message": f"✓ {req.username} is ONLINE"
        }

# ═══════════════════════════════════════════════════════════════════
# 📡 ADMIN - GET LIVE USERS
# ═══════════════════════════════════════════════════════════════════

@app.get("/admin/users")
async def admin_get_all_users(_: bool = Depends(verify_admin_key)):
    """
    Admin gets LIVE user list.
    Automatically marks users OFFLINE if no heartbeat for 30s.
    """
    with get_db() as db:
        rows = db.execute("SELECT * FROM users ORDER BY last_seen DESC").fetchall()
    
    now = int(time.time())
    users = []
    
    for row in rows:
        # Check if OFFLINE (no heartbeat for 30 seconds)
        time_since_seen = now - row["last_seen"]
        is_online = time_since_seen <= HEARTBEAT_TIMEOUT
        
        users.append({
            "username": row["username"],
            "status": "Online" if is_online else "Offline",
            "online": is_online,
            "last_seen": row["last_seen"],
            "last_seen_ago_seconds": time_since_seen,
            "ip_address": row["ip_address"],
            "os_info": row["os_info"],
            "current_status": row["current_status"],
            "page": row["current_status"],
            "activity": "Active" if is_online else "No heartbeat",
        })
    
    return {
        "users": users,
        "total": len(users),
        "online_count": len([u for u in users if u["online"]]),
        "timestamp": now
    }

@app.get("/admin/users/{username}")
async def admin_get_user(username: str, _: bool = Depends(verify_admin_key)):
    """Get single user info"""
    user = get_user_by_name(username)
    if not user:
        raise HTTPException(404, "User not found")
    return user

# ═══════════════════════════════════════════════════════════════════
# 🎮 CONTROL COMMANDS
# ═══════════════════════════════════════════════════════════════════

CONTROL_EVENTS = {}  # {username: [event1, event2, ...]}

@app.post("/admin/control/{username}")
async def admin_send_control_event(
    username: str,
    request: Request,
    _: bool = Depends(verify_admin_key)
):
    """Admin sends mouse/keyboard control to user"""
    try:
        event = await request.json()
        
        if username not in CONTROL_EVENTS:
            CONTROL_EVENTS[username] = []
        
        event_with_ts = {**event, "timestamp": int(time.time() * 1000)}
        CONTROL_EVENTS[username].append(event_with_ts)
        
        # Limit queue
        if len(CONTROL_EVENTS[username]) > 100:
            CONTROL_EVENTS[username] = CONTROL_EVENTS[username][-50:]
        
        return {"ok": True, "queued": len(CONTROL_EVENTS[username])}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/control/poll/{username}")
async def user_poll_control_events(
    username: str,
    _: bool = Depends(verify_user_key)
):
    """User polls for pending commands"""
    events = CONTROL_EVENTS.get(username, [])
    # Clear after fetch
    CONTROL_EVENTS[username] = []
    return {"events": events}

# ═══════════════════════════════════════════════════════════════════
# 🔧 ADMIN ACTIONS
# ═══════════════════════════════════════════════════════════════════

@app.post("/admin/disconnect/{username}")
async def admin_disconnect_user(
    username: str,
    request: Request,
    _: bool = Depends(verify_admin_key)
):
    """Admin disconnects a user"""
    try:
        data = await request.json()
        reason = data.get("reason", "Admin disconnected")
        
        with get_db() as db:
            db.execute(
                "UPDATE users SET disconnect_requested=1 WHERE username=?",
                (username,)
            )
        
        return {"ok": True, "message": f"User {username} will disconnect", "reason": reason}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/admin/extend/{username}")
async def admin_extend_user_time(
    username: str,
    request: Request,
    _: bool = Depends(verify_admin_key)
):
    """Admin extends user session time"""
    try:
        data = await request.json()
        additional_seconds = int(data.get("additional_seconds", 0))
        
        now = int(time.time())
        expires_at = now + additional_seconds
        
        with get_db() as db:
            db.execute(
                "UPDATE users SET expires_at=? WHERE username=?",
                (expires_at, username)
            )
        
        return {
            "ok": True,
            "message": f"Extended by {additional_seconds} seconds",
            "expires_at": expires_at
        }
    except Exception as e:
        raise HTTPException(400, str(e))

# ═══════════════════════════════════════════════════════════════════
# 🏥 HEALTH CHECKS
# ═══════════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    return {
        "service": "SK PRO Server",
        "version": "2.0",
        "status": "online",
        "timestamp": int(time.time())
    }

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": int(time.time())}

# ═══════════════════════════════════════════════════════════════════
# 🚀 START SERVER
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     SK PRO Server - FIXED VERSION                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"[SERVER] Admin API Key: {ADMIN_API_KEY[:20]}...")
    print(f"[SERVER] User API Key: {USER_API_KEY[:20]}...")
    print(f"[SERVER] Heartbeat timeout: {HEARTBEAT_TIMEOUT} seconds")
    print(f"[SERVER] Starting on port {port}...")
    print()
    
    uvicorn.run("server:app", host="0.0.0.0", port=port, log_level="info")
