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

# (3)urlaplit()

