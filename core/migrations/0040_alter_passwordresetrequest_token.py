# Generated by Django 5.1.4 on 2025-03-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='5OaxO4a31w1IDNRumsmzkhMWSmes4IM8', editable=False, max_length=32, unique=True),
        ),
    ]
