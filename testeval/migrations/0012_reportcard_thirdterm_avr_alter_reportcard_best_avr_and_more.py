# Generated by Django 5.1.4 on 2025-03-23 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testeval', '0011_schoolclasranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportcard',
            name='thirdterm_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='best_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='firstterm_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='general_subjs_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='prof_subjs_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='secondterm_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='total_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='reportcard',
            name='worst_avr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
    ]
