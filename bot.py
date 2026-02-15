import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if BOT_TOKEN is None:
    raise RuntimeError("BOT_TOKEN not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "/sensi - Generate Sensi\n"
        "/admin - Admin Panel"
    )

async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = random.randint(90, 150)
    await update.message.reply_text(
        f"🎯 Sensi Generated:\n"
        f"General: {base}\n"
        f"Red Dot: {base+5}\n"
        f"2x: {base+10}\n"
        f"4x: {base+15}"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and str(update.effective_user.id) == ADMIN_ID:
        await update.message.reply_text("✅ Admin Access")
    else:
        await update.message.reply_text("❌ Not Admin")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sensi", sensi))
    app.add_handler(CommandHandler("admin", admin))
    print("BOT STARTED")
    app.run_polling()

if __name__ == "__main__":
    main()
