import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 8688294225

support_map = {}

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید", callback_data="buy")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی", callback_data="support")]
    ])

def vpn_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("5 گیگ", callback_data="vpn_5")],
        [InlineKeyboardButton("10 گیگ", callback_data="vpn_10")],
        [InlineKeyboardButton("20 گیگ", callback_data="vpn_20")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به ربات خوش آمدید 👇", reply_markup=menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "buy":
        await q.message.reply_text("یکی را انتخاب کنید 👇", reply_markup=vpn_menu())

    elif q.data == "vpn_5":
        await q.message.reply_text("5 گیگ - 80 هزار\n\n6104338644728640\nامیررضا هژبر")

    elif q.data == "vpn_10":
        await q.message.reply_text("10 گیگ - 120 هزار\n\n6104338644728640\nامیررضا هژبر")

    elif q.data == "vpn_20":
        await q.message.reply_text("20 گیگ - 200 هزار\n\n6104338644728640\nامیررضا هژبر")

    elif q.data == "support":
        context.user_data["support"] = True
        await q.message.reply_text("پیام خود را ارسال کنید ❤️‍🔥")

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # پیام کاربر به ادمین
    if update.effective_user.id != ADMIN_ID and context.user_data.get("support"):
        context.user_data["support"] = False

        msg = await context.bot.send_message(
            ADMIN_ID,
            f"📩 پیام جدید\n\n{update.effective_user.id}\n\n{update.message.text or ''}"
        )

        support_map[msg.message_id] = update.effective_user.id

        await update.message.reply_text("ارسال شد 🌹")
        return

    # ریپلای ادمین
    if update.effective_user.id == ADMIN_ID and update.message.reply_to_message:
        target = support_map.get(update.message.reply_to_message.message_id)
        if target:
            await context.bot.send_message(target, update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT, handler))

    app.run_polling()

if __name__ == "__main__":
    main()
