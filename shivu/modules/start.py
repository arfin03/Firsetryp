import random
import json

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

app = Client("my_bot")

collection = db['total_pm_users']

MUST_JOIN = "DARK_DREAM_WORLD"

@app.on_message(filters.command(["start"]))
async def start_command(_, message):
    await start(message)

async def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    chat_id = message.chat.id
    chat_type = message.chat.type
    chat_title = message.chat.title  # Get the group's title

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
                            f"User: [{first_name}](tg://user?id={user_id})"
            await app.send_message(chat_id=GROUP_ID, text=group_message, parse_mode='MarkdownV2')

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
        keyboard = [
            [{"text": "ᴀᴅᴅ ᴍᴇ", "url": f'http://t.me/{BOT_USERNAME}?startgroup=new'}],
            [{"text": "sᴜᴘᴘᴏʀᴛ", "url": f'https://t.me/{SUPPORT_CHAT}'},
             {"text": "ᴜᴘᴅᴀᴛᴇs", "url": f'https://t.me/{UPDATE_CHAT}'}],
            [{"text": "ʜᴇʟᴘ", "callback_data": 'help'}],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await app.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='MarkdownV2')

    else:
        photo_url = random.choice(image_urls)
        keyboard = [
            [{"text": "sᴜᴘᴘᴏʀᴛ", "url": f'https://t.me/{SUPPORT_CHAT}'},
             {"text": "ᴜᴏᴅᴀᴛᴇs", "url": f'https://t.me/{UPDATE_CHAT}'}],
            [{"text": "ᴀᴅᴅ ᴍᴇ", "url": f'http://t.me/{BOT_USERNAME}?startgroup=new'}],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await app.send_photo(chat_id=message.chat.id, photo=photo_url, caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ", reply_markup=reply_markup)

@app.on_callback_query(filters.regex("^help$"))
async def help_callback(_, query):
    await button(query)

@app.on_callback_query(filters.regex("^back$"))
async def back_callback(_, query):
    await button(query)

async def button(query):
    if query.data == 'help':
        help_text = """
    ***Help Section:***
    
***/guess: Tᴏ Gᴜᴇss ᴄʜᴀʀᴀᴄᴛᴇʀ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘ)***
***/fav: Aᴅᴅ Yᴏᴜʀ ғᴀᴠ***
***/trade : Tᴏ ᴛʀᴀᴅᴇ Cʜᴀʀᴀᴄᴛᴇʀs***
***/gift: Gɪᴠᴇ ᴀɴʏ Cʜᴀʀᴀᴄᴛᴇʀ ғʀᴏᴍ Yᴏᴜʀ Cᴏʟʟᴇᴄᴛɪᴏɴ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ.. (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs)***
***/collection: Tᴏ sᴇᴇ Yᴏᴜʀ Cᴏʟʟᴇᴄᴛɪᴏɴ***
***/topgroups : Sᴇᴇ Tᴏᴘ Gʀᴏᴜᴘs.. Pᴘʟ Gᴜᴇssᴇs Mᴏsᴛ ɪɴ ᴛʜᴀᴛ Gʀᴏᴜᴘs***
***/top: Tᴏᴏ Sᴇᴇ Tᴏᴘ Usᴇʀs***
***/ctop : Yᴏᴜʀ CʜᴀᴛTᴏᴘ***
***/changetime: Cʜᴀɴɢᴇ Cʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀ ᴛɪᴍᴇ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ Gʀᴏᴜᴘs)***
   """
        help_keyboard = [[InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await query.message.edit_caption(caption=help_text, reply_markup=reply_markup, parse_mode='MarkdownV2')

    elif query.data == 'back':

        caption = f"""
        ***Hoyyyy...*** ✨

***I am An Open Source Character Catcher Bot..​Add Me in Your group.. And I will send Random Characters After.. every 100 messages in Group... Use /guess to.. Collect that Characters in Your Collection.. and see Collection by using /Harem... So add in Your groups and Collect Your harem***
        """

        
        keyboard = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_caption(caption=caption, reply_markup=reply_markup, parse_mode='MarkdownV2')

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(_, msg):
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

