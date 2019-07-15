# 第三章
# (1)urlopen
import urllib.request

response = urllib.request.urlopen('https://www.python.org')
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))

'''
data参数（可选参数）
需要使用bytes()方法将参数转化为字节流编码格式的内容，bytes类型。他的请求方式就不再是GET方法，而是POST方法
'''
import urllib.parse
import urllib.request

data = bytes(urllib.parse.urlencode({'word':'hello'}), encoding='utf-8')
'''这里我们传递了一个参数word,值是hello。他需要被转码成bytes(字节流)类型。
bytes方法第一个参数必须是str类型，urllib.parse.urlencode()方法将字典转化为字符串，第二个参数指定编码格式'''
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read())

'''timeout参数用于设置超时时间，单位为秒'''

import urllib.request

response = urllib.request.urlopen('http://httpbin.org/get',timeout=1)
print(response.read())


import socket
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('Time Out')

# 其他参数
'''
context参数（ssl.SSLContext）类型，用来指定SSL设置
cafile和capath这两个参数指定CA证书和它的路径

'''


# (2)Request
'''
如果请求中加入Header等信息
'''
import urllib.request

request = urllib.request.Request('http://www.baidu.com')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
'''
url, data=None, headers={},origin_req_host=None, unverifiable=False,method=None
url是必传参数
'''
from urllib import request, parse
url = 'http://httpbin.org/post'
headers={
    'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)',
    'Host':'httpbin.org'
}
dict = {
    'name':'Germey'
}
data = bytes(parse.urlencode(dict), encoding='utf-8')
req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))

# (3)高级用法
'''
面对cookie处理，代理设置，可以做到http请求中的所有事情
urllib.request模块里的BaseHandle类，它是所有其他Handle的父类，它提供了最基本的方法
HTTPDefaultErrorHandle:用于处理HTTP响应错误，错误都会抛出HTTPError类型错误
HTTPRedirectHandle:用于处理重定向
HTTPCookieProcessor:用于处理Cookies
ProxyHandle:用于设置代理，默认代理为空
HTTPPasswordMgr:用于管理密码，它维护了用户民和密码的表
HTTPBasicAuthHandle:用于管理认证，如果一个链接打开时需要认证，那么可以用它来解决认证问题。
以后在用
'''
'''
另外还有opener
'''
# 面对一个需要验证用户名和密码的页面
from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
from urllib.error import URLError

username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handle = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handle)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)

'''
这里首先实例化HTTPBasicAuthHandler对象，其参数是HTTPPasswordMgrWithDefaultRealm对象，
它利用add_password()添加进去用户名和密码，这样就建立了一个处理验证的Handle
接下来，利用这个Handle并使用build_opener()方法构建一个opener，这个opener在发送请求时就相当于已经验证成功了
'''

# 代理
'''在做爬虫的时候使用代理'''

from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy_handle = ProxyHandler({
    'http':'http://127.0.0.1:9743',
    'https':'https://127.0.0.1:9743'
})
opener = build_opener(proxy_handle)
try:
    response = opener.open('https://www.baidu.com')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
'''
可以添加多个代理
'''

# Cookies
'''Cookies的处理就需要相关的Handler'''
import http.cookiejar, urllib.request

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name + "=" + item.value)
'''
解释：首先，我们必须声明一个Cookiesjar对象。接下来，就需要利用HTTPCookieProcessor来构建一个Handler，
最后利用build_opener()函数构建一个opener,执行open函数
'''

# 不过既然能输出，也可以输出文件格式，Cookies本身也是以文本形式保存的

filename = 'cookies.txt'
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)
'''
解释：这时CookieJar就需要换成MozillaCookieJar，它在生成文件时会用到，
是CookieJar的子类，可以用来处理Cookies和文件相关的事件，比如读取和保存Cookies,
可以将Cookies保存成Mozilla型浏览器的Cookies格式。

运行之后，可以发现生成一个cookies.txt文件
'''


'''
另外，LWPCookieJar同样可以读取和保存Cookies,但是保存的格式和MozillaCookieJar不一样，
它会保存成libwww-perl(LWP)格式的Cookies文件。
'''
filename = 'cookies.txt'
cookie = http.cookiejar.LWPCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)

