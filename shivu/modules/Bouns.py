from telegram.ext import CommandHandler, MessageHandler 
from shivu import application, user_collection
from telegram import Update
from telegram.ext import CallbackContext

from datetime import datetime, timedelta

async def bonus(update, context):
    user_id = update.effective_user.id

    # Check if the user has claimed the bonus this week
    user_data = await user_collection.find_one({'id': user_id}, projection={'last_bonus_claim': 1})

    if user_data and user_data.get('last_bonus_claim') is not None:
        last_claimed_date = user_data['last_bonus_claim']
        current_date = datetime.utcnow()

        # Calculate the difference in days since the last claim
        days_since_last_claim = (current_date - last_claimed_date).days

        if days_since_last_claim < 7:
            # User has already claimed the bonus this week
            await update.message.reply_text("You have already claimed the bonus this week. You can claim again next week.")
            return

    # Check if the user is already a member of the support channel
    is_member = await context.bot.get_chat_member("@SUKUNA_UPDATE_CHANNEL", user_id)

    if is_member.status == 'left':
        # User is not a member, send them a message to join the support channel
        await update.message.reply_text("To claim the bonus, please join our support channel @SUKUNA_UPDATE_CHANNEL.")
    elif is_member.status == 'kicked':
        # User was kicked from the channel, inform them to contact support
        await update.message.reply_text("You were kicked from our support channel. Please contact support for assistance.")
    else:
        # User is already a member, grant the bonus
        await user_collection.update_one({'id': user_id}, {'$inc': {'balance': 200}, '$set': {'last_bonus_claim': datetime.utcnow()}})
        await update.message.reply_text("Congratulations! You've been awarded 200 coins as a weekly bonus.")

# Add the command handler to your application
application.add_handler(CommandHandler("bonus", bonus, block=False))
