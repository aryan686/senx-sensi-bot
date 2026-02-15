# bot.py
import os
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

# ================== CONFIG - Edit these ==================
BOT_TOKEN = "8564307153:AAFQ5D6un_WHjXmn6bpcXvk2OP75PotmIyA"   # <-- paste your Bot token here
ADMIN_ID = 8130333205                 # <-- paste your numeric Telegram ID here

UPI_ID = "aryankumar6333@navi"
VIP_PRICE = 199
QR_FILENAME = "qr.png"  # Put your qr.png in the same folder
SIGNATURE_TEXT = "Sensi by AryanSenx"     # signature text (displayed in result)
# =========================================================

if BOT_TOKEN == "PASTE_YOUR_BOT_TOKEN_HERE" or ADMIN_ID == 123456789:
    print("⚠️ Please set BOT_TOKEN and ADMIN_ID in bot.py before running.")
    # not raising: just a helpful console message

# Conversation states
FREE_DEVICE, FREE_RAM = range(2)
VIP_WAIT_PAY, VIP_DEVICE, VIP_RAM, VIP_LEVEL = range(4, 8)

# runtime VIP store (in-memory). For permanent store use DB.
vip_users = set()

# ---------------- start ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 <b>SENX SENSI BOT</b>\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML"
    )

# --------------- FREE FLOW ----------------
async def free_entry(callback_query, context):
    await callback_query.answer()
    await callback_query.message.reply_text("📱 Enter Device Name:")
    return FREE_DEVICE

async def free_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text.strip()
    await update.message.reply_text("💾 Enter RAM (GB) — just a number e.g. 4 or 6:")
    return FREE_RAM

async def free_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    try:
        ram = int(txt)
    except:
        await update.message.reply_text("Enter RAM as a number (e.g. 4 or 6). Try again:")
        return FREE_RAM

    device = context.user_data.get("device", "Unknown")
    # Free sensi: stable medium values
    sensi = random.randint(105, 120)
    fire = round(sensi / 10, 1)

    msg = (
        f"⚡ <b>FREE SENSI</b>\n"
        f"📱 <code>{device}</code>\n"
        f"💾 RAM: <b>{ram}GB</b>\n\n"
        f"🎯 Sensi: <b>{sensi}</b>\n"
        f"🔥 Fire size: <b>{fire}</b>\n\n"
        f"<b>{SIGNATURE_TEXT}</b>"
    )
    await update.message.reply_text(msg, parse_mode="HTML")
    return ConversationHandler.END

# --------------- VIP FLOW ----------------
async def vip_entry(callback_query, context):
    await callback_query.answer()
    user_id = callback_query.from_user.id

    if user_id in vip_users:
        # already VIP -> proceed to collect device
        await callback_query.message.reply_text("📱 Enter Device Name:")
        return VIP_DEVICE

    # not VIP -> show QR + instructions + command to submit ref
    caption = (
        f"💎 <b>VIP SENSI ACCESS</b>\n\n"
        f"💰 Price: ₹{VIP_PRICE}\n"
        f"💜 UPI ID: <b>{UPI_ID}</b>\n\n"
        "👉 Scan the QR or pay via UPI (GPay/PhonePe/Paytm/Navi).\n"
        "After paying, use the command:\n"
        "<code>/submitref YOUR_PAYMENT_REF</code>\n"
        "You can also send payment screenshot to the admin.\n\n"
        "Admin will verify payment and then grant VIP."
    )
    # send photo if available, else send text
    if os.path.exists(QR_FILENAME):
        with open(QR_FILENAME, "rb") as f:
            await callback_query.message.reply_photo(photo=InputFile(f), caption=caption, parse_mode="HTML")
    else:
        # fallback if image missing
        await callback_query.message.reply_text(
            caption + "\n\n⚠️ QR image missing on server. Admin must upload qr.png",
            parse_mode="HTML"
        )

    await callback_query.message.reply_text(
        "When paid, send: /submitref REF_CODE (or attach screenshot + message to admin)."
    )
    return ConversationHandler.END

