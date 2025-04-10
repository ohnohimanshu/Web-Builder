"""
Admin configuration for website manager app.
"""
from django.contrib import admin
from .models import Website, ShareLink, Asset, WebsiteVersion


class AssetInline(admin.TabularInline):
    """Inline admin for assets"""
    model = Asset
    extra = 1


class ShareLinkInline(admin.TabularInline):
    """Inline admin for share links"""
    model = ShareLink
    extra = 1


class WebsiteVersionInline(admin.TabularInline):
    """Inline admin for website versions"""
    model = WebsiteVersion
    extra = 0
    readonly_fields = ('version_number', 'content', 'created_at', 'created_by')
    max_num = 0
    can_delete = False


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    """Admin for Website model"""
    list_display = ('title', 'user', 'status', 'created_at', 'updated_at', 'published_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    inlines = [AssetInline, ShareLinkInline, WebsiteVersionInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'user')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at', 'published_at')
        }),
        ('Content', {
            'fields': ('content', 'template', 'generation_request')
        }),
        ('Domain', {
            'fields': ('custom_domain',)
        }),
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """Admin for Asset model"""
    list_display = ('name', 'website', 'asset_type', 'created_at')
    list_filter = ('asset_type', 'created_at')
    search_fields = ('name', 'website__title')


@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    """Admin for ShareLink model"""
    list_display = ('website', 'uuid', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('website__title',)
    readonly_fields = ('uuid', 'created_at')


@admin.register(WebsiteVersion)
class WebsiteVersionAdmin(admin.ModelAdmin):
    """Admin for WebsiteVersion model"""
    list_display = ('website', 'version_number', 'created_at', 'created_by')
    list_filter = ('created_at',)
    search_fields = ('website__title',)
    readonly_fields = ('website', 'version_number', 'content', 'created_at', 'created_by')