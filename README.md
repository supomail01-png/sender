# ProjectSender - Complete System v6

نظام متكامل متقدم مع إنشاء EXE مخصص للعملاء

## 🎯 الميزات الرئيسية (v6)

### ✨ نظام إنشاء EXE المخصص

**الآن يمكنك:**

1. **في Admin Panel:**
   - أدخل أسماء الصفحات (orders, confirmation, client)
   - حدد عدد الصور لكل صفحة
   - انقر "Generate EXE"
   - احصل على EXE ID

2. **في Client EXE:**
   - المستخدم يشغل EXE
   - يختار من الصفحات المتاحة
   - ينقر "Start Capture"
   - الصور تظهر في Admin Panel

### 📊 التدفق الجديد

```
Admin Panel
    ↓
أدخل الأسماء والكميات
    ↓
انقر Generate EXE
    ↓
احصل على EXE ID
    ↓
أعطِ EXE ID للعميل
    ↓
Client EXE
    ↓
اختر الصفحة والكمية
    ↓
Start Capture
    ↓
الصور تظهر في Admin Panel
```

## 📦 محتويات الحزمة

```
ProjectSender_v6/
├── main_backend_v3.py              # Backend محدث مع API إنشاء EXE
├── panel_v4_railway.py             # Admin Panel مع تبويب Generate EXE
├── screenshot_client_v2_gui.py     # Client مع واجهة اختيار الأسماء
├── build_exe_from_config.py        # Script لبناء EXE من الإعدادات
├── requirements_complete.txt       # الاعتماديات
└── README.md                       # هذا الملف
```

## 🚀 البدء السريع

### 1. تثبيت المتطلبات

```bash
pip install -r requirements_complete.txt
```

### 2. تشغيل Backend

```bash
python main_backend_v3.py
```

### 3. تشغيل Admin Panel

```bash
python panel_v4_railway.py
```

### 4. إنشاء EXE مخصص

**في Admin Panel:**
1. انتقل إلى تبويب "Generate EXE"
2. أدخل الأسماء والكميات:
   ```
   Page 1: orders (50)
   Page 2: confirmation (100)
   Page 3: client (75)
   ```
3. انقر "Generate EXE"
4. احصل على EXE ID: `abc12345`

### 5. بناء EXE

```bash
python build_exe_from_config.py abc12345 ProjectSender_Client.exe
```

### 6. إعطاء EXE للعميل

- أرسل `ProjectSender_Client.exe` للعميل
- أخبره بـ EXE ID: `abc12345`
- العميل يشغل EXE ويختار الصفحة

## 🔄 مثال الاستخدام الكامل

### الخطوة 1: Admin Panel

```
[Generate EXE Tab]
Page 1: orders (50)
Page 2: confirmation (100)
→ Generate EXE
✅ EXE Created! ID: abc12345
```

### الخطوة 2: بناء EXE

```bash
$ python build_exe_from_config.py abc12345 ProjectSender_Client.exe
🔨 Building EXE for ID: abc12345
📄 Pages: ['orders', 'confirmation']
✅ EXE created: ProjectSender_Client.exe
```

### الخطوة 3: Client يشغل EXE

```
ProjectSender Client
Client ID: xxxx-xxxx
Computer: DESKTOP-ABC
EXE ID: abc12345

📄 اختر الصفحة
[orders (50 photos)]
[confirmation (100 photos)]

▶️ Start Capture
```

### الخطوة 4: Admin Panel يرى الصور

```
[Clients Tab]
🟢 DESKTOP-ABC

📋 معلومات العميل
Client ID: xxxx-xxxx
Display Name: orders
Screenshots: 50

🖼️ معرض الصور
[photo1] [photo2] [photo3] ...
```

## 🔧 الملفات الجديدة

### 1. Backend v3 (`main_backend_v3.py`)

**Endpoints الجديدة:**
- `POST /api/generate_exe` - إنشاء إعدادات EXE
- `GET /api/exe_config/{exe_id}` - الحصول على إعدادات EXE
- `GET /api/exe_configs` - قائمة جميع الإعدادات

**الميزات:**
- ✅ حفظ الإعدادات في JSON
- ✅ دعم عدة صفحات
- ✅ API آمن مع مفاتيح

### 2. Admin Panel v4 (`panel_v4_railway.py`)

**التحديثات:**
- ✅ تبويب جديد "Generate EXE"
- ✅ جدول لإدخال الأسماء والكميات
- ✅ زر "Generate EXE"
- ✅ عرض EXE ID بعد الإنشاء

### 3. Client v2 (`screenshot_client_v2_gui.py`)

**الميزات:**
- ✅ واجهة Tkinter لاختيار الصفحات
- ✅ عرض عدد الصور لكل صفحة
- ✅ التقاط الصور وإرسالها
- ✅ حذف الصور المحلية بعد الرفع

### 4. Build Script (`build_exe_from_config.py`)

**الاستخدام:**
```bash
python build_exe_from_config.py <exe_id> [output_file]
```

**الميزات:**
- ✅ تحميل الإعدادات من الخادم
- ✅ إنشاء script مخصص
- ✅ بناء EXE باستخدام PyInstaller

## 📋 API Endpoints

### إنشاء EXE

```bash
POST /api/generate_exe
Headers: X-API-Key: skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR
Body: {
  "pages": [
    {"name": "orders", "photo_count": 50},
    {"name": "confirmation", "photo_count": 100}
  ],
  "exe_name": "ProjectSender_Client"
}

Response: {
  "status": "ok",
  "exe_id": "abc12345",
  "message": "EXE configuration saved. ID: abc12345"
}
```

### الحصول على إعدادات EXE

```bash
GET /api/exe_config/{exe_id}
Headers: X-API-Key: skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV

Response: {
  "exe_id": "abc12345",
  "pages": [
    {"name": "orders", "photo_count": 50},
    {"name": "confirmation", "photo_count": 100}
  ],
  "created_at": "2026-05-11T12:34:56",
  "exe_name": "ProjectSender_Client"
}
```

## 🔐 الأمان

- ✅ جميع الاتصالات آمنة (HTTPS)
- ✅ استخدام مفاتيح API
- ✅ حفظ الإعدادات محلياً
- ✅ لا يتم إرسال بيانات حساسة

## 📈 الإصدار

- **الإصدار:** 6.0
- **التاريخ:** 2026-05-11
- **الحالة:** جاهز للاستخدام ✅

## 🔗 الروابط

- [Railway](https://railway.app)
- [PyInstaller](https://pyinstaller.org)
- [FastAPI](https://fastapi.tiangolo.com)

## 📝 ملاحظات

- جميع البيانات تُحدّث تلقائياً كل 5 ثوان
- الصور تُعرض بحجم 150x150 بكسل
- يتم عرض أول 10 صور فقط في المعرض
- الإعدادات تُحفظ محلياً على العميل

## 🎯 الخطوات التالية المحتملة

1. **إضافة واجهة ويب:** لإدارة الإعدادات عبر المتصفح
2. **دعم قاعدة بيانات:** لتخزين البيانات بشكل دائم
3. **إضافة تقارير:** لعرض إحصائيات الالتقاط
4. **دعم متعدد اللغات:** لدعم لغات أخرى

---

**نظام متكامل وجاهز للاستخدام الفوري!** 🚀
