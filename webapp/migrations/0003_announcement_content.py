# Generated by Django 3.2.5 on 2021-07-28 17:33

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_team_looking_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
