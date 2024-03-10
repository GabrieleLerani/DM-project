import os
from configparser import ConfigParser

def config(filename, section):
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))


    # Construct the absolute path to the configuration file
    file_path = os.path.join(current_dir, filename)


    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(file_path)


    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, file_path)
        )

    return db
