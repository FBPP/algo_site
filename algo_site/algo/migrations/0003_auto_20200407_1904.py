# Generated by Django 3.0.5 on 2020-04-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0002_auto_20200404_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='cin_example',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='question',
            name='cin_format',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='cout_example',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='question',
            name='cout_format',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='data_range',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(max_length=600),
        ),
    ]
