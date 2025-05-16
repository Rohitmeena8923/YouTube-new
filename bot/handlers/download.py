from telegram.ext import MessageHandler, filters, CallbackQueryHandler

async def handle_quality_selection(update, context):
    await update.callback_query.answer("Quality selected")

async def handle_direct_link(update, context):
    await update.message.reply_text("Processing link...")

def setup(application):
    application.add_handler(CallbackQueryHandler(handle_quality_selection, pattern="^quality_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_direct_link))