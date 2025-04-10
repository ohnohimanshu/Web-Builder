"""
URL patterns for the preview engine app.
"""
from django.urls import path
from .views import preview_website, shared_preview, create_share_link 
from . import views  # Fixed the space after 'from'

urlpatterns = [
    path('<int:website_id>/', preview_website, name='preview_website'),
    path('share/<uuid:share_uuid>/', shared_preview, name='shared_preview'),
    path('<int:website_id>/share/', create_share_link, name='create_share_link'),
    path('api/placeholder/<int:width>/<int:height>', views.PlaceholderImageView.as_view(), name='placeholder-image'),
]