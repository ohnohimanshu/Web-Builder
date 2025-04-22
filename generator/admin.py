from django.contrib import admin
from .models import (
    WebsiteTemplate, 
    CustomizationField, 
    UserWebsite, 
    WebsiteCustomization, 
    GeneratedWebsite,
    AIPromptTemplate
)

class CustomizationFieldInline(admin.TabularInline):
    model = CustomizationField
    extra = 1

@admin.register(WebsiteTemplate)
class WebsiteTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    inlines = [CustomizationFieldInline]

@admin.register(CustomizationField)
class CustomizationFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'template', 'field_type', 'required', 'order')
    list_filter = ('template', 'field_type', 'required')
    search_fields = ('label', 'name', 'help_text')
    ordering = ('template', 'order')

class WebsiteCustomizationInline(admin.TabularInline):
    model = WebsiteCustomization
    extra = 1

@admin.register(UserWebsite)
class UserWebsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'template', 'created_at')
    search_fields = ('name', 'user__username')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [WebsiteCustomizationInline]

@admin.register(WebsiteCustomization)
class WebsiteCustomizationAdmin(admin.ModelAdmin):
    list_display = ('website', 'field', 'value')
    list_filter = ('website', 'field')
    search_fields = ('website__name', 'field__label', 'value')

@admin.register(GeneratedWebsite)
class GeneratedWebsiteAdmin(admin.ModelAdmin):
    list_display = ('website', 'generated_at')
    search_fields = ('website__name',)

@admin.register(AIPromptTemplate)
class AIPromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description', 'prompt_template')
