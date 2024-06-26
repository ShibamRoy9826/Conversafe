# Generated by Django 4.2.4 on 2024-02-23 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(blank=True, null=True)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('followers', models.IntegerField(blank=True, null=True)),
                ('following', models.IntegerField(blank=True, null=True)),
                ('acheivements', models.IntegerField(blank=True, null=True)),
                ('avatar', models.ImageField(default='res/dummyProfile.png', upload_to='profilePic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
