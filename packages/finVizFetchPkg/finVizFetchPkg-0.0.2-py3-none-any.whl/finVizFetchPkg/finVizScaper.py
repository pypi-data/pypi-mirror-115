# finviz scraping class
#TODO imports to init.py?

class finvizStreamer():
    #Declare class variables
    #---------------------
    #declare dictionary (key:value)  to store ticker and associated html tables
    news_tables = {} 
    
    #declare list (array) to store arrays of parsed data
    parsed_data = [] 
    tickers = [] 
    #---------------------
    #constructor
    def __init__(self):
        
        self.url = 'https://www.finviz.com/quote.ashx?t='
        #self.headers = {'Content-Type': 'application/json'}
 
    def scrape_finziz(self):
        from urllib.request import urlopen, Request
        import json
        from bs4 import BeautifulSoup
        import pandas as pd
        
        symbol = input('What is the stock symbol? (Please enter only one.)')

        finviz_url = 'https://www.finviz.com/quote.ashx?t='
        
        #print('tickers : ', tickers)
        
        tickers = [symbol]
        
        #print('tickers : ', tickers)
        #print('self.parsed_data : ', self.parsed_data)

        for ticker in tickers:
            print('ticker inside for loop: ', ticker)
            url = self.url + ticker

            req = Request(url = url, headers = {'user-agent': 'my-app'})
            print ("request url:" +url)
            response = urlopen(req)

            html = BeautifulSoup(response, 'html')
            news_table = html.find(id = 'news-table')
            self.news_tables[ticker] = news_table

        for ticker, news_table in self.news_tables.items():
            for row in news_table.findAll('tr'):

                title = row.a.get_text()
                link = row.a.get('href') #captures the link
                date_data = row.td.text.split(' ')

                if len(date_data) == 1: # if there is both a date and time it parses them into two columns
                    time = date_data[0]
                else: 
                    date = date_data[0] 
                    time = date_data[1]
                #print(ticker) #shows all of the ticker symbols in news_table
                self.parsed_data.append([ticker, date, time, title, link])
         
        df = pd.DataFrame(self.parsed_data, columns = ['ticker', 'date', 'time', 'title', 'link'])  

        self.news_tables.clear() #need to clear global dictionaries or data will be retained for each run
        self.parsed_data.clear() #need to clear global dictionaries or data will be retained for each run
        
        #del news_table #news_table is storing all of the previous runs so it must be deleted
    
        return df