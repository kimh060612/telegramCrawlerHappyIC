import configparser
from mysql.channelRepository import ChannelRepository

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('./config.ini')

    db_username = config['MySQLConfig']['username']
    db_password = config['MySQLConfig']['password']
    db_host = config['MySQLConfig']['host']
    db_port = config['MySQLConfig']['port']
    db_database = config['MySQLConfig']['database']
    
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        cRepository.migrateChannel()