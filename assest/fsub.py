from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from app import logger

async def check_force_sub(client: Client, message: Message):
    """Check if user is subscribed to the required channel"""
    try:
        # Check if user is in the channel
        user_status = await client.get_chat_member(Config.REQUIRED_CHANNEL, message.from_user.id)
        
        # If user is not member or left the channel
        if user_status.status in ["left", "kicked", "banned"]:
            join_url = f"https://t.me/{Config.REQUIRED_CHANNEL.replace('@', '')}"
            
            # Create inline keyboard with join button
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url=join_url)],
                [InlineKeyboardButton("🔄 Check Again", callback_data="check_force_sub")]
            ])
            
            await message.reply_text(
                f"🛑 **Access Denied!**\n\n"
                f"You must join our channel to use this bot.\n"
                f"Please join: **{Config.REQUIRED_CHANNEL}**",
                reply_markup=keyboard,
                disable_web_page_preview=True,
                quote=True
            )
            return False
        return True
        
    except UserNotParticipant:
        join_url = f"https://t.me/{Config.REQUIRED_CHANNEL.replace('@', '')}"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=join_url)],
            [InlineKeyboardButton("🔄 Check Again", callback_data="check_force_sub")]
        ])
        
        await message.reply_text(
            f"🛑 **Access Denied!**\n\n"
            f"You must join our channel to use this bot.\n"
            f"Please join: **{Config.REQUIRED_CHANNEL}**",
            reply_markup=keyboard,
            disable_web_page_preview=True,
            quote=True
        )
        return False
        
    except Exception as e:
        logger.error(f"Subscription check error: {e}")
        await message.reply_text(
            "❌ An error occurred during subscription check.\n"
            "Please try again later.",
            quote=True
        )
        return False

# Create a global FORCESUB object that can be used
class ForceSub:
    def __init__(self):
        self.check = check_force_sub

FORCESUB = ForceSub()