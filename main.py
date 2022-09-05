from datalogger import PulseDataLogger
from datasink import MqttDataSink
import network, rp2, time, ntptime, json, machine
from credentials import wifi_password, wifi_ssid

from umqttsimple import MQTTClient

from machine import Pin

def add(a, b):
	print('adding..alkdjfs')
	return a + b

def connect_to_wifi(password = wifi_password):
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
			time.sleep(3)
		connected = wlan.isconnected()
		if connected:
			print(wlan.ifconfig())
		else:
			print('Error: {}'.format(wlan.status()))
		return connected


def set_clock():
	remaining_attempts = 10
	while remaining_attempts > 0:
		remaining_attempts -= 1
		try:
			print('attempting to set time...')
			ntptime.settime()
			print('time set')
			print(time.gmtime())
			return
		except:
			if remaining_attempts == 0:
				machine.reset()
				raise
			time.sleep(5)


def mqtt_connect(mqtt_server = '192.168.8.116', client_id = 'energymon'):
	client = MQTTClient(client_id, mqtt_server, keepalive=60)
	client.connect()
	print('Connected to %s MQTT Broker'%(mqtt_server))
	return client

def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

def main():
	connect_to_wifi()
	set_clock()
	data_sink = MqttDataSink()
	data_logger = PulseDataLogger(onData=data_sink.publish_gas_pulse)
	
	while True:
		data_logger.recordPulse()
		time.sleep(10)
	# message = {
	# 	'timestamp': round(time.time_ns() / 1_000_000)
	# }
	# client.publish('energymonitor/test', msg=json.dumps(message))
	# print('published message')
	# led = Pin('LED', Pin.OUT)
	# while True:
	# 	print('loop...')
	# 	led.value(1)
	# 	utime.sleep(1)
	# 	led.value(0)
	# 	utime.sleep(2)

main()