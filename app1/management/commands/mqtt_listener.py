from django.core.management.base import BaseCommand
from app1.alert_call import alert
import json
from django.utils import timezone
from datetime import datetime
import psycopg2
from django.db import connection
# from app1.management.commands.mqtt_listener.

class Command(BaseCommand):
    help = 'Starts the MQTT message listener'


    def handle(self, *args, **options):
        broker_address = "4.240.114.7"
        broker_port = 1883
        username = "BarifloLabs"
        password = "Bfl@123"
        topics = ["topic123"] # Replace with your MQTT topic
        # params = {
        #     'host':'20.244.48.88',
        #     'database':'iotdb',
        #     'user':'bariflolabs',
        #     'password':'bariflo123'
        #     } 


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
            try:
                data = json.loads(message.payload.decode('utf-8'))
                print(f"Received message: {data}")
                from app1.models import Mqtt_device,Parameter,Account,User,Device

                device_id = data['deviceId']
                print(device_id)
                device, _ = Mqtt_device.objects.get_or_create(device_id=device_id)

                # timestamp = timezone.now()
                # data_point = DataPoint.objects.create(device=device, timestamp=timestamp)
                param_type = data['paramType']
                param_value = data['paramValue']
            
                received_timestamp = datetime.fromisoformat(data['dataPoint'])
                date_component = received_timestamp.date()
                time_component = received_timestamp.time()
                # try:
                #     cur = connection.cursor() 
                #     cur.execute(f"insert into device_{device_id}(device, param_type, param_value, date, time) values({device_id}, '{param_type}', {param_value}, '{date_component}', '{time_component}');") 
                #     # cur.commit()
                #     print("data stored in database")
                #     Parameter.objects.create(device=device,param_type=param_type,param_value=param_value,date=date_component,time=time_component)
                #     print("data stored in database through django models")
                # except Exception as e:
                #     print(e)
                # alert(device_id)  # calling alert function 
            except Exception as e:
                print(e)
            
        from paho.mqtt.client import Client
        while True:
            # conn = psycopg2.connect(**params)  
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
