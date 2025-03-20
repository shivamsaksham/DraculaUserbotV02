from telethon import TelegramClient , events
from config import api_hash , api_id
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Use your own values from my.telegram.org
api_id = api_id
api_hash = api_hash

client = TelegramClient('dracula_ub_session', api_id, api_hash)

@client.on(events.NewMessage(pattern=r'\.save'))
async def my_event_handler(event : events.NewMessage.Event):
    print(event)
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        pic = await client.download_profile_photo(sender)
        await client.send_file('me' , pic , caption=f"@{sender.username}")
        await client.edit_message(event.message , 'Saved your photo {}'.format(sender.username))
        await os.remove(pic)

client.start()
print("Bot Started")
client.run_until_disconnected()

