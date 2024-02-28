from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from shivu import collection, user_collection, application

async def info_character(update, context):
    # Parse character ID from the command
    character_id = context.args[0] if context.args else None

    if not character_id:
        await update.message.reply_text("Please provide a character ID.")
        return

    # Retrieve information about the character
    character_info = await collection.find_one({'id': character_id})

    if not character_info:
        await update.message.reply_text("Character not found.")
        return

    # Retrieve users who have the character in their harem
    users_with_character = await user_collection.find({'characters.id': character_id}).to_list(length=None)

    if not users_with_character:
        await update.message.reply_text("No user has this character in their harem.")
        return

    # Create inline keyboard with buttons for each user
    keyboard = []
    for user in users_with_character:
        user_id = user['id']
        username = user.get('username', 'Unknown')
        button_text = f"{username}'s Profile"
        callback_data = f"profile:{user_id}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Character Info: {character_info['name']}", reply_markup=reply_markup)

async def profile_callback(update, context):
    query = update.callback_query
    data = query.data

    if data.startswith("profile:"):
        user_id = int(data.split(":")[1])

        # You can implement the logic to open the profile here
        await query.answer("Opening profile...")
        # Add your logic to open the user's profile

# Add handlers to the application
application.add_handler(CommandHandler("info2", info_character))
application.add_handler(CallbackQueryHandler(profile_callback))
  
