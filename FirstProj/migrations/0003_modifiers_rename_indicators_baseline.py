# Generated by Django 4.2.5 on 2023-09-18 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProj', '0002_remove_disease_indicator_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modifiers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('indicator_name', models.CharField(max_length=300)),
                ('indicator_code', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameModel(
            old_name='Indicators',
            new_name='Baseline',
        ),
    ]
