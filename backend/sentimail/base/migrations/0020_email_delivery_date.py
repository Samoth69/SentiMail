# Generated by Django 4.2.7 on 2024-01-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_email_recipient_email_sender_email_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='delivery_date',
            field=models.CharField(default='', max_length=100),
        ),
    ]