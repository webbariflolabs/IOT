# Generated by Django 4.2.4 on 2023-08-31 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_mqtt_device_device_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mqtt_device',
            name='id',
        ),
        migrations.AlterField(
            model_name='mqtt_device',
            name='device_id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]