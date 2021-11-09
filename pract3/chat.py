# File: sipub.py
#
# The simplest MQTT producer.
import time

import paho.mqtt.client as mqtt

THE_BROKER = "test.mosquitto.org"
THE_TOPIC = "upv/rse/chat"
CLIENT_ID = ""
USERNAME = "alalca3"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)
    client.subscribe(THE_TOPIC, qos=0)

# The callback for when a message is published.
#def on_publish(client, userdata, mid):
#    print("sipub: msg published (mid={})".format(mid))

# The callback for when a message is received from the server.
def on_message(client, userdata, msg):
    print((msg.payload))

client = mqtt.Client(client_id=CLIENT_ID, 
                     clean_session=True, 
                     userdata=None, 
                     protocol=mqtt.MQTTv311, 
                     transport="tcp")

client.on_connect = on_connect
#client.on_publish = on_publish
client.on_message = on_message

client.username_pw_set(None, password=None)
client.connect(THE_BROKER, port=1883, keepalive=60)

client.loop_start()

time.sleep(5)
print("Puede escribir mensajes desde la línea de comandos. Para salir del chat escriba ESC")
while client.is_connected:
    mensaje = input("")
    if mensaje == "ESC":
        print("Saliendo del chat.......")
        break
    msg_to_be_sent = "[{}]: {}".format(USERNAME, mensaje)
    client.publish(THE_TOPIC, 
    payload=msg_to_be_sent, 
    qos=0, 
    retain=False)
client.loop_stop()
