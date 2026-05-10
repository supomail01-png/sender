import os, time, uuid, base64
from typing import Dict, Any, List
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR")
USER_API_KEY = os.getenv("USER_API_KEY", "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV")

app = FastAPI(title="ProjectSender Screenshot API PRO")

clients: Dict[str, Dict[str, Any]] = {}
logs: Dict[str, List[Dict[str, Any]]] = {}
screenshots: Dict[str, List[Dict[str, Any]]] = {}

def now():
    return int(time.time())

def check_admin(x_api_key: str | None):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key")

def check_user(x_api_key: str | None):
    if x_api_key != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user key")

class RegisterIn(BaseModel):
    client_id: str | None = None
    computer: str = ""
    os: str = ""
    ip: str = ""
    app: str = "screenshot_client"

class HeartbeatIn(BaseModel):
    client_id: str
    status: str = "online"
    current_url: str = ""
    screenshots_count: int = 0
    current_task: str = "idle"

class ConfigIn(BaseModel):
    client_id: str
    target_url: str
    photo_count: int
    delay: float

class CommandIn(BaseModel):
    client_id: str

class LogIn(BaseModel):
    client_id: str
    level: str = "info"
    message: str

class ShotIn(BaseModel):
    client_id: str
    filename: str
    image_base64: str
    target_url: str = ""

@app.get("/")
def root():
    return {"ok": True, "service": "ProjectSender Screenshot API PRO", "endpoints": ["/health", "/api/clients"]}

@app.get("/health")
def health():
    return {"ok": True, "time": now(), "clients": len(clients)}

@app.post("/api/register")
def register(data: RegisterIn, x_api_key: str | None = Header(default=None)):
    check_user(x_api_key)
    cid = data.client_id or str(uuid.uuid4())
    clients[cid] = clients.get(cid, {})
    clients[cid].update({
        "client_id": cid,
        "computer": data.computer,
        "os": data.os,
        "ip": data.ip,
        "app": data.app,
        "status": "online",
        "current_url": clients[cid].get("current_url", ""),
        "screenshots_count": clients[cid].get("screenshots_count", 0),
        "current_task": clients[cid].get("current_task", "idle"),
        "last_seen": now(),
        "config": clients[cid].get("config", {"target_url": "https://example.com", "photo_count": 10, "delay": 2.0}),
        "command": clients[cid].get("command", "idle")
    })
    logs.setdefault(cid, []).append({"ts": now(), "level": "ok", "message": "client registered"})
    screenshots.setdefault(cid, [])
    return {"ok": True, "client_id": cid, "config": clients[cid]["config"], "command": clients[cid]["command"]}

@app.post("/api/heartbeat")
def heartbeat(data: HeartbeatIn, x_api_key: str | None = Header(default=None)):
    check_user(x_api_key)
    if data.client_id not in clients:
        raise HTTPException(status_code=404, detail="client not registered")
    clients[data.client_id].update(data.model_dump())
    clients[data.client_id]["last_seen"] = now()
    return {"ok": True, "command": clients[data.client_id].get("command", "idle"), "config": clients[data.client_id].get("config", {})}

@app.post("/api/logs")
def add_log(data: LogIn, x_api_key: str | None = Header(default=None)):
    check_user(x_api_key)
    logs.setdefault(data.client_id, []).append({"ts": now(), "level": data.level, "message": data.message})
    logs[data.client_id] = logs[data.client_id][-500:]
    return {"ok": True}

@app.post("/api/screenshot")
def add_screenshot(data: ShotIn, x_api_key: str | None = Header(default=None)):
    check_user(x_api_key)
    arr = screenshots.setdefault(data.client_id, [])
    arr.append({"ts": now(), "filename": data.filename, "image_base64": data.image_base64, "target_url": data.target_url})
    screenshots[data.client_id] = arr[-80:]
    if data.client_id in clients:
        clients[data.client_id]["screenshots_count"] = len(screenshots[data.client_id])
        clients[data.client_id]["current_url"] = data.target_url
        clients[data.client_id]["last_seen"] = now()
    logs.setdefault(data.client_id, []).append({"ts": now(), "level": "ok", "message": f"screenshot saved: {data.filename}"})
    return {"ok": True}

@app.get("/api/clients")
def list_clients(x_api_key: str | None = Header(default=None)):
    check_admin(x_api_key)
    out = []
    t = now()
    for c in clients.values():
        item = dict(c)
        if t - int(item.get("last_seen", 0)) > 30:
            item["status"] = "offline"
        out.append(item)
    return {"ok": True, "clients": out}

@app.get("/api/client/{client_id}")
def get_client(client_id: str, x_api_key: str | None = Header(default=None)):
    check_admin(x_api_key)
    return {"ok": True, "client": clients.get(client_id), "logs": logs.get(client_id, [])[-200:], "screenshots": screenshots.get(client_id, [])[-30:]}

@app.post("/api/set_config")
def set_config(data: ConfigIn, x_api_key: str | None = Header(default=None)):
    check_admin(x_api_key)
    if data.client_id not in clients:
        raise HTTPException(status_code=404, detail="client not found")
    clients[data.client_id]["config"] = {"target_url": data.target_url, "photo_count": data.photo_count, "delay": data.delay}
    logs.setdefault(data.client_id, []).append({"ts": now(), "level": "ok", "message": "config updated by admin"})
    return {"ok": True}

@app.post("/api/start")
def start(data: CommandIn, x_api_key: str | None = Header(default=None)):
    check_admin(x_api_key)
    if data.client_id not in clients:
        raise HTTPException(status_code=404, detail="client not found")
    clients[data.client_id]["command"] = "start"
    logs.setdefault(data.client_id, []).append({"ts": now(), "level": "ok", "message": "start command sent"})
    return {"ok": True}

@app.post("/api/stop")
def stop(data: CommandIn, x_api_key: str | None = Header(default=None)):
    check_admin(x_api_key)
    if data.client_id not in clients:
        raise HTTPException(status_code=404, detail="client not found")
    clients[data.client_id]["command"] = "stop"
    logs.setdefault(data.client_id, []).append({"ts": now(), "level": "ok", "message": "stop command sent"})
    return {"ok": True}

@app.post("/api/clear_command")
def clear_command(data: CommandIn, x_api_key: str | None = Header(default=None)):
    check_user(x_api_key)
    if data.client_id in clients:
        clients[data.client_id]["command"] = "idle"
    return {"ok": True}
