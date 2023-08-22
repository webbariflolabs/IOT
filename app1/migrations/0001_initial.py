# Generated by Django 4.2.4 on 2023-08-18 06:04

from django.db import migrations, models
import django.db.models.aggregates
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_name', models.CharField(max_length=100)),
                ('Account_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=24)),
                ('version', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('Name', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobno', models.IntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('user_type', models.CharField(choices=[('general', 'ACCOUNT USER'), ('admin', 'ACCOUNT ADMIN')], default=(('general', 'ACCOUNT USER'), ('admin', 'ACCOUNT ADMIN')), max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField()),
                ('device_name', models.CharField(max_length=100)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='app1.account')),
                ('device_type', models.ForeignKey(on_delete=django.db.models.aggregates.Aggregate, related_name='device_type', to='app1.devicetype')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.CharField(max_length=100)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='app1.device')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='app1.user'),
        ),
    ]
