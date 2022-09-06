class ChannelEntity:
    def __init__(self, 
                 channel_name,
                 channel_id,
                 channel_status
                ):
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.channel_status = channel_status
    
class BlackListEntity:
    def __init__(self,  
                 blacklist_regex, 
                 blacklist_description,
                 blacklist_status
                ):
        self.blacklist_regex = blacklist_regex
        self.blacklist_description = blacklist_description
        self.blacklist_status = blacklist_status