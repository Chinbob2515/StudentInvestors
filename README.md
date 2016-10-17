# StudentInvestors

This is a terrible API for using the Student Investors (SI) website. You can pull lists of stock info from SI or from google, and request to buy or sell stocks (including just requesting the max amount).

The main file you need to use is Investor.py, and its StudentInvestor object.
Most uses are self-evident.

Initiate the StudentInvestor object- investor = StudentInvestor("User", "pass")

Sell stocks- investor.sellStock("III:LON", "max")

Buy stocks- investor.buyStock("III:LON", "max")

Get stock data- stocks = investor.getStocks()

Get team investement data- invs = investor.getInvestements()



WARNING- if you make too many requests for google stock data, they will just temp block your ip, leading to many 503 Service Denied errors. If this happens, stop your code for a bit, and rewrite it to make fewer requests. 
