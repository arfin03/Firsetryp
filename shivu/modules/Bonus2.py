from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from datetime import datetime, timedelta
from pyrogram import filters

from shivu import application, user_collection, shivuu

GROUP_ID = -1002059626060
SUPPORT_GROUP_LINK = "https://t.me/dark_world_231"

async def bonus(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Check if the user is a member of the support group
    user_support_group = await context.bot.get_chat_member(GROUP_ID, user_id)

    if user_support_group.status == "left":
        # User is not a member, prompt them to join the support group
        await update.message.reply_text("To claim the bonus, please join our support group: {}".format(SUPPORT_GROUP_LINK))
        return

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

    # Provide a button to claim the bonus
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Claim Bonus", callback_data='claim_bonus')]])
    await update.message.reply_text("You can claim your bonus by clicking the button below.", reply_markup=keyboard)

    await callback_query.message.delete()

# Function to handle button click for claiming bonus
@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data == "claim_bonus"))
async def claim_bonus_button(client, callback_query):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name  # Get the user's first name

    # Check if user has claimed the bonus within the last week
    user_data = await user_collection.find_one({"id": user_id})
    if user_data:
        last_claim_time = user_data.get('last_claim_time')
        if last_claim_time and datetime.now() - last_claim_time < timedelta(days=7):
            await callback_query.message.reply_text(f"{user_name}, you have already claimed your bonus this week. Please try again next week.")
            return


    # Give bonus coins to the user
    bonus_coins = 400
    user_balance_data = await user_collection.find_one({"id": user_id})
    if user_balance_data:
        await user_collection.update_one(
            {"id": user_id},
            {"$inc": {"balance": bonus_coins}, "$set": {"last_claim_time": datetime.now()}}
        )
    else:
        await user_collection.insert_one({"id": user_id, "balance": bonus_coins, "last_claim_time": datetime.now()})
        
    # Send a message to the user with their bonus and name
    await callback_query.message.reply_text(f"Congratulations ! You received a bonus of {bonus_coins} coins for joining the support group!")

    # Close the button after claiming the bonus
    await callback_query.answer()

# Add the /bonus command handler
application.add_handler(CommandHandler("bonus", bonus))
