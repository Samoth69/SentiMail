# Generated by Django 4.2.7 on 2023-12-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_uploadfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='responseMetadataSPF',
            field=models.CharField(default='', max_length=100),
        ),
    ]
