# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactoryData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npuresult', models.CharField(default=b'None', max_length=300)),
                ('usbresult', models.CharField(default=b'None', max_length=300)),
                ('ddrresult', models.CharField(default=b'None', max_length=300)),
                ('stressresult', models.CharField(default=b'None', max_length=300)),
            ],
        ),
    ]
