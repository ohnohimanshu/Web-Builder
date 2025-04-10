"""
Views for the home dashboard
"""
from django.shortcuts import render
from django.http import FileResponse
import os
from django.conf import settings

def dashboard_view(request):
    """Serve the dashboard HTML page"""
    template_path = os.path.join(settings.BASE_DIR, 'templates/home/dashboard.html')
    return FileResponse(open(template_path, 'rb'))