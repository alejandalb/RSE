import argparse
import base64
import json
import logging
import signal
import struct
import sys
import time

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import paho.mqtt.client as mqtt
from datetime import datetime, timezone

#Variables para la recogida de datos
help_value = "/gettemp - Valor de la temperatura \n /getlum - Valor de la luminosidad \n /gethum - Valor de la humedad"
temp_value = "VOID"
lum_value = "VOID"
hum_value = "VOID"

#Parámetros de configuración de TTN
config = {
    "Broker": "eu1.cloud.thethings.network",
    "Username": "lopys2ttn@ttn",
    "Password": "NNSXS.A55Z2P4YCHH2RQ7ONQVXFCX2IPMPJQLXAPKQSWQ.A5AB4GALMW623GZMJEWNIVRQSMRMZF4CHDBTTEQYRAOFKBH35G2A",
    "Topic": "v3/+/devices/#"
}

#Parámetros de configuración del bot
user = "alalca3_bot"
bot = "rse2021_alalca3_bot"
token = "2129351678:AAH_3XRw-ra-LY7ppTa6H7IgsO4mdgwUHLA"


def on_connect(client, userdata, flags, rc):
    print("Connected to ", client._host, "port: ", client._port)
    print("Flags: ", flags, "returned code: ", rc)

    client.subscribe("v3/+/devices/#", qos=0)


def on_message(client, userdata, msg):
    global temp_value
    global lum_value
    global hum_value
    print("msg received with topic: {} and payload: {}".format(
        msg.topic, str(msg.payload)))

    if (msg.topic == "v3/lopys2ttn@ttn/devices/lopy4sense/up"):
        themsg = json.loads(msg.payload.decode("utf-8"))
        dpayload = themsg["uplink_message"]["decoded_payload"]

        print("@%s >> temp=%.3f hum=%.3f lux=%.3f" %
              (time.strftime("%H:%M:%S"), dpayload["temperature"],
               dpayload["lux"], dpayload["humidity"]))

        temp_value = dpayload["temperature"]
        lum_value = dpayload["lux"]
        hum_value = dpayload["humidity"]


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me! \n" + help_value)


# def getdata(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text=str(help_value))

#Funciones manejadoras

def gettemp(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=str(temp_value))

def gethum(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=str(hum_value))

def getlum(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=str(lum_value))

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command. \n" + help_value)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(
    config["Username"],
    password=config["Password"]
)
client.connect(config["Broker"], port=1883, keepalive=60)
client.loop_start()

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Asignamos los handlers

# getdata_handler = CommandHandler('getdata', getdata, pass_args=False)
# dispatcher.add_handler(getdata_handler)

gettemp_handler = CommandHandler('gettemp', gettemp, pass_args=False)
dispatcher.add_handler(gettemp_handler)

getlum_handler = CommandHandler('getlum', getlum, pass_args=False)
dispatcher.add_handler(getlum_handler)

gethum_handler = CommandHandler('gethum', gethum, pass_args=False)
dispatcher.add_handler(gethum_handler)

unknown_handler = MessageHandler(Filters.text & (~Filters.command), unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

updater.idle()
