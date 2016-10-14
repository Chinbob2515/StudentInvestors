import urllib2, json, stockinfo

class GoogleFinanceAPI: # Oh praise stackoverflow, for providing me with this glourious bountry of code. It pulls from this wierd google website, with a ticker symbol,
			# which then returns a shit tonne of randomly labelled data. Some correlates to stock value, change, etc., so I put it in better places in the
			# returned dictionary, then pass on that.
	def __init__(self):
		self.prefix = "http://finance.google.com/finance/info?client=ig&q=" # oh shit too many requests and google just stops caring. we need to give google some time.
	
	def get(self,symbol,exchange):
		url = self.prefix+"%s:%s"%(exchange,symbol)
		u = urllib2.urlopen(url)
		content = u.read()
		
		obj = json.loads(content[3:])
		obj[0]["value"] = float(obj[0]["l"].replace(",", ""))
		obj[0]["grad"] = float(obj[0]["c"].replace(",", ""))
		obj[0]["%"] = float(obj[0]["c_fix"].replace(",", ""))
		return obj[0]

if __name__ == "__main__":
	c = GoogleFinanceAPI()
	
	stocks = stockinfo.getStockData()
	print "Read stock info, now just printing them to prove we can pull data."
	
	for stock in stocks:
		got = c.get(stock[0], stock[1]) # Request stock data from google
		print (stock[0], stock[1], stock[2]), "is value:", got["value"], "; grad:", got["grad"], "; and %:", got["%"] # Pretty print the received data
	
