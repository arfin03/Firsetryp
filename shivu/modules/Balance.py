from telegram.ext import CommandHandler, MessageHandler 
from shivu import application, user_collection
from telegram import Update
from telegram.ext import CallbackContext

async def balance(update, context):
    user_id = update.effective_user.id

    # Retrieve user balance from the database (replace this with your actual database query)
    user_balance = await user_collection.find_one({'id': user_id}, projection={'balance': 1})

    if user_balance:
        balance_amount = user_balance.get('balance', 0)
        balance_message = f"Yᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ʙᴀʟᴀɴᴄᴇ ɪs: 💵{balance_amount} coins."
    else:
        balance_message = "Unable to retrieve your balance."

    await update.message.reply_text(balance_message)

async def pay(update, context):
    sender_id = update.effective_user.id

    # Check if the command was a reply
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to use /pay.")
        return

    # Extract the recipient's user ID
    recipient_id = update.message.reply_to_message.from_user.id

    # Parse the amount from the command
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid amount. Usage: /pay <amount>")
        return

    # Check if the amount is positive
    if amount <= 0:
        await update.message.reply_text("Amount must be a positive number.")
        return

    # Check if the sender has enough balance
    sender_balance = await user_collection.find_one({'id': sender_id}, projection={'balance': 1})
    if not sender_balance or sender_balance.get('balance', 0) < amount:
        await update.message.reply_text("Insufficient balance to make the payment.")
        return

    # Perform the payment
    await user_collection.update_one({'id': sender_id}, {'$inc': {'balance': -amount}})
    await user_collection.update_one({'id': recipient_id}, {'$inc': {'balance': amount}})

    # Fetch updated sender balance
    updated_sender_balance = await user_collection.find_one({'id': sender_id}, projection={'balance': 1})

    # Reply with payment success and updated balance
    await update.message.reply_text(f"💵 Payment successful! You paid {amount} coins to {update.message.reply_to_message.from_user.username}. "
                                    f"Your current balance is: 💵{updated_sender_balance.get('balance', 0)} coins.")

    # Trigger /balance command for the sender
    await context.bot.send_message(chat_id=update.message.chat_id, text='/balance', reply_to_message_id=update.message.message_id)


    await context.bot.send_message(chat_id=update.message.chat_id, text='/balance', reply_to_message_id=update.message.message_id)

async def mtop(update, context):
    # Retrieve the top 10 users with the highest balance
    top_users = await user_collection.find({}, projection={'id': 1, 'first_name': 1, 'last_name': 1, 'balance': 1}).sort('balance', -1).limit(10).to_list(10)

    # Create a message with the top users
    top_users_message = "Top 10 Users with Highest Balance:\n"
    for i, user in enumerate(top_users, start=1):
        first_name = user.get('first_name', 'Unknown')
        last_name = user.get('last_name', '')
        user_id = user.get('id', 'Unknown')

        # Concatenate first_name and last_name if last_name is available
        full_name = f"{first_name} {last_name}" if last_name else first_name

        top_users_message += f"{i}. <a href='tg://user?id={user_id}'>{full_name}</a>, \n Balance: 💵{user.get('balance', 0)} coins\n\n"

    # Send the photo and include the top_users_message in the caption
    photo_path = 'https://telegra.ph/file/8fce79d744297133b79b6.jpg'
    await update.message.reply_photo(photo=photo_path, caption=top_users_message, parse_mode='HTML')



from datetime import datetime, timedelta

async def daily_reward(update, context):
    user_id = update.effective_user.id

    # Check if the user already claimed the daily reward today
    user_data = await user_collection.find_one({'id': user_id}, projection={'last_daily_reward': 1, 'balance': 1})

    if user_data:
        last_claimed_date = user_data.get('last_daily_reward')

        if last_claimed_date and last_claimed_date.date() == datetime.utcnow().date():
            await update.message.reply_text("You've already claimed your daily reward today. Come back tomorrow!")
            return

    # Grant the daily reward
    await user_collection.update_one(
        {'id': user_id},
        {'$inc': {'balance': 20}, '$set': {'last_daily_reward': datetime.utcnow()}}
    )

    await update.message.reply_text("Congratulations! You've claimed your daily reward of 20 coins.")

# Add the command handler to your application
application.add_handler(CommandHandler("dailyreward", daily_reward, block=False))

application.add_handler(CommandHandler("balance", balance, block=False))
application.add_handler(CommandHandler("pay", pay, block=False))
application.add_handler(CommandHandler("mtop", mtop, block=False))
