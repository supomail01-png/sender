#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build EXE from Config - Auto Mode
أداة لبناء EXE مخصص يبدأ التقاط الصور تلقائياً
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
import io

# ✅ إصلاح مشكلة ترميز الأحرف على Windows
if sys.platform == 'win32':
    # تعيين ترميز UTF-8 للـ stdout و stderr
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def create_client_script(exe_id, pages, output_dir):
    """إنشاء script العميل المخصص"""
    
    # تحويل الصفحات إلى JSON
    pages_json = json.dumps(pages, ensure_ascii=False, indent=2)
    
    client_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ProjectSender Client - Auto Generated
عميل مخصص تم إنشاؤه تلقائياً
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import json
import os
from datetime import datetime
from PIL import Image, ImageGrab
import time
import uuid
import base64
from pathlib import Path
import io
import sys

# ✅ إصلاح مشكلة ترميز الأحرف على Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# ==================== التكوين ====================

class Config:
    SERVER_URL = "https://web-production-80fa0.up.railway.app"
    USER_API_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"
    EXE_ID = "{exe_id}"
    
    CLIENT_ID = None
    COMPUTER_NAME = None
    
    CONFIG_FILE = "client_config.json"
    
    @staticmethod
    def load():
        if os.path.exists(Config.CONFIG_FILE):
            try:
                with open(Config.CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    Config.SERVER_URL = data.get("server_url", Config.SERVER_URL)
                    Config.USER_API_KEY = data.get("user_key", Config.USER_API_KEY)
                    Config.CLIENT_ID = data.get("client_id", Config.CLIENT_ID)
                    Config.EXE_ID = data.get("exe_id", Config.EXE_ID)
            except:
                pass
    
    @staticmethod
    def save():
        with open(Config.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({{
                "server_url": Config.SERVER_URL,
                "user_key": Config.USER_API_KEY,
                "client_id": Config.CLIENT_ID,
                "exe_id": Config.EXE_ID
            }}, f, indent=2, ensure_ascii=False)

# ==================== الواجهة الرسومية ====================

class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ProjectSender Client")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e1e")
        
        # تحميل الإعدادات
        Config.load()
        
        # متغيرات
        self.pages = {pages_json}
        self.selected_page = None
        self.is_capturing = False
        self.capture_thread = None
        
        # الحصول على معرف الحاسوب
        import socket
        Config.COMPUTER_NAME = socket.gethostname()
        
        # إنشاء معرف العميل إذا لم يكن موجوداً
        if not Config.CLIENT_ID:
            Config.CLIENT_ID = str(uuid.uuid4())
            Config.save()
        
        # إنشاء الواجهة
        self.create_ui()
    
    def create_ui(self):
        """إنشاء الواجهة الرسومية"""
        
        # العنوان
        title_label = tk.Label(
            self.root,
            text="ProjectSender Client",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title_label.pack(pady=10)
        
        # معلومات العميل
        info_frame = tk.Frame(self.root, bg="#2d2d2d")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(info_frame, text=f"Client ID: {{Config.CLIENT_ID[:8]}}", bg="#2d2d2d", fg="#ffffff").pack(anchor=tk.W)
        tk.Label(info_frame, text=f"Computer: {{Config.COMPUTER_NAME}}", bg="#2d2d2d", fg="#ffffff").pack(anchor=tk.W)
        tk.Label(info_frame, text=f"EXE ID: {{Config.EXE_ID}}", bg="#2d2d2d", fg="#ffffff").pack(anchor=tk.W)
        
        # قسم اختيار الصفحة
        pages_frame = tk.LabelFrame(
            self.root,
            text="📄 اختر الصفحة",
            font=("Arial", 10, "bold"),
            bg="#2d2d2d",
            fg="#00ff88",
            padx=10,
            pady=10
        )
        pages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Listbox للصفحات
        self.pages_listbox = tk.Listbox(
            pages_frame,
            bg="#1e1e1e",
            fg="#00ff88",
            font=("Arial", 11),
            height=8
        )
        self.pages_listbox.pack(fill=tk.BOTH, expand=True)
        self.pages_listbox.bind("<<ListboxSelect>>", self.on_page_select)
        
        # تحديث قائمة الصفحات
        self.update_pages_list()
        
        # معلومات الصفحة المختارة
        info_frame2 = tk.Frame(self.root, bg="#2d2d2d")
        info_frame2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(info_frame2, text="Photo Count:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.photo_count_label = tk.Label(info_frame2, text="0", bg="#2d2d2d", fg="#00ff88", font=("Arial", 11, "bold"))
        self.photo_count_label.pack(side=tk.LEFT, padx=5)
        
        # أزرار التحكم
        buttons_frame = tk.Frame(self.root, bg="#1e1e1e")
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = tk.Button(
            buttons_frame,
            text="▶️ Start Capture",
            bg="#00aa00",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.start_capture,
            padx=15,
            pady=10
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            buttons_frame,
            text="⏹️ Stop Capture",
            bg="#ff0000",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.stop_capture,
            padx=15,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # حالة الالتقاط
        self.status_label = tk.Label(
            self.root,
            text="🔴 Ready",
            font=("Arial", 10, "bold"),
            bg="#1e1e1e",
            fg="#ff0000"
        )
        self.status_label.pack(pady=5)
    
    def update_pages_list(self):
        """تحديث قائمة الصفحات"""
        self.pages_listbox.delete(0, tk.END)
        for page in self.pages:
            text = f"{{page['name']}} ({{page['photo_count']}} photos)"
            self.pages_listbox.insert(tk.END, text)
    
    def on_page_select(self, event):
        """عند اختيار صفحة"""
        selection = self.pages_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_page = self.pages[index]
            self.photo_count_label.config(text=str(self.selected_page['photo_count']))
    
    def register_client(self):
        """تسجيل العميل"""
        try:
            headers = {{"X-API-Key": Config.USER_API_KEY}}
            data = {{
                "client_id": Config.CLIENT_ID,
                "computer": Config.COMPUTER_NAME,
                "status": "online"
            }}
            
            response = requests.post(
                f"{{Config.SERVER_URL}}/api/register",
                json=data,
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
        except:
            return False
    
    def send_heartbeat(self):
        """إرسال نبض"""
        try:
            headers = {{"X-API-Key": Config.USER_API_KEY}}
            data = {{
                "client_id": Config.CLIENT_ID,
                "status": "online",
                "task": "capturing" if self.is_capturing else "idle",
                "photos_count": 0
            }}
            
            response = requests.post(
                f"{{Config.SERVER_URL}}/api/heartbeat",
                json=data,
                headers=headers,
                timeout=5
            )
            
            return response.status_code == 200
        except:
            return False
    
    def capture_screenshots(self):
        """التقاط الصور"""
        if not self.selected_page:
            messagebox.showerror("Error", "Please select a page!")
            return
        
        page_name = self.selected_page['name']
        photo_count = self.selected_page['photo_count']
        
        # تسجيل العميل
        self.register_client()
        
        # إنشاء مجلد محلي
        local_dir = f"screenshots_{{page_name}}"
        Path(local_dir).mkdir(exist_ok=True)
        
        self.is_capturing = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🟢 Capturing...", fg="#00ff00")
        
        # بدء خيط الالتقاط
        self.capture_thread = threading.Thread(
            target=self._capture_loop,
            args=(page_name, photo_count, local_dir)
        )
        self.capture_thread.daemon = True
        self.capture_thread.start()
    
    def _capture_loop(self, page_name, photo_count, local_dir):
        """حلقة الالتقاط"""
        try:
            for i in range(photo_count):
                if not self.is_capturing:
                    break
                
                # التقاط الصورة
                screenshot = ImageGrab.grab()
                filename = f"{{page_name}}_{{i+1:03d}}.png"
                
                # حفظ محلياً
                local_path = os.path.join(local_dir, filename)
                screenshot.save(local_path)
                
                # تحويل إلى base64
                with open(local_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                
                # رفع للخادم
                headers = {{"X-API-Key": Config.USER_API_KEY}}
                upload_data = {{
                    "client_id": Config.CLIENT_ID,
                    "filename": filename,
                    "image_base64": image_data,
                    "timestamp": time.time()
                }}
                
                try:
                    requests.post(
                        f"{{Config.SERVER_URL}}/api/upload_screenshot",
                        json=upload_data,
                        headers=headers,
                        timeout=10
                    )
                except:
                    pass
                
                # إرسال نبض
                self.send_heartbeat()
                
                # حذف الملف المحلي
                try:
                    os.remove(local_path)
                except:
                    pass
                
                # الانتظار
                time.sleep(1)
            
            # إرسال إشعار الإكمال
            self.send_heartbeat()
            
            self.is_capturing = False
            self.root.after(0, self._capture_complete)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.is_capturing = False
            self.root.after(0, self._capture_complete)
    
    def _capture_complete(self):
        """عند إكمال الالتقاط"""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="🔴 Ready", fg="#ff0000")
        messagebox.showinfo("Success", "Capture completed!")
    
    def start_capture(self):
        """بدء الالتقاط"""
        self.capture_screenshots()
    
    def stop_capture(self):
        """إيقاف الالتقاط"""
        self.is_capturing = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="🔴 Ready", fg="#ff0000")

# ==================== البرنامج الرئيسي ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientGUI(root)
    root.mainloop()
'''
    
    # حفظ الـ script مع ترميز UTF-8
    client_file = os.path.join(output_dir, "client.py")
    with open(client_file, "w", encoding="utf-8") as f:
        f.write(client_code)
    
    return client_file

def build_exe(exe_id, pages, output_file):
    """بناء EXE من الإعدادات"""
    
    print(f"🔨 Building EXE for ID: {exe_id}")
    print(f"📄 Pages: {[p['name'] for p in pages]}")
    
    # إنشاء مجلد مؤقت
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Temp directory: {temp_dir}")
        
        # إنشاء script العميل
        client_file = create_client_script(exe_id, pages, temp_dir)
        print(f"✅ Client script created: {client_file}")
        
        # نسخ المتطلبات
        requirements = [
            "requests",
            "pillow"
        ]
        
        # بناء EXE باستخدام PyInstaller
        try:
            cmd = [
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--name", f"ProjectSender_Client_{exe_id}",
                "--icon", "NONE",
                "--add-data", f"{client_file}:.",
                client_file
            ]
            
            print(f"🔨 Running: {' '.join(cmd)}")
            
            # ✅ تعيين ترميز UTF-8 للـ subprocess
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            # ✅ استخدام DEVNULL بدلاً من PIPE للتجنب مشاكل الترميز
            kwargs = {
                "cwd": temp_dir,
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
                "env": env
            }
            
            if sys.platform == 'win32':
                import subprocess as sp
                kwargs['creationflags'] = sp.CREATE_NO_WINDOW
            
            result = subprocess.run(cmd, **kwargs)
            
            if result.returncode != 0:
                print(f"❌ Build failed with return code: {result.returncode}")
                return False
            
            # نسخ EXE إلى المكان المطلوب
            exe_source = os.path.join(temp_dir, "dist", f"ProjectSender_Client_{exe_id}.exe")
            if os.path.exists(exe_source):
                shutil.copy(exe_source, output_file)
                print(f"✅ EXE created: {output_file}")
                return True
            else:
                print(f"❌ EXE not found at {exe_source}")
                return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

def main():
    """البرنامج الرئيسي"""
    
    if len(sys.argv) < 2:
        print("Usage: python build_exe_from_config.py <exe_id> [output_file]")
        sys.exit(1)
    
    exe_id = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"ProjectSender_Client_{exe_id}.exe"
    
    # تحميل الإعدادات من الخادم
    print(f"📥 Loading config for EXE ID: {exe_id}")
    
    try:
        headers = {"X-API-Key": "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR"}
        response = requests.get(
            f"https://web-production-80fa0.up.railway.app/api/exe_config/{exe_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to load config: {response.text}")
            sys.exit(1)
        
        config = response.json()
        pages = config.get("pages", [])
        
        print(f"✅ Config loaded: {len(pages)} pages")
        
        # بناء EXE
        if build_exe(exe_id, pages, output_file):
            print(f"🎉 EXE built successfully: {output_file}")
        else:
            print(f"❌ Failed to build EXE")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
