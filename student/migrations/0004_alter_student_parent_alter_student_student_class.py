# Generated by Django 5.1.4 on 2025-01-14 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_classroom_modified_by'),
        ('student', '0003_remove_parent_created_by_parent_added_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.parent'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.classroom'),
        ),
    ]