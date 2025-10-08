# Django Single-Page Business Site - AI Coding Instructions

## Project Architecture

This is a Django-based single-page application for LIVE i TECH, a security systems company. The architecture follows a **section-based content management** pattern where the homepage is composed of database-driven sections.

### Key Components
- **Main app**: `lit_app` - Contains all models, views, and business logic
- **Settings**: `lit_settings` - Django project configuration
- **Virtual environment**: `lit-venv/` - Isolated Python environment (activate before development)
- **Database**: SQLite (`db.sqlite3`) - Simple file-based database for content storage

### Single-Page Architecture Pattern
The homepage (`templates/pages/index.html`) includes multiple section templates that render content from corresponding database models:
- Hero → `HeroSection` model
- About → `AboutSection` model  
- Services → `ServicesSection` + `ServiceItem` models
- Portfolio → `PortfolioSection` model
- Partners → `PartnersSection` + `PartnerItem` models
- Examples → `ExamplesSection` + `ExampleVideo` models
- Contact → `ContactSection` model
- Footer → `FooterSection` model

## Development Workflow

### Essential Commands
```bash
# Activate virtual environment (Windows)
lit-venv\Scripts\activate

# Run development server
python manage.py runserver

# Database operations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Populate with default content
python manage.py populate_content
```

### Database Content Management
- **All content is database-driven** via Django admin at `/admin/`
- Each section model has an `is_active` field for visibility control
- Models with multiple items (Services, Partners, etc.) use `order` fields for sorting
- Use the `populate_content` management command to seed initial data

## Project-Specific Patterns

### CKEditor Integration
- Rich text editing via `django_ckeditor_5` with custom toolbar configurations
- **Critical**: Subtitle fields use `strip_outer_p` template filter to remove CKEditor's automatic `<p>` wrappers
- Example: `{{ about.subtitle|strip_outer_p|safe }}` in templates
- Configuration in `settings.py` includes custom color palettes and toolbar layouts

### Template Organization
```
templates/
├── base/base.html          # Main layout
├── components/             # Reusable UI components  
├── sections/              # Page section templates
├── pages/                 # Full page templates
└── forms/                 # Form-related templates
```

### Static File Structure
- CSS/JS in `static/` (development) and `staticfiles/` (production)
- Media files (uploads) in `media/` with organized subdirectories by model
- Images are uploaded via admin interface to model-specific folders

### Admin Configuration
- Extensive admin customization in `lit_app/admin.py` with fieldsets for organization
- List displays show key fields and status
- Inline editing for order fields where applicable
- Help text guides content editors on image dimensions and requirements

## Critical Dependencies

- **django-ckeditor-5**: WYSIWYG editor (version 0.2.18)
- **python-decouple**: Environment configuration management
- **Pillow**: Image processing for uploaded media
- **django-crispy-forms**: Enhanced form rendering

## Development Notes

### Environment Variables
Uses `python-decouple` for configuration. Key variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Development mode toggle  
- `ALLOWED_HOSTS` - Comma-separated host list

### URL Patterns
- Minimal routing: Homepage (`/`), contact form (`/send-mail/`), confirmation (`/email-sent/`)
- Admin interface at `/admin/`
- CKEditor uploads at `/ckeditor5/`

### Common Tasks
- **Adding new sections**: Create model → admin registration → template → add to index.html
- **Content updates**: Use Django admin interface, not code changes
- **Image management**: Upload via admin, organized in `media/` subfolders
- **Template debugging**: Check `strip_outer_p` filter usage for CKEditor content

### Custom Management Commands
- `populate_content.py` - Seeds database with hardcoded content from old templates
- `clearcache.py` - Cache management utility
- Located in `lit_app/management/commands/`

This codebase prioritizes content management flexibility over complex functionality, making the Django admin interface the primary tool for non-technical content updates.
