from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from services.youtube import YouTubeService
from services.user_manager import UserManager

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not (UserManager.is_admin(user_id) or UserManager.is_subscribed(user_id)):
        await update.message.reply_text("🔒 Premium feature! Please /subscribe")
        return

    if not context.args:
        await update.message.reply_text("Usage: /search query")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching: {query}...")

    try:
        videos = await YouTubeService.search_videos(query)
        if not videos:
            await update.message.reply_text("❌ No results found")
            return

        keyboard = [
            [InlineKeyboardButton(
                f"{i+1}. {video['title'][:50]}...", 
                callback_data=f"video_{video['id']}"
            )]
            for i, video in enumerate(videos)
        ]
        await update.message.reply_text(
            "🎬 Results:",
            reply_markup=InlineKeyboardMarkup(keyboard)
    except Exception as e:
        await update.message.reply_text(f"❌ Search failed: {str(e)}")

async def handle_video_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    video_id = query.data.split("_")[1]
    try:
        video_info = await YouTubeService.get_video_info(video_id)
        if not video_info:
            await query.edit_message_text("❌ Video unavailable")
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
        await query.edit_message_text(
            f"🎥 <b>{video_info['title']}</b>\n"
            f"⏱ Duration: {video_info['duration']}s\n\n"
            "⬇️ Select quality:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")

def setup(application):
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CallbackQueryHandler(handle_video_selection, pattern="^video_"))