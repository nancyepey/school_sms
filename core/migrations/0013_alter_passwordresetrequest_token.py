# Generated by Django 5.1.4 on 2025-02-09 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='BpkV7QTlopiEszFBwvFOhqqJAK6kzbjz', editable=False, max_length=32, unique=True),
        ),
    ]
