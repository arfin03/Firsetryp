from telegraph import upload_file
from pyrogram import filters
from shivu import shivuu
from pyrogram.types import InputMediaPhoto
from pyrogram.enums import ParseMode


app = shivuu

@app.on_message(filters.command(["tgm" , "telegraph"]))
def ul(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("𝐌𝙰𝙺𝙴 𝐀 𝐋𝙸𝙽𝙺...")
        path = reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://telegra.ph" + x

        i.edit(f'Yᴏᴜʀ ʟɪɴᴋ sᴜᴄᴄᴇssғᴜʟ Gᴇɴ `{url}`')

########____________________________________________________________######

@app.on_message(filters.command(["graph" , "grf"]))
def ul(_, message):
    reply = message.reply_to_message
    if reply.media:
        i = message.reply("𝐌𝙰𝙺𝙴 𝐀 𝐋𝙸𝙽𝙺...")
        path = reply.download()
        fk = upload_file(path)
        for x in fk:
            url = "https://graph.org" + x

        i.edit(f'Yᴏᴜʀ ʟɪɴᴋ sᴜᴄᴄᴇssғᴜʟ Gᴇɴ `{url}`')

await message.reply_to_message(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
)
