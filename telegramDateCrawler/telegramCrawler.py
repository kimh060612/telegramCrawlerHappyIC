import sys
import os
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import configparser
import argparse
from datetime import date, timedelta, tzinfo
import json
from mysql.channelRepository import ChannelRepository
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig
from telethon.tl.types import PeerChannel
from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200', basic_auth=('elastic', 'H@ppYiCP@sswD9!*2'))
parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

account = args.account
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account, os.path.abspath('../config.ini'))
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

async def telegramCrawler(channel_id: str, from_date: date, limit=300):    
    async for message in client.iter_messages(PeerChannel(int(channel_id)), offset_date=from_date, limit=limit):
        msg = message.to_dict()
        # print(msg["id"], msg["date"], msg["message"])
        elastic_msg = {
            "id": str(msg["id"]),
            "date": msg["date"].strftime('%Y-%m-%d %H:%M'),
            "content": msg["message"],
            "mentioned": msg["mentioned"],
            "forwards": msg["forwards"]
        }
        if not msg["fwd_from"] is None:
            try :
                elastic_msg["fwd_msg_channel"] = str(msg["fwd_from"]["from_id"]["channel_id"])
                elastic_msg["fwd_msg_id"] = str(msg["fwd_from"]["channel_post"])
                elastic_msg["fwd_msg_date"] = msg["fwd_from"]["date"].strftime('%Y-%m-%d %H:%M')
            except :
                print(msg)
                continue
        print(json.dumps(elastic_msg, indent=4))
        _ = es.index(index='telegram', document=elastic_msg)
        print("\n")

def daterange(start: date, end: date):
    for n in range(int((end - start).days)):
        yield start + timedelta(n)

if __name__ == "__main__":
    print("########################### Telegram Offline Crawler ############################")
    print("############ Caution! This Crawler does not contain the photo savings ############")
    
    s = input("Crawling Start Date (ISO Format: YYYY-MM-DD) > ")
    e = input("Crawling End Date (ISO Format: YYYY-MM-DD) > ")
    sdate = date.fromisoformat(s)
    edate = date.fromisoformat(e)
    
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig(os.path.abspath('../config.ini'))
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        channelList = cRepository.getChannelWhiteList(table=table)
        for channel_id, channel_name, _ in channelList:
            for _date in daterange(sdate, edate):
                client.loop.run_until_complete(telegramCrawler(channel_id=channel_id, from_date=_date))

    
