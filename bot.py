# bot.py
import os
import sys
import traceback
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ---- Logging config (Railway logs will show these) ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("senx-sensi-bot")

# ---- Read env vars ----
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # keep as string, compare as string later

# ---- Validate early and give helpful error messages ----
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is NOT SET. Add it in Railway Variables.")
    raise RuntimeError("BOT_TOKEN not set")

if ADMIN_ID:
    try:
        # keep string for comparison, but confirm it's numeric
        int(ADMIN_ID)
    except Exception:
        logger.error("ADMIN_ID is present but not numeric. Set ADMIN_ID to your Telegram numeric ID.")
        raise RuntimeError("ADMIN_ID must be numeric")
else:
    logger.warning("ADMIN_ID not set. /admin command will respond 'not admin' to everyone.")

# ---- Bot commands ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info("Received /start from user=%s id=%s", user.username if user else "unknown", user.id if user else "unknown")
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "Commands:\n"
        "/sensi - Generate Free Sensi\n"
        "/admin - Admin Panel"
    )

async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example: real generator logic can be added here
    logger.info("/sensi called by %s (%s)", update.effective_user.username, update.effective_user.id)
    await update.message.reply_text(
        "🎯 SENSI SETTINGS\n"
        "General: 135\n"
        "Red Dot: 140\n"
        "2x Scope: 145\n"
        "4x Scope: 150\n"
        "AWM: 95\n"
        "Fire Button suggestion: 52%"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caller_id = str(update.effective_user.id)
    logger.info("/admin called by id=%s", caller_id)
    if ADMIN_ID and caller_id == str(ADMIN_ID):
        await update.message.reply_text("👑 Admin Access Granted\nBot is running ✅")
    else:
        await update.message.reply_text("❌ You are not admin")

# ---- Main runner ----
def main():
    try:
        logger.info("Starting SENX SENSI BOT")
        app = Application.builder().token(BOT_TOKEN).build()

        # register handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("sensi", sensi))
        app.add_handler(CommandHandler("admin", admin))

        logger.info("Handlers registered. Running polling loop.")
        app.run_polling()
    except Exception as e:
        logger.error("Unhandled exception in main(): %s", e)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
