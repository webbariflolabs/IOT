from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission


class DeviceTypeserializers(serializers.ModelSerializer):
      class Meta:
            model=DeviceType
            fields='__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class Accountserializers(serializers.ModelSerializer):
      class Meta:
            model=Account
            fields='__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class AdminUserSerializer(serializers.ModelSerializer):
    # user_img = serializers.ImageField(write_only=True)
    class Meta:
        model =AdminUser
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model =Registration
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    user_pic = serializers.ImageField(write_only=True)
    user_docs = serializers.FileField(write_only=True)
    class Meta:
        model = User
        fields = "__all__"

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model =Data
        fields = '__all__'

