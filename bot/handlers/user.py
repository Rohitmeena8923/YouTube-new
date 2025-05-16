from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from services.user_manager import UserManager
from config.settings import SUBSCRIPTION_PRICE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if UserManager.is_admin(user_id):
        await update.message.reply_text("👑 Welcome Admin!\nUse /search or send YouTube links.")
        return
    
    if UserManager.is_subscribed(user_id):
        await update.message.reply_text("🌟 Welcome back! Your subscription is active.")
        return
    
    if UserManager.add_free_user(user_id):
        await update.message.reply_text(
            "🆓 Welcome! Free version with limits.\n"
            f"Subscribe with /subscribe (${SUBSCRIPTION_PRICE}/month)"
        )
    else:
        await update.message.reply_text(
            "⚠️ Free user limit reached!\n"
            f"Please /subscribe (${SUBSCRIPTION_PRICE}/month)"
        )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if UserManager.is_subscribed(user_id):
        expiry = user_db[user_id]["subscription_expiry"].strftime("%Y-%m-%d")
        await update.message.reply_text(f"🌟 Active subscription!\nExpires: {expiry}")
        return

    await update.message.reply_text(
        f"💳 Subscription: ${SUBSCRIPTION_PRICE}/month\n"
        "Send payment to: paypal@example.com\n"
        "Then send transaction ID to @admin"
    )

def setup(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("subscribe", subscribe))