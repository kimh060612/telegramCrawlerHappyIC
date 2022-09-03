import sys
import os
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import argparse
from telethon import events
from elasticsearch import Elasticsearch
from telegramConnection import getTelegramClient, getTelegramConfig
from telethon.tl.types import PeerChannel
import asyncio

es = Elasticsearch('http://localhost:9200', basic_auth=('elastic', 'H@ppYiCP@sswD9!*2'))
parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--channel_id', required=True, help='Channel ID for subscribing')
args = parser.parse_args()

account = args.account
Channel = PeerChannel(int(args.channel_id))
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account, os.path.abspath('../config.ini'))
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

@client.on(events.NewMessage(chats=Channel))
async def newMessageListener(event):
    newMessage = event.message
    print(newMessage)
    
if __name__ == "__main__":
    client.run_until_disconnected()