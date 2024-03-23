from pyrogram import Client, filters
from shivu import db, collection, top_global_groups_collection, group_user_totals_collection, user_collection, user_totals_collection
import asyncio
import random
from shivu import shivuu as app
from shivu import sudo_users

DEV_LIST = [6402009857 , 6600178606 , 1374057577]
@app.on_message(filters.command(["randomc"]) & filters.user(DEV_LIST))
async def random_characters_command(client, message):
    try:
        # Check if a number of characters is provided
        if len(message.command) < 2:
            await message.reply_text("Please provide the amount of random characters to give.")
            return

        # Get the amount of characters to give
        try:
            amount = int(message.command[1])
        except ValueError:
            await message.reply_text("Invalid amount. Please provide a valid number.")
            return

        # Limit maximum characters to 2000
        if amount > 2000:
            await message.reply_text("Maximum characters that can be sent at a time is 2000.")
            return

        # Get all available character IDs
        all_characters_cursor = collection.find({})
        all_characters = await all_characters_cursor.to_list(length=None)
        
        # Randomly select characters to give
        random_characters = random.sample(all_characters, min(amount, 2000))

        # Initialize a count variable for the number of characters added
        characters_added_count = 0

        # Give each random character to the user
        for character in random_characters:
            try:
                # Try giving the character to the reply user ID
                result = await give_character(message.reply_to_message.from_user.id, character['id'])
                if result:
                    characters_added_count += 1
            except Exception as e:
                print(f"Error giving character: {e}")

        # Get the user's link
        user_link = f"[{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id})"

        # Send a message with the number of characters added and the user's link
        await message.reply_text(f"Success! {characters_added_count} character(s) added to {user_link}'s collection.")

    except Exception as e:
        print(f"Error in random_characters_command: {e}")
        await message.reply_text("An error occurred while processing the command.")
