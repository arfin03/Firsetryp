from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import logging

# Assuming you have necessary functions defined elsewhere
from Grabber import user_collection, application

# Initialize active_users dictionary
active_users = {}

async def back_1_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    rarities = {character['rarity'] for character in active_users[user_id]['characters']}
    
    buttons = [
        InlineKeyboardButton(rarity, callback_data=f'rarity2_{rarity}')
        for rarity in rarities
    ]
    
    button_chunks = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    reply_markup = InlineKeyboardMarkup(button_chunks)
    
    await query.edit_message_media(
        media=InputMediaPhoto("https://telegra.ph/file/036135b624b6a7d1babee.jpg"),
        reply_markup=reply_markup
    )

async def rarity2_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    parts = data.split('_')
    if len(parts) < 2:
        await query.answer("Invalid callback data format.", show_alert=True)
        return

    action = parts[0]
    rarity = parts[1]

    user_id = query.from_user.id

    if user_id not in active_users:
        await query.answer("You are not authorized to interact with these buttons.")
        return

    page = int(parts[2]) if len(parts) == 3 else 0

    user = await user_collection.find_one({'id': user_id})

    if not user or 'characters' not in user:
        await query.answer("Your list is empty.", show_alert=True)
        return

    filtered_characters = [
        character for character in user['characters']
        if character.get('rarity') == rarity
    ]

    chunk_size = 10
    total_pages = (len(filtered_characters) + chunk_size - 1) // chunk_size

    if action == 'next':
        page = min(page + 1, total_pages - 1)
    elif action == 'prev':
        page = max(page - 1, 0)

    current_characters = filtered_characters[page * chunk_size: (page + 1) * chunk_size]

    message = '\n'.join([f"🆔 ID: {char['id']}\n🎗️ Rarity: {char['rarity']}\n👁️‍🗨️ Character: {char['name']}\n\n " for char in current_characters])

    if total_pages > 1:
        keyboard = [
            [InlineKeyboardButton("Next", callback_data=f"next_{rarity}_{page+1}")],
            [InlineKeyboardButton("Previous", callback_data=f"prev_{rarity}_{page-1}")],
            [InlineKeyboardButton("Back", callback_data="back_1")]  # Back button added here
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        # If there's only one page, no need for pagination buttons
        keyboard = [
            [InlineKeyboardButton("Back", callback_data="back_1")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(caption=message, reply_markup=reply_markup)

async def hmode(update: Update, context: CallbackContext) -> None:
    # Assuming user_id can be fetched from update object
    user_id = update.effective_user.id

    # Fetch user data from database
    user = await user_collection.find_one({'id': user_id})
    
    if not user or 'characters' not in user:
        await update.message.reply_text("Your list is empty.")
        return
    
    # Extract unique rarities from user's characters
    rarities = {character['rarity'] for character in user['characters']}
    
    # Generate buttons for each rarity
    buttons = [
        InlineKeyboardButton(rarity, callback_data=f'rarity2_{rarity}')
        for rarity in rarities
    ]
    
    # Split buttons into chunks of 2 buttons per row
    button_chunks = [buttons[i:i+2] for i in range(0, len(buttons), 2)]

# Create reply markup with buttons
    reply_markup = InlineKeyboardMarkup(button_chunks)
    
    # Store user as active user with relevant session information
    active_users[user_id] = {'mode': 'hmode', 'characters': user.get('characters', [])}  # You can add more session information as needed
    
    # Send image with rarity buttons
    await update.message.reply_photo(
        photo="https://telegra.ph/file/036135b624b6a7d1babee.jpg",
        reply_markup=reply_markup
    )

# Add command handler for /hmode command
application.add_handler(CommandHandler("hmode", hmode))

# Add callback handler for rarity buttons
application.add_handler(CallbackQueryHandler(rarity2_callback, pattern=r'^rarity2_'))

# Add callback handler for back button
application.add_handler(CallbackQueryHandler(back_1_callback, pattern=r'^back_1$'))
