"""
Views for the website generator app.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Template, GenerationPrompt, GenerationRequest
from .serializers import (
    TemplateSerializer, GenerationPromptSerializer, 
    GenerationRequestSerializer, WebsiteGenerationInputSerializer
)
from .ai_service import generate_website_content
from website_manager.models import Website
from website_manager.serializers import WebsiteDetailSerializer
from utils.response_handler import build_success_response, build_error_response


class TemplateListView(APIView):
    """
    List all templates.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """List all active templates"""
        templates = Template.objects.filter(is_active=True)
        serializer = TemplateSerializer(templates, many=True)
        return build_success_response(serializer.data)


class TemplateDetailView(APIView):
    """
    Retrieve a template.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, format=None):
        """Retrieve a template"""
        template = get_object_or_404(Template, pk=pk, is_active=True)
        serializer = TemplateSerializer(template)
        return build_success_response(serializer.data)


class GenerateWebsiteView(APIView):
    """
    Generate a website using AI.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        """Generate a website"""
        # Validate input data
        input_serializer = WebsiteGenerationInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return build_error_response(
                "Invalid generation input", 
                details=input_serializer.errors
            )
        
        # Get validated data
        business_type = input_serializer.validated_data['business_type']
        industry = input_serializer.validated_data['industry']
        target_audience = input_serializer.validated_data['target_audience']
        key_features = input_serializer.validated_data['key_features']
        additional_info = input_serializer.validated_data.get('additional_info', '')
        template_id = input_serializer.validated_data.get('template_id')
        
        try:
            # Get template if provided
            template = None
            if template_id:
                template = get_object_or_404(Template, pk=template_id, is_active=True)
            
            # Create generation request
            generation_request = GenerationRequest.objects.create(
                user=request.user,
                business_type=business_type,
                industry=industry,
                target_audience=target_audience,
                key_features=key_features,
                additional_info=additional_info,
                template=template,
                status='processing'
            )
            
            # Generate website content
            try:
                # Set status to processing
                generation_request.status = 'processing'
                generation_request.save()
                
                # Generate content
                content = generate_website_content(generation_request)
                
                # Create website
                website = Website.objects.create(
                    user=request.user,
                    title=f"{business_type} - {industry}",
                    description=f"AI-generated website for {business_type} in the {industry} industry",
                    content=content,
                    status='draft',
                    template=template,
                    generation_request=generation_request
                )
                
                # Update generation request status
                generation_request.status = 'completed'
                generation_request.save()
                
                # Return response
                serializer = WebsiteDetailSerializer(website)
                return build_success_response(
                    serializer.data, 
                    message="Website generated successfully", 
                    status_code=status.HTTP_201_CREATED
                )
                
            except Exception as e:
                # Update generation request status
                generation_request.status = 'failed'
                generation_request.save()
                
                return build_error_response(
                    f"Failed to generate website content: {str(e)}", 
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return build_error_response(
                f"Failed to generate website: {str(e)}", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegenerateWebsiteSectionView(APIView):
    """
    Regenerate a section of a website using AI.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get generation request by ID and check ownership"""
        return get_object_or_404(GenerationRequest, pk=pk, user=user)
    
    def post(self, request, pk, section_type, format=None):
        """Regenerate a section"""
        # Validate section type
        valid_sections = ['header', 'hero', 'about', 'features', 'services', 'testimonials', 'contact', 'footer']
        if section_type not in valid_sections:
            return build_error_response(
                f"Invalid section type. Valid options are: {', '.join(valid_sections)}"
            )
        
        # Get generation request
        generation_request = self.get_object(pk, request.user)
        
        try:
            # Regenerate the section
            section_content = generate_website_content(
                generation_request, 
                section_only=True, 
                section_type=section_type
            )
            
            # Update the website content
            websites = Website.objects.filter(generation_request=generation_request)
            if websites.exists():
                website = websites.first()
                
                # Create a new version before updating
                from website_manager.models import WebsiteVersion
                WebsiteVersion.objects.create(
                    website=website,
                    version_number=WebsiteVersion.objects.filter(website=website).count() + 1,
                    content=website.content,
                    created_by=request.user
                )
                
                # Update only the specified section
                website.content[section_type] = section_content[section_type]
                website.save()
                
                serializer = WebsiteDetailSerializer(website)
                return build_success_response(
                    serializer.data, 
                    message=f"Section '{section_type}' regenerated successfully"
                )
            else:
                return build_error_response(
                    "No website found for this generation request",
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return build_error_response(
                f"Failed to regenerate section: {str(e)}", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerationRequestListView(APIView):
    """
    List all generation requests.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """List all generation requests for the authenticated user"""
        requests = GenerationRequest.objects.filter(user=request.user)
        serializer = GenerationRequestSerializer(requests, many=True)
        return build_success_response(serializer.data)


class GenerationRequestDetailView(APIView):
    """
    Retrieve a generation request.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        """Get generation request by ID and check ownership"""
        return get_object_or_404(GenerationRequest, pk=pk, user=user)
    
    def get(self, request, pk, format=None):
        """Retrieve a generation request"""
        generation_request = self.get_object(pk, request.user)
        serializer = GenerationRequestSerializer(generation_request)
        return build_success_response(serializer.data)


    from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class WebsiteContentUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk, format=None):
        try:
            website = self.get_object(pk, request.user)
            
            if 'content' not in request.data:
                return Response(
                    {"detail": "Content field is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create version before updating
            WebsiteVersion.objects.create(
                website=website,
                version_number=WebsiteVersion.objects.filter(website=website).count() + 1,
                content=website.content,
                created_by=request.user
            )

            website.content = request.data['content']
            website.save()

            serializer = WebsiteDetailSerializer(website)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError):
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    