# Generated by Django 2.2.12 on 2020-07-20 12:36

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20200628_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='background_image',
            field=models.ImageField(default='default_background.jpg', null=True, upload_to=account.models.introduction_image_save_path),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='default_profile.jpg', null=True, upload_to=account.models.profile_image_save_path),
        ),
    ]