# Generated by Django 5.1.4 on 2025-03-23 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='gE8x21CsxSZorsgSoc85QMHtoFLwirKH', editable=False, max_length=32, unique=True),
        ),
    ]
