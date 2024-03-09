from telegram import Update, ChatMember
from telegram.ext import CommandHandler, CallbackContext
from pymongo import MongoClient
from shivu import application

# MongoDB connection
client = MongoClient("mongodb+srv://harshmanjhi180:harsh2279@cluster0.z1pajuv.mongodb.net/?retryWrites=true&w=majority")
db = client["image_database"]
collection = db["images"]

# Channel ID and Username
CHANNEL_ID = -1002114813114
CHANNEL_USERNAME = "SUKUNA_UPDATE_CHANNEL"

async def check_membership(update: Update, context: CallbackContext) -> bool:
    user_id = update.effective_user.id
    chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
    if chat_member.status in ['member', 'administrator']:
        return True
    else:
        # Check if user is already joined the channel but not an active member
        user = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if user.is_member():
            return True
        else:
            return False


# Function to handle the /up command
async def upload(update: Update, context: CallbackContext):
    # Extracting arguments from the command
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Please use the command in the format /up <img_url> <id>")
        return

    img_url = args[0]
    img_id = args[1]

    # Inserting image URL and ID into MongoDB
    result = await collection.insert_one({"id": img_id, "url": img_url})
    await update.message.reply_text("Image uploaded successfully.")

# Function to handle the /down command
async def download(update: Update, context: CallbackContext):
    if not await check_membership(update, context):
        await update.message.reply_text(f"You need to be a member of the channel to download images. Join the channel here: @{CHANNEL_USERNAME}")
        return

    # Extracting the id from the command
    img_id = context.args[0]

    # Retrieving image URL from MongoDB
    img_data = await collection.find_one({"id": img_id})
    if img_data:
        img_url = img_data["url"]
        await update.message.reply_photo(photo=img_url)
    else:
        await update.message.reply_text("Image not found.")

# Adding command handlers
application.add_handler(CommandHandler("down", download))
application.add_handler(CommandHandler("up", upload))
