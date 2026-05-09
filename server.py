"""
SK PRO 4.2 - SERVER (CLEAN REBUILD)
Complete API backend with proper client registration + heartbeat
"""

import time
import sqlite3
import os
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uvicorn

# ════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR")
USER_API_KEY = os.getenv("USER_API_KEY", "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV")
DB_PATH = os.getenv("DB_PATH", "/tmp/skpro.db")
PORT = int(os.getenv("PORT", 8080))  # Railway uses 8080
HEARTBEAT_TIMEOUT = 30  # Mark offline after 30s no heartbeat

app = FastAPI()

# ════════════════════════════════════════════════════════════════════
# DATABASE
# ════════════════════════════════════════════════════════════════════

def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Users table (from Users Management)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'Client',
            is_active INTEGER DEFAULT 1,
            created_at REAL,
            last_login REAL,
            allowed_pages TEXT,
            expiry_date TEXT
        )
    """)
    
    # Active clients table (from client registration + heartbeat)
    c.execute("""
        CREATE TABLE IF NOT EXISTS active_clients (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            device_name TEXT,
            status TEXT DEFAULT 'online',
            registered_at REAL,
            last_seen REAL,
            current_page TEXT,
            current_activity TEXT
        )
    """)
    
    # Screenshots table
    c.execute("""
        CREATE TABLE IF NOT EXISTS screenshots (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            timestamp REAL,
            image_data BLOB
        )
    """)
    
    # Commands table
    c.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            command TEXT,
            args TEXT,
            status TEXT DEFAULT 'pending',
            created_at REAL
        )
    """)
    
    conn.commit()
    conn.close()
    print("[DB] Database initialized")

init_db()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ════════════════════════════════════════════════════════════════════
# MODELS
# ════════════════════════════════════════════════════════════════════

class ClientRegisterRequest(BaseModel):
    username: str
    device_name: str = "Client"

class ClientHeartbeatRequest(BaseModel):
    username: str
    page: str = ""
    activity: str = ""
    timestamp: float

class ScreenshotRequest(BaseModel):
    username: str
    image_base64: str
    timestamp: float

# ════════════════════════════════════════════════════════════════════
# ADMIN ENDPOINTS
# ════════════════════════════════════════════════════════════════════

@app.get("/api/admin/test")
async def test_admin_connection(auth=Header(None, alias="x-api-key")):
    """Test admin connection"""
    print(f"[ADMIN_TEST] Request from admin")
    
    if auth != ADMIN_API_KEY:
        print(f"[ADMIN_TEST] ❌ AUTH FAILED")
        raise HTTPException(status_code=401, detail="Invalid admin API key")
    
    print(f"[ADMIN_TEST] ✅ AUTHENTICATED")
    return {
        "ok": True,
        "role": "admin",
        "status": "connected",
        "server": "SK PRO v4.2",
        "timestamp": time.time()
    }

@app.get("/api/admin/clients")
async def get_active_clients(auth=Header(None, alias="x-api-key")):
    """Get all active clients (Live Monitor)"""
    print(f"[ADMIN_CLIENTS] Request from admin")
    
    if auth != ADMIN_API_KEY:
        print(f"[ADMIN_CLIENTS] ❌ AUTH FAILED")
        raise HTTPException(status_code=401, detail="Invalid admin API key")
    
    try:
        conn = get_db()
        
        # Mark offline if heartbeat timeout
        timeout_threshold = time.time() - HEARTBEAT_TIMEOUT
        print(f"[ADMIN_CLIENTS] Checking timeouts (threshold: {HEARTBEAT_TIMEOUT}s ago)")
        
        conn.execute("""
            UPDATE active_clients SET status = 'offline'
            WHERE last_seen < ? AND status = 'online'
        """, (timeout_threshold,))
        
        rows = conn.execute("""
            SELECT username, status, device_name, registered_at, last_seen, 
                   current_page, current_activity
            FROM active_clients ORDER BY last_seen DESC
        """).fetchall()
        
        conn.commit()
        conn.close()
        
        clients = []
        for row in rows:
            clients.append({
                "username": row[0],
                "status": row[1],
                "device_name": row[2],
                "registered_at": row[3],
                "last_seen": row[4],
                "page": row[5] or "-",
                "activity": row[6] or "-",
                "session_duration": time.time() - row[4] if row[4] else 0
            })
        
        print(f"[ADMIN_CLIENTS] ✅ Returning {len(clients)} clients")
        for c in clients:
            status_emoji = "🟢" if c["status"] == "online" else "🔴"
            print(f"  {status_emoji} {c['username']}: {c['status']}")
        
        return {"ok": True, "clients": clients}
    
    except Exception as e:
        print(f"[ADMIN_CLIENTS] ❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/screenshot/{username}")
