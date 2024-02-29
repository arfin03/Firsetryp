from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.error import Unauthorized

from shivu import application 

def token(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide a Telegram bot token.")
        return
    
    bot_token = context.args[0]
    
    try:
        bot = context.bot.set_token(bot_token)
        bot.get_me()
        update.message.reply_text("The token is valid.")
    except Unauthorized:
        update.message.reply_text("The token is invalid or the bot is unauthorized to use it.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")

# Add the command handler to your dispatcher
token_handler = CommandHandler('token', token)
application.add_handler(token_handler)
