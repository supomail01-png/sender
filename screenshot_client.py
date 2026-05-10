import os, time, uuid, socket, platform, threading, base64, webbrowser
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
from io import BytesIO
import requests
from PIL import ImageGrab

CONFIG_FILE = "client_config.json"
DEFAULT_SERVER = "https://sender-production-32bc.up.railway.app"
DEFAULT_USER_KEY = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"

def load_cfg():
    import json
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    cid = str(uuid.uuid4())
    cfg = {"server_url": DEFAULT_SERVER, "user_api_key": DEFAULT_USER_KEY, "client_id": cid}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return cfg

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Client")
        self.root.geometry("760x560")
        self.cfg = load_cfg()
        self.server = self.cfg["server_url"].rstrip("/")
        self.key = self.cfg["user_api_key"]
        self.client_id = self.cfg["client_id"]
        self.stop_flag = False
        self.capturing = False
        self.current_url = ""
        self.count = 0
        self.build_ui()
        threading.Thread(target=self.loop, daemon=True).start()

    def build_ui(self):
        self.root.configure(bg="#11162b")
        tk.Label(self.root, text="📸 ProjectSender Screenshot Client", bg="#11162b", fg="#00e5ff", font=("Arial", 16, "bold")).pack(anchor="w", padx=18, pady=12)
        self.status = tk.Label(self.root, text="Connecting...", bg="#11162b", fg="orange", font=("Arial", 11, "bold"))
        self.status.pack(anchor="w", padx=18)
        info = f"Client ID: {self.client_id}\nComputer: {socket.gethostname()}\nServer: {self.server}"
        tk.Label(self.root, text=info, bg="#26304d", fg="white", justify="left", anchor="w").pack(fill="x", padx=18, pady=12)
        self.logbox = ScrolledText(self.root, bg="#26304d", fg="white", height=18)
        self.logbox.pack(fill="both", expand=True, padx=18, pady=8)

    def ui_log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.logbox.insert("end", f"[{ts}] {msg}\n")
        self.logbox.see("end")

    def api(self, method, path, json=None, timeout=10):
        h = {"X-API-Key": self.key}
        url = self.server + path
        r = requests.request(method, url, headers=h, json=json, timeout=timeout)
        r.raise_for_status()
        return r.json()

    def send_log(self, msg, level="info"):
        try:
            self.api("POST", "/api/logs", {"client_id": self.client_id, "level": level, "message": msg}, timeout=5)
        except Exception:
            pass

    def register(self):
        data = {
            "client_id": self.client_id,
            "computer": socket.gethostname(),
            "os": platform.platform(),
            "ip": "",
            "app": "screenshot_client"
        }
        res = self.api("POST", "/api/register", data)
        self.status.config(text="● Registered / Online", fg="#00ff88")
        self.ui_log("registered successfully")
        return res

    def heartbeat(self):
        return self.api("POST", "/api/heartbeat", {
            "client_id": self.client_id,
            "status": "online",
            "current_url": self.current_url,
            "screenshots_count": self.count,
            "current_task": "capturing" if self.capturing else "idle"
        })

    def upload_shot(self, path, target_url):
        img = ImageGrab.grab()
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        Path(path).write_bytes(buf.getvalue())
        self.api("POST", "/api/screenshot", {
            "client_id": self.client_id,
            "filename": os.path.basename(path),
            "image_base64": b64,
            "target_url": target_url
        }, timeout=20)

    def capture_job(self, cfg):
        if self.capturing:
            return
        self.capturing = True
        self.stop_flag = False
        target = cfg.get("target_url", "https://example.com")
        total = int(cfg.get("photo_count", 10))
        delay = float(cfg.get("delay", 2.0))
        self.current_url = target
        folder = Path("screenshots") / self.client_id
        folder.mkdir(parents=True, exist_ok=True)
        self.ui_log(f"capture started: {target}")
        self.send_log(f"capture started: {target}", "ok")
        try:
            webbrowser.open(target)
            time.sleep(3)
            for i in range(1, total + 1):
                if self.stop_flag:
                    break
                fname = folder / f"photo_{i:04d}.png"
                self.upload_shot(str(fname), target)
                self.count += 1
                self.ui_log(f"photo saved: {fname}")
                time.sleep(delay)
        except Exception as e:
            self.ui_log(f"capture error: {e}")
            self.send_log(f"capture error: {e}", "error")
        finally:
            self.capturing = False
            self.stop_flag = False
            self.send_log("capture finished/stopped", "ok")
            self.ui_log("capture finished/stopped")

    def loop(self):
        registered = False
        while True:
            try:
                if not registered:
                    self.register()
                    registered = True
                res = self.heartbeat()
                cmd = res.get("command", "idle")
                cfg = res.get("config", {})
                if cmd == "start" and not self.capturing:
                    self.api("POST", "/api/clear_command", {"client_id": self.client_id})
                    threading.Thread(target=self.capture_job, args=(cfg,), daemon=True).start()
                elif cmd == "stop":
                    self.stop_flag = True
                    self.api("POST", "/api/clear_command", {"client_id": self.client_id})
                    self.ui_log("stop command received")
                time.sleep(5)
            except Exception as e:
                registered = False
                self.status.config(text=f"● Register failed: {e}", fg="#ff4444")
                self.ui_log("register failed, retrying...")
                time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    ClientApp(root)
    root.mainloop()
