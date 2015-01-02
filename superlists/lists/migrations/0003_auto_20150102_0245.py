# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_item_test'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='test',
            new_name='text',
        ),
    ]
