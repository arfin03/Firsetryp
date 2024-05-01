from telegram.ext import CommandHandler
from shivu import application, user_collection

OWNER = 6995317382  # Replace with the actual owner's user ID

async def add(update, context):
    # Check if the user is the owner
    if update.effective_user.id != OWNER:
        await update.message.reply_text('You are not authorized to use this command.')
        return

    # Parse the user ID and amount from the command
    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid format. Usage: /add <user_id> <amount>")
        return

    # Update the user's balance with the provided amount
    await user_collection.update_one({'id': user_id}, {'$inc': {'balance': amount}})

    # Fetch the updated user balance
    user = await user_collection.find_one({'id': user_id}, projection={'balance': 1})
    updated_balance = user.get('balance', 0)

    # Reply with the success message and updated balance
    await update.message.reply_text(f"💰 {amount} coins added to user {user_id}. Updated balance: 💵{updated_balance} coins.")

# Add the command handler to your application
application.add_handler(CommandHandler("add", add, block=False))
