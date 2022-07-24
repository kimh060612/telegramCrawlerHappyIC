import argparse
import configparser
import json
from telegramConnection import getTelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
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

API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig()
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

async def main():
    async for entity in client.iter_dialogs(offset_date=None,
                                            offset_id=0,
                                            offset_peer=InputPeerEmpty()):
        print('{:>14}: {}'.format(entity.id, entity.title))

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    