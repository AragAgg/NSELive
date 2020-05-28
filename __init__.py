print("""
# Stock module has been loaded #
    """)
import logging
logging.basicConfig(level=logging.DEBUG)
s = None
class stocks():

    # init function
    def __init__(self,Threads):
        from nsetools import Nse
        Nse = Nse()
        import requests
        import threading
        import json
        self.threading = threading
        # create a new variable for headers
        self.headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36"}
        # create a new array for stocks
        self.stocksArray = Nse.get_stock_codes()
        # create a new TCP Connection
        self.json = json
        # init an variable for number of threads
        self.threads = Threads
        self.s = requests.Session()
        print("initiated")

    def getMultiple(self,Stocks):
        print("getMultiple executed")
        self.data = []
        counter = 1
        for Stock in Stocks:
            if counter == self.threads:
                # Thread limit reached
                pendingThreads = self.threading.enumerate()
                for pThread in pendingThreads:
                    if pThread is self.threading.current_thread():
                        continue
                    pThread.join()
                counter = 1
            thread = self.threading.Thread(target=self.getInfo,args=(Stock,True))
            thread.start()
            counter += 1
        for thread in self.threading.enumerate():
            if thread is self.threading.current_thread():
                continue
            thread.join()
        tempArray = self.data
        del self.data
        return tempArray

    def getInfo(self,Name,Append):
        print("getInfo executed")
        # create a new dictionary for storing this stock's data
        dataArray = {

            'Name':Name,

        }
        # create a new variable for url for finincials
        finincialsurl = "https://www.nseindia.com/api/quote-equity?symbol="+Name
        bidAskurl = "https://www.nseindia.com/api/quote-equity?symbol="+Name+"&section=trade_info"

        try:

            finincerequest = self.s.get(url=finincialsurl,headers=self.headers)
            bidAskRequest = self.s.get(url=bidAskurl,headers=self.headers)

            finianceResult = self.json.loads(finincerequest.text)
            bidAskResult = self.json.loads(bidAskRequest.text)

        except self.json.decoder.JSONDecodeError:

            return "DecodeError"

        except KeyError:

            return "KeyError"

        except OSError:

            return "OSError"


        # parse this data
        # applicable conditions
        conditions = ('priceInfo' in finianceResult and 'price' in finianceResult['preOpenMarket']['preopen'][0] and finianceResult['priceInfo']['intraDayHighLow']['min'] is not 0 and finianceResult['priceInfo']['intraDayHighLow']['min'] is not None )


        if conditions != True:
            return False

        dataArray.update({
            'CBP':bidAskResult['marketDeptOrderBook']['bid'][0]['price'],
            'CSP':bidAskResult['marketDeptOrderBook']['ask'][0]['price'],
            'CBQ':bidAskResult['marketDeptOrderBook']['totalBuyQuantity'],
            'CSQ':bidAskResult['marketDeptOrderBook']['totalSellQuantity'],
            'TSQ':finianceResult['preOpenMarket']['totalBuyQuantity'],
            'TBQ':finianceResult['preOpenMarket']['totalSellQuantity'],
            'DayHigh':finianceResult['priceInfo']['intraDayHighLow']['max'],
            'DayLow':finianceResult['priceInfo']['intraDayHighLow']['min'],
            'WeekHigh':finianceResult['priceInfo']['weekHighLow']['max'],
            'WeekLow':finianceResult['priceInfo']['weekHighLow']['min'],
            'UpperCircuit':finianceResult['priceInfo']['upperCP'],
            'LowerCircuit':finianceResult['priceInfo']['lowerCP'],
            'Open':finianceResult['priceInfo']['open'],
            'Sector':finianceResult['info']['industry'],
            'CompanyName':finianceResult['info']['companyName']
        })
        if Append is not None:
            self.data.append(dataArray)
        return dataArray

    
    
    
    print("""
# Stocks module is ready to use #
    """)

