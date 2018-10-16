class DBResults2FileException(Exception):
	def __init__(self, message, *args, **kwargs):
		super(DBResults2FileException, self).__init__(*args, **kwargs)
		self._message = message

	def __str__(self):
		return str(self._message)

class CSVWriterError(DBResults2FileException):
	def __init__(self, message):
		super(CSVWriterError, self).__init__(message)

class ExcelWriterError(DBResults2FileException):
	
	def __init__(self, message):
		super(ExcelWriterError, self).__init__(message)

class TXTWriterError(DBResults2FileException):
	def __init__(self, message):
		super(TXTWriterError, self).__init__(message)

