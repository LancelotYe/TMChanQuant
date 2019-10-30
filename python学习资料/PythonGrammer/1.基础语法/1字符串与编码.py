# 对于单个字符的编码，Python提供了ord()函数获取字符的整数表示，chr()函数把编码转换为对应的字符：
ord('A')
ord('中')
chr(66)
chr(25991)
# 编码
'ABC'.encode('ascii')
'中文'.encode('utf-8')
# '中文'.encode('ascii')
# 解码
b'ABC'.decode('ascii')
b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
# 如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节：
b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')

'Age: %s. Gender: %s' % (25, True)
'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)

# 转十
int('1101',2)
int('0o226',8)
int('0x96',16)

# 转二
bin(13)
bin(0o37)
bin(0x37)

# 转八
oct(10)
oct(0b100101)
oct(0x37)

# 转十六
hex(10)
hex(0b100101)
hex(0o37)

