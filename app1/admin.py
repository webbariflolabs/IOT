from django.contrib import admin
from .models import User,Account,Device,Data,DeviceType
# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(Device)
admin.site.register(Data)
admin.site.register(DeviceType)