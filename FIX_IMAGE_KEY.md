# Fix: Image Data Key Mismatch - Backend Response

## Problem

Photos window showed "No image data" for all screenshots, even though the files were successfully uploaded and stored on the server.

## Root Cause

**Key name mismatch between Backend and Panel:**

### Backend Response (WRONG):
```json
{
  "screenshots": [
    {
      "filename": "order_0000_...",
      "image": "base64_encoded_data"  // ❌ WRONG KEY
    }
  ]
}
```

### Panel Expected (CORRECT):
```json
{
  "screenshots": [
    {
      "filename": "order_0000_...",
      "image_base64": "base64_encoded_data"  // ✅ CORRECT KEY
    }
  ]
}
```

### Panel Code (line 554):
```python
image_data = screenshot.get('image_base64', '')  # Looks for 'image_base64'
```

**Result:**
- Backend sends: `"image": "..."`
- Panel looks for: `"image_base64"`
- Panel finds: nothing (empty string)
- Panel displays: "No image data"

## Solution

Changed the key name in Backend's `/api/screenshots/{client_id}` endpoint:

### Before (WRONG):
```python
screenshots.append({
    "filename": filename,
    "image": image_data  # ❌ WRONG
})
```

### After (CORRECT):
```python
screenshots.append({
    "filename": filename,
    "image_base64": image_data  # ✅ CORRECT
})
```

## Files Modified

- `main_backend_v4.py` - Line 337: Changed `"image"` to `"image_base64"`

## Testing

1. Push Backend to Railway
2. Wait for deployment (1-2 minutes)
3. Run Client EXE
4. Wait for screenshots to upload
5. Open Admin Panel
6. Double-click client
7. Photos should now display correctly ✅

## Expected Result

- ✅ Photo filenames displayed (green text)
- ✅ Actual images shown (thumbnails)
- ✅ Delete buttons visible
- ✅ No "No image data" errors

## Deployment

1. Push to GitHub:
   ```bash
   git add main_backend_v4.py FIX_IMAGE_KEY.md
   git commit -m "Fix: Image data key mismatch - change 'image' to 'image_base64'"
   git push origin main
   ```

2. Railway auto-deploys (wait 1-2 minutes)

3. Test with Panel:
   - Double-click client
   - Photos should appear

## Status

✅ Fixed and ready for deployment

## Notes

- This was a simple key name mismatch
- Backend was encoding images correctly
- Panel was looking for the wrong key name
- Now both use the same key: `image_base64`
