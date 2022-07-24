from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

async def getTelegramClient(api_id, api_hash, username, phone):
    client = TelegramClient(username, api_id, api_hash)
    await client.start(phone)
    print("Client Created")
    # Ensure you're authorized
    isAuthenticated = await client.is_user_authorized()
    if not isAuthenticated:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    return client