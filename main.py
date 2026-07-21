import os
import asyncio
import logging
from telegram.ext import Application, CommandHandler
from telegram import Update

# Setup logging for Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Simple handlers for testing
async def start(update: Update, context):
    await update.message.reply_text("""
⚡ *Welcome to MatchPulse!* ⚡

Your sports analytics bot is running on Railway!

Commands:
/start - Welcome message
/help - Show help
/ping - Check if bot is alive
""", parse_mode='Markdown')

async def help_command(update: Update, context):
    await update.message.reply_text("""
📚 Available Commands:
/start - Start the bot
/help - Show this help
/ping - Check if bot is working
""")

async def ping(update: Update, context):
    await update.message.reply_text("🏓 Pong! Bot is alive and running on Railway!")

def main():
    # Get token from Railway environment variables
    TOKEN = os.getenv('BOT_TOKEN')
    
    if not TOKEN:
        logger.error("❌ BOT_TOKEN not set in Railway environment variables!")
        return
    
    logger.info("🤖 Starting MatchPulse Bot on Railway...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    
    logger.info("✅ Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
