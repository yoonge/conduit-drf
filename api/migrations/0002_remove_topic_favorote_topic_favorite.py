# Generated by Django 4.2.11 on 2024-05-29 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='favorote',
        ),
        migrations.AddField(
            model_name='topic',
            name='favorite',
            field=models.IntegerField(default=0, verbose_name='favorite'),
        ),
    ]