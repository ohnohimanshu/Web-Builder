"""
URL patterns for the website manager app.
"""
from django.urls import path
from .views import (
    WebsiteListCreateView, WebsiteDetailView, WebsiteContentUpdateView,
    WebsitePublishView, WebsiteArchiveView,
    AssetListCreateView, AssetDetailView,
    WebsiteVersionListView, WebsiteVersionRestoreView
)
from . import views

urlpatterns = [
    # Website endpoints
    path('', WebsiteListCreateView.as_view(), name='website-list-create'),
    path('<int:pk>/', WebsiteDetailView.as_view(), name='website-detail'),
    path('<int:pk>/update/', WebsiteContentUpdateView.as_view(), name='website-content-update'),
    path('<int:pk>/publish/', WebsitePublishView.as_view(), name='website-publish'),
    path('<int:pk>/archive/', WebsiteArchiveView.as_view(), name='website-archive'),
    
    # Asset endpoints
    path('<int:website_id>/assets/', AssetListCreateView.as_view(), name='asset-list-create'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    
    # Version endpoints
    path('<int:website_id>/versions/', WebsiteVersionListView.as_view(), name='website-version-list'),
    path('versions/<int:pk>/restore/', WebsiteVersionRestoreView.as_view(), name='website-version-restore'),
    
    # Add this URL pattern to your existing urlpatterns
    path('<int:pk>/edit/', views.WebsiteEditView.as_view(), name='website-edit'),
]