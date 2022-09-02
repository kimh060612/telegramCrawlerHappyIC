import argparse
from xmlrpc.client import boolean
from mysql.channelRepository import ChannelRepository
from mysql.channelEntity import ChannelEntity
from DBConfig import getDatabaseConfig
from telegramConnection import getTelegramClient, getTelegramConfig
from telethon.tl.types import InputPeerEmpty
from telethon.client import TelegramClient
from telethon import utils
import pandas as pd

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

db_username, db_password, db_host, db_port, db_database = getDatabaseConfig()

def printHelp():
    print("----------------------------------Help-----------------------------------")
    print("> ListAll: List the telegram channel listed in the Whitelist")
    print("> Whitelist: List the telegram channel listed in the Whitelist")
    print("> Register <id>: Register telegram channel in the Whitelist")
    print("> Unregister <id>: Delete telegram channel in the Whitelist")
    print("> Activity <id>: Check the Message Activity of the Telegram Channel")
    print("> Update <User>: Update Telegram Channel List")
    print("> help: Print Help Menu")
    print("-------------------------------------------------------------------------")

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

def updateWhitelist(uuid: str, status: bool):
    table = args.table
    with ChannelRepository(host=db_host, 
                        port=db_port, 
                        username=db_username,
                        password=db_password,
                        db=db_database) as cRepository:
        cRepository.updateChannel(table, uuid, status)
        cRepository.complete()

async def updateChannels(_client: TelegramClient):
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig()
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
                cRepository.insertChannel(ChannelEntity(entity.title, real_id, "N"), table)
                print('{:>14}: {} save success!'.format(real_id, entity.title))
            except:
                print('{:>14}: {} save failed!'.format(real_id, entity.title))
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
            elif com == "Register":
                _id = command.split(' ')[1]
                updateWhitelist(_id, True)
            elif com == "Unregister":
                _id = command.split(' ')[1]
                updateWhitelist(_id, False)
            elif com == "Update":
                user = command.split(' ')[1]
                API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(user)
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
    
    