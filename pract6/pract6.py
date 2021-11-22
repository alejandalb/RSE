from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('telegraf')

results = client.query('select * from TTN WHERE time > now() - 15m')

points=results.get_points()
for item in points:  
    if (item['uplink_message_decoded_payload_temperature'] != None and item['uplink_message_decoded_payload_humidity'] != None):
        print(item['time'], " Temperature-> ", item['uplink_message_decoded_payload_temperature'])
        print(item['time'], " Humidity-> ", item['uplink_message_decoded_payload_humidity'])