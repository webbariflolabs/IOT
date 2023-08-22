from django.contrib import admin
from .models import User,Account,Device,Data,DeviceType,CustomPermission
# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['Name','Mobno','password','user_type']

@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = ['account_name','Account_id','user']

@admin.register(Device)
class Device(admin.ModelAdmin):
    list_display = ['device_id','device_name','device_type','account']

@admin.register(Data)
class Data(admin.ModelAdmin):
    list_display = ['timestamp','value','device']

@admin.register(DeviceType)
class DeviceType(admin.ModelAdmin):
    list_display = ['Name','version']

@admin.register(CustomPermission)
class DeviceType(admin.ModelAdmin):
    list_display = ['user','user_create','user_edit','user_delete']
