from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from services.user_manager import UserManager

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not UserManager.is_admin(user_id):
        await update.message.reply_text("❌ Admin only")
        return

    stats = UserManager.get_user_stats()
    await update.message.reply_text(
        "📊 Stats:\n"
        f"Total: {stats['total_users']}\n"
        f"Subscribed: {stats['subscribed_users']}\n"
        f"Free: {stats['free_users']}"
    )

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not UserManager.is_admin(user_id):
        await update.message.reply_text("❌ Admin only")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast message")
        return

    message = "📢 Announcement:\n" + " ".join(context.args)
    stats = {"success": 0, "failures": 0}

    for user_id in user_db:
        try:
            await context.bot.send_message(user_id, message)
            stats["success"] += 1
        except Exception:
            stats["failures"] += 1

    await update.message.reply_text(
        f"Broadcast sent:\n"
        f"✅ {stats['success']}\n"
        f"❌ {stats['failures']}"
    )

def setup(application):
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("broadcast", admin_broadcast))