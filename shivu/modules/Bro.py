from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext
from shivu import application

# Define the command callback function as async
async def set_pic(update: Update, context: CallbackContext) -> None:
    # Extract the image URL from the command arguments
    if len(context.args) != 1:
        await update.message.reply_text("Invalid command! Usage: /setpic <image_url>")
        return
    image_url = context.args[0]

    # Save the image URL to chat_data for later use
    context.chat_data['image_url'] = image_url

    await update.message.reply_text("Image URL has been set successfully!")

# Define the send_message function to use the set image URL
async def send_message(update: Update, context: CallbackContext) -> None:
    # Extract the message text from the command arguments
    message_text = ' '.join(context.args)

    # Check if image URL is set in chat_data
    image_url = context.chat_data.get('image_url')
    if not image_url:
        await update.message.reply_text("Please set an image URL first using /setpic <image_url>")
        return

    # Create the inline keyboard buttons
    keyboard = [
        [
            InlineKeyboardButton("🎀Aᴅᴅ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ🎀", url="http://t.me/Dark_waifu_Bot?startgroup=new")
        ],
        [
            InlineKeyboardButton("📢Sᴜᴘᴘᴏʀᴛ📢", url="https://t.me/dark_world_231"),
            InlineKeyboardButton("🔔Uᴘᴅᴀᴛᴇ🔔", url="https://t.me/SUKUNA_UPDATE_CHANNEL")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the image and buttons
    await update.message.reply_photo(
        photo=image_url,
        caption=message_text,
        reply_markup=reply_markup
    )

# Add the command handlers to the dispatcher
application.add_handler(CommandHandler("setpic", set_pic))
application.add_handler(CommandHandler("msg", send_message))
