import stockinfo, login as loggy, stack, time
from alphaAPI import AlphaFinanceAPI
from bs4 import BeautifulSoup

#TODO: make it so it doesn't have to login each time.
#TODO: return a failure code if requests prompt an HTTP fail code

class StudentInvestor():
	
	def __init__(self, username, password):
		self.coreURL = "http://www.studentinvestor.org"
		self.username = username
		self.password = password
		self.broker = AlphaFinanceAPI()
		self.lastGot = -1
		self.cachedStocks = {}
		self.log = loggy.Login(self.username, self.password)
	
	def _login(self):
		return self.log.doLog()
	
	def getStocks(self, LOG=False):
		
		self._login()
		
		# Load SI page to get what stocks we need, and info on them.
		html =  self.log.request(self.coreURL + "/stock-info.php")
		table = html.find(id="ftse100")
		table2 = html.find(id="ifs50")
		# Concatenate rows into a single list of all stock info
		rows = table.find_all("tr")[1:] + table2.find_all("tr")[1:]
		
		infos = {}
		for row in rows:
			info = [[], []]
			
			# Scrape info from SI HTML
			index = row.find("th").a.string # The name of the companies are in the <th>'s
			change = float(row.findAll("td")[4].string.split(" ")[1].strip("(").strip("%)")) # The percent change is in the last <td>'s, as the second word, surrounded with unneccesary brackets and a percent sign
			ticker = row.find("td", {"class":"tickercol"}).string # The ticker is stored in the <td>'s with class tickercol
			#if ticker in ["ADM:LN", "BA/:LN", "BT/A:LN", "DCC:LN", "DLG:LN",  "HL/:LN",  "INF:LN",  "IAG:LN",  "MDC:LN",  "PPB:LN",  "RDSA:LN",  "SKY:LN",  "SKG:LN",  "STJ:LN",  "TUI:LN",  "WPP:LN",  "ABC:LN",  "BEZ:LN",  "BKG:LN",  "DMGT:LN",  "EVR:LN",  "NXG:LN",  "OCDO:LN",  "RNK:LN",  "SAFE:LN",  "SVS:LN",  "SHB:LN",  "SHI:LN",  "TALK:LN",  "TCAP:LN",  "VEC:LN",  "VSVS:LN",  "YOU:LN",  "ZYT:LN"]: continue
			value = float(row.findAll("td")[3].string) # The value of the stock in pence is in the fourth <td>'s
			info[0] = [value, change, ticker] # Assemble info into a list
			
			# Request info from broker API
			brokerTicker = ticker.split(":")[0].strip("/") # Change ticker into correct format.
			try: brokerObj = self.broker.get(brokerTicker)
			except: continue
			value = brokerObj["value"]
			change = brokerObj["%"]
			info[1] = [value, change, brokerTicker]
			
			infos[index] = info
		
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
	import time
	print "Starting", time.time()
        username = ""
        password = ""
        with open("secret.txt", "r") as file:
          username, password = file.read().split("\n")[:2]
        investor = StudentInvestor(username, password)
	print len(investor.getStocks())
	#print investor.sellStock("SHI:LN")
	#print investor.buyStock("III:LN")
	print "Finished", time.time()

