import json
import os
import TMQ.Tool.TMConfig as tmc


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


# tesk_dict结构
'''
{
    '000001.SZ':[['20190103','20190110'],['20190103','20190110'],['20190103','20190110']],
    '000002.SZ':[['20190103','20190110'],['20190103','20190110'],['20190103','20190110']]
}
'''
def saveTasksJsonFile(ts_code, tasks_arr):
    filepath = tmc.get_json_path()
    tasks_dic = {}
    if os.path.exists(filepath):
        tasks_dic = readJsonFile(filepath)
    tasks_dic[ts_code] = tasks_arr
    saveJsonFile(filepath, tasks_dic)


def readTaskJsonFile(ts_code):
    path = tmc.get_json_path()
    task_dic = readJsonFile(path)
    tasks = task_dic[ts_code]
    return tasks

def finishTaskTellJsonFile(ts_code, task):
    task_dic = readTaskJsonFile()
    tasks = task_dic[ts_code]
    tasks.remove(task)
    task_dic[ts_code] = tasks
    saveTasksJsonFile(ts_code, task_dic)


# def insertJonsToFile(filepath, dict):
# path = tmc.get_json_path()
# saveJsonFile(path, test_dict)
# dict = readJsonFile(path)
# dict = readJsonFile('x')