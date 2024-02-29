from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from shivu import application 

async def token(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a Telegram bot token.")
        return
    
    bot_token = context.args[0]
    
    try:
        bot = context.bot.set_token(bot_token)
        await bot.get_me()
        await update.message.reply_text("The token is valid.")
    except Exception as e:
        error_message = str(e)
        if "unauthorized" in error_message.lower():
            await update.message.reply_text("The token is invalid or the bot is unauthorized to use it.")
        else:
            await update.message.reply_text(f"An error occurred: {error_message}")

# Add the command handler to your dispatcher
token_handler = CommandHandler('token', token)
application.add_handler(token_handler)

