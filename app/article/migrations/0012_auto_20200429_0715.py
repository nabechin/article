# Generated by Django 3.0.5 on 2020-04-29 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_auto_20200427_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=None, max_length=150, unique=True),
        ),
    ]
