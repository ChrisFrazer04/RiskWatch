# Generated by Django 4.2.4 on 2023-09-05 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProj', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disease',
            name='indicator_code',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='indicator_name',
        ),
        migrations.CreateModel(
            name='StoredData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FirstProj.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Indicators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator_code', models.CharField(max_length=50)),
                ('indicator_name', models.CharField(max_length=300)),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FirstProj.disease')),
            ],
        ),
    ]