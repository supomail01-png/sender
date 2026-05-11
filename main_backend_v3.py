#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ProjectSender Backend v3
خادم متقدم مع دعم إنشاء EXE مخصص والإعدادات المتعددة
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import uuid
import time
import json
import os
from datetime import datetime
from pathlib import Path
import base64
import zipfile
import shutil

# ==================== التكوين ====================

ADMIN_API_KEY = "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR"
USER_API_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"
DATA_DIR = "data"
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
COMMANDS_FILE = os.path.join(DATA_DIR, "commands.json")
SCREENSHOTS_DIR = os.path.join(DATA_DIR, "screenshots")
CONFIGS_DIR = os.path.join(DATA_DIR, "configs")
EXES_DIR = os.path.join(DATA_DIR, "exes")

# إنشاء المجلدات
Path(DATA_DIR).mkdir(exist_ok=True)
Path(SCREENSHOTS_DIR).mkdir(exist_ok=True)
Path(CONFIGS_DIR).mkdir(exist_ok=True)
Path(EXES_DIR).mkdir(exist_ok=True)

# ==================== نماذج البيانات ====================

class ClientRegister(BaseModel):
    client_id: str
    computer: str
    status: str = "online"

class ClientHeartbeat(BaseModel):
    client_id: str
    status: str
    task: str = "idle"
    photos_count: int = 0
    target_url: Optional[str] = None

class CaptureConfig(BaseModel):
    client_id: str
    target_url: str
    photo_count: int = 50
    delay: float = 1.0
    name_slug: Optional[str] = None

class ScreenshotUpload(BaseModel):
    client_id: str
    filename: str
    image_base64: str
    timestamp: float

class CommandRequest(BaseModel):
    client_id: str
    command: str
    target_url: Optional[str] = None
    photo_count: int = 50

class PageConfig(BaseModel):
    name: str
    photo_count: int

class ExeGenerationRequest(BaseModel):
    pages: List[PageConfig]
    exe_name: str = "ProjectSender_Client"

class ExeConfig(BaseModel):
    """إعدادات EXE المخصص"""
    pages: List[Dict]  # [{"name": "orders", "photo_count": 50}, ...]
    created_at: str
    exe_id: str

# ==================== دوال مساعدة ====================

def extract_display_name(url):
    """استخراج أول مسار من URL"""
    try:
        from urllib.parse import urlparse
        import re
        
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        if not path:
            return "site"
        
        segments = path.split("/")
        first_segment = segments[0]
        
        first_segment = re.sub(r'[^a-zA-Z0-9_-]', '_', first_segment)
        
        if not first_segment:
            return "site"
        
        return first_segment
    except:
        return "site"

# ==================== إدارة البيانات ====================

def load_clients():
    """تحميل بيانات العملاء"""
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_clients(clients):
    """حفظ بيانات العملاء"""
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)

def load_commands():
    """تحميل الأوامر"""
    if os.path.exists(COMMANDS_FILE):
        with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_commands(commands):
    """حفظ الأوامر"""
    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=2, ensure_ascii=False)

def load_exe_config(exe_id):
    """تحميل إعدادات EXE"""
    config_file = os.path.join(CONFIGS_DIR, f"{exe_id}.json")
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_exe_config(exe_id, config):
    """حفظ إعدادات EXE"""
    config_file = os.path.join(CONFIGS_DIR, f"{exe_id}.json")
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# ==================== التحقق من المفاتيح ====================

def verify_admin_key(x_api_key: str = Header(None)):
    """التحقق من مفتاح Admin"""
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid admin key")
    return x_api_key

def verify_user_key(x_api_key: str = Header(None)):
    """التحقق من مفتاح User"""
    if x_api_key != USER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid user key")
    return x_api_key

# ==================== تطبيق FastAPI ====================

app = FastAPI(title="ProjectSender Backend v3")

# ==================== Endpoints ====================

@app.get("/health")
async def health():
    """فحص صحة الخادم"""
    return {"status": "ok", "version": "3.0"}

# ==================== عمليات العملاء ====================

@app.post("/api/register")
async def register_client(data: ClientRegister, key: str = Depends(verify_user_key)):
    """تسجيل عميل جديد"""
    clients = load_clients()
    
    client_id = data.client_id or str(uuid.uuid4())
    clients[client_id] = {
        "client_id": client_id,
        "computer": data.computer,
        "status": "online",
        "task": "idle",
        "target_url": None,
        "display_name": None,
        "photo_count": 0,
        "delay": 1.0,
        "screenshots_count": 0,
        "last_seen": datetime.now().isoformat(),
        "registered_at": datetime.now().isoformat()
    }
    
    save_clients(clients)
    return {"client_id": client_id, "status": "registered"}

@app.post("/api/heartbeat")
async def heartbeat(data: ClientHeartbeat, key: str = Depends(verify_user_key)):
    """نبض العميل"""
    clients = load_clients()
    
    if data.client_id not in clients:
        clients[data.client_id] = {
            "client_id": data.client_id,
            "computer": "Unknown",
            "status": "online",
            "task": "idle",
            "target_url": None,
            "display_name": None,
            "photo_count": 0,
            "delay": 1.0,
            "screenshots_count": 0,
            "last_seen": datetime.now().isoformat()
        }
    
    clients[data.client_id]["status"] = data.status
    clients[data.client_id]["task"] = data.task
    clients[data.client_id]["photos_count"] = data.photos_count
    clients[data.client_id]["last_seen"] = datetime.now().isoformat()
    
    if data.target_url:
        clients[data.client_id]["target_url"] = data.target_url
        clients[data.client_id]["display_name"] = extract_display_name(data.target_url)
    
    save_clients(clients)
    
    # الحصول على الأمر التالي
    commands = load_commands()
    command = commands.get(data.client_id, {"command": "idle"})
    
    return {
        "status": "ok",
        "command": command.get("command", "idle"),
        "target_url": command.get("target_url"),
        "photo_count": command.get("photo_count", 50),
        "delay": command.get("delay", 1.0)
    }

