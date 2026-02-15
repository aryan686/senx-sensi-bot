import random
import os
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
SIGNATURE = "🔥 Sensi by AryanSenx 🔥"
# =========================================

# runtime memory
user_flow = {}   # uid -> {"mode": free/vip, "step": device/ram, "device": str}
vip_users = set()

# ================ START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\n"
        "Type exactly:\n"
        "➡ Free Sensi\n"
        "➡ VIP Sensi"
    )

# ============== MAIN TEXT HANDLER =========
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()

    # ---------- FREE ENTRY ----------
    if text.lower() == "free sensi":
        user_flow[uid] = {"mode": "free", "step": "device"}
        await update.message.reply_text("📱 Enter Device Name:")
        return

    # ---------- VIP ENTRY ----------
    if text.lower() == "vip sensi":
        if uid not in vip_users and uid != ADMIN_ID:
            if os.path.exists("qr.png"):
                with open("qr.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption=(
                            f"💎 VIP SENSI\n"
                            f"Price: ₹{VIP_PRICE}\n"
                            f"UPI ID: {UPI_ID}\n\n"
                            "Payment ke baad admin verify karega."
                        )
                    )
            else:
                await update.message.reply_text(
                    f"VIP SENSI ₹{VIP_PRICE}\nUPI: {UPI_ID}\n(QR missing)"
                )
            return

        user_flow[uid] = {"mode": "vip", "step": "device"}
        await update.message.reply_text("📱 Enter Device Name:")
        return

    # ---------- CONTINUE FLOW ----------
    if uid not in user_flow:
        return

    state = user_flow[uid]

    # DEVICE STEP
    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter RAM (number only):")
        return

    # RAM STEP
    if state["step"] == "ram":
        try:
            ram = int(text)
        except:
            await update.message.reply_text("❌ RAM number me likho (4,6,8)")
            return

        device = state["device"]

        # FREE RESULT
        if state["mode"] == "free":
            sensi = random.randint(105, 120)

        # VIP RESULT
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

        user_flow.pop(uid)
        return

# ============== ADMIN COMMANDS ============
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return
    vip_users.add(int(context.args[0]))
    await update.message.reply_text("✅ VIP verified")

async def viptest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    vip_users.add(ADMIN_ID)
    await update.message.reply_text("🧪 VIP test enabled")

# ============== MAIN ======================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CommandHandler("viptest", viptest))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.run_polling()

if _name_ == "_main_":
    main()
