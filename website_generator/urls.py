"""
URL patterns for the website generator app.
"""
from django.urls import path
from .views import (
    TemplateListView, TemplateDetailView,
    GenerateWebsiteView, RegenerateWebsiteSectionView,
    GenerationRequestListView, GenerationRequestDetailView
)

urlpatterns = [
    # Template endpoints
    path('templates/', TemplateListView.as_view(), name='template-list'),
    path('templates/<int:pk>/', TemplateDetailView.as_view(), name='template-detail'),
    
    # Generation endpoints
    path('generate/', GenerateWebsiteView.as_view(), name='generate-website'),
    path('regenerate/<int:pk>/<str:section_type>/', RegenerateWebsiteSectionView.as_view(), name='regenerate-section'),
    
    # Generation request endpoints
    path('requests/', GenerationRequestListView.as_view(), name='generation-request-list'),
    path('requests/<int:pk>/', GenerationRequestDetailView.as_view(), name='generation-request-detail'),
]