

CREATE DATABASE IF NOT EXISTS DR_DataBase;
-- 使用数据库
USE DR_DataBase;
-- 创建表格
CREATE TABLE test_table (
  -- id int NOT NULL AUTO_INCREMENT,
  ts_code varchar(255) NOT NULL,
  trade_time datetime NOT NULL,
  open_price decimal(19,4) NULL,
  high_price decimal(19,4) NULL,
  low_price decimal(19,4) NULL,
  close_price decimal(19,4) NULL,
  volume bigint NULL,
  amount bigint NULL,
  trade_date datetime NOT NULL,
  pre_close_price decimal(19,4) NULL,
  PRIMARY KEY (trade_time),
  KEY index_ts_code (ts_code)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--INSERT INTO test_table VALUES(5, '2016-10-10 14:59:00', 9.12 ,9.12, 9.12, 9.12, 0, 0, '20161010', 9.12);
--INSERT INTO ttaaa (ts_code, trade_time) values(2,'2016-10-10 14:59:00'),(3,'2017-10-10 14:59:00'),(3,'2017-10-10 14:59:00'),(3,'2017-10-10 14:59:00'),(3,'2017-10-10 14:59:00');

