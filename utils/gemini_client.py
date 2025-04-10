"""
Google Gemini API client for AI content generation.
"""
import requests
import json
from django.conf import settings


class GeminiClient:
    """Client for interacting with the Google Gemini API"""
    
    def __init__(self):
        """Initialize the Gemini API client with API key"""
        self.api_key = settings.GEMINI_API_KEY
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def generate_content(self, prompt, temperature=0.7, max_tokens=4096):
        """
        Generate content using Gemini API.
        
        Args:
            prompt (str): The prompt to send to the API
            temperature (float): Controls randomness (0.0 to 1.0)
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            str: The generated text response
        """
        if not self.api_key:
            raise ValueError("Gemini API key is not configured")
        
        # For demo purposes, generate dummy content if API integration fails
        use_dummy_content = True
        
        if use_dummy_content:
            return self._generate_dummy_content(prompt)
            
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Parse response
            result = response.json()
            
            # Extract generated text
            try:
                generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
                return generated_text.strip()
            except (KeyError, IndexError) as e:
                print(f"Error parsing Gemini API response: {str(e)}")
                print(f"Response: {json.dumps(result, indent=2)}")
                return f"Error: Failed to parse response - {str(e)}"
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to Gemini API: {str(e)}")
            return self._generate_dummy_content(prompt)
            
    def _generate_dummy_content(self, prompt):
        """Generate dummy content for demo purposes"""
        print("Using dummy content generator because API call failed")
        
        if "business" in prompt.lower():
            business_type = "Coffee Shop"
            if "type" in prompt.lower():
                import random
                business_types = ["Coffee Shop", "Restaurant", "Retail Store", "Tech Startup", "Consulting Firm"]
                business_type = random.choice(business_types)
                
            # Generate a basic dummy response about a business
            return {
                "title": f"{business_type} Website",
                "header": {
                    "title": f"{business_type} Name",
                    "navigation": [
                        {"text": "Home", "url": "#"},
                        {"text": "About", "url": "#about"},
                        {"text": "Services", "url": "#services"},
                        {"text": "Contact", "url": "#contact"}
                    ]
                },
                "hero": {
                    "title": f"Welcome to Our {business_type}",
                    "subtitle": "Your one-stop solution for all your needs",
                    "button_text": "Learn More",
                    "button_url": "#about"
                },
                "features": {
                    "title": "Our Features",
                    "subtitle": "What makes us special",
                    "items": [
                        {
                            "title": "Quality Service",
                            "description": "We provide top-notch service to all our customers."
                        },
                        {
                            "title": "Affordable Prices",
                            "description": "Our prices are competitive and affordable."
                        },
                        {
                            "title": "24/7 Support",
                            "description": "We are available around the clock to assist you."
                        }
                    ]
                },
                "about": {
                    "title": "About Us",
                    "content": "We are a dedicated team of professionals committed to providing the best service to our customers. Founded in 2022, we have quickly established ourselves as leaders in our industry."
                },
                "services": {
                    "title": "Our Services",
                    "subtitle": "What we offer",
                    "items": [
                        {
                            "title": "Service 1",
                            "description": "Description of service 1."
                        },
                        {
                            "title": "Service 2",
                            "description": "Description of service 2."
                        },
                        {
                            "title": "Service 3",
                            "description": "Description of service 3."
                        }
                    ]
                },
                "testimonials": {
                    "title": "Testimonials",
                    "subtitle": "What our clients say",
                    "items": [
                        {
                            "quote": "Great service! Highly recommended.",
                            "name": "John Doe",
                            "title": "CEO, Company XYZ"
                        },
                        {
                            "quote": "Very professional and efficient.",
                            "name": "Jane Smith",
                            "title": "Marketing Director, ABC Inc."
                        }
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
                    "copyright": "© 2025 Company Name. All rights reserved."
                }
            }
        
        # Default dummy content
        return "This is a placeholder response generated because the API call failed. The actual content would be generated by the Gemini API."