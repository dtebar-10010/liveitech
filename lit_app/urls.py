from django.urls import path
from . import views

app_name = 'lit_app'

urlpatterns = [
 # Main homepage (single page app)
 path( '', views.index, name = 'index' ),

 # Form handling
 path( 'send-mail/', views.send_mail, name = 'send_mail' ),
 path( 'email-sent/', views.email_sent, name = 'email_sent' ),
]
