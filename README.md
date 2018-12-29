# dbresults2file
a Python package that makes it easy to generate spreadsheets or text files from database query results

##Description
This Python package aims to make it simple to go from a set of database results to a file you can look at, or send your boss, or whatever you need to do.  So long as you use PyODBC, or pass in an array of dicts that the package can work with, you should have no trouble.

##Features

* create CSV, XLSX, or TXT files
* handle errors by excepting Exception subclasses for each file type, making error handling easier
* the package tries to handle encoding problems by converting to UTF-8, though support for text encodings is *not* promised
* supports setting column widths for XLSX files
* Lets you pass a function to a column, which will be called with each row's value for that cell before the result is placed in the file. Great for converting dates to a different format, changing text case, etc.
* supports customizing the column and line separators for TXT files

##Basic Example
The first thing you have to do is define the headers. This is an array of arrays, where each sub-array lays out the column name, the index (as a string or number) of the field that will be placed in the column, a function that will be given the value of the column, and so on.

Say our result set is simply a list of fruits and their colors. Something like

(fruit, color)
(apple, red)
(orange, orange)
(blueberry, blue)
(blackberry, black)

We might use this set of headers to make a spreadsheet from our list:

headers = [
	("Fruit Name", "fruit"),
	("Color", "color")
]
	
Now, we can make a CSV of this data in just a few lines, like this:

filename = "fruits.csv"
csvWriter = dbresults2file.CSVWriter(filename, headers, results)
try:
	csvWriter.createFile()
except dbresults2file.CSVWriterError err:
	#handle the error

That's it. Once you get a result set and set up your headers, you can make a text file, a CSV file, or an Excel spreadsheet pretty simply.
