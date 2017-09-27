
def getStockData(google=1):
	if google:
		return getStockDataForGoogle()
	else:
		return getStockDataForSI()

def getStockDataForGoogle():
	
	invalids = ["ARM", "BG", "ALNT", "TCY", "AN/"] # For some reason these ones always fail to load, crashing everything.
	invalids = [i+":LN" for i in invalids] # Ticker symbols need to specify it's the london stock exchange (lon[don]).
	
	fileT = ""
	with open("resources/names3.txt", "r") as f: # Read ticker symbols from the file.
		fileT = f.read().replace("/The", "").replace("/", ".")
	
	stocks = []
	for stock in [i for i in fileT.replace("\r","").split("\n") if not (':'.join(i.split(":")[:2])) in invalids and i != '']: # Simple parsing to get only valid stock ticker symbols.
		stockO = stock.split(":")
		stockO[1] = "lon"
		stockO[0] = stockO[0].strip(".").lower()
		stocks.append(stockO)
	return stocks

def getStockDataForSI():
	
	invalids = ["arm", "bg", "alnt", "tcy", "an/"] # For some reason these ones always fail to load, crashing everything.
	invalids = ["lon:"+i for i in invalids] # Ticker symbols need to specify it's the london stock exchange (lon[don]).
	
	fileT = ""
	with open("resources/names3.txt", "r") as f: # Read ticker symbols from the file.
		fileT = f.read() #.replace("/The", "")
	
	stocks = []
	for stock in [i for i in fileT.replace("\r","").split("\n") if not i in invalids and i != '']: # Simple parsing to get only valid stock ticker symbols.
		stockO = stock.split(":")
		stocks.append(stockO)
	return stocks
