# Generated by Django 3.1.5 on 2021-01-24 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myawwards', '0003_auto_20210124_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='url',
        ),
    ]