# cookie = http.cookiejar.LWPCookieJar(filename)
cookie = http.cookiejar.LWPCookieJar()
cookie.load(filename='cookies.txt', ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
print(response.read().decode('utf-8'))

'''
载入本地的Cookies文件，首先保存的格式与读取的格式必须一样。
'''

# 3.1.2处理异常
# (1)URLError来自urllib库中的error模块，它继承自OSError类，是error异常模块的基类，
# 由request模块产生的异常都可以通过捕获这个类来处理。
from urllib import request, error
try:
    response = request.urlopen('https://cuiqingcai.com/index.htm')
except:
    print(e.reason)

# (2)HTTPError
# code返回HTTP
'''
状态码：
404 网页不存在
500 服务器内部错误
'''
#reason 错误原因
#headers 返回请求头

from urllib import request, error
try:
    response = request.urlopen('https://cuiqingcai.coom/index.html')
except error.HTTPError as e:
    print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
    print(e.reason)
else:
    print('Request Successful')


'''
这样就可以做到先捕获HTTPError,获取它的错误码状态，原因，header等信息
'''
import socket
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('https://www.baidu.com', timeout=0.01)
except urllib.error.URLError as e:
    print(type(e.reason))
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')

# 3.1.3解析链接
'''
urllib提供了parse模块，它定义了处理URL的标准接口，列入实现了URL各部分的抽取，合并以及链接转换。
支持如下协议：
file,ftp,gopher,hdl,http,https,imap,mailto,mms,news,nntp,prospero,rsync,rtsp,rtspu,sftp,sip,sips
,snews,svn,svn+ssh,telnet和wais
'''
# (1)urlparse()
# 该方法可以实现URL的识别以及分段
from urllib.parse import urlparse

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(result), result)
# 这里我们利用urlparse()方法进行了一个URL解析。
#返回结果： <class 'urllib.parse.ParseResult'> ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5', fragment='comment')

# 可以看到返回的结果是一个parseResult类型对象，包含6个部分，scheme,netloc,path,params,query,fragment
# 参数1
# urlstring这是必填项，即待解析的URL
# 参数2
# scheme它是默认的协议（比如http和https等）。假如这个链接没有带协议信息，会将这个作为默认的协议
from urllib.parse import urlparse
result = urlparse('www.baidu.com/index.html;user?id=3#ccomment', scheme='https')
print(result)
# 参数3
'''
allow_fragments即是否忽略fragment。如果它被设置为False,fragment部分就会被忽略，
它会被解析为path,params或者query的一部分，而fragment部分为空。
'''
from urllib.parse import urlparse

result = urlparse('https://www.baidu.com/index.html;user?id=5#comment', allow_fragments=False)
print(result)
'''
可以发现，当URL中不包含params和query时，fragment便会被解析为path的一部分
返回结果ParseResult实际上是个元祖，我们可以用索引顺序来获取，也可以用属性名获取
'''

# (2)urlunparse()
'''
有了urlparse()，相应地就有了他的对立方法urlunparse()。它接受的参数是一个可迭代对象。，但是它的长度必须是6，
否则会抛出参数数量不足或者过多的问题。
'''
from urllib.parse import urlunparse
data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(urlunparse(data))

# (3)urlsplit()
'''
这个方法和urlparse()函数非常相似
#标识符代表网页中的一个位置
'''
from urllib.parse import urlsplit
result = urlsplit('http://wwww.baidu.com/index.html;user?id=5#comment')
print(result)
'''
返回的是一个SplitResult元祖类型，既可以用属性获取值，也可以用索引来获取
'''
from urllib.parse import urlsplit
result = urlsplit('http://www.baidu.com/index.html;usesr?id=5#comment')
print(result.scheme, result[0])


# (4)urlunsplit()
'''
与urlunparse()类似，它也将链接各个部分组合成完整链接的方法，传入参数也是一个可迭代对象，例如列表，元祖等，
唯一的区别是长度必须为5
'''
from urllib.parse import urlunsplit
data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
print(urlunsplit(data))

# (5)urljoin()
'''
有了urlunparse()和urlunsplit()方法，我们可以完成链接的合并，不过前提是必须要有特定长度的对象，
链接的每一部分都要清晰分开
'''
from urllib.parse import urljoin

print(urljoin('http://www.baidu.com','FAQ.html'))
print(urljoin('http://www.baidu.com','http://yejunhai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html','http://yejunhai.com/FAQ.html'))

# (6)urlencode()
'''
这里我们再介绍一个常用的方法----urlencode(),它构造GET请求参数的时候非常有用
'''
from urllib.parse import urlencode
params = {
    'name':'germey',
    'age':22
}
base_url = 'http://www.baidu.com'
url = base_url + urlencode(params)
print(url)

# (7)parse_qs()
'''
有了序列化，必然就有反序列化。如果我们有一串GET请求参数，利用parse_qs()方法，就可以将其转化为字典
'''
from urllib.parse import parse_qs

