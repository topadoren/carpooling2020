# Generated by Django 2.2.2 on 2019-06-30 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0005_auto_20190630_0105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tripstatus',
            old_name='trip_description',
            new_name='tripstatus_description',
        ),
    ]
