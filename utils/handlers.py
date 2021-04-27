import os
import csv
from logging import handlers
import time
import utils.customexceptions as exceptions

class CSVTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
	def __init__(self, filename, when='D', interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False, atTime=None,
                 errors=None, retryLimit=5, retryInterval=0.5,header="NO HEADER SPECIFIED"):
		self.RETRY_LIMIT = retryLimit
		self._header = header
		self._retryLimit = retryLimit
		self._retryInterval = retryInterval
		self._hasHeader = False
		super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
		if os.path.getsize(self.baseFilename) == 0:
			writer = csv.writer(self.stream, quoting=csv.QUOTE_ALL)
			writer.writerow(self._header)
		self._hasHeader = True

	def doRollover(self):
		self._hasHeader = False
		self._retryLimit = self.RETRY_LIMIT
		super().doRollover()
		writer = csv.writer(self.stream, quoting=csv.QUOTE_ALL)
		writer.writerow(self._header)
		self._hasHeader = True

	def emit(self, record):
		while self._hasHeader == False:
			if self._retryLimit == 0:
				raise exceptions.CouldNotBeReady
			time.sleep(self._retryInterval)
			self._retryLimit -= 1
			pass
		super().emit(record)