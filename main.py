from datalogger import PulseDataLogger
from datasink import MqttDataSink
import network, rp2, time, ntptime, json, machine
from pulsedetector import PinPulseDetector
from credentials import wifi_password, wifi_ssid
import uasyncio

from umqttsimple import MQTTClient

from machine import Pin

def add(a, b):
	print('adding..alkdjfs')
	return a + b

async def connect_to_wifi(password = wifi_password):
	rp2.country('GB')
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	print('Connecting...')
	while True:
		# while not wlan.isconnected() and wlan.status() >= 0:
		while not wlan.isconnected():
			wlan.connect(wifi_ssid, password)
			print('Waiting to connect...')
			print('wlan.status = {}'.format(wlan.status()))
			await uasyncio.sleep_ms(3000)
		connected = wlan.isconnected()
		if connected:
			print(wlan.ifconfig())
		else:
			print('Error: {}'.format(wlan.status()))
		return connected

async def set_clock():
	remaining_attempts = 10
	while remaining_attempts > 0:
		remaining_attempts -= 1
		try:
			print('attempting to set time...')
			ntptime.settime()
			print('time set')
			print(time.gmtime())
			return True
		except BaseException as e:
			print(e)
			if remaining_attempts == 0:
				return False
			await uasyncio.sleep_ms(5000)


def mqtt_connect(mqtt_server = '192.168.8.116', client_id = 'energymon'):
	client = MQTTClient(client_id, mqtt_server, keepalive=60)
	client.connect()
	print('Connected to %s MQTT Broker'%(mqtt_server))
	return client

async def main():
	clock_set = False
	while not clock_set:
		await connect_to_wifi()
		clock_set = await set_clock()

	# while True:
	# 	print('in main loop')
	# 	await uasyncio.sleep_ms(2000)
	data_sink = MqttDataSink()
	uasyncio.create_task(data_sink.run())

	data_logger = PulseDataLogger(onData=data_sink.sendGasPulse)
	
	pulse_detector = PinPulseDetector(data_logger.recordPulse)
	await uasyncio.create_task(pulse_detector.run())
	# while True:
	# 	print('main loop sending pulse')
	# 	await data_logger.recordPulse()
	# 	await uasyncio.sleep_ms(10000)


uasyncio.run(main())