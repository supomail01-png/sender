"""
ProjectSender API Server - Production Ready
FastAPI backend matching Project_Sender_2027_To_2040.py panel routes
PORT: 8080
"""

from fastapi import FastAPI, HTTPException, Header, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import os
import hashlib
import uuid
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ProjectSender API",
    description="Admin panel backend for ProjectSender",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# CONFIG & DATABASE
# ═══════════════════════════════════════════════════════════════

CONFIG_FILE = "server.json"
DB_FILE = "data.json"

def load_config():
    """Load server configuration"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            "admin_key": os.environ.get("ADMIN_KEY", "admin_key_12345"),
            "database_url": "memory",
            "max_users": 100,
            "enable_ssl": False
        }

def load_database():
    """Load user database"""
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"users": {}, "clients": {}}

def save_database(db):
    """Save user database"""
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(db, f, indent=2)
    except:
        pass

CONFIG = load_config()
DATABASE = load_database()

# ═══════════════════════════════════════════════════════════════
# MODELS - MATCHING PANEL EXACTLY
# ═══════════════════════════════════════════════════════════════

class User(BaseModel):
    """User creation model - matches panel form exactly
    Email is OPTIONAL because panel doesn't ask for it"""
    username: str
    password: str
    email: Optional[str] = None
    expiry_days: int = Field(default=30, ge=1)
    max_devices: int = Field(default=5, ge=1)
    is_active: bool = True
    notes: Optional[str] = None
    role: str = "user"

class ClientRegister(BaseModel):
    """Client registration"""
    username: str
    user_id: str
    api_key: str
    build_version: str
    machine_name: str

class Heartbeat(BaseModel):
    """Client heartbeat"""
    username: str
    user_id: str
    ip: str
    machine_name: str
    build_version: str
    is_active: bool = True

class Command(BaseModel):
    """User command"""
    command: str
    args: Optional[Dict[str, Any]] = None

class CommandAck(BaseModel):
    """Command acknowledgement"""
    command_id: str
    username: str
    status: str
    result: Optional[str] = None

# ═══════════════════════════════════════════════════════════════
# MIDDLEWARE
# ═══════════════════════════════════════════════════════════════

async def verify_admin_key(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    auth: Optional[str] = Header(None, alias="auth")
):
    """Verify admin API key from Authorization Bearer, X-API-Key, or auth header."""
    admin_key = os.environ.get("ADMIN_KEY") or CONFIG.get('admin_key', 'admin_key_12345')

    candidates = []
    for value in (authorization, x_api_key, auth):
        if not value or not isinstance(value, str):
            continue
        if value.startswith("Bearer "):
            candidates.append(value.split("Bearer ", 1)[1].strip())
        else:
            candidates.append(value.strip())

    if admin_key not in candidates:
        logger.warning("❌ Invalid admin key attempt")
        raise HTTPException(status_code=401, detail="Unauthorized: invalid admin key")

    return admin_key

