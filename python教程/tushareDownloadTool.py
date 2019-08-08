

import requests,io,random,os
import pandas as pd
from datetime import datetime

stock="sz000868" #安凯客车股票代码
path = os.path.join(os.getcwd(), 'data')

for x1 in range(2017,2018):
    data=pd.DataFrame(columns=['date','time','datetime' 'price', 'change', 'volume','amount','type'])
    for x2 in range(1,13):
        ipAddress = str(random.randint(0,255))+'.'+str(random.randint(0,255))+'.'+str(random.randint(0,255))+'.'+str(random.randint(0,255))
        headers = {"X-Forwarded-For": ipAddress}
        for x3 in range(1,32):
            if x2<10 and x3<10:
                Date=str(x1)+'-0'+str(x2)+'-0'+str(x3)
            elif x2<10 and x3>9:
                Date=str(x1)+'-0'+str(x2)+'-'+str(x3)
            elif x2>9 and x3<10:
                Date=str(x1)+'-'+str(x2)+'-0'+str(x3)
            elif x2>9 and x3>9:
                Date=str(x1)+'-'+str(x2)+'-'+str(x3)
            print(x2,x3,Date)
            params = {"date": Date, "symbol": stock}
            url = 'https://market.finance.sina.com.cn/downxls.php'
            r = requests.get(url, params=params, headers=headers)
            r.encoding = 'gbk'
            df= pd.read_table(io.StringIO(r.text), names=['time', 'price', 'change', 'volume', 'amount', 'type'],
                                skiprows=[0])
#            #print(df)
            #当列表值大于三的时候 才转换对日期进行格式
            if len(df.index)>3:
                tempDatetime = datetime.strptime(Date, "%Y-%m-%d")  #string--->datetime
                Date = tempDatetime.strftime("%Y%m%d" )        #datetime-->string
            df['date']=Date
            df=df.sort_values(by=['time'],ascending=True)#按列进行排序
            timelist=list(df['time'])
#            #print(len(timelist))
            if len(timelist)>3:
                try:
                    times=[datetime.strptime(val, "%H:%M:%S").strftime("%H%M%S") for val in timelist]
                    print(times)
                except Exception as e:
                    print(params)
                    print(headers)
                    print(e)
                    break
                df['time']=times
#            #print(df)
            df['datetime'] = df[['date', 'time']].apply(lambda x: ''.join(str(value) for value in x), axis=1)
            df['type']=df['type'].replace('卖盘',-1)
            df['type']=df['type'].replace('中性盘',0)
            df['type']=df['type'].replace('买盘',1)
            data = pd.concat([data, df])
    filePath = os.path.join(path, '{}.csv'.format(x1))
    data.to_csv(filePath)

    # for x1 in range(2017, 2019):
    #     path = os.path.join(os.getcwd(), 'data')
    #     filePath = os.path.join(path, '{}.csv'.format(x1))
    #     print(filePath)
    params={'date': '2017-01-01', 'symbol': 'sz000868'}
    headers = {'X-Forwarded-For': '120.16.244.83'}
    url = 'https://market.finance.sina.com.cn/downxls.php'
    r = requests.get(url, params=params, headers=headers)