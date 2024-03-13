import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext, CommandHandler
from pyrogram import Client, filters

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

async def shop(update: Update, context: CallbackContext) -> None:
    rarity_3_characters = await collection.find({'rarity': "💸 Premium Edition"}).to_list(length=7)

    if not rarity_3_characters:
        await update.message.reply_text("No legendary characters available in the shop.")
        return
        
    first_character = rarity_3_characters[0]
    reply_markup = get_inline_keyboard(first_character)
    message = await context.bot.send_photo(
        update.message.chat_id,
        photo=first_character['img_url'],
        caption=create_caption(first_character),
        reply_markup=reply_markup
    )
    
    context.user_data['shop_message'] = {'message_id': message.message_id, 'current_index': 0, 'user_id': update.effective_user.id}

@shivuu.on_callback_query(filters.regex('^shop:next:\d+$'))
async def next_character(callback_query):
    query = callback_query
    data = query.data
    user_id = query.from_user.id
    user_data = query.message.context.user_data.get(user_id)
    if user_data is None:
        return  # Do nothing if user_data is not found
    current_index = user_data.get('current_index', 0)
    rarity_3_characters = await collection.find({'rarity': "💸 Premium Edition"}).to_list(length=7)
    if current_index + 1 < len(rarity_3_characters):
        current_index += 1
        next_character = rarity_3_characters[current_index]
        reply_markup = get_inline_keyboard(next_character, current_index)
        caption = create_caption(next_character)
        await query.message.edit_media(
            media=InputMediaPhoto(media=next_character['img_url'], caption=caption),
            reply_markup=reply_markup
        )
        user_data['current_index'] = current_index

@shivuu.on_callback_query(filters.regex('^shop:back$'))
async def previous_character(callback_query):
    query = callback_query
    data = query.data
    user_id = query.from_user.id
    user_data = query.message.context.user_data.get(user_id)
    if user_data is None:
        return  # Do nothing if user_data is not found
    current_index = user_data.get('current_index', 0)
    rarity_3_characters = await collection.find({'rarity': "💸 Premium Edition"}).to_list(length=7)
    if current_index - 1 >= 0:
        current_index -= 1
        previous_character = rarity_3_characters[current_index]
        reply_markup = get_inline_keyboard(previous_character, current_index)
        caption = create_caption(previous_character)
        await query.message.edit_media(
            media=InputMediaPhoto(media=previous_character['img_url'], caption=caption),
            reply_markup=reply_markup
        )
        user_data['current_index'] = current_index

@shivuu.on_callback_query(filters.regex('^buy:\d+$'))
async def buy_character(callback_query):
    query = callback_query
    data = query.data
    user_id = query.from_user.id
    user_data = query.message.context.user_data.get(user_id)
    if user_data is None:
        return
    character_id_str = data.split(":")[1]  # Extract character ID as a string
    character = await collection.find_one({'id': character_id_str})  # Use the string ID in the query
    if not character:
        await query.answer("Character not found.")
        return
    coin_price = int(character.get('coin_price', 0))  # Convert coin_price to integer
    if user_data.get('balance', 0) < coin_price:
        await query.answer("Insufficient balance to buy this character.")
        return
    await user_collection.update_one({'id': user_id}, {'$inc': {'balance': -coin_price}})
    await user_collection.update_one({'id': user_id}, {'$push': {'characters': character}})
    await query.answer(f"You have successfully bought {character['name']} for {coin_price} coins!")

@shivuu.on_callback_query(filters.regex('^shop:closed$'))
async def close_shop(callback_query):
    query = callback_query
    user_id = query.from_user.id
    user_data = query.message.context.user_data.get(user_id)
    if user_data is None:
        return
    message_id = user_data.get('message_id')
    if message_id:
        try:
            await query.message.delete()
        except Exception as e:
            logging.error(f"Error deleting message: {e}")
    del query.message.context.user_data[user_id]

def create_caption(character):
    return f"🪙Welcome to the Shop! Choose a character to buy:\n\n" \
           f"🏮Anime Name: {character['anime']}\n" \
           f"🎴Character Name: {character['name']}\n" \
           f"🌀Rarity: {character['rarity']}\n" \
           f"🎗️Character ID: {character['id']}\n" \
           f"💸Coin Price: {character['coin_price']}"

def get_inline_keyboard(character, current_index=0, total_count=7):
    keyboard = []

    if current_index == 0:
        # For the first character, display "CLOSED" and "NEXT" buttons
        keyboard.append([
            InlineKeyboardButton("❎CLOSED❎", callback_data="shop:closed"),
            InlineKeyboardButton("➡️NEXT➡️", callback_data=f"shop:next:{current_index + 1}")
        ])
    elif current_index == total_count - 1:
        # For the last character, display "BACK" and "CLOSED" buttons
        keyboard.append([
            InlineKeyboardButton("⬅️BACK⬅️", callback_data="shop:back"),
            InlineKeyboardButton("❎CLOSED❎", callback_data="shop:closed")
        ])
    else:
        # For all other characters, display both "BACK" and "NEXT" buttons
        keyboard.append([
            InlineKeyboardButton("⬅️BACK⬅️", callback_data="shop:back"),
            InlineKeyboardButton("➡️NEXT➡️", callback_data=f"shop:next:{current_index + 1}")
        ])

    # Add "Buy" button for all characters
    keyboard.append([InlineKeyboardButton("✅BUY✅", callback_data=f"buy:{character['id']}")])

    return InlineKeyboardMarkup(keyboard)


application.add_handler(CommandHandler("shop", shop, block=False))
