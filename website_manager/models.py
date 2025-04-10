"""
Models for the website manager app.
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Website(models.Model):
    """Model for storing websites"""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='websites')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    template = models.ForeignKey('website_generator.Template', on_delete=models.SET_NULL, null=True, blank=True)
    generation_request = models.ForeignKey('website_generator.GenerationRequest', on_delete=models.SET_NULL, 
                                          null=True, blank=True, related_name='generated_websites')
    custom_domain = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def publish(self):
        """Publish the website"""
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()
    
    def archive(self):
        """Archive the website"""
        self.status = 'archived'
        self.save()
    
    class Meta:
        ordering = ['-updated_at']


class ShareLink(models.Model):
    """Model for storing website share links"""
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='share_links')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Share link for {self.website.title}"
    
    def is_expired(self):
        """Check if the share link is expired"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at


class Asset(models.Model):
    """Model for storing website assets"""
    
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('other', 'Other')
    )
    
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='assets')
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class WebsiteVersion(models.Model):
    """Model for storing website versions for history tracking"""
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    content = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.website.title} - Version {self.version_number}"
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ['website', 'version_number']