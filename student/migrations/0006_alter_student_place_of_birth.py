# Generated by Django 5.1.4 on 2025-02-26 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_minesec_ident_num_student_place_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
