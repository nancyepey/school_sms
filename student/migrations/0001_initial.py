# Generated by Django 5.1.4 on 2025-01-13 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(blank=True, max_length=250, null=True)),
                ('father_occupation', models.CharField(blank=True, max_length=250, null=True)),
                ('father_mobile', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('father_email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('mother_name', models.CharField(blank=True, max_length=250, null=True)),
                ('mother_occupation', models.CharField(blank=True, max_length=250, null=True)),
                ('mother_mobile', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('mother_email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('carer_name', models.CharField(blank=True, max_length=250, null=True)),
                ('carer_occupation', models.CharField(blank=True, max_length=250, null=True)),
                ('carer_mobile', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('carer_email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('present_address', models.TextField(blank=True, null=True)),
                ('permanent_address', models.TextField(null=True)),
                ('created_by', models.EmailField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('student_uid', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100)),
                ('date_of_birth', models.DateField()),
                ('student_class', models.CharField(max_length=100)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('joining_date', models.DateField()),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('admission_number', models.CharField(max_length=15)),
                ('section', models.CharField(max_length=100)),
                ('student_image', models.ImageField(blank=True, upload_to='student/img/')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.parent')),
            ],
        ),
    ]