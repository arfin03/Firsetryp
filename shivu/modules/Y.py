from telegram.ext import MessageHandler, Filters
import logging

from shivu import application 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define message handler
async def handle_promotion(update, context):
    promoting_user = update.message.from_user
    await update.message.reply_text(f"{promoting_user.username} promoted someone.")

# Add message handler
await application.add_handler(MessageHandler(handle_promotion, ~Filters.update.edited_message))
