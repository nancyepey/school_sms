# Generated by Django 5.1.4 on 2025-01-26 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('teacher_uid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100)),
                ('date_of_birth', models.DateField()),
                ('joining_date', models.DateField()),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('section', models.CharField(max_length=100)),
                ('teacher_image', models.ImageField(blank=True, upload_to='teacher/img/')),
                ('permanent_address', models.TextField(null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('added_by', models.CharField(max_length=100, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('is_actif', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('classrooms', models.ManyToManyField(to='school.classroom')),
                ('t_subjects', models.ManyToManyField(to='subject.subject')),
            ],
        ),
    ]
