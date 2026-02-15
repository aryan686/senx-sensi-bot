import os
import time
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# ===== MEMORY STORES (simple, restart pe reset honge) =====
VIP_USERS = set()
LAST_USED = {}   # user_id -> timestamp
COOLDOWN = 30    # seconds

# ===== HELPERS =====
def in_cooldown(user_id: int) -> int:
    now = time.time()
    last = LAST_USED.get(user_id, 0)
    if now - last < COOLDOWN:
        return int(COOLDOWN - (now - last))
    LAST_USED[user_id] = now
    return 0

def free_sensi_text():
    base = random.randint(90, 120)
    return (
        "🎮 FREE SENSI\n\n"
        f"General: {base}\n"
        f"Red Dot: {base+5}\n"
        f"2x Scope: {base+10}\n"
        f"4x Scope: {base+15}\n"
        f"AWM: {random.randint(50,80)}"
    )

def vip_sensi_text():
    base = random.randint(150, 200)
    return (
        "👑 VIP SENSI\n\n"
        f"General: {base}\n"
        f"Red Dot: {base}\n"
        f"2x Scope: {base}\n"
        f"4x Scope: {base}\n"
        f"AWM: {random.randint(80,100)}"
    )

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("⚡ Generate Free Sensi", callback_data="free")],
        [InlineKeyboardButton("👑 VIP Sensi", callback_data="vip")],
        [InlineKeyboardButton("💎 Buy VIP", callback_data="buy")],
    ]
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(kb),
    )

async def admin_add_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_ID or str(update.effective_user.id) != str(ADMIN_ID):
        await update.message.reply_text("❌ Admin only")
        return
    if not context.args:
        await update.message.reply_text("Usage: /addvip USER_ID")
        return
    try:
        uid = int(context.args[0])
        VIP_USERS.add(uid)
        await update.message.reply_text(f"✅ VIP added for user {uid}")
    except:
        await update.message.reply_text("Invalid USER_ID")

# ===== BUTTON HANDLER =====
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    wait = in_cooldown(uid)
    if wait > 0:
        await q.message.reply_text(f"⏳ Please wait {wait}s before next generate.")
        return

    if q.data == "free":
        await q.message.reply_text(free_sensi_text())

    elif q.data == "vip":
        if uid not in VIP_USERS:
            await q.message.reply_text("❌ VIP required. Click **Buy VIP**.", parse_mode="Markdown")
            return
        await q.message.reply_text(vip_sensi_text())

    elif q.data == "buy":
        await q.message.reply_text(
            "💎 VIP PLAN\n\n"
            "Price: ₹XX\n"
            "UPI: aryankumar6333@navi\n\n"
            "Payment ke baad admin ko screenshot bhejo.\n"
            "Admin VIP unlock karega."
        )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addvip", admin_add_vip))
    app.add_handler(CallbackQueryHandler(on_button))

    print("🤖 BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
