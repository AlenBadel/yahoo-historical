import datetime as dt
import pandas as pd
import requests
import re
import time
import datetime

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

class Fetcher:
    api_url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=%s&events=%s&crumb=%s"
    def __init__(self):

        self.cookie = None
        self.crumb = None

    def getCookie(self, ticker):
        """Returns a tuple pair of cookie and crumb used in the request"""
        url = 'https://finance.yahoo.com/quote/%s/history' % (ticker)
        r = requests.get(url)
        txt = r.content
        cookie = r.cookies['B']
        pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

        for line in txt.splitlines():
            m = pattern.match(line.decode("utf-8"))
            if m is not None:
                crumb = m.groupdict()['crumb']
                crumb = crumb.replace(u'\\u002F', '/')

        return cookie, crumb  # return a tuple of crumb and cookie

    def getData(self, events, ticker, start=None, end=None, interval='1d'):

        endTime = None
        startTime = None

        #Ticker needs to be uppercase
        ticker = ticker.upper()
        #Replace class seperators '.' with '-'
        ticker = ticker.replace('.', '-')

        #Make sure we have a cookie and crumb
        if(self.cookie is None and self.crumb is None):
            self.cookie, self.crumb = self.getCookie(ticker)

        if(start is None):
            startTime = 0
        else:
            startTime = int(time.mktime(dt.datetime(start[0],start[1],start[2]).timetuple()))

        if end is not None:
            endTime = int(time.mktime(dt.datetime(end[0],end[1],end[2]).timetuple()))
        else:
            endTime = int(time.time())

        """Returns a list of historical data from Yahoo Finance"""
        if interval not in ["1d", "1wk", "1mo"]:
            raise ValueError("Incorrect interval: valid intervals are 1d, 1wk, 1mo")

        url = self.api_url % (ticker, startTime, endTime, interval, events, self.crumb)
        #print("Debug: url")
        #print(url)

        data = requests.get(url, cookies={'B':self.cookie})
        content = StringIO(data.content.decode("utf-8"))
        return pd.read_csv(content, sep=',')


    def getHistorical(self, ticker, start=None, end=None, interval='1d'):
        """Returns a list of historical price data from Yahoo Finance"""
        return self.getData('history', ticker, start, end, interval)

    def getDividends(self, ticker, start=None, end=None, interval='1d'):
        """Returns a list of historical dividends data from Yahoo Finance"""
        return self.getData('div', ticker, start, end, interval)

    def getSplits(self, ticker, start=None, end=None, interval='1d'):
        """Returns a list of historical splits data from Yahoo Finance"""
        return self.getData('split', ticker, start, end , interval)

    def getDatePrice(self, ticker, start=None, end=None, interval='1d'):
        """Returns a DataFrame for Date and Price from getHistorical()"""
        return self.getHistorical(ticker, start, end, interval).ix[:,[0,4]]

    def getDateVolume(self, ticker, start=None, end=None, interval='1d'):
        """Returns a DataFrame for Date and Volume from getHistorical()"""
        return self.getHistorical(ticker, start, end, interval).ix[:,[0,6]]

