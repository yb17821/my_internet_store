# Generated by Django 2.0.2 on 2018-03-06 14:50

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_auto_20180306_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_desc',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='内容'),
        ),
    ]
