# Generated by Django 4.2.4 on 2024-03-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.TextField(blank=True, default='GuestUser', max_length=30, null=True),
        ),
    ]
