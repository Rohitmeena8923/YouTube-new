import logging
from telegram.ext import Application
from config.settings import TELEGRAM_TOKEN, WEBHOOK_URL, PORT
from handlers import register_handlers
from utils.logger import configure_logging

def main() -> None:
    """Start the bot."""
    configure_logging()
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    register_handlers(application)

    if WEBHOOK_URL:
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL,
        )
    else:
        application.run_polling()

if __name__ == "__main__":
    main()