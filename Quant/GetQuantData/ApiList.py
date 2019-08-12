list500CompaniesInWiki = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

yahoo_url = "http://ichart.finance.yahoo.com/table.csv"



#test

import datetime
import requests
ticker = "AAPL"
# start_date=(2000,1,1)
start_date=(2019,8,1)
end_date=datetime.date.today().timetuple()[0:3]
ticker_tup = (
    ticker, start_date[1]-1, start_date[2],
    start_date[0], end_date[1]-1, end_date[2],
    end_date[0]
)
yahoo_url = yahoo_url
yahoo_url += "?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"
yahoo_url = yahoo_url % ticker_tup
try:
    yf_data = requests.get(yahoo_url).text.split("\n")[1:-1]
    prices = []
    for y in yf_data:
        p = y.strip().split(',')
        prices.append(
            (datetime.datetime.strptime(p[0], '%Y-%m-%d'),
             p[1], p[2], p[3], p[4], p[5], p[6])
        )
except Exception as e:
    print("Could not download Yahoo data: %s" % e)
