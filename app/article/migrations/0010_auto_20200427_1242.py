# Generated by Django 3.0.5 on 2020-04-27 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='nabeyuma', max_length=150, unique=True),
            preserve_default=False,
        ),
    ]
