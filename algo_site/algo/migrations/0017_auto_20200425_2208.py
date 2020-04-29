# Generated by Django 3.0.5 on 2020-04-25 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('algo', '0016_auto_20200417_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sol_vote',
            old_name='flag',
            new_name='down',
        ),
        migrations.AddField(
            model_name='sol_vote',
            name='up',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sol_comment',
            name='sol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algo.Solution'),
        ),
        migrations.AlterField(
            model_name='sol_vote',
            name='sol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algo.Solution'),
        ),
    ]
