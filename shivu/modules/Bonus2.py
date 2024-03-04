from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler
import pymongo
from datetime import datetime, timedelta
from pyrogram import filters


from shivu import application, user_collection, shivuu


# Function to handle /bonus command
async def bonus(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    # Check if user has joined the support group
    user_support_group = await update.effective_chat.get_member("dark_world_231")
    if user_support_group.status == "member" or user_support_group.status == "administrator":
        # Provide a button to claim the bonus
        keyboard = [[InlineKeyboardButton("Claim Bonus", callback_data='claim_bonus')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("You are already a member of the support group! Click the button below to claim your bonus.", reply_markup=reply_markup)
    else:
        # Prompt the user to join the support group
        await update.message.reply_text("You need to join the support group to claim the bonus. Join here: https://t.me/dark_world_231")

# Function to handle button click for claiming bonus
@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data == "claim_bonus"))
async def claim_bonus_button(client, callback_query):
    user_id = callback_query.from_user.id

    # Check if user has joined the support group
    user_support_group = await callback_query.from_user.get_chat_member("dark_world_231")
    if user_support_group.status == "member" or user_support_group.status == "administrator":
        # Give bonus coins to the user
        bonus_coins = 200
        user_balance_data = await user_collection.find_one({"id": user_id})
        if user_balance_data:
            await user_collection.update_one(
                {"id": user_id},
                {"$inc": {"balance": bonus_coins}}
            )
        else:
            await user_collection.insert_one({"id": user_id, "balance": bonus_coins})
        
        await callback_query.message.reply_text("Congratulations! You received a bonus of 200 coins for joining the support group!")
    else:
        await callback_query.message.reply_text("It seems you left the support group. Please join the group and try again.")

    # Close the button after claiming the bonus
    await callback_query.answer()

# Add the /bonus command handler to your application
application.add_handler(CommandHandler("bonus", bonus))
  
