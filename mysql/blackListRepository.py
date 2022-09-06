from .service import AbstractRepository, StoreException
from .channelEntity import BlackListEntity

class BlackListRepository(AbstractRepository):
    def __init__(self, host, port, username, password, db):
        super().__init__(host, port, username, password, db)
    
    def getBlackList(self, table: str):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM {}'.format(table))
            return c.fetchall()
        except Exception as e:
            raise StoreException('error reading channel')
    
    def getActivatedBlackList(self, table: str):
        try:
            c = self.conn.cursor()
            c.execute('SELECT * FROM {} WHERE blacklist_status="Y"'.format(table))
            return c.fetchall()
        except Exception as e:
            raise StoreException('error reading channel')
    
    def updateBlackList(self, table: str, uuid: str, status: bool):
        try:
            c = self.conn.cursor()
            statusCode = "Y" if status else "N"
            c.execute('UPDATE {} SET blacklist_status="{}" WHERE id="{}"'.format(table, statusCode, uuid))
        except Exception as e:
            raise StoreException('error updating channel')
    
    def insertBlackList(self, blackList: BlackListEntity, table: str):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO {}(blacklist_regex, blacklist_description, blacklist_status) VALUES("{}", "{}", "{}")'.format(
                table,
                blackList.blacklist_regex,
                blackList.blacklist_description,
                blackList.blacklist_status
            ))
        except Exception as e:
            raise StoreException('error inserting channel') 
    
    def migrateBlackList(self, table_name):
        try:
            c = self.conn.cursor()
            c.execute('CREATE TABLE {}( id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                                        blacklist_regex TEXT not null, \
                                        blacklist_description TEXT not null, \
                                        blacklist_status varchar(10) not null \
                                    )'.format(table_name))
        except Exception as e:
            raise StoreException('error updating channel')