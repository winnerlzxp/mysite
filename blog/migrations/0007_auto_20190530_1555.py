# Generated by Django 2.0 on 2019-05-30 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190530_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='readnum',
            old_name='readed_num',
            new_name='read_num',
        ),
    ]
