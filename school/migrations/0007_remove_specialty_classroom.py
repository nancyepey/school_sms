# Generated by Django 5.1.4 on 2025-01-23 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_specialty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialty',
            name='classroom',
        ),
    ]