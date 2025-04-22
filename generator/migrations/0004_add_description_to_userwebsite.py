from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_websitetemplate_features_websitetemplate_is_premium_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwebsite',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ] 