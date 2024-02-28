from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from urllib.parse import quote_plus
from shivu import user_collection, application, image_urls
import random

async def top(update: Update, context: CallbackContext):
    # Retrieve users along with their character counts
    users = await user_collection.find().to_list(length=None)

    # Sort users by character counts in descending order
    top_users = sorted(users, key=lambda user: len(user.get('characters', [])), reverse=True)[:10]

    if top_users:
        # Generate the message
        message = "<b>Top 10 Users by Number of Characters:</b>\n\n"
        for idx, user in enumerate(top_users, start=1):
            character_count = len(user.get('characters', []))
            
            # Fetch user profile details from the database based on ID (user["_id"])
            # Replace this line with your actual code to fetch user profile details
            user_profile = await fetch_user_profile(user["_id"])
            
            # If user profile is found, get the username
            if user_profile:
                username = user_profile.get('username', 'Unknown')
                user_link = f'<a href="tg://user?id={user["_id"]}">{username}</a>'
            else:
                # If user profile is not found, use a placeholder
                user_link = "Unknown User"
            
            message += f"{idx}. {user_link}: {character_count}\n"

        # Send the message
        await update.message.reply_text(message, parse_mode='HTML')
    else:
        await update.message.reply_text("No users found.")

# Define the command handler for /top command
top_handler = CommandHandler('top', top)

# Add the command handler to the dispatcher
application.add_handler(top_handler)
