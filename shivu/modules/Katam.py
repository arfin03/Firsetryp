from telegram import Update
import asyncio
from telegram.ext import CommandHandler, CallbackContext
from shivu import user_collection, application 

OWNER_ID = 6867197197

async def katam(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /katam [user_id]")
        return
    
    user_id = int(context.args[0])

    await delete_user_data(user_id)
    await update.message.reply_text(f"Data associated with user ID {user_id} has been deleted.")

async def delete_user_data(user_id: int) -> None:
    # Delete user data from the database
    await user_collection.delete_many({'id': user_id})
    
application.add_handler(CommandHandler("katam", katam))

