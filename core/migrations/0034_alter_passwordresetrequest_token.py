# Generated by Django 5.1.4 on 2025-03-02 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='xWcOhIjSNdcdvrnO9658dNufPESdR2wg', editable=False, max_length=32, unique=True),
        ),
    ]
