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
                   expires_at, blocked, disconnect_requested, created_at
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
