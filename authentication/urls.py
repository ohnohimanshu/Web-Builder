"""
URL patterns for the authentication app.
"""
from django.urls import path
from .views import (
    RegisterView, 
    CustomTokenObtainPairView, 
    CustomTokenRefreshView, 
    UserProfileView,
    LogoutView,
    PasswordResetView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
]
