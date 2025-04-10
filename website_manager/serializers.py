"""
Serializers for the website manager app.
"""
from rest_framework import serializers
from .models import Website, Asset, WebsiteVersion


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for the Asset model"""
    
    class Meta:
        model = Asset
        fields = ['id', 'name', 'asset_type', 'file_url', 'created_at']
        read_only_fields = ['id', 'created_at']


class WebsiteSerializer(serializers.ModelSerializer):
    """Serializer for the Website model (list view)"""
    assets_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Website
        fields = [
            'id', 'title', 'description', 'status', 
            'created_at', 'updated_at', 'published_at', 'assets_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'published_at']
    
    def get_assets_count(self, obj):
        """Get count of assets for the website"""
        return obj.assets.count()


class WebsiteDetailSerializer(serializers.ModelSerializer):
    """Serializer for the Website model (detail view)"""
    assets = AssetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Website
        fields = [
            'id', 'title', 'description', 'content', 'status', 
            'custom_domain', 'created_at', 'updated_at', 'published_at',
            'assets'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'published_at'
        ]


class WebsiteUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Website"""
    
    class Meta:
        model = Website
        fields = [
            'title', 'description', 'content', 'status', 'custom_domain'
        ]
    
    def validate_custom_domain(self, value):
        """Validate custom domain format"""
        if value and not value.strip():
            return None
        return value


class WebsiteVersionSerializer(serializers.ModelSerializer):
    """Serializer for the WebsiteVersion model"""
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = WebsiteVersion
        fields = [
            'id', 'website', 'version_number', 'content', 
            'created_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = [
            'id', 'website', 'version_number', 'content', 
            'created_at', 'created_by', 'created_by_name'
        ]
    
    def get_created_by_name(self, obj):
        """Get name of the user who created the version"""
        if obj.created_by:
            return obj.created_by.name
        return None