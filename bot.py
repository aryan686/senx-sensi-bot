import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# ENV VARIABLES
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "Commands:\n"
        "/sensi - Generate Free Sensi\n"
        "/admin - Admin Panel"
    )

# /sensi
async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sensi_value = random.randint(90, 150)
    await update.message.reply_text(
        f"🎯 Your Free Fire Sensi:\n\n"
        f"General: {sensi_value}\n"
        f"Red Dot: {sensi_value + 5}\n"
        f"2x Scope: {sensi_value + 10}\n"
        f"4x Scope: {sensi_value + 15}"
    )

# /admin
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if ADMIN_ID and user_id == ADMIN_ID:
        await update.message.reply_text("✅ Admin access granted")
    else:
        await update.message.reply_text("❌ You are not admin")

# MAIN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sensi", sensi))
    app.add_handler(CommandHandler("admin", admin))

    print("🤖 SENX SENSI BOT STARTED")
    app.run_polling()

if __name__ == "__main__":
    main()
