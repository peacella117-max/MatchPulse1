import os
import logging
from telegram.ext import Application, CommandHandler
from telegram import Update

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get token from Railway environment
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    logger.error("❌ BOT_TOKEN not set in Railway variables!")
    exit(1)

async def start(update: Update, context):
    await update.message.reply_text("""
⚡ *Welcome to MatchPulse!* ⚡

Your bot is running on Railway!

Commands:
/start - Welcome
/ping - Check if bot is alive
""", parse_mode='Markdown')

async def ping(update: Update, context):
    await update.message.reply_text("🏓 Pong! Bot is alive on Railway!")

def main():
    logger.info("🤖 Starting MatchPulse Bot on Railway...")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    
    logger.info("✅ Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
