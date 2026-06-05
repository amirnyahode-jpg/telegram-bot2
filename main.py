import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید", callback_data="buy")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی", callback_data="support")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به ربات خوش آمدید 👇", reply_markup=menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "support":
        context.user_data["support"] = True
        await q.message.reply_text("پیام خود را همینجا ارسال کنید ❤️‍🔥")

    elif q.data == "buy":
        await q.message.reply_text(
            "💳 پکیج‌ها:\n\n"
            "1) 5 گیگ - 80 هزار\n"
            "2) 10 گیگ - 120 هزار\n"
            "3) 20 گیگ - 200 هزار\n\n"
            "📌 شماره کارت:\n"
            "6104338644728640\n"
            "به نام امیررضا هژبر\n\n"
            "بعد از پرداخت رسید را ارسال کنید 🌹"
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # پشتیبانی
    if context.user_data.get("support"):
        context.user_data["support"] = False

        await update.message.reply_text("پیام شما ارسال شد 🌹")

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 پشتیبانی:\n{update.message.text}"
        )

    # رسید عکس
    elif update.message.photo:
        await update.message.reply_text(
            "🌹 رسید دریافت شد\nدر حال بررسی... ❤️‍🔥"
        )

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption="📥 رسید جدید"
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
