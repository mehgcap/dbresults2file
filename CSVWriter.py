from base import DBResults2File
import codecs
import csv
from Exceptions import CSVWriterError

class CSVWriter(DBResults2File):

	def __init__(self,
		filename,
		headers,
		dbResultSet,
		delimiter = ",",
		dialect="excel",
		*args, **kwargs
	):
		super(CSVWriter, self).__init__(filename, headers, dbResultSet, *args, **kwargs)
		self.delimiter = delimiter
		self.dialect = dialect
		self.csvFile = codecs.open(self.filename, "wb")
		self.csvWriter = csv.writer(self.csvFile, dialect=self.dialect, delimiter=self.delimiter)

	def createFile(self, printProgressInterval=0):
		try:
			self.csvWriter.writerow(self._headerStrings)
			for result in self.dbResultSet:
				self.csvWriter.writerow([info for info in self._arrayFromRow(result)])
				self.processedResultCount += 1
				if printProgressInterval > 0 and self.processedResultCount % printProgressInterval == 0: print "Items processed: %s" %(self.processedResultCount)
			self.csvFile.close()
		except Exception as err:
			raise CSVWriterError(str(err))

