# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='master',
        ),
        migrations.AddField(
            model_name='subscription',
            name='masters',
            field=models.ManyToManyField(related_name='master_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
