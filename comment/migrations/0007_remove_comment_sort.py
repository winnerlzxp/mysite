# Generated by Django 2.0 on 2019-06-03 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_auto_20190603_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='sort',
        ),
    ]
