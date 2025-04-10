"""
Views for the website manager app.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Website, Asset, WebsiteVersion, ShareLink
from .serializers import (
    WebsiteSerializer, WebsiteDetailSerializer, WebsiteUpdateSerializer,
    AssetSerializer, WebsiteVersionSerializer
)
from utils.response_handler import build_success_response, build_error_response


class WebsiteListCreateView(APIView):
    """
    List all websites or create a new website.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """List all websites for the authenticated user"""
        websites = Website.objects.filter(user=request.user)
        serializer = WebsiteSerializer(websites, many=True)
        return build_success_response(serializer.data)
    
    def post(self, request, format=None):
        """Create a new website"""
        serializer = WebsiteDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user to the authenticated user
            serializer.save(user=request.user)
            return build_success_response(
                serializer.data, 
                message="Website created successfully", 
                status_code=status.HTTP_201_CREATED
            )
        return build_error_response(
            "Failed to create website", 
            details=serializer.errors
        )


class WebsiteDetailView(APIView):
    """
    Retrieve, update or delete a website.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def get(self, request, pk, format=None):
        """Retrieve a website"""
        website = self.get_object(pk, request.user)
        serializer = WebsiteDetailSerializer(website)
        return build_success_response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Update a website"""
        website = self.get_object(pk, request.user)
        serializer = WebsiteUpdateSerializer(website, data=request.data)
        
        if serializer.is_valid():
            # Create a version before updating
            WebsiteVersion.objects.create(
                website=website,
                version_number=WebsiteVersion.objects.filter(website=website).count() + 1,
                content=website.content,
                created_by=request.user
            )
            
            serializer.save()
            return build_success_response(
                serializer.data, 
                message="Website updated successfully"
            )
        return build_error_response(
            "Failed to update website", 
            details=serializer.errors
        )
    
    def delete(self, request, pk, format=None):
        """Delete a website"""
        website = self.get_object(pk, request.user)
        website.delete()
        return build_success_response(
            message="Website deleted successfully", 
            status_code=status.HTTP_204_NO_CONTENT
        )


class WebsiteContentUpdateView(APIView):
    """
    Update website content.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def put(self, request, pk, format=None):
        """Update website content"""
        website = self.get_object(pk, request.user)
        
        # Check if we're updating the full website or just content
        if 'title' in request.data or 'description' in request.data:
            # This is a full website update with content
            if 'title' in request.data:
                website.title = request.data['title']
            
            if 'description' in request.data:
                website.description = request.data['description']
        
        # Check for content update
        if 'content' not in request.data:
            return build_error_response("Content field is required")
        
        # Create a version before updating
        WebsiteVersion.objects.create(
            website=website,
            version_number=WebsiteVersion.objects.filter(website=website).count() + 1,
            content=website.content,
            created_by=request.user
        )
        
        website.content = request.data['content']
        website.updated_at = timezone.now()
        website.save()
        
        serializer = WebsiteDetailSerializer(website)
        return build_success_response(
            serializer.data, 
            message="Website updated successfully"
        )


class WebsitePublishView(APIView):
    """
    Publish a website.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def post(self, request, pk, format=None):
        """Publish a website"""
        website = self.get_object(pk, request.user)
        website.publish()
        serializer = WebsiteSerializer(website)
        
        return build_success_response(
            serializer.data, 
            message="Website published successfully"
        )


class WebsiteArchiveView(APIView):
    """
    Archive a website.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def post(self, request, pk, format=None):
        """Archive a website"""
        website = self.get_object(pk, request.user)
        website.archive()
        serializer = WebsiteSerializer(website)
        
        return build_success_response(
            serializer.data, 
            message="Website archived successfully"
        )


class AssetListCreateView(APIView):
    """
    List all assets or create a new asset for a website.
    """
    permission_classes = [IsAuthenticated]
    
    def get_website(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def get(self, request, website_id, format=None):
        """List all assets for a website"""
        website = self.get_website(website_id, request.user)
        assets = Asset.objects.filter(website=website)
        serializer = AssetSerializer(assets, many=True)
        return build_success_response(serializer.data)
    
    def post(self, request, website_id, format=None):
        """Create a new asset for a website"""
        website = self.get_website(website_id, request.user)
        serializer = AssetSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(website=website)
            return build_success_response(
                serializer.data, 
                message="Asset created successfully", 
                status_code=status.HTTP_201_CREATED
            )
        return build_error_response(
            "Failed to create asset", 
            details=serializer.errors
        )


class AssetDetailView(APIView):
    """
    Retrieve, update or delete an asset.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get asset by ID and check ownership"""
        return get_object_or_404(Asset, pk=pk, website__user=user)
    
    def get(self, request, pk, format=None):
        """Retrieve an asset"""
        asset = self.get_object(pk, request.user)
        serializer = AssetSerializer(asset)
        return build_success_response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Update an asset"""
        asset = self.get_object(pk, request.user)
        serializer = AssetSerializer(asset, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return build_success_response(
                serializer.data, 
                message="Asset updated successfully"
            )
        return build_error_response(
            "Failed to update asset", 
            details=serializer.errors
        )
    
    def delete(self, request, pk, format=None):
        """Delete an asset"""
        asset = self.get_object(pk, request.user)
        asset.delete()
        return build_success_response(
            message="Asset deleted successfully", 
            status_code=status.HTTP_204_NO_CONTENT
        )


class WebsiteVersionListView(APIView):
    """
    List all versions of a website.
    """
    permission_classes = [IsAuthenticated]
    
    def get_website(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def get(self, request, website_id, format=None):
        """List all versions of a website"""
        website = self.get_website(website_id, request.user)
        versions = WebsiteVersion.objects.filter(website=website)
        serializer = WebsiteVersionSerializer(versions, many=True)
        return build_success_response(serializer.data)


class WebsiteVersionRestoreView(APIView):
    """
    Restore a website to a previous version.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get version by ID and check ownership"""
        return get_object_or_404(WebsiteVersion, pk=pk, website__user=user)
    
    def post(self, request, pk, format=None):
        """Restore a website to a previous version"""
        version = self.get_object(pk, request.user)
        website = version.website
        
        # Create a new version with the current content
        new_version = WebsiteVersion.objects.create(
            website=website,
            version_number=WebsiteVersion.objects.filter(website=website).count() + 1,
            content=website.content,
            created_by=request.user
        )
        
        # Update website content with the version content
        website.content = version.content
        website.updated_at = timezone.now()
        website.save()
        
        serializer = WebsiteDetailSerializer(website)
        return build_success_response(
            serializer.data, 
            message=f"Website restored to version {version.version_number}"
        )


class WebsiteEditView(APIView):
    """
    Edit a website.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get website by ID and check ownership"""
        return get_object_or_404(Website, pk=pk, user=user)
    
    def get(self, request, pk, format=None):
        """Retrieve a website for editing"""
        website = self.get_object(pk, request.user)
        serializer = WebsiteDetailSerializer(website)
        return render(request, 'website_editor.html', {
            'website': serializer.data
        })