query = 'name=germey&age=22'
print(parse_qs(query))

# (8)parse_qsl()
'''
另外，还有一个parse_qsl()方法，它用于将参数转化为元祖组成的列表
'''
from urllib.parse import parse_qsl
query = 'name=germey&age=22'
print(parse_qsl(query))
'''
总结7，8：
8运行结果是一个列表，而列表中的每一个元素都是一个元祖，元祖的第一个内容是参数名，第二个内容是参数值
'''

# (9)quote()
'''
该方法可以将内容转化为URL编码格式，URL中带有中文参数时，有时可能会导致乱码问题，
此时用这个方法可以将中文字符转化为URL编码
'''
from urllib.parse import quote
keyword = '壁纸'
url = 'http://www.baidu.com/s?wd=' + quote(keyword)
print(url)

# (10)unquote()
'''
有了quote()方法，当然还有unquote()方法，它可以进行URL解码
'''
from urllib.parse import unquote
url = 'https://www.baidu.com/s?wd=%E5%A3%81%E7%BA%B8'
print(unquote(url))


# 3.1.4
# (1)分析Robot协议
'''
作用：利用urllib的robotparser模块，我们可以实现网站Robots协议的分析。
'''
'''
Robot协议是啥？
Robot协议也称作爬虫协议，机器人协议，他的协议全名叫做网络爬虫排除标准（Robots Exclusion Protocol）,
用来告诉爬虫和搜索引擎哪些页面可以抓取，哪些不可以抓。通过robots.txt文本文件。
当搜索爬虫访问一个站点时，它首先会检查这个站点根目录下是否存在robots.txt文件，如果存在，
搜索爬虫会根据其中定义的爬去范围来爬去。如果没有找到这个文件，搜索爬虫便会访问所有可直接访问的页面。
'''
'''
robot.txt实现对所有搜索爬虫只允许爬去public目录功能。
User-agent描述了搜索爬虫的名称，，*代表盖协议对任何任何爬取的爬虫有效

'''
#（2）爬虫名称
'''
常见爬虫名称
BaiduSpider
Googlebot
360Spider
YodaoBot
is_archiver
Scooter
'''
#(3)robotparser
'''
了解Robots协议之后，我们就可以使用robotparser模块来解析robots.txt了。该模块提供了一个类RobotFileParser
'''
urllib.robotparser.RobotFileParser(url='')
# set_url():用来设置robot.txt文件链接。如果创建RobotFileParser对象是传入了链接，那么就不需要使用这个方法设置了。
# read():读取robot.txt文件并进行分析。
# parse():用来解析robot.txt文件，传入的参数是robot.txt某些行的内容
# can_fetch():该方法传入两个参数，第一个是User-agent，第二个是抓取的URL.返回的内容是该搜索引擎是否可以抓取这个URL，，返回结果True和False
# mtime():返回的是上次抓取和分析robots.txt的时间，这对于长时间分析和抓取的搜索爬虫是很有必要的。
# modified():它同样对长时间分析和抓取的搜索爬虫很有帮助，将当前时间设置为上次抓取和分析robot.txt的时间。

from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url('http://www.jianshu.com/robots.txt')
rp.read()
print(rp.can_fetch('*', 'https://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*', 'http://www.jianshu.com/serach?q=python&page=1&type=collections'))

# ==
rp = RobotFileParser('http://www.jianshu.com/robots.txt')

from urllib.request import urlopen
rp = RobotFileParser()
rp.parse(urlopen('http://www.jianshu.com/robots.txt').read().decode('utf-8').split('\n'))
print(rp.can_fetch('*','http://www.jianshu.com/p/b67554025d7d'))
print(rp.can_fetch('*','http://www.jianshu.com/serach?q=python&page=1&type=collections'))


# 3.2使用requests
'''
urllib使用起来有点复杂，为了方便使用requests
'''
# 3.2.1
import requests

r = requests.get('http://www.baidu.com')
print(type(r))
print(r.status_code)
print(type(r.text))
print(r.cookies)

r = requests.post('http://httpbin.org/post')
r = requests.put('http://httpbin.org/put')
r = requests.delete('http://httpbin.org/delete')
r = requests.head('http://httpbin.org/head')
r = requests.options('http://httpbin.org/options')

# GET请求
import requests

r = requests.get('http://httpbin.org/get')
print(r.text)

r = requests.get('http://httpbin.org/get?name=germey&age=22')

'''
利用params，更加人性化
'''
data = {
    'name':'germy',
    'age':22
}
r = requests.get('http://httpbin.org/get', params=data)
print(r.text)
'''
返回的是字符串
'''
'''
json()方法，是JSON格式
'''
import requests

