# Generated by Django 3.0.5 on 2020-04-17 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20200405_2237'),
        ('algo', '0009_auto_20200416_1547'),
    ]

    operations = [
        migrations.CreateModel(
            name='solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('source', models.URLField()),
                ('q_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='algo.Question')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.User')),
            ],
        ),
    ]
