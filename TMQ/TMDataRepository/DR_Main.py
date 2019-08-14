import TMQ.TMDataRepository.DR_SymbolTickPip as symbolPip

symbolPip.connect_MySQL()
symbolPip.insertData(ts_code='000001.SZ', start_date='20120301', end_date='20120304')

# symbolPip.get_tick_from_pip（ts_code='000001.SZ', start_date='20120301', end_date='20120304'）
