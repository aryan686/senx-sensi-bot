import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 SENX SENSI BOT\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------- BUTTON HANDLER ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data == "free":
        user_state[uid] = {"mode": "free", "step": "device"}
        await query.message.reply_text("📱 Enter Device Name:")
        return

    if query.data == "vip":
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=QR_FILE_ID,
            caption=(
                "💎 VIP SENSI ACCESS\n\n"
                f"💰 Price: ₹{VIP_PRICE}\n"
                f"🟣 UPI ID: {UPI_ID}\n\n"
                "Pay via GPay / PhonePe / Paytm / Navi\n"
                "Payment ke baad admin verify karega"
            ),
            parse_mode="Markdown"
        )
        user_state[uid] = {"mode": "vip", "step": "device"}
        await query.message.reply_text("📱 Enter Device Name:")
        return

    if query.data.startswith("vip_"):
        await vip_level_handler(update, context)

# ---------- TEXT HANDLER ----------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text.strip()

    if uid not in user_state:
        return

    state = user_state[uid]

    # STEP 1 — DEVICE
    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter RAM (e.g. 4GB):")
        return

    # STEP 2 — RAM
    if state["step"] == "ram":
        state["ram"] = text

        # ===== FREE SENSI =====
        if state["mode"] == "free":
            sensi = random.randint(90, 150)
            fire = round(sensi / 10, 1)

            await update.message.reply_text(
                f"⚡ FREE SENSI\n\n"
                f"📱 {state['device']}\n"
                f"💾 {state['ram']}\n\n"
                f"🎯 Sensi: {sensi}\n"
                f"🔥 Fire: {fire}\n\n"
                "Sensi by AryanSenx",
                parse_mode="Markdown"
            )
            user_state.pop(uid, None)
            return

        # ===== VIP FLOW =====
        if state["mode"] == "vip":
            if uid not in vip_users and uid != ADMIN_ID:
                await update.message.reply_text("❌ VIP not verified.")
                return

            keyboard = [
                [
                    InlineKeyboardButton("Low", callback_data="vip_low"),
                    InlineKeyboardButton("Medium", callback_data="vip_medium"),
                    InlineKeyboardButton("High", callback_data="vip_high"),
                ]
            ]
            state["step"] = "vip_level"
            await update.message.reply_text(
                "⚙️ Choose Sensi Level:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

# ---------- VIP LEVEL ----------
async def vip_level_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    state = user_state.get(uid)

    if not state:
        return

    if uid not in vip_users and uid != ADMIN_ID:
        await query.message.reply_text("❌ VIP not verified.")
        return

    if query.data == "vip_low":
        sensi = random.randint(90, 95)
    elif query.data == "vip_medium":
        sensi = random.randint(100, 150)
    else:
        sensi = random.randint(150, 200)

    fire = round(sensi / 10, 1)

    await query.message.reply_text(
        f"💎 VIP SENSI\n\n"
        f"📱 {state['device']}\n"
        f"💾 {state['ram']}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}\n\n"
        "Sensi by AryanSenx",
        parse_mode="Markdown"
    )

    user_state.pop(uid, None)

# ---------- ADMIN VERIFY ----------
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    vip_users.add(int(context.args[0]))
    await update.message.reply_text("✅ VIP verified successfully.")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if _name_ == "_main_":
    main()
