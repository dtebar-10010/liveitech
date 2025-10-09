# PythonAnywhere Deployment Guide for LIVE i TECH

## Issue: Images Not Displaying in Production

### Root Cause
Django's built-in static file serving only works when `DEBUG=True`. In production (DEBUG=False), media files uploaded through the admin interface were not being served.

### Solution Implemented
We've configured WhiteNoise middleware and updated URL patterns to properly serve both static and media files in production.

---

## Pre-Deployment Checklist

### 1. Local Environment Setup
```bash
# Activate virtual environment (Windows)
lit-venv\Scripts\activate

# Install WhiteNoise (if not already installed)
pip install whitenoise==6.8.2

# Update requirements.txt
pip freeze > requirements.txt
```

### 2. Environment Configuration
Create or update `.env` file with production settings:
```ini
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=yourusername.pythonanywhere.com,www.liveitech.com,liveitech.com
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## PythonAnywhere Configuration

### 1. Upload Files to PythonAnywhere
Upload your entire project to PythonAnywhere via:
- Git (recommended): `git clone https://github.com/yourusername/liveitech.git`
- File upload through PythonAnywhere dashboard
- Or use `rsync` for updates

### 2. Create Virtual Environment on PythonAnywhere
```bash
# In PythonAnywhere Bash console
cd /home/yourusername/liveitech
python3.13 -m venv lit-venv
source lit-venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Web App

#### A. Basic Settings
- **Source code:** `/home/yourusername/liveitech`
- **Working directory:** `/home/yourusername/liveitech`
- **Python version:** 3.13 (or your version)
- **Virtualenv:** `/home/yourusername/liveitech/lit-venv`

#### B. WSGI Configuration File
Edit the WSGI configuration file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/liveitech'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'lit_settings.settings'

# Activate virtual environment
activate_this = '/home/yourusername/liveitech/lit-venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### C. Static Files Mapping
In the PythonAnywhere Web tab, add these static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/liveitech/staticfiles/` |
| `/media/` | `/home/yourusername/liveitech/media/` |

**Important:** The `/media/` mapping is critical for serving uploaded images!

### 4. Database Setup
```bash
# In PythonAnywhere Bash console
source lit-venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_content  # If using initial content
```

### 5. Set Environment Variables
Create `.env` file in project root on PythonAnywhere:
```bash
nano /home/yourusername/liveitech/.env
```

Add:
```ini
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourusername.pythonanywhere.com,www.liveitech.com,liveitech.com
```

### 6. Reload Web App
Click the green "Reload" button in the PythonAnywhere Web tab.

---

## Verification Steps

### 1. Check File Permissions
```bash
# Ensure media directory is readable
chmod -R 755 /home/yourusername/liveitech/media/
chmod -R 755 /home/yourusername/liveitech/staticfiles/
```

### 2. Verify Files Exist
```bash
# Check media files are uploaded
ls -la /home/yourusername/liveitech/media/hero/
ls -la /home/yourusername/liveitech/media/services/
ls -la /home/yourusername/liveitech/media/partners/

# Check static files are collected
ls -la /home/yourusername/liveitech/staticfiles/
```

### 3. Test URLs Directly
In your browser, try accessing:
- `https://yourusername.pythonanywhere.com/media/hero/logo-large-light-2.png`
- `https://yourusername.pythonanywhere.com/static/css/style.css`

If these return 404, check:
1. Static files mapping in PythonAnywhere Web tab
2. File paths are correct
3. Files have proper permissions

### 4. Check Error Logs
In PythonAnywhere Web tab:
- View **Error log** for Python/Django errors
- View **Server log** for HTTP request errors
- Look for 404 errors on media URLs

### 5. Browser Developer Tools
- Open browser console (F12)
- Check Network tab for failed image requests
- Look for 404 or 403 errors on image URLs

---

## Common Issues and Solutions

### Issue: Images Still Not Displaying

**Solution 1: Verify Static Mapping**
- Go to PythonAnywhere Web tab
- Check `/media/` is mapped to `/home/yourusername/liveitech/media/`
- Ensure there's no trailing or missing slashes

**Solution 2: Check File Paths**
```python
# In PythonAnywhere Python console
from lit_settings import settings
print(settings.MEDIA_ROOT)  # Should show absolute path
print(settings.MEDIA_URL)   # Should show /media/
```

**Solution 3: Verify Database Has Image Paths**
```python
# In PythonAnywhere Python console
from lit_app.models import HeroSection
hero = HeroSection.objects.filter(is_active=True).first()
print(hero.logo_image.url)  # Should show /media/hero/filename.png
print(hero.logo_image.path) # Should show full system path
```

**Solution 4: Re-upload Images via Admin**
If images were uploaded before WhiteNoise configuration:
1. Log into admin: `https://yourusername.pythonanywhere.com/admin/`
2. Navigate to each section
3. Re-upload images (they'll be saved with proper paths)

### Issue: 500 Internal Server Error

Check error logs for details:
```bash
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

Common causes:
- Missing `.env` file
- Incorrect `SECRET_KEY`
- Database not migrated
- Missing dependencies in virtual environment

### Issue: Admin Page Loads But No Styling

Run collectstatic again:
```bash
python manage.py collectstatic --clear --noinput
```

Then reload the web app.

---

## Updating Content (After Initial Deployment)

### Upload New Images
1. Log into Django admin: `/admin/`
2. Update content sections with new images
3. Images automatically save to `/media/` directory
4. No server reload needed!

### Update Code
```bash
# In PythonAnywhere Bash console
cd /home/yourusername/liveitech
git pull origin main
source lit-venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then reload the web app.

---

## Key Configuration Files

### settings.py Changes
```python
# Static and Media URLs with leading slashes
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# WhiteNoise middleware added
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Added
    # ... other middleware
]

# WhiteNoise configuration
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
WHITENOISE_ROOT = MEDIA_ROOT
WHITENOISE_ALLOW_ALL_ORIGINS = True
```

### urls.py Changes
```python
# Media files served in production too
if settings.DEBUG:
    # Development: serve both static and media
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: serve media files (static handled by WhiteNoise)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Testing Locally with Production Settings

To test production configuration locally:

```bash
# Set DEBUG=False in .env
DEBUG=False

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and verify images display correctly.

**Important:** Set `DEBUG=True` for normal development!

---

## Support Resources

- **PythonAnywhere Help:** https://help.pythonanywhere.com/
- **Django Static Files:** https://docs.djangoproject.com/en/5.2/howto/static-files/
- **WhiteNoise Documentation:** https://whitenoise.readthedocs.io/

---

## Quick Reference Commands

```bash
# Activate virtual environment (PythonAnywhere)
source lit-venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Database operations
python manage.py migrate
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Check media files
ls -la media/hero/ media/services/ media/partners/

# View error logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

After any changes, remember to **Reload** your web app in the PythonAnywhere Web tab!
