import os
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ADMIN_KEY = os.getenv("ADMIN_KEY", "skpro_admin_xK9mP3qR")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = []

def check_admin_key(
    authorization: str = None,
    x_api_key: str = None
):
    token = None

    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "").strip()
        else:
            token = authorization.strip()

    if not token and x_api_key:
        token = x_api_key.strip()

    if token != ADMIN_KEY:
        raise HTTPException(
            status_code=401,
            detail={
                "detail": "Unauthorized: invalid admin key",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Project Sender API",
        "port": 8080
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "time": datetime.utcnow().isoformat()
    }

@app.get("/api/admin/test")
def admin_test(
    authorization: str = Header(None),
    x_api_key: str = Header(None)
):
    check_admin_key(authorization, x_api_key)

    return {
        "success": True,
        "message": "Admin authenticated"
    }

@app.get("/api/admin/users")
def get_users(
    authorization: str = Header(None),
    x_api_key: str = Header(None)
):
    check_admin_key(authorization, x_api_key)

    return {
        "success": True,
        "count": len(users_db),
        "users": users_db
    }

@app.post("/api/admin/create-user")
async def create_user(
    request: Request,
    authorization: str = Header(None),
    x_api_key: str = Header(None)
):
    check_admin_key(authorization, x_api_key)

    data = await request.json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="username/password required")

    for u in users_db:
        if u["username"] == username:
            raise HTTPException(status_code=400, detail="User already exists")

    user = {
        "username": username,
        "password": password,
        "expiry_days": data.get("expiry_days", 30),
        "max_devices": data.get("max_devices", 5),
        "is_active": data.get("is_active", True),
        "notes": data.get("notes", ""),
        "created_at": datetime.utcnow().isoformat()
    }

    users_db.append(user)

    return {
        "success": True,
        "message": "User created successfully",
        "user": user
    }

@app.delete("/api/admin/delete-user/{username}")
def delete_user(
    username: str,
    authorization: str = Header(None),
    x_api_key: str = Header(None)
):
    check_admin_key(authorization, x_api_key)

    global users_db

    users_db = [u for u in users_db if u["username"] != username]

    return {
        "success": True,
        "message": f"User {username} deleted"
    }

@app.get("/api/admin/live")
def live_monitor(
    authorization: str = Header(None),
    x_api_key: str = Header(None)
):
    check_admin_key(authorization, x_api_key)

    return {
        "success": True,
        "online_users": [],
        "count": 0
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8080,
        reload=False
    )
