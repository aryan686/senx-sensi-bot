import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== ENV VARIABLES =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

if not ADMIN_ID:
    raise RuntimeError("ADMIN_ID not set")

ADMIN_ID = int(ADMIN_ID)

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT LIVE 🔥\n\n"
        "Commands:\n"
        "/sensi - Generate sensi\n"
        "/admin - Admin only"
    )

async def sensi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 SENX SENSI GENERATED 🎯\n\n"
        "General: 145\n"
        "Red Dot: 138\n"
        "2x Scope: 150\n"
        "4x Scope: 142\n"
        "AWM: 72\n\n"
        "🔥 Headshot Accuracy Boosted 🔥"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not admin")
        return

    await update.message.reply_text(
        "✅ ADMIN PANEL\n\n"
        "Bot is running perfectly."
    )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sensi", sensi))
    app.add_handler(CommandHandler("admin", admin))

    print("Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
