from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

async def getTelegramClient(api_id, api_hash, username, phone):
    client = TelegramClient(username, api_id, api_hash)
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    return client