def _user_public(username: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Return user object formatted for the desktop panel without exposing raw password hash."""
    item = user_data.copy()
    item['username'] = username
    if username in DATABASE.get("clients", {}):
        c = DATABASE["clients"][username]
        item.update({
            "online": True,
            "is_online": True,
            "ip": c.get("ip", item.get("ip")),
            "machine_name": c.get("machine_name", item.get("machine_name")),
            "build_version": c.get("build_version", item.get("build_version")),
            "last_login": c.get("last_heartbeat", item.get("last_login")),
            "last_seen": c.get("last_heartbeat", item.get("last_login")),
            "ping": c.get("ping", item.get("ping", 0)),
        })
    else:
        item.setdefault("online", False)
        item.setdefault("is_online", False)
    item.pop("password", None)
    return item

# ═══════════════════════════════════════════════════════════════
# HEALTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    users_count = len(DATABASE["users"])
    clients_count = len(DATABASE["clients"])
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "users_count": users_count,
        "clients_online": clients_count,
        "api": "ProjectSender API"
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API info"""
    return {
        "name": "ProjectSender API",
        "version": "1.0.0",
        "status": "running",
        "description": "Admin panel backend for ProjectSender",
        "endpoints": {
            "health": "/health",
            "admin": "/api/admin/*",
            "client": "/api/client/*",
            "user": "/api/user/*",
            "docs": "/docs"
        },
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# ADMIN ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/admin/test", tags=["Admin"])
async def admin_test(authorization: Optional[str] = Header(None, alias="Authorization"), x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Test admin authentication"""
    try:
        await verify_admin_key(authorization, x_api_key)
        logger.info("✓ Admin authentication test passed")
        return {
            "status": "authenticated",
            "message": "Admin API key valid",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        logger.warning("❌ Admin test failed: " + str(e.detail))
        raise

@app.get("/api/admin/users", tags=["Admin"])
async def get_users(authorization: Optional[str] = Header(None, alias="Authorization"), x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Get all users"""
    try:
        await verify_admin_key(authorization, x_api_key)
        
        users_list = []
        for username, user_data in DATABASE["users"].items():
            users_list.append(_user_public(username, user_data))
        
        logger.info(f"✓ Retrieved {len(users_list)} users")
        return {
            "users": users_list,
            "count": len(users_list),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        raise

@app.post("/api/admin/create-user", tags=["Admin"])
async def create_user(
    user: User,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Create new user - matches panel form exactly
    Email is optional (panel doesn't ask for it)"""
    try:
        await verify_admin_key(authorization, x_api_key)
        
        # Validate
        if not user.username or not user.password:
            raise HTTPException(status_code=400, detail="Username and password required")
        
        if user.username in DATABASE["users"]:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create user
        user_id = str(uuid.uuid4())
        expiry_date = datetime.now() + timedelta(days=user.expiry_days)
        api_key = str(uuid.uuid4())
        
        DATABASE["users"][user.username] = {
            "user_id": user_id,
            "email": user.email or f"{user.username}@projectsender.local",
            "password": hashlib.sha256(user.password.encode()).hexdigest(),
            "role": user.role,
            "is_active": user.is_active,
            "expiry_date": expiry_date.isoformat(),
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "ip": None,
            "machine_name": None,
            "build_version": None,
            "notes": user.notes or "",
            "api_key": api_key,
            "max_devices": user.max_devices,
            "ping": 0
        }
        
        save_database(DATABASE)
        
        logger.info(f"✓ User created: {user.username}")
        return {
            "status": "created",
            "user_id": user_id,
            "username": user.username,
            "email": DATABASE["users"][user.username]["email"],
            "api_key": api_key,
            "expiry_date": expiry_date.isoformat(),
            "message": "User created successfully",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"❌ User creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/delete-user", tags=["Admin"])
async def delete_user(
    username: Optional[str] = Query(None),
    payload: Optional[Dict[str, Any]] = Body(None),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Delete user"""
    try:
        await verify_admin_key(authorization, x_api_key)
        if not username and payload:
            username = payload.get("username") or payload.get("user")
        if not username:
            raise HTTPException(status_code=400, detail="username required")
        
        if username not in DATABASE["users"]:
            raise HTTPException(status_code=404, detail="User not found")
        
        del DATABASE["users"][username]
        if username in DATABASE["clients"]:
            del DATABASE["clients"][username]
        
        save_database(DATABASE)
        
        logger.info(f"✓ User deleted: {username}")
        return {
            "status": "deleted",
            "username": username,
            "message": "User deleted successfully",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        raise

@app.post("/api/admin/build", tags=["Admin"])
async def create_build(
    username: Optional[str] = Query(None),
    payload: Optional[Dict[str, Any]] = Body(None),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Generate build for user"""
    try:
        await verify_admin_key(authorization, x_api_key)
        if not username and payload:
            username = payload.get("username") or payload.get("user")
        if not username:
            raise HTTPException(status_code=400, detail="username required")
        
        if username not in DATABASE["users"]:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = DATABASE["users"][username]
        
        logger.info(f"✓ Build created for user: {username}")
        return {
            "status": "build_created",
            "username": username,
            "user_id": user.get("user_id"),
            "build_url": f"/builds/{username}/launcher.sh",
            "message": "Build package created",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        raise


@app.get("/api/users", tags=["Admin Alias"])
@app.get("/users", tags=["Admin Alias"])
@app.get("/admin/users", tags=["Admin Alias"])
async def get_users_alias(authorization: Optional[str] = Header(None, alias="Authorization"), x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    return await get_users(authorization, x_api_key)

@app.post("/api/users", tags=["Admin Alias"])
@app.post("/users", tags=["Admin Alias"])
@app.post("/api/admin/users", tags=["Admin Alias"])
@app.post("/api/admin/users/create", tags=["Admin Alias"])
@app.post("/api/auth/register", tags=["Admin Alias"])
async def create_user_alias(user: User, authorization: Optional[str] = Header(None, alias="Authorization"), x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    return await create_user(user, authorization, x_api_key)

@app.get("/api/admin/live", tags=["Admin"])
@app.get("/api/admin/monitor", tags=["Admin"])
async def live_monitor(authorization: Optional[str] = Header(None, alias="Authorization"), x_api_key: Optional[str] = Header(None, alias="X-API-Key")):
    await verify_admin_key(authorization, x_api_key)
    users = [_user_public(u, d) for u, d in DATABASE["users"].items()]
    online = [u for u in users if u.get("online")]
    return {"status":"ok", "users": users, "online": online, "online_count": len(online), "count": len(users), "timestamp": datetime.now().isoformat()}

# ═══════════════════════════════════════════════════════════════
# CLIENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.post("/api/client/register", tags=["Client"])
async def client_register(client: ClientRegister):
    """Client registration"""
    try:
        if client.username not in DATABASE["users"]:
            raise HTTPException(status_code=401, detail="User not found")
        
        user = DATABASE["users"][client.username]
        if user["api_key"] != client.api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        # Register client
        DATABASE["clients"][client.username] = {
            "user_id": client.user_id,
            "ip": "unknown",
            "machine_name": client.machine_name,
            "build_version": client.build_version,
            "registered_at": datetime.now().isoformat(),
            "last_heartbeat": datetime.now().isoformat(),
            "is_active": True
        }
        
        save_database(DATABASE)
        
        logger.info(f"✓ Client registered: {client.username}")
        return {
            "status": "registered",
            "username": client.username,
            "user_id": client.user_id,
            "message": "Client registered successfully",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"❌ Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/client/heartbeat", tags=["Client"])
async def client_heartbeat(hb: Heartbeat):
    """Client heartbeat - keep alive"""
    try:
        if hb.username not in DATABASE["users"]:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Update client status
        DATABASE["clients"][hb.username] = {
            "user_id": hb.user_id,
            "ip": hb.ip,
            "machine_name": hb.machine_name,
            "build_version": hb.build_version,
            "is_active": hb.is_active,
            "last_heartbeat": datetime.now().isoformat()
        }
        
        # Update user in database
        if hb.username in DATABASE["users"]:
            DATABASE["users"][hb.username]["last_login"] = datetime.now().isoformat()
            DATABASE["users"][hb.username]["ip"] = hb.ip
            DATABASE["users"][hb.username]["machine_name"] = hb.machine_name
            DATABASE["users"][hb.username]["build_version"] = hb.build_version
        
        save_database(DATABASE)
        
        logger.info(f"✓ Heartbeat received from: {hb.username}")
        return {
            "status": "heartbeat_received",
            "message": "Keep alive",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"❌ Heartbeat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/client/screenshot/{username}", tags=["Client"])
async def get_screenshot(username: str):
    """Get screenshot from client"""
    if username not in DATABASE["clients"]:
        raise HTTPException(status_code=404, detail="Client not online")
    
    return {
        "status": "screenshot_request",
        "username": username,
        "message": "Screenshot feature - Phase 2",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# USER ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api/user/commands", tags=["User"])
async def get_commands(username: str = ""):
    """Get pending commands for user"""
    if not username or username not in DATABASE["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    commands = []  # TODO: Implement command queue
    
    return {
        "commands": commands,
        "count": len(commands),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/user/command-ack", tags=["User"])
async def command_ack(ack: CommandAck):
    """Acknowledge command execution"""
    if ack.username not in DATABASE["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"✓ Command acknowledged: {ack.command_id} from {ack.username}")
    
    return {
        "status": "acknowledged",
        "command_id": ack.command_id,
        "username": ack.username,
        "message": "Command acknowledged",
        "timestamp": datetime.now().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now().isoformat()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(f"❌ Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.now().isoformat()}
    )

# ═══════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    print("╔════════════════════════════════════════════════════════╗")
    print("║    ProjectSender API Server - Started                 ║")
    print("╠════════════════════════════════════════════════════════╣")
    print(f"✓ Admin Key: {CONFIG.get('admin_key', 'admin_key_12345')[:15]}...")
    print(f"✓ Users: {len(DATABASE['users'])}")
    print(f"✓ Clients Online: {len(DATABASE['clients'])}")
    print("✓ API Docs: /docs")
    print("✓ Health: /health")
    print("✓ Port: 8080")
    print("✓ Email: Optional (auto-generated if missing)")
    print("╚════════════════════════════════════════════════════════╝")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