r = requests.get('http://httpbin.org/get')
print(type(r.text))
print(r.json())
print(type(r.json()))

'''
抓取网页
'''
import requests
import re

headers = {
    'User-Agent':'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get('http://www.zhihu.com/explore', headers = headers)
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
title = re.findall(pattern, r.text)
print(title)

'''抓取二进制数据'''
import requests
r = requests.get('https://github.com/favicon.ico')
print(r.text)
print(r.content)
with open('favicon.ico', 'wb') as f:
    f.write(r.content)
'''
这里用了open()方法，它的第一个参数是文件名称，第二个参数代表以二进制写的形式打开，可以向文件里写入二进制数据
'''

'''
添加headers
与urllib.request一样
'''
import requests
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
}
r = requests.get('https://www.zhihu.com/explore', headers = headers)
print(r.text)


'''
POST请求
'''
import requests

data = {'name':'germey','age':'22'}
r = requests.post('http://httpbin.org/post', data=data)
print(r.text)


'''
响应
发送请求后，得到的自然就响应。在上面的实例中，我们使用text和content获取了响应的内容，
还有很多其他的属性和方法来获取其他信息，比如状态码，响应头，cookies等
'''

import requests
r = requests.get('http://www.jianshu.com')
print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)

r = requests.get('http://www.jianshu.com')
exit() if not r.status_code == requests.codes.ok else print('Request Successfully')


'''
3.2.2高级用法
'''
# (1)文件上传
import requests
files = {'file':open('favicon.ico', 'rb')}
r = requests.post('http://httpbin.org/post', files = files)
print(r.text)
# (2)Cookies
import requests
r = requests.get('http://www.baidu.com')
print(r.cookies)
for key, value in r.cookies.items():
    print(key+'='+value)

'''
利用Cookies来维持登录状态
'''
import requests

headers = {
    'Cookie':'_zap=13280478-15db-48ab-a6df-1e43e6a32c46; d_c0="AFAjl9trHA-PTln73NR7-FN7OquxByF2c-w=|1552385360"; q_c1=4e92e027c30a40ff94367488088c9dbd|1562318813000|1552385361000; r_cap_id="NWNhNTgyYmViMjE4NDM1YmE2ZTlkZGExMjhlMDE0OTc=|1562318813|fa8587fcdfc66a78d593f633de481662e94eabf3"; cap_id="OTgwN2U4ODQ3ZmYyNDg4ODljZTFiNzAwMTZjYmI4OWI=|1562318813|a1b1c7959dc5c1aa5b302022db33bb1db5e075ce"; l_cap_id="MGFiZjUzZDkyZWI3NGMyM2I1NGFkNmJjN2UzM2NkZDM=|1562318813|657bf64f4e66eeea8d6bb7e569d44665cceed4b4"; __utma=51854390.1777506407.1562318817.1562318817.1562318817.1; __utmz=51854390.1562318817.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20190312=1; tgw_l7_route=116a747939468d99065d12a386ab1c5f; _xsrf=I6DCEkb1E3kwMITwkb5X571tMJPkfUPY; capsion_ticket="2|1:0|10:1562555527|14:capsion_ticket|44:YjI4YzdlYzA0ZTY5NDA1OWEwZTQ5ZTYyNTBmMjVhZTY=|45010a3fd03015438045c47ca5e4ede8a19f470afd4a90901a9db2263ccab5f3"; z_c0="2|1:0|10:1562555591|4:z_c0|92:Mi4xWjcwZUFnQUFBQUFBVUNPWDIyc2NEeWNBQUFDRUFsVk54MEZLWFFDejlYcFo5TmN0ZHRHRmdTZzJNenNrMWd5ZWV3|0965229dad19c5ff8069fbf0042103f9baff20a171660ff1fbfb9de074aca88b"; tst=r; unlock_ticket="ABAMh_V_vQgnAAAAhAJVTdK7Il03kUxMxObUkahwa8llHY5h8ecOZw==',
    'Host':'www.zhihu.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
}
r = requests.get('http://www.zhihu.com', headers = headers)
print(r.text)


# (3)会话支持
'''
在requests中，如果直接使用get()或者post()请求，实际上相当于不同会话，也就是两个不同浏览器打开不同页面
如何维持会话呢？
由此出现新对象Session
'''
# 以下错误
import requests
requests.get('http://httpbin.org/cookies/set/number/123456789')
r = requests.get('http://httpbin.org/cookies')
print(r.text)
# 以下正确
import requests

