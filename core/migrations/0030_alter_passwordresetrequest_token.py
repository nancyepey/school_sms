# Generated by Django 5.1.4 on 2025-03-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='8osmWe6kCyluTUjciLklHrvOJ8DsuY52', editable=False, max_length=32, unique=True),
        ),
    ]
