# Generated by Django 5.1.4 on 2025-03-01 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='Lk2IuAUw6qTkjB6DwFTbYnJYFtNdidVZ', editable=False, max_length=32, unique=True),
        ),
    ]
