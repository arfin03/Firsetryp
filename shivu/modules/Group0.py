from telegram.ext import Updater, MessageHandler
from telegram import Update
from telegram.ext import filters
import logging

from shivu import application 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# ID of the logging group
logging_group_id = -1002059626060

def welcome_new_member(update: Update, context):
    # Extract relevant information from the update
    new_members = update.message.new_chat_members
    added_by = update.message.from_user
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title

    # Send a welcome message to the group
    welcome_message = f"Hello! I'm {context.bot.username}. Thank you for adding me to {chat_title}."
    context.bot.send_message(chat_id, welcome_message)

    # Log information about the group and who added the bot in the logging group
    log_message = f"New group: {chat_title} (ID: {chat_id}). Added by: {added_by.first_name} (ID: {added_by.id})."
    context.bot.send_message(logging_group_id, log_message)



    # Register handler for new chat members
    application.add_handler(MessageHandler(filters.status_update.new_chat_members, welcome_new_member))

    
  
