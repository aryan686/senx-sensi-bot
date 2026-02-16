import os
import random
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

# ========== ENV ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN or ADMIN_ID == 0:
    raise RuntimeError("BOT_TOKEN or ADMIN_ID missing")

# ========== CONFIG ==========
UPI_ID = "aryankumar6333@navi"
PRICE = "₹199"
QR_URL = "https://i.imgur.com/6QpK0Zk.png"
VIP_PASSWORD = "SenxBot"

# ========== STATES ==========
(
    FREE_DEVICE, FREE_RAM,
    VIP_UTR, VIP_PASSWORD_STATE,
    VIP_DEVICE, VIP_RAM, VIP_LEVEL
) = range(7)

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")],
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown",
    )

# ========== FREE ==========
async def free_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("📱 Enter Device Name:")
    return FREE_DEVICE

async def free_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text
    await update.message.reply_text("💾 Enter RAM (GB):")
    return FREE_RAM

async def free_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sensi = random.randint(95, 120)
    fire = round(random.uniform(9.5, 12.5), 1)

    context.user_data["fire"] = fire

    kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="free_fire")]]

    await update.message.reply_text(
        f"⚡ *FREE SENSI GENERATED*\n\n"
        f"📱 Device: {context.user_data['device']}\n"
        f"💾 RAM: {update.message.text}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}\n\n"
        "*Sensi By AryanSenxSensi*",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown",
    )
    return ConversationHandler.END

async def free_fire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    fire = round(random.uniform(9.5, 12.5), 1)
    await update.callback_query.message.reply_text(f"🔥 New Fire: {fire}")

# ========== VIP ==========
async def vip_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = update.callback_query.from_user.id

    if user_id == ADMIN_ID:
        await update.callback_query.message.reply_text(
            "✅ Admin access granted\n\nPaste VIP Password:"
        )
        return VIP_PASSWORD_STATE

    await update.callback_query.message.reply_text(
        f"💎 *VIP SENSI ACCESS*\n\n"
        f"Price: {PRICE}\n"
        f"UPI ID: `{UPI_ID}`\n\n"
        f"📷 QR: {QR_URL}\n\n"
        "Payment ke baad UTR paste karo 👇",
        parse_mode="Markdown",
    )
    return VIP_UTR

async def vip_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⏳ Payment noted\nAdmin verify ke baad password milega."
    )
    return VIP_PASSWORD_STATE

async def vip_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != VIP_PASSWORD:
        await update.message.reply_text("❌ Wrong password")
        return VIP_PASSWORD_STATE

    await update.message.reply_text("✅ VIP Access Granted\n📱 Enter Device Name:")
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
        "⚙️ Choose Sensi Level:",
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

    fire = round(random.uniform(10.0, 14.5), 1)

    kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="vip_fire")]]

    await update.callback_query.message.reply_text(
        f"💎 *VIP SENSI GENERATED*\n\n"
        f"📱 Device: {context.user_data['device']}\n"
        f"💾 RAM: {context.user_data['ram']}\n"
        f"⚙️ Level: {level.title()}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}\n\n"
        "*Sensi By AryanSenxSensi*",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown",
    )
    return ConversationHandler.END

async def vip_fire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    fire = round(random.uniform(10.0, 14.5), 1)
    await update.callback_query.message.reply_text(f"🔥 New Fire: {fire}")

# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(free_fire, pattern="^free_fire$"))
    app.add_handler(CallbackQueryHandler(vip_fire, pattern="^
