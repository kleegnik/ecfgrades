# Generated by Django 3.0.6 on 2020-07-31 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0003_auto_20200731_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='fidecode',
        ),
        migrations.AddField(
            model_name='grade',
            name='fidecode',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
