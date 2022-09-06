from .service import AbstractRepository, StoreException
from .channelEntity import ChannelEntity

class ChannelRepository(AbstractRepository):
    def __init__(self, host, port, username, password, db):
        super().__init__(host, port, username, password, db)
    
    def getChannelList(self, table: str):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM {}'.format(table))
            return c.fetchall()
        except Exception as e:
            raise StoreException('error reading channel')
    
    def getChannelWhiteList(self, table: str):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM {} WHERE channel_status="Y"'.format(table))
            return c.fetchall()
        except Exception as e:
            raise StoreException('error reading channel')
    
    def getChannelByName(self, table: str, channel_name: str):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM {} WHERE channel_name="{}" AND channel_status="Y"'.format(table, channel_name))
            return c.fetchone()
        except Exception as e:
            raise StoreException('error reading channel')
            
    def getChannelById(self, table: str, channel_id: str):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM {} WHERE channel_id="{}" AND channel_status="Y"'.format(table, channel_id))
            return c.fetchone()
        except Exception as e:
            raise StoreException('error reading channel')
    
    def insertChannel(self, channel: ChannelEntity, table: str):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO {}(channel_id, channel_name, channel_status) VALUES("{}", "{}", "{}")'.format(
                table,
                channel.channel_id,
                channel.channel_name,
                channel.channel_status
            ))
        except Exception as e:
            raise StoreException('error inserting channel')
    
    def updateChannel(self, table: str, uuid: str, status: bool):
        try:
            c = self.conn.cursor()
            statusCode = "Y" if status else "N"
            c.execute('UPDATE {} SET channel_status="{}" WHERE channel_id="{}"'.format(table, statusCode, uuid))
        except Exception as e:
            raise StoreException('error updating channel')
    
    def migrateChannel(self, table_name):
        try:
            c = self.conn.cursor()
            c.execute('CREATE TABLE {}( channel_id varchar(100) not null primary key, \
                                              channel_name varchar(255) not null, \
                                              channel_status varchar(10) not null \
                                            )'.format(table_name))
        except Exception as e:
            raise StoreException('error creating table')