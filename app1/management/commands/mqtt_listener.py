
from django.core.management.base import BaseCommand
from app1.models import Mqtt_device,Parameter  # Replace with your actual model
import json
from django.utils import timezone
from datetime import datetime


class Command(BaseCommand):
    help = 'Starts the MQTT message listener'


    def handle(self, *args, **options):
        broker_address = "16.171.160.72"
        broker_port = 1883
        username = "BarifloLabs"
        password = "Bfl@123"
        topics = ["topic123"] # Replace with your MQTT topic
 

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker")
                for topic in topics:
                    client.subscribe(topic)
            else:
                print(f"Connection failed with code {rc}")

        # def on_message(client, userdata, message):

            # payload = message.payload.decode()
            # print(f"Received message: {payload}")

           

        def on_message(client, userdata, message):
            # payload = message.payload.decode()
            # print(f"Received message: {payload}")
            data = json.loads(message.payload.decode('utf-8'))
            print(f"Received message: {data}")


            device_id = data['deviceId']
            device, _ = Mqtt_device.objects.get_or_create(device_id=device_id)
 

            # timestamp = timezone.now()

            # data_point = DataPoint.objects.create(device=device, timestamp=timestamp)

 
            param_type = data['paramType']
            param_value = data['paramValue']
           
            received_timestamp = datetime.fromisoformat(data['dataPoint'])
            date_component = received_timestamp.date()
            time_component = received_timestamp.time()
            Parameter.objects.create(device=device,param_type=param_type,param_value=param_value,date=date_component,time=time_component)
            

        from paho.mqtt.client import Client
        mqtt_client = Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.username_pw_set(username, password)
        mqtt_client.connect(broker_address, broker_port)
        mqtt_client.loop_start()
 

        try:
            print('MQTT listener started')
            while True:
                pass
        except KeyboardInterrupt:
            mqtt_client.loop_stop()
            print('MQTT listener stopped')