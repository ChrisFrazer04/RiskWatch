# Generated by Django 4.2.5 on 2023-09-21 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProj', '0005_baselinedata_delete_storeddata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baselinedata',
            name='incidence',
            field=models.FloatField(),
        ),
    ]
