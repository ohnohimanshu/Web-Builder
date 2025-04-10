"""
Serializers for the authentication app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'password_confirm', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        """Validate that passwords match"""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        """Create a new user"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer to include additional user data"""
    
    def validate(self, attrs):
        """Override validate to add additional data to the token"""
        data = super().validate(attrs)
        
        # Add extra user data to the response
        user = self.user
        data.update({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        })
        
        return data


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate that the user exists with the given email"""
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            # We don't reveal if the user exists or not for security reasons
            pass
        return value
    
    def save(self):
        """Generate password reset token and send reset email"""
        email = self.validated_data['email']
        # Even if the user doesn't exist, we pretend to send an email for security
        if hasattr(self, 'user'):
            user = self.user
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://localhost:5000/reset-password/{uid}/{token}/"
            
            # In a real application, you'd implement proper email sending
            # For this example, we'll just print the reset URL
            print(f"Password reset URL for {email}: {reset_url}")
            
            # Attempt to send email if SMTP is configured
            try:
                send_mail(
                    'Password Reset Request',
                    f'Please use the following link to reset your password: {reset_url}',
                    'noreply@websitebuilder.com',
                    [email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending error: {e}")