async def vip_device(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["device"] = update.message.text.strip()
    await update.message.reply_text("💾 Enter RAM (GB) — just a number e.g. 4 or 6:")
    return VIP_RAM

async def vip_ram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    try:
        ram = int(txt)
    except:
        await update.message.reply_text("Enter RAM as a number (e.g. 4 or 6). Try again:")
        return VIP_RAM
    context.user_data["ram"] = ram

    kb = [
        [
            InlineKeyboardButton("Low", callback_data="vip_low"),
            InlineKeyboardButton("Medium", callback_data="vip_medium"),
            InlineKeyboardButton("High", callback_data="vip_high"),
        ]
    ]
    await update.message.reply_text("⚙️ Choose Sensi Level:", reply_markup=InlineKeyboardMarkup(kb))
    return VIP_LEVEL

async def vip_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    level_data = update.callback_query.data  # vip_low / vip_medium / vip_high
    level = level_data.split("_")[1]

    device = context.user_data.get("device", "Unknown")
    ram = context.user_data.get("ram", 4)

    # Sensitivity rules you requested:
    # Low  -> 90-95 (user wanted 90-95 if ram>4; keep stable 90-95)
    # Medium -> 100-150
    # High -> 150-200
    if level == "low":
        sensi = random.randint(90, 95)
    elif level == "medium":
        sensi = random.randint(100, 150)
    else:  # high
        sensi = random.randint(150, 200)

    # Keep final RANGES: ensure not below requested mins
    if level == "high" and sensi < 150:
        sensi = 150
    fire = round(sensi / 10, 1)

    await update.callback_query.message.reply_text(
        f"💎 <b>VIP SENSI</b>\n"
        f"📱 <code>{device}</code>\n"
        f"💾 RAM: <b>{ram}GB</b>\n"
        f"⚙️ Level: <b>{level.upper()}</b>\n\n"
        f"🎯 Sensi: <b>{sensi}</b>\n"
        f"🔥 Fire size: <b>{fire}</b>\n\n"
        f"<b>{SIGNATURE_TEXT}</b>",
        parse_mode="HTML"
    )
    return ConversationHandler.END

# ============== Submit payment reference ==============
async def submitref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user runs: /submitref REF_CODE
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("Usage: /submitref YOUR_REFERENCE_CODE\nAttach screenshot if available.")
        return
    ref = " ".join(context.args)
    # forward to admin
    admin_msg = (
        f"🔔 Payment submission from @{user.username or user.first_name} (id: {user.id})\n\n"
        f"Reference: {ref}\n\n"
        "Check payment and run:\n"
        f"/verifyvip {user.id}"
    )
    # forward any attached photo along with message
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        # user included a photo in reply -> forward that photo to admin
        await update.message.reply_to_message.forward(chat_id=ADMIN_ID)
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)
    await update.message.reply_text("✅ Reference submitted. Admin will verify and then you will get VIP access.")

# ============== Admin verify command ==============
async def verifyvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # admin only
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not admin.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /verifyvip USER_ID")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid USER_ID.")
        return
    vip_users.add(uid)
    await update.message.reply_text(f"✅ User {uid} is now VIP.")
    # inform user
    try:
        await context.bot.send_message(chat_id=uid, text="✅ Your payment is verified. You are now VIP. Use /start to begin.")
    except Exception as e:
        await update.message.reply_text(f"Could not notify user: {e}")

# ============== Admin VIP test (simulate) ==============
async def viptest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("You are not admin.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /viptest USER_ID   (grants vip for testing only)")
        return
    uid = int(context.args[0])
    vip_users.add(uid)
    await update.message.reply_text(f"VIP test: {uid} granted VIP (runtime).")

# simple /whoami helper
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Your id: {user.id}\nusername: @{user.username or ''}")

# fallback cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# ================ Setup & Run ================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Free conversation
    free_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(lambda q, c: free_entry(q, c), pattern="free")],
        states={
            FREE_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_device)],
            FREE_RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_ram)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True
    )

    # VIP conversation (only enters full vip device flow when user already verified)
    vip_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(lambda q, c: vip_entry(q, c), pattern="vip")],
        states={
            VIP_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_device)],
            VIP_RAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, vip_ram)],
            VIP_LEVEL: [CallbackQueryHandler(vip_level, pattern="vip_.*")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(free_conv)
    app.add_handler(vip_conv)
    app.add_handler(CommandHandler("submitref", submitref))
    app.add_handler(CommandHandler("verifyvip", verifyvip))
    app.add_handler(CommandHandler("viptest", viptest))
    app.add_handler(CommandHandler("whoami", whoami))  # helpful

    print("Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
