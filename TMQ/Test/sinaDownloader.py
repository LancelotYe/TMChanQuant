from urllib import request
import json
import pandas as pd


def get_data(id):
    url_60m = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine60m?symbol='
    # url_60m = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine5m?symbol='
    url = url_60m + id
    req = request.Request(url)
    rsp = request.urlopen(req)
    res = rsp.read()
    res_json = json.loads(res)


    bar_list = []

    res_json.reverse()
    for line in res_json:
        bar = {}
        bar['Datetime'] = line[0]
        bar['Open'] = float(line[1])
        bar['High'] = float(line[2])
        bar['Low'] = float(line[3])
        bar['Close'] = float(line[4])
        bar['Volume'] = int(line[5])
        bar_list.append(bar)

    df = pd.DataFrame(data=bar_list)
    print(df)
    df.to_csv('./data.csv', index=None)

if __name__ == '__main__':
    get_data('rb1910')
