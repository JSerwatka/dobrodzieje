# Generated by Django 3.2.5 on 2021-08-27 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_notification_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='data',
            new_name='extra_data',
        ),
    ]
