# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_factorydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isbackup',
            field=models.CharField(default=b'no', max_length=300),
        ),
    ]
