class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
OWNER_ID = '6995317382'
sudo_users = ["6995317382", "6090374191", "6655070772", "5297949798", "6655070772", "6655070772"]
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


    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
