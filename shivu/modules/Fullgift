from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from shivu import user_collection, shivuu

pending_gifts = {}

# Owner ID
OWNER_ID = 6867197197

@shivuu.on_message(filters.command("fullgift"))
async def fullgift(client, message):
    if len(message.command) != 3:
        await message.reply_text("Invalid command format! Use /fullgift [sender_id] [receiver_id]")
        return

    sender_id = int(message.command[1])
    receiver_id = int(message.command[2])

    sender = await user_collection.find_one({'id': sender_id})
    receiver = await user_collection.find_one({'id': receiver_id})

    if not sender or not receiver:
        await message.reply_text("Invalid sender or receiver user ID!")
        return

    # Check if the user is the owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("You are not authorized to use this command!")
        return

    if not sender['characters']:
        await message.reply_text("Sender doesn't have any characters to gift!")
        return

    pending_gifts[(sender_id, receiver_id)] = {
        'characters': sender['characters'],
        'receiver_id': receiver_id
    }

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Gift", callback_data="confirm_fullgift")],
            [InlineKeyboardButton("Cancel Gift", callback_data="cancel_fullgift")]
        ]
    )

    await message.reply_text(f"Do you really want to gift all characters to user with ID {receiver_id}?", reply_markup=keyboard)


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_fullgift", "cancel_fullgift"]))
async def on_callback_query_fullgift(client, callback_query):
    sender_id = callback_query.from_user.id

    for (sender_id, receiver_id), gift in pending_gifts.items():
        if sender_id == sender_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_fullgift":
        sender = await user_collection.find_one({'id': sender_id})
        receiver_id = gift['receiver_id']

        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': []}})

        await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': {'$each': gift['characters']}}})

        del pending_gifts[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"You have successfully gifted all your characters to user with ID {receiver_id}!")

