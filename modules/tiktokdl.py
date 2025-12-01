'''
import os
import uuid
import asyncio
import sys
import os

# Add the parent directory to Python path so we can import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from yt_dlp import YoutubeDL, DownloadError

# Import from the main app and other modules
from app import app, logger
from assest.fsub import FORCESUB

DOWNLOAD_DIR = "downloads"

tiktok_filter = filters.regex(r'https?://(?:www\.|m\.|vm\.|vt\.)?tiktok\.com/')

@app.on_message(filters.private & tiktok_filter)
async def tiktok_downloader(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Force subscribe check
    try:
        # Check if user is subscribed
        is_subscribed = await FORCESUB.check(client, message)
        if not is_subscribed:
            return  # Stop if user is not subscribed
    except Exception as e:
        logger.error(f"Force sub check error: {e}")
        await message.reply_text("❌ Error checking subscription status.")
        return

    status_msg = await message.reply_text("⏳ Processing... Downloading video.")
    final_file_path = None

    try:
        # Create downloads directory
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        unique_id = str(uuid.uuid4())
        save_path_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")

        # yt-dlp options
        ydl_opts = {
            'outtmpl': save_path_template,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
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
            await status_msg.edit_text("📤 Uploading to Telegram...")
            
            try:
                await message.reply_video(
                    video=final_file_path,
                    caption="✅ **Downloaded Successfully!**\n\n📹 **Via TikTok Downloader Bot**",
                    quote=True
                )
                await status_msg.edit_text("✅ Download completed!")
                
            except FloodWait as e:
                await status_msg.edit_text(f"⏳ Please wait {e.value} seconds due to flood limit")
                await asyncio.sleep(e.value)
                # Retry upload after flood wait
                await message.reply_video(
                    video=final_file_path,
                    caption="✅ **Downloaded Successfully!**\n\n📹 **Via TikTok Downloader Bot**",
                    quote=True
                )
                await status_msg.edit_text("✅ Download completed!")
                
        else:
            await status_msg.edit_text("❌ Error: File not found after download.")

    except DownloadError as e:
        error_msg = str(e).lower()
        if "private" in error_msg:
            await status_msg.edit_text("❌ This is a private TikTok video.")
        elif "not found" in error_msg:
            await status_msg.edit_text("❌ Video not found. Link may be invalid.")
        else:
            await status_msg.edit_text("❌ TikTok refused connection. Link might be invalid.")
        logger.error(f"DownloadError: {e}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_msg.edit_text(f"❌ Error: {str(e)}")
        
    finally:
        # Cleanup with delay
        await asyncio.sleep(2)
        try:
            await status_msg.delete()
        except:
            pass
            
        # Cleanup downloaded file
        if final_file_path and os.path.exists(final_file_path):
            try:
                os.remove(final_file_path)
            except Exception as cleanup_error:
                logger.error(f"Cleanup error: {cleanup_error}")
# Add callback handler for force sub check
@app.on_callback_query(filters.regex("check_force_sub"))
async def check_force_sub_callback(client, callback_query):
    """Handle the check again button for force subscription"""
    try:
        # Delete the previous message
        await callback_query.message.delete()
        
        # Check subscription again
        is_subscribed = await FORCESUB.check(client, callback_query.message)
        
        if is_subscribed:
            await callback_query.message.reply_text(
                "✅ **Thank you for joining!**\n\n"
                "You can now use the bot. Send me a TikTok URL to download.",
                quote=True
            )
            
    except Exception as e:
        logger.error(f"Force sub callback error: {e}")
        '''