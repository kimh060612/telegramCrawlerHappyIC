import sys
import os
from turtle import towards
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import argparse
from mysql.channelRepository import ChannelRepository
from mysql.blackListRepository import BlackListRepository
from DBConfig import getDatabaseConfig
from telethon import events
from elasticsearch import Elasticsearch
from telegramConnection import getTelegramBotTowards, getTelegramClient, getTelegramConfig
from telethon.tl.types import PeerChannel
import requests
import json
import regex as re
from .elasticSearchBody import body

es = Elasticsearch('http://localhost:9200', basic_auth=('elastic', 'H@ppYiCP@sswD9!*2'))
_res = es.indices.create(index="telegram_msg", body=body, include_type_name =True, ignore=[400, 404])
parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

CONFIG_PATH = os.path.abspath('../config.ini')
BLACKLIST_TABLE = "BlackList"
_towards = PeerChannel(int(getTelegramBotTowards(CONFIG_PATH)))
db_username, db_password, db_host, db_port, db_database = getDatabaseConfig(CONFIG_PATH)
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(args.account, CONFIG_PATH)
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)
ChannelList = []
print("<----------------------Loading White Channels from DB....---------------------->")
with ChannelRepository(host=db_host, 
                        port=db_port, 
                        username=db_username,
                        password=db_password,
                        db=db_database) as cRepository:
    channelList = cRepository.getChannelWhiteList(args.table)
    for channel_id, name, _ in channelList:
        Channel = PeerChannel(int(channel_id))
        print("Channel {} Load Success!".format(name))
        ChannelList.append(Channel)
print("<-------------------------White Channel Load Complete!------------------------->")
reqSession = requests.session()

def printStatus(status):
    if status >= 400:
        print("Failed to Send the Message to bot!")
    else :
        print("Successfully Send the Message to bot!")

@client.on(events.NewMessage(chats=ChannelList))
async def newMessageListener(event):
    rawMsg = event.message
    msg = rawMsg.to_dict()
    print(msg)
    elastic_msg = {
        "id": str(msg["id"]),
        "date": msg["date"],
        "content": msg["message"],
        "mentioned": msg["mentioned"],
        "forwards": str(msg["forwards"])
    }
    sendMsgFlag = False
    if msg["fwd_from"] is None:
        print(json.dumps(elastic_msg, indent=4))
        # send request to telegram bot
        sendMsgFlag = True
    else:
        try :
            _id = str(msg["fwd_from"]["from_id"]["channel_id"])
            with ChannelRepository(host=db_host, 
                        port=db_port, 
                        username=db_username,
                        password=db_password,
                        db=db_database) as cRepository:
                _c = cRepository.getChannelById(args.table, _id)
                if not _c:
                    elastic_msg["fwd_msg_channel"] = str(_id)
                    elastic_msg["fwd_msg_id"] = str(msg["fwd_from"]["channel_post"] if not msg["fwd_from"]["channel_post"] is None else -1)
                    elastic_msg["fwd_msg_date"] = msg["fwd_from"]["date"].strftime('%Y-%m-%d %H:%M')
                    print(json.dumps(elastic_msg, indent=4))
                    # send request to telegram bot
                    sendMsgFlag = True
                else :
                    print("This is duplicated message! Skipping...")
        except Exception as e:
            print(e)
            print("Invalid Message Format!")
    with BlackListRepository(host=db_host, 
                        port=db_port, 
                        username=db_username,
                        password=db_password,
                        db=db_database) as bRepository:
        blackList = bRepository.getActivatedBlackList(BLACKLIST_TABLE)
        for _, regex, des, _ in blackList:
            if re.match(regex, msg["message"]):
                print("Regex {} Matched!".format(des))
                sendMsgFlag = False
    if sendMsgFlag:
        _ = es.index(index='telegram_msg', document=elastic_msg)
        channel_toward = await client.get_entity(_towards)
        await client.forward_messages(channel_toward, rawMsg)
    print("\n")
    
if __name__ == "__main__":
    print("<----------------------Start Publishing the Chatbot!---------------------->")
    client.run_until_disconnected()