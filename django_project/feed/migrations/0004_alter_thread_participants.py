# Generated by Django 5.1.6 on 2025-02-21 15:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_message_is_read'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='participants',
            field=models.ManyToManyField(blank=True, null=True, related_name='threads', to=settings.AUTH_USER_MODEL),
        ),
    ]
