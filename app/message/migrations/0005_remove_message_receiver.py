# Generated by Django 2.2.12 on 2020-07-03 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_message_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
    ]
