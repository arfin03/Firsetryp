import uuid  # for generating unique IDs
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
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
        return False


# Function to handle the /up command
# Function to handle the /up command
async def upload(update: Update, context: CallbackContext):
    # Extracting arguments from the command
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Please use the command in the format /up <img_url>")
        return

    img_url = args[0]
    img_id = str(uuid.uuid4())  # Generate a unique ID

    # Inserting image URL and ID into MongoDB
    collection.insert_one({"id": img_id, "url": img_url})
    await update.message.reply_text(f"Image uploaded successfully. ID: {img_id}")

# Function to handle the /down command
async def download(update: Update, context: CallbackContext):
    if not await check_membership(update, context):
        await update.message.reply_text(f"You need to be a member of the channel to download images. Join the channel here: @{CHANNEL_USERNAME}")
        return

    # Check if arguments are provided
    if not context.args:
        await update.message.reply_text("Please provide the ID of the image you want to download.")
        return

    # Extracting the id from the command
    img_id = context.args[0]

    # Retrieving image data from MongoDB
    img_data = collection.find_one({"id": img_id})
    if img_data:
        img_url = img_data["url"]
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=img_url)
    else:
        await update.message.reply_text("Image not found.")


# Add handlers to the application
application.add_handler(CommandHandler("down", download))
application.add_handler(CommandHandler("up", upload))

