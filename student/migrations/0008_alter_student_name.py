# Generated by Django 5.1.4 on 2025-01-16 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_student_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]