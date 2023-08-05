# Generated by Django 2.1.4 on 2019-02-08 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trosnoth', '0023_auto_20181214_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trosnothserversettings',
            name='webPort',
            field=models.SmallIntegerField(default=0, help_text='Leave as 0 to automatically select a free port.', verbose_name='Web server port'),
        ),
    ]
