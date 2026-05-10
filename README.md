# ProjectSender Screenshot Admin PRO

## 1) GitHub / Railway API files
Upload these files to GitHub:
- main.py
- requirements.txt
- Procfile
- railway.json

Railway Variables:
- ADMIN_API_KEY
- USER_API_KEY

After deploy, open:
https://YOUR-RAILWAY-URL/health

## 2) Panel
Run:
python panel_screenshot_admin.py

Click **Test + Save API**, then Refresh Now.

## 3) Client
Run:
python screenshot_client.py

The client is visible and shows connection status. It does not hide itself and does not auto-start.

## 4) Build EXE
From the panel click:
Build screenshot.exe

Or run:
pyinstaller --onefile --noconsole --name screenshot_client screenshot_client.py
