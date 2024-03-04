import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from motor import motor_asyncio

from shivu import application 

# MongoDB connection
client = motor_asyncio.AsyncIOMotorClient('mongodb+srv://harshmanjhi180:harsh2279@cluster0.z1pajuv.mongodb.net/?retryWrites=true&w=majority')
db = client['karma']  # Replace 'your_database_name' with your actual database name
karma_collection = db['karma']

# Function to get karma points for a user
async def get_karma(user_id):
    user_karma = await karma_collection.find_one({'user_id': user_id})
    return user_karma['karma'] if user_karma else 0

# Function to update karma points for a user
async def update_karma(user_id, points):
    await karma_collection.update_one({'user_id': user_id}, {'$inc': {'karma': points}}, upsert=True)

# Function to handle messages and update karma points
async def message_handler(update: Update, context: CallbackContext):
    positive_messages = ["thanks", "nice", "+", "+1"]  # Add more positive messages as needed
    text = update.message.text.lower()
    user_id = update.message.from_user.id
    if any(message in text for message in positive_messages):
        await update_karma(user_id, 1)

# Function to handle the /karma command
async def karma_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    karma = await get_karma(user_id)
    await update.message.reply_text(f'Your karma points: {karma}')


    application.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
    application.add_handler(CommandHandler("karma", karma_command))
    
if __nane__ == '__KARMA__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
  
