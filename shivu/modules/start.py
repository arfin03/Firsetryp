import random
from html import escape 
from pyrogram import idle

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, db, GROUP_ID, BOT_USERNAME, SUPPORT_CHAT, UPDATE_CHAT, image_urls
from shivu import pm_users as collection 

collection = db['total_pm_users']

NAME = "ᴅᴀʀᴋ ᴅʀᴇᴀᴍ ᴡᴏʀʟᴅ"
gc_link = f'<a href="thttps://t.me/dark_world_231">{NAME}</a>'

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    chat_title = update.effective_chat.title  # Get the group's title

    user_data = await collection.find_one({"_id": user_id})

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

***I am An Open Source Character Catcher Bot...​Add Me in Your group.. And I will send Random Characters After every 100 messages in the Group... Use /guess to Collect those Characters in Your Collection... and see your Collection by using /Harem... So add me to your groups and start collecting your harem!\n\n {gc_link} ***
        """
        keyboard = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(image_urls)
        keyboard = [
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("ᴜᴏᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ\n\n {gc_link} ", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

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
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***Hoyyyy...*** ✨

***I am An Open Source Character Catcher Bot..​Add Me in Your group.. And I will send Random Characters After.. every 100 messages in Group... Use /guess to.. Collect that Characters in Your Collection.. and see Collection by using /Harem... So add in Your groups and Collect Your harem\n\n {gc_link} ***
        """

        
        keyboard = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
