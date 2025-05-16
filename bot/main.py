import os
import logging
from telegram.ext import Application
from bot.handlers import register_handlers
from bot.utils.logger import configure_logging

def create_app():
    configure_logging()
    os.makedirs("data/downloads", exist_ok=True)
    
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    register_handlers(application)
    return application

def main():
    app = create_app()
    
    if os.getenv("WEBHOOK_URL"):
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 8443)),
            webhook_url=os.getenv("WEBHOOK_URL"),
            secret_token=os.getenv("WEBHOOK_SECRET"),
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()