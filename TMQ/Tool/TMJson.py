import json
import os
import TMQ.Tool.TMConfig as tmc

# 字典转json
test_dict = {'bigberg': [7600, {1: [['iPhone', 6300], ['Bike', 800], ['shirt', 300]]}]}
print(test_dict)
print(type(test_dict))
 #dumps 将数据转换成字符串
json_str = json.dumps(test_dict)
print(json_str)
print(type(json_str))

# json转字典
new_dict = json.loads(json_str)
print(new_dict)
print(type(new_dict))



def saveJsonFile(filepath, dict):
    try:
        with open(filepath, "w+") as f:
            json.dump(dict, f)
        f.close()
    except OSError as e:
        print('出错啦：' + str(e))


def readJsonFile(filepath):
    load_dict = None
    try:
        with open(filepath, 'r') as f:
            load_dict = json.load(f)
        f.close()
    except OSError as e:
        print('出错啦：' + str(e))
    return load_dict

def saveJsonInToRecord(dict):
    path = tmc.get_json_path()
    saveJsonFile(path, dict)

def readJsonFromRedord():
    path = tmc.get_json_path()
    dict = readJsonFile(path)
    return

# def insertJonsToFile(filepath, dict):


# path = tmc.get_json_path()
# saveJsonFile(path, test_dict)
# dict = readJsonFile(path)
#
# dict = readJsonFile('x')