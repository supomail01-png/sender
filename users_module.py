"""
═══════════════════════════════════════════════════════════════════
🔐 USERS MANAGEMENT MODULE — Integrated with ProjectSender
═══════════════════════════════════════════════════════════════════
هذا الملف يحتوي على نظام إدارة المستخدمين الكامل
يتم استيراده في ProjectSender.py
"""

import sqlite3
import json
import bcrypt
import pyotp
import qrcode
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

# استيراد PIL بشكل آمن
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ═══════════════════════════════════════════════════════════════════
# 🗄️ DATABASE MANAGER
# ═══════════════════════════════════════════════════════════════════

class UsersDatabase:
    """إدارة قاعدة بيانات المستخدمين"""
    
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """تهيئة قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                permissions TEXT DEFAULT '[]',
                two_fa_secret TEXT,
                two_fa_enabled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username, email, password, role='user', permissions=None):
        """إضافة مستخدم جديد"""
        if permissions is None:
            permissions = []
        
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, permissions)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, role, json.dumps(permissions)))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            self.log_action(user_id, 'USER_CREATED', f'تم إنشاء المستخدم {username}')
            return True, user_id
        except sqlite3.IntegrityError:
            return False, "المستخدم أو البريد الإلكتروني موجود بالفعل"
        except Exception as e:
            return False, str(e)
    
    def verify_password(self, username, password):
        """التحقق من كلمة المرور"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, is_active, locked_until FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False, "المستخدم غير موجود"
        
        user_id, password_hash, is_active, locked_until = result
        
        if locked_until:
            locked_time = datetime.fromisoformat(locked_until)
            if datetime.now() < locked_time:
                return False, "الحساب مقفول مؤقتاً"
        
        if not is_active:
            return False, "الحساب معطل"
        
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            self.reset_failed_attempts(user_id)
            self.log_action(user_id, 'LOGIN_SUCCESS', 'تسجيل دخول ناجح')
            return True, user_id
        else:
            self.increment_failed_attempts(user_id)
            return False, "كلمة المرور غير صحيحة"
    
    def increment_failed_attempts(self, user_id):
        """زيادة محاولات الفشل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT failed_attempts FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result:
            failed_attempts = result[0] + 1
            
            if failed_attempts >= 5:
                locked_until = datetime.now() + timedelta(minutes=15)
                cursor.execute('''
                    UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?
                ''', (failed_attempts, locked_until.isoformat(), user_id))
            else:
                cursor.execute('UPDATE users SET failed_attempts = ? WHERE id = ?', (failed_attempts, user_id))
            
            conn.commit()
        
        conn.close()
    
    def reset_failed_attempts(self, user_id):
        """إعادة تعيين محاولات الفشل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def get_user(self, user_id):
        """الحصول على بيانات المستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, role, is_active, created_at, last_login FROM users')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def update_user(self, user_id, **kwargs):
        """تحديث بيانات المستخدم"""
        allowed_fields = ['email', 'role', 'permissions', 'is_active']
        
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False
        
        set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE users SET {set_clause} WHERE id = ?', values)
        conn.commit()
        conn.close()
        
        return True
    
    def delete_user(self, user_id):
        """حذف مستخدم"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        self.log_action(None, 'USER_DELETED', f'تم حذف المستخدم {user_id}')
    
    def change_password(self, user_id, new_password):
        """تغيير كلمة المرور"""
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
        conn.commit()
        conn.close()
        
        self.log_action(user_id, 'PASSWORD_CHANGED', 'تم تغيير كلمة المرور')
    
    def enable_2fa(self, user_id):
        """تفعيل المصادقة الثنائية"""
        secret = pyotp.random_base32()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET two_fa_secret = ?, two_fa_enabled = 1 WHERE id = ?', (secret, user_id))
        conn.commit()
        conn.close()
        
        self.log_action(user_id, '2FA_ENABLED', 'تم تفعيل المصادقة الثنائية')
        return secret
    
    def verify_2fa(self, user_id, token):
        """التحقق من رمز المصادقة الثنائية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT two_fa_secret FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        secret = result[0]
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    def log_action(self, user_id, action, details):
        """تسجيل الإجراء"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_logs (user_id, action, details)
            VALUES (?, ?, ?)
        ''', (user_id, action, details))
        conn.commit()
        conn.close()
    
    def get_audit_logs(self, limit=100):
        """الحصول على سجلات التدقيق"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT users.username, audit_logs.action, audit_logs.details, audit_logs.timestamp
            FROM audit_logs
            LEFT JOIN users ON audit_logs.user_id = users.id
            ORDER BY audit_logs.timestamp DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        return results


# ═══════════════════════════════════════════════════════════════════
# 🎨 USERS MANAGEMENT TAB
# ═══════════════════════════════════════════════════════════════════

class UsersManagementTab(tk.Frame):
    """تاب إدارة المستخدمين"""
    
    def __init__(self, parent, log_func=None):
        super().__init__(parent, bg="#1a1a2e")
        self.log_func = log_func
        self.db = UsersDatabase()
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """إعداد الأنماط"""
        self.bg_dark = "#1a1a2e"
        self.bg_darker = "#0f3460"
        self.accent_blue = "#00d4ff"
        self.accent_green = "#00ff88"
        self.accent_red = "#ff0055"
        self.text_light = "#e0e0e0"
    
    def create_widgets(self):
        """إنشاء الواجهة"""
        # Header
        header = tk.Frame(self, bg=self.bg_dark)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(header, text="👥 إدارة المستخدمين", bg=self.bg_dark, 
                        fg=self.accent_blue, font=('Arial', 14, 'bold'))
        title.pack(side=tk.LEFT)
        
        refresh_btn = tk.Button(header, text="🔄 تحديث", command=self.refresh_users,
                               bg=self.bg_darker, fg=self.text_light, relief="flat")
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        add_btn = tk.Button(header, text="➕ إضافة مستخدم", command=self.show_add_user_dialog,
                           bg=self.bg_darker, fg=self.text_light, relief="flat")
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Main content
        main_frame = tk.Frame(self, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Users List
        self.create_users_tab()
        
        # Tab 2: Permissions
        self.create_permissions_tab()
        
        # Tab 3: Audit Logs
        self.create_audit_tab()
    
    def create_users_tab(self):
        """إنشاء تاب قائمة المستخدمين"""
        frame = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(frame, text="👥 المستخدمون")
        
        # Tableau des utilisateurs
        columns = ('اسم المستخدم', 'البريد الإلكتروني', 'الدور', 'الحالة', 'تاريخ الإنشاء', 'آخر دخول')
        self.users_tree = ttk.Treeview(frame, columns=columns, height=20, show='headings')
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        self.users_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_tree.configure(yscroll=scrollbar.set)
        
        # Buttons
        button_frame = tk.Frame(frame, bg=self.bg_dark)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="✏️ تعديل", command=self.edit_user,
                 bg=self.bg_darker, fg=self.text_light, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔑 تغيير كلمة المرور", command=self.change_password,
                 bg=self.bg_darker, fg=self.text_light, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔐 تفعيل 2FA", command=self.enable_2fa,
                 bg=self.bg_darker, fg=self.text_light, relief="flat").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ حذف", command=self.delete_user,
                 bg=self.bg_darker, fg=self.text_light, relief="flat").pack(side=tk.LEFT, padx=5)
        
        self.refresh_users()
    
    def create_permissions_tab(self):
        """إنشاء تاب الصلاحيات"""
        frame = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(frame, text="🔐 الصلاحيات")
        
        info_label = tk.Label(frame, text="إدارة الصلاحيات والأدوار", bg=self.bg_dark,
                             fg=self.text_light, font=('Arial', 10))
        info_label.pack(padx=10, pady=10)
        
        # Tableau
        columns = ('اسم المستخدم', 'الدور', 'الصلاحيات')
        self.perms_tree = ttk.Treeview(frame, columns=columns, height=20, show='headings')
        
        for col in columns:
            self.perms_tree.heading(col, text=col)
            self.perms_tree.column(col, width=250)
        
        self.perms_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.refresh_permissions()
    
    def create_audit_tab(self):
        """إنشاء تاب سجلات التدقيق"""
        frame = tk.Frame(self.notebook, bg=self.bg_dark)
        self.notebook.add(frame, text="📋 سجلات التدقيق")
        
        columns = ('المستخدم', 'الإجراء', 'التفاصيل', 'الوقت')
        self.logs_tree = ttk.Treeview(frame, columns=columns, height=20, show='headings')
        
        for col in columns:
            self.logs_tree.heading(col, text=col)
            self.logs_tree.column(col, width=200)
        
        self.logs_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.logs_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.logs_tree.configure(yscroll=scrollbar.set)
        
        self.refresh_audit_logs()
    
    def refresh_users(self):
        """تحديث قائمة المستخدمين"""
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        users = self.db.get_all_users()
        for user in users:
            user_id, username, email, role, is_active, created_at, last_login = user
            status = "✅ نشط" if is_active else "❌ معطل"
            self.users_tree.insert('', tk.END, values=(username, email, role, status, created_at[:10], last_login or "لم يدخل"))
    
    def refresh_permissions(self):
        """تحديث قائمة الصلاحيات"""
        for item in self.perms_tree.get_children():
            self.perms_tree.delete(item)
        
        users = self.db.get_all_users()
        for user in users:
            user_id, username, email, role, is_active, created_at, last_login = user
            user_data = self.db.get_user(user_id)
            permissions = user_data[5] if user_data else "[]"
            self.perms_tree.insert('', tk.END, values=(username, role, permissions))
    
    def refresh_audit_logs(self):
        """تحديث سجلات التدقيق"""
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)
        
        logs = self.db.get_audit_logs(50)
        for log in logs:
            username, action, details, timestamp = log
            self.logs_tree.insert('', tk.END, values=(username or "نظام", action, details, timestamp[:19]))
    
    def show_add_user_dialog(self):
        """عرض نافذة إضافة مستخدم"""
        dialog = tk.Toplevel(self)
        dialog.title("إضافة مستخدم جديد")
        dialog.geometry("400x350")
        dialog.configure(bg=self.bg_dark)
        
        tk.Label(dialog, text="اسم المستخدم:", bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=5)
        username_entry = tk.Entry(dialog, width=30, bg=self.bg_darker, fg=self.text_light)
        username_entry.pack(padx=10, pady=5)
        
        tk.Label(dialog, text="البريد الإلكتروني:", bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=5)
        email_entry = tk.Entry(dialog, width=30, bg=self.bg_darker, fg=self.text_light)
        email_entry.pack(padx=10, pady=5)
        
        tk.Label(dialog, text="كلمة المرور:", bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=5)
        password_entry = tk.Entry(dialog, width=30, show="*", bg=self.bg_darker, fg=self.text_light)
        password_entry.pack(padx=10, pady=5)
        
        tk.Label(dialog, text="الدور:", bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=5)
        role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(dialog, textvariable=role_var, values=["admin", "user", "moderator"], width=27)
        role_combo.pack(padx=10, pady=5)
        
        def add_user():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            role = role_var.get()
            
            if not all([username, email, password]):
                messagebox.showerror("خطأ", "جميع الحقول مطلوبة")
                return
            
            success, result = self.db.add_user(username, email, password, role)
            if success:
                messagebox.showinfo("نجاح", f"تم إنشاء المستخدم {username} بنجاح!")
                self.refresh_users()
                self.refresh_permissions()
                dialog.destroy()
            else:
                messagebox.showerror("خطأ", str(result))
        
        tk.Button(dialog, text="إنشاء مستخدم", command=add_user,
                 bg=self.accent_green, fg="#000", relief="flat").pack(pady=20)
    
    def edit_user(self):
        """تعديل مستخدم"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر مستخدماً أولاً")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        messagebox.showinfo("معلومة", f"تعديل المستخدم: {username}\n(قريباً)")
    
    def change_password(self):
        """تغيير كلمة المرور"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر مستخدماً أولاً")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        
        dialog = tk.Toplevel(self)
        dialog.title(f"تغيير كلمة المرور - {username}")
        dialog.geometry("300x150")
        dialog.configure(bg=self.bg_dark)
        
        tk.Label(dialog, text="كلمة المرور الجديدة:", bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=5)
        password_entry = tk.Entry(dialog, width=25, show="*", bg=self.bg_darker, fg=self.text_light)
        password_entry.pack(padx=10, pady=5)
        
        def change():
            new_password = password_entry.get()
            if not new_password:
                messagebox.showerror("خطأ", "كلمة المرور لا يمكن أن تكون فارغة")
                return
            
            users = self.db.get_all_users()
            for user in users:
                if user[1] == username:
                    self.db.change_password(user[0], new_password)
                    messagebox.showinfo("نجاح", "تم تغيير كلمة المرور بنجاح!")
                    dialog.destroy()
                    return
        
        tk.Button(dialog, text="تغيير", command=change,
                 bg=self.accent_green, fg="#000", relief="flat").pack(pady=10)
    
    def enable_2fa(self):
        """تفعيل المصادقة الثنائية"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر مستخدماً أولاً")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        
        users = self.db.get_all_users()
        for user in users:
            if user[1] == username:
                user_id = user[0]
                secret = self.db.enable_2fa(user_id)
                
                totp = pyotp.TOTP(secret)
                qr = qrcode.QRCode()
                qr.add_data(totp.provisioning_uri(name=username, issuer_name='SendM9awed'))
                qr.make()
                
                dialog = tk.Toplevel(self)
                dialog.title(f"إعداد 2FA - {username}")
                dialog.geometry("400x500")
                dialog.configure(bg=self.bg_dark)
                
                tk.Label(dialog, text=f"السر: {secret}", bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=10)
                tk.Label(dialog, text="امسح رمز QR هذا باستخدام تطبيق المصادقة:", 
                        bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=5)
                
                # عرض QR code إذا كان PIL متاحاً
                if PIL_OK:
                    try:
                        qr_img = qr.make_image(fill_color="black", back_color="white")
                        qr_img = qr_img.resize((300, 300))
                        qr_photo = ImageTk.PhotoImage(qr_img)
                        
                        label = tk.Label(dialog, image=qr_photo, bg=self.bg_dark)
                        label.image = qr_photo
                        label.pack(padx=10, pady=10)
                    except Exception as e:
                        tk.Label(dialog, text=f"⚠ خطأ في عرض QR: {str(e)}", 
                                bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=10)
                else:
                    tk.Label(dialog, text="⚠ PIL غير متاح - استخدم السر أعلاه مباشرة", 
                            bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=10)
                
                tk.Label(dialog, text="احفظ هذا السر في مكان آمن!", 
                        bg=self.bg_dark, fg=self.text_light).pack(padx=10, pady=10)
                tk.Button(dialog, text="إغلاق", command=dialog.destroy,
                         bg=self.bg_darker, fg=self.text_light, relief="flat").pack(pady=10)
                
                return
    
    def delete_user(self):
        """حذف مستخدم"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر مستخدماً أولاً")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        
        if messagebox.askyesno("تأكيد", f"حذف المستخدم {username}؟"):
            users = self.db.get_all_users()
            for user in users:
                if user[1] == username:
                    self.db.delete_user(user[0])
                    messagebox.showinfo("نجاح", "تم حذف المستخدم بنجاح!")
                    self.refresh_users()
                    self.refresh_permissions()
                    return
