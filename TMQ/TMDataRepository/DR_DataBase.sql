CREATE DR_DataBase IF NOT EXISTS DR_DataBase;

--CREATE TABLE 'one_minute' (
--  'id' int NOT NULL AUTO_INCREMENT,
--  'ts_code' int NOT NULL,
--  'trade_time' datetime NOT NULL,
--  'open_price' decimal(19,4) NULL,
--  'high_price' decimal(19,4) NULL,
--  'low_price' decimal(19,4) NULL,
--  'close_price' decimal(19,4) NULL,
--  'volume' bigint NULL,
--  'amount' bigint NULL,
--  'trade_date' datetime NOT NULL,
--  'pre_close_price' decimal(19,4) NULL,
--  PRIMARY KEY ('id'),
--  KEY 'index_ts_code' ('ts_code')
--) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;