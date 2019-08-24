import configparser as cp
import os



def get_project_dir():
    # return os.getcwd()
    return os.path.join(os.getcwd(),'TMQ','TMDataRepository')



def get_config_path():
    return os.path.join(get_project_dir(), 'conf.ini')

def get_mysql_config_dict():
    mysql_cfg = get_config_path()
    print(mysql_cfg)
    conf = cp.ConfigParser()
    conf.read(mysql_cfg)
    # mysql = conf.mysql()
    # print(mysql)
    d = {}
    for section in conf.keys():
        # print("[{s}]".format(s=section))
        for key in conf[section]:
            # print("{k} = {v}".format(k=key, v=conf[section][key]))
            d[key] = conf[section][key]
    return d


def get_json_path():
    return os.path.join(get_project_dir(), 'record.json')