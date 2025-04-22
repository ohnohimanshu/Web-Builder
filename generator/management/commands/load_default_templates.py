from django.core.management.base import BaseCommand
from generator.models import WebsiteTemplate
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Loads default website templates from templates folder'

    def handle(self, *args, **kwargs):
        templates_dir = os.path.join(settings.BASE_DIR, 'generator', 'templates', 'templates')
        
        # Portfolio template
        with open(os.path.join(templates_dir, 'portfolio.html'), 'r') as file:
            portfolio_html = file.read()

        portfolio_css = """
        :root {
            --primary-color: {{ primary_color|default:'#007bff' }};
            --secondary-color: {{ secondary_color|default:'#6c757d' }};
            --text-color: {{ text_color|default:'#333333' }};
            --background-color: {{ background_color|default:'#ffffff' }};
        }
        """

        portfolio_template = WebsiteTemplate.objects.create(
            name='Modern Portfolio',
            description='A clean and modern portfolio template perfect for showcasing your work',
            template_type='portfolio',
            html_structure=portfolio_html,
            css_structure=portfolio_css,
            features={
                'sections': ['hero', 'about', 'projects', 'skills', 'contact'],
                'responsive': True,
                'animations': True,
                'social_links': True
            },
            is_premium=False
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created template: {portfolio_template.name}')
        )