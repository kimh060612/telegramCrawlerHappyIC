from .service import AbstractRepository, StoreException
from .channelEntity import ChannelEntity

class ChannelRepository(AbstractRepository):
    def __init__(self, host, port, username, password, db):
        super().__init__(host, port, username, password, db)
    
    def getChannelList(self):
        
        pass
    
    def insertChannel(self, channel: ChannelEntity):
        pass
    
    def migrateChannel(self):
        try:
            c = self.conn.cursor()
            c.execute('CREATE TABLE channels( channel_id varchar(100) not null primary key, \
                                              channel_name varchar(255) not null, \
                                              channel_status varchar(10) not null \
                                            )')
        except Exception as e:
            raise StoreException('error creating table')