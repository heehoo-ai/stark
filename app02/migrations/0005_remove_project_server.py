# Generated by Django 2.1.5 on 2020-09-03 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0004_auto_20200903_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='server',
        ),
    ]
