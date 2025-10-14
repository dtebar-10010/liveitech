from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .forms import ContactForm

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
def send_mail_view(request):
    if request.method == 'POST':
        # Extract form data directly from POST
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        company = request.POST.get('company', '')
        title = request.POST.get('title', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')
        system_of_interest = request.POST.get('systemofinterest', '')
        message = request.POST.get('message', '')
        current_customer = request.POST.get('currentcust', 'off')
        
        # Compose email
        subject = f'New Contact Form Submission from {name}'
        email_message = f"""
New contact form submission from LIVE i TECH website:

Name: {name}
Company: {company}
Title: {title}
Email: {email}
Phone: {phone}

Address: {address}
City: {city}
State: {state}
Zip Code: {zipcode}

System of Interest: {system_of_interest}
Current Customer: {'Yes' if current_customer == 'on' else 'No'}

Comments:
{message}

---
This email was sent from the LIVE i TECH contact form.
        """
        
        try:
            # Send email
            send_mail(
                subject=subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully'})
        except Exception as e:
            # Log error but still return success to user
            print(f"Error sending email: {e}")
            # Return success status so modal shows, but log error on server
            return JsonResponse({'status': 'error', 'message': 'There was an issue sending your email. Please try again or contact us directly.'})
    
    # If GET request, redirect to homepage
    return redirect('index')
