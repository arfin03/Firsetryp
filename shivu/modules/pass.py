from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, user_collection  # Assuming Grabber is your module/package

async def create_password(update: Update, context: CallbackContext):
    # Extract the user ID
    user_id = update.effective_user.id
    
    # Check if the command is sent via private message
    if update.effective_chat.type != 'private':
        await update.message.reply_text("This command can only be used in private messages.")
        return
    
    # Extract the password from the command
    try:
        password = context.args[0]
    except IndexError:
        await update.message.reply_text("Please provide a password.")
        return
    
    # Save the password to the database
    await user_collection.update_one({'id': user_id}, {'$set': {'password': password}}, upsert=True)
    await update.message.reply_text("Your password has been set successfully.")

async def my_password(update: Update, context: CallbackContext):
    # Extract the user ID
    user_id = update.effective_user.id
    
    # Check if the command is sent via private message
    if update.effective_chat.type != 'private':
        await update.message.reply_text("This command can only be used in private messages.")
        return
    
    # Retrieve the user's password from the database
    user_data = await user_collection.find_one({'id': user_id})
    password = user_data.get('password') if user_data else None
    
    if password:
        await update.message.reply_text(f"Your password is: {password}")
    else:
        await update.message.reply_text("You haven't set a password yet.")

# Define handlers
create_password_handler = CommandHandler('create_password', create_password)
my_password_handler = CommandHandler('my_password', my_password)

# Add handlers to the dispatcher
application.add_handler(create_password_handler)
application.add_handler(my_password_handler)
