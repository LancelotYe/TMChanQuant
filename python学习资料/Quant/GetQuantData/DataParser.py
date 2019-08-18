

# 安装rqData
# pip install --extra-index-url https://rquser:ricequant99@py.ricequant.com/simple/rqdatac


import rqdatac as rq

rq.init()

rq.get_price('000001.XSHE','2018-3-23','2018-3-23','tick')