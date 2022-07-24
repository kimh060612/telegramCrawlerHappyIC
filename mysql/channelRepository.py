from .service import AbstractRepository, StoreException
from .channelEntity import ChannelEntity

class ChannelRepository(AbstractRepository):
    def __init__(self, host, port, username, password, db):
        super().__init__(host, port, username, password, db)
    
    def getChannelList(self):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM channels WHERE channel_status="Y"')
        except Exception as e:
            raise StoreException('error reading channel')
    
    def insertChannel(self, channel: ChannelEntity):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO channels(channel_id, channel_name, channel_status) VALUES({}, {}, {})'.format(
                channel.channel_id,
                channel.channel_name,
                channel.channel_status
            ))
        except Exception as e:
            raise StoreException('error inserting channel')
    
    def migrateChannel(self, table_name):
        try:
            c = self.conn.cursor()
            c.execute('CREATE TABLE {}( channel_id varchar(100) not null primary key, \
                                              channel_name varchar(255) not null, \
                                              channel_status varchar(10) not null \
                                            )'.format(table_name))
        except Exception as e:
            raise StoreException('error creating table')