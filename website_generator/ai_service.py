"""
AI service for website content generation using Google Gemini API.
"""
import json
import re
from django.conf import settings
from utils.gemini_client import GeminiClient


def generate_website_content(generation_request, section_only=False, section_type=None):
    """
    Generate website content using Gemini API based on user inputs.
    
    Args:
        generation_request (GenerationRequest): The generation request object
        section_only (bool): Whether to generate only a specific section
        section_type (str): The type of section to generate (if section_only is True)
    
    Returns:
        dict: Generated content structure
    """
    # Extract data from the generation request
    business_type = generation_request.business_type
    industry = generation_request.industry
    target_audience = generation_request.target_audience
    key_features = generation_request.key_features
    additional_info = generation_request.additional_info or ''
    
    # Initialize Gemini API client
    client = GeminiClient()
    
    if section_only and section_type:
        # Generate just one section
        return generate_single_section(client, business_type, industry, target_audience, 
                                     key_features, additional_info, section_type)
    else:
        # Generate full website
        return generate_full_website(client, business_type, industry, target_audience, 
                                    key_features, additional_info)


def generate_full_website(client, business_type, industry, target_audience, key_features, additional_info):
    """
    Generate a complete website structure.
    
    Returns:
        dict: Complete website content structure
    """
    # Check if Gemini API key is configured
    if not settings.GEMINI_API_KEY:
        # If no API key, return a dummy content structure
        return generate_dummy_content(business_type, industry)
    
    # Construct the prompt for the AI
    prompt = f"""
    You are a professional website content generator. Create complete content for a website based on the following information:
    
    Business Type: {business_type}
    Industry: {industry}
    Target Audience: {target_audience}
    Key Features/Offerings: {key_features}
    Additional Information: {additional_info}
    
    Generate a complete website content structure formatted as a JSON object with the following sections:
    - title: The website title
    - header: Navigation and logo information
      - title: Header title/company name
      - navigation: Array of navigation items (each with text and url)
    - hero: Hero section
      - title: Main heading
      - subtitle: Subheading or tagline
      - button_text: Call to action text
      - button_url: Link for the button (use # for placeholder)
    - about: About section
      - title: Section heading
      - content: Company description
    - features: Features section
      - title: Section heading
      - subtitle: Section description
      - items: Array of features (each with title and description)
    - services: Services section
      - title: Section heading
      - subtitle: Section description
      - items: Array of services (each with title and description)
    - testimonials: Testimonials section
      - title: Section heading
      - subtitle: Section description
      - items: Array of testimonials (each with quote, name, and title)
    - contact: Contact section
      - title: Section heading
      - subtitle: Section description
      - email: Contact email
      - phone: Contact phone
      - address: Physical address
    - footer: Footer information
      - copyright: Copyright text
    
    The content should be relevant to the business type, industry, and target audience. Make it professional, engaging, and optimized for conversion.
    
    Output only the JSON object with no additional text or explanation.
    """
    
    try:
        # Send request to Gemini API
        response = client.generate_content(prompt, temperature=0.7)
        
        # Check if response is already a dictionary (from dummy generator)
        if isinstance(response, dict):
            return response
            
        # Extract JSON from the response if it's a string
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
            content = json.loads(json_str)
            return content
        else:
            # Fallback to dummy content if JSON parsing fails
            return generate_dummy_content(business_type, industry)
    
    except Exception as e:
        # Log the error and return dummy content
        print(f"Error generating content with Gemini API: {str(e)}")
        return generate_dummy_content(business_type, industry)


