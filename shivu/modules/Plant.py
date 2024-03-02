from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler
import pymongo
from datetime import datetime, timedelta

from suivu import application, user_collection 

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://harshmanjhi180:harsh2279@cluster0.z1pajuv.mongodb.net/?retryWrites=true&w=majority")
db = client["plant_game3"]
collection = db["user_plants"]

plant_image_urls = {
    1: "https://telegra.ph/file/8b017c909aca80620dd70.png",
    20: "https://telegra.ph/file/5c3b67113186e532effa1.jpg",
    40: "https://telegra.ph/file/5ae2de95199e349bc5a05.jpg",
    60: "https://telegra.ph/file/f9b1607ffe259b8aaac3d.png"
}

# Function to handle button click
async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    # Retrieve user's plant data from MongoDB
    user_data = collection.find_one({"user_id": user_id})

    if user_data:
        last_claim_time = user_data.get('last_claim_time')
        if last_claim_time and datetime.now() - last_claim_time < timedelta(days=1):
            await query.edit_message_text(text="You have already claimed your coins for today.")
        else:
            coins = calculate_coins(user_data['level'])
            collection.update_one({"user_id": user_id}, {"$set": {"last_claim_time": datetime.now()}, "$inc": {"coins": coins}}, upsert=True)
            await query.edit_message_text(text=f"🎉 You have claimed {coins} coins!")
    else:
        await query.edit_message_text(text="You don't have a plant.")

# Function to handle /myplant command
async def my_plant(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # Retrieve user's plant data from MongoDB
    user_data = collection.find_one({"user_id": user_id})

    if user_data:
        plant_level = user_data['level']
        user_code = user_data.get('user_code', "No code assigned")  # Get user code or default message
        plant_image_url = get_plant_image_url(plant_level)
        coins = user_data.get('coins', 0)
        message = f"🌱 Your plant, {user_name}, is currently at level {plant_level}. Keep growing it!\n\nYour unique code: {user_id}"

        # Create inline keyboard with a "Claim" button
        keyboard = [[InlineKeyboardButton("Claim Reward", callback_data='claim')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message with plant image, user's plant level, user's code, and the inline keyboard
        await update.message.reply_photo(photo=plant_image_url, caption=message, reply_markup=reply_markup)
    else:
        # If user doesn't have a plant, create one with initial level 1 and save to MongoDB
        new_plant = {"user_id": user_id, "level": 1}
        collection.insert_one(new_plant)
        plant_image_url = plant_image_urls[1]  # Default plant image for level 1
        message = f"🌱 Welcome, {user_name}! Your new plant has been planted. Keep nurturing it to help it grow!\n user code: {user_id}"

        # Send message with plant image, user's plant level, user's code
        await update.message.reply_photo(photo=plant_image_url, caption=message)

# Function to handle /code command
async def code(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Please provide a target user's ID.")
        return

    target_user_id = int(context.args[0])

    if target_user_id == user_id:
        await update.message.reply_text("You cannot use the /code command with your own user ID.")
        return

    # Check if the user has already used the code
    user_data = collection.find_one({"user_id": user_id})

    if user_data and user_data.get('code_used', False):
        await update.message.reply_text("You have already used your code.")
        return

    # Retrieve target user's plant data from MongoDB
    target_user_data = collection.find_one({"user_id": target_user_id})

    if not target_user_data:
        await update.message.reply_text("The specified user does not exist or does not have a plant yet.")
        return

    # Increase target user's plant level by 1 and update MongoDB
    collection.update_one({"user_id": target_user_id}, {"$inc": {"level": 1}}, upsert=True)
    updated_level = collection.find_one({"user_id": target_user_id})['level']

    # Calculate coins earned by the target user
    coins_earned = calculate_coins(updated_level)

    # Mark the user's code as used
    collection.update_one({"user_id": user_id}, {"$set": {"code_used": True}}, upsert=True)

    await update.message.reply_text(f"🌿 Congratulations! The plant belonging to user ID {target_user_id} has leveled up to level {updated_level}!")

# Function to handle /mycode command
async def my_code(update: Update, context: CallbackContext):
    user_id = update.effective_user.id  # Get the user's ID who triggered the command

    # Send the user's ID as a reply
    await update.message.reply_text(f"Your user ID is: {user_id}")

# Function to calculate coins earned based on plant level
def calculate_coins(level):
    return level * 100

# Function to get plant image URL based on level
def get_plant_image_url(level):
    for threshold in sorted(plant_image_urls.keys(), reverse=True):
        if level >= threshold:
            return plant_image_urls[threshold]
    return plant_image_urls[1]  # Default to level 1 image if no match


async def top_plant_levels(update: Update, context: CallbackContext):
    # Retrieve plant data for multiple users
    top_users_cursor = collection.find().sort("level", pymongo.DESCENDING).limit(10)
    
    top_users_info = []
    for idx, user_data in enumerate(top_users_cursor, start=1):
        # Get user object
        user = await context.bot.get_chat(user_data['user_id'])
        if user.first_name:
            full_name = user.first_name
            if user.last_name:
                full_name += " " + user.last_name
            user_link = f'<a href="tg://user?id={user.id}">{full_name}</a>'
            top_users_info.append(f"{user_link} - Level: {user_data['level']}")
    
    if top_users_info:
        message = "\n".join(top_users_info)
        pic = "https://telegra.ph/file/f466f1fdab10ab5a0fc11.jpg"
        await update.message.reply_photo(photo=pic, caption=f"Top 10 Users by Plant Level:\n\n{message}", parse_mode="HTML")
    else:
        await update.message.reply_text("No users found.")

# Add the /top command handler to your application
application.add_handler(CommandHandler("ptop", top_plant_levels))

# Add the /claim command handler to y
application.add_handler(CommandHandler("myplant", my_plant))
application.add_handler(CommandHandler("mycode", my_code))
application.add_handler(CommandHandler("code", code))
