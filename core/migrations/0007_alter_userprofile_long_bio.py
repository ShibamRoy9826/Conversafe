# Generated by Django 4.2.4 on 2024-03-12 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_userprofile_long_bio_userprofile_short_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='long_bio',
            field=models.TextField(default='Description not provided by user', max_length=500),
        ),
    ]
