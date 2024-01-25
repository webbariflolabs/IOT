from django.core.management.base import BaseCommand
from datetime import datetime
# import psycopg2
# from django.db import connection
import paho.mqtt.client as mqtt
import time
import threading
from PIL import Image
from io import BytesIO
import numpy as np
import json


class Command(BaseCommand):
    def __init__(self, broker, port, username, password):
        self.mqttBroker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client("Client")
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.mqttBroker, port=self.port)


def on_message(client, userdata, message):
    recive_data = message.payload
    try:
        from app1.models import Data,Device
        rcvd_data = json.loads(recive_data.decode('utf-8'))
        print(rcvd_data)
        device_id = rcvd_data['deviceId']
        device, _ = Device.objects.get_or_create(device_id=device_id)
        param_type = rcvd_data['paramType']
        param_value = rcvd_data['paramValue']
        received_timestamp = datetime.fromisoformat(rcvd_data['dataPoint'])
        date_component = received_timestamp.date()
        time_component = received_timestamp.time()
        Data.objects.create(device=device,param_type=param_type,param_value=param_value,date=date_component,time=time_component)

    except UnicodeDecodeError:
        from app1.models import Thermal_Actual_Image
        try:
            compressed_data = np.load(BytesIO(recive_data))
            image_array = compressed_data['arr_0']
            image = Image.fromarray(image_array)
            image_io = BytesIO()
            image.save(image_io, format='PNG')  # Save the image to the BytesIO object
            test = Thermal_Actual_Image()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            test.image.save(f"{timestamp}.png", image_io, save=True)
            print("Image saved to the database")
        except Exception as e:
            print("Error converting received message to image:", str(e))
    except:
        print("No Device ID is there, check the device id")



def read_binary_data(file_path):
    with open(file_path, "rb") as file:
        return file.read()
    

# def publishData(s1):
#     try:
#         binary_data_1 = read_binary_data("np/20240122_173517_mlx20240119_1432_26.npz")
#         binary_data_2 = read_binary_data("np/20240122_173518_mlx16210.npz")

#         time.sleep(5)

#         s1.client.publish("BinFile", binary_data_1)
#         s1.client.publish("BinFile", binary_data_2)

#         print("Data Published")
#     except Exception as e:
#         print("Error publishing data:", str(e))



def reciveData(s1):
    client = mqtt.Client("Recive")
    client.username_pw_set(s1.username, s1.password)
    client.connect(s1.mqttBroker, port=s1.port)

    client.on_message = on_message

    client.subscribe("BinFile")
    client.subscribe("topic123")

    client.loop_start()

# if __name__ == "__main__":
broker_address = "4.240.114.7"
broker_port = 1883
broker_username = "BarifloLabs"
broker_password = "Bfl@123"

s1 = Command(broker_address, broker_port, broker_username, broker_password)

t1 = threading.Thread(target=reciveData, args=(s1,))
# t2 = threading.Thread(target=publishData, args=(s1,))

t1.start()
# t2.start()
# 
t1.join()
# t2.join()

print("Done")
try:
    while True:
        pass
except KeyboardInterrupt:
    s1.client.loop_stop()
    print('MQTT listener stopped')









#                 # try:
#                 #     cur = connection.cursor() 
#                 #     cur.execute(f"insert into device_{device_id}(device, param_type, param_value, date, time) values({device_id}, '{param_type}', {param_value}, '{date_component}', '{time_component}');") 
#                 #     # cur.commit()
#                 #     print("data stored in database")
#                 #     print("data stored in database through django models")
#                 # except Exception as e:
#                 #     print(e)