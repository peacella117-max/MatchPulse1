import asyncio
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from telegram import Update
from bot.config import config
from bot.handlers.start import start_command, help_command
from bot.handlers.matches import (
    upcoming_matches,
    match_details,
    live_scores
)
from bot.handlers.analytics import (
    team_analytics,
    player_stats,
    head_to_head
)
from bot.handlers.predictions import (
    get_prediction,
    daily_picks
)
from bot.handlers.subscription import (
    subscribe,
    unsubscribe,
    subscription_status
)
from bot.database import init_db
from bot.services.cache_manager import cache_manager

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MatchPulseBot:
    def __init__(self):
        self.application = Application.builder().token(config.BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all command handlers"""
        # Commands
        self.application.add_handler(CommandHandler("start", start_command))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(CommandHandler("matches", upcoming_matches))
        self.application.add_handler(CommandHandler("live", live_scores))
        self.application.add_handler(CommandHandler("match", match_details))
        self.application.add_handler(CommandHandler("team", team_analytics))
        self.application.add_handler(CommandHandler("player", player_stats))
        self.application.add_handler(CommandHandler("h2h", head_to_head))
        self.application.add_handler(CommandHandler("predict", get_prediction))
        self.application.add_handler(CommandHandler("picks", daily_picks))
        self.application.add_handler(CommandHandler("subscribe", subscribe))
        self.application.add_handler(CommandHandler("unsubscribe", unsubscribe))
        self.application.add_handler(CommandHandler("status", subscription_status))
        
        # Callback queries
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))
        
        # Error handler
        self.application.add_error_handler(self._error_handler)
    
    async def _handle_callback(self, update: Update, context):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        if data.startswith('match_'):
            await match_details(update, context)
        elif data.startswith('team_'):
            await team_analytics(update, context)
        elif data.startswith('predict_'):
            await get_prediction(update, context)
    
    async def _error_handler(self, update, context):
        """Log errors"""
        logger.error(f"Update {update} caused error {context.error}")
    
    async def start(self):
        """Start the bot"""
        await init_db()
        await cache_manager.initialize()
        
        if config.WEBHOOK_URL:
            # Production: Use webhook
            await self.application.bot.set_webhook(
                url=f"{config.WEBHOOK_URL}/webhook",
                allowed_updates=["message", "callback_query"]
            )
            logger.info(f"Webhook set to {config.WEBHOOK_URL}")
        else:
            # Development: Use polling
            logger.info("Starting polling...")
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
    
    async def stop(self):
        """Stop the bot"""
        await self.application.stop()
        await self.application.shutdown()

def main():
    """Main entry point"""
    bot = MatchPulseBot()
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        asyncio.run(bot.stop())

if __name__ == "__main__":
    main()
