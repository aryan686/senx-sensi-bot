import os
import random
from typing import Dict
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
    ContextTypes,
    filters,
)

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID  = os.getenv("ADMIN_ID")
UPI_ID    = os.getenv("UPI_ID", "aryankumar6333@navi")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# ===== STATE STORE (in-memory; restart pe reset) =====
# user_id -> dict
STATE: Dict[int, Dict] = {}
VIP_USERS = set()
PENDING_VIP = {}  # user_id -> reference_code

# ===== HELPERS =====
def signature():
    return "\n\n— Sensi by Aryansenx"

def gen_free_sensi(ram_gb: int):
    base = random.randint(90, 120)
    fire = random.randint(48, 58)
    return (
        f"🎮 FREE SENSI\n\n"
        f"General: {base}\n"
        f"Red Dot: {base+5}\n"
        f"2x Scope: {base+10}\n"
        f"4x Scope: {base+15}\n"
        f"AWM: {random.randint(50,80)}\n"
        f"🔥 Fire Button: {fire}%"
        + signature()
    )

def gen_vip_sensi(level: str):
    if level == "low":
        base = random.randint(140, 160)
    elif level == "medium":
        base = random.randint(165, 185)
    else:
        base = random.randint(190, 210)
    fire = random.randint(58, 65)
    return (
        f"👑 VIP SENSI ({level.upper()})\n\n"
        f"General: {base}\n"
        f"Red Dot: {base}\n"
        f"2x Scope: {base}\n"
        f"4x Scope: {base}\n"
        f"AWM: {random.randint(85,100)}\n"
        f"🔥 Fire Button: {fire}%"
        + signature()
    )

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Free Sensi", callback_data="free")],
        [InlineKeyboardButton("👑 VIP Sensi", callback_data="vip")],
    ])

def vip_levels():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("Low", callback_data="vip_low"),
        InlineKeyboardButton("Medium", callback_data="vip_medium"),
        InlineKeyboardButton("High", callback_data="vip_high"),
    ]])

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    STATE.pop(update.effective_user.id, None)
    await update.message.reply_text(
        "🔥 SENX SENSI BOT 🔥\n\nChoose:",
        reply_markup=main_menu()
    )

# ===== BUTTON HANDLER =====
async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    if q.data == "free":
        STATE[uid] = {"flow": "free", "step": "device"}
        await q.message.reply_text("📱 Enter your **Device Name**:")

    elif q.data == "vip":
        # show UPI + reference input
        STATE[uid] = {"flow": "vip_pay", "step": "ref"}
        await q.message.reply_text(
            "💎 VIP SENSI\n\n"
            f"UPI ID: **{UPI_ID}**\n"
            "Pay and paste **UPI Reference Code** below.\n\n"
            "⚠️ After verify, VIP unlock hoga."
        )

    elif q.data.startswith("vip_"):
        if uid not in VIP_USERS:
            await q.message.reply_text("❌ VIP not unlocked yet.")
            return
        level = q.data.split("_")[1]
        await q.message.reply_text(gen_vip_sensi(level))

# ===== TEXT INPUT HANDLER =====
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.strip()

    if uid not in STATE:
        return

    st = STATE[uid]

    # ---- FREE FLOW ----
    if st.get("flow") == "free":
        if st["step"] == "device":
            st["device"] = text
            st["step"] = "ram"
            await update.message.reply_text("💾 Enter **Phone RAM (GB)** (e.g., 4, 6, 8):")
        elif st["step"] == "ram":
            try:
                ram = int(text)
            except:
                await update.message.reply_text("Please enter RAM as number (e.g., 4, 6, 8).")
                return
            await update.message.reply_text(gen_free_sensi(ram))
            STATE.pop(uid, None)

    # ---- VIP PAYMENT FLOW ----
    elif st.get("flow") == "vip_pay":
        # save ref, ask admin to approve
        ref = text
        PENDING_VIP[uid] = ref
        await update.message.reply_text(
            "⏳ Reference received. Admin verifying...\n"
            "You’ll be unlocked soon."
        )
        # notify admin
        if ADMIN_ID:
            try:
                await context.bot.send_message(
                    chat_id=int(ADMIN_ID),
                    text=f"VIP VERIFY REQUEST\nUser: {uid}\nRef: {ref}\n\nApprove: /approve {uid}"
                )
            except:
                pass

    # ---- VIP DETAILS FLOW ----
    elif st.get("flow") == "vip_details":
        if st["step"] == "device":
            st["device"] = text
            st["step"] = "ram"
            await update.message.reply_text("💾 Enter **Phone RAM (GB)**:")
        elif st["step"] == "ram":
            try:
                st["ram"] = int(text)
            except:
                await update.message.reply_text("Enter RAM as number.")
                return
            await update.message.reply_text("Select level:", reply_markup=vip_levels())

# ===== ADMIN COMMAND =====
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_ID or str(update.effective_user.id) != str(ADMIN_ID):
        return
    if not context.args:
        await update.message.reply_text("Usage: /approve USER_ID")
        return
    try:
        uid = int(context.args[0])
        VIP_USERS.add(uid)
        STATE[uid] = {"flow": "vip_details", "step": "device"}
        await update.message.reply_text(f"✅ VIP approved for {uid}")
        await context.bot.send_message(
            chat_id=uid,
            text="👑 VIP UNLOCKED!\n📱 Enter your **Device Name**:"
        )
    except:
        await update.message.reply_text("Invalid USER_ID")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    print("BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
