# Generated by Django 4.2.6 on 2023-11-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_plan', '0004_alter_stravauserprofile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='stravauserprofile',
            name='client_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stravauserprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]