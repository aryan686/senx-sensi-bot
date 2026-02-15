import os
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQuerYHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # numeric string

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing in Railway Variables")

QR_PATH = "qr.png"

# ================== USER STATES ==================
user_state = {}
user_data = {}
vip_users = set()  # manually verified VIP users

# ================== HELPERS ==================
def reset_user(uid: int):
    user_state.pop(uid, None)
    user_data.pop(uid, None)

def safe_int(text):
    try:
        return int(text)
    except:
        return None

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    reset_user(uid)

    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")],
    ]
    await update.message.reply_text(
        "🔥 SENX SENSI BOT\nChoose an option:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ================== BUTTON HANDLER ==================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    data = query.data

    if data == "free":
        reset_user(uid)
        user_state[uid] = "FREE_DEVICE"
        await query.message.reply_text("📱 Enter Device Name:")

    elif data == "vip":
        reset_user(uid)
        user_state[uid] = "VIP_WAIT"

        # Send QR if exists
        if os.path.exists(QR_PATH):
            await query.message.reply_photo(
                photo=InputFile(QR_PATH),
                caption=(
                    "💎 VIP SENSI ACCESS\n"
                    "💰 Price: ₹199\n"
                    "🆔 UPI ID: aryankumar6333@navi\n\n"
                    "Payment ke baad admin verify karega"
                ),
                parse_mode="Markdown",
            )
        else:
            await query.message.reply_text("❌ QR image missing (qr.png)")

        await query.message.reply_text(
            "🛡️ VIP ke liye admin verify karega.\n"
            "Admin command: /verifyvip USER_ID",
            parse_mode="Markdown",
        )

# ================== MESSAGE HANDLER ==================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()

    state = user_state.get(uid)

    # -------- FREE FLOW --------
    if state == "FREE_DEVICE":
        user_data[uid] = {"device": text}
        user_state[uid] = "FREE_RAM"
        await update.message.reply_text("💾 Enter RAM (e.g. 4):")
        return

    if state == "FREE_RAM":
        ram = safe_int(text)
        if ram is None:
            await update.message.reply_text("❌ RAM number me likho (e.g. 4)")
            return

        device = user_data[uid]["device"]

        sensi = random.randint(90, 120)
        fire = round(random.uniform(9.0, 12.0), 1)

        await update.message.reply_text(
            f"⚡ FREE SENSI\n"
            f"📱 {device}\n"
            f"💾 RAM: {ram}GB\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            f"*Sensi by AryanSenx*",
            parse_mode="Markdown",
        )

        reset_user(uid)
        return

    # -------- VIP BLOCK --------
    if state and state.startswith("VIP"):
        await update.message.reply_text("❌ VIP not verified.")
        return

# ================== ADMIN VERIFY ==================
async def verify_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_ID):
        await update.message.reply_text("❌ Admin only command")
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    uid = context.args[0]
    vip_users.add(uid)
    await update.message.reply_text(f"✅ VIP verified for {uid}")

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verify_vip))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if _name_ == "_main_":
    main()
