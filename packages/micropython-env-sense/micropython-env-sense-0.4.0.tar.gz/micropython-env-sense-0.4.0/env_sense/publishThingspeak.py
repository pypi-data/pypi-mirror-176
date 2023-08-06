# https://opensource.org/licenses/GPL-3.0
# Publish to a thingspeak channel via MQTT

from umqtt.robust import MQTTClient


class ThingspeakMqtt:
    def __init__(self, credentials):
        THINGSPEAK_URL = b"mqtt3.thingspeak.com"
        self.client = MQTTClient(client_id=credentials['client_id'],
                                 user=credentials['client_id'],  # username==client_id for thingspeak
                                 password=credentials['password'],
                                 server=THINGSPEAK_URL,
                                 ssl=False)
        self.client.connect()
        self.channel_id = credentials['channel_id']

    def publish(self, payload):
        credentials = bytes("channels/{:s}/publish".format(self.channel_id), 'utf-8')
        mqtt_payload = ['{key}={val}'.format(key=key, val=val) for key, val in payload.items()]
        mqtt_payload = '&'.join(mqtt_payload) + '\n'
        mqtt_payload = bytes(mqtt_payload, 'utf-8')
        self.client.publish(credentials, mqtt_payload)
