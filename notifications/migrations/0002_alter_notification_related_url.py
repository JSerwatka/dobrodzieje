# Generated by Django 3.2.5 on 2021-08-24 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='related_url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='related url'),
        ),
    ]
