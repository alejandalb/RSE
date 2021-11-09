import paho.mqtt.client as mqtt

#THE_BROKER = "test.mosquitto.org"
#THE_TOPIC = "upv/rse/chat"
CLIENT_ID = ""
#USERNAME = "alalca3"

#Parámetros de configuración
config = {
    "Broker": "eu1.cloud.thethings.network",
    "Username": "lopys2ttn@ttn",
    "Password": "NNSXS.A55Z2P4YCHH2RQ7ONQVXFCX2IPMPJQLXAPKQSWQ.A5AB4GALMW623GZMJEWNIVRQSMRMZF4CHDBTTEQYRAOFKBH35G2A",
    "Topic": "v3/+/devices/#"
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)

    client.subscribe(config["Topic"])

# The callback for when a message is received from the server.    
def on_message(client, userdata, msg):
    print(msg.payload)

    
client = mqtt.Client(client_id=CLIENT_ID, 
                     clean_session=True, 
                     userdata=None, 
                     protocol=mqtt.MQTTv311, 
                     transport="tcp")

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(config["Username"], password=config["Password"])
client.connect(config["Broker"])

client.loop_forever()