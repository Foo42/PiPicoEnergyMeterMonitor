from umqttsimple import MQTTClient
import json
import queue

class MqttDataSink:
	def __init__(self, mqtt_server = '192.168.8.116', client_id = 'energymon'):
		self.mqtt_server = mqtt_server
		self.client_id = client_id
		self.queue = queue.Queue()

		self.reconnect()
	
	async def run(self):
		while True:
			pulseMessage = await self.queue.get()
			print('Data sink received pulse')
			sent = False
			while not sent:
				try:
					print('Data sink attempting to publish pulse...')
					self.client.publish('energymonitor/gas/pulse', msg=json.dumps(pulseMessage))
					print('published message')
					sent = True
				except:
					print('Error publishing message. Attempting MQTT reconnect')
					self.reconnect()

	async def sendGasPulse(self, pulseMessage):
		await self.queue.put(pulseMessage)
	
	def reconnect(self):
		self.client = MQTTClient(self.client_id, self.mqtt_server, keepalive=60)
		self.client.connect()
		print('Datasink connected to %s MQTT Broker'%(self.mqtt_server))