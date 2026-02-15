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

# ========== CONFIG ==========
BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"
ADMIN_ID = 8130333205
QR_FILE_ID = "PASTE_QR_FILE_ID"
UPI_ID = "aryankumar6333@navi"
VIP_PRICE = 199
# ============================

user_state = {}
vip_users = set()

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------- BUTTONS ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    # ---- FREE ----
    if query.data == "free":
        user_state[uid] = {"mode": "free", "step": "device"}
        await query.message.reply_text("📱 Enter Device Name:")

    # ---- VIP ----
    elif query.data == "vip":
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=QR_FILE_ID,
            caption=(
                "💎 *VIP SENSI ACCESS*\n\n"
                f"💰 Price: *₹{VIP_PRICE}*\n"
                f"🟣 *UPI ID:* `{UPI_ID}`\n\n"
                "Pay using GPay / PhonePe / Paytm / Navi\n"
                "_Payment ke baad admin verify karega_"
            ),
            parse_mode="Markdown"
        )

        user_state[uid] = {"mode": "vip", "step": "device"}
        await query.message.reply_text("📱 Enter Device Name:")

# ---------- TEXT ----------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text

    if uid not in user_state:
        return

    state = user_state[uid]

    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter RAM (e.g. 4GB):")
        return

    if state["step"] == "ram":
        state["ram"] = text

        # ===== FREE FLOW =====
        if state["mode"] == "free":
            sensi = random.randint(90, 150)
            fire = round(sensi / 10, 1)

            await update.message.reply_text(
                f"⚡ *FREE SENSI*\n\n"
                f"📱 `{state['device']}`\n"
                f"💾 `{state['ram']}`\n\n"
                f"🎯 Sensi: `{sensi}`\n"
                f"🔥 Fire: `{fire}`\n\n"
                "_Sensi by AryanSenx_",
                parse_mode="Markdown"
            )
            user_state.pop(uid)
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
            await update.message.reply_text(
                "⚙️ Choose Sensi Level:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

# ---------- VIP LEVEL ----------
async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    state = user_state.get(uid)
    if not state:
        return

    if uid not in vip_users and uid != ADMIN_ID:
        await query.message.reply_text("❌ VIP not verified.")
        return

    if "low" in query.data:
        sensi = random.randint(90, 95)
    elif "medium" in query.data:
        sensi = random.randint(100, 150)
    else:
        sensi = random.randint(150, 200)

    fire = round(sensi / 10, 1)

    await query.message.reply_text(
        f"💎 *VIP SENSI*\n\n"
        f"📱 `{state['device']}`\n"
        f"💾 `{state['ram']}`\n\n"
        f"🎯 Sensi: `{sensi}`\n"
        f"🔥 Fire: `{fire}`\n\n"
        "_Sensi by AryanSenx_",
        parse_mode="Markdown"
    )

    user_state.pop(uid)

# ---------- ADMIN ----------
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    vip_users.add(int(context.args[0]))
    await update.message.reply_text("✅ VIP verified.")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CallbackQueryHandler(buttons, pattern="^(free|vip)$"))
    app.add_handler(CallbackQueryHandler(vip_level, pattern="^vip_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