def generate_single_section(client, business_type, industry, target_audience, 
                            key_features, additional_info, section_type):
    """
    Generate content for a specific section.
    
    Args:
        section_type (str): The type of section to generate
    
    Returns:
        dict: The section content
    """
    # Check if Gemini API key is configured
    if not settings.GEMINI_API_KEY:
        # If no API key, return dummy section content
        dummy_content = generate_dummy_content(business_type, industry)
        return {section_type: dummy_content.get(section_type, {})}
    
    # Construct the prompt for the AI
    prompt = f"""
    You are a professional website content generator. Create content for the '{section_type}' section of a website based on the following information:
    
    Business Type: {business_type}
    Industry: {industry}
    Target Audience: {target_audience}
    Key Features/Offerings: {key_features}
    Additional Information: {additional_info}
    
    Generate the content for the '{section_type}' section only, formatted as a JSON object with the appropriate structure for that section:
    
    For 'header':
    {{
      "title": "Company Name",
      "navigation": [
        {{ "text": "Home", "url": "#" }},
        {{ "text": "About", "url": "#about" }},
        ...
      ]
    }}
    
    For 'hero':
    {{
      "title": "Main heading",
      "subtitle": "Subheading",
      "button_text": "Call to action",
      "button_url": "#"
    }}
    
    For 'about':
    {{
      "title": "About Us",
      "content": "Detailed company description"
    }}
    
    For 'features':
    {{
      "title": "Features",
      "subtitle": "What makes us special",
      "items": [
        {{ "title": "Feature 1", "description": "Description 1" }},
        {{ "title": "Feature 2", "description": "Description 2" }},
        ...
      ]
    }}
    
    For 'services':
    {{
      "title": "Our Services",
      "subtitle": "What we offer",
      "items": [
        {{ "title": "Service 1", "description": "Description 1" }},
        {{ "title": "Service 2", "description": "Description 2" }},
        ...
      ]
    }}
    
    For 'testimonials':
    {{
      "title": "Testimonials",
      "subtitle": "What our clients say",
      "items": [
        {{ "quote": "Great service!", "name": "Client Name", "title": "Position" }},
        {{ "quote": "Amazing results!", "name": "Client Name", "title": "Position" }},
        ...
      ]
    }}
    
    For 'contact':
    {{
      "title": "Contact Us",
      "subtitle": "Get in touch",
      "email": "info@example.com",
      "phone": "+1 234 567 890",
      "address": "123 Street, City, Country"
    }}
    
    For 'footer':
    {{
      "copyright": "© 2025 Company Name. All rights reserved."
    }}
    
    The content should be relevant to the business type, industry, and target audience. Make it professional, engaging, and optimized for conversion.
    
    Output only the JSON object for the requested section with no additional text or explanation.
    """
    
    try:
        # Send request to Gemini API
        response = client.generate_content(prompt, temperature=0.7)
        
        # Check if response is already a dictionary (from dummy generator)
        if isinstance(response, dict):
            # If it's already a dict, return it wrapped in the section type
            return {section_type: response}
        
        # Extract JSON from the response if it's a string
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
            section_content = json.loads(json_str)
            return {section_type: section_content}
        else:
            # Fallback to dummy content if JSON parsing fails
            dummy_content = generate_dummy_content(business_type, industry)
            return {section_type: dummy_content.get(section_type, {})}
    
    except Exception as e:
        # Log the error and return dummy content
        print(f"Error generating section content with Gemini API: {str(e)}")
        dummy_content = generate_dummy_content(business_type, industry)
        return {section_type: dummy_content.get(section_type, {})}


def generate_dummy_content(business_type, industry):
    """
    Generate a dummy content structure when the API is unavailable.
    
    Args:
        business_type (str): The type of business
        industry (str): The industry
        
    Returns:
        dict: A basic content structure
    """
    return {
        "title": f"{business_type} - {industry}",
        "header": {
            "title": f"{business_type}",
            "navigation": [
                {"text": "Home", "url": "#"},
                {"text": "About", "url": "#about"},
                {"text": "Services", "url": "#services"},
                {"text": "Contact", "url": "#contact"}
            ]
        },
        "hero": {
            "title": f"Welcome to {business_type}",
            "subtitle": f"Your trusted partner in the {industry} industry",
            "button_text": "Learn More",
            "button_url": "#about"
        },
        "about": {
            "title": "About Us",
            "content": f"We are a leading {business_type} in the {industry} industry, dedicated to providing exceptional products and services to our clients. With years of experience and a team of experts, we strive for excellence in everything we do."
        },
        "features": {
            "title": "Our Features",
            "subtitle": "What makes us special",
            "items": [
                {"title": "Quality", "description": "We provide top-quality products and services"},
                {"title": "Expertise", "description": "Our team consists of industry experts"},
                {"title": "Customer Service", "description": "We are dedicated to customer satisfaction"},
                {"title": "Innovation", "description": "We stay ahead with innovative solutions"}
            ]
        },
        "services": {
            "title": "Our Services",
            "subtitle": "What we offer",
            "items": [
                {"title": "Service 1", "description": "Description of service 1"},
                {"title": "Service 2", "description": "Description of service 2"},
                {"title": "Service 3", "description": "Description of service 3"},
                {"title": "Service 4", "description": "Description of service 4"}
            ]
        },
        "testimonials": {
            "title": "Testimonials",
            "subtitle": "What our clients say",
            "items": [
                {"quote": "Great service and excellent results!", "name": "John Doe", "title": "CEO, Company A"},
                {"quote": "Professional team and amazing quality!", "name": "Jane Smith", "title": "Manager, Company B"}
            ]
        },
        "contact": {
            "title": "Contact Us",
            "subtitle": "Get in touch with us",
            "email": "info@example.com",
            "phone": "+1 234 567 890",
            "address": "123 Street, City, Country"
        },
        "footer": {
            "copyright": f"© {2025} {business_type}. All rights reserved."
        }
    }