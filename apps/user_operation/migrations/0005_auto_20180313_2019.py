# Generated by Django 2.0.2 on 2018-03-13 20:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_auto_20180306_1746'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_operation', '0004_auto_20180313_2002'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together={('user', 'goods')},
        ),
    ]
