from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from lit_app import views

urlpatterns = [
 path( 'admin/', admin.site.urls ),
 path( 'ckeditor5/', include( 'django_ckeditor_5.urls' ) ),
 path( '', views.index, name='index' ),
 path( 'send-mail/', views.send_mail_view, name='send_mail' ),
 path( 'email-sent/', views.email_sent, name='email_sent' ),
]

# Serve static and media files during development
if settings.DEBUG :
 urlpatterns +=\
  static( settings.STATIC_URL,
    document_root = settings.STATICFILES_DIRS[ 0 ] )
 urlpatterns +=\
  static( settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT )
else:
 # In production, serve media files (static files handled by WhiteNoise)
 urlpatterns +=\
  static( settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT )
