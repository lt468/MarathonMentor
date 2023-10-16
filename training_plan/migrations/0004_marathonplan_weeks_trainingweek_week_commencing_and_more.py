# Generated by Django 4.2.3 on 2023-10-14 16:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('training_plan', '0003_trainingweek'),
    ]

    operations = [
        migrations.AddField(
            model_name='marathonplan',
            name='weeks',
            field=models.PositiveIntegerField(blank=True, help_text='Do not touch - is calculated in plan_ago.py', null=True),
        ),
        migrations.AddField(
            model_name='trainingweek',
            name='week_commencing',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='run',
            name='name',
            field=models.CharField(default='Basic Run', max_length=100),
        ),
        migrations.AlterField(
            model_name='scheduledruns',
            name='run',
            field=models.CharField(default='Training Run', max_length=100),
        ),
    ]