# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 07:51:48 2019

@author: 26063
"""

import requests
from lxml import etree
#伪装Chrome浏览器

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',}
Url='https://www.hao24.com/channel/live_list.html'
request=requests.get(Url, headers=headers)
request.encoding='utf-8'
html=request.text
html_1=etree.HTML(html)
# result = html_1.xpath('//*[@id="today_quan"]/ul[2]/li[2]/p[1]/a//text()')
# print(result)

result=html_1.xpath('//li//p[@class="one"]//text()')
result_1=html_1.xpath('//li//p[@class="two"]//text()')
result_2=html_1.xpath('//li//p[@class="title"]//a//text()')
result_3=html_1.xpath('//li//p[@class="price"]//text()')
for x in result:
    print(x)


result = [x for x in result if '-' in x]
for i in range(len(result)):
    print(result[i] + '|' + result_1[i] + '|' + result_2[i] + '|' + result_3[i])



