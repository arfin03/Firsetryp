from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from shivu import user_collection, shivuu


@shivuu.on_message(filters.command("fullgift"))
async def fullgift(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("You need to reply to a user's message to gift all characters!")
        return

    receiver_id = message.reply_to_message.from_user.id
    receiver_username = message.reply_to_message.from_user.username
    receiver_first_name = message.reply_to_message.from_user.first_name

    if sender_id == receiver_id:
        await message.reply_text("You can't gift characters to yourself!")
        return

    sender = await user_collection.find_one({'id': sender_id})

    if not sender['characters']:
        await message.reply_text("You don't have any characters to gift!")
        return

    pending_gifts[(sender_id, receiver_id)] = {
        'characters': sender['characters'],
        'receiver_username': receiver_username,
        'receiver_first_name': receiver_first_name
    }

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Gift", callback_data="confirm_fullgift")],
            [InlineKeyboardButton("Cancel Gift", callback_data="cancel_fullgift")]
        ]
    )

    await message.reply_text(f"Do you really want to gift all your characters to {message.reply_to_message.from_user.mention}?", reply_markup=keyboard)


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_fullgift", "cancel_fullgift"]))
async def on_callback_query_fullgift(client, callback_query):
    sender_id = callback_query.from_user.id

    for (_sender_id, receiver_id), gift in pending_gifts.items():
        if _sender_id == sender_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_fullgift":
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': []}})

        if receiver:
            await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': {'$each': gift['characters']}}})
        else:
            await user_collection.insert_one({
                'id': receiver_id,
                'username': gift['receiver_username'],
                'first_name': gift['receiver_first_name'],
                'characters': gift['characters'],
            })

        del pending_gifts[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"You have successfully gifted all your characters to [{gift['receiver_first_name']}](tg://user?id={receiver_id})!")
      
