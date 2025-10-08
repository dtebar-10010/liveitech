from django.shortcuts import render
from .models import (
    HeroSection, AboutSection, ServiceItem, ServicesSection,
    PortfolioSection, PartnerItem, PartnersSection,
    ExampleVideo, ExamplesSection, ContactSection, FooterSection
)

def index( request ) :
 """Homepage view"""
 context = {
  'hero': HeroSection.objects.filter(is_active=True).first(),
  'about': AboutSection.objects.filter(is_active=True).first(),
  'services_header': ServicesSection.objects.filter(is_active=True).first(),
  'services': ServiceItem.objects.filter(is_active=True),
  'portfolio': PortfolioSection.objects.filter(is_active=True).first(),
  'partners_header': PartnersSection.objects.filter(is_active=True).first(),
  'partners': PartnerItem.objects.filter(is_active=True),
  'examples_header': ExamplesSection.objects.filter(is_active=True).first(),
  'examples': ExampleVideo.objects.filter(is_active=True),
  'contact': ContactSection.objects.filter(is_active=True).first(),
  'footer': FooterSection.objects.filter(is_active=True).first(),
 }
 return render( request, 'pages/index.html', context )

# def blog( request ) :
#  """Blog page view"""
#  return render( request, 'pages/blog.html' )

# def contact( request ) :
#  """Contact form view"""
#  return render( request, 'pages/contactus.html' )

def email_sent( request ) :
 """Email sent confirmation view"""
 return render( request, 'pages/emailsent.html' )

# def portfolio( request ) :
#  """Portfolio page view"""
#  return render( request, 'pages/portfolio.html' )
#
# def services( request ) :
#  """Services page view"""
#  return render( request, 'pages/services.html' )

# def about( request ) :
#  """About page view"""
#  return render( request, 'pages/about.html' )

# def team( request ) :
#  """Team page view"""
#  return render( request, 'pages/theteam.html' )

# Form handling view (for contact form)
def send_mail( request ) :
 """Handle contact form submission"""
 if request.method == 'POST' :
  # For now, just redirect to email sent page
  # Later you can add actual email sending logic here
  return render( request, 'pages/emailsent.html' )
 else :
  # If not POST, redirect to contact page
  return render( request, 'pages/contactus.html' )
