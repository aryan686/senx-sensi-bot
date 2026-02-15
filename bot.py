import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"
ADMIN_ID = 8130333205
QR_FILE_ID = "AgACAgUAAxkBAANCaZHeSYv5eJwaFESB71sCoC3foTIAAv0Oaxue75BUKBXoj4Ay89wBAAMCAAN5AAM6BA"
UPI_ID = "aryankumar6333@navi"
VIP_PRICE = 199
# ==========================================

user_state = {}
vip_users = set()

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------- BUTTON HANDLER ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data == "free":
        user_state[uid] = {"mode": "free", "step": "device"}
        await query.message.reply_text("📱 Enter your *Device Name*:", parse_mode="Markdown")

    elif query.data == "vip":
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=QR_FILE_ID,
            caption=(
                "💎 *VIP SENSI ACCESS*\n\n"
                f"💰 Price: *₹{VIP_PRICE}*\n"
                f"🟣 *UPI ID:* `{UPI_ID}`\n\n"
                "Pay using:\n"
                "• Google Pay\n• PhonePe\n• Paytm\n• Navi\n\n"
                "_Payment ke baad admin verify karega_"
            ),
            parse_mode="Markdown"
        )

        user_state[uid] = {"mode": "vip", "step": "device"}
        await query.message.reply_text("📱 Enter your *Device Name*:", parse_mode="Markdown")

# ---------- TEXT HANDLER ----------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text

    if uid not in user_state:
        return

    state = user_state[uid]

    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter your *RAM* (e.g. 4GB, 6GB):", parse_mode="Markdown")

    elif state["step"] == "ram":
        state["ram"] = text

        if state["mode"] == "free":
            sensi = random.randint(90, 150)
            fire = round(sensi / 10, 1)
            await update.message.reply_text(
                f"🎯 *FREE SENSI GENERATED*\n\n"
                f"📱 Device: `{state['device']}`\n"
                f"💾 RAM: `{state['ram']}`\n\n"
                f"🔹 Sensi: `{sensi}`\n"
                f"🔥 Fire Button: `{fire}`\n\n"
                f"_Sensi by AryanSenx_",
                parse_mode="Markdown"
            )
            user_state.pop(uid)

        else:
            if uid not in vip_users and uid != ADMIN_ID:
                await update.message.reply_text("⛔ VIP not activated yet.")
                return

            keyboard = [
                [
                    InlineKeyboardButton("Low", callback_data="vip_low"),
                    InlineKeyboardButton("Medium", callback_data="vip_medium"),
                    InlineKeyboardButton("High", callback_data="vip_high")
                ]
            ]
            await update.message.reply_text(
                "⚙️ Choose *Sensi Level*:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

# ---------- VIP LEVEL ----------
async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    state = user_state.get(uid)

    if not state:
        return

    if "low" in query.data:
        sensi = random.randint(90, 95)
    elif "medium" in query.data:
        sensi = random.randint(100, 150)
    else:
        sensi = random.randint(150, 200)

    fire = round(sensi / 10, 1)

    await query.message.reply_text(
        f"💎 *VIP SENSI GENERATED*\n\n"
        f"📱 Device: `{state['device']}`\n"
        f"💾 RAM: `{state['ram']}`\n\n"
        f"🔹 Sensi: `{sensi}`\n"
        f"🔥 Fire Button: `{fire}`\n\n"
        f"_Sensi by AryanSenx_",
        parse_mode="Markdown"
    )

    user_state.pop(uid)

# ---------- ADMIN VERIFY ----------
async def verify_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    uid = int(context.args[0])
    vip_users.add(uid)
    await update.message.reply_text(f"✅ VIP Activated for {uid}")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verify_vip))
    app.add_handler(CallbackQueryHandler(buttons, pattern="^(free|vip)$"))
    app.add_handler(CallbackQueryHandler(vip_level, pattern="^vip_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
