from pyrogram import filters
from app import app, logger
from assest.fsub import FORCESUB

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
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

    await message.reply_text(
        "🤖 **TikTok Downloader Bot**\n\n"
        "Send me a TikTok URL and I'll download the video for you!\n\n"
        "**Supported URLs:**\n"
        "• https://www.tiktok.com/@username/video/123456789\n"
        "• https://vm.tiktok.com/ABC123/\n"
        "• https://vt.tiktok.com/XYZ789/"
    )

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
        else:
            await callback_query.message.reply_text(
                " **Your not joined our channel**\n\n"
                "plese join",
                quote=True

            )

            
    except Exception as e:
        logger.error(f"Force sub callback error: {e}")