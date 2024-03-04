from telegram.ext import Updater, MessageHandler, filters
import logging

from shivu import application 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define message handler
def handle_promotion(update, context):
    promoting_user = update.message.from_user
    if update.message.reply_to_message:
        promoted_user = update.message.reply_to_message.from_user
        update.message.reply_text(f"{promoting_user.username} promoted {promoted_user.username}.")

# Add message handler
application.add_handler(MessageHandler(Filters.reply & Filters.text & ~Filters.user(username="YourBotUsername"), handle_promotion))
