import argparse
from xmlrpc.client import boolean
from mysql.blackListRepository import BlackListRepository
from mysql.channelRepository import ChannelRepository
from mysql.channelEntity import BlackListEntity, ChannelEntity
from DBConfig import getDatabaseConfig
from telegramConnection import getTelegramClient, getTelegramConfig
from telethon.tl.types import InputPeerEmpty
from telethon.client import TelegramClient
from telethon import utils
import pandas as pd
import os 
import regex as re
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

db_username, db_password, db_host, db_port, db_database = getDatabaseConfig(os.path.abspath('./config.ini'))

BLACKLIST_TABLE = "BlackList"
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
"]+", flags=re.UNICODE)

def printHelp():
    print("--------------------------------------Help---------------------------------------")
    print("> ListAll: List the telegram channel listed in the Whitelist")
    print("> Whitelist: List the telegram channel listed in the Whitelist")
    print("> BlacklistAll: List all the telegram message filter regex in the Blacklist")
    print("> Blacklist: List the telegram message filter regex activated in the Blacklist")
    print("> RegisterRegex <file directory>: Register Telegram Message filter regex in the Blacklist")
    print("> UnregisterRegex <ids>: Delete telegram message filter regex in the Blacklist")
    print("> Register <ids>: Register telegram channel in the Whitelist")
    print(">>>>> <ids>: format like 'id_1,id_2,id_3,id_4...,id_N'")
    print("> Unregister <ids>: Delete telegram channel in the Whitelist")
    print("> Activity <ids>: Check the Message Activity of the Telegram Channel")
    print("> Update <User>: Update Telegram Channel List")
    print("> help: Print The Descriptions of Command")
    print("---------------------------------------------------------------------------------")

def printBlackList(showAll: bool):
    with BlackListRepository (host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as bRepository:
        blackList = []
        if showAll:
            blackList = bRepository.getBlackList(BLACKLIST_TABLE)
        else :
            blackList = bRepository.getActivatedBlackList(BLACKLIST_TABLE)
        data = {
            "id": [],
            "regex": [],
            "description": [],
            "status": []
        }
        for id, regex, description, status in blackList:
            data["id"].append(id)
            data["regex"].append(regex)
            data["description"].append(description)
            data["status"].append(status)
        df = pd.DataFrame(data)
        print(df.to_markdown())
        
def registerBlackList(file_dir: str):
    df = pd.read_csv(file_dir, header=0)
    print(df.to_markdown())
    with BlackListRepository (host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as bRepository:
        for _, row in tqdm(df.iterrows(), total=df.shape[0]):
            regex = row["regex"]
            description = row["description"]
            try:
                re.compile(regex)
            except:
                print("Invalid Regex: {}".format(regex))
                continue
            bRepository.insertBlackList(BlackListEntity(blacklist_regex=regex, 
                                                        blacklist_description=description, 
                                                        blacklist_status="Y"), BLACKLIST_TABLE)
            bRepository.complete()

def unregisterBlacklist(idList: list):
    with BlackListRepository (host=db_host, 
                        port=db_port, 
                        username=db_username,
                        password=db_password,
                        db=db_database) as bRepository:
        for id in idList:
            bRepository.updateBlackList(BLACKLIST_TABLE, id, False)
        bRepository.complete()

def printChannelList(whitelist: bool):
    table = args.table
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        channelList = []
        if whitelist:
            channelList = cRepository.getChannelWhiteList(table)
        else :
            channelList = cRepository.getChannelList(table)
        uuidList = []
        channelNameList = []
        channelStatus = []
        for channel_id, channel_name, channel_status in channelList:
            uuidList.append(channel_id)
            channelNameList.append(channel_name)
            channelStatus.append(channel_status)
        data = {
            "uuid": uuidList,
            "name": channelNameList,
            "status": channelStatus
        }
        df = pd.DataFrame(data)
        print(df.to_markdown())

def updateWhitelist(idList: list, status: bool):
    table = args.table
    with ChannelRepository(host=db_host, 
                            port=db_port, 
                            username=db_username,
                            password=db_password,
                            db=db_database) as cRepository:
        for id in idList:
            cRepository.updateChannel(table, id, status)
        cRepository.complete()

async def updateChannels(_client: TelegramClient):
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig(os.path.abspath('./config.ini'))
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        async for entity in _client.iter_dialogs(offset_date=None,
                                                offset_id=0,
                                                offset_peer=InputPeerEmpty()):
            try:
                real_id, _ = utils.resolve_id(int(entity.id))
                title = emoji_pattern.sub(r'', entity.title)
                cRepository.insertChannel(ChannelEntity(title, real_id, "N"), table)
                print('{:>14}: {} save success!'.format(real_id, title))
            except:
                print('{:>14}: {} save failed!'.format(real_id, title))
        cRepository.complete()
        
if __name__ == "__main__":
    
    printHelp()
    while True:
        try:
            command = input("Command> ")
            com = command.split(' ')[0]
            if com == "ListAll":
                printChannelList(False)
            elif com == "Whitelist":
                printChannelList(True)
            elif com == "BlacklistAll":
                printBlackList(True)
            elif com == "Blacklist":
                printBlackList(False)
            elif com == "RegisterRegex":
                _dir = command.split(' ')[1]
                registerBlackList(_dir)
            elif com == "UnregisterRegex":
                _ids = _ids = command.split(' ')[1]
                idList = _ids.split(',')
                unregisterBlacklist(idList)
            elif com == "Register":
                _ids = command.split(' ')[1]
                idList = _ids.split(',')
                updateWhitelist(idList, True)
            elif com == "Unregister":
                _ids = command.split(' ')[1]
                idList = _ids.split(',')
                updateWhitelist(idList, False)
            elif com == "Update":
                user = command.split(' ')[1]
                API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(user, os.path.abspath('./config.ini'))
                client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)
                client.loop.run_until_complete(updateChannels(client))
            elif com == "Activity":
                print("Activity Rate is not implemented yet!")
            elif com == "help":
                printHelp()
            else :
                print("Command not exists")
        except KeyboardInterrupt:
            print("Quit")
            break
    
    