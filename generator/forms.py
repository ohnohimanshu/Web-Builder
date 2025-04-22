from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserWebsite, WebsiteCustomization, CustomizationField
from .models import WebsiteTemplate

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class WebsiteCreationForm(forms.ModelForm):
    template = forms.ModelChoiceField(
        queryset=WebsiteTemplate.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserWebsite
        fields = ['name', 'description', 'template']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter website name'}),
        }

class CustomizationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        template = kwargs.pop('template', None)
        website = kwargs.pop('website', None)
        super().__init__(*args, **kwargs)
        
        if template:
            # Dynamically create form fields based on template's customization fields
            for field in template.customization_fields.all().order_by('order'):
                field_id = f'field_{field.id}'
                
                # Get existing value if website is provided
                initial_value = None
                if website:
                    try:
                        customization = WebsiteCustomization.objects.get(website=website, field=field)
                        initial_value = customization.value
                    except WebsiteCustomization.DoesNotExist:
                        initial_value = field.default_value
                else:
                    initial_value = field.default_value
                
                # Create the appropriate form field based on field type
                if field.field_type == 'text':
                    self.fields[field_id] = forms.CharField(
                        label=field.label,
                        required=field.required,
                        help_text=field.help_text,
                        initial=initial_value,
                        widget=forms.TextInput(attrs={'class': 'form-control'})
                    )
                elif field.field_type == 'textarea':
                    self.fields[field_id] = forms.CharField(
                        label=field.label,
                        required=field.required,
                        help_text=field.help_text,
                        initial=initial_value,
                        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
                    )
                elif field.field_type == 'color':
                    self.fields[field_id] = forms.CharField(
                        label=field.label,
                        required=field.required,
                        help_text=field.help_text,
                        initial=initial_value or '#000000',
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'color'})
                    )
                elif field.field_type == 'image':
                    self.fields[field_id] = forms.ImageField(
                        label=field.label,
                        required=field.required,
                        help_text=field.help_text,
                        widget=forms.FileInput(attrs={'class': 'form-control'})
                    )
                    # If there's an existing image, we can't show it in the form directly
                    # but we can handle it in the template
                elif field.field_type == 'select':
                    choices = [(option, option) for option in field.get_options_list()]
                    self.fields[field_id] = forms.ChoiceField(
                        label=field.label,
                        required=field.required,
                        help_text=field.help_text,
                        initial=initial_value,
                        choices=choices,
                        widget=forms.Select(attrs={'class': 'form-control'})
                    )
                elif field.field_type == 'checkbox':
                    self.fields[field_id] = forms.BooleanField(
                        label=field.label,
                        required=False,  # Checkboxes can't be required in HTML forms
                        help_text=field.help_text,
                        initial=initial_value == 'True' if initial_value else False,
                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
                    )

class AIContentGenerationForm(forms.Form):
    content_type = forms.ChoiceField(
        choices=[
            ('heading', 'Heading'),
            ('paragraph', 'Paragraph'),
            ('call_to_action', 'Call to Action'),
            ('feature_list', 'Feature List'),
            ('testimonial', 'Testimonial'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe what you want to generate...'}),
        help_text="Provide details about what you want the AI to generate"
    )
    tone = forms.ChoiceField(
        choices=[
            ('professional', 'Professional'),
            ('casual', 'Casual'),
            ('enthusiastic', 'Enthusiastic'),
            ('formal', 'Formal'),
            ('friendly', 'Friendly'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class WebsiteSpecificationsForm(forms.Form):
    # Basic Information
    site_title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., My Awesome Blog'})
    )
    tagline = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A short description of your website'})
    )
    
    # Contact Information
    contact_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@example.com'})
    )
    contact_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'})
    )
    
    # Social Media
    facebook_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/yourpage'})
    )
    twitter_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/yourhandle'})
    )
    instagram_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/yourprofile'})
    )
    
    # Color Scheme
    primary_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'color'})
    )
    secondary_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'color'})
    )
    
    # Content Preferences
    blog_posts_per_page = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=6,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    # Additional Features
    enable_comments = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    enable_search = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        template_type = kwargs.pop('template_type', None)
        super().__init__(*args, **kwargs)
        
        # Show/hide fields based on template type
        if template_type == 'blog':
            self.fields['blog_posts_per_page'].widget.attrs['class'] = 'form-control'
            self.fields['enable_comments'].widget.attrs['class'] = 'form-check-input'
        else:
            self.fields.pop('blog_posts_per_page')
            self.fields.pop('enable_comments')
            
        if template_type == 'business':
            self.fields['contact_email'].required = True
            self.fields['contact_phone'].required = True
        elif template_type == 'portfolio':
            self.fields['instagram_url'].required = True