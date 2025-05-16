from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from services.youtube import YouTubeService
from services.user_manager import UserManager
import os

async def handle_quality_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, video_id, quality = query.data.split("_")
    video_url = f"https://youtube.com/watch?v={video_id}"
    user_id = query.from_user.id

    if not (UserManager.is_admin(user_id) or UserManager.is_subscribed(user_id)):
        await query.edit_message_text("🔒 Subscribe to download")
        return

    await query.edit_message_text(f"⏳ Downloading {quality}...")

    try:
        file_path = await YouTubeService.download_video(video_url, quality, update, context)
        if not file_path:
            return

        chat_id = query.message.chat_id
        if quality == "audio":
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=open(file_path, "rb"),
                caption=f"🎵 Downloaded by @{context.bot.username}"
            )
        else:
            await context.bot.send_video(
                chat_id=chat_id,
                video=open(file_path, "rb"),
                caption=f"🎥 {quality} - @{context.bot.username}"
            )
        
        os.remove(file_path)
    except Exception as e:
        await query.edit_message_text(f"❌ Download failed: {str(e)}")

async def handle_direct_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not (UserManager.is_admin(user_id) or UserManager.is_subscribed(user_id)):
        await update.message.reply_text("🔒 Subscribe to download")
        return

    url = update.message.text
    if not ("youtube.com" in url or "youtu.be" in url):
        return

    try:
        video_id = url.split("v=")[1].split("&")[0] if "youtube.com" in url else url.split("/")[-1]
        video_info = await YouTubeService.get_video_info(video_id)
        if not video_info:
            await update.message.reply_text("❌ Invalid link")
            return

        keyboard = [
            [
                InlineKeyboardButton("144p", callback_data=f"quality_{video_id}_144p"),
                InlineKeyboardButton("360p", callback_data=f"quality_{video_id}_360p"),
            ],
            [
                InlineKeyboardButton("720p", callback_data=f"quality_{video_id}_720p"),
                InlineKeyboardButton("1080p", callback_data=f"quality_{video_id}_1080p"),
            ],
            [
                InlineKeyboardButton("Audio", callback_data=f"quality_{video_id}_audio"),
            ],
        ]
        await update.message.reply_text(
            f"🎥 <b>{video_info['title']}</b>\n"
            "⬇️ Select quality:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def setup(application):
    application.add_handler(CallbackQueryHandler(handle_quality_selection, pattern="^quality_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_direct_link))