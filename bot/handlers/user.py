from telegram.ext import CommandHandler

async def start(update, context):
    await update.message.reply_text("Bot started!")

async def subscribe(update, context):
    await update.message.reply_text("Subscribe command")

def setup(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("subscribe", subscribe))