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
sudo_users = ["6655070772", "6090374191", "6655070772", "5297949798", "6655070772", "5955023340"]
GROUP_ID = "-1002059626060"
TOKEN = "6786511875:AAGGM-y9P4N3hEjFS6Aj_rYuYt7RAPObVdY"
mongo_url = "mongodb+srv://Komi:Aarught5645@cluster0.8usl8ul.mongodb.net/?retryWrites=true&w=majority"
PHOTO_URL = ["https://telegra.ph/file/aa06eb4b312f456e1fd28.jpg", "https://telegra.ph/file/aa06eb4b312f456e1fd28.jpg"]
SUPPORT_CHAT = "dark_world_231"
UPDATE_CHAT = "SUKUNA_UPDATE_CHANNEL"
BOT_USERNAME = "Dark_waifu_Bot"
CHARA_CHANNEL_ID = "-1002059626060"
api_id = "28062766"
api_hash = "2087f7a333490600faeb42a9c0267406"

image_urls = [
    "https://telegra.ph/file/405ee89d4a708d161a41b.jpg",
    "https://telegra.ph/file/a80fae6bc9a09d4bc8cb4.jpg",
    "https://telegra.ph/file/002d4caee6e74370848c0.jpg",
    "https://telegra.ph/file/48b536de686bb20e3068b.jpg",
    "https://telegra.ph/file/a986e00083dae9ad32269.jpg",
    "https://telegra.ph/file/ba318dc0749b495b434b3.jpg",
    "https://telegra.ph/file/badce7884ce06e92cedb5.jpg"
]

application = Application.builder().token(TOKEN).build()
shivuu = Client("Shivu", api_id, api_hash, bot_token=TOKEN)
lol = AsyncIOMotorClient(mongo_url)
db = lol['Character_catcher']
collection = db['anime_characters']
user_totals_collection = db['user_totals_2']
user_collection = db["user_collection_2"]
group_user_totals_collection = db['group_user_total_2']
top_global_groups_collection = db['top_global_groups_2']
pm_users = db['total_pm_users']
