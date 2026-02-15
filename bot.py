import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ENV VARIABLES
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# COMMAND: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to SENX SENSI BOT 🔥\n\n"
        "Commands:\n"
        "/sensi - Generate Free Sensi\n"
        "/admin - Admin Panel"
    )

# COMMAND: /sensi
async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 Your Sensi:\n"
        "General: 135\n"
        "Red Dot: 140\n"
        "2x Scope: 145\n"
        "4x Scope: 150\n"
        "AWM: 95\n"
        "Fire Button: 52%"
    )

# COMMAND: /admin
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and str(update.effective_user.id) == str(ADMIN_ID):
        await update.message.reply_text(
            "👑 ADMIN PANEL\n\n"
            "Bot is running fine ✅"
        )
    else:
        await update.message.reply_text("❌ You are not admin")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sensi", sensi))
    app.add_handler(CommandHandler("admin", admin))

    print("🤖 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
