# Generated by Django 2.0.2 on 2018-03-13 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0003_auto_20180313_1954'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together=set(),
        ),
    ]
