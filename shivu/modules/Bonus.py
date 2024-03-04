from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Grabber import application, user_collection
from datetime import datetime, timedelta
from pyrogram import filters

app = shivuu


@app.on_callback_query(filters.create(lambda _, __, query: query.data == 'claim_bonus'))
async def button(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    # Check if the user has claimed the bonus this week
    user_data = await user_collection.find_one({'id': user_id}, projection={'last_bonus_claim': 1})

    if user_data and user_data.get('last_bonus_claim') is not None:
        last_claimed_date = user_data['last_bonus_claim']
        current_date = datetime.utcnow()

        # Calculate the difference in days since the last claim
        days_since_last_claim = (current_date - last_claimed_date).days

        if days_since_last_claim < 7:
            # User has already claimed the bonus this week
            await query.answer("You have already claimed the bonus this week. You can claim again next week.")
            return

    # Check if the user is already a member of the support channel
    is_member = await context.bot.get_chat_member("@SUKUNA_UPDATE_CHANNEL", user_id)

    if is_member.status == 'left':
        # User is not a member, send them a message to join the support channel
        await query.answer("To claim the bonus, please join our support channel @SUKUNA_UPDATE_CHANNEL.")
    elif is_member.status == 'kicked':
        # User was kicked from the channel, inform them to contact support
        await query.answer("You were kicked from our support channel. Please contact support for assistance.")
    else:
        # User is already a member, grant the bonus
        await user_collection.update_one({'id': user_id}, {'$inc': {'balance': 200}, '$set': {'last_bonus_claim': datetime.utcnow()}})
        await query.answer()
        await query.message.reply_text("Congratulations! You've been awarded 200 coins as a weekly bonus.")

# To add the command handler, you can use the same function as before:
@app.on_message(filters.command("bonus"))
async def bonus(update, context):
    user_id = update.message.from_user.id
    keyboard = [[InlineKeyboardButton("Claim Bonus", callback_data='claim_bonus')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("You're eligible for the weekly bonus! Click the button below to claim it.", reply_markup=reply_markup)
