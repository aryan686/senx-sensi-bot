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

# =========================
# 🔴 REQUIRED SETTINGS
# =========================
BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"
ADMIN_ID = 8130333205      
UPI_ID = "aryankumar6333@navi"       
QR_FILE_ID = None
# =========================

# user state memory
STATE = {}

# =========================
# START
# =========================
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

# =========================
# BUTTON HANDLER
# =========================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    if q.data == "free":
        STATE[uid] = {"mode": "free", "step": "device"}
        await q.message.reply_text("📱 Enter your *Device Name*:")

    elif q.data == "vip":
        STATE[uid] = {"mode": "vip", "step": "pay"}
        if QR_FILE_ID:
            await q.message.reply_photo(
                photo=QR_FILE_ID,
                caption=(
                    "💎 *VIP PAYMENT*\n\n"
                    "Pay using:\n"
                    "• Google Pay\n• Paytm\n• Navi\n\n"
                    f"UPI ID: `{UPI_ID}`\n\n"
                    "Payment ke baad *Reference / UTR ID* bhejo ⬇️"
                ),
                parse_mode="Markdown"
            )
        else:
            await q.message.reply_text(
                "❗ QR not set yet.\n"
                "Admin ko QR image bhejo pehle."
            )

# =========================
# PHOTO HANDLER (QR FILE_ID)
# =========================
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global QR_FILE_ID

    # jab admin QR bheje
    if update.message.from_user.id == ADMIN_ID and update.message.photo:
        QR_FILE_ID = update.message.photo[-1].file_id
        await update.message.reply_text(
            f"✅ QR FILE_ID SET SUCCESSFULLY\n\n{QR_FILE_ID}"
        )
    else:
        await update.message.reply_text("❌ Only admin can set QR.")

# =========================
# TEXT HANDLER
# =========================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text.strip()

    if uid not in STATE:
        return

    st = STATE[uid]

    # -------- FREE FLOW --------
    if st["mode"] == "free":
        if st["step"] == "device":
            st["device"] = text
            st["step"] = "ram"
            await update.message.reply_text("💾 Enter RAM (GB):")

        elif st["step"] == "ram":
            base = random.randint(90, 150)
            fire = round(base / 10, 1)

            await update.message.reply_text(
                f"🎯 *FREE SENSI GENERATED*\n\n"
                f"📱 Device: {st['device']}\n"
                f"💾 RAM: {text}\n\n"
                f"General: {base}\n"
                f"Red Dot: {base+5}\n"
                f"Scope: {base-5}\n"
                f"🔥 Fire Button: {fire}\n\n"
                "_— Sensi by Aryansenx_",
                parse_mode="Markdown"
            )
            STATE.pop(uid)

    # -------- VIP FLOW --------
    elif st["mode"] == "vip":
        if st["step"] == "pay":
            st["utr"] = text
            st["step"] = "device"
            await update.message.reply_text("📱 Enter Device Name:")

        elif st["step"] == "device":
            st["device"] = text
            st["step"] = "ram"
            await update.message.reply_text("💾 Enter RAM (GB):")

        elif st["step"] == "ram":
            keyboard = [
                [
                    InlineKeyboardButton("LOW", callback_data="vip_low"),
                    InlineKeyboardButton("MEDIUM", callback_data="vip_medium"),
                    InlineKeyboardButton("HIGH", callback_data="vip_high"),
                ]
            ]
            await update.message.reply_text(
                "⚙️ Choose VIP Level:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

# =========================
# VIP LEVEL HANDLER
# =========================
async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    if q.data == "vip_low":
        base = random.randint(90, 95)
    elif q.data == "vip_medium":
        base = random.randint(100, 150)
    else:
        base = random.randint(150, 200)

    fire = round(base / 10, 1)

    await q.message.reply_text(
        f"💎 *VIP SENSI GENERATED*\n\n"
        f"General: {base}\n"
        f"Red Dot: {base+5}\n"
        f"Scope: {base-5}\n"
        f"🔥 Fire Button: {fire}\n\n"
        "_— Sensi by Aryansenx_",
        parse_mode="Markdown"
    )
    STATE.pop(uid)

# =========================
# MAIN
# =========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons, pattern="^(free|vip)$"))
app.add_handler(CallbackQueryHandler(vip_level, pattern="^vip_"))
app.add_handler(MessageHandler(filters.PHOTO, photo_handler)) 
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("🤖 BOT RUNNING")
app.run_polling()
