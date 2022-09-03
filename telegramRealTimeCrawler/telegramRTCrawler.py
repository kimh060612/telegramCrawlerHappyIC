import sys
import os
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import argparse
from telethon import events
from elasticsearch import Elasticsearch
from telethon.tl.types import InputPeerEmpty
from telegramConnection import getTelegramClient, getTelegramConfig
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
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    client.run_until_disconnected()
    loop.close()