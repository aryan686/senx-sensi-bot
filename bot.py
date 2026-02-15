import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"
ADMIN_ID = 8130333205

UPI_ID = "aryankumar6333@navi"
VIP_PRICE = 199
SIGNATURE = "Sensi by AryanSenx"
# ========================================

user_state = {}
vip_users = set()

# ---------------- START -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "Type one option:\n"
        "1️⃣ Free Sensi\n"
        "2️⃣ VIP Sensi"
    )

# --------------- TEXT -------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    uid = update.effective_user.id

    # -------- FREE START --------
    if text == "free sensi":
        user_state[uid] = {"mode": "free", "step": 1}
        await update.message.reply_text("📱 Enter Device Name:")
        return

    # -------- VIP START --------
    if text == "vip sensi":
        if uid not in vip_users and uid != ADMIN_ID:
            try:
                with open("qr.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption=(
                            f"💎 VIP SENSI ₹{VIP_PRICE}\n"
                            f"UPI: {UPI_ID}\n\n"
                            "Payment ke baad admin verify karega.\n"
                            "Phir VIP sensi milega."
                        )
                    )
            except:
                await update.message.reply_text(
                    f"VIP SENSI ₹{VIP_PRICE}\nUPI: {UPI_ID}\n(QR missing)"
                )
            return

        user_state[uid] = {"mode": "vip", "step": 1}
        await update.message.reply_text("📱 Enter Device Name:")
        return

    # -------- STATE FLOW --------
    if uid not in user_state:
        return

    state = user_state[uid]

    # STEP 1 → DEVICE
    if state["step"] == 1:
        state["device"] = text
        state["step"] = 2
        await update.message.reply_text("💾 Enter RAM (number):")
        return

    # STEP 2 → RAM + RESULT
    if state["step"] == 2:
        try:
            ram = int(text)
        except:
            await update.message.reply_text("RAM number me likho (4,6,8)")
            return

        device = state["device"]

        if state["mode"] == "free":
            sensi = random.randint(105, 120)
        else:
            if uid not in vip_users and uid != ADMIN_ID:
                await update.message.reply_text("❌ VIP not verified.")
                return
            sensi = random.randint(150, 200)

        fire = round(sensi / 10, 1)

        await update.message.reply_text(
            f"🎯 RESULT\n\n"
            f"Device: {device}\n"
            f"RAM: {ram}GB\n\n"
            f"Sensi: {sensi}\n"
            f"Fire Button: {fire}\n\n"
            f"{SIGNATURE}"
        )

        user_state.pop(uid)
        return

# -------------- ADMIN -------------------
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
        await context.bot.send_message(uid, "✅ VIP activated. Type 'VIP Sensi'")
    except:
        pass

async def viptest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    vip_users.add(ADMIN_ID)
    await update.message.reply_text("🧪 VIP TEST ENABLED")

# -------------- MAIN --------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CommandHandler("viptest", viptest))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if _name_ == "_main_":
    main()
