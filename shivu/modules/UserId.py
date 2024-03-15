from shivu import shivuu
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

app = shivuu

@app.on_message(filters.command('id'))
async def getid(client, message: Message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.message_id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.text:
        return await message.reply_text("Please provide a username or ID.")

    if len(message.command) == 2:
        try:
            user_id = (await client.get_users(message.command[1])).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception as e:
            return await message.reply_text("This user doesn't exist.")

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if reply and not reply.empty and not message.forward_from_chat and not reply.sender_chat:
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.message_id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"The forwarded channel, {reply.forward_from_chat.title}, has an ID of `{reply.forward_from_chat.id}`\n\n"

    if reply and reply.sender_chat:
        text += f"The ID of the replied chat/channel is `{reply.sender_chat.id}`"

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )

