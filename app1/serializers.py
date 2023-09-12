from rest_framework import serializers
from .models import Account,DeviceType,CustomPermission,Device,Parameter,Mqtt_device
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

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'

class MqttSerializer(serializers.ModelSerializer):
    class Meta:
        model =Mqtt_device
        fields = '__all__'
