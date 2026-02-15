import random
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =====================================================
# 🔴 CONFIG – YAHAN VALUE PASTE KARO
# =====================================================

BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"
ADMIN_ID = 8130333205
VIP_PRICE = 199
VIP_ACCESS_CODE = "SenxBot"

# =====================================================
# MEMORY (restart pe reset hota hai – normal hai)
# =====================================================
user_state = {}
pending_vip = set()
vip_users = set()

# =====================================================
# /start
# =====================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔥 Free Sensi"],
        ["💎 VIP Sensi ₹199"]
    ]
    await update.message.reply_text(
        "🔥 **SENX SENSI BOT** 🔥\n\nChoose option 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# =====================================================
# TEXT HANDLER (FREE + VIP FLOW)
# =====================================================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    # ---------- FREE START ----------
    if text == "🔥 Free Sensi":
        user_state[uid] = {"mode": "free", "step": "device"}
        await update.message.reply_text("📱 Enter Device Name:")
        return

    # ---------- VIP START ----------
    if text == "💎 VIP Sensi ₹199":
        pending_vip.add(uid)
        await update.message.reply_text(
            f"💎 **VIP SENSI** 💎\n\n"
            f"Price: ₹{VIP_PRICE}\n\n"
            f"UPI: aryankumar6333@navi\n\n"
            f"Pay using:\n"
            f"• Google Pay\n• PhonePe\n• Paytm\n• Navi\n\n"
            f"Payment ke baad admin verify karega.\n"
            f"Verification ke baad VIP unlock hoga.",
            parse_mode="Markdown"
        )
        return

    # ---------- STATE FLOW ----------
    if uid not in user_state:
        return

    state = user_state[uid]

    # DEVICE STEP
    if state["step"] == "device":
        state["device"] = text
        state["step"] = "ram"
        await update.message.reply_text("💾 Enter Phone RAM (GB):")
        return

    # RAM STEP
    if state["step"] == "ram":
        state["ram"] = text

        # FREE RESULT
        if state["mode"] == "free":
            sensi = random.randint(90, 150)
            fire = round(sensi / 2)

            await update.message.reply_text(
                f"🎯 **FREE SENSI GENERATED**\n\n"
                f"📱 Device: {state['device']}\n"
                f"💾 RAM: {state['ram']}\n\n"
                f"General: `{sensi}`\n"
                f"🔥 Fire Button: `{fire}%`\n\n"
                f"— Sensi by AryanSenx",
                parse_mode="Markdown"
            )
            user_state.pop(uid)
            return

        # VIP (after verify)
        if state["mode"] == "vip":
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
            return

# =====================================================
# VIP LEVEL BUTTONS
# =====================================================
async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if uid not in vip_users:
        await query.message.reply_text("❌ VIP not verified.")
        return

    if query.data == "vip_low":
        sensi = random.randint(90, 95)
    elif query.data == "vip_medium":
        sensi = random.randint(100, 150)
    else:
        sensi = random.randint(150, 200)

    fire = round(sensi / 1.8)

    await query.message.reply_text(
        f"💎 **VIP SENSI GENERATED** 💎\n\n"
        f"General: `{sensi}`\n"
        f"🔥 Fire Button: `{fire}%`\n\n"
        f"🔓 VIP ACCESS CODE: `{VIP_ACCESS_CODE}`\n\n"
        f"— Sensi by AryanSenx",
        parse_mode="Markdown"
    )

    user_state.pop(uid, None)

# =====================================================
# ADMIN VERIFY VIP (hidden)
# =====================================================
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /verifyvip <user_id>")
        return

    user_id = int(context.args[0])

    if user_id in pending_vip:
        pending_vip.remove(user_id)
        vip_users.add(user_id)
        user_state[user_id] = {"mode": "vip", "step": "device"}

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "✅ **VIP VERIFIED**\n\n"
                f"🔓 Access Code: `{VIP_ACCESS_CODE}`\n\n"
                "Enter Device Name to generate VIP sensi 🚀"
            ),
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ VIP Activated")
    else:
        await update.message.reply_text("❌ No pending VIP")

# =====================================================
# ADMIN VIP TEST (sirf tumhare liye)
# =====================================================
async def viptest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    vip_users.add(ADMIN_ID)
    user_state[ADMIN_ID] = {"mode": "vip", "step": "device"}

    await update.message.reply_text(
        "🧪 **VIP TEST MODE ENABLED**\n\n"
        f"Access Code: `{VIP_ACCESS_CODE}`\n"
        "Ab tum VIP flow test kar sakte ho.",
        parse_mode="Markdown"
    )

# =====================================================
# MAIN
# =====================================================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CommandHandler("viptest", viptest))
    app.add_handler(CallbackQueryHandler(vip_level))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
