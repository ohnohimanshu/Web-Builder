"""
Views for website preview functionality.
"""
"""
Views for website preview functionality.
"""
import uuid
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView  # Add this import

from website_manager.models import Website
from .template_engine_new import render_website

# ... rest of the code remains the same ...


def preview_website(request, website_id):
    """Preview a website (authenticated, with controls)"""
    try:
        # Try to get authentication token from various sources
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header and 'auth_token' in request.GET:
            auth_header = f"Bearer {request.GET.get('auth_token')}"
        
        # Get user from token if present
        user = None
        if auth_header.startswith('Bearer '):
            from rest_framework_simplejwt.tokens import AccessToken
            from django.contrib.auth import get_user_model
            try:
                token = auth_header.split(' ')[1]
                token_obj = AccessToken(token)
                user_id = token_obj['user_id']
                User = get_user_model()
                user = User.objects.get(id=user_id)
            except Exception as e:
                print(f"Token validation error: {str(e)}")
        
        # Check if user exists and owns the website
        if user:
            website = get_object_or_404(Website, id=website_id, user=user)
        else:
            # For demo purposes, allow preview without authentication
            website = get_object_or_404(Website, id=website_id)
        
        # Render website using template engine
        html_content = render_website(website)
        
        # Add script to handle authentication for the preview
        auth_script = """
        <script>
        // Automatically add Authorization header to all fetch/XHR requests
        (function() {
            // Get token from localStorage
            const token = localStorage.getItem('access_token');
            
            if (token) {
                // Override fetch
                const originalFetch = window.fetch;
                window.fetch = function(url, options) {
                    options = options || {};
                    options.headers = options.headers || {};
                    options.headers['Authorization'] = `Bearer ${token}`;
                    return originalFetch(url, options);
                };
                
                // Override XMLHttpRequest
                const originalXHROpen = XMLHttpRequest.prototype.open;
                XMLHttpRequest.prototype.open = function() {
                    const result = originalXHROpen.apply(this, arguments);
                    this.setRequestHeader('Authorization', `Bearer ${token}`);
                    return result;
                };
            }
        })();
        </script>
        """
        
        # Insert auth script before closing head tag
        html_content = html_content.replace('</head>', f'{auth_script}</head>')
        
        # Return rendered HTML
        return HttpResponse(html_content)
        
    except Website.DoesNotExist:
        return JsonResponse(
            {"detail": "Website not found or access denied"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"detail": f"Error rendering website: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def shared_preview(request, share_uuid):
    """Public shared preview (no authentication required)"""
    try:
        # Get website by share UUID
        from django.db.models import Q
        website = Website.objects.filter(
            Q(share_links__uuid=share_uuid) & 
            (Q(share_links__expires_at__gt=timezone.now()) | Q(share_links__expires_at=None))
        ).first()
        
        if not website:
            raise Http404("Shared preview link is invalid or has expired")
        
        # Render website using template engine
        html_content = render_website(website, is_public=True)
        
        # Return rendered HTML
        return HttpResponse(html_content)
        
    except Http404:
        return HttpResponse("Shared preview link is invalid or has expired", status=404)
    except Exception as e:
        return HttpResponse(f"Error rendering website: {str(e)}", status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_share_link(request, website_id):
    """Create a shareable preview link"""
    try:
        # Check if user owns the website
        website = get_object_or_404(Website, id=website_id, user=request.user)
        
        # Get expiry time from request (optional)
        expires_days = request.data.get('expires_days')
        if expires_days:
            try:
                expires_days = int(expires_days)
                expires_at = timezone.now() + timezone.timedelta(days=expires_days)
            except (ValueError, TypeError):
                expires_at = None
        else:
            expires_at = None
        
        # Create share link (mock implementation since we don't have a ShareLink model yet)
        share_uuid = uuid.uuid4()
        
        # In a real implementation, you would create a ShareLink model instance here
        # For now, let's return the UUID directly
        
        # Build the full shareable URL
        share_url = request.build_absolute_uri(f'/preview/share/{share_uuid}/')
        
        return Response({
            "detail": "Share link created successfully",
            "share_url": share_url,
            "expires_at": expires_at
        }, status=status.HTTP_201_CREATED)
        
    except Website.DoesNotExist:
        return Response(
            {"detail": "Website not found or access denied"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"detail": f"Error creating share link: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



from django.http import HttpResponse
from PIL import Image
import io

class PlaceholderImageView(APIView):
    """Generate placeholder images for preview"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, width, height):
        """Generate a placeholder image with specified dimensions"""
        try:
            # Create a new image with a gradient background
            image = Image.new('RGB', (int(width), int(height)), '#f3f4f6')
            
            # Save the image to a bytes buffer
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Return the image
            return HttpResponse(
                buffer.getvalue(),
                content_type='image/png'
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )