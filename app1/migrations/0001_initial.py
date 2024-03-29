# Generated by Django 5.0.1 on 2024-02-06 11:20

import app1.models
import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_name', models.CharField(max_length=100)),
                ('Account_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('area', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('Name', models.CharField(max_length=30)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobno', models.BigIntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('user_category', models.CharField(choices=[('3d', '3D PRINTING'), ('aqua', 'AQUA CULTURE'), ('water', 'WATER BODY MANAGEMENT')], default=(('3d', '3D PRINTING'), ('aqua', 'AQUA CULTURE'), ('water', 'WATER BODY MANAGEMENT')), max_length=20)),
                ('user_img', models.ImageField(blank=True, upload_to=app1.models.admin_img)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=24)),
                ('version', models.BigIntegerField()),
                ('controls', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('Name', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobno', models.BigIntegerField(primary_key=True, serialize=False)),
                ('Adhaar', models.BigIntegerField()),
                ('params', models.JSONField(blank=True, null=True)),
                ('user_category', models.CharField(choices=[('3d', '3D PRINTING'), ('aqua', 'AQUA CULTURE'), ('water', 'WATER BODY MANAGEMENT')], default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=30)),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=100)),
                ('sensors', models.JSONField(blank=True, default=list, max_length=100, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='app1.account')),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_type', to='app1.devicetype')),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('param_type', models.CharField(max_length=100)),
                ('param_value', models.JSONField()),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.device')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('Name', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobno', models.BigIntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('Adhaar', models.BigIntegerField()),
                ('token', models.CharField(max_length=100)),
                ('user_pic', models.ImageField(blank=True, upload_to='user_img/')),
                ('user_docs', models.FileField(blank=True, upload_to='user_docs/')),
                ('user_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.adminuser')),
            ],
        ),
        migrations.CreateModel(
            name='Thermal_Actual_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='thermal_images/')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user')),
            ],
        ),
        migrations.CreateModel(
            name='OcrImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Ocr_images/')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='app1.user'),
        ),
    ]
