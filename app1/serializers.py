from rest_framework import serializers
from .models import Account,DeviceType,CustomPermission
from django.contrib.auth.models import Permission

class Accountserializers(serializers.ModelSerializer):
      class Meta:
            model=Account
            fields='__all__'

class DeviceTypeserializers(serializers.ModelSerializer):
      class Meta:
            model=DeviceType
            fields='__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

from rest_framework import serializers

class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ['user_create', 'user_edit', 'user_delete']
