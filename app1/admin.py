from django.contrib import admin
from .models import *
from django.contrib.gis import admin
# Register your models here.

@admin.register(Registration)
class Registration(admin.ModelAdmin):
    list_display = ['Name','Email','Mobno','Adhaar','params','user_category']

@admin.register(SuperAdmin)
class SuperAdminUser(admin.ModelAdmin):
    list_display = ['Username','Password']

@admin.register(AdminUser)
class AdminUser(admin.ModelAdmin):
    list_display = ['Name','Email','Mobno','password','user_category','user_img','token']

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['Name','Email','Mobno','password','Adhaar','user_category','user_pic','user_docs','token']

@admin.register(Account)
class Account(admin.GISModelAdmin):
    list_display = ['account_name','Account_id','area','location','user']

@admin.register(Device)
class Device(admin.ModelAdmin):
    list_display = ['device_id','device_name','device_type','account','sensors']

@admin.register(Data)
class Data(admin.ModelAdmin):
    list_display = ['device','param_type','param_value','date','time']

@admin.register(DeviceType)
class DeviceType(admin.ModelAdmin):
    list_display = ['Name','version','controls']

@admin.register(Thermal_Actual_Image)
class Thermal_Actual_Image(admin.ModelAdmin):
    list_display = ['id','image','user','date']

@admin.register(OcrImage)
class OcrImage(admin.ModelAdmin):
    list_display = ['id','image','name','user']   


