# Generated by Django 3.0.5 on 2020-04-17 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0013_auto_20200417_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sol_comment',
            name='sol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algo.Solution'),
        ),
    ]
