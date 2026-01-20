import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.config import BOT_TOKEN
from bot.handlers.user import start
from bot.handlers.admin import broadcast, admin_help
from bot.database import db
import sys

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found. Please set it in .env file.")
        return

    # Check Database Connection
    if db.client is None:
        print("❌ CRITICAL ERROR: Could not connect to MongoDB.")
        print("Please check your MONGODB_URI and ensure your IP is whitelisted.")
        sys.exit(1)
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # User Handlers
    application.add_handler(CommandHandler("start", start))

    # Admin Handlers
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("help", admin_help))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
