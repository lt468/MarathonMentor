# Generated by Django 4.2.3 on 2023-10-15 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_plan', '0005_rename_scheduledruns_scheduledrun'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marathonplan',
            name='active',
        ),
        migrations.RemoveField(
            model_name='runneruser',
            name='current_plan',
        ),
    ]