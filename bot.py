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

# ================= ENV (SAFE LOAD) =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_RAW = os.getenv("ADMIN_ID")

ADMIN_ID = int(ADMIN_ID_RAW) if ADMIN_ID_RAW and ADMIN_ID_RAW.isdigit() else None

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

# ================= CONFIG =================
VIP_PASSWORD = "SenxBot"
UPI_ID = "aryankumar6333@navi"
QR_URL = "https://i.imgur.com/6QpK0Zk.png"

# ================= STATE STORE =================
USERS = {}   # user_id -> state dict

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    USERS[uid] = {"state": "idle"}

    kb = [
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Sensi", callback_data="vip")],
    ]
    await update.message.reply_text(
        "🔥 *SENX SENSI BOT*\n\nChoose option:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="Markdown",
    )

# ================= CALLBACKS =================
async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    USERS.setdefault(uid, {"state": "idle"})
    st = USERS[uid]

    # -------- FREE --------
    if q.data == "free":
        st.clear()
        st["state"] = "free_device"
        await q.message.reply_text("📱 Enter Device Name:")
        return

    # -------- VIP --------
    if q.data == "vip":
        st.clear()

        if ADMIN_ID and uid == ADMIN_ID:
            st["state"] = "vip_password"
            st["vip"] = True
            await q.message.reply_text("🔑 Enter VIP Password:")
        else:
            st["state"] = "vip_password"
            await q.message.reply_text(
                f"💎 *VIP ACCESS*\n\n"
                f"₹199\n"
                f"UPI: `{UPI_ID}`\n"
                f"QR: {QR_URL}\n\n"
                "Payment ke baad password paste karo 👇",
                parse_mode="Markdown",
            )
        return

    # -------- VIP LEVEL --------
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
            parse_mode="Markdown",
        )
        return

    # -------- RANDOM FIRE --------
    if q.data in ("free_fire", "vip_fire"):
        fire = round(random.uniform(9.5, 14.5), 1)
        await q.message.reply_text(f"🔥 New Fire: {fire}")
        return

# ================= TEXT =================
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msg = update.message.text.strip()

    USERS.setdefault(uid, {"state": "idle"})
    st = USERS[uid]

    # VIP PASSWORD
    if st.get("state") == "vip_password":
        if msg == VIP_PASSWORD:
            st["vip"] = True
            st["state"] = "vip_device"
            await update.message.reply_text("✅ VIP Access Granted\n📱 Enter Device Name:")
        else:
