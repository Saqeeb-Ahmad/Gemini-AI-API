# Generated by Django 5.0.3 on 2024-05-12 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gemini_app', '0006_remove_customuser_irst_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
