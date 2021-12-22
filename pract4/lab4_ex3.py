import sys
import time
import base64

import json
import struct

import paho.mqtt.client as mqtt

TTN = {
    "Broker": "eu1.cloud.thethings.network",
    "Topic": "v3/+/devices/#",
    "Username": "lopys2ttn@ttn",
    "Password": "NNSXS.A55Z2P4YCHH2RQ7ONQVXFCX2IPMPJQLXAPKQSWQ.A5AB4GALMW623GZMJEWNIVRQSMRMZF4CHDBTTEQYRAOFKBH35G2A"
} 

UBIDOTS = {
    "Broker": "things.ubidots.com",
    "Topic": "/v1.6/devices/alalca3-p3",
    "Username": "BBFF-wvQS9vdw11PtIAGfbBNcInFhe7QV6h",
    "Password": None
}

def on_connectTTN(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)

    client.subscribe(TTN["Topic"])

def on_connectUBI(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)

# The callback for when a message is received from the server.
def on_messageTTN(client, userdata, msg):
#    print("sisub: msg received with topic: {} and payload: {}".format(msg.topic, str(msg.payload)))
    print("sisub: msg received with topic: {} ".format(msg.topic))

    if (msg.topic == "v3/lopys2ttn@ttn/devices/lopy4sense/up"):

        themsg = json.loads(msg.payload.decode("utf-8"))
        dpayload = themsg["uplink_message"]["decoded_payload"]
        msg_to_be_sent = {"variable" : dpayload["temperature"]}

        print(dpayload["temperature"])

        clientUBI.publish(UBIDOTS["Topic"],
            payload=json.dumps(msg_to_be_sent))



clientTTN = mqtt.Client()
clientUBI = mqtt.Client()

clientTTN.on_connect = on_connectTTN
clientTTN.on_message = on_messageTTN
clientUBI.on_connect = on_connectUBI

clientTTN.username_pw_set(TTN["Username"], password=TTN["Password"])
clientTTN.connect(TTN["Broker"])

clientUBI.username_pw_set(UBIDOTS["Username"], UBIDOTS["Password"])
clientUBI.connect(UBIDOTS["Broker"])

clientTTN.loop_forever()

