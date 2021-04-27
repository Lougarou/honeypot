import logging
import csv
import io

class CSVFormatter(logging.Formatter):
	def __init__(self):
		super().__init__()
	def format(self, record):
		stringIO = io.StringIO()
		writer = csv.writer(stringIO, quoting=csv.QUOTE_ALL)
		writer.writerow(record.msg)
		record.msg = stringIO.getvalue().strip()
		return super().format(record)