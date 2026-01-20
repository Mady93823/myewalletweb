import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_IDS = [int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id.strip()]

# Database Configuration
MONGODB_URI = os.getenv("MONGODB_URI")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL)
)
logger = logging.getLogger(__name__)

# Validation
if not BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables.")
if not MONGODB_URI:
    logger.error("MONGODB_URI is not set in environment variables.")
