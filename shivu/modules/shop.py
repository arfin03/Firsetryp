from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import logging

from shivu import collection, user_collection, application, shivuu
import logging


app = shivuu


user_collection = {}  # Placeholder for user_collection

# Shop command handler
@app.on_message(filters.command("shop"))
async def shop_command(_, update):
    rarity_3_characters = await collection.find({'rarity': "💸 Premium Edition"}).to_list(length=7)

    if not rarity_3_characters:
        await update.reply_text("No legendary characters available in the shop.")
        return

    first_character = rarity_3_characters[0]
    reply_markup = get_inline_keyboard(first_character)
    message = await _.send_photo(
        chat_id=update.chat.id,
        photo=first_character['img_url'],
        caption=f"🪙Welcome to the Shop! Choose a character to buy:\n\n"
                f"🏮Anime Name: {first_character['anime']}\n"
                f"🎴Character Name: {first_character['name']}\n"
                f"🌀Rarity: {first_character['rarity']}\n"
                f"🎗️Character ID: {first_character['id']}\n"
                f"💸Coin Price: {first_character['coin_price']}",
        reply_markup=reply_markup
    )

    user_data = {'message_id': message.message_id, 'current_index': 0, 'user_id': update.from_user.id}
    await _.chat.set_data('shop_message', user_data)
    
# Next character handler
@app.on_callback_query(filters.regex(r'shop_next_\d+'))
async def next_character(_, query):
    user_data = await _.chat.get_data('shop_message')
    if user_data is None or user_data['user_id'] != query.from_user.id:
        return  # Do nothing if user_data is not found or the user is different

    current_index = user_data.get('current_index', 0)
    rarity_3_characters = await collection.find({'rarity': "💸 Premium Edition"}).to_list(length=700)

    if current_index + 1 < len(rarity_3_characters):
        # Increment the current_index to get the next character
        current_index += 1
        next_character = rarity_3_characters[current_index]
        reply_markup = get_inline_keyboard(next_character, current_index)

        # Create the caption with details of the next character
        caption = f"🪙Welcome to the Shop! Choose a character to buy:\n\n" \
                  f"🏮Anime Name: {next_character['anime']}\n" \
                  f"🎴Character Name: {next_character['name']}\n" \
                  f"🌀Rarity: {next_character['rarity']}\n" \
                  f"🎗️Character ID: {next_character['id']}\n" \
                  f"💸Coin Price: {next_character['coin_price']}"

        # Update the existing message with details of the next character
        await query.message.edit_media(
            media=InputMediaPhoto(media=next_character['img_url'], caption=caption),
            reply_markup=reply_markup
        )

        # Update the current_index in user_data
        user_data['current_index'] = current_index
        await _.chat.set_data('shop_message', user_data)

# Close shop handler
@app.on_callback_query(filters.regex(r'shop:closed'))
async def close_shop(_, query):
    user_data = await _.chat.get_data('shop_message')
    if user_data is None:
        return  # Do nothing if user_data is not found

    message_id = user_data.get('message_id')
    if message_id:
        try:
            await query.message.delete()
        except Exception as e:
            logging.error(f"Error deleting message: {e}")

    await _.chat.delete_data('shop_message')

# Helper function to generate inline keyboard
def get_inline_keyboard(character, current_index=0, total_count=7):
    keyboard = []

    if current_index == 0:
        # For the first character, display "CLOSED" and "NEXT" buttons
        keyboard.append([
            InlineKeyboardButton("❎𝘾𝙇𝙊𝙎𝙀𝘿❎", callback_data="shop:closed"),
            InlineKeyboardButton("➡️𝙉𝙀𝙓𝙏➡️", callback_data=f"shop_next_{current_index + 1}")
        ])
    else:
        # For all other characters, display both "BACK" and "NEXT" buttons
        keyboard.append([
            InlineKeyboardButton(" ⬅️𝘽𝘼𝘾𝙆⬅️", callback_data="shop:back"),
            InlineKeyboardButton("➡️𝙉𝙀𝙓𝙏➡️", callback_data=f"shop_next_{current_index + 1}")
        ])

    # Add "Buy" button for all characters
    keyboard.append([InlineKeyboardButton("✅𝘽𝙐𝙔✅", callback_data=f"buy:{character['id']}")])

    return InlineKeyboardMarkup(keyboard)

# Buy character handler
@app.on_callback_query(filters.regex(r'^buy:\d+$'))
async def buy_character(_, query):
    character_id_str = query.data.split(":")[1]  # Extract character ID as a string
    character_id = int(character_id_str)

    character = await collection.find_one({'id': character_id_str})  # Use the string ID in the query

    if not character:
        await query.answer("Character not found.")
        return

    user_id = query.from_user.id

    user_data = await user_collection.find_one({'id': user_id}, projection={'balance': 1, 'characters': 1})

    if not user_data:
        await query.answer("Failed to retrieve user data.")
        return

    coin_price = int(character.get('coin_price', 0))  # Convert coin_price to integer

    if user_data.get('balance', 0) < coin_price:
        await query.answer("Insufficient balance to buy this character.")
        return

    await user_collection.update_one({'id': user_id}, {'$inc': {'balance': -coin_price}})
    await user_collection.update_one({'id': user_id}, {'$push': {'characters': character}})

    await query.answer(f"You have successfully bought {character['name']} for {coin_price} coins!")
