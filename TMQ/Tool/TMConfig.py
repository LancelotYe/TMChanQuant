import configparser as cp
import os



def get_project_dir():
    # return os.getcwd()
    return os.path.join(os.getcwd(),'TMQ','TMDataRepository')



def get_config_path():
    return os.path.join(get_project_dir(), 'conf.ini')

def get_mysql_config_dict():
    return get_config('mysql')

def get_ts_tokens():
    token_dic = get_config('ts_token')
    tokens = []
    for key in token_dic:
        tokens.append(token_dic[key])
    return tokens

def get_config(conf_key):
    mysql_cfg = get_config_path()
    # print(mysql_cfg)
    conf = cp.ConfigParser()
    conf.read(mysql_cfg)
    # mysql = conf.mysql()
    # print(mysql)
    d = {}
    s = conf[conf_key]
    for key in s:
        # print("{k} = {v}".format(k=key, v=s[key]))
        d[key] = s[key]
    return d


def get_json_path():
    return os.path.join(get_project_dir(), 'tasks.json')


debug = True
def tm_print(str):
    global  debug
    # nonlocal debug
    if debug:
        print(str)


# tokens = get_ts_tokens()
