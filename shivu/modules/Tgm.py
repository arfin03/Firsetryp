from telegraph import upload_file
from pyrogram import filters
from shivu import shivuu
from pyrogram.types import InputMediaPhoto
from pyrogram.enums import ParseMode

app = shivuu

@app.on_message(filters.command(["tgm", "telegraph"]))
async def telegraph_link(_, message):
    reply = message.reply_to_message
    if reply and reply.media:
        i = await message.reply_text("𝐌𝙰𝙺𝙴 𝐀 𝐋𝙸𝙽𝙺...")
        path = await reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://telegra.ph" + x
            await i.edit_text(f'Yᴏᴜʀ <a href="{url}">ʟɪɴᴋ</a> sᴜᴄᴄᴇssғᴜʟʟʏ Gᴇɴᴇʀᴀᴛᴇᴅ: <code>{url}</code>', parse_mode=ParseMode.HTML)

@app.on_message(filters.command(["graph", "grf"]))
async def graph_link(_, message):
    reply = message.reply_to_message
    if reply and reply.media:
        i = await message.reply_text("𝐌𝙰𝙺𝙴 𝐀 𝐋𝙸𝙽𝙺...")
        path = await reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://graph.org" + x
            await i.edit_text(f'Yᴏᴜʀ <a href="{url}">ʟɪɴᴋ</a> sᴜᴄᴄᴇssғᴜʟʟʏ Gᴇɴᴇʀᴀᴛᴇᴅ: <code>{url}</code>', parse_mode=ParseMode.HTML)

