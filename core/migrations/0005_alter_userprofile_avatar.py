# Generated by Django 4.2.4 on 2024-03-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_userprofile_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='profilePics/dummyProfile.png', upload_to='profilePics'),
        ),
    ]
