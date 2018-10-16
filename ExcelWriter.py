from base import DBResults2File
from Exceptions import ExcelWriterError
import xlsxwriter

class ExcelWriter(DBResults2File):

	def __init__(self,
		filename,
		headers,
		dbResultSet,
		comments={},
		formats=None,
		*args,
		**kwargs
	):
		super(ExcelWriter, self).__init__(filename, headers, dbResultSet, *args, **kwargs)
		self._filePath = filename
		self._comments = comments
		self._workbook = xlsxwriter.Workbook(self._filePath)
		self._worksheets = {} #keys: worksheet names as strings. Values: references to worksheet objects
		self._formats = {} #holds references to the actual format objects so we can use them, as opposed to the passed-in list of names and definitions
		if formats is not None:
			for formatName, formatDefinition in formats.iteritems():
				self._formats[formatName] = self._workbook.add_format(formatDefinition)
		#if dbResultSet is a dictionary, assume it's split by worksheets, so make each key a new worksheet
		if type(self.dbResultSet) is dict:
			[self.addWorksheet(sectionName) for sectionName in self.dbResultSet.keys()]
	
	def addFormat(self, formatName, formatValue):
		self._formats[formatName] = self._workbook.addFormat(formatValue)
	
	def addWorksheet(self, worksheetName):
		#make a new worksheet
		worksheet = self._workbook.add_worksheet(worksheetName)
		i = 0
		#if headers is a dictionary, get the section for this spreadsheet, else use the same headers for all spreadsheets
		if type(self.headers) is dict:
			try:
				headers = self.headers[worksheetName]
			except KeyError:
				raise ExcelWriterError("Headers was set up as a dictionary, but has no key for the worksheet name \"{name}\".".format(name=worksheetName))
		else:
			headers = self.headers
		#examine the headers for width and formatting information
		for i in range(len(headers)):
			header = headers[i]
			width = None
			if len(header) > 3: #get the extra parameters
				if type(header[3]) is int:
					width = header[3]
				elif type(header[3]) is str and header[3].lower() == "auto".lower():
					width = len(header[0])
				else:
					raise ExcelWriterError("Invalid value set for header width. Header name: {name}. Width: {width}".format(name=header[0], width=header[3]))
			format = None
			if len(header) > 4 and header[4] is not None:
				if header[4] in self._formats.keys():
					format = self._formats[header[4]]
				else:
					raise ExcelWriterError("Format \"{format}\" has not been added to this worksheet.".format(format=header[4]))
			worksheet.set_column(i, i, width, format)
		self._worksheets[worksheetName] = worksheet
	
	def populateWorksheet(self, worksheetName, data=None):
		if worksheetName not in self._worksheets.keys(): raise ExcelWriterError("No worksheet named \"{name}\" has been added.".format(name=worksheetName))
		if data is None: #assume we are to use the proper section from self.dbResultSet instead
			if type(self.dbResultSet) == dict:
				if worksheetName not in self.dbResultSet.keys():
					raise ExcelWriterError("Database results dictionary has no key that matches \"{name}\"".format(name=worksheetName))
				data = self.dbResultSet[worksheetName]
			else: #we don't have a dictionary, so just use the whole result set
				data = self.dbResultSet
		#write the column headers
		[self._worksheets[worksheetName].write(0, i, self._headerStrings[i]) for i in range(len(self._headerStrings))]
		#now write the data
		#yes, the below could be a list comprehension, but it would be very long and confusing to read
		for i in range(len(data)):
			self._worksheets[worksheetName].write_row((i+1), 0, self._arrayFromRow(data[i]))
		if worksheetName in self._comments.keys():
			[self._worksheets[worksheetName].write_comment(comment[0], comment[1], comment[2]) for comment in self._comments[worksheetName]]

	def createFile(self):
		#if no work has been done on the workbook, create a blank worksheet and put our DB results in it
		#if we already have a worksheet, assume the user called populateWorksheet and is managing things themselves, so don't do it for them
		if len(self._worksheets) == 0:
			self.addWorksheet("Worksheet 1")
			#self.populateWorksheet("worksheet 1")
		#now populate the worksheet(s)
		if type(self.dbResultSet) == dict:
			[self.populateWorksheet(worksheetName) for worksheetName in self._worksheets.keys()]
		else:
			self.populateWorksheet(self._worksheets.keys()[0], self.dbResultSet)
		self._workbook.close()