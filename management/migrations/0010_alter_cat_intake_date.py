# Generated by Django 5.0 on 2023-12-15 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_remove_spayneuterrecord_clinic_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='intake_date',
            field=models.DateField(default='12/15/2023'),
        ),
    ]