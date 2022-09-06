import uasyncio
import random

import machine

class FakePulseDetector:
	def __init__(self, on_pulse) -> None:
		self.on_pulse = on_pulse
	
	async def run(self):
		while True:
			random_delay = round(random.random() * 15000 + 5000)
			print('next pulse in {}ms...'.format(random_delay))
			await uasyncio.sleep_ms(random_delay)
			await self.on_pulse()

class PinPulseDetector:
	def __init__(self, on_pulse) -> None:
		self.on_pulse = on_pulse
		self.pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
	
	async def run(self):
		last_open = True
		while True:
			if self.pin.value() == 1:
				last_open = True
				await uasyncio.sleep_ms(100)
			else:
				if last_open:
					print('transmitting pulse')
					await self.on_pulse()
				last_open = False
				await uasyncio.sleep_ms(1000)