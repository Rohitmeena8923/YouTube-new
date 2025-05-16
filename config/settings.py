import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8443))
MAX_FREE_USERS = int(os.getenv("MAX_FREE_USERS", 10))
SUBSCRIPTION_PRICE = float(os.getenv("SUBSCRIPTION_PRICE", 5.0))