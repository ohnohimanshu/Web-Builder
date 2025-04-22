from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_website, name='create_website'),
    path('specifications/', views.website_specifications, name='website_specifications'),
    path('preview/<int:website_id>/', views.preview_website, name='preview_website'),
    path('customize/<int:website_id>/', views.customize_website, name='customize_website'),
    path('generate-content/', views.generate_ai_content, name='generate_ai_content'),
    path('publish/<int:website_id>/', views.publish_website, name='publish_website'),
]