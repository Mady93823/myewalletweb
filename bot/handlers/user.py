from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, WebAppInfo
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bot.database import db
import os
import asyncio

WELCOME_TEXT = """
🚀 <b>Welcome to myewallet.global!</b>

Your gateway to intelligent finance. Experience the future of digital asset management with AI-driven insights and secure transactions.

✨ <b>Smart Analysis</b>
🛡️ <b>Bank-Grade Security</b>
⚡ <b>Instant Transfers</b>

<i>Manage your wealth smarter, not harder.</i>
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Add user to database (Non-blocking)
    # We use asyncio.to_thread to prevent the DB call from blocking the event loop
    asyncio.create_task(asyncio.to_thread(
        db.add_user, user.id, user.username, user.first_name, user.last_name
    ))

    # Set the persistent Menu Button (Open App)
    try:
        await context.bot.set_chat_menu_button(
            chat_id=update.effective_chat.id,
            menu_button=MenuButtonWebApp(text="Open App", web_app=WebAppInfo(url="https://myewallet.global/"))
        )
    except Exception as e:
        # Log error but don't stop the welcome flow
        print(f"Failed to set menu button: {e}")

    # Prepare the welcome message
    keyboard = [
        [InlineKeyboardButton("Open Wallet 🌐", web_app=WebAppInfo(url="https://myewallet.global/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send photo with caption
    photo_path = os.path.join(os.getcwd(), 'img.jpg')
    
    try:
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=WELCOME_TEXT,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup
                )
        else:
            # Fallback if image is missing
            await update.message.reply_text(
                text=WELCOME_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup
            )
    except Exception as e:
        # Fallback in case of error (e.g., file permission)
        await update.message.reply_text(
            text=f"{WELCOME_TEXT}\n\n(Image could not be loaded)",
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
