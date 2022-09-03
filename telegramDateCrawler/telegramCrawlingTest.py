import sys
import os
sys.path.append(os.path.abspath('../mysql'))
sys.path.append(os.path.abspath('../'))
import argparse
from datetime import date
from pydoc import doc
from mysql.channelRepository import ChannelRepository
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig
from telethon.tl.types import PeerChannel
from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch('http://localhost:9200', basic_auth=('elastic', 'H@ppYiCP@sswD9!*2'))
print(es.info())
parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

account = args.account
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account, os.path.abspath('../config.ini'))
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

async def main():
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig(os.path.abspath('../config.ini'))
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        channelList = cRepository.getChannelWhiteList(table=table)
        print(channelList)
        
        for channel_id, channel_name, _ in channelList:
            print('----------------------{}-----------------------'.format(channel_name))
            # real_id, _ = utils.resolve_id(int(channel_id))
            # print(real_id)
            async for message in client.iter_messages(PeerChannel(int(channel_id)), offset_date=date.fromisoformat('2022-09-02'), limit=300, reverse=True):
                msg = message.to_dict()
                # print(msg["id"], msg["date"], msg["message"], msg["mentioned"])
                elastic_msg = {
                    "id": str(msg["id"]),
                    "date": msg["date"].strftime('%Y-%m-%d %H:%M'),
                    "content": msg["message"],
                    "mentioned": msg["mentioned"]
                }
                if not msg["fwd_from"] is None:
                    # print(msg["forwards"], msg["fwd_from"]["date"], msg["fwd_from"]["from_id"]["channel_id"]) # forwards: number that original msg is forwarded to another channels
                    # channel_forward = PeerChannel(int(msg["fwd_from"]["from_id"]["channel_id"]))
                    # msg_forward = await client.get_messages(channel_forward, ids=msg["fwd_from"]["channel_post"])
                    elastic_msg["forwards"] = msg["forwards"]
                    elastic_msg["fwd_msg_channel"] = str(msg["fwd_from"]["from_id"]["channel_id"])
                    elastic_msg["fwd_msg_id"] = str(msg["fwd_from"]["channel_post"])
                    elastic_msg["fwd_msg_date"] = msg["fwd_from"]["date"].strftime('%Y-%m-%d %H:%M')
                print(json.dumps(elastic_msg, indent=4))
                res = es.index(index='telegram', document=elastic_msg)
                print(res)
                print("\n")
                
            print('----------------------{}-----------------------'.format('-' * len(channel_name)))
        

if __name__ == "__main__":
    client.loop.run_until_complete(main())