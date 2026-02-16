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

# ============ ENV ============
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

# ============ CONFIG ============
VIP_PASSWORD = "SenxBot"          # Admin + VIP test password
UPI_ID = "aryankumar6333@navi"

# ============ USER STATE ============
USERS = {}

# ============ START ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    USERS[uid] = {"state": "idle"}

    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# ============ CALLBACKS ============
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    USERS.setdefault(uid, {"state": "idle"})
    st = USERS[uid]

    if q.data == "free":
        st.clear()
        st["state"] = "free_device"
        await q.message.reply_text("📱 Enter Device Name:")
        return

    if q.data == "vip":
        st.clear()
        st["state"] = "vip_password"
        await q.message.reply_text(
            f"💎 *VIP ACCESS*\n\n"
            f"Price: ₹199\n"
            f"UPI: `{UPI_ID}`\n\n"
            "Password paste karo 👇",
            parse_mode="Markdown"
        )
        return

    if q.data in ("low", "medium", "high") and st.get("vip"):
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
            f"💾 RAM: {st['ram']} GB\n"
            f"⚙️ Level: {q.data.title()}\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            "*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        return

    if q.data in ("free_fire", "vip_fire"):
        fire = round(random.uniform(9.5, 14.5), 1)
        await q.message.reply_text(f"🔥 New Fire: {fire}")

# ============ TEXT ============
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msg = update.message.text.strip()

    USERS.setdefault(uid, {"state": "idle"})
    st = USERS[uid]

    if st.get("state") == "vip_password":
        if msg == VIP_PASSWORD:
            st["vip"] = True
            st["state"] = "vip_device"
            await update.message.reply_text("✅ VIP Access Granted\n📱 Enter Device Name:")
        else:
            await update.message.reply_text("❌ Wrong password")
        return

    if st.get("state") == "free_device":
        st["device"] = msg
        st["state"] = "free_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    if st.get("state") == "free_ram":
        sensi = random.randint(95, 120)
        fire = round(random.uniform(9.5, 12.5), 1)

        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="free_fire")]]

        await update.message.reply_text(
            f"⚡ *FREE SENSI GENERATED*\n\n"
            f"📱 Device: {st['device']}\n"
            f"💾 RAM: {msg} GB\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            "*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        USERS[uid] = {"state": "idle"}
        return

    if st.get("state") == "vip_device":
        st["device"] = msg
        st["state"] = "vip_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    if st.get("state") == "vip_ram":
        st["ram"] = msg
        st["state"] = "vip_level"

        kb = [[
            InlineKeyboardButton("Low", callback_data="low"),
            InlineKeyboardButton("Medium", callback_data="medium"),
            InlineKeyboardButton("High", callback_data="high")
        ]]
        await update.message.reply_text(
            "⚙️ Choose Sensi Level:",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        return

# ============ MAIN ============
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
