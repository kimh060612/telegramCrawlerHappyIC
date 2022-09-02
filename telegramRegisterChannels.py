import argparse
from mysql.channelRepository import ChannelRepository
from mysql.channelEntity import ChannelEntity
from telegramConnection import getTelegramClient, getTelegramConfig
from DBConfig import getDatabaseConfig
from telethon.tl.types import InputPeerEmpty
from telethon import utils

parser = argparse.ArgumentParser(description="Telegram Chatting Crawler for HappyIC Project")
parser.add_argument('--account', required=True, default="AlexYong" ,help='Which Account you want to Crawl from Telegram')
parser.add_argument('--table', required=True, default="channels" ,help='Table name for telegram channel list')
args = parser.parse_args()

account = args.account
API_ID, API_HASH, USERNAME, PHONE = getTelegramConfig(account)
client = getTelegramClient(API_ID, API_HASH, USERNAME, PHONE)

async def main():
    table = args.table
    db_username, db_password, db_host, db_port, db_database = getDatabaseConfig()
    with ChannelRepository(host=db_host, 
                           port=db_port, 
                           username=db_username,
                           password=db_password,
                           db=db_database) as cRepository:
        async for entity in client.iter_dialogs(offset_date=None,
                                                offset_id=0,
                                                offset_peer=InputPeerEmpty()):
            try:
                real_id, _ = utils.resolve_id(int(entity.id))
                cRepository.insertChannel(ChannelEntity(entity.title, real_id, "N"), table)
                print('{:>14}: {} save success!'.format(entity.id, entity.title))
            except:
                print('{:>14}: {} save failed!'.format(entity.id, entity.title))
        cRepository.complete()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
    