import urllib.request
from pymongo import ReturnDocument

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from shivu import application, sudo_users, collection, db, user_collection, user_totals_collection, CHARA_CHANNEL_ID

rarity_coin_mapping = {
    "⚪ Common": 40,
    "🟣 Rare": 100,
    "🟡 Legendary": 80,
    "🟢 Medium": 60,
    "💮 Special edition": 180,
    "🔮 Limited Edition": 240
}


async def sell(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    args = context.args

    if len(args) != 1:
        await update.message.reply_text("Please provide the character ID to sell.")
        return

    character_id = args[0]

    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text("You have not guessed any characters yet.")
        return

    # Check if the character exists in the user's harem
    character_to_sell = next((c for c in user['characters'] if c['id'] == character_id), None)
    if not character_to_sell:
        await update.message.reply_text("This character does not exist in your harem.")
        return

    # Check if the character's rarity is in the mapping
    rarity = character_to_sell.get('rarity', 'Unknown')
    coins_awarded = rarity_coin_mapping.get(rarity, None)
    
    if coins_awarded is None:
        await update.message.reply_text(f"Cannot sell character {character_id}. Rarity '{rarity}' not found in mapping.")
        return

    # Deduct the character from the user's harem
    user['characters'].remove(character_to_sell)
    await user_collection.update_one({'id': user_id}, {'$set': {'characters': user['characters']}})

    # Award coins based on rarity
    if 'balance' in user:
        user['balance'] += coins_awarded
    else:
        user['balance'] = coins_awarded
    await user_collection.update_one({'id': user_id}, {'$set': {'balance': user['balance']}})
    await update.message.reply_text(f"Character {character_id} sold! You received {coins_awarded} coins.")

# Inside main(), add this line to register the /sell command handler
SELL_HANDLER = CommandHandler('sell', sell, block=False)
application.add_handler(SELL_HANDLER)
