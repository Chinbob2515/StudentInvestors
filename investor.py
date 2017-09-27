import stockinfo, login as loggy, stack, time
from googleAPI import GoogleFinanceAPI
from bs4 import BeautifulSoup

#TODO: make it so it doesn't have to login each time.
#TODO: return a failure code if requests prompt an HTTP fail code

class StudentInvestor():
	
	def __init__(self, username, password):
		self.coreURL = "http://www.studentinvestor.org"
		self.username = username
		self.password = password
		self.google = GoogleFinanceAPI()
		self.lastGot = -1
		self.cachedStocks = {}
		self.log = loggy.Login(self.username, self.password)
	
	def _login(self):
		return self.log.doLog()
	
	def getStocks(self, LOG=False):
		
		self._login()
		
		#load html source
		html =  self.log.request(self.coreURL + "/stock-info.php")
		table = html.find(id="ftse100")
		table2 = html.find(id="ifs50")
		rows = table.find_all("tr")[1:] + table2.find_all("tr")[1:]
		
		tickerList = stockinfo.getStockData(google=0)
		if LOG: print sorted([i[2] for i in stockinfo.getStockData(google=0)]), "---------", sorted([i[2] for i in stockinfo.getStockData(google=1)])
		infos = {}
		for row in rows:
			infos[stack.rchop(row.find("a").contents[0], "/The")] = [[float(row.find_all("td")[3].contents[0]), float(row.find_all("td")[4].contents[0].split(" ")[0]), row.find(class_="tickercol").contents[0]],[]]
		if LOG: print "Starting load from google, may take some time..."
		for comp in stockinfo.getStockData(google=1):
			if LOG: print "Retrieved", comp[2], "from google;"
			data = self.google.get(comp[0], comp[1])
			infos[comp[2]][1] = [data["value"], data["%"], comp[0]+":"+comp[1]]
		# infos is a dictionary. each index is the name of a company in nice plain text. each value is 2 arrays, for SI and google data respectivly.
		# each array contains 3 values of [float, float, string], which are [pence price of stock, % change from opening price, stock ticker]
		self.cachedStocks = infos
		self.lastGot = time.time()
		return infos
	
	def getInvestements(self):
		
		self._login()
		
		html = self.log.request(self.coreURL+"/portfolio.php")
		table = html.find(id="stocks")
		if not table: # If the team has no stocks, return an empty dict
			return {}
		rows = table.find_all("tr")[1:]
		
		infos = {}
		for row in rows:
			infos[stack.rchop(row.find("a").contents[0], "/The")] = [float(row.find(class_="scpricecol").contents[0].replace(",","")), float(row.find_all("td")[5].contents[0].replace(",",""))]
		
		return infos
	
	def sellStock(self, ticker, quantity="max", type="active", note="Selling stocks to make a cool/chicken profit"):
		self._login()
		
		if quantity == "max":
			magicStartIndex = 17 # where in the sentence the max stock number usually is (I know, terrible)
			resp = self.log.request(self.coreURL+"/stock-sell.php?ticker="+ticker+"&type="+type)
			list = resp.find_all("ul")[2].find_all("li")[1].contents[0]
			#print "list-", stack.getNum(list[magicStartIndex:])
			quantity = stack.getNum(list[magicStartIndex:])
		
		return self.log.submit(self.coreURL+"/stock-sell.php",
			{"submitted":0, "confirmed":1, "type":type, "ifs-quantity":quantity, "ifs-note":note, "ticker":ticker, "ifs-cost": "noog"})
	
	def buyStock(self, ticker, quantity="max", type="active", note="Buying stocks to make a cool/chicken loss"):
		self._login()
		
		if quantity == "max":
			resp = self.log.request(self.coreURL+"/stock-buy.php?ticker="+ticker+"&type="+type)
			#print resp.prettify()
			try:
				list = resp.find_all("ul")[2].find_all("li")[1].contents[0]
			except Exception,e:
				print "ERROR BUYING STOCK-", e
				return -1
			#print "list-", stack.getNum(list[list.index("is")+3:])
			quantity = stack.getNum(list[list.index("is")+3:])
		
		return self.log.submit(self.coreURL+"/stock-buy.php",
			{"submitted":"0", "confirmed":"1", "type":type, "ifs-quantity":str(quantity), "ifs-note":note, "ticker":ticker, "ifs-cost": "nug"})
	

if __name__ == "__main__":
	print "Starting"
        username = ""
        password = ""
        with open("secret.txt", "r") as file:
          username, password = file.read().split("\n")[:2]
        investor = StudentInvestor(username, password)
	print investor.getInvestements()
	#print investor.sellStock("SHI:LN")
	#print investor.buyStock("III:LN")
	print "Finished"

