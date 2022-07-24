import pymysql

class ChannelEntity:
    def __init__(self, 
                 channel_name,
                 channel_id,
                 channel_status
                ):
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.channel_status = channel_status
    
    