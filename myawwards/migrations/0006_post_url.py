# Generated by Django 3.1.5 on 2021-01-24 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myawwards', '0005_auto_20210125_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]