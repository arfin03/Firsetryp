from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler
import pymongo
from datetime import datetime, timedelta
from pyrogram import filters


from shivu import application, user_collection, shivuu

GROUP_ID = -1002059626060

# Function to handle /bonus command
async def bonus(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Check if user has claimed the bonus within the last week
    user_data = await user_collection.find_one({"id": user_id})
    if user_data:
        last_claim_time = user_data.get('last_claim_time')
        if last_claim_time and datetime.now() - last_claim_time < timedelta(days=7):
            await update.message.reply_text("You have already claimed your bonus this week. Please try again next week.")
            return

    try:
        # Check if user is a member of the group
        user_support_group = await context.bot.get_chat_member(GROUP_ID, user_id)
        if user_support_group.status == "member" or user_support_group.status == "administrator":
            # Provide a button to claim the bonus
            keyboard = [[InlineKeyboardButton("Claim Bonus", callback_data='claim_bonus')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("You are already a member of the support group! Click the button below to claim your bonus.", reply_markup=reply_markup)
        else:
            # Prompt the user to join the support group
            await update.message.reply_text("You need to join the support group to claim the bonus. Join here: https://t.me/dark_world_231")
    except Unauthorized:
        await update.message.reply_text("You need to join the support group to claim the bonus. Join here: https://t.me/dark_world_231")
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text("There was an error processing your request. Please try again later.")


# Function to handle button click for claiming bonus
@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data == "claim_bonus"))
async def claim_bonus_button(client, callback_query):
    user_id = callback_query.from_user.id

    # Check if user has claimed the bonus within the last week
    user_data = await user_collection.find_one({"id": user_id})
    if user_data:
        last_claim_time = user_data.get('last_claim_time')
        if last_claim_time and datetime.now() - last_claim_time < timedelta(days=7):
            await callback_query.message.reply_text("You have already claimed your bonus this week. Please try again next week.")
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
        
    await callback_query.message.reply_text("Congratulations! You received a bonus of 400 coins for joining the support group!")

    # Close the button after claiming the bonus
    await callback_query.answer()

application.add_handler(CommandHandler("bonus", bonus))
