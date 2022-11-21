from configparser import ConfigParser
import os

from datetime import date
import logging

today = date.today()
d2 = today.strftime("%B %d %Y")
log_file_name = 'Log '+str(d2)+'.txt'

logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format="%(asctime)s %(message)s", filemode="a")

db_config_file_dir = os.path.dirname(os.path.abspath(__file__))
db_config_file_path = db_config_file_dir + '\\db.ini'

print(db_config_file_path)
def config(filename=db_config_file_path, section='postgresql'):
    # create parser
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    # get section, defatult to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        print(f"db.ini file does not contain {section} section") 

    return db 