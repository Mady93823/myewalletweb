from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import RetryAfter, Forbidden
from bot.config import ADMIN_IDS
from bot.database import db
from bot.utils.helpers import parse_time_string
import logging
import asyncio

logger = logging.getLogger(__name__)

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            # Silently ignore or reply? Usually ignore to not leak admin existence.
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

@admin_only
async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats_text = f"📊 <b>Bot Statistics</b>\n"
    stats_text += f"Total Users: {db.count_users()}\n"
    
    help_text = """
<b>Admin Commands:</b>

/broadcast [time] [message]
Schedule a broadcast message.
Time format: 10s, 15m, 2h, 1d. Use '0s' or 'now' for immediate.

Examples:
<code>/broadcast now Hello everyone!</code>
<code>/broadcast 2h Don't forget to check the app!</code>
    """
    await update.message.reply_text(stats_text + help_text, parse_mode='HTML')

async def send_broadcast(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    message = job.data
    users = db.get_all_users()
    
    success_count = 0
    fail_count = 0
    
    for user in users:
        user_id = user.get('user_id')
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            success_count += 1
            # Rate limiting: Sleep 0.05s to stay around 20 msgs/sec
            await asyncio.sleep(0.05)
            
        except RetryAfter as e:
            # If we hit a rate limit, sleep for the requested time
            logger.warning(f"Rate limit hit. Sleeping for {e.retry_after} seconds.")
            await asyncio.sleep(e.retry_after)
            # Retry once
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
                success_count += 1
            except Exception as e2:
                logger.warning(f"Failed to send broadcast to {user_id} after retry: {e2}")
                fail_count += 1
                
        except Forbidden:
            # User blocked the bot
            logger.info(f"User {user_id} has blocked the bot.")
            fail_count += 1
            # Optional: Mark user as inactive in DB
            
        except Exception as e:
            logger.warning(f"Failed to send broadcast to {user_id}: {e}")
            fail_count += 1
            
    # Notify admins about completion
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id, 
                text=f"📢 Broadcast completed.\nSuccess: {success_count}\nFailed: {fail_count}"
            )
        except:
            pass

@admin_only
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /broadcast [time] [message]")
        return

    time_str = args[0]
    message = ' '.join(args[1:])
    
    delay = 0
    if time_str.lower() != 'now':
        delay = parse_time_string(time_str)
        if delay is None:
            await update.message.reply_text("Invalid time format. Use 10s, 15m, 2h, etc.")
            return

    # Schedule the job
    context.job_queue.run_once(send_broadcast, delay, data=message)
    
    if delay > 0:
        await update.message.reply_text(f"✅ Broadcast scheduled in {time_str}.")
    else:
        await update.message.reply_text("✅ Broadcast started immediately.")
