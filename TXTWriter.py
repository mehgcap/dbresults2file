from base import DBResults2File
import codecs
from Exceptions import TXTWriterError

class TXTWriter(DBResults2File):

	def __init__(self,
		filename,
		headers,
		dbResultSet,
		delimiter = "\t",
		newLine = "\r\n",
		fileMode = "wb",
		*args, **kwargs
	):
		super(TXTWriter, self).__init__(filename, headers, dbResultSet, *args, **kwargs)
		self.delimiter = delimiter
		self.newLine = newLine
		self.fileMode = fileMode
		self.textFile = open(self.filename, self.fileMode)
		self.textFile.write("{data}{newLine}".format(data=self.delimiter.join(self._headerStrings), newLine=self.newLine))

	def createFile(self, printProgressInterval=0):
		try:
			for result in self.dbResultSet:
				self.textFile.write("{line}{newLine}".format(line=self.delimiter.join(self._arrayFromRow(result, forceStringConversion=self.forceStringConversion)), newLine=self.newLine))
				self.processedResultCount += 1
			self.textFile.close()
		except Exception as err:
			raise TXTWriterError(str(err))
