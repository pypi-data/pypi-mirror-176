import configparser
import os
BASEDIR=os.path.join(os.path.expanduser("~"), ".vecb")

def get_config_file():
    return os.path.join(BASEDIR, "config.ini")    

def write_default_config(fname):
    config = get_default_config()
    with open(fname, 'w') as f:
        config.write(f)    
    return config

def get_config():
    user_config = get_config_file()
    if not os.path.isfile(user_config):
        os.makedirs(BASEDIR, exist_ok=True)        
        config = write_default_config(user_config)
    else:
        config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        config.read(user_config)
    return config

def get_default_config():
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

    config.add_section('API')
    config['API']['endpoint'] = ""
    config['API']['token'] = ""
    return config
