# Generated by Django 4.2.7 on 2023-12-11 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_uploadfile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='username',
        ),
    ]