# Grab the tips from Options.xml

from xmllib import *
import string, os

print "Extracting translatable bits from Options.xml..."

class Parser(XMLParser):
	data = ""

	def unknown_starttag(self, tag, attrs):
		for x in ['title', 'label', 'end', 'unit']:
			if attrs.has_key(x):
				self.trans(attrs[x])
		self.data = ""
	
	def handle_data(self, data):
		self.data = self.data + data
	
	def unknown_endtag(self, tag):
		data = string.strip(self.data)
		if data:
			self.trans(data)
	
	def trans(self, data):
		data = string.join(string.split(data, '\n'), '\\n')
		if data:
			out.write('_("%s")\n' % data)

try:
	os.chdir("po")
except OSError:
	pass
	
file = open('../Options.xml', 'rb')
out = open('../tips', 'wb')
parser = Parser()
parser.feed(file.read())
file.close()
parser.close()
out.close()
