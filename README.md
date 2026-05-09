# ProjectSender V42 - Complete Remote Control System

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run server (on Windows or Linux):
```bash
python server.py
```

3. Run admin panel (on Windows):
```bash
python panel.py
```

4. Build client EXE (on Windows):
```bash
build_client.bat
```

5. Run client EXE (as Administrator):
```bash
dist\client_receiver.exe
```

## Testing

1. Start server
2. Start admin panel
3. Start client EXE
4. Monitor Live → Remote View
5. Control: ON
6. Click Test Click button
7. Check logs for:
   - [ADMIN] mouse_click sent
   - [SERVER] CONTROL RECEIVED
   - [CLIENT] CONTROL RECEIVED
   - [CLIENT] CONTROL EXECUTED

