#!/usr/bin/env python3
"""
ProjectSender Client - FIXED VERSION
- Proper heartbeat to server
- Real-time user online tracking
- Control command receiver
- Auto offline on disconnect
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
# 🔧 API CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

API_URL = "https://sender-production-32bc.up.railway.app"
API_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"

# Get client name from arg or env
CLIENT_NAME = os.getenv("CLIENT_NAME", "SK_PRO_Client")
HEARTBEAT_INTERVAL = 5  # Send heartbeat every 5 seconds

# ═══════════════════════════════════════════════════════════════════
# 🎮 CONTROL COMMAND HANDLER
# ═══════════════════════════════════════════════════════════════════

class ControlCommandHandler:
    """Handle remote control commands from admin"""
    
    @staticmethod
    def execute(cmd):
        """Execute control command"""
        try:
            cmd_type = cmd.get("type")
            data = cmd.get("data", {})
            
            print(f"[CLIENT] CONTROL: {cmd_type} {data}")
            
            if cmd_type == "ping_control":
                print("[CLIENT] ✓ PING received")
            
            elif cmd_type == "mouse_move":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                try:
                    import pyautogui
                    pyautogui.moveTo(x, y)
                    print(f"[CLIENT] ✓ Mouse moved to ({x}, {y})")
                except Exception as e:
                    print(f"[CLIENT] ✗ Mouse move error: {e}")
            
            elif cmd_type == "mouse_click":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                button = data.get("button", "left")
                try:
                    import pyautogui
                    pyautogui.click(x, y, button=button)
                    print(f"[CLIENT] ✓ Mouse click ({button}) at ({x}, {y})")
                except Exception as e:
                    print(f"[CLIENT] ✗ Mouse click error: {e}")
            
            elif cmd_type == "double_click":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                try:
                    import pyautogui
                    pyautogui.doubleClick(x, y)
                    print(f"[CLIENT] ✓ Double click at ({x}, {y})")
                except Exception as e:
                    print(f"[CLIENT] ✗ Double click error: {e}")
            
            elif cmd_type == "key_press":
                key = data.get("key", "")
                try:
                    import pyautogui
                    pyautogui.press(key)
                    print(f"[CLIENT] ✓ Key pressed: {key}")
                except Exception as e:
                    print(f"[CLIENT] ✗ Key press error: {e}")
            
            elif cmd_type == "hotkey":
                keys = data.get("keys", [])
                try:
                    import pyautogui
                    if len(keys) >= 2:
                        pyautogui.hotkey(*keys)
                        print(f"[CLIENT] ✓ Hotkey: {'+'.join(keys)}")
                except Exception as e:
                    print(f"[CLIENT] ✗ Hotkey error: {e}")
            
            else:
                print(f"[CLIENT] ⚠ Unknown command: {cmd_type}")
            
            return {"status": "ok"}
        
        except Exception as e:
            print(f"[CLIENT] ✗ Handler error: {e}")
            return {"status": "error"}

# ═══════════════════════════════════════════════════════════════════
# 💓 HEARTBEAT - Keep user ONLINE
# ═══════════════════════════════════════════════════════════════════

def send_heartbeat():
    """Send heartbeat to server to keep user ONLINE"""
    headers = {"x-api-key": API_KEY}
    
    while True:
        try:
            # Get system info
            os_info = platform.system() + " " + platform.release()
            
            # Send heartbeat
            resp = requests.post(
                f"{API_URL}/heartbeat",
                headers=headers,
                json={
                    "username": CLIENT_NAME,
                    "os_info": os_info,
                    "current_status": "online"
                },
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                
                # Check if disconnect requested
                if data.get("disconnect_requested"):
                    print("[CLIENT] ⚠ DISCONNECT REQUESTED BY ADMIN")
                    sys.exit(0)
                
                # Check expiry
                if data.get("expires_at"):
                    print(f"[CLIENT] ✓ Heartbeat OK, expires at: {data.get('expires_at')}")
            
            time.sleep(HEARTBEAT_INTERVAL)
        
        except Exception as e:
            print(f"[CLIENT] ✗ Heartbeat error: {e}")
            time.sleep(HEARTBEAT_INTERVAL)

# ═══════════════════════════════════════════════════════════════════
# 🎮 CONTROL POLLING - Receive commands
# ═══════════════════════════════════════════════════════════════════

def poll_control_commands():
    """Poll for control commands from admin"""
    headers = {"x-api-key": API_KEY}
    
    while True:
        try:
            # Poll for commands
            resp = requests.get(
                f"{API_URL}/control/poll/{CLIENT_NAME}",
                headers=headers,
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                events = data.get("events", [])
                
                if events:
                    print(f"[CLIENT] 📨 Received {len(events)} commands")
                    for evt in events:
                        ControlCommandHandler.execute(evt)
            
            time.sleep(0.5)
        
        except Exception as e:
            print(f"[CLIENT] ✗ Poll error: {e}")
            time.sleep(1)

# ═══════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    """Main client loop"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     SK PRO Client - FIXED VERSION                          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"[CLIENT] Name: {CLIENT_NAME}")
    print(f"[CLIENT] API: {API_URL}")
    print(f"[CLIENT] Heartbeat every {HEARTBEAT_INTERVAL} seconds")
    print()
    
    # Start heartbeat thread
    hb_thread = threading.Thread(target=send_heartbeat, daemon=True)
    hb_thread.start()
    print("[CLIENT] ✓ Heartbeat thread started")
    
    # Start control polling thread
    ctrl_thread = threading.Thread(target=poll_control_commands, daemon=True)
    ctrl_thread.start()
    print("[CLIENT] ✓ Control polling thread started")
    
    print()
    print("[CLIENT] ✓ Client ONLINE and ready for commands")
    print("[CLIENT] Press Ctrl+C to exit")
    print()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[CLIENT] ⚠ Shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
