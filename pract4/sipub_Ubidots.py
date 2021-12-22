# File: sipub.py
#
# The simplest MQTT producer.

import random
import time
import json

import paho.mqtt.client as mqtt

THE_BROKER = "things.ubidots.com"
THE_TOPIC = "/v1.6/devices/alalca3-p3"
CLIENT_ID = "BBFF-wvQS9vdw11PtIAGfbBNcInFhe7QV6h"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)

# The callback for when a message is published.
def on_publish(client, userdata, mid):
    print("sipub: msg published (mid={})".format(mid))


client = mqtt.Client(client_id=CLIENT_ID,
                     clean_session=True, 
                     userdata=None, 
                     protocol=mqtt.MQTTv311, 
                     transport="tcp")

client.on_connect = on_connect
client.on_publish = on_publish

client.username_pw_set(CLIENT_ID, password=None)
client.connect(THE_BROKER, port=1883, keepalive=60)

client.loop_start()

while True:
    randint= random.randint(0, 100)
    msg_to_be_sent = json.dumps({"variable": str(randint)})
    client.publish(THE_TOPIC, 
                   payload=msg_to_be_sent, 
                   qos=0, 
                   retain=False)

    time.sleep(15)

client.loop_stop()