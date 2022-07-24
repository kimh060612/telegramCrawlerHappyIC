import argparse
import configparser
import asyncio
from telegramConnection import getTelegramClient
from telethon.tl.functions.messages import GetHistoryRequest, GetDialogsRequest
from telethon.tl.types import PeerChannel, InputPeerEmpty

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
args = parser.parse_args()

async def main():
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
    
    t_client = await getTelegramClient(api_id, api_hash, username, phone)
    channels = await t_client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=100,
        hash=0
    ))
    print(channels.chats)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()