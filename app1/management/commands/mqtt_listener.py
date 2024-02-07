from django.core.management.base import BaseCommand
from datetime import datetime
# import psycopg2
# from django.db import connection
import paho.mqtt.client as mqtt
from paho.mqtt.client import Client
import time
import threading
from PIL import Image
from io import BytesIO
import numpy as np
import json


class Command(BaseCommand):
    help = 'Starts the MQTT message listener'


    def handle(self, *args, **options):
        broker_address = "4.240.114.7"
        broker_port = 1883
        username = "BarifloLabs"
        password = "Bfl@123"
        topics = ["topic1234","BinFile"] # Replace with your MQTT topic
 

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker")
                for topic in topics:
                    client.subscribe(topic)
            else:
                print(f"Connection failed with code {rc}")
        from app1.models import Device,Data,User
        def on_message(client, userdata, message):
            payload = message.payload
            print(f"Received message: {payload}")
            try:
                data = json.loads(payload.decode('utf-8'))
                print(f"Received message: {data}")
                device_id = data['deviceId']
                device = Device.objects.get(device_id=device_id)
                param_type = data['paramType']
                param_value = data['paramValue']
            
                received_timestamp = datetime.fromisoformat(data['dataPoint'])
                date_component = received_timestamp.date()
                time_component = received_timestamp.time()
                d = Data(device=device,param_type=param_type,param_value=param_value,date=date_component,time=time_component)
                d.save()
            except UnicodeDecodeError:
                from app1.models import Thermal_Actual_Image,User
                
                try:
                    compressed_data = np.load(BytesIO(payload))
                    image_array = compressed_data['arr_0']
                    image = Image.fromarray(image_array)
                    image_io = BytesIO()
                    image.save(image_io, format='PNG')  # Save the image to the BytesIO object
                    # test = Thermal_Actual_Image(image=image_io,user=)
                    # timestamp = time.strftime("%Y%m%d_%H%M%S")
                    # test.image.save(f"{timestamp}.png", image_io, save=True)
                    print("Image saved to the database")
                except Exception as e:
                    print("Error converting received message to image:", str(e))
    # except:
    #     print("No Device ID is there, check the device id")
        
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