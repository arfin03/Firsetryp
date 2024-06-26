from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
import threading
import asyncio
import logging
import random
from html import escape
from itertools import groupby
import math

from shivu import collection, user_collection, application


# ID of the logging group
logging_group_id = -1002059626060

# Dictionary mapping rarity to emojis
RARITY_EMOJIS = {
    '⚪ Common': '⚪',
    '🟡 Legendary': '🟡',
    '🟢 Medium': '🟢',
    '🟣 Rare': '🟣',
    '💮 Special edition': '💮',
    '🔮 Limited Edition': '🔮',
    '💸 Premium Edition': '💸',
}

async def harem(update: Update, context: CallbackContext, page=0) -> None:
    user_id = update.effective_user.id

    user = await user_collection.find_one({'id': user_id})
    if not user:
        if update.message:
            await update.message.reply_text('You Have Not Guessed any Characters Yet..')
        else:
            await update.callback_query.edit_message_text('You Have Not Guessed any Characters Yet..')
        return

    characters = sorted(user['characters'], key=lambda x: (x['anime'], x['id']))

    character_counts = {k: len(list(v)) for k, v in groupby(characters, key=lambda x: x['id'])}

    unique_characters = list({character['id']: character for character in characters}.values())

    total_pages = math.ceil(len(unique_characters) / 15)

    if page < 0 or page >= total_pages:
        page = 0

    harem_message = f"<b>{escape(update.effective_user.first_name)}'s Harem - Page {page+1}/{total_pages}</b>\n"

    current_characters = unique_characters[page*15:(page+1)*15]

    current_grouped_characters = {k: list(v) for k, v in groupby(current_characters, key=lambda x: x['anime'])}

    for anime, characters in current_grouped_characters.items():
        harem_message += f'\n<b>{anime} {len(characters)}/{await collection.count_documents({"anime": anime})}</b>\n'

        for character in characters:
            character_id = character['id']
            db_character = await collection.find_one({'id': character_id})

            if db_character:
                rarity = db_character.get('rarity', 'Unknown Rarity')
                count = character_counts[character_id]
                # Replace rarity text with emoji
                rarity_emoji = RARITY_EMOJIS.get(rarity, '❓')
                harem_message += f'ID : {character_id}\nRARITY : [{rarity_emoji}]\nCHARACTER : {character["name"]} ×{count}\n'
            else:
                # Handle the case when character information is not found in the database
                count = character_counts[character_id]
                harem_message += f'{character_id} (Unknown Rarity) {character["name"]} ×{count}\n'

    total_count = len(user['characters'])

    keyboard = [[InlineKeyboardButton(f"See Collection ({total_count})", switch_inline_query_current_chat=f"collection.{user_id}")]]

    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"harem:{page-1}:{user_id}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"harem:{page+1}:{user_id}"))
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)

    if 'favorites' in user and user['favorites']:
        fav_character_id = user['favorites'][0]
        fav_character = next((c for c in user['characters'] if c['id'] == fav_character_id), None)

        if fav_character and 'img_url' in fav_character and fav_character['img_url']:
            if update.message:
                await update.message.reply_photo(photo=fav_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
            elif update.callback_query and update.callback_query.message:
                if update.callback_query.message.caption != harem_message:
                    await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
            else:
                # Handle the case where neither update.message nor update.callback_query.message is available
                pass
        else:
            if update.message:
                await update.message.reply_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
            elif update.callback_query and update.callback_query.message:
                if update.callback_query.message.text != harem_message:
                    await update.callback_query.edit_message_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
            else:
                # Handle the case where neither update.message nor update.callback_query.message is available
                pass
    else:
        if user['characters']:
            random_character = random.choice(user['characters'])

            if 'img_url' in random_character and random_character['img_url']:
                if update.message:
                    await update.message.reply_photo(photo=random_character['img_url'], parse_mode='HTML', caption=harem_message, reply_markup=reply_markup)
                elif update.callback_query and update.callback_query.message:
                    if update.callback_query.message.caption != harem_message:
                        await update.callback_query.edit_message_caption(caption=harem_message, reply_markup=reply_markup, parse_mode='HTML')
                else:
                    # Handle the case where neither update.message nor update.callback_query.message is available
                    pass
            else:
                if update.message:
                    await update.message.reply_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
                elif update.callback_query and update.callback_query.message:
                    if update.callback_query.message.text != harem_message:
                        await update.callback_query.edit_message_text(harem_message, parse_mode='HTML', reply_markup=reply_markup)
                else:
                    # Handle the case where neither update.message nor update.callback_query.message is available
                    pass
        else:
            if update.message:
                await update.message.reply_text("Your List is Empty :)")

async def harem_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    _, page, user_id = data.split(':')

    page = int(page)
    user_id = int(user_id)

    if query.from_user.id != user_id:
        await query.answer("It's Not Your Harem", show_alert=True)
        return

    await harem(update, context, page)

application.add_handler(CommandHandler(["harem", "collection"], harem, block=False))
harem_handler = CallbackQueryHandler(harem_callback, pattern='^harem', block=False)
application.add_handler(harem_handler)
