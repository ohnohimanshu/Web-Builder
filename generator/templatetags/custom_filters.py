from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def safe(value):
    """
    Custom safe filter that marks a string as safe for HTML rendering.
    This is a workaround for the |safe filter that was causing issues.
    """
    return mark_safe(value)

@register.filter
def get_status_color(status):
    colors = {
        'draft': 'warning',
        'published': 'success',
        'archived': 'secondary'
    }
    return colors.get(status, 'secondary')

@register.filter
def get_template_icon(template_type):
    icons = {
        'blog': 'fas fa-blog',
        'portfolio': 'fas fa-briefcase',
        'business': 'fas fa-building',
        'ecommerce': 'fas fa-shopping-cart'
    }
    return icons.get(template_type, 'fas fa-globe')

@register.filter
def get_template_description(template_type):
    descriptions = {
        'blog': 'Perfect for personal blogs, news sites, and content creators',
        'portfolio': 'Ideal for showcasing your work and projects',
        'business': 'Great for corporate websites and professional services',
        'ecommerce': 'Designed for online stores and product showcases'
    }
    return descriptions.get(template_type, 'A professional website template')
