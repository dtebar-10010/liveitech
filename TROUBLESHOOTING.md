# Image Display Troubleshooting - Quick Reference

## Local Testing (Before Deployment)

### 1. Test with Production Settings Locally
```powershell
# In your local project directory
lit-venv\Scripts\activate

# Temporarily set DEBUG=False in .env
# DEBUG=False

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver

# Visit http://127.0.0.1:8000/ and check if images display
# If they display locally with DEBUG=False, they should work on PythonAnywhere
```

### 2. Verify Image Files Exist
```powershell
# Check if media files are present
dir media\hero
dir media\services
dir media\partners
dir media\portfolio
dir media\footer
```

### 3. Check Database Has Image References
```powershell
python manage.py shell
```
```python
# In Django shell
from lit_app.models import HeroSection, ServicesSection, ServiceItem
hero = HeroSection.objects.filter(is_active=True).first()
print(f"Hero logo: {hero.logo_image.url}")  # Should print: /media/hero/filename.png
print(f"Hero bg: {hero.background_image.url}")

services = ServiceItem.objects.all()
for service in services:
    if service.image:
        print(f"{service.title}: {service.image.url}")
```

---

## PythonAnywhere Troubleshooting

### 1. Verify Static Files Mapping (Critical!)
**Go to PythonAnywhere Web tab → Static files section**

Ensure these mappings exist:
```
URL: /static/
Directory: /home/yourusername/liveitech/staticfiles/

URL: /media/
Directory: /home/yourusername/liveitech/media/
```

**Important:** 
- URLs must have leading AND trailing slashes: `/media/`
- Directories must have trailing slashes: `/home/yourusername/liveitech/media/`
- Paths must be absolute (starting with `/home/`)

### 2. Check File Permissions
```bash
# In PythonAnywhere Bash console
cd /home/yourusername/liveitech

# Check and fix permissions
chmod -R 755 media/
chmod -R 755 staticfiles/

# Verify files are readable
ls -la media/hero/
ls -la media/services/
```

### 3. Test Media URLs Directly
Open these URLs in your browser (replace `yourusername`):
```
https://yourusername.pythonanywhere.com/media/hero/logo-large-light-2.png
https://yourusername.pythonanywhere.com/media/hero/city-network-tech.jpg
```

**Expected Results:**
- ✅ **200 OK**: Image displays → Media serving works!
- ❌ **404 Not Found**: Check static files mapping
- ❌ **403 Forbidden**: Check file permissions
- ❌ **500 Error**: Check error logs

### 4. Check Django Configuration
```bash
# In PythonAnywhere Bash console
cd /home/yourusername/liveitech
source lit-venv/bin/activate
python manage.py shell
```

```python
# In Django shell
from django.conf import settings
print("DEBUG:", settings.DEBUG)  # Should be False
print("MEDIA_URL:", settings.MEDIA_URL)  # Should be /media/
print("MEDIA_ROOT:", settings.MEDIA_ROOT)  # Should be full path
print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)  # Should include your domain

# Check if files exist
import os
print("\nMedia directory exists:", os.path.exists(settings.MEDIA_ROOT))
print("Media files:")
for root, dirs, files in os.walk(settings.MEDIA_ROOT):
    for file in files:
        print(os.path.join(root, file))
```

### 5. Check Database Image Paths
```python
# Still in Django shell
from lit_app.models import HeroSection, ServiceItem, PartnerItem
hero = HeroSection.objects.filter(is_active=True).first()
if hero:
    print("Hero logo URL:", hero.logo_image.url)
    print("Hero logo path:", hero.logo_image.path)
    print("File exists:", os.path.exists(hero.logo_image.path))
```

### 6. View Error Logs
```bash
# In PythonAnywhere Bash console
tail -50 /var/log/yourusername.pythonanywhere.com.error.log
tail -50 /var/log/yourusername.pythonanywhere.com.server.log
```

Look for:
- 404 errors on `/media/` URLs
- Permission denied errors
- Import errors (missing WhiteNoise)

### 7. Check Browser Console
1. Open your site in Chrome/Firefox
2. Press F12 to open Developer Tools
3. Go to Network tab
4. Reload page (Ctrl+R)
5. Look for red/failed requests
6. Click on failed image requests to see:
   - Request URL (should be `https://yourusername.pythonanywhere.com/media/...`)
   - Status code (404, 403, etc.)
   - Response details

---

## Common Issues and Quick Fixes

### Issue: All Images Show Broken Icon
**Cause:** Static files mapping not configured

**Fix:**
1. Go to PythonAnywhere Web tab
2. Scroll to "Static files" section
3. Add mapping: URL `/media/` → Directory `/home/yourusername/liveitech/media/`
4. Click ✓ to save
5. Reload web app

### Issue: Some Images Display, Others Don't
**Cause:** Files missing or wrong paths in database

**Fix:**
```bash
# Check which files exist
ls -la /home/yourusername/liveitech/media/hero/
ls -la /home/yourusername/liveitech/media/services/
```

**Option 1:** Re-upload missing images via admin:
- Login to `/admin/`
- Edit the section
- Upload image again

