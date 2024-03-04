from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from shivu import application 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Define command handlers
def promote(update, context):
    promoted_user = update.message.reply_to_message.from_user
    promoting_user = update.message.from_user
    update.message.reply_text(f"{promoted_user.username} was promoted by {promoting_user.username}.")

def demote(update, context):
    demoted_user = update.message.reply_to_message.from_user
    demoting_user = update.message.from_user
    update.message.reply_text(f"{demoted_user.username} was demoted by {demoting_user.username}.")

def profile(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Username: {query.data}")


    # Add command handlers
    application.add_handler(CommandHandler("promote", promote))
    application.add_handler(CommandHandler("demote", demote))
