# Generated by Django 4.2.7 on 2023-11-29 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_email_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadfile',
            old_name='data',
            new_name='uuid',
        ),
    ]