import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command( BaseCommand ) :
 help = 'Convert PHP templates to Django templates'

 def __init__( self, *args, **kwargs ) :
  super( ).__init__( *args, **kwargs )
  self.dry_run = False
  self.backup = True

 def add_arguments( self, parser ) :
  parser.add_argument(
   '--dry-run',
   action = 'store_true',
   help = 'Show what would be converted without actually converting files',
  )
  parser.add_argument(
   '--no-backup',
   action = 'store_true',
   help = 'Skip creating backup of templates',
  )

 def handle( self, *args, **options ) :
  self.dry_run = options[ 'dry_run' ]
  self.backup = not options[ 'no_backup' ]

  templates_dir = Path( settings.BASE_DIR ) / 'templates'

  if not templates_dir.exists( ) :
   raise CommandError( f'Templates directory not found: {templates_dir}' )

  self.stdout.write(
   self.style.SUCCESS( 'Starting PHP to Django template conversion...' )
  )

  # Create backup if needed
  if self.backup and not self.dry_run :
   backup_dir = templates_dir.parent / 'templates_php_backup'
   if not backup_dir.exists( ) :
    import shutil

    shutil.copytree( templates_dir, backup_dir )
    self.stdout.write( f'Created backup at: {backup_dir}' )

  # Convert all HTML files
  converted_count = 0
  for html_file in templates_dir.rglob( '*.html' ) :
   if self.convert_template( html_file ) :
    converted_count += 1

  if self.dry_run :
   self.stdout.write(
    self.style.WARNING( f'DRY RUN - Would convert {converted_count} files' )
   )
  else :
   self.stdout.write(
    self.style.SUCCESS( f'Converted {converted_count} template files!' )
   )

 def convert_template( self, file_path ) :
  """Convert a single template file from PHP to Django"""
  try :
   with open( file_path, 'r', encoding = 'utf-8' ) as f :
    content = f.read( )

   original_content = content

   # Skip if already converted (contains Django template tags)
   if '{% load static %}' in content or '{% extends' in content :
    return False

   # Convert PHP includes to Django includes
   content = self.convert_php_includes( content )

   # Convert static file references
   content = self.convert_static_references( content )

   # Remove PHP tags
   content = self.remove_php_tags( content )

   # Add Django template tags if needed
   content = self.add_django_template_tags( content, file_path )

   # Clean up whitespace
   content = self.clean_whitespace( content )

   if content != original_content :
    if self.dry_run :
     self.stdout.write( f'Would convert: {file_path}' )
    else :
     with open( file_path, 'w', encoding = 'utf-8' ) as f :
      f.write( content )
     self.stdout.write( f'Converted: {file_path}' )
    return True

  except Exception as e :
   self.stdout.write(
    self.style.ERROR( f'Error converting {file_path}: {str( e )}' )
   )

  return False

 @staticmethod
 def convert_php_includes( content ) :
  """Convert PHP require_once to Django includes"""

  # Mapping of PHP paths to Django template paths
  include_mapping = {
   r"php-pages/includes/head/head\.php" : "base/base.html",
   r"php-pages/includes/hero\.php" : "components/hero.html",
   r"php-pages/includes/floatbutton\.php" : "components/floatbutton.html",
   r"php-pages/includes/carousel\.php" : "components/carousel.html",
   r"php-pages/includes/about\.php" : "sections/about.html",
   r"php-pages/includes/portfolio\.php" : "sections/portfolio.html",
   r"php-pages/includes/services\.php" : "sections/services.html",
   r"php-pages/includes/partners\.php" : "sections/partners.html",
   r"php-pages/includes/examples\.php" : "sections/examples.html",
   r"php-pages/includes/theteam\.php" : "sections/theteam.html",
   r"php-pages/includes/testimonials\.php" : "sections/testimonials.html",
   r"php-pages/includes/blog\.php" : "sections/blog.html",
   r"php-pages/includes/contactus\.php" : "pages/contactus.html",
   r"php-pages/includes/footer\.php" : "sections/footer.html",
  }

  # Convert PHP includes to Django includes
  for php_path, django_path in include_mapping.items( ) :
   # Convert require_once
   pattern = rf"<\?php\s+require_once\s*\(\s*['\"]({php_path})['\"]?\s*\)\s*;\s*\?>"
   replacement = f"{{% include '{django_path}' %}}"
   content = re.sub( pattern, replacement, content, flags = re.IGNORECASE )

  # Convert PHP comments to Django comments
  content = re.sub( r'//\s*require_once\([^)]+\);?', r'{# \g<0> #}', content )

  return content

 @staticmethod
 def remove_php_tags( content ) :
  """Remove remaining PHP tags"""
  # Remove opening and closing PHP tags
  content = re.sub( r'<\?php.*?\?>', '', content, flags = re.DOTALL )
  return content

 @staticmethod
 def convert_static_references( content ) :
  """Convert static file references to Django static tags"""
  # Convert common static file patterns
  patterns = [
   (r'href\s*=\s*["\']([^"\']*\.css)["\']', r'href="{% static \'\1\' %}"'),
   (r'src\s*=\s*["\']([^"\']*\.(js|png|jpg|gif|ico))["\']', r'src="{% static \'\1\' %}"'),
  ]

  for pattern, replacement in patterns :
   content = re.sub( pattern, replacement, content )

  return content

 def add_django_template_tags( self, content, file_path ) :
  """Add necessary Django template tags"""
  # Determine if we need {% load static %}
  if '{% static' in content and '{% load static %}' not in content :
   # Add {% load static %} at the top
   if content.strip( ).startswith( '<!DOCTYPE' ) or content.strip( ).startswith( '<html' ) :
    content = '{% load static %}\n' + content
   else :
    content = '{% load static %}\n\n' + content

  # Check if this is a main page that should extend base
  file_name = file_path.name
  if file_name in [ 'index.html' ] and file_path.parent.name == 'pages' :
   if not content.strip( ).startswith( '{% extends' ) :
    # Convert to extending base template
    content = self.convert_to_extending_template( content, file_name )

  return content

 @staticmethod
 def convert_to_extending_template( content, filename ) :
  """Convert standalone HTML to template that extends base"""
  # Extract title if present
  title_match = re.search( r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE )

  # Use filename to create a more specific title
  if title_match :
   title = title_match.group( 1 )
  else :
   # Generate title based on filename
   base_name = filename.replace( '.html', '' ).replace( '_', ' ' ).title( )
   title = f'{base_name} - LIVEiTECH'

  # Extract body content
  body_match = re.search( r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE )
  if body_match :
   body_content = body_match.group( 1 ).strip( )

   # Remove the ioswrapper div if present
   body_content = re.sub( r'<div[^>]*id\s*=\s*["\']ioswrapper["\'][^>]*>(.*?)</div>$',
                          r'\1', body_content, flags = re.DOTALL )

   return f"""{{% extends 'base/base.html' %}}
{{% load static %}}

{{% block title %}}{title}{{% endblock %}}

{{% block content %}}
{body_content.strip( )}
{{% endblock %}}"""

  return content

 @staticmethod
 def clean_whitespace( content ) :
  """Clean up excessive whitespace"""
  # Remove multiple consecutive empty lines
  content = re.sub( r'\n\s*\n\s*\n', '\n\n', content )
  # Remove trailing whitespace
  content = '\n'.join( line.rstrip( ) for line in content.splitlines( ) )
  return content
