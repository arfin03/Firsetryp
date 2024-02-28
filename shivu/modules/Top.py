from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import user_collection, application, image_urls
import random
from urllib.parse import quote_plus

async def top(update: Update, context: CallbackContext):
    users = await user_collection.find().to_list(length=None)

    top_users = sorted(users, key=lambda user: len(user.get('characters', [])), reverse=True)[:10]

    if top_users:
        image_url = random.choice(image_urls)

        message = "<b>Top 10 Users by Number of Characters:</b>\n\n"
        for idx, user in enumerate(top_users, start=1):
            character_count = len(user.get('characters', []))
            first_name = user.get('first_name', 'Unknown')
            userid = user.get('id')
            user_link = f"https://t.me/{userid}" if username else None
            if user_link:
                message += f"{idx}. <a href='{user_link}'>{first_name}</a>: {character_count}\n"
            else:
                message += f"{idx}. {first_name}: {character_count}\n"
        
        await update.message.reply_photo(photo=image_url, caption=message, parse_mode='HTML')
    else:
        await update.message.reply_text("No users found.")

# Define the command handler for /top command
top_handler = CommandHandler('top', top)

# Add the command handler to the dispatcher
application.add_handler(top_handler)
