# Generated by Django 5.0 on 2023-12-08 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catentry', '0010_cat_previous_status_alter_cat_cat_surgery_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adopter',
            name='adopter_state',
            field=models.TextField(max_length=2, null=True),
        ),
    ]
