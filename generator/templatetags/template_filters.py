from django import template

register = template.Library()

@register.filter
def get_template_icon(template_type):
    icons = {
        'blog': 'fas fa-blog',
        'portfolio': 'fas fa-briefcase',
        'business': 'fas fa-building',
        'ecommerce': 'fas fa-shopping-cart',
        'restaurant': 'fas fa-utensils',
        'event': 'fas fa-calendar-alt',
        'real_estate': 'fas fa-home',
        'education': 'fas fa-graduation-cap',
        'healthcare': 'fas fa-heartbeat',
        'nonprofit': 'fas fa-hands-helping',
        'personal': 'fas fa-user',
        'landing': 'fas fa-rocket',
    }
    return icons.get(template_type, 'fas fa-globe')

@register.filter
def get_template_description(template_type):
    descriptions = {
        'blog': 'personal blogs, news sites, and content creators',
        'portfolio': 'showcasing your work and projects',
        'business': 'corporate websites and professional services',
        'ecommerce': 'online stores and product showcases',
        'restaurant': 'menus, reservations, and food delivery',
        'event': 'conferences, weddings, and special occasions',
        'real_estate': 'property listings and real estate agencies',
        'education': 'schools, courses, and educational content',
        'healthcare': 'medical practices and health services',
        'nonprofit': 'charities and community organizations',
        'personal': 'personal branding and resumes',
        'landing': 'product launches and marketing campaigns',
    }
    return descriptions.get(template_type, 'general purpose websites') 