import configparser

def getDatabaseConfig(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    
    db_username = config['MySQLConfig']['username']
    db_password = config['MySQLConfig']['password']
    db_host = config['MySQLConfig']['host']
    db_port = config['MySQLConfig']['port']
    db_database = config['MySQLConfig']['database']
    
    return db_username, db_password, db_host, db_port, db_database