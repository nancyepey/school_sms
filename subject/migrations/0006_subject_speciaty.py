# Generated by Django 5.1.4 on 2025-01-23 21:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_specialty'),
        ('subject', '0005_alter_subject_coef'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='speciaty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.specialty'),
        ),
    ]