import os
import uuid
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from yt_dlp import YoutubeDL, DownloadError

# ==========================================
# CONFIGURATION
# ==========================================
API_ID = 38729067 
API_HASH = "3c37feee078c641e6b9bab21a118fbb4" 
REQUIRED_CHANNEL = "@lazoxx"
BOT_TOKEN = "5751521169:AAEzb-BXgFc6cpteurCgoCy6g2n0TeYi8Y8"
DOWNLOAD_DIR = "downloads"

# ==========================================
# LOGGING & SETUP
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Pyrogram Client
app = Client(
    "tiktok_bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ==========================================
# BOT LOGIC
# ==========================================


tiktok_filter = filters.regex(r'https?://(?:www\.|m\.|vm\.|vt\.)?tiktok\.com/')

@app.on_message(filters.private & tiktok_filter)
async def tiktok_downloader(client: Client, message: Message):
    try:
        await client.get_chat_member(REQUIRED_CHANNEL, message.from_user.id)
    except UserNotParticipant:
        join_url = f"https://t.me/{REQUIRED_CHANNEL.replace('@', '')}"
        await message.reply_text(
            f"🛑 **Access Denied!**\n\n"
            f"You must be a **subscriber** of our channel to download videos.\n"
            f"Please join: [Our Channel]({join_url})",
            disable_web_page_preview=True,
            quote=True
         )
        return
    except Exception as e:
        logger.error(f"Subscription check error: {e}")
        await message.reply_text("❌ An error occurred during the subscription check. Make sure the bot is an **admin** in the channel.")
        return
    status_msg = await message.reply_text("⏳ Processing... Downloading video.")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    unique_id = str(uuid.uuid4())
    save_path_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")
    final_file_path = None

    try:
        ydl_opts = {
            'outtmpl': save_path_template,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        # Download using yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            
            if 'requested_downloads' in info:
                final_file_path = info['requested_downloads'][0]['filepath']
            else:
                final_file_path = ydl.prepare_filename(info)

        # Upload to Telegram
        if final_file_path and os.path.exists(final_file_path):
            await message.reply_video(
                video=final_file_path,
                caption="✅ Here is your video!",
                quote=True
            )
        else:
            await status_msg.edit("❌ Error: File not found after download.")

    except DownloadError:
        await status_msg.edit("❌ TikTok refused connection. Link might be invalid.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit(f"❌ Error: {e}")
    finally:
        # Cleanup: Delete the status message and the file
        await status_msg.delete()
        if final_file_path and os.path.exists(final_file_path):
            os.remove(final_file_path)

# ==========================================
# RUN THE BOT
# ==========================================
if __name__ == "__main__":
    print("Bot is running with Pyrogram...")
    app.run()