async def get_latest_screenshot(username: str, auth=Header(None, alias="x-api-key")):
    """Get latest screenshot from client"""
    if auth != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin API key")
    
    try:
        conn = get_db()
        row = conn.execute("""
            SELECT image_data, timestamp FROM screenshots
            WHERE username = ? ORDER BY timestamp DESC LIMIT 1
        """, (username,)).fetchone()
        conn.close()
        
        if row:
            return {
                "ok": True,
                "image_base64": row[0].decode() if isinstance(row[0], bytes) else row[0],
                "timestamp": row[1]
            }
        else:
            raise HTTPException(status_code=404, detail="No screenshot found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ════════════════════════════════════════════════════════════════════
# CLIENT ENDPOINTS
# ════════════════════════════════════════════════════════════════════

@app.get("/api/user/test")
async def test_user_connection(auth=Header(None, alias="x-api-key")):
    """Test user connection"""
    print(f"[USER_TEST] Request from client")
    
    if auth != USER_API_KEY:
        print(f"[USER_TEST] ❌ AUTH FAILED")
        raise HTTPException(status_code=401, detail="Invalid user API key")
    
    print(f"[USER_TEST] ✅ AUTHENTICATED")
    return {
        "ok": True,
        "role": "user",
        "status": "connected",
        "server": "SK PRO v4.2",
        "timestamp": time.time()
    }

@app.post("/api/client/register")
async def client_register(req: ClientRegisterRequest, auth=Header(None, alias="x-api-key")):
    """Client registers itself on startup"""
    print(f"[REGISTER] Client registering: {req.username}")
    
    if auth != USER_API_KEY:
        print(f"[REGISTER] ❌ AUTH FAILED for {req.username}")
        raise HTTPException(status_code=401, detail="Invalid user API key")
    
    try:
        conn = get_db()
        
        # Register/update client
        conn.execute("""
            INSERT OR REPLACE INTO active_clients 
            (username, device_name, status, registered_at, last_seen)
            VALUES (?, ?, ?, ?, ?)
        """, (req.username, req.device_name, "online", time.time(), time.time()))
        
        conn.commit()
        conn.close()
        
        print(f"[REGISTER] ✅ Client {req.username} REGISTERED as ONLINE")
        return {"ok": True, "status": "registered", "client_id": 1}
    
    except Exception as e:
        print(f"[REGISTER] ❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/client/heartbeat")
async def client_heartbeat(req: ClientHeartbeatRequest, auth=Header(None, alias="x-api-key")):
    """Client sends heartbeat (keep-alive + status update)"""
    print(f"[HEARTBEAT] From {req.username} - Page: {req.page}, Activity: {req.activity}")
    
    if auth != USER_API_KEY:
        print(f"[HEARTBEAT] ❌ AUTH FAILED for {req.username}")
        raise HTTPException(status_code=401, detail="Invalid user API key")
    
    try:
        conn = get_db()
        
        # Update client status
        conn.execute("""
            UPDATE active_clients 
            SET last_seen = ?, status = 'online', current_page = ?, current_activity = ?
            WHERE username = ?
        """, (req.timestamp, req.page, req.activity, req.username))
        
        conn.commit()
        conn.close()
        
        print(f"[HEARTBEAT] ✅ Updated {req.username} - ONLINE")
        return {"ok": True, "status": "heartbeat_received"}
    
    except Exception as e:
        print(f"[HEARTBEAT] ❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/client/screenshot")
async def client_upload_screenshot(req: ScreenshotRequest, auth=Header(None, alias="x-api-key")):
    """Client uploads screenshot"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user API key")
    
    try:
        conn = get_db()
        image_data = req.image_base64.encode() if isinstance(req.image_base64, str) else req.image_base64
        
        conn.execute("""
            INSERT INTO screenshots (username, timestamp, image_data)
            VALUES (?, ?, ?)
        """, (req.username, req.timestamp, image_data))
        
        conn.commit()
        conn.close()
        
        return {"ok": True, "screenshot_id": 1}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/commands")
async def get_commands(username: str, auth=Header(None, alias="x-api-key")):
    """Get pending commands for client"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user API key")
    
    try:
        conn = get_db()
        rows = conn.execute("""
            SELECT id, command, args FROM commands
            WHERE username = ? AND status = 'pending'
        """, (username,)).fetchall()
        conn.close()
        
        return {
            "ok": True,
            "commands": [{"id": r[0], "command": r[1], "args": r[2]} for r in rows]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/user/command-ack")
async def ack_command(cmd_id: int, auth=Header(None, alias="x-api-key")):
    """Client acknowledges command execution"""
    if auth != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user API key")
    
    try:
        conn = get_db()
        conn.execute("UPDATE commands SET status = 'executed' WHERE id = ?", (cmd_id,))
        conn.commit()
        conn.close()
        
        return {"ok": True, "command_acknowledged": cmd_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": time.time()}

# ════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("="*80)
    print("SK PRO 4.2 SERVER STARTING")
    print(f"Database: {DB_PATH}")
    print(f"Port: {PORT}")
    print(f"Admin Key: {ADMIN_API_KEY[:20]}...")
    print(f"User Key: {USER_API_KEY[:20]}...")
    print("="*80)
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)

