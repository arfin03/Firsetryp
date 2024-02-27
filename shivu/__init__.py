import logging  
import os
from pyrogram import Client 
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

from shivu.config import Development as Config


OWNER_ID = '6655070772'
sudo_users = ["6655070772", "6090374191", "6655070772", "5297949798", "6655070772", "6655070772"]
GROUP_ID = "-1002059626060"
TOKEN = "6721869429:AAFQUnBJLuicOoD8w-lknA4_s4fe1bYg6-U"
mongo_url = "mongodb+srv://Komi:Aarught5645@cluster0.8usl8ul.mongodb.net/?retryWrites=true&w=majority"
PHOTO_URL = ["https://telegra.ph/file/aa06eb4b312f456e1fd28.jpg", "https://telegra.ph/file/aa06eb4b312f456e1fd28.jpg"]
SUPPORT_CHAT = "dark_world_231"
UPDATE_CHAT = "SUKUNA_UPDATE_CHANNEL"
BOT_USERNAME = "Dark_waifu_Bot"
CHARA_CHANNEL_ID = "-1002059626060"
api_id = "28062766"
api_hash = "2087f7a333490600faeb42a9c0267406"



application = Application.builder().token(TOKEN).build()
shivuu = Client("Shivu", api_id, api_hash, bot_token=TOKEN)
lol = AsyncIOMotorClient(mongo_url)
db = lol['Character_catcher']
collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
