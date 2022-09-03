import sys
import os
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import argparse
from telethon import events
from mysql.channelRepository import ChannelRepository
from elasticsearch import Elasticsearch
from telethon.tl.types import InputPeerEmpty
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig
import pandas as pd
import asyncio

es = Elasticsearch('http://localhost:9200', basic_auth=('elastic', 'H@ppYiCP@sswD9!*2'))
parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
args = parser.parse_args()

account = args.account
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account, os.path.abspath('../config.ini'))
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)
    
async def main():
    channelList = {
        "id": [],
        "name": []
    }
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig(os.path.abspath('../config.ini'))
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        async for entity in client.iter_dialogs(offset_date=None,
                                            offset_id=0,
                                            offset_peer=InputPeerEmpty()):
            channelList["id"].append(entity.id)
            channelList["name"].append(entity.title)

    df = pd.DataFrame(channelList)
    print("Select Channel ID for Subscribing the Telegram Channel")
    print(df.to_markdown())
    
    _id = input("Channel ID > ")

    @client.on(events.NewMessage(chats=[_id]))
    async def newMessageListener(event):
        newMessage = event.message.message
        print(newMessage)
    
    client.run_until_disconnected()
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()