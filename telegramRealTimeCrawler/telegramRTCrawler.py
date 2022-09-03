import sys
import os
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import argparse
from telethon import events
from elasticsearch import Elasticsearch
from telethon.tl.types import PeerChannel
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

account = args.account
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account, os.path.abspath('../config.ini'))
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

@client.on(events.NewMessage())
async def newMessageListener(event):
    newMessage = event.message.message
    print(newMessage)
    
if __name__ == "__main__":
    client.run_until_disconnected()