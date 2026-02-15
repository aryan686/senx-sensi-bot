import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"
ADMIN_ID = 8130333205     # ← apna Telegram numeric ID
UPI_ID = "aryankumar6333@navi"
VIP_PRICE = 199
SIGNATURE = "🔥 *ARYAN* | *SENX* 🔥"
# ==========================================

# user states
user_state = {}
vip_users = set()

# ============== /start ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["⚡ Free Sensi"],
        ["💎 VIP Sensi"]
    ]
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\nChoose option 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ============== TEXT HANDLER ===============
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    uid = update.effective_user.id

    # ---------- FREE START ----------
    if text == "⚡ Free Sensi":
        user_state[uid] = {"mode": "free", "step": "device"}
        await update.message.reply_text("📱 Enter Device Name:")
        return

    # ---------- VIP START ----------
    if text == "💎 VIP Sensi":
        if uid not in vip_users and uid != ADMIN_ID:
            try:
                with open("qr.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption=(
                            f"💎 VIP SENSI ACCESS\n\n"
                            f"Price: ₹{VIP_PRICE}\n"
                            f"UPI ID: {UPI_ID}\n\n"
                            "Pay via GPay / PhonePe / Paytm / Navi\n"
                            "Payment ke baad admin verify karega."
                        )
                    )
            except:
                await update.message.reply_text(
                    f"💎 VIP SENSI ACCESS\n\n"
                    f"Price: ₹{VIP_PRICE}\n"
                    f"UPI ID: {UPI_ID}\n\n"
                    "(QR image missing)"
                )
            return
        else:
            user_state[uid] = {"mode": "vip", "step": "device"}
            await update.message.reply_text("📱 Enter Device Name:")
            return

    # ---------- STATE FLOW ----------
    if uid not in user_state:
        return

    state = user_state[uid]

    # DEVICE STEP
    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    # RAM STEP
    if state["step"] == "ram":
        try:
            ram = int(text)
        except:
            await update.message.reply_text("❌ RAM number me likho (4,6,8)")
            return

        device = state["device"]

        # ---------- FREE RESULT ----------
        if state["mode"] == "free":
            sensi = random.randint(105, 120)
            fire = round(sensi / 10, 1)

            await update.message.reply_text(
                f"⚡ FREE SENSI\n\n"
                f"Device: {device}\n"
                f"RAM: {ram}GB\n\n"
                f"Sensi: {sensi}\n"
                f"Fire Button: {fire}\n\n"
                f"{SIGNATURE}"
            )
            user_state.pop(uid)
            return

        # ---------- VIP RESULT ----------
        if state["mode"] == "vip":
            if uid not in vip_users and uid != ADMIN_ID:
                await update.message.reply_text("❌ VIP not verified.")
                return

            sensi = random.randint(150, 200)
            fire = round(sensi / 10, 1)

            await update.message.reply_text(
                f"💎 VIP SENSI\n\n"
                f"Device: {device}\n"
                f"RAM: {ram}GB\n\n"
                f"Sensi: {sensi}\n"
                f"Fire Button: {fire}\n\n"
                f"{SIGNATURE}"
            )
            user_state.pop(uid)
            return

# ============== ADMIN VERIFY ===============
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    uid = int(context.args[0])
    vip_users.add(uid)
    await update.message.reply_text("✅ VIP verified")
    try:
        await context.bot.send_message(uid, "✅ VIP activated. Use VIP Sensi now.")
    except:
        pass

# ============== ADMIN TEST ================
async def viptest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    vip_users.add(ADMIN_ID)
    await update.message.reply_text("🧪 VIP TEST ENABLED")

# ============== MAIN ======================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CommandHandler("viptest", viptest))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if _name_ == "_main_":
    main()
