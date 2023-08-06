class finData():
    def __init__(self, key):
        self.key = key

    def getTickers(self,index):
        indexTicketGet = rs.get(f'https://eodhistoricaldata.com/api/exchange-symbol-list/{index}?api_token={self.key}&fmt=json').json() 
        tickerList = [item['Code'] for item in indexTicketGet]
        return tickerList
    
    def getRawFundData (self,TICKER):
        return rs.get(f'https://eodhistoricaldata.com/api/fundamentals/{TICKER}.US?api_token={self.key}').json()
