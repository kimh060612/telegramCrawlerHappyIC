import configparser
import argparse
from mysql.channelRepository import ChannelRepository

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--channel', help='Table name for telegram channel list')
parser.add_argument('--blacklist', help='Table name for telegram Black list')
args = parser.parse_args()

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
        if not args.blacklist is None:
            cRepository.migrateBlackList(args.blacklist)
        if not args.channel is None:
            cRepository.migrateChannel(args.channel)