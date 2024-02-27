import urllib.request
from pymongo import ReturnDocument

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from Grabber import application, sudo_users, collection, db, CHARA_CHANNEL_ID

async def total_characters(update: Update, context: CallbackContext) -> None:
    try:
        # Count the total number of characters in the collection
        total_count = await collection.count_documents({})
        await update.message.reply_text(f"Total characters: {total_count}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Register the command handler for the /total command
TOTAL_HANDLER = CommandHandler('total', total_characters, block=False)
application.add_handler(TOTAL_HANDLER)
