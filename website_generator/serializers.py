"""
Serializers for the website generator app.
"""
from rest_framework import serializers
from .models import Template, GenerationPrompt, GenerationRequest


class TemplateSerializer(serializers.ModelSerializer):
    """Serializer for the Template model"""
    
    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'category', 'template_path', 'thumbnail_url']


class GenerationPromptSerializer(serializers.ModelSerializer):
    """Serializer for the GenerationPrompt model"""
    
    class Meta:
        model = GenerationPrompt
        fields = ['id', 'name', 'description', 'prompt_text', 'section_type']


class GenerationRequestSerializer(serializers.ModelSerializer):
    """Serializer for the GenerationRequest model"""
    template_name = serializers.SerializerMethodField()
    
    class Meta:
        model = GenerationRequest
        fields = [
            'id', 'business_type', 'industry', 'target_audience', 
            'key_features', 'additional_info', 'template', 'template_name',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']
    
    def get_template_name(self, obj):
        """Get template name if template exists"""
        if obj.template:
            return obj.template.name
        return None


class WebsiteGenerationInputSerializer(serializers.Serializer):
    """Serializer for website generation input"""
    business_type = serializers.CharField(max_length=100)
    industry = serializers.CharField(max_length=100)
    target_audience = serializers.CharField()
    key_features = serializers.CharField()
    additional_info = serializers.CharField(required=False, allow_blank=True)
    template_id = serializers.IntegerField(required=False, allow_null=True)