import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

# ===== CONFIG =====
VIP_PASSWORD = "SenxBot"
UPI_ID = "aryankumar6333@navi"

# ===== STATE =====
USERS = {}

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    USERS[uid] = {"step": None}

    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown"
    )

# ===== CALLBACKS =====
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    USERS.setdefault(uid, {})

    if q.data == "free":
        USERS[uid] = {"step": "free_device"}
        await q.message.reply_text("📱 Enter Device Name:")

    elif q.data == "vip":
        USERS[uid] = {"step": "vip_password"}
        await q.message.reply_text(
            f"💎 *VIP ACCESS*\n\n₹199\nUPI: `{UPI_ID}`\n\nPassword paste karo 👇",
            parse_mode="Markdown"
        )

    elif q.data in ["low", "medium", "high"] and USERS[uid].get("vip"):
        if q.data == "low":
            sensi = random.randint(90, 95)
        elif q.data == "medium":
            sensi = random.randint(100, 150)
        else:
            sensi = random.randint(150, 200)

        fire = round(random.uniform(10, 14), 1)
        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="fire")]]

        await q.message.reply_text(
            f"💎 *VIP SENSI GENERATED*\n\n"
            f"📱 Device: {USERS[uid]['device']}\n"
            f"💾 RAM: {USERS[uid]['ram']} GB\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            "*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )

    elif q.data == "fire":
        fire = round(random.uniform(9.5, 14.5), 1)
        await q.message.reply_text(f"🔥 New Fire: {fire}")

# ===== TEXT =====
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msg = update.message.text.strip()
    USERS.setdefault(uid, {})

    if USERS[uid].get("step") == "vip_password":
        if msg == VIP_PASSWORD:
            USERS[uid]["vip"] = True
            USERS[uid]["step"] = "vip_device"
            await update.message.reply_text("📱 Enter Device Name:")
        else:
            await update.message.reply_text("❌ Wrong password")
        return

    if USERS[uid].get("step") == "free_device":
        USERS[uid]["device"] = msg
        USERS[uid]["step"] = "free_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    if USERS[uid].get("step") == "free_ram":
        sensi = random.randint(95, 120)
        fire = round(random.uniform(9.5, 12.5), 1)
        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="fire")]]

        await update.message.reply_text(
            f"⚡ *FREE SENSI GENERATED*\n\n"
            f"📱 Device: {USERS[uid]['device']}\n"
            f"💾 RAM: {msg} GB\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            "*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        USERS[uid] = {}
        return

    if USERS[uid].get("step") == "vip_device":
        USERS[uid]["device"] = msg
        USERS[uid]["step"] = "vip_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    if USERS[uid].get("step") == "vip_ram":
        USERS[uid]["ram"] = msg
        USERS[uid]["step"] = "vip_level"
        kb = [[
            InlineKeyboardButton("Low", callback_data="low"),
            InlineKeyboardButton("Medium", callback_data="medium"),
            InlineKeyboardButton("High", callback_data="high")
        ]]
        await update.message.reply_text(
            "⚙️ Choose Sensi Level:",
            reply_markup=InlineKeyboardMarkup(kb)
        )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
