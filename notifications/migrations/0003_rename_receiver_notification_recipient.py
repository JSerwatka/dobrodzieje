# Generated by Django 3.2.5 on 2021-08-24 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notification_related_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='receiver',
            new_name='recipient',
        ),
    ]