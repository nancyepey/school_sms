# Generated by Django 5.1.4 on 2025-02-28 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='Z15qsaIC3NMIgqk2fv3ryuAevWAIvw62', editable=False, max_length=32, unique=True),
        ),
    ]
