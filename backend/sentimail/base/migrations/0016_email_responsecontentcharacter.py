# Generated by Django 4.2.7 on 2024-01-09 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_email_responsecontentkeywords_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='responseContentCharacter',
            field=models.CharField(default='', max_length=100),
        ),
    ]