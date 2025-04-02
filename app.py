from telethon import TelegramClient , events
from config import api_hash , api_id , unsplash_access_key
import logging
import os
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()

logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Use your own values from my.telegram.org
api_id = api_id
api_hash = api_hash

client = TelegramClient('dracula_ub_session', api_id, api_hash)
botClient = TelegramClient("bot", api_id=api_id, api_hash=api_hash)

# Unsplash API configuration
UNSPLASH_ACCESS_KEY = unsplash_access_key
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

@botClient.on(events.InlineQuery)
async def inline_handler(event : events.InlineQuery.Event):
    if not event.text:
        return

    async with aiohttp.ClientSession() as session:
        params = {
            "query": event.text,
            "per_page": 10,
            "client_id": UNSPLASH_ACCESS_KEY
        }
        async with session.get(UNSPLASH_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results = []
                
                for photo in data.get("results", []):
                    results.append(
                        event.builder.photo(
                            file=photo["urls"]["regular"],
                            text=f"📸 {photo['alt_description'] or 'No description available'}\n\nPhoto by: {photo['user']['name']} on Unsplash"
                        )
                    )
                
                await event.answer(results)


@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def handler(event : events.NewMessage.Event):
    print(event)
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        path = await client.download_profile_photo(sender)
        await client.send_file("me" , path , caption=f"@{sender.username}")
        await client.edit_message(event.message , 'Saved your photo @{}'.format(sender.username))
        
        os.remove(path=path)
        
async def main():
    print("Starting clients...")
    
    # Start both clients
    await client.start()
    await botClient.start(bot_token="8032102060:AAHZwcw7gv8OKSZrAnxUYG-Nd8VQi6UI7Rw")
    
    print("Started - Listening for messages...")
    
    # Run both clients concurrently
    await asyncio.gather(
        client.run_until_disconnected(),
        botClient.run_until_disconnected()
    )
    
if __name__ == "__main__":
    asyncio.run(main())


