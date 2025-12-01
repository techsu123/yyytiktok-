import os
import logging
from pyrogram import Client, filters

from config import Config

# ==========================================
# LOGGING & SETUP
# ==========================================

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the Pyrogram Client
app = Client(
    "tiktok_bot_session",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="modules")  # This will auto-load modules from modules folder
)

# ==========================================
# MAKE APP & LOGGER AVAILABLE GLOBALLY
# ==========================================

# These will be imported by other modules
from app import app, logger

# ==========================================
# START COMMAND (in main app.py)
# ==========================================



# ==========================================
# RUN THE BOT
# ==========================================
if __name__ == "__main__":
    print("🤖 Bot is starting...")
    print("📁 Loading modules from 'modules' folder...")
    app.run()