from django.db import models
from django.utils import timezone

class Registration(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Mobno=models.BigIntegerField(primary_key=True)
    Adhaar=models.IntegerField()
    account_name=models.CharField(max_length=50)
    device_details=models.CharField(max_length=200)
    USER_TYPES = (
        ('3d', '3D PRINTING'),
        ('aqua', 'AQUA CULTURE'),
        ('water', 'WATER BODY MANAGEMENT'),
    )
    user_category = models.CharField(max_length=20, choices=USER_TYPES,default=None)
    # user_category=models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    # def __str__(self):
    #     name=f"{self.Name}"
    #     return name

class AdminUser(models.Model):
    Name=models.CharField(max_length=30)
    Email=models.EmailField()
    Mobno=models.BigIntegerField(primary_key=True)
    password=models.CharField(max_length=20)
    USER_TYPES = (
        ('3d', '3D PRINTING'),
        ('aqua', 'AQUA CULTURE'),
        ('waterbody', 'WATER BODY MANAGEMENT'),
    )
    user_category = models.CharField(max_length=20, choices=USER_TYPES,default=USER_TYPES)
    def __str__(self):
        name = f"{self.user_category}"
        return name

class User(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Mobno=models.BigIntegerField(primary_key=True)
    password=models.CharField(max_length=20)
    Adhaar=models.IntegerField()
    user_pic=models.ImageField(upload_to='user_img/',blank=True)
    user_docs=models.FileField(upload_to='user_docs/',blank=True)
    user_category=models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    def __str__(self):
        name=f"{self.Name}"
        return name

class Account(models.Model):
    account_name = models.CharField(max_length=100)
    Account_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    
    def __str__(self):
        data=f"{self.account_name}"
        return data
    
class DeviceType(models.Model):
      Name=models.CharField(max_length=24)
      version=models.IntegerField()
      controls = models.JSONField(null=True,blank=True)
      def __str__(self):
          name=f"{self.Name} {self.version}"
          return name



class Device(models.Model):
    device_id = models.IntegerField(primary_key=True)
    device_name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accounts')
    device_type = models.ForeignKey(DeviceType, on_delete=models.Aggregate, related_name='device_type')
    def __str__(self):
        data=f"{self.device_id}"
        return data

class Data(models.Model):
    timestamp = models.DateTimeField()
    value = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='data')
    def __str__(self):
        data=f"{self.device.device_id}"
        return data

class CustomPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permission')
    User_create = models.BooleanField(default=False)
    User_edit = models.BooleanField(default=False)
    User_views = models.BooleanField(default=False)
    User_delete = models.BooleanField(default=False)
    Account_create = models.BooleanField(default=False)
    Account_edit = models.BooleanField(default=False)
    Account_views = models.BooleanField(default=False)
    Account_delete = models.BooleanField(default=False)
    Device_create = models.BooleanField(default=False)
    Device_edit = models.BooleanField(default=False)
    Device_delete = models.BooleanField(default=False)
    Device_views = models.BooleanField(default=False)
    Device_instruction = models.BooleanField(default=False)
    Setting = models.BooleanField(default=False)

# class Mqtt(models.Model):
#     Device_id = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='deviceid')
#     Temprature = models.FloatField(null=True,blank=True)
#     DO = models.FloatField(null=True,blank=True)
#     pH = models.FloatField(null=True,blank=True)
#     ORP = models.FloatField(null=True,blank=True)
#     TDS = models.FloatField(null=True,blank=True)
#     Date = models.DateField(default=timezone.now) 
#     Time = models.TimeField(default=timezone.now) 
    
class Mqtt_device(models.Model):
    device_id = models.BigIntegerField(primary_key=True)
    def __str__(self):
        return f"{self.device_id}"


class Parameter(models.Model):
    device = models.ForeignKey(Mqtt_device,on_delete=models.CASCADE,to_field='device_id')  # Renamed to avoid conflict
    param_type = models.CharField(max_length=100)
    param_value = models.JSONField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    @property
    def mqtt_device_id(self):
        return self.device.device_id

    

    