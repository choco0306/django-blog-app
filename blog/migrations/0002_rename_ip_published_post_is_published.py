# Generated by Django 4.0.3 on 2022-04-04 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='ip_published',
            new_name='is_published',
        ),
    ]
