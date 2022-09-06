import time, utime

def make_timestamp():
	timestamp = time.time()
	# timestamp = round(time.time_ns() / 1_000)
	print('making timestamp {} at {}'.format(timestamp, time.gmtime()))
	return timestamp

class PulseDataLogger:
	def __init__(self, onData):
		self.counter = 0
		self.onData = onData
		self.previous = None
		self.previous_ticks = None
	
	async def recordPulse(self):
		previous = self.previous
		datum = {
			'counter': self.counter,
			'timestamp': make_timestamp(),
		}
		self.counter += 1
		ticks_ms = utime.ticks_ms()
		datum['msSincePrevious'] = ticks_ms - self.previous_ticks if self.previous_ticks != None else None
		self.previous_ticks = ticks_ms
		self.previous = datum
		print('passing datum to sink')
		await self.onData(datum)