s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/123456')
r = s.get('http://httpbin.org/cookies')
print(r.text)


#(4)SSL证书验证
import requests
'''
requests还提供了证书验证的功能。发送HTTP请求的时候，它会检查SSL证书，我们可以使用Verify参数控制是否检查此证书。
如果不加Verify参数的话，默认是True,会自动验证。
'''
response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)
'''
不验证的话虽然能请求成功但是会有警告
'''
import requests
from requests.packages import urllib3

urllib3.disable_warnings()
response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)
'''或者通过捕获警告到日志的方式忽略警告'''

import logging
import requests
logging.captureWarning(True)
response = requests.get('https://www.12306.cn', verify=False)
print(response.status_code)

'''当然我们也可以指定本地证书用作客户端证书，这可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元祖'''
import requests
response = requests.get('https://www.12306.cn', cert=('/path/server.crt','/path/key'))
print(response.status_code)
'''
本地私有证书的key必须是解密状态
'''

#(5)代理设置
'''
防止封IP
'''
import requests
proxies = {
    'http':'http://10.10.1.10:3128',
    'https':'http://10.10.1.10:1080'
}
requests.get("https://www.taobao.com",proxies= proxies)

#(6)超时设置
'''
在本机网络状态不好或者服务器网络响应太慢甚至无响应时，我们可能会等待特别久的时间才能接受到响应，甚至到最后收不到响应而报错。为了防止服务器不能及时响应，应该设置一个超时时间，即超过了这个时间还没有得到响应，那就报错。
这需要用到timeout参数。这个时间的计算是发出请求带服务器返回响应的时间。
'''
import requests
r = requests.get('https://www.taobao.com', timeout=2)
print(r.status_code)
'''
通过这样的方式，我们可以将超时时间设置为2秒
上面设置的timeout将用作连接和读取二者的timeout的总和
'''
# 如果分别指定
r = requests.get('https://www.taobao.com', timeout(5,30))
'''
如果想永久等待，可以直接将timeout设置为None，或者不设置直接留空，因为内容为None，这样永远不会返回超时错误。
'''

#（7)身份验证
import requests
from requests.auth import HTTPBasicAuth

r = requests.get('http://localhost:5000',auth=HTTPBasicAuth('username','password'))
print(r.status_code)
# 可以简写如下
r = requests.get('http://localhost:5000',auth=('username','password'))

'''
使用OAuth1验证的方法如下
'''
import requests
from requests_oauthlib import OAuth1

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
requests.get(url, auth=auth)

# (8)Prepared Request
'''前面介绍urllib时，我们可以将请求表示为数据结构，其中各个参数都可以通过一个Request对象来表示。'''
from requests import Request, Session

url = 'http://httpbin.org/post'
data = {
    'name':'germey'
}
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
}
s = Session()
req = Request('POST', url, data = data, headers = headers)
prepped = s.prepare_request(req)
r = s.send(prepped)
print(r.text)
'''
我们引用了Request，然后用url，data，和headers参数构造一个Request对象，这时需要在调用Session的prepare_request()
方法将其转换为一个prepare_request()方法将其转换为一个Prepared Request对象，然后调用send()方法发送即可
'''
'''
有了Request对象，就可以将请求当作独立的对象来看待，这样在进行队列调度时会非常方便。
'''


'''
3.3正则表达式
'''
# http://tool.oschina.net/regex/
# (2)match()
'''
这里首先介绍第一个常用的匹配方法--match()，向它传入要匹配的字符串以及正则表达式，就可以检测这个正则表达式是否匹配字符串
match()方法会尝试从字符串的起始位置匹配正则表达式，如果匹配，就返回匹配成功的结果；如果不匹配就返回None。
'''
import re

content = 'Hello 123 4567 World_This is a Regex Demo'
print(len(content))
result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}', content)
print(result)
print(result.group())
print(result.span())


'''
匹配目标
'''

import re

content = 'Hello 1234567 World_This is a Regex Demo'

result = re.match('^Hello\s(\d+)\sWorld',content)
print(result)
print(result.group())
print(result.group(1))
print(result.span())

'''
通用匹配*
'''
import re
content = 'Hello 123 4567 World_This is a Regex Demo'
result = re.match('^Hello.*Demo$', content)
print(result)
print(result.group())
print(result.span())

'''
贪婪与非贪婪
使用上面的通用匹配.*时，可能有时候匹配到的并不是我们想要的结果。
'''
import re
# 贪婪匹配
'''
贪婪匹配.*匹配了（ 123456）
(\d)匹配了 （7）
'''
content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match('^He.*(\d+).*Demo$', content)
print(result)
print(result.group(1))

