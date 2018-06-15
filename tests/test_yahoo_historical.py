from yahoo_historical import Fetcher


print("Starting Yahoo Historical Test")
yahooDataSource = Fetcher()
print("Get Historical for T")
data = yahooDataSource.getHistorical("T", [1998,3,1], [2017,1,1])
print("Printing Result")
print(data)
print("Get Historical MAX for T")
data = yahooDataSource.getHistorical("T")
print("Printing Result")
print(data)
print("Getting Historical Data for AAPL")
data = yahooDataSource.getHistorical("AAPL", [2007,1,1], [2017,1,1])
print("Printing Result")
print(data)
