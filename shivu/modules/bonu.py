from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
from shivu import user_collection, shivuu
# Initialize Pyrogram client
app = shivuu

# Bonus command handler
@app.on_message(filters.command("bonus10"))
async def bonus_command(_, update):
    user_id = update.from_user.id

    # Check if the user has already claimed the bonus this week
    user_data = user_collection.get(user_id, {})
    last_bonus_claim = user_data.get('last_bonus_claim')

    if last_bonus_claim:
        # Calculate the current week and last claimed week
        current_week = datetime.datetime.now().isocalendar()[1]
        last_claimed_week = last_bonus_claim.isocalendar()[1]

        if current_week == last_claimed_week:
            await update.reply_text("You have already claimed your bonus for this week.")
            return

    # Update user data with the current time
    user_data['last_bonus_claim'] = datetime.datetime.now()
    user_collection[user_id] = user_data

    # Add the bonus amount to the user's balance
    # For demonstration, let's assume the user's balance is stored in the user_data dictionary
    bonus_amount = 500
    user_data['balance'] = user_data.get('balance', 0) + bonus_amount

    # Inform the user that the bonus has been successfully claimed
    await update.reply_text("You have claimed your weekly bonus of 500 coins!")

# Start command handler (for demonstration purposes)
@app.on_message(filters.command("bonus"))
async def start_command(_, update):
    # Send a welcome message with the bonus button
    await update.reply_text("Claim your weekly bonus now.",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("Claim Bonus", callback_data="claim_bonus")]
                            ]))

# Bonus claim button handler
@app.on_callback_query(filters.regex(r'^claim_bonus$'))
async def claim_bonus(_, query):
    user_id = query.from_user.id
    user_data = user_collection.get(user_id, {})

    # Check if the user has already claimed the bonus this week
    last_bonus_claim = user_data.get('last_bonus_claim')
    if last_bonus_claim:
        current_week = datetime.datetime.now().isocalendar()[1]
        last_claimed_week = last_bonus_claim.isocalendar()[1]

        if current_week == last_claimed_week:
            await query.answer("You have already claimed your bonus for this week.")
            return

    # Update user data with the current time
    user_data['last_bonus_claim'] = datetime.datetime.now()
    user_collection[user_id] = user_data

    # Add the bonus amount to the user's balance
    # For demonstration, let's assume the user's balance is stored in the user_data dictionary
    bonus_amount = 500
    user_data['balance'] = user_data.get('balance', 0) + bonus_amount

    # Inform the user that the bonus has been successfully claimed
    await query.answer("You have successfully claimed your weekly bonus of 500 coins!")

    # Update the message to show that the bonus has been claimed
    await query.message.edit_reply_markup(reply_markup=None)

