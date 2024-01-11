# Generated by Django 4.2.7 on 2023-11-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_hash_email_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfile',
            name='data',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='email',
            name='uuid',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
