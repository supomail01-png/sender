"""
SK PRO 4.2 - BUILD CLIENT EXE
Creates ClientPanel_{username}.exe for each user
Non-blocking (runs in background thread)
"""

import os
import sys
import subprocess
import threading
import time

def build_exe_for_user(username, server_url, user_api_key, callback=None):
    """
    Build EXE for specific user (non-blocking, runs in background)
    
    Args:
        username: User to build for
        server_url: Server URL (e.g., https://sender-production-32bc.up.railway.app)
        user_api_key: User API key
        callback: Function to call when done (callback(success, message))
    """
    
    def task():
        try:
            print(f"\n{'='*60}")
            print(f"🔨 Building EXE for user: {username}")
            print(f"{'='*60}")
            
            # Check PyInstaller
            try:
                subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
                print("✅ PyInstaller found")
            except:
                print("📦 Installing PyInstaller...")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"], check=True)
            
            # Create launcher script
            launcher_code = f'''
import os
import sys

# Inject environment variables for this user
os.environ['USERNAME'] = {repr(username)}
os.environ['SERVER_URL'] = {repr(server_url)}
os.environ['USER_API_KEY'] = {repr(user_api_key)}

# Import and run client receiver
from client_receiver import main
if __name__ == "__main__":
    main()
'''
            
            launcher_file = f"launcher_{username}.py"
            with open(launcher_file, "w") as f:
                f.write(launcher_code)
            print(f"✅ Created launcher: {launcher_file}")
            
            # Build EXE name
            exe_name = f"ClientPanel_{username}"
            
            # PyInstaller command
            cmd = [
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--name", exe_name,
                "--icon", "app_icon.ico" if os.path.exists("app_icon.ico") else None,
                "--hidden-import=requests",
                "--hidden-import=PIL",
                "--hidden-import=pyautogui",
                "--hidden-import=pyperclip",
                launcher_file
            ]
            
            cmd = [x for x in cmd if x]
            
            print(f"\n🔨 PyInstaller command:")
            print(f"   {' '.join(cmd)}")
            print(f"\n⏳ Building... (this may take 1-2 minutes)")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                exe_path = f"dist/{exe_name}.exe"
                if os.path.exists(exe_path):
                    size_mb = os.path.getsize(exe_path) / (1024*1024)
                    print(f"\n✅ SUCCESS!")
                    print(f"   EXE: {exe_path}")
                    print(f"   Size: {size_mb:.1f} MB")
                    print(f"   User: {username}")
                    print(f"   Server: {server_url}")
                    
                    # Cleanup launcher
                    try:
                        os.remove(launcher_file)
                        os.remove(f"build/{exe_name}/base_library.zip")
                    except:
                        pass
                    
                    if callback:
                        callback(True, f"✅ {exe_name}.exe created successfully!\n\nLocation: {os.path.abspath(exe_path)}")
                    return True
            
            error_msg = result.stderr or "Unknown error"
            print(f"\n❌ BUILD FAILED")
            print(f"   Error: {error_msg[:200]}")
            
            if callback:
                callback(False, f"❌ Build failed\n\n{error_msg[:300]}")
            
            return False
        
        except Exception as e:
            print(f"\n❌ EXCEPTION: {str(e)}")
            if callback:
                callback(False, f"❌ Exception: {str(e)}")
            return False
    
    # Run in background thread (non-blocking)
    thread = threading.Thread(target=task, daemon=True)
    thread.start()
    return thread

def main():
    """Test build"""
    if len(sys.argv) < 2:
        print("Usage: python build_client_exe.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    server_url = "https://sender-production-32bc.up.railway.app"
    user_api_key = "skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV"
    
    def done_callback(success, msg):
        print(f"\n{'='*60}")
        print(msg)
        print(f"{'='*60}")
    
    thread = build_exe_for_user(username, server_url, user_api_key, done_callback)
    thread.join()  # Wait for completion

if __name__ == "__main__":
    main()

