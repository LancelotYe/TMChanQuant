import TMQ.TMDataRepository.DR_SymbolTickPip as symbolPip
# from TMQ.TMDataRepository.DR_MysqlTool import dr_mysql_tool
# import TMQ.TMDataRepository.DR_Config as drc
# import TMQ.TMDataRepository.DR_TushareTool as tst



# symbolPip.connect_MySQL()
# symbolPip.insertData(ts_code='000001.SZ', start_date='20120301', end_date='20120304')

# symbolPip.get_tick_from_pip（ts_code='000001.SZ', start_date='20120301', end_date='20120304'）






# import os
#
# path = os.path.join(os.getcwd(), "Data", "test.csv")
# df.to_csv(path)

def main_go():
    ts_code = '000001.SZ'
    start_date = '20120103'
    end_date = '20120530'
    # df = tst.ts_get_oms_price(ts_code, start_date, end_date)
    #
    # conf_dict = drc.get_mysql_config_dict()
    #
    # # conf_dict = {'host': 'localhost',
    # #  'port': '3306',
    # #  'user': 'root',
    # #  'password': '68466296aB',
    # #  'db': 'DR_DataBase'}
    # mysqltool = dr_mysql_tool(conf_dict)
    # mysqltool.create_oms_table(ts_code)

    # mysqltool.insert_oms_data(ts_code, df)

    # #
    # start = start_date[0:4] + '-' + start_date[4:6] + '-' + start_date[6:8]
    # end = end_date[0:4] + '-' + end_date[4:6] + '-' + end_date[6:8]
    # dfd = mysqltool.get_oms_data_from_db(ts_code, start, end, True)
    #
    #
    # trdf = mysqltool.get_oms_exist_trade_date_index(ts_code, start, end)
    # trade_date_df = tst.ts_get_trade_date(start_date, end_date)


    # result = trdf

    # result_df = mysqltool.get_oms_data_from_db(ts_code, start, end, True)


    dr_pip = symbolPip.dr_oms_pip()

    df = dr_pip.pip_start(ts_code, start_date,end_date)
    return df
    print(df)


if __name__ == "__main__":
    dfx = main_go()