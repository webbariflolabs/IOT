from django.contrib import admin
from .models import User,Account,Device,Data,DeviceType,CustomPermission,Parameter,Mqtt_device,AdminUser,Registration
# Register your models here.

@admin.register(Registration)
class Registration(admin.ModelAdmin):
    list_display = ['Name','Email','Mobno','Adhaar','account_name','device_details','user_category']

@admin.register(AdminUser)
class AdminUser(admin.ModelAdmin):
    list_display = ['Name','Email','Mobno','password','user_category']

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['Name','Email','Mobno','password','Adhaar','user_category','user_pic','user_docs']

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
    list_display = ['Name','version','controls']

@admin.register(CustomPermission)
class AdminCustomPermission(admin.ModelAdmin):
    list_display = ['user','User_create','User_edit','User_delete','User_views','Account_create','Account_edit','Account_views','Account_delete','Device_create','Device_edit','Device_delete','Device_views','Device_instruction','Setting']

@admin.register(Mqtt_device)
class AdminMqtt_device(admin.ModelAdmin):
    list_display = ['device_id']

@admin.register(Parameter)
class AdminDeviceParameter(admin.ModelAdmin):
    list_display = ['device','param_type','param_value','date','time',]
    def mqtt_device_id(self,obj):
        return obj.device.device_id
    
    mqtt_device_id.short_description = 'Device ID'