# 非贪婪匹配
'''
贪婪匹配.*匹配了（ ）
(\d)匹配了 （1234567）
'''
content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match('^He.*?(\d+).*Demo$', content)
print(result)
print(result.group(1))


'''
修饰符
正则表达式可以包含一些可选标注修饰符控制匹配的模式。修饰符被指定为一个可选的标志。我们用实例来看一下
'''
import re
content = '''Hello 1234567World_This
 is a Regex Demo'''
result = re.match('He.*?(\d+).*?Demo$', content, re.S)
print(result.group(1))

'''这里需要一个re.S，即可修正（.匹配除换行符以外的任意字符串，如果遇到换行符就匹配不到了）'''


'''
转移匹配
.匹配除换行符以外的所有字符串，如果包含.字符怎么办
'''
import re
content = '（百度）www.baidu.com'
result = re.match('\（百度\）www\.baidu\.com',content)
print(result.group())

'''
search()
match()是从开头开始匹配的
'''
import re
content = 'Extra stings Hello 1234567 World_This is a Regex Demo Extra stings'
result = re.match('Hello.*?(\d+).*?Demo', content)
print(result)
'''
匹配失败
所以存在另一个方法search()

'''
result = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S)
if result:
    print(result.group(1),result.group(2))


# (4)findall()
# 寻找所有
results = re.findall('<li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S)
for result in results:
    print(result)
    print(type(result))

# (5)sub()方法进行替换
import re
content = '54aK54yr5oiR54ix5L2g'
content = re.sub('\d+', '', content)
print(content)

# 替换html
html = re.sub('<a.*?>|</a>', '', html)
print(html)
results = re.findall('<li.*?>(.*?)</li>', html, re.S)
for result in results:
    print(result.strip())

# (6)compile()
'''
这个方法可以将正则字符串编译成正则表达式对象，
'''
import re
content1 = '2016-12-15 12:00'
content2 = '2016-12-15 12:00'
content3 = '2016-12-15 12:00'
pattern = re.compile('\d{2}:\d{2}')
result1 = re.sub(pattern, '', content1)
result2 = re.sub(pattern, '', content2)
result3 = re.sub(pattern, '', content3)
print(result1, result2, result3)



'''
实例1 猫眼电影
'''
maoyan = 'http://maoyan.com/board/4'

import requests
from requests.exceptions import RequestException
import time
import re

def get_one_page(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
        }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None




def parse_one_page(html):
    pattern = re.compile(
        # '<dd>.*?board-index.*?>(\d+)</i>.*?title={.*?}class.*?img alt.*?src="{.*?}".*?"star">{.*?}</p>.*?releasetime">{.*?}</p>.*?integer">{.*?}</i>.*?fraction">{.*?}</i>.*?</dd>',
        # '<dd>.*?board-index.*?>(\d+)</i>.*?<a.*?title="(.*?)".*?<img\salt.*?src="(.*?)">.*?</a>.*?</dd>',
        '<dd>.*?board-index.*?>(\d+)</i>.*?<a.*?title="(.*?)".*?\ssrc="(.*?)"\salt.*?<img\sdata-src="(.*?)"\salt.*?class="star">(.*?)</p>.*?</dd>',
        # '<dd>.*?board-index.*?>(\d+)</i>.*?<a.*?title="(.*?)".*?\ssrc="(.*?)"\salt.*?<img\sdata-src="(.*?)"\salt.*?class ="star"\s>(.*?)</p>.*?class="releasetime">(.*?)</p>.*?"integer">(.*?)</i>.*?class="fraction">(.*?)</i>.*?</dd>',
        re.S
    )
    items = re.findall(pattern, html)
    for i in items:
        yield{
            'index':i[0],
            'name':i[1],
            'image':i[3],
            'star':i[4]
        }


# parse_one_page(html)


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dump)

for i in range(10):
    main(i*10)
    time.sleep(1)


# 第四章
# 解析库 XPath
from lxml import etree
text = '''
<div>
    <html></html>
</div>
'''
html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))

