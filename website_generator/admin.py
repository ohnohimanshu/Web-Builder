"""
Admin configuration for website generator app.
"""
from django.contrib import admin
from .models import Template, GenerationPrompt, GenerationRequest


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """Admin for Template model"""
    list_display = ('name', 'category', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')


@admin.register(GenerationPrompt)
class GenerationPromptAdmin(admin.ModelAdmin):
    """Admin for GenerationPrompt model"""
    list_display = ('name', 'section_type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('section_type', 'is_active')
    search_fields = ('name', 'description', 'prompt_text')


@admin.register(GenerationRequest)
class GenerationRequestAdmin(admin.ModelAdmin):
    """Admin for GenerationRequest model"""
    list_display = ('user', 'business_type', 'industry', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'industry')
    search_fields = ('business_type', 'industry', 'target_audience')
    readonly_fields = ('user', 'created_at', 'updated_at')