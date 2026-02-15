import os
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile
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

BOT_TOKEN = os.getenv("8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA")        # Railway variable
ADMIN_ID = int(os.getenv("8130333205"))     # Railway variable

VIP_PRICE = 199
UPI_ID = "aryankumar6333@navi"

SIGNATURE = "<b><span style='color:red'>Sensi</span> <span style='color:black'>by AryanSenx</span></b>"

# user state storage
USER_STATE = {}
VIP_USERS = set()   # verified vip users (runtime)

# ================= START ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 <b>SENX SENSI BOT</b>\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

# ================= BUTTON HANDLER =================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "free":
        USER_STATE[user_id] = {"mode": "free", "step": "device"}
        await query.message.reply_text("📱 Enter Device Name:")

    elif query.data == "vip":
        if user_id not in VIP_USERS:
            await send_qr(query)
        else:
            USER_STATE[user_id] = {"mode": "vip", "step": "device"}
            await query.message.reply_text("📱 Enter Device Name:")

    elif query.data.startswith("vip_level"):
        level = query.data.split("_")[-1]
        state = USER_STATE.get(user_id)

        if not state or state.get("mode") != "vip":
            return

        device = state["device"]
        ram = state["ram"]

        sensi = generate_sensi(level)
        fire = round(sensi / 10, 1)

        await query.message.reply_text(
            f"💎 <b>VIP SENSI</b>\n\n"
            f"📱 {device}\n"
            f"💾 {ram}GB\n"
            f"🎯 Level: {level.capitalize()}\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            f"{SIGNATURE}",
            parse_mode="HTML"
        )

        USER_STATE.pop(user_id, None)

# ================= QR =================

async def send_qr(query):
    with open("qr.png", "rb") as f:
        await query.message.reply_photo(
            photo=InputFile(f),
            caption=(
                "💎 <b>VIP SENSI ACCESS</b>\n\n"
                f"💰 Price: ₹{VIP_PRICE}\n"
                f"🟣 UPI ID: <b>{UPI_ID}</b>\n\n"
                "Pay via GPay / PhonePe / Paytm / Navi\n\n"
                "Payment ke baad admin verify karega.\n"
                "Verify hone ke baad VIP auto enable ho jayega."
            ),
            parse_mode="HTML"
        )

# ================= TEXT FLOW =================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id not in USER_STATE:
        return

    state = USER_STATE[user_id]

    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter RAM (e.g. 4, 6, 8):")

    elif state["step"] == "ram":
        if not text.isdigit():
            await update.message.reply_text("❌ Only number allowed (e.g. 4)")
            return

        state["ram"] = text

        if state["mode"] == "free":
            sensi = random.randint(110, 120)
            fire = round(sensi / 10, 1)

            await update.message.reply_text(
                f"⚡ <b>FREE SENSI</b>\n\n"
                f"📱 {state['device']}\n"
                f"💾 {state['ram']}GB\n\n"
                f"🎯 Sensi: {sensi}\n"
                f"🔥 Fire: {fire}\n\n"
                f"{SIGNATURE}",
                parse_mode="HTML"
            )
            USER_STATE.pop(user_id, None)

        else:
            keyboard = [[
                InlineKeyboardButton("Low", callback_data="vip_level_low"),
                InlineKeyboardButton("Medium", callback_data="vip_level_medium"),
                InlineKeyboardButton("High", callback_data="vip_level_high"),
            ]]
            await update.message.reply_text(
                "⚙️ Choose Sensi Level:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

# ================= ADMIN =================

async def verify_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    uid = int(context.args[0])
    VIP_USERS.add(uid)

    await update.message.reply_text(f"✅ VIP enabled for {uid}")
    await context.bot.send_message(
        chat_id=uid,
        text="💎 VIP ACCESS ENABLED!\nAb VIP Sensi use kar sakte ho."
    )

# ================= UTILS =================

def generate_sensi(level):
    if level == "low":
        return random.randint(90, 100)
    if level == "medium":
        return random.randint(100, 110)
    return random.randint(110, 125)

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verify_vip))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if _name_ == "_main_":
    main()
