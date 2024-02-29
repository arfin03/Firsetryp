import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from shivu import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from shivu import pm_users as collection 

SUPPORT_GC = -1002059626060

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=GROUP_ID, 
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)})</a>", 
                                       parse_mode='HTML')
        

    # Check if bot is a member of the support group
    if not await context.bot.get_chat_member(SUPPORT_GC, context.bot.id):
        # Send a message to the user asking them to invite the bot to the support group
        await context.bot.send_message(chat_id=user_id, 
                                       text=f"Welcome! Please invite me to join our support group @dark_world_231 to start using the bot.")
        
        # Send another message with an invitation link to the support group
        invite_link = await context.bot.export_chat_invite_link(SUPPORT_CHAT)
        await context.bot.send_message(chat_id=user_id,
                                       text=f"You can invite me to the support group using this [invite link]({invite_link}).",
                                       parse_mode='markdown')
        return

    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***Heyyyy...***

***I am An Open Source Character Catcher Bot...​Add Me in Your group.. And I will send Random Characters After.. every 100 messages in Group... Use /guess to.. Collect that Characters in Your Collection.. and see Collection by using /Harem... So add in Your groups and Collect Your harem***
        """
        
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("HELP", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(PHOTO_URL)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(PHOTO_URL)
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("HELP", callback_data='help')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="🎴Alive!?... \n connect to me in PM For more information ",reply_markup=reply_markup )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***Help Section:***
    
***/guess: To Guess character (only works in group)***
***/fav: Add Your fav***
***/trade : To trade Characters***
***/gift: Give any Character from Your Collection to another user.. (only works in groups)***
***/collection: To see Your Collection***
***/topgroups : See Top Groups.. Ppl Guesses Most in that Groups***
***/top: Too See Top Users***
***/ctop : Your ChatTop***
***/changetime: Change Character appear time (only works in Groups)***
   """
        help_keyboard = [[InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***Hoyyyy...*** ✨

***I am An Open Source Character Catcher Bot..​Add Me in Your group.. And I will send Random Characters After.. every 100 messages in Group... Use /guess to.. Collect that Characters in Your Collection.. and see Collection by using /Harem... So add in Your groups and Collect Your harem***
        """

        
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("UPDATES", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("HELP", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')


application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
