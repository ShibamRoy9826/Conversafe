# Generated by Django 4.2.4 on 2024-03-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_auser_firstlogin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auser',
            name='firstLogin',
            field=models.CharField(default='No', max_length=3),
        ),
    ]