# 读取文本
html = etree.parse('./test.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))

# 5所有节点
'''
我们一般会用//开头的XPath规则来选取所有符合要求节点。
如果要选取所有节点
'''
from lxml import etree
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//*')
print(result)



'''
所有节点
'''
url = 'http://maoyan.com/board/4'
html = get_one_page(url)
html = etree.HTML(html)
r = html.xpath('//*')
print(r)
# (*代表匹配所有节点，也就是整个html文本中的所有节点都会被获取。)
r2 = html.xpath('//li')

'''
子节点
'''
# 获取所有li节点获取直接的子节点a
r3 = html.xpath('//li/a')
# 获取所有li节点获取子孙节点
r4 = html.xpath('//li//a')

'''
父节点
..
'''
r5 = html.xpath('//a[@href="/films/837"]/../@class')
# 也可以使用parent::获取父节点
r5 = html.xpath('//a[@href="/films/837"]/parent::*/@class')

'''
属性匹配
'''
r6 = html.xpath('//p[@class="name"]')
'''
文本获取
'''
r7 = html.xpath('//p[@class="name"]//text()')
'''
属性获取
'''
r8 = html.xpath('//p/a/@href')
'''
属性多值匹配
有时候，某些节点的某个属性可能有多个值
'''
from lxml import etree
text = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
r9 = html.xpath('//li[contains(@class, "li")]/a/text()')
print(r9)

'''
多属性匹配
'''
from lxml import etree
text = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
r10 = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
print(r10)

'''
按顺序选择
'''
from lxml import etree
text = '''
<div>
<ul>
<li class="item-0"><a href="link1.html">first item</a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''
html = etree.HTML(text)
r11 = html.xpath('//li[1]/a/text()')
r12 = html.xpath('//li[last()]/a/text()')
r13 = html.xpath('//li[position()<3]/a/text()')
r14 = html.xpath('//li[last()-2]/a/text()')

'''
节点选择器
'''
text = '''
<div>
<ul>
<li class="item-0"><span><a href="link1.html">first item</a></span></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''
html = etree.HTML(text)
# 获取祖先节点
r15 = html.xpath('//li[1]/ancestor::*')
# 找到只有div的祖先节点
r16 = html.xpath('//li[1]/ancestor::div')
# 获取所有属性值
r17 = html.xpath('//li[1]/attribute::*')
# 获取所有直接子节点，并且href属性==link1.html
r18 = html.xpath('//li[1]/child::a[@href="link1.html"]')
# 获取所有子孙节点，并且是span
r19 = html.xpath('//li[1]/descendant::span')
# 可以获取当前节点之后第二个节点后所有节点
r20 = html.xpath('//li[1]/following::*[2]')
# 获取当前节点同级别节点
r21 = html.xpath('//li[1]/following-sibling::*')


# 解析库 Beautiful Soup
from bs4 import BeautifulSoup
soup = BeautifulSoup('<p>Hello</p>', 'lxml')
print(soup.p.string)

# 基本用法
html= '''
<div>
<ul>
<li class="item-0"><span><a href="link1.html">first item</a></span></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
print(soup.li.string)
'''
选择元素
'''
print(soup.ul)
print(type(soup.ul))
print(soup.ul.string)
print(soup.div)


'''
提取信息
'''
# 节点名
print(soup.li.name)
# 属性
print(soup.li.attrs)
print(soup.li.attrs['class'])
# 获取内容
print(soup.li.string)

'''
嵌套选择
'''
print(soup.ul.li.string)
'''
关联选择
'''
# 子节点与子孙节点
html = '''
<html>
<p class = "story">
hahhahah
<a href="http://www">
<span>Elsa</span>
</a>
<a href="haha">Tom</a>
and
<a href="haha">Tom</a>
adfadsfasdf
</p>
</html>
'''
'''
直接子节点
'''
soup = BeautifulSoup(html, 'lxml')
print(soup.p.contents)
# =
print(soup.p.children)
for i, child in enumerate(soup.p.children):
    print(i, child)

'''
如果要得到所有子孙节点
'''
print(soup.p.descendants)
for i, child in enumerate(soup.p.descendants):
    print(i, child)


'''
父节点和祖先节点
'''
html = '''
<html>
<p class = "story">
hahhahah
<a href="http://www">
<span>Elsa</span>
</a>
<a href="haha">Tom</a>
and

adfadsfasdf
</p>
<a href="haha">Tom</a>
</html>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.a.parent)
'''这里选择第一个a节点的父节点元素'''
'''现在开始找祖先节点'''
print(type(soup.a.parents))
print(list(enumerate(soup.a.parents)))

'''
兄弟节点
'''
html = '''
<html>
<body>
<p>dasdas
<a href="sdasdas"><span>asdasd</span></a>
<a href="sdasdas"><span>asdasd</span></a>
<a href="sdasdas"><span>asdasd</span></a>
</p>
</body>
</html>
'''

print('Next Sibing',soup.a.next_sibling)
print('Prev Sibing',soup.a.previous_sibling)
print('Next Sibling', list(enumerate(soup.a.next_siblings)))
print('Prev_Sibling', list(enumerate(soup.a.previous_siblings)))

