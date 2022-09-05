import time

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
	
	def recordPulse(self):
		previous = self.previous
		datum = {
			'counter': self.counter,
			'timestamp': make_timestamp(),
		}
		self.counter += 1
		datum['secondsSincePrevious'] = datum['timestamp'] - previous['timestamp'] if previous != None else None
		self.previous = datum
		print('passing datum to sink')
		self.onData(datum)