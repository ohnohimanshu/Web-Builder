from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.template import Template, Context
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserWebsite, WebsiteTemplate, WebsiteCustomization, GeneratedWebsite
from .forms import WebsiteCreationForm, CustomizationForm, AIContentGenerationForm, WebsiteSpecificationsForm
from django.contrib.auth.forms import UserCreationForm
import os
import json

def home(request):
    templates = WebsiteTemplate.objects.all().order_by('-created_at')
    return render(request, 'generator/home.html', {'templates': templates})

@login_required
def create_website(request):
    if request.method == 'POST':
        form = WebsiteCreationForm(request.POST)
        if form.is_valid():
            # Store the form data in session
            request.session['website_data'] = {
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'template_id': form.cleaned_data['template'].id,
                'template_type': form.cleaned_data['template'].template_type
            }
            return redirect('website_specifications')
    else:
        form = WebsiteCreationForm()
    
    # Get available templates
    templates = WebsiteTemplate.objects.all()
    if not templates.exists():
        messages.warning(request, 'No templates are available at the moment. Please contact the administrator.')
    
    return render(request, 'generator/create_website.html', {
        'form': form,
        'templates': templates,
        'template_types': WebsiteTemplate.TEMPLATE_TYPES,
        'template_descriptions': WebsiteTemplate.TEMPLATE_DESCRIPTIONS,
    })

@login_required
def website_specifications(request):
    # Check if we have the initial website data
    if 'website_data' not in request.session:
        messages.warning(request, 'Please select a template first.')
        return redirect('create_website')
    
    template_type = request.session['website_data']['template_type']
    
    if request.method == 'POST':
        form = WebsiteSpecificationsForm(request.POST, template_type=template_type)
        if form.is_valid():
            try:
                # Get the stored website data
                website_data = request.session['website_data']
                
                # Get template with error handling
                template = WebsiteTemplate.objects.filter(id=website_data['template_id']).first()
                if not template:
                    messages.error(request, 'Selected template no longer exists.')
                    return redirect('create_website')
                
                # Create the website
                website = UserWebsite.objects.create(
                    user=request.user,
                    name=website_data['name'],
                    description=website_data['description'],
                    template=template
                )
                
                # Create website customizations
                WebsiteCustomization.objects.create(
                    website=website,
                    specifications=form.cleaned_data
                )
                
                # Clear the session data
                del request.session['website_data']
                
                # Redirect to preview
                return redirect('preview_website', website_id=website.id)
                
            except Exception as e:
                messages.error(request, f'Error creating website: {str(e)}')
                return redirect('create_website')
    else:
        form = WebsiteSpecificationsForm(template_type=template_type)
    
    return render(request, 'generator/website_specifications.html', {
        'form': form,
        'template_type': template_type
    })

@login_required
def customize_website(request, website_id):
    website = get_object_or_404(UserWebsite, id=website_id, user=request.user)
    template = website.template
    
    if request.method == 'POST':
        form = CustomizationForm(request.POST, request.FILES, template=template, website=website)
        if form.is_valid():
            # Save customizations
            for field_name, value in form.cleaned_data.items():
                if field_name.startswith('field_'):
                    field_id = int(field_name.split('_')[1])
                    field = template.customization_fields.get(id=field_id)
                    
                    # Handle file uploads
                    if field.field_type == 'image' and value:
                        # Save the image and store its path
                        file_path = handle_uploaded_file(value, website)
                        value = file_path
                    
                    # Update or create customization
                    WebsiteCustomization.objects.update_or_create(
                        website=website,
                        field=field,
                        defaults={'value': str(value)}
                    )
            
            # Generate the website
            generate_website_content(website)
            return redirect('preview_website', website_id=website.id)
    else:
        form = CustomizationForm(template=template, website=website)
    
    return render(request, 'generator/customize_website.html', {
        'form': form,
        'website': website
    })

def handle_uploaded_file(f, website):
    # Create directory for website assets if it doesn't exist
    assets_dir = os.path.join(settings.MEDIA_ROOT, 'generated_websites', str(website.id), 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(assets_dir, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    # Return the relative path for storage
    return os.path.join('generated_websites', str(website.id), 'assets', f.name)

def generate_website_content(website):
    template = website.template
    customizations = website.customizations.all()
    
    # Create a context with all customizations
    context = {}
    for customization in customizations:
        field_name = customization.field.name
        value = customization.value
        context[field_name] = value
    
    # Render the template with customizations
    html_template = Template(template.html_structure)
    rendered_html = html_template.render(Context(context))
    
    # Process CSS with customizations
    css_template = Template(template.css_structure)
    rendered_css = css_template.render(Context(context))
    
    # Process JavaScript if present
    rendered_js = ''
    if template.js_structure:
        js_template = Template(template.js_structure)
        rendered_js = js_template.render(Context(context))
    
    # Save or update generated website
    generated, created = GeneratedWebsite.objects.update_or_create(
        website=website,
        defaults={
            'html_content': rendered_html,
            'css_content': rendered_css,
            'js_content': rendered_js,
            'assets_directory': str(website.id)
        }
    )

@login_required
def preview_website(request, website_id):
    website = get_object_or_404(UserWebsite, id=website_id, user=request.user)
    customizations = website.customizations.first()
    
    return render(request, 'generator/preview_website.html', {
        'website': website,
        'customizations': customizations
    })

@login_required
def publish_website(request, website_id):
    website = get_object_or_404(UserWebsite, id=website_id, user=request.user)
    
    if request.method == 'POST':
        website.status = 'published'
        website.published_at = timezone.now()
        website.save()
        return JsonResponse({'status': 'success', 'message': 'Website published successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def generate_ai_content(request):
    if request.method == 'POST':
        form = AIContentGenerationForm(request.POST)
        if form.is_valid():
            content_type = form.cleaned_data['content_type']
            description = form.cleaned_data['description']
            tone = form.cleaned_data['tone']
            
            # Here you would integrate with your AI service
            # For now, return a placeholder response
            generated_content = f"Generated {content_type} content with {tone} tone: {description}"
            
            return JsonResponse({
                'status': 'success',
                'content': generated_content
            })
    else:
        form = AIContentGenerationForm()
    
    return render(request, 'generator/ai_content.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    # Get all websites for the current user
    websites = UserWebsite.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'generator/dashboard.html', {
        'websites': websites
    })

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
