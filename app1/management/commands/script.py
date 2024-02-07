import paho.mqtt.client as mqtt
import time
import threading
from PIL import Image
from io import BytesIO
import numpy as np

class PublishBin:
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
        compressed_data = np.load(BytesIO(recive_data))
        image_array = compressed_data['arr_0']
        image = Image.fromarray(image_array)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_image_path = f"recived_img/output_image_{timestamp}.png"
        
        image.save(output_image_path)
        print(f"Received message and converted to image saved as {output_image_path}")
    except Exception as e:
        print("Error converting received message:", str(e))



def read_binary_data(file_path):
    with open(file_path, "rb") as file:
        return file.read()
    

def publishData(s1):
    try:
        binary_data_1 = read_binary_data("np/20240122_173517_mlx20240119_1432_26.npz")
        binary_data_2 = read_binary_data("np/20240122_173518_mlx16210.npz")

        time.sleep(5)

        s1.client.publish("BinFile", binary_data_1)
        s1.client.publish("BinFile", binary_data_2)

        print("Data Published")
    except Exception as e:
        print("Error publishing data:", str(e))



def reciveData(s1):
    try : 
        client = mqtt.Client("Recive")
        client.username_pw_set(s1.username, s1.password)
        client.connect(s1.mqttBroker, port=s1.port)

        client.on_message = on_message

        client.subscribe("topic1234")

        client.loop_forever()
    except KeyboardInterrupt :
        client.loop_stop()

if __name__ == "__main__":
    broker_address = "4.240.114.7"
    broker_port = 1883
    broker_username = "BarifloLabs"
    broker_password = "Bfl@123"

    s1 = PublishBin(broker_address, broker_port, broker_username, broker_password)

    t1 = threading.Thread(target=reciveData, args=(s1,))
    t2 = threading.Thread(target=publishData, args=(s1,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Done")
