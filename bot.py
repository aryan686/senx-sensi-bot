import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")
if ADMIN_ID == 0:
    raise RuntimeError("ADMIN_ID missing")

# ===== STATES =====
(
    FREE_DEVICE, FREE_RAM,
    VIP_UTR, VIP_PASSWORD,
    VIP_DEVICE, VIP_RAM, VIP_LEVEL
) = range(7)

VIP_PASSWORDS = {}
VIP_VERIFIED = set()

UPI_ID = "aryankumar6333@navi"
QR_URL = "https://i.imgur.com/6QpK0Zk.png"   # ✅ QR IMAGE URL
PRICE = "₹199"

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")],
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown",
    )

# ================= FREE =================
async def free_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("📱 Enter device name:")
    return FREE_DEVICE

async def free_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text
    await update.message.reply_text("💾 Enter RAM (GB):")
    return FREE_RAM

async def free_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sensi = random.randint(95, 120)
    fire = round(random.uniform(9.5, 12.0), 1)

    await update.message.reply_text(
        f"⚡ *FREE SENSI*\n\n"
        f"📱 Device: {context.user_data['device']}\n"
        f"💾 RAM: {update.message.text}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}",
        parse_mode="Markdown",
    )
    return ConversationHandler.END

# ================= VIP =================
async def vip_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    await update.callback_query.message.reply_text(
        f"💎 *VIP SENSI ACCESS*\n\n"
        f"Price: {PRICE}\n"
        f"UPI ID: `{UPI_ID}`\n\n"
        f"📷 QR: {QR_URL}\n\n"
        "Payment ke baad *UTR paste karo* 👇",
        parse_mode="Markdown",
    )
    return VIP_UTR

async def vip_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    utr = update.message.text

    password = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    VIP_PASSWORDS[user_id] = password

    await context.bot.send_message(
        ADMIN_ID,
        f"💎 VIP REQUEST\nUser: {user_id}\nUTR: {utr}\nPassword: {password}",
    )

    await update.message.reply_text(
        "⏳ Payment received\nWait 5 minutes — admin verify karega.",
    )
    return VIP_PASSWORD

async def vip_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in VIP_VERIFIED:
        await update.message.reply_text("❌ Admin verification pending")
        return VIP_PASSWORD

    if update.message.text != VIP_PASSWORDS.get(user_id):
        await update.message.reply_text("❌ Wrong password")
        return VIP_PASSWORD

    await update.message.reply_text("✅ Access granted\n📱 Enter device name:")
    return VIP_DEVICE

async def vip_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text
    await update.message.reply_text("💾 Enter RAM (GB):")
    return VIP_RAM

async def vip_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ram"] = update.message.text

    kb = [[
        InlineKeyboardButton("Low", callback_data="low"),
        InlineKeyboardButton("Medium", callback_data="medium"),
        InlineKeyboardButton("High", callback_data="high"),
    ]]
    await update.message.reply_text(
        "⚙️ Choose sensi level:",
        reply_markup=InlineKeyboardMarkup(kb),
    )
    return VIP_LEVEL

async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    level = update.callback_query.data

    if level == "low":
        sensi = random.randint(90, 95)
    elif level == "medium":
        sensi = random.randint(100, 150)
    else:
        sensi = random.randint(150, 200)

    fire = round(random.uniform(10.0, 14.0), 1)

    await update.callback_query.message.reply_text(
        f"💎 *VIP SENSI*\n\n"
        f"📱 Device: {context.user_data['device']}\n"
        f"💾 RAM: {context.user_data['ram']}\n"
        f"⚙️ Level: {level.title()}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}",
        parse_mode="Markdown",
    )
    return ConversationHandler.END

# ================= ADMIN =================
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    user_id = int(context.args[0])
    VIP_VERIFIED.add(user_id)

    await context.bot.send_message(
        user_id,
        f"✅ VIP VERIFIED\nPassword: `{VIP_PASSWORDS[user_id]}`\nPaste it here 👇",
        parse_mode="Markdown",
    )

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verifyvip))

    app.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(free_entry, pattern="^free$")],
        states={
            FREE_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_device)],
            FREE_RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_ram)],
        },
        fallbacks=[],
    ))

    app.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(vip_entry, pattern="^vip$")],
        states={
            VIP_UTR: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_utr)],
            VIP_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_password)],
            VIP_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_device)],
            VIP_RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_ram)],
            VIP_LEVEL: [CallbackQueryHandler(vip_level)],
        },
        fallbacks=[],
    ))

    app.run_polling()

if __name__ == "__main__":
    main()
