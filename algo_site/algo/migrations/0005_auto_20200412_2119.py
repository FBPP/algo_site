# Generated by Django 3.0.5 on 2020-04-12 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0004_auto_20200411_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='memory_restrict',
            new_name='memory_limit',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='time_restrict',
            new_name='time_limit',
        ),
    ]
