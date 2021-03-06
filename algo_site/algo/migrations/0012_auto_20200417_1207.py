# Generated by Django 3.0.5 on 2020-04-17 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0011_auto_20200417_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='time',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='sol_comment',
            name='sol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algo.Solution'),
        ),
    ]
