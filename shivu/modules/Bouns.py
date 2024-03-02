from telegram.ext import CommandHandler, Updater, CallbackContext, InlineKeyboardMarkup, InlineKeyboardButton

from shivu import application, user_collection
from telegram import Update
from datetime import datetime, timedelta

async def bonus(update: Update, context: CallbackContext):
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
        # User is already a member, prompt them to confirm claiming the bonus

        keyboard = InlineKeyboardMarkup(row_width=1)
        claim_button = InlineKeyboardButton(text="Claim Bonus", callback_data="claim_bonus")
        keyboard.add(claim_button)

        await update.message.reply_text(
            "Are you sure you want to claim your weekly bonus of 200 coins?",
            reply_markup=keyboard
        )

# Define a callback handler for the claim button
def claim_bonus_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    # Perform claim logic here (similar to existing bonus function)
    # ...

    # Reply to the user after processing
    query.answer("Bonus claimed successfully!")

application.add_handler(CommandHandler("bonus", bonus, block=False))

# Add the callback handler for the claim button
application.add_handler(CallbackQueryHandler(claim_bonus_callback))
