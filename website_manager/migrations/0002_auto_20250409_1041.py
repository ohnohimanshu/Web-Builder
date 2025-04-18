# Generated by Django 3.1.12 on 2025-04-09 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website_generator', '0001_initial'),
        ('website_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='website',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterModelOptions(
            name='websiteversion',
            options={'ordering': ['-version_number']},
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document'), ('other', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='website',
            name='generation_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generated_websites', to='website_generator.generationrequest'),
        ),
        migrations.AlterField(
            model_name='website',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='websites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='websiteversion',
            name='content',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='websiteversion',
            name='version_number',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='ShareLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_links', to='website_manager.website')),
            ],
        ),
    ]
