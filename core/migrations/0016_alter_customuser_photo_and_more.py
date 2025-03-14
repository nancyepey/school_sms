# Generated by Django 5.1.4 on 2025-02-22 19:34

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default='default.png', upload_to=core.models.image_file_upload_handler),
        ),
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='9fz6LTNkHG0ei3vxA2dUEuvCdHrmkjCv', editable=False, max_length=32, unique=True),
        ),
    ]
