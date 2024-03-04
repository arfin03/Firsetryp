from telegram.ext import MessageHandler, filters
import logging

from shivu import application 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define message handler
async def handle_promotion(update, context):
    promoting_user = update.message.from_user
    if update.message.reply_to_message:
        promoted_user = update.message.reply_to_message.from_user
        await update.message.reply_text(f"{promoting_user.username} promoted {promoted_user.username}.")

# Add message handler within an asynchronous function
async def add_handlers():
    await application.add_handler(MessageHandler(filters.Filters.reply & filters.Filters.text & ~filters.Filters.user(username="dark_waifu_bot"), handle_promotion))

# Call the asynchronous function
await add_handlers()
