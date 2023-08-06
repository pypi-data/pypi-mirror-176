from umqtt.robust import MQTTClient
myMqttClient = b'OS86Ig8YMhwkEzwGBREEDCA'
user = b'OS86Ig8YMhwkEzwGBREEDCA'
password = b'KsAem0D640xOi5BX/M27zR9o'
THINGSPEAK_URL = b"mqtt3.thingspeak.com"
client = MQTTClient(client_id=myMqttClient, user=user, password=password, server=THINGSPEAK_URL, ssl=False)
client.connect()
