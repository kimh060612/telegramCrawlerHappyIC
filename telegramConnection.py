import configparser
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import os

def getTelegramClient(api_id, api_hash, username, phone):
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    print("Client Created")
    # Ensure you're authorized
    isAuthenticated = client.is_user_authorized()
    if not isAuthenticated:
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    return client

def getTelegramConfig(account, config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    #### Configuration Parsing
    # Parse API Account Information
    api_id = config[account]['api_id']
    api_hash = config[account]['api_hash']
    api_hash = str(api_hash)
    phone = config[account]['phone']
    username = config[account]['username']
    
    return api_id, api_hash, username, phone