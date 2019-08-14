show databases;
drop database DR_DataBase;
use DR_DataBase;

show tables;
select * from TT;

select * from TT order by trade_time desc;
select * from TT order by trade_time asc;

-- insert into TT values (1,'readonly','yang') ON DUPLICATE KEY UPDATE status ='drain';
insert ignore into TT values('000001.SZ', '2013-01-04 15:00:00', 16.0, 16.0, 15.99, 15.99, 440538.0, 7044203.0, '20130104', 16.0);




