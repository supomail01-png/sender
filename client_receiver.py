#!/usr/bin/env python3
"""
ProjectSender Client - WITH CONTROL COMMAND RECEIVER
"""

import os
import sys
import time
import json
import requests
import threading
from datetime import datetime

# Configuration
API_URL = "{api_url}"
API_KEY = "{api_key}"
CLIENT_NAME = "{client_name}"
HEARTBEAT_INTERVAL = 2

class ControlCommandHandler:
    """Handle remote control commands"""
    
    @staticmethod
    def execute(cmd):
        """Execute control command"""
        try:
            cmd_type = cmd.get("type")
            data = cmd.get("data", {{}})
            
            print(f"[CLIENT] CONTROL RECEIVED: {{cmd_type}} {{data}}")
            
            if cmd_type == "ping_control":
                print("[CLIENT] PING CONTROL RECEIVED")
            
            elif cmd_type == "mouse_move":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                try:
                    import win32api
                    win32api.SetCursorPos((x, y))
                    print(f"[CLIENT] CONTROL EXECUTED: mouse_move ({{x}}, {{y}})")
                except Exception as e:
                    print(f"[CLIENT] ERROR: mouse_move - {{e}}")
            
            elif cmd_type == "mouse_click":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                button = data.get("button", "left")
                try:
                    import win32api
                    import win32con
                    
                    win32api.SetCursorPos((x, y))
                    if button == "left":
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    elif button == "right":
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                    
                    print(f"[CLIENT] CONTROL EXECUTED: mouse_click ({{x}}, {{y}}, {{button}})")
                except Exception as e:
                    print(f"[CLIENT] ERROR: mouse_click - {{e}}")
            
            elif cmd_type == "double_click":
                x = int(data.get("x", 0))
                y = int(data.get("y", 0))
                try:
                    import win32api
                    import win32con
                    
                    win32api.SetCursorPos((x, y))
                    for _ in range(2):
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    
                    print(f"[CLIENT] CONTROL EXECUTED: double_click ({{x}}, {{y}})")
                except Exception as e:
                    print(f"[CLIENT] ERROR: double_click - {{e}}")
            
            elif cmd_type == "key_press":
                key = data.get("key", "")
                try:
                    import pyautogui
                    pyautogui.press(key)
                    print(f"[CLIENT] CONTROL EXECUTED: key_press ({{key}})")
                except Exception as e:
                    print(f"[CLIENT] ERROR: key_press - {{e}}")
            
            elif cmd_type == "hotkey":
                keys = data.get("keys", [])
                try:
                    import pyautogui
                    if len(keys) >= 2:
                        pyautogui.hotkey(*keys)
                        print(f"[CLIENT] CONTROL EXECUTED: hotkey ({{'+'.join(keys)}})")
                except Exception as e:
                    print(f"[CLIENT] ERROR: hotkey - {{e}}")
            
            else:
                print(f"[CLIENT] UNKNOWN COMMAND: {{cmd_type}}")
            
            return {{"status": "ok"}}
        
        except Exception as e:
            print(f"[CLIENT] HANDLER ERROR: {{e}}")
            return {{"status": "error"}}

def poll_control_commands():
    """Poll for control commands from admin"""
    headers = {{"x-api-key": API_KEY}}
    
    while True:
        try:
            # Poll for commands
            resp = requests.post(
                f"{{API_URL}}/client/control/poll/{{CLIENT_NAME}}",
                headers=headers,
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                commands = data.get("commands", [])
                
                for cmd in commands:
                    ControlCommandHandler.execute(cmd)
            
            time.sleep(0.5)
        
        except Exception as e:
            print(f"[CLIENT] POLL ERROR: {{e}}")
            time.sleep(1)

def main():
    """Main client loop"""
    print(f"[CLIENT] Starting - {{CLIENT_NAME}}")
    print(f"[CLIENT] API: {{API_URL}}")
    
    # Start control command polling thread
    control_thread = threading.Thread(target=poll_control_commands, daemon=True)
    control_thread.start()
    
    # Main heartbeat loop
    headers = {{"x-api-key": API_KEY}}
    
    while True:
        try:
            # Send heartbeat
            resp = requests.post(
                f"{{API_URL}}/client/heartbeat/{{CLIENT_NAME}}",
                headers=headers,
                json={{"status": "online"}},
                timeout=5
            )
            
            time.sleep(HEARTBEAT_INTERVAL)
        
        except Exception as e:
            print(f"[CLIENT] HEARTBEAT ERROR: {{e}}")
            time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    main()
