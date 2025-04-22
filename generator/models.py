from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import json
import os
from django.utils import timezone
from django.utils.timezone import now

class WebsiteTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('blog', 'Blog'),
        ('portfolio', 'Portfolio'),
        ('business', 'Business'),
        ('ecommerce', 'E-commerce'),
    ]
    
    TEMPLATE_DESCRIPTIONS = {
        'blog': 'Perfect for personal blogs, news sites, and content creators',
        'portfolio': 'Ideal for showcasing your work and projects',
        'business': 'Great for corporate websites and professional services',
        'ecommerce': 'Designed for online stores and product showcases',
    }
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    html_structure = models.TextField()
    css_structure = models.TextField()
    js_structure = models.TextField(blank=True, null=True)
    preview_image = models.ImageField(upload_to='template_previews/', blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    features = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_template_type_icon(self):
        icons = {
            'blog': 'fas fa-blog',
            'portfolio': 'fas fa-briefcase',
            'business': 'fas fa-building',
            'ecommerce': 'fas fa-shopping-cart',
        }
        return icons.get(self.template_type, 'fas fa-globe')
    
    def get_features(self):
        return self.features

class CustomizationField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text'),
        ('textarea', 'Text Area'),
        ('color', 'Color Picker'),
        ('image', 'Image Upload'),
        ('select', 'Select Options'),
        ('checkbox', 'Checkbox'),
    )
    
    template = models.ForeignKey(WebsiteTemplate, on_delete=models.CASCADE, related_name='customization_fields')
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    options = models.TextField(blank=True, null=True, help_text="JSON array of options for select fields")
    required = models.BooleanField(default=False)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.template.name} - {self.label}"
    
    def get_options_list(self):
        if self.options and self.field_type == 'select':
            return json.loads(self.options)
        return []

class UserWebsite(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    template = models.ForeignKey(WebsiteTemplate, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/preview/{self.slug}/"

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

class WebsiteCustomization(models.Model):
    website = models.ForeignKey(UserWebsite, on_delete=models.CASCADE, related_name='customizations')
    field = models.ForeignKey(CustomizationField, on_delete=models.CASCADE)
    value = models.TextField()
    specifications = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Customizations for {self.website.name}"

class GeneratedWebsite(models.Model):
    website = models.OneToOneField(UserWebsite, on_delete=models.CASCADE, related_name='generated')
    html_content = models.TextField()
    css_content = models.TextField()
    js_content = models.TextField(blank=True, null=True)
    assets_directory = models.CharField(max_length=255, blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Generated content for {self.website.name}"
    
    def get_assets_path(self):
        if self.assets_directory:
            return os.path.join('generated_websites', self.assets_directory)
        return None

class AIPromptTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    prompt_template = models.TextField(help_text="Template with placeholders for AI generation")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
