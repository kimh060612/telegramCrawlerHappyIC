import configparser
import json
import argparse
import uuid
import asyncio
import pandas as pd

from mysql.channelRepository import ChannelRepository
from telegramConnection import getTelegramClient

from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
args = parser.parse_args()

if __name__ == "__main__":
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
    
    # Save file 
    file_directory_1 = config['FileDirectory']['first_directory']
    file_directory_2 = config['FileDirectory']['second_directory']
    
    # Crawler Channel Configuration
    db_username = config['MySQLConfig']['username']
    db_password = config['MySQLConfig']['password']
    db_host = config['MySQLConfig']['host']
    db_port = config['MySQLConfig']['port']
    db_database = config['MySQLConfig']['database']
    #### 
    
    t_client = getTelegramClient(api_id, api_hash, username, phone)

    
    


    
