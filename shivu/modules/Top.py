from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from urllib.parse import quote_plus
from Grabber import user_collection, application, image_urls
import random

async def top(update: Update, context: CallbackContext):
    # Retrieve users along with their character counts
    users = await user_collection.find().to_list(length=None)

    # Sort users by character counts in descending order
    top_users = sorted(users, key=lambda user: len(user.get('characters', [])), reverse=True)[:10]

    if top_users:
        # Randomly select an image URL
        image_url = random.choice(image_urls)

        # Generate the message
        message = "<b>Top 10 Users by Number of Characters:</b>\n\n"
        for idx, user in enumerate(top_users, start=1):
            character_count = len(user.get('characters', []))
            username = user.get('username', 'Unknown')
            user_link = f'<a href="tg://user?id={user["_id"]}">{username}</a>'
            message += f"{idx}. {user_link}: {character_count}\n"

        # Send the message along with the image
        await update.message.reply_photo(photo=image_url, caption=message, parse_mode='HTML')
    else:
        await update.message.reply_text("No users found.")

# Define the command handler for /top command
top_handler = CommandHandler('top', top)

# Add the command handler to the dispatcher
application.add_handler(top_handler)
