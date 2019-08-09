import pymysql


connection = pymysql.connect(host='localhost',
port=3306,
user='root',
password='68466296aB',
# db='demo',
charset='utf8')


cursor = connection.cursor()
# 创建数据库
effect_row = cursor.execute(
    '''CREATE DATABASE MysqlTestDB'''
)
connection.commit()

# 创建数据表
effect_row = cursor.execute(
    '''CREATE TABLE 'users' (
        'name' varchar(32) NOT NULL,
        'age' int(10) unsigned NOT NULL DEFAULT '0',
        PRIMARY KEY (‘name')
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8'''
)

# 插入数据(元组或列表)
effect_row = cursor.execute('INSERT INTO `users` (`name`, `age`) VALUES (%s, %s)', ('mary', 18))

# 插入数据(字典)
info = {'name': 'fake', 'age': 15}
effect_row = cursor.execute('INSERT INTO `users` (`name`, `age`) VALUES (%(name)s, %(age)s)', info)

connection.commit()

''' 批量插入'''
# 获取游标
cursor = connection.cursor()

effect_row = cursor.executemany(
    'INSERT INTO `users` (`name`, `age`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE age=VALUES(age)', [
        ('hello', 13),
        ('fake', 28),
    ])

connection.commit()


'''获取自增ID'''
cursor.lastrowid

'''查询数据'''
# 执行查询 SQL
cursor.execute('SELECT * FROM `users`')
# 获取单条数据
cursor.fetchone()
# 获取前N条数据
cursor.fetchmany(3)
# 获取所有数据
cursor.fetchall()

'''游标控制'''
# 所有的数据查询操作均基于游标，我们可以通过cursor.scroll(num, mode)控制游标的位置。
cursor.scroll(1, mode='relative') # 相对当前位置移动
cursor.scroll(2, mode='absolute') # 相对绝对位置移动

'''指定游标类型'''
# Cursor: 默认，元组类型
# DictCursor: 字典类型
# DictCursorMixin: 支持自定义的游标类型，需先自定义才可使用
# SSCursor: 无缓冲元组类型
# SSDictCursor: 无缓冲字典类型

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='demo',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

'''事务处理'''
# 开启事务 connection.begin()
# 提交修改 connection.commit()
# 回滚事务 connection.rollback()