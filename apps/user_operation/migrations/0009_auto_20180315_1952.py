# Generated by Django 2.0.2 on 2018-03-15 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0008_auto_20180315_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userleavingmessage',
            name='file',
            field=models.FileField(blank=True, help_text='上传的文件', null=True, upload_to='message/images/', verbose_name='上传的文件'),
        ),
    ]
