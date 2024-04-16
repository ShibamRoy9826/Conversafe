# Generated by Django 4.2.4 on 2024-04-12 17:09

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
            name='AIRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('userConnected', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ai_chat_room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayName', models.CharField(default='ErrorOnDisplay', max_length=30)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('messageType', models.CharField(choices=[('NORMAL', 'Normal'), ('JOINED', 'Joined'), ('LEFT', 'Left')], default='NORMAL', max_length=6)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AIMessages', to='AIChat.airoom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AIMessages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time',),
            },
        ),
    ]
