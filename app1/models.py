from django.db import models
from django.utils import timezone
import datetime
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Registration(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Mobno=models.BigIntegerField(primary_key=True)
    Adhaar=models.BigIntegerField()
    params = models.JSONField(null=True,blank=True)
    USER_TYPES = (
        ('3d', '3D PRINTING'),
        ('aqua', 'AQUA CULTURE'),
        ('water', 'WATER BODY MANAGEMENT'),
    )
    user_category = models.CharField(max_length=20, choices=USER_TYPES,default=None)

class SuperAdmin(models.Model):
    Username=models.CharField(max_length=30)
    Password=models.CharField(max_length=50)

def admin_img(instance,filename):
    current_dt = datetime.datetime.now()
    date_str = current_dt.strftime("%d-%m-%Y")
    return '/'.join(['Admin_user_profile',str((instance.Name)+" "+date_str),filename])
class AdminUser(models.Model):
    Name=models.CharField(max_length=30)
    Email=models.EmailField()
    Mobno=models.BigIntegerField(primary_key=True)
    password=models.CharField(max_length=20)
    USER_TYPES = (
        ('3d', '3D PRINTING'),
        ('aqua', 'AQUA CULTURE'),
        ('water', 'WATER BODY MANAGEMENT'),
    )
    user_category = models.CharField(max_length=20, choices=USER_TYPES,default=USER_TYPES)
    user_img = models.ImageField(upload_to=admin_img,blank=True)
    token = models.CharField(max_length=100)
    def __str__(self):
        name = f"{self.user_category}"
        return name

class User(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Mobno=models.BigIntegerField(primary_key=True)
    password=models.CharField(max_length=20)
    Adhaar=models.BigIntegerField()
    token = models.CharField(max_length=100)
    user_pic=models.ImageField(upload_to='user_img/',blank=True)
    user_docs=models.FileField(upload_to='user_docs/',blank=True)
    user_category=models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    def __str__(self):
        name=f"{self.Name}"
        return name

class Account(models.Model):
    account_name = models.CharField(max_length=100)
    Account_id = models.BigIntegerField(primary_key=True)
    area = models.CharField(max_length=100)
    location = models.PointField(geography=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    def __str__(self):
        data=f"{self.account_name}"
        return data
    
class DeviceType(models.Model):
      Name=models.CharField(max_length=24)
      version=models.BigIntegerField()
      controls = models.JSONField(null=True,blank=True)
      def __str__(self):
          name=f"{self.Name}"
          return name
      
class Device(models.Model):
    device_id = models.BigIntegerField(primary_key=True)
    device_name = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accounts')
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='device_type')
    sensors = models.JSONField(max_length=100, blank=True, null=True, default=list)

    def save(self, *args, **kwargs):
        if self.device_type.Name == 'Aeration':
            self.sensors = ['current', 'voltage']
        else:
            self.sensors = ['do', 'ph', 'orp']
        super().save(*args, **kwargs)
    def __str__(self):
          name=f"{self.device_name}"
          return name

class Data(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE,to_field='device_id')  # Renamed to avoid conflict
    param_type = models.CharField(max_length=100)
    param_value = models.JSONField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

class Thermal_Actual_Image(models.Model):
      image=models.ImageField(upload_to='thermal_images/', blank=True, null=True)
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      date = models.DateField(default=timezone.now)
      def __str__(self):
          name=f"{self.user.Name}"
          return name
      
class OcrImage(models.Model):
      image=models.ImageField(upload_to='Ocr_images/', blank=True, null=True)
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      name = models.CharField(max_length=100)
      date = models.DateField(default=timezone.now)
      def __str__(self):
          name=f"{self.user.Name}"
          return name
