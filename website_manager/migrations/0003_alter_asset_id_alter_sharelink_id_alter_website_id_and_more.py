# Generated by Django 5.2 on 2025-04-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_manager', '0002_auto_20250409_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sharelink',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='website',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='websiteversion',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
