from telegram.ext import CommandHandler

async def admin_stats(update, context):
    await update.message.reply_text("Admin stats")

async def admin_broadcast(update, context):
    await update.message.reply_text("Broadcasting...")

def setup(application):
    application.add_handler(CommandHandler("stats", admin_stats))
    application.add_handler(CommandHandler("broadcast", admin_broadcast))