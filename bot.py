import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ========== ENV ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN or ADMIN_ID == 0:
    raise RuntimeError("BOT_TOKEN / ADMIN_ID missing")

# ========== CONFIG ==========
VIP_PASSWORD = "SenxBot"
UPI_ID = "aryankumar6333@navi"
PRICE = "₹199"
QR_URL = "https://i.imgur.com/6QpK0Zk.png"

# ========== USER STATE ==========
users = {}

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    users[uid] = {}

    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# ========== BUTTON HANDLER ==========
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    users.setdefault(uid, {})

    # FREE
    if q.data == "free":
        users[uid] = {"mode": "free_device"}
        await q.message.reply_text("📱 Enter Device Name:")

    # VIP
    elif q.data == "vip":
        if uid == ADMIN_ID:
            users[uid] = {"mode": "vip_password", "vip": True}
            await q.message.reply_text("🔑 Enter VIP Password:")
        else:
            users[uid] = {"mode": "vip_wait"}
            await q.message.reply_text(
                f"💎 *VIP SENSI ACCESS*\n\n"
                f"Price: {PRICE}\n"
                f"UPI ID: `{UPI_ID}`\n\n"
                f"📷 QR: {QR_URL}\n\n"
                "Payment ke baad password paste karo 👇",
                parse_mode="Markdown"
            )

    # VIP LEVEL BUTTONS
    elif q.data in ["low", "medium", "high"]:
        st = users.get(uid, {})
        if not st.get("vip"):
            return

        if q.data == "low":
            sensi = random.randint(90, 95)
        elif q.data == "medium":
            sensi = random.randint(100, 150)
        else:
            sensi = random.randint(150, 200)

        fire = round(random.uniform(10.0, 14.5), 1)

        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="vip_fire")]]

        await q.message.reply_text(
            f"💎 *VIP SENSI GENERATED*\n\n"
            f"📱 Device: {st['device']}\n"
            f"💾 RAM: {st['ram']}\n"
            f"⚙️ Level: {q.data.title()}\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            "*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )

    # RANDOM FIRE
    elif q.data in ["free_fire", "vip_fire"]:
        fire = round(random.uniform(9.5, 14.5), 1)
        await q.message.reply_text(f"🔥 New Fire: {fire}")

# ========== TEXT HANDLER ==========
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    txt = update.message.text
    st = users.setdefault(uid, {})

    # VIP PASSWORD
    if st.get("mode") == "vip_wait":
        if txt == VIP_PASSWORD:
            st["vip"] = True
            st["mode"] = "vip_device"
            await update.message.reply_text("✅ VIP Access Granted\n📱 Enter Device Name:")
        else:
            await update.message.reply_text("❌ Wrong password")
        return

    # FREE DEVICE
    if st.get("mode") == "free_device":
        st["device"] = txt
        st["mode"] = "free_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    # FREE RAM
    if st.get("mode") == "free_ram":
        sensi = random.randint(95, 120)
        fire = round(random.uniform(9.5, 12.5), 1)

        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="free_fire")]]

        await update.message.reply_text(
            f"⚡ *FREE SENSI GENERATED*\n\n"
            f"📱 Device: {st['device']}\n"
            f"💾 RAM: {txt}\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            "*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        users[uid] = {}
        return

    # VIP DEVICE
    if st.get("mode") == "vip_device":
        st["device"] = txt
        st["mode"] = "vip_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    # VIP RAM
    if st.get("mode") == "vip_ram":
        st["ram"] = txt
        kb = [[
            InlineKeyboardButton("Low", callback_data="low"),
            InlineKeyboardButton("Medium", callback_data="medium"),
            InlineKeyboardButton("High", callback_data="high"),
        ]]
        await update.message.reply_text(
            "⚙️ Choose Sensi Level:",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        st["mode"] = "vip_level"

# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    app.run_polling(drop_pending_updates=True)

if __name__ == "
