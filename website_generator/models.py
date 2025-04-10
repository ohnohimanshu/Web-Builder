"""
Models for the website generator app.
"""
from django.db import models
from django.conf import settings


class Template(models.Model):
    """Model for website templates"""
    
    CATEGORY_CHOICES = (
        ('business', 'Business'),
        ('portfolio', 'Portfolio'),
        ('blog', 'Blog'),
        ('shop', 'E-commerce'),
        ('landing', 'Landing Page'),
        ('other', 'Other')
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    template_path = models.CharField(max_length=255)
    thumbnail_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class GenerationPrompt(models.Model):
    """Model for storing AI generation prompts"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    prompt_text = models.TextField()
    section_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.section_type}"


class GenerationRequest(models.Model):
    """Model for tracking website generation requests"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    target_audience = models.TextField()
    key_features = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Generation for {self.user.email} - {self.business_type} ({self.status})"
