from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class HeroSection(models.Model):
    """Hero section with logo and background image"""
    logo_image = models.ImageField(upload_to='hero/', help_text='Logo image (280x auto)')
    background_image = models.ImageField(upload_to='hero/', help_text='Hero background image')
    is_active = models.BooleanField(default=True, help_text='Display this hero section')

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'

    def __str__(self):
        return f"Hero Section ({'Active' if self.is_active else 'Inactive'})"


class AboutSection(models.Model):
    """About Us section"""
    title = models.CharField(max_length=200, default='About Us')
    subtitle = CKEditor5Field('Subtitle', config_name='extends')
    description = CKEditor5Field('Description', config_name='extends')

    # Service icons (displayed as grid)
    service_1_icon = models.CharField(max_length=50, default='fa fa-comments', help_text='FontAwesome class (e.g., fa fa-comments)')
    service_1_text = models.CharField(max_length=100, default='PA & Audio')

    service_2_icon = models.CharField(max_length=50, default='fa fa-phone')
    service_2_text = models.CharField(max_length=100, default='Intercom & Phone')

    service_3_icon = models.CharField(max_length=50, default='fa fa-lock')
    service_3_text = models.CharField(max_length=100, default='Access Control')

    service_4_icon = models.CharField(max_length=50, default='fa fa-support')
    service_4_text = models.CharField(max_length=100, default='CCTV')

    service_5_icon = models.CharField(max_length=50, default='fa fa-random')
    service_5_text = models.CharField(max_length=100, default='Support')

    service_6_icon = models.CharField(max_length=50, default='fa fa-ambulance')
    service_6_text = models.CharField(max_length=100, default='Maintenance')

    service_7_icon = models.CharField(max_length=50, default='fa fa-exclamation-triangle', blank=True)
    service_7_text = models.CharField(max_length=100, blank=True)

    service_8_icon = models.CharField(max_length=50, default='fa fa-code')
    service_8_text = models.CharField(max_length=100, default='Custom Software')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'About Section'
        verbose_name_plural = 'About Section'

    def __str__(self):
        return self.title


class ServiceItem(models.Model):
    """Individual service item in Services section"""
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='extends')
    image = models.ImageField(upload_to='services/')
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    anchor_id = models.CharField(max_length=50, blank=True, help_text='HTML anchor ID (e.g., cctv, card)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Service Item'
        verbose_name_plural = 'Service Items'
        ordering = ['order']

    def __str__(self):
        return self.title


class ServicesSection(models.Model):
    """Services section header"""
    title = models.CharField(max_length=200, default='Our Services')
    subtitle = CKEditor5Field('Subtitle', config_name='extends')
    description = CKEditor5Field('Description', config_name='extends')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Services Section Header'
        verbose_name_plural = 'Services Section Header'

    def __str__(self):
        return self.title


class PortfolioSection(models.Model):
    """Portfolio section"""
    title = models.CharField(max_length=200, default='Portfolio')
    subtitle = CKEditor5Field('Subtitle', config_name='extends')
    description = CKEditor5Field('Description', config_name='extends')

    # Portfolio images
    image_1 = models.ImageField(upload_to='portfolio/', blank=True)
    image_1_alt = models.CharField(max_length=200, default='Portfolio Project 1')

    image_2 = models.ImageField(upload_to='portfolio/', blank=True)
    image_2_alt = models.CharField(max_length=200, default='Portfolio Project 2')

    image_3 = models.ImageField(upload_to='portfolio/', blank=True)
    image_3_alt = models.CharField(max_length=200, default='Portfolio Project 3')

    image_4 = models.ImageField(upload_to='portfolio/', blank=True)
    image_4_alt = models.CharField(max_length=200, default='Portfolio Project 4')

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Portfolio Section'
        verbose_name_plural = 'Portfolio Section'

    def __str__(self):
        return self.title


class PartnerItem(models.Model):
    """Individual partner logo"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['order']

    def __str__(self):
        return self.name


class PartnersSection(models.Model):
    """Partners section header"""
    title = models.CharField(max_length=200, default='Our Partners')
    subtitle = CKEditor5Field('Subtitle', config_name='extends')
    description = CKEditor5Field('Description', config_name='extends')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Partners Section Header'
        verbose_name_plural = 'Partners Section Header'

    def __str__(self):
        return self.title


class ExampleVideo(models.Model):
    """Individual example video"""
    youtube_url = models.URLField(help_text='Full YouTube URL (will be converted to embed)')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Example Video'
        verbose_name_plural = 'Example Videos'
        ordering = ['order']

    def __str__(self):
        return f"Video {self.order}: {self.youtube_url[:50]}"


class ExamplesSection(models.Model):
    """Examples section header"""
    title = models.CharField(max_length=200, default='Examples')
    subtitle = CKEditor5Field('Subtitle', config_name='extends')
    description = CKEditor5Field('Description', config_name='extends')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Examples Section Header'
        verbose_name_plural = 'Examples Section Header'

    def __str__(self):
        return self.title


class ContactSection(models.Model):
    """Contact section"""
    title = models.CharField(max_length=200, default='Get LiT Now!')
    subtitle = CKEditor5Field('Subtitle', config_name='extends')
    phone = models.CharField(max_length=50, default='(954) 445-0712')
    google_maps_embed_url = models.URLField(help_text='Google Maps embed iframe src URL')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Contact Section'
        verbose_name_plural = 'Contact Section'

    def __str__(self):
        return self.title


class FooterSection(models.Model):
    """Footer section"""
    logo_image = models.ImageField(upload_to='footer/')

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    copyright_text = models.CharField(max_length=200, default='©2025 LIVE i TECH, Inc.')
    phone = models.CharField(max_length=50, default='(954) 445-0712')
    location = models.CharField(max_length=200, default='Ft. Lauderdale, Fl')

    developer_text = models.CharField(max_length=200, default='Tébar Software')
    developer_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Footer Section'
        verbose_name_plural = 'Footer Section'

    def __str__(self):
        return 'Footer Section'