**Option 2:** Copy files from local:
```bash
# On your local machine (Windows)
scp -r media/* yourusername@ssh.pythonanywhere.com:/home/yourusername/liveitech/media/
```

### Issue: Images Work in Admin, But Not on Site
**Cause:** WhiteNoise not installed or configured

**Fix:**
```bash
# In PythonAnywhere Bash console
source lit-venv/bin/activate
pip install whitenoise==6.8.2
```

Then verify `settings.py` has WhiteNoise in MIDDLEWARE (should be done already).

Reload web app.

### Issue: Fresh Install, No Images at All
**Cause:** Need to populate database and upload images

**Fix:**
1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Populate content: `python manage.py populate_content` (if available)
4. Login to admin and upload images manually

### Issue: 403 Forbidden on Media Files
**Cause:** File permissions too restrictive

**Fix:**
```bash
chmod -R 755 /home/yourusername/liveitech/media/
```

### Issue: Changes Not Appearing
**Cause:** Forgot to reload web app

**Fix:**
1. Go to PythonAnywhere Web tab
2. Click green "Reload yourusername.pythonanywhere.com" button
3. Wait 30 seconds
4. Hard refresh browser (Ctrl+Shift+R)

---

## Quick Diagnostic Script

Create this file to run all checks at once:

```python
# Save as check_media.py in project root
import os
from django.conf import settings
from lit_app.models import HeroSection, ServiceItem, PartnerItem, FooterSection

def check_media():
    print("=" * 60)
    print("LIVE i TECH - Media Files Diagnostic")
    print("=" * 60)
    
    # 1. Settings
    print("\n1. Django Settings:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"   MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}")
    
    # 2. Check WhiteNoise
    print("\n2. WhiteNoise Check:")
    has_whitenoise = 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE
    print(f"   WhiteNoise configured: {has_whitenoise}")
    
    # 3. Database models with images
    print("\n3. Database Image References:")
    
    hero = HeroSection.objects.filter(is_active=True).first()
    if hero:
        print(f"   Hero logo: {hero.logo_image.url}")
        print(f"   Hero logo exists: {os.path.exists(hero.logo_image.path)}")
        print(f"   Hero bg: {hero.background_image.url}")
        print(f"   Hero bg exists: {os.path.exists(hero.background_image.path)}")
    
    services = ServiceItem.objects.filter(is_active=True)[:3]
    print(f"\n   Services with images: {services.count()}")
    for service in services:
        if service.image:
            exists = os.path.exists(service.image.path)
            status = "✓" if exists else "✗"
            print(f"   {status} {service.title}: {service.image.url}")
    
    partners = PartnerItem.objects.filter(is_active=True)[:3]
    print(f"\n   Partners with logos: {partners.count()}")
    for partner in partners:
        if partner.logo:
            exists = os.path.exists(partner.logo.path)
            status = "✓" if exists else "✗"
            print(f"   {status} {partner.name}: {partner.logo.url}")
    
    # 4. Media directory structure
    print("\n4. Media Directory Structure:")
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        level = root.replace(str(settings.MEDIA_ROOT), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Show first 5 files per directory
            print(f'{subindent}{file}')
        if len(files) > 5:
            print(f'{subindent}... and {len(files) - 5} more files')
    
    print("\n" + "=" * 60)
    print("Diagnostic Complete!")
    print("=" * 60)

if __name__ == "__main__":
    check_media()
```

Run it:
```bash
# On PythonAnywhere
python check_media.py

# Or via manage.py
python manage.py shell < check_media.py
```

---

## Post-Fix Verification Checklist

After applying fixes, verify:

- [ ] Static files mapping configured in PythonAnywhere Web tab
- [ ] WhiteNoise installed: `pip list | grep whitenoise`
- [ ] Media files exist: `ls media/hero/`
- [ ] File permissions correct: `ls -la media/`
- [ ] Direct URL test works: `/media/hero/filename.png`
- [ ] Django shell shows correct paths
- [ ] Error logs are clear (no 404s on media files)
- [ ] Browser console shows no failed image requests
- [ ] Web app reloaded after changes
- [ ] Hard refresh browser (Ctrl+Shift+R)

---

## Need More Help?

### Collect Information:
1. Screenshot of PythonAnywhere Static files section
2. Output of: `ls -la /home/yourusername/liveitech/media/`
3. Error log contents: Last 50 lines
4. Browser console Network tab screenshot
5. Output of Django shell commands above

### Contact Support:
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Django Discord: https://discord.gg/xcRH6mN4fa
- Stack Overflow: Tag with `django`, `pythonanywhere`, `static-files`

---

## Success Indicators

Your images are working correctly when:

✅ Homepage displays hero background and logo  
✅ Services section shows service icons/images  
✅ Partners section displays partner logos  
✅ Portfolio section shows project images  
✅ Footer displays footer logo  
✅ Browser console (F12) shows no 404 errors  
✅ Direct media URLs are accessible  
✅ Admin interface displays uploaded images  

**All images should load within 2-3 seconds on good connection.**
