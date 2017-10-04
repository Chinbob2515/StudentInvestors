import urllib2, json, stockinfo

from yahoo_finance import Share

class AlphaFinanceAPI:
	def __init__(self):
		self.prefix = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=1min&apikey=EJJ81YLLY6C4OLYI"
	
	def get(self,symbol):
		#if obj[0]["c"] == "": obj[0]["c"] = "-500" # If any value is missing, assume the worst(ish)
		#if obj[0]["l"] == "": obj[0]["l"] = "-500"
		#if obj[0]["c_fix"] == "": obj[0]["c_fix"] = "-500"
		#obj[0]["value"] = float(obj[0]["l"].replace(",", ""))
		#obj[0]["grad"] = float(obj[0]["c"].replace(",", ""))
		#obj[0]["%"] = float(obj[0]["c_fix"].replace(",", ""))
		
		url = self.prefix % (symbol+".L") # Add .L to represent that this is the London Stock Exchange- as all in game should be as of 2017.
		u = urllib2.urlopen(url)
		content = u.read()
		obj = json.loads(content)["Time Series (1min)"]
		sortedKeys = sorted(obj.iterkeys()) # Get the keys sorted timewise
		recentValue = obj[sortedKeys[-1]] # Get the most recent time period value
		
		value = float(recentValue["4. close"])
		grad = value-float(recentValue["1. open"])
		percentChange = grad/value
		
		return {"value": value, "grad": grad, "%": percentChange}

if __name__ == "__main__":
	
	a = AlphaFinanceAPI()
	print a.get("III")
	
	"""c = GoogleFinanceAPI()
	
	stocks = stockinfo.getStockData()
	print "Read stock info, now just printing them to prove we can pull data."
	
	for stock in stocks:
		got = c.get(stock[0], stock[1]) # Request stock data from google
		print (stock[0], stock[1], stock[2]), "is value:", got["value"], "; grad:", got["grad"], "; and %:", got["%"] # Pretty print the received data"""
