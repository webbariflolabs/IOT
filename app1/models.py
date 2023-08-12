from django.db import models

class User(models.Model):
    Name=models.CharField(max_length=20)
    Email=models.EmailField()
    Mobno=models.IntegerField(primary_key=True)
    password=models.CharField(max_length=20)
    USER_TYPES = (
        ('general', 'ACCOUNT USER'),
        ('admin', 'ACCOUNT ADMIN'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES,default=USER_TYPES)
    def __str__(self):
        name=f"{self.Name}"
        return name

class Account(models.Model):
    id=models.IntegerField()
    account_name = models.CharField(max_length=100)
    Account_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    def __str__(self):
        data=f"{self.account_name}"
        return data
    
class DeviceType(models.Model):
      Name=models.CharField(max_length=24)
      version=models.IntegerField()
      def __str__(self):
          name=f"{self.Name}"
          return name

class Device(models.Model):
    device_name = models.CharField(max_length=100)
    device_type = models.ForeignKey(DeviceType, on_delete=models.Aggregate, related_name='device_type')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='devices')
    def __str__(self):
        data=f"{self.device_name}   &   {self.device_type}"
        return data

class Data(models.Model):
    timestamp = models.DateTimeField()
    value = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='data')
    def __str__(self):
        data=f"{self.device}"
        return data



