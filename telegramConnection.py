from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

def getTelegramClient(api_id, api_hash, username, phone):
    client = TelegramClient(username, api_id, api_hash)
    client.start(phone)
    print("Client Created")
    # Ensure you're authorized
    isAuthenticated = client.is_user_authorized()
    if not isAuthenticated:
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    return client