'''
提取信息
如果想要获取他们的信息，比如文本，属性等
'''
print('Next Sibing:')
print(type(soup.a.next_sibling))
print(soup.a.next_sibling)
print(soup.a.next_sibling.string)

print('Parent:')
print(type(soup.a.parents))
print(list(soup.a.parents)[0])
print(list(soup.a.parents)[0].attrs['class'])

'''方法选择器'''
# find_all(name, attr, recursive, text, **kwargs)
html = '''
<html>
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4>
</div>
<div class="panel-body">
<ul class="list" id="list-1", name="elements">
<li class="element">Foo</li>
<li class="element">Bar</li>
<li class="element">Jar</li>
</ul>
<ul class="list list-small" id="list-2">
<li class="element">Foo</li>
<li class="element">Bar</li>
</ul>
</div>
</div>
</html>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
'''find_all'''
# name
print(soup.find_all(name="ul"))
print(type(soup.find_all(name="ul")[0]))

ul = soup.find_all(name="ul")
for u in ul:
    print(u.find_all(name="li"))

for u in ul:
    for l in u.find_all(name="li"):
        print(l.string)

# attrs
print(soup.find_all(attrs={'id':'list-1'}))
print(soup.find_all(attrs={'name':'elements'}))
print(soup.find_all(id='list-1'))
print(soup.find_all(class_='element'))
# text
'''text参数可用来匹配节点的文本，传入的形式可以是字符串，可以是正则表达式对象'''
import re
html = '''
<div class="panel">
<div class="panel-body">
<a>Hello, this is a link</a>
<a>Hello, this is a link, too</a>
</div>
</div>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all(text=re.compile('link')))

'''find'''
# 返回单个元素，也就是后者返回的是个元素，也就是第一个匹配的元素，而前者返回的是所有匹配的元素的列表
html = '''
<html>
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4>
</div>
<div class="panel-body">
<ul class="list" id="list-1", name="elements">
<li class="element">Foo</li>
<li class="element">Bar</li>
<li class="element">Jar</li>
</ul>
<ul class="list list-small" id="list-2">
<li class="element">Foo</li>
<li class="element">Bar</li>
</ul>
</div>
</div>
</html>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "lxml")
print(soup.find(name='ul'))
print(type(soup.find(name='ul')))
print(soup.find(class_='list'))
'''
find_parents()和find_parent():返回祖先节点和直接父节点
find_next_siblings()和find_next_sibling():返回后面所有的兄弟节点，返回后面第一个用地节点
find_previous_siblings()和find_previous_sibling():返回前面所有兄弟节点，返回前面第一个兄弟节点
find_all_next()和find_next():返回节点后所有符合条件的节点，返回第一个符合条件的节点
fing_all_previous()和find_previous():返回节点前所有符合条件的节点，返回第一个符合条件的节点
'''

'''css选择器'''
print(soup.select('.panel .panel-heading'))
print(soup.select('ul li'))
print(soup.select('#list-2 .element'))
print(soup.select('ul')[0])

'''嵌套选择'''
# select方法同样支持嵌套选择
for ul in soup.select('ul'):
    print(ul.select('li'))

# 获取属性
for ul in soup.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])

# 获取文本
for li in soup.select('li'):
    print('Get Text:', li.get_text())
    print('string:', li.string)



'''使用pyquery'''
from pyquery import PyQuery as pq
doc = pq(html)
print(doc('li'))

'''URL初始化'''
doc = pq(url='https://cuiqingcai.com')
print(doc('title'))

import requests
doc = pq(requests.get('https://cuiqingcai.com').text)
print(doc('li'))

doc = pq(filename='demo.html')
print(doc('li'))

'''
基本css选择器
'''
html = '''
<div id="container">
<ul class="list">
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span>third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''
doc = pq(html)
print(doc('#container .list li'))
print(type(doc('#container .lis li')))

'''
查找节点
'''
# 子节点，需要用到find()方法，此时传入的参数CSS的选择器
doc = pq(html)
items = doc('.list')
print(type(items))
lis = items.find('li')
print(type(lis))
print(lis)
'''find方法的查找范围是节点的所有子节点，而如果我们只想查找子孙节点，那么可以用到children方法'''
lis = items.children()
print(type(lis))
print(lis)
'''如果要筛选所有子节点中符合条件的节点'''
lis = items.children('.active')
print(lis)

'''父节点'''
# 我们可以用parent()方法来获取某个节点父节点
items = doc('.list')
container = items.parent()
print(type(container))
print(container)

