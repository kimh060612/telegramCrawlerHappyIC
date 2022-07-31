import configparser
import argparse
from pydoc import cli
from mysql.channelRepository import ChannelRepository
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig
from telethon import functions
from telethon import utils
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChat, PeerChannel

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

account = args.account
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account)
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

config = configparser.ConfigParser()
config.read('./config.ini')

# Directory for saving files
file_directory_1 = config['FileDirectory']['first_directory']
file_directory_2 = config['FileDirectory']['second_directory']

async def main():
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig()
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        channelList = cRepository.getChannelList(table=table)
        async for channel_id, channel_name in channelList:
            print('----------------------{}-----------------------'.format(channel_name))
            real_id, _ = utils.resolve_id(channel_id)
            full = await client(functions.channels.GetFullChannelRequest(PeerChannel(real_id)))
            full_channel = full.full_chat
            if full_channel.migrated_from_chat_id:
                migrated_from_chat = next(c for c in full.chats if c.id == full_channel.migrated_from_chat_id)
                print(migrated_from_chat.title)
            if full_channel.linked_chat_id:
                linked_group = next(c for c in full.chats if c.id == full_channel.linked_chat_id)
                print(linked_group.username)
            print('----------------------{}-----------------------'.format('-' * len(channel_name)))
        

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    

    
    


    
