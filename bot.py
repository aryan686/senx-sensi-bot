import os
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ================== ENV ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")
if ADMIN_ID == 0:
    raise RuntimeError("ADMIN_ID missing")

# ================== STATES ==================
FREE_DEVICE, FREE_RAM = range(2)
VIP_DEVICE, VIP_RAM, VIP_LEVEL = range(3)

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")],
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )

# ================== FREE FLOW ==================
async def free_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("📱 Enter Device Name:")
    return FREE_DEVICE

async def free_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text
    await update.message.reply_text("💾 Enter RAM (e.g. 4GB / 6GB):")
    return FREE_RAM

async def free_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ram = update.message.text
    device = context.user_data.get("device", "Unknown")

    sensi = random.randint(105, 120)
    fire = round(random.uniform(10.5, 12.5), 1)

    text = (
        "⚡ *FREE SENSI GENERATED*\n\n"
        f"📱 Device: {device}\n"
        f"💾 RAM: {ram}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}\n\n"
        "🖤❤️ *Sensi by AryanSenx*"
    )

    await update.message.reply_text(text, parse_mode="Markdown")
    return ConversationHandler.END

# ================== VIP FLOW ==================
async def vip_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    vip_users = context.application.bot_data.get("vip_users", set())
    user_id = update.callback_query.from_user.id

    if user_id not in vip_users and user_id != ADMIN_ID:
        await update.callback_query.message.reply_text(
            "💎 *VIP ACCESS REQUIRED*\n\n"
            "Price: ₹199\n"
            "UPI ID: aryankumar6333@navi\n\n"
            "Payment ke baad admin verify karega.",
            parse_mode="Markdown",
        )
        return ConversationHandler.END

    await update.callback_query.message.reply_text("📱 Enter Device Name:")
    return VIP_DEVICE

async def vip_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text
    await update.message.reply_text("💾 Enter RAM (e.g. 4GB / 6GB):")
    return VIP_RAM

async def vip_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ram"] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("Low", callback_data="vip_low"),
            InlineKeyboardButton("Medium", callback_data="vip_medium"),
            InlineKeyboardButton("High", callback_data="vip_high"),
        ]
    ]
    await update.message.reply_text(
        "⚙️ Choose Sensi Level:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return VIP_LEVEL

async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    level = update.callback_query.data
    device = context.user_data.get("device")
    ram = context.user_data.get("ram")

    if level == "vip_low":
        sensi, fire = 90, 9.0
    elif level == "vip_medium":
        sensi, fire = 100, 10.0
    else:
        sensi, fire = 110, 11.0

    text = (
        "💎 *VIP SENSI GENERATED*\n\n"
        f"📱 Device: {device}\n"
        f"💾 RAM: {ram}\n"
        f"⚙️ Level: {level.replace('vip_', '').title()}\n\n"
        f"🎯 Sensi: {sensi}\n"
        f"🔥 Fire: {fire}\n\n"
        "🖤❤️ *Sensi by AryanSenx*"
    )

    await update.callback_query.message.reply_text(text, parse_mode="Markdown")
    return ConversationHandler.END

# ================== ADMIN VERIFY ==================
async def verify_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
    except:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return

    vip_users = context.application.bot_data.setdefault("vip_users", set())
    vip_users.add(user_id)

    await update.message.reply_text(f"✅ VIP Verified for {user_id}")

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    free_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(free_entry, pattern="^free$")],
        states={
            FREE_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_device)],
            FREE_RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_ram)],
        },
        fallbacks=[],
    )

    vip_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(vip_entry, pattern="^vip$")],
        states={
            VIP_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_device)],
            VIP_RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_ram)],
            VIP_LEVEL: [CallbackQueryHandler(vip_level)],
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verifyvip", verify_vip))
    app.add_handler(free_conv)
    app.add_handler(vip_conv)

    app.run_polling()

if __name__ == "__main__":
    main()
