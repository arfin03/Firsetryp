import json
import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, db, GROUP_ID, BOT_USERNAME, SUPPORT_CHAT, UPDATE_CHAT, image_urls, shivuu

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

app = shivuu

collection = db['total_pm_users']

MUST_JOIN = "dosti_ki_baate"


import random

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from shivu import application, db, GROUP_ID, image_urls, shivuu

app = shivuu

collection = db['total_pm_users']

MUST_JOIN = "DARK_DREAM_WORLD"


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title  # Get the group's title

    user_data = await collection.find_one({"_id": user_id})

    try:
        if MUST_JOIN:
            await app.get_chat_member(MUST_JOIN, user_id)
    except UserNotParticipant:
        # User has not joined, return without sending the start message
        return

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})

        # Send information to the specified group
        if chat_type != "private":
            group_message = f"New user started the bot in group {chat_title} ({chat_id}).\n" \
                            f"User: <a href='tg://user?id={user_id}'>{escape(first_name)}</a>"
            await context.bot.send_message(chat_id=GROUP_ID, text=group_message, parse_mode='HTML')

    # Update the existing code below...
    if user_data is not None:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    if chat_type == "private":
        photo_url = random.choice(image_urls)

        caption = """
        ***Heyyyy...***

***hello i am tg game bot***
        """

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, parse_mode='markdown')

    else:
        photo_url = random.choice(image_urls)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ")

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://telegra.ph/file/415a20d01e642ffc1bb6d.jpg", caption=f"๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ʏᴇᴛ, ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ ᴊᴏɪɴ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ ! ",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("๏Jᴏɪɴ๏", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"๏ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴍᴜsᴛ_Jᴏɪɴ ᴄʜᴀᴛ ๏: {MUST_JOIN}")

start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
