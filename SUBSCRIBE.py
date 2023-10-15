import random
import time
import paho.mqtt.client as mqtt

broker = 'b97b659315cf4f0cafd48b90e3421aa6.s2.eu.hivemq.cloud'
port = 8883 #for ssl encryption
topic = 'methane/mqtt'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'psusnec'
password = 'Psusnec06'
export_file = r"D:\pythonProject\MQTT\received_data.txt"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt.Client(client_id)
    # Set CA certificate
    client.tls_set(ca_certs=r'D:\pythonProject\MQTT\xuanwang\isrgrootx11.pem')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        with open(export_file, 'a') as file:
            file.write(f"Topic: {msg.topic}, Message: {msg.payload.decode()}\n")
    client.subscribe(topic, qos=0)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
