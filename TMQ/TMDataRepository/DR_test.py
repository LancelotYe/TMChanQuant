from TMQ.TMDataRepository.DR_MysqlTool import CheckTradeDateMysqlTool
import TMQ.TMDataRepository.DR_TushareTool as tst


start = '20181220'
end = '20181221'
ts_code = '000001.SZ'


tdf = tst.ts_get_trade_date(start,end)
pdf = tst.ts_get_oms_price(ts_code, start, end)

pdf.fillna(None)





# pdf.iloc[239]

tdf['ts_code'] = ts_code
tdf['has_data'] = 0

checkTradeDate = CheckTradeDateMysqlTool()

checkTradeDate.insert_data(tdf)

checkTradeDate.disconnect_db()


# ['ts_code', 'exchange', 'cal_date', 'is_open', 'has_data']
tdf = tst.ts_get_trade_date(start,end)
tdf['ts_code'] = ts_code
tdf['has_data'] = 0

df = checkTradeDate.get_data_from_db(ts_code, start, end)

checkTradeDate.disconnect_db()