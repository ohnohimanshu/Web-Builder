"""
URL configuration for website_builder project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import status
import os
from .home_views import dashboard_view

def api_root(request):
    """API root endpoint to check if the API is running"""
    return JsonResponse({
        'status': 'ok',
        'message': 'AI Website Builder API is running'
    }, status=status.HTTP_200_OK)

def serve_api_tester(request):
    """Serve the API tester HTML page"""
    file_path = os.path.join(settings.BASE_DIR, 'static/register.html')
    return FileResponse(open(file_path, 'rb'))

def redirect_to_dashboard(request):
    """Redirect root URL to dashboard"""
    return redirect('dashboard')

urlpatterns = [
    path('', redirect_to_dashboard, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/auth/', include('authentication.urls')),
    path('api/generator/', include('website_generator.urls')),
    path('api/websites/', include('website_manager.urls')),
    path('preview/', include('preview_engine.urls')),
    path('api-tester/', serve_api_tester, name='api_tester'),
    path('home/dashboard/', dashboard_view, name='dashboard'),
]

# Add Django's static file handling
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
