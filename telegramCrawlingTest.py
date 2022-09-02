import configparser
import argparse
from datetime import date
from pydoc import cli
from mysql.channelRepository import ChannelRepository
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig
from telethon import functions
from telethon import utils
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChat, PeerChannel
import pprint 

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

pp = pprint.PrettyPrinter(indent=4)

async def main():
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig()
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        channelList = cRepository.getChannelWhiteList(table=table)
        print(channelList)
        
        for channel_id, channel_name, _ in channelList:
            print('----------------------{}-----------------------'.format(channel_name))
            # real_id, _ = utils.resolve_id(int(channel_id))
            # print(real_id)
            async for message in client.iter_messages(PeerChannel(int(channel_id)), offset_date=date.today(), limit=300, reverse=True):
                msg = message.to_dict()
                print(msg["id"], msg["date"], msg["message"], msg["mentioned"])
                if not msg["fwd_from"] is None:
                    print(msg["forwards"], msg["fwd_from"]["date"], msg["fwd_from"]["from_id"]["channel_id"]) # forwards: number that original msg is forwarded to another channels
                    channel_forward = PeerChannel(int(msg["fwd_from"]["from_id"]["channel_id"]))
                    msg_forward = await client.get_messages(channel_forward, ids=msg["fwd_from"]["channel_post"])
                    pp.pprint(msg_forward.to_dict())
                # pp.pprint(msg)
                print("\n")
            print('----------------------{}-----------------------'.format('-' * len(channel_name)))
        

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    

    
    


    
