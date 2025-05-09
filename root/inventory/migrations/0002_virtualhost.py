# Generated by Django 5.2 on 2025-05-01 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualHost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('state', models.IntegerField()),
                ('memory', models.IntegerField()),
                ('vcpus', models.IntegerField()),
                ('disk', models.IntegerField()),
                ('physical_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.physicalhost')),
            ],
        ),
    ]
