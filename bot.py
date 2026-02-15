import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if BOT_TOKEN is None:
    print("BOT_TOKEN missing")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "/sensi - Generate Sensi\n"
        "/admin - Admin Panel"
    )

async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎯 SENSI GENERATED\n\n"
        f"General: {random.randint(90,150)}\n"
        f"Red Dot: {random.randint(100,150)}\n"
        f"2x Scope: {random.randint(100,150)}\n"
        f"4x Scope: {random.randint(100,150)}\n"
        f"AWM: {random.randint(50,100)}"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID is None:
        await update.message.reply_text("Admin not configured")
        return

    if str(update.effective_user.id) != str(ADMIN_ID):
        await update.message.reply_text("❌ Access Denied")
        return

    await update.message.reply_text("✅ Welcome Admin")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sensi", sensi))
    app.add_handler(CommandHandler("admin", admin))

    print("BOT STARTED SUCCESSFULLY")
    app.run_polling()

if __name__ == "__main__":
    main()
