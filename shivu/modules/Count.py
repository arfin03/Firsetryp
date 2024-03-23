from pyrogram import Client, filters
from shivu import db, collection, top_global_groups_collection, group_user_totals_collection, user_collection, user_totals_collection
import asyncio
import random
from shivu import shivuu as app
from shivu import sudo_users

DEV_LIST = [6402009857 , 6600178606 , 1374057577]

@app.on_message(filters.command(["gremove"]) & filters.user(DEV_LIST))
async def remove_character_all_users_command(client, message):
    try:
        # Check if a character ID is provided
        if len(message.command) < 2:
            await message.reply_text("Please provide a character ID.")
            return

        # Get the character ID
        character_id = str(message.command[1])

        # Get all users with collections
        users_with_collections_cursor = user_collection.find({})
        users_with_collections = await users_with_collections_cursor.to_list(length=None)

        # Initialize a count variable for the number of users' collections updated
        collections_updated_count = 0

        # Remove the character from each user's collection
        for user in users_with_collections:
            try:
                # Try removing the character from the user's collection
                await kill_character(user['id'], character_id)
                collections_updated_count += 1
            except Exception as e:
                print(f"Error removing character for user {user['id']}: {e}")

        # Send a message with the number of users' collections updated
        await message.reply_text(f"Success! Removed character with ID {character_id} from collections of {collections_updated_count} user(s).")

    except Exception as e:
        print(f"Error in remove_character_all_users_command: {e}")
        await message.reply_text("An error occurred while processing the command.")
