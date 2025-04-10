"""
Views for the authentication app.
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, CustomTokenObtainPairSerializer, PasswordResetSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain pair view for JWT authentication"""
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view for JWT authentication"""
    pass


class RegisterView(generics.CreateAPIView):
    """User registration view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    """Password reset view"""
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset email has been sent."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """View for user logout"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Client should delete the tokens on their side
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
