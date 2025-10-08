from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import shutil
from pathlib import Path

class Command( BaseCommand ) :
 help = 'Reorganize Django templates into a better folder structure'

 def __init__( self, *args, **kwargs ) :
  super( ).__init__( *args, **kwargs )
  self.dry_run = False
  self.no_backup = False

 def add_arguments( self, parser ) :
  parser.add_argument(
   '--dry-run',
   action = 'store_true',
   help = 'Show what would be moved without actually moving files',
  )
  parser.add_argument(
   '--no-backup',
   action = 'store_true',
   help = 'Skip creating backup of templates directory',
  )
  parser.add_argument(
   '--templates-dir',
   type = str,
   default = 'templates',
   help = 'Templates directory path (default: templates)',
  )

 def handle( self, *args, **options ) :
  self.dry_run = options[ 'dry_run' ]
  self.no_backup = options[ 'no_backup' ]
  templates_dir = options[ 'templates_dir' ]

  self.stdout.write(
   self.style.SUCCESS( 'Starting template reorganization...' )
  )

  # Get the base path (project root)
  base_path = Path( settings.BASE_DIR ) / templates_dir

  if not base_path.exists( ) :
   raise CommandError( f'Templates directory not found: {base_path}' )

  # Create backup unless --no-backup is specified
  if not self.no_backup and not self.dry_run :
   backup_path = Path( settings.BASE_DIR ) / f'{templates_dir}_backup'
   if not backup_path.exists( ) :
    shutil.copytree( base_path, backup_path )
    self.stdout.write(
     self.style.SUCCESS( f'Created backup at: {backup_path}' )
    )

  # Create new structure
  self.create_template_structure( base_path )

  # Reorganize templates
  self.reorganize_templates( base_path )

  if self.dry_run :
   self.stdout.write(
    self.style.WARNING( 'DRY RUN - No files were actually moved' )
   )
  else :
   self.stdout.write(
    self.style.SUCCESS( 'Template reorganization complete!' )
   )

 def create_template_structure( self, base_path ) :
  """Create the new template folder structure"""
  folders = [
   'base',
   'components',
   'sections',
   'pages',
   'forms',
   'data',
   'lit_app'
  ]

  for folder in folders :
   folder_path = base_path / folder
   if self.dry_run :
    self.stdout.write( f'Would create folder: {folder_path}' )
   else :
    folder_path.mkdir( exist_ok = True )
    self.stdout.write( f'Created folder: {folder_path}' )

 def reorganize_templates( self, base_path ) :
  """Move templates to their appropriate folders"""
  # Template categorization
  template_mapping = {
   # Base templates
   'base' : [ 'head.html' ],

   # Reusable components
   'components' : [ 'hero.html', 'carousel.html', 'floatbutton.html',
                    'preloader.html', 'beatlesmenu.html' ],

   # Page sections
   'sections' : [ 'about.html', 'portfolio.html', 'services.html',
                  'partners.html', 'examples.html', 'theteam.html', 'footer.html' ],

   # Complete pages
   'pages' : [ 'index.html', 'blog.html', 'contactus.html', 'emailsent.html' ],

   # Forms
   'forms' : [ 'send_mail.html' ],

   # Data templates
   'data' : [ 'JSON.html', 'geo-zip-codes.html' ]
  }

  # Move files to their new locations
  for folder, templates in template_mapping.items( ) :
   for template in templates :
    src = base_path / template
    dst = base_path / folder / template

    if src.exists( ) :
     if self.dry_run :
      self.stdout.write( f'Would move: {src} -> {dst}' )
     else :
      shutil.move( str( src ), str( dst ) )
      self.stdout.write(
       self.style.SUCCESS( f'Moved: {src} -> {dst}' )
      )
    else :
     self.stdout.write(
      self.style.WARNING( f'Template not found: {src}' )
     )

  # Show final structure if not dry run
  if not self.dry_run :
   self.show_template_structure( base_path )

 def show_template_structure( self, base_path ) :
  """Display the final template structure"""
  self.stdout.write( '\nFinal template structure:' )
  for root, dirs, files in os.walk( base_path ) :
   level = root.replace( str( base_path ), '' ).count( os.sep )
   indent = '  ' * level
   folder_name = os.path.basename( root ) or 'templates'
   self.stdout.write( f'{indent}{folder_name}/' )
   subindent = '  ' * (level + 1)
   for file in files :
    self.stdout.write( f'{subindent}{file}' )
