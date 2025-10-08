from django.contrib import admin
from .models import (
    HeroSection, AboutSection, ServiceItem, ServicesSection,
    PortfolioSection, PartnerItem, PartnersSection,
    ExampleVideo, ExamplesSection, ContactSection, FooterSection
)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Images', {
            'fields': ['logo_image', 'background_image']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'description']
        }),
        ('Service Icons Row 1', {
            'fields': [
                ('service_1_icon', 'service_1_text'),
                ('service_2_icon', 'service_2_text'),
                ('service_3_icon', 'service_3_text'),
                ('service_4_icon', 'service_4_text'),
            ]
        }),
        ('Service Icons Row 2', {
            'fields': [
                ('service_5_icon', 'service_5_text'),
                ('service_6_icon', 'service_6_text'),
                ('service_7_icon', 'service_7_text'),
                ('service_8_icon', 'service_8_text'),
            ]
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'description']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'anchor_id', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order']
    ordering = ['order']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'description', 'image']
        }),
        ('Settings', {
            'fields': ['order', 'anchor_id', 'is_active']
        }),
    ]


@admin.register(PortfolioSection)
class PortfolioSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'description']
        }),
        ('Portfolio Images', {
            'fields': [
                ('image_1', 'image_1_alt'),
                ('image_2', 'image_2_alt'),
                ('image_3', 'image_3_alt'),
                ('image_4', 'image_4_alt'),
            ]
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(PartnersSection)
class PartnersSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'description']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(PartnerItem)
class PartnerItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order']
    ordering = ['order']
    fieldsets = [
        ('Content', {
            'fields': ['name', 'logo']
        }),
        ('Settings', {
            'fields': ['order', 'is_active']
        }),
    ]


@admin.register(ExamplesSection)
class ExamplesSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'description']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(ExampleVideo)
class ExampleVideoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order']
    ordering = ['order']
    fieldsets = [
        ('Content', {
            'fields': ['youtube_url']
        }),
        ('Settings', {
            'fields': ['order', 'is_active']
        }),
    ]


@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Content', {
            'fields': ['title', 'subtitle', 'phone', 'google_maps_embed_url']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active']
    list_filter = ['is_active']
    fieldsets = [
        ('Logo', {
            'fields': ['logo_image']
        }),
        ('Social Media Links', {
            'fields': ['facebook_url', 'twitter_url', 'instagram_url', 'youtube_url']
        }),
        ('Contact Information', {
            'fields': ['copyright_text', 'phone', 'location']
        }),
        ('Developer Credit', {
            'fields': ['developer_text', 'developer_url']
        }),
        ('Status', {
            'fields': ['is_active']
        }),
    ]
