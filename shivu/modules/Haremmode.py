from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

# Assuming you have necessary functions defined elsewhere
from shivu import user_collection, shivuu

# Initialize active_users dictionary
active_users = {}

# Initialize your Pyrogram client
app = shivuu

@app.on_message(filters.command("hmode"))
async def hmode(client, message):
    user_id = message.from_user.id
    user = await user_collection.find_one({'id': user_id})
    
    if not user or 'characters' not in user:
        await message.reply_text("Your list is empty.")
        return
    
    rarities = {character['rarity'] for character in user['characters']}
    
    buttons = [
        [InlineKeyboardButton(rarity, callback_data=f'rarity2_{rarity}')]
        for rarity in rarities
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    active_users[user_id] = {'mode': 'hmode', 'characters': user.get('characters', [])}
    
    await message.reply_photo(
        photo="https://telegra.ph/file/036135b624b6a7d1babee.jpg",
        reply_markup=reply_markup
    )

@app.on_callback_query(filters.regex('^rarity2_'))
async def rarity2_callback(client, callback_query):
    query = callback_query
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

    keyboard = []

    if total_pages > 1:
        keyboard.append([InlineKeyboardButton("Next", callback_data=f"next_{rarity}_{page+1}")])
        keyboard.append([InlineKeyboardButton("Previous", callback_data=f"prev_{rarity}_{page-1}")])
    else:
        keyboard.append([InlineKeyboardButton("Back", callback_data="back_1")])

    reply_markup = InlineKeyboardMarkup(keyboard)


        query.edit_message_caption(caption=message, reply_markup=reply_markup)


@app.on_callback_query(filters.regex('^(next|prev)_'))
async def next_or_back_callback(client, callback_query):
    query = callback_query
    data = query.data

    parts = data.split('_')
    action = parts[0]
    rarity = parts[1]
    page = int(parts[2])

    if user_id not in active_users:
        await query.answer("You are not authorized to interact with these buttons.")
        return

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

    keyboard = []

    if total_pages > 1:
        keyboard.append([InlineKeyboardButton("Next", callback_data=f"next_{rarity}_{page+1}")])
        keyboard.append([InlineKeyboardButton("Previous", callback_data=f"prev_{rarity}_{page-1}")])
    else:
        keyboard.append([InlineKeyboardButton("Back", callback_data="back_1")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_caption(caption=message, reply_markup=reply_markup)

@app.on_callback_query(filters.regex('^back_1$'))
async def back_1_callback(client, callback_query):
    query = callback_query
    user_id = query.from_user.id

    rarities = {character['rarity'] for character in active_users[user_id]['characters']}
    
    buttons = [
        [InlineKeyboardButton(rarity, callback_data=f'rarity2_{rarity}')]
        for rarity in rarities
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await query.edit_message_media(
        media=InputMediaPhoto("https://telegra.ph/file/036135b624b6a7d1babee.jpg"),
        reply_markup=reply_markup
    )
