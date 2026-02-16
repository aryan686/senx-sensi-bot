import os, random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# ---- ENV (ONLY ONE SECRET) ----
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

# ---- CONFIG ----
VIP_PASSWORD = "SenxBot"
UPI_ID = "aryankumar6333@navi"

# ---- STATE ----
U = {}  # user_id -> dict

# ---- START ----
async def start(update, ctx):
    uid = update.effective_user.id
    U[uid] = {"step": None}
    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")]
    ]
    await update.message.reply_text(
        "🔥 SENX SENSI BOT\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

# ---- CALLBACKS ----
async def cb(update, ctx):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    U.setdefault(uid, {})

    if q.data == "free":
        U[uid] = {"step": "free_device"}
        await q.message.reply_text("📱 Enter Device Name:")
        return

    if q.data == "vip":
        U[uid] = {"step": "vip_pass"}
        await q.message.reply_text(
            f"💎 VIP ACCESS\n₹199\nUPI: {UPI_ID}\n\nPassword paste karo"
        )
        return

    if q.data in ("low","medium","high") and U[uid].get("vip"):
        sensi = random.randint(90,95) if q.data=="low" else \
                random.randint(100,150) if q.data=="medium" else \
                random.randint(150,200)
        fire = round(random.uniform(10,14.5),1)
        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="fire")]]
        await q.message.reply_text(
            f"💎 VIP SENSI\n"
            f"📱 {U[uid]['device']}\n"
            f"💾 {U[uid]['ram']} GB\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            f"*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        return

    if q.data == "fire":
        await q.message.reply_text(f"🔥 New Fire: {round(random.uniform(9.5,14.5),1)}")

# ---- TEXT ----
async def text(update, ctx):
    uid = update.effective_user.id
    msg = update.message.text.strip()
    U.setdefault(uid, {})

    if U[uid].get("step") == "vip_pass":
        if msg == VIP_PASSWORD:
            U[uid]["vip"] = True
            U[uid]["step"] = "vip_device"
            await update.message.reply_text("📱 Enter Device Name:")
        else:
            await update.message.reply_text("❌ Wrong password")
        return

    if U[uid].get("step") == "free_device":
        U[uid]["device"] = msg
        U[uid]["step"] = "free_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    if U[uid].get("step") == "free_ram":
        sensi = random.randint(95,120)
        fire = round(random.uniform(9.5,12.5),1)
        kb = [[InlineKeyboardButton("🔥 Random Fire", callback_data="fire")]]
        await update.message.reply_text(
            f"⚡ FREE SENSI\n"
            f"📱 {U[uid]['device']}\n"
            f"💾 {msg} GB\n\n"
            f"🎯 Sensi: {sensi}\n"
            f"🔥 Fire: {fire}\n\n"
            f"*Sensi By AryanSenxSensi*",
            reply_markup=InlineKeyboardMarkup(kb),
            parse_mode="Markdown"
        )
        U[uid] = {}
        return

    if U[uid].get("step") == "vip_device":
        U[uid]["device"] = msg
        U[uid]["step"] = "vip_ram"
        await update.message.reply_text("💾 Enter RAM (GB):")
        return

    if U[uid].get("step") == "vip_ram":
        U[uid]["ram"] = msg
        kb = [[
            InlineKeyboardButton("Low", callback_data="low"),
            InlineKeyboardButton("Medium", callback_data="medium"),
            InlineKeyboardButton("High", callback_data="high"),
        ]]
        await update.message.reply_text("Choose level:", reply_markup=InlineKeyboardMarkup(kb))
        return

# ---- MAIN ----
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    app.run_polling()

if __name__ == "__main__":
    main()