@app.get("/api/clients")
async def get_clients(key: str = Depends(verify_admin_key)):
    """الحصول على قائمة العملاء"""
    clients = load_clients()
    return {"clients": clients}

# ==================== عمليات الصور ====================

@app.post("/api/upload_screenshot")
async def upload_screenshot(data: ScreenshotUpload, key: str = Depends(verify_user_key)):
    """رفع صورة"""
    try:
        clients = load_clients()
        if data.client_id not in clients:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # فك تشفير الصورة
        image_data = base64.b64decode(data.image_base64)
        
        # إنشاء مجلد العميل
        client_dir = os.path.join(SCREENSHOTS_DIR, data.client_id)
        Path(client_dir).mkdir(exist_ok=True)
        
        # حفظ الصورة
        file_path = os.path.join(client_dir, data.filename)
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        # تحديث عدد الصور
        clients[data.client_id]["screenshots_count"] = len(os.listdir(client_dir))
        save_clients(clients)
        
        return {"status": "ok", "filename": data.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screenshots/{client_id}")
async def get_screenshots(client_id: str, key: str = Depends(verify_admin_key)):
    """الحصول على الصور"""
    try:
        client_dir = os.path.join(SCREENSHOTS_DIR, client_id)
        
        if not os.path.exists(client_dir):
            return {"screenshots": []}
        
        screenshots = []
        for filename in sorted(os.listdir(client_dir))[:10]:  # أول 10 صور
            file_path = os.path.join(client_dir, filename)
            with open(file_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            screenshots.append({
                "filename": filename,
                "image": image_data
            })
        
        return {"screenshots": screenshots}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== عمليات الأوامر ====================

@app.post("/api/set_config")
async def set_config(data: CaptureConfig, key: str = Depends(verify_admin_key)):
    """تعيين إعدادات الالتقاط"""
    commands = load_commands()
    
    commands[data.client_id] = {
        "command": "capture",
        "target_url": data.target_url,
        "photo_count": data.photo_count,
        "delay": data.delay,
        "name_slug": data.name_slug or extract_display_name(data.target_url)
    }
    
    save_commands(commands)
    return {"status": "ok"}

@app.post("/api/start")
async def start_capture(data: CommandRequest, key: str = Depends(verify_admin_key)):
    """بدء الالتقاط"""
    commands = load_commands()
    
    commands[data.client_id] = {
        "command": "start",
        "target_url": data.target_url,
        "photo_count": data.photo_count,
        "delay": 1.0
    }
    
    save_commands(commands)
    return {"status": "started"}

@app.post("/api/stop")
async def stop_capture(data: CommandRequest, key: str = Depends(verify_admin_key)):
    """إيقاف الالتقاط"""
    commands = load_commands()
    
    commands[data.client_id] = {
        "command": "stop"
    }
    
    save_commands(commands)
    return {"status": "stopped"}

@app.get("/api/get_command/{client_id}")
async def get_command(client_id: str, key: str = Depends(verify_user_key)):
    """الحصول على الأمر"""
    commands = load_commands()
    command = commands.get(client_id, {"command": "idle"})
    return command

@app.post("/api/task_completed")
async def task_completed(data: CommandRequest, key: str = Depends(verify_user_key)):
    """إكمال المهمة"""
    commands = load_commands()
    
    if data.client_id in commands:
        del commands[data.client_id]
    
    save_commands(commands)
    return {"status": "ok"}

# ==================== عمليات إنشاء EXE ====================

@app.post("/api/generate_exe")
async def generate_exe(request: ExeGenerationRequest, key: str = Depends(verify_admin_key)):
    """إنشاء EXE مخصص"""
    try:
        exe_id = str(uuid.uuid4())[:8]
        
        # حفظ الإعدادات
        exe_config = {
            "exe_id": exe_id,
            "pages": [{"name": p.name, "photo_count": p.photo_count} for p in request.pages],
            "created_at": datetime.now().isoformat(),
            "exe_name": request.exe_name
        }
        
        save_exe_config(exe_id, exe_config)
        
        return {
            "status": "ok",
            "exe_id": exe_id,
            "message": f"EXE configuration saved. ID: {exe_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/exe_config/{exe_id}")
async def get_exe_config(exe_id: str, key: str = Depends(verify_user_key)):
    """الحصول على إعدادات EXE"""
    config = load_exe_config(exe_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="EXE config not found")
    
    return config

@app.get("/api/exe_configs")
async def list_exe_configs(key: str = Depends(verify_admin_key)):
    """قائمة جميع إعدادات EXE"""
    configs = []
    
    for filename in os.listdir(CONFIGS_DIR):
        if filename.endswith(".json"):
            exe_id = filename.replace(".json", "")
            config = load_exe_config(exe_id)
            if config:
                configs.append(config)
    
    return {"configs": configs}

# ==================== تشغيل الخادم ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
