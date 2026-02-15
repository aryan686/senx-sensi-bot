import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# ================= USER DATA =================
users = {}

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="FREE")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="VIP")],
    ]
    await update.message.reply_text(
        "🔥 SENX SENSI BOT\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

# ================= BUTTON HANDLER =================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data == "FREE":
        users[uid] = {"mode": "FREE", "step": "DEVICE"}
        await query.message.reply_text("📱 Enter Device Name:")

    elif query.data == "VIP":
        users[uid] = {"mode": "VIP", "step": "DEVICE"}
        await query.message.reply_text(
            "💎 VIP SENSI\n\n"
            "💰 Price: ₹199\n"
            "UPI: aryankumar6333@navi\n\n"
            "Payment ke baad admin verify karega.\n\n"
            "📱 Enter Device Name:",
            parse_mode="Markdown",
        )

# ================= TEXT HANDLER =================
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text

    if uid not in users:
        return

    user = users[uid]

    # DEVICE
    if user["step"] == "DEVICE":
        user["device"] = text
        user["step"] = "RAM"
        await update.message.reply_text("💾 Enter RAM (4 / 6 / 8):")
        return

    # RAM
    if user["step"] == "RAM":
        if not text.isdigit():
            await update.message.reply_text("❌ RAM number me likho")
            return

        user["ram"] = int(text)

        if user["mode"] == "FREE":
            sensi = random.randint(110, 135)
            fire = round(sensi / 10, 1)

            await update.message.reply_text(
                f"⚡ FREE SENSI\n\n"
                f"📱 Device: {user['device']}\n"
                f"💾 RAM: {user['ram']}GB\n\n"
                f"🎯 Sensi: {sensi}\n"
                f"🔥 Fire: {fire}\n\n"
                f"🔴 Sensi by AryanSenx",
                parse_mode="Markdown",
            )
            users.pop(uid)
            return

        # VIP FLOW
        if user["mode"] == "VIP":
            keyboard = [
                [
                    InlineKeyboardButton("Low", callback_data="VIP_LOW"),
                    InlineKeyboardButton("Medium", callback_data="VIP_MED"),
                    InlineKeyboardButton("High", callback_data="VIP_HIGH"),
                ]
            ]
            user["step"] = "LEVEL"
            await update.message.reply_text(
                "⚙️ Choose VIP Sensi Level:",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
            return

# ================= VIP LEVEL =================
async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if uid not in users or users[uid]["mode"] != "VIP":
        await query.message.reply_text("❌ VIP not active")
        return

    level = query.data
    base = {"VIP_LOW": 90, "VIP_MED": 105, "VIP_HIGH": 120}[level]
    sensi = base + random.randint(5, 15)
    fire = round(sensi / 10, 1)

    user = users[uid]

    await query.message.reply_text(
        f"💎 VIP SENSI\n\n"
        f"📱 Device: {user['device']}\n"
        f"💾 RAM: {user['ram']}GB\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}\n\n"
        f"🔴 Sensi by AryanSenx",
        parse_mode="Markdown",
    )

    users.pop(uid)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(vip_level, pattern="VIP_"))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("Bot running...")
    app.run_polling()

if _name_ == "_main_":
    main()
