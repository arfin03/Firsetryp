from telegram.ext import MessageHandler, filters
from telegram import Update
import threading
import asyncio
import logging
from shivu import application

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# ID of the logging group
logging_group_id = -1002059626060

async def welcome_new_member(update: Update, context):
    # Extract relevant information from the update
    new_members = update.message.new_chat_members
    added_by = update.message.from_user
    chat_id = update.message.chat.id
    chat_title = update.message.chat.title

    # Send a welcome message to the group
    welcome_message = f"Hello! I'm {context.bot.username}. Thank you for adding me to {chat_title}."
    await context.bot.send_message(chat_id, welcome_message)

    # Log information about the group and who added the bot in the logging group
    log_message = f"New group: {chat_title} (ID: {chat_id}). Added by: {added_by.first_name} (ID: {added_by.id})."
    await context.bot.send_message(logging_group_id, log_message)

def run_async_function(update, context):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(welcome_new_member(update, context))
    loop.close()

def synchronous_handler(update, context):
    thread = threading.Thread(target=run_async_function, args=(update, context))
    thread.start()

application.add_handler(MessageHandler(filters.StatusUpdate.new_chat_members, synchronous_handler))
