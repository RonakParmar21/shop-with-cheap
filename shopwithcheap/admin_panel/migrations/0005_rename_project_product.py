# Generated by Django 5.1.4 on 2025-01-09 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project',
            new_name='Product',
        ),
    ]
