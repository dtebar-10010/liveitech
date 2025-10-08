import os
from django.core.management.base import BaseCommand
from django.conf import settings
from lit_app.models import (
    HeroSection, AboutSection, ServiceItem, ServicesSection,
    PortfolioSection, PartnerItem, PartnersSection,
    ExampleVideo, ExamplesSection, ContactSection, FooterSection
)

class Command(BaseCommand):
    help = 'Populate database with existing hardcoded content from templates'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting content population...'))

        # Helper to get static file paths
        static_root = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT

        # 1. Hero Section
        self.stdout.write('Creating Hero Section...')
        hero, created = HeroSection.objects.get_or_create(
            id=1,
            defaults={
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Hero Section created (you need to upload images in admin)'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Hero Section already exists'))

        # 2. About Section
        self.stdout.write('Creating About Section...')
        about, created = AboutSection.objects.get_or_create(
            id=1,
            defaults={
                'title': 'About Us',
                'subtitle': '<h6 class="m-b-2">The technology world grows at an expontential rate and is integrated into myriad applications that better our physical world. LIVE i TECH was founded with the sole purpose of understanding this growth and providing its full potential to our clients through customized, tech-based systems.</h6>',
                'description': '<p>Our team takes pride in offering a full-service approach to our clients including consultation, design, installation, service & maintenance. LIVE i TECH continues to build and maintain strong relationships with our vendors in the Security, Surveillance & IOT (Internet of Things) industries so that we may always provide the best solutions for our clients. LIVE i TECH strives to keep its community informed about the latest technologies so that together we can innovate a smarter, safer and better world. Our corporate office is located in Fort Lauderdale Florida, and we service the entire USA.</p>',
                'service_1_icon': 'fa fa-comments',
                'service_1_text': 'PA & Audio',
                'service_2_icon': 'fa fa-phone',
                'service_2_text': 'Intercom & Phone',
                'service_3_icon': 'fa fa-lock',
                'service_3_text': 'Access Control',
                'service_4_icon': 'fa fa-support',
                'service_4_text': 'CCTV',
                'service_5_icon': 'fa fa-random',
                'service_5_text': 'Support',
                'service_6_icon': 'fa fa-ambulance',
                'service_6_text': 'Maintenance',
                'service_7_icon': '',
                'service_7_text': '',
                'service_8_icon': 'fa fa-code',
                'service_8_text': 'Custom Software',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] About Section created'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] About Section already exists'))

        # 3. Services Section Header
        self.stdout.write('Creating Services Section Header...')
        services_header, created = ServicesSection.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Our Services',
                'subtitle': '<h6>Our family of consultants and systems engineers are equipped with the knowledge to design the perfect system to address all of your security, network and low voltage needs. From surveillance to audio, our team of technicians can install any system for both, residential and commercial applications.</h6>',
                'description': '<p>Our installers have the knowledge and support to do the job right, the first time. Check out what LIVE i TECH has to offer --below, and schedule your free assessment today!</p>',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Services Section Header created'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Services Section Header already exists'))

        # 4. Service Items
        self.stdout.write('Creating Service Items...')
        services_data = [
            {
                'title': 'CCTV',
                'description': '<p>LIVE i TECH has worked with many of the leading CCTV manufacturers to consistently stay informed on new systems. Whether you have a home, business, or municipality, our team is equipped to handle projects of any size. Our systems are modular and therefore can be scaled for future growth.</p>',
                'order': 1,
                'anchor_id': 'cctv',
            },
            {
                'title': 'Access Control',
                'description': '<p>Our access control or "keyless entry" systems assist our clients by providing restricted access to certain areas of their home, or business. Whether it\'s a keypad to restrict entry, or a dozen biometric readers logging traffic in and out of multiple areas, we have the knowledge and expertise to get you exactly what you need. We have multiple systems to choose from; these systems are available for many different budgets, and needs.</p>',
                'order': 2,
                'anchor_id': 'card',
            },
            {
                'title': 'IOT LAN & WAN',
                'description': '<p>The Internet of Things is growing as every year more devices are connected to the internet. What used to be only a computer hardwired with an ethernet cable, is now a network of interconnected devices. Since our family realized this change, we have been continuously educating ourselves on the latest networked systems so that we may offer you the latest in VOIP, RFID Asset Tracking, etc. We have the capabilities to install your physical network infrastructure, or your private wireless area network.</p>',
                'order': 3,
                'anchor_id': 'iot',
            },
            {
                'title': 'Intercom & PA',
                'description': '<p>Did you hear? LIVE i TECH can help you with all of your audio needs as well. Our commercial installers can assist you in setting up your intercom and/or public address systems; high-quality sound, and quality installations to address your specific needs.</p>',
                'order': 4,
                'anchor_id': 'intercom',
            },
            {
                'title': 'System Design',
                'description': '<p>Our consultants are provided with consistent access to education and training so that they may design the system that meets your needs. LIVE i TECH maintains strong relationships with local municipalities to get your projects completed in a timely manner. Our team has designed customized systems for multiple applications in many different industries.</p>',
                'order': 5,
                'anchor_id': 'design',
            },
            {
                'title': 'Software Development/Consulting',
                'description': '<p>LIVE i TECH has added an experienced software development team. We now offer custom web sites and full-fledged eCommerce web applications!</p>',
                'order': 6,
                'anchor_id': 'software',
            },
        ]

        for service_data in services_data:
            service, created = ServiceItem.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'order': service_data['order'],
                    'anchor_id': service_data['anchor_id'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Service "{service_data["title"]}" created (upload image in admin)'))
            else:
                self.stdout.write(self.style.WARNING(f'  [SKIP] Service "{service_data["title"]}" already exists'))

        # 5. Portfolio Section
        self.stdout.write('Creating Portfolio Section...')
        portfolio, created = PortfolioSection.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Portfolio',
                'subtitle': '<h6 class="m-b-2">LIVE i TECH embraces a culture dedicated to excellence. Therefore, our business philosophy is built around trust, partnership, and leveraging proven technologies that will provide you with maximum value and reliability for years to come.</h6>',
                'description': '<p>From best-in-class security cameras and video surveillance solutions, to the latest intercom and access control systems, to advanced information management solutions, we never lose sight of the fact that we are in the business of protecting people, not just property.</p>',
                'image_1_alt': 'Elite Flower Portfolio Project',
                'image_2_alt': 'Bay Harbor Islands Portfolio Project',
                'image_3_alt': 'BNM Portfolio Project',
                'image_4_alt': 'PTZ Escalator Security System',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Portfolio Section created (upload images in admin)'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Portfolio Section already exists'))

        # 6. Partners Section Header
        self.stdout.write('Creating Partners Section Header...')
        partners_header, created = PartnersSection.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Our Partners',
                'subtitle': '<h6>LIVE i TECH strives to build and maintain relationships with top manufacturers in the security and technology industry. With these relationships in place, our clients can rest assured that they are receiving the very best technology.</h6>',
                'description': '<p>Get priceless peace of mind.</p>',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Partners Section Header created'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Partners Section Header already exists'))

        # 7. Partner Items
        self.stdout.write('Creating Partner Items...')
        partners_data = [
            {'name': 'BioConnect Suprema', 'order': 1},
            {'name': 'Digital Watch Dog', 'order': 2},
            {'name': 'Aiphone', 'order': 3},
            {'name': 'Keyscan', 'order': 4},
            {'name': 'Honeywell', 'order': 5},
            {'name': 'Nortek', 'order': 6},
            {'name': 'Axis Communications', 'order': 7},
            {'name': 'Comelit', 'order': 8},
            {'name': 'Ubiquiti Networks', 'order': 9},
        ]

        for partner_data in partners_data:
            partner, created = PartnerItem.objects.get_or_create(
                name=partner_data['name'],
                defaults={
                    'order': partner_data['order'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Partner "{partner_data["name"]}" created (upload logo in admin)'))
            else:
                self.stdout.write(self.style.WARNING(f'  [SKIP] Partner "{partner_data["name"]}" already exists'))

        # 8. Examples Section Header
        self.stdout.write('Creating Examples Section Header...')
        examples_header, created = ExamplesSection.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Examples',
                'subtitle': '<h6>Our work, in action.</h6>',
                'description': '<p>Subscribe to our YouTube channel.</p>',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Examples Section Header created'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Examples Section Header already exists'))

        # 9. Example Videos
        self.stdout.write('Creating Example Videos...')
        videos_data = [
            {'url': 'https://www.youtube-nocookie.com/embed/i5n6OMiVgEU?rel=0&modestbranding=1&showinfo=0', 'order': 1},
            {'url': 'https://www.youtube-nocookie.com/embed/o36rO2BBWKE?rel=0&modestbranding=1&showinfo=0', 'order': 2},
            {'url': 'https://www.youtube-nocookie.com/embed/n0mFru_O_Z4?rel=0&modestbranding=1&showinfo=0', 'order': 3},
            {'url': 'https://www.youtube-nocookie.com/embed/0164NzWczEU?rel=0&modestbranding=1&showinfo=0', 'order': 4},
            {'url': 'https://www.youtube-nocookie.com/embed/VKisTNDkQpo?rel=0&modestbranding=1&showinfo=0', 'order': 5},
        ]

        for video_data in videos_data:
            video, created = ExampleVideo.objects.get_or_create(
                youtube_url=video_data['url'],
                defaults={
                    'order': video_data['order'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Video {video_data["order"]} created'))
            else:
                self.stdout.write(self.style.WARNING(f'  [SKIP] Video {video_data["order"]} already exists'))

        # 10. Contact Section
        self.stdout.write('Creating Contact Section...')
        contact, created = ContactSection.objects.get_or_create(
            id=1,
            defaults={
                'title': 'Get LiT Now!',
                'subtitle': '<h6>Schedule a free assessment.</h6>',
                'phone': '(954) 445-0712',
                'google_maps_embed_url': 'https://www.google.com/maps/embed?pb=!1m10!1m8!1m3!1d764022.0392365947!2d-81.10230656282094!3d26.32140860227949!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sus!4v1556176806680!5m2!1sen!2sus',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Contact Section created'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Contact Section already exists'))

        # 11. Footer Section
        self.stdout.write('Creating Footer Section...')
        footer, created = FooterSection.objects.get_or_create(
            id=1,
            defaults={
                'facebook_url': 'https://www.facebook.com/LIVEiTECHINC/',
                'twitter_url': 'https://x.com/LIVEiTECH',
                'instagram_url': 'https://www.instagram.com/liveitech/',
                'youtube_url': 'https://www.youtube.com/channel/UCXq_QNtvHMJQCqChthZs6VA',
                'copyright_text': '©2025 LIVE i TECH, Inc.',
                'phone': '(954) 445-0712',
                'location': 'Ft. Lauderdale, Fl',
                'developer_text': 'Tébar Software',
                'developer_url': 'https://dtebar.pythonanywhere.com',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] Footer Section created (upload logo in admin)'))
        else:
            self.stdout.write(self.style.WARNING('  [SKIP] Footer Section already exists'))

        self.stdout.write(self.style.SUCCESS('\n[DONE] Content population complete!'))
        self.stdout.write(self.style.WARNING('\n[IMPORTANT] You still need to upload images in the Django admin for:'))
        self.stdout.write('   - Hero Section (logo + background)')
        self.stdout.write('   - Service Items (6 images)')
        self.stdout.write('   - Portfolio (4 images)')
        self.stdout.write('   - Partners (9 logos)')
        self.stdout.write('   - Footer (1 logo)')
        self.stdout.write(self.style.SUCCESS('\nAccess admin at: http://localhost:8000/admin/'))
