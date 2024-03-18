import os
import re
import asyncio
import time
from pyrogram import *
from pyrogram.types import *
from random import choice
from shivu import shivuu



API_HASH = "ec69ce8b56c71541499c914fabd08286"
API_ID = "25635673"
ASSUSERNAME = "not allowed"
app = shivuu

IMG = ["https://graph.org/file/1aaff3780b5ba59cb1f63.jpg", "https://graph.org/file/1aaff3780b5ba59cb1f63.jpg", "https://graph.org/file/1aaff3780b5ba59cb1f63.jpg", "https://graph.org/file/1aaff3780b5ba59cb1f63.jpg"]
MESSAGE = "Heya! I'm a music bot hoster/Cloner\n\nI can Host Your Bot On My Server within seconds\n\nTry /clone Token from @botfather"

@app.on_message(filters.private & filters.command("copy"))
async def copy(client, message: Message):
    buttons = [
           [
                InlineKeyboardButton("✘ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url="t.me/"),
            ],
            [
                InlineKeyboardButton("✘ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="t.me/"),
            ],
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, f"{choice(IMG)}", caption=MESSAGE, reply_markup=reply_markup)


@app.on_message(filters.private & filters.command("clone"))
async def clone(bot, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /clone token")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("Booting Your Client")
                   # change this Directry according to ur repo
        client = Client(name="Shivu", api_id=API_ID, api_hash=API_HASH, bot_token=phone, plugins=dict(root="shivu/modules"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f"Your Client Has Been Successfully Started As @{user.username}! ✅ \n\n Now Add Your Bot And Assistant @{ASSUSERNAME} To Your Chat!\n\nThanks for Cloning.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")
