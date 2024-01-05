# Generated by Django 4.2.5 on 2023-09-20 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FirstProj', '0004_remove_baseline_id_alter_baseline_disease'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaselineData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=5)),
                ('country_name', models.CharField(max_length=50)),
                ('incidence', models.IntegerField()),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FirstProj.disease')),
            ],
        ),
        migrations.DeleteModel(
            name='StoredData',
        ),
    ]
