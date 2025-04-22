from django.db import migrations

def create_portfolio_fields(apps, schema_editor):
    WebsiteTemplate = apps.get_model('generator', 'WebsiteTemplate')
    CustomizationField = apps.get_model('generator', 'CustomizationField')
    
    portfolio = WebsiteTemplate.objects.filter(template_type='portfolio').first()
    if portfolio:
        fields = [
            {
                'name': 'site_title',
                'label': 'Site Title',
                'field_type': 'text',
                'default_value': 'My Portfolio',
                'required': True,
                'order': 1
            },
            {
                'name': 'name',
                'label': 'Your Name',
                'field_type': 'text',
                'required': True,
                'order': 2
            },
            {
                'name': 'profession',
                'label': 'Profession/Title',
                'field_type': 'text',
                'required': True,
                'order': 3
            },
            {
                'name': 'profile_image',
                'label': 'Profile Image',
                'field_type': 'image',
                'required': True,
                'order': 4
            },
            {
                'name': 'about_me',
                'label': 'About Me',
                'field_type': 'textarea',
                'required': True,
                'order': 5
            },
            {
                'name': 'primary_color',
                'label': 'Primary Color',
                'field_type': 'color',
                'default_value': '#007bff',
                'order': 6
            },
            {
                'name': 'secondary_color',
                'label': 'Secondary Color',
                'field_type': 'color',
                'default_value': '#6c757d',
                'order': 7
            }
        ]
        
        for field_data in fields:
            CustomizationField.objects.create(
                template=portfolio,
                **field_data
            )

class Migration(migrations.Migration):
    dependencies = [
        ('generator', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_portfolio_fields),
    ]