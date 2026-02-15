import os
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =========================
# ENV VARIABLES
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# =========================
# COMMANDS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "/sensi - Generate Free Sensi\n"
        "/admin - Admin Panel"
    )

async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    general = random.randint(90, 150)
    red_dot = random.randint(100, 150)
    scope_2x = random.randint(100, 150)
    scope_4x = random.randint(100, 150)
    awm = random.randint(50, 100)

    await update.message.reply_text(
        f"🎯 SENSI GENERATED\n\n"
        f"General: {general}\n"
        f"Red Dot: {red_dot}\n"
        f"2x Scope: {scope_2x}\n"
        f"4x Scope: {scope_4x}\n"
        f"AWM: {awm}"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_ID:
        await update.message.reply_text("Admin ID not set")
        return

    if str(update.effective_user.id) != str(ADMIN_ID):
        await update.message.reply_text("❌ You are not admin")
        return

    await update.message.reply_text("✅ Welcome Admin")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sensi", sensi))
    app.add_handler(CommandHandler("admin", admin))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
