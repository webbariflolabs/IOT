from rest_framework import serializers
from .models import Account,DeviceType,CustomPermission,Device
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


class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = '__all__'

# class DeviceParameterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeviceParameter
#         fields = '__all__'
