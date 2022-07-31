import argparse
import configparser
from mysql.channelRepository import ChannelRepository
from mysql.channelEntity import ChannelEntity
from telegramConnection import getTelegramClient
from telethon.tl.types import InputPeerEmpty

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

def getTelegramConfig():
    account = args.account
    config = configparser.ConfigParser()
    config.read('./config.ini')

    #### Configuration Parsing
    # Parse API Account Information
    api_id = config[account]['api_id']
    api_hash = config[account]['api_hash']
    api_hash = str(api_hash)
    phone = config[account]['phone']
    username = config[account]['username']
    
    return api_id, api_hash, username, phone

def getDatabaseConfig():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    
    db_username = config['MySQLConfig']['username']
    db_password = config['MySQLConfig']['password']
    db_host = config['MySQLConfig']['host']
    db_port = config['MySQLConfig']['port']
    db_database = config['MySQLConfig']['database']
    
    return db_username, db_password, db_host, db_port, db_database
    
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig()
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

async def main():
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig()
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        async for entity in client.iter_dialogs(offset_date=None,
                                                offset_id=0,
                                                offset_peer=InputPeerEmpty()):
            try:
                cRepository.insertChannel(ChannelEntity(entity.title, entity.id, "Y"), table)
                print('{:>14}: {} save success!'.format(entity.id, entity.title))
            except:
                print('{:>14}: {} save failed!'.format(entity.id, entity.title))
        cRepository.complete()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    