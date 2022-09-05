from umqttsimple import MQTTClient
import json

class MqttDataSink:
	def __init__(self, mqtt_server = '192.168.8.116', client_id = 'energymon'):
		self.mqtt_server = mqtt_server
		self.client_id = client_id
		self.reconnect()
	
	def publish_gas_pulse(self, pulseMessage):
		print('publishing message')
		while True:
			try:
				self.client.publish('energymonitor/gas/pulse', msg=json.dumps(pulseMessage))
				print('published message')
				return
			except:
				print('Error publishing message. Attempting MQTT reconnect')
				self.reconnect()

	
	def reconnect(self):
		self.client = MQTTClient(self.client_id, self.mqtt_server, keepalive=60)
		self.client.connect()
		print('Datasink connected to %s MQTT Broker'%(self.mqtt_server))