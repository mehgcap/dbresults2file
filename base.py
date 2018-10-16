class DBResults2File(object):

	def __init__(self,
		filename,
		headers,
		dbResultSet,
		textEncoding="utf8",
		forceStringConversion=False
	):
		"""filename: the path and name of the output file to create
		dbResultSet: a pyodbc.execute() result. This must be an iterable object with indexable objects in it.
		Headers: an array of tuples in the form (string, index) where string is the header (appears at the top of the column) and index is the index of the column's information in each row of dbResultSet.
		Optionally, a third item can appear in the tuple: a function. If present, the function will be called, getting passed the current item. Good for formatting a date, for instance."""

		self.filename = filename
		self.dbResultSet = dbResultSet
		self.headers = headers
		self.forceStringConversion = forceStringConversion
		self._headerStrings = []
		[self._headerStrings.append(i[0]) for i in self.headers]
		self.textEncoding = textEncoding
		self.processedResultCount = 0

	def createFile(self, printProgressInterval=0):
		raise NotImplementedError

	def _arrayFromRow(self, row, headers=None, forceStringConversion=False):
		"""Returns an array of items to be written to the file. Expects a row of DB results and an array of header tuples. Falls back to self.headers if none are provided."""
		resultInfo = [] #stores the items to be returned, after being pulled from the row and transformed
		if headers is None: headers = self.headers
		for header in headers:
			if type(header[1]) is int:
				obj = row[header[1]] #header[1] is the index in the row where this header's result is found
			else:
				obj = getattr(row, header[1]) #this lets us access attributes of objects, since pyodbc supports something like row.field_name
			if len(header) == 3 and header[2] is not None and callable(header[2]): obj = header[2](obj) #if a function was included, run the object through it first
			if type(obj)is unicode: #most file outputters can't handle unicode, so encode it first
				obj = obj.encode(self.textEncoding)
			if forceStringConversion:
				obj = str(obj)
			resultInfo.append(obj)
		return resultInfo
