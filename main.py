import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛒 خرید", callback_data="buy")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی", callback_data="support")]
    ]
    update.message.reply_text("به ربات خوش آمدید 👇", reply_markup=InlineKeyboardMarkup(keyboard))

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "support":
        context.user_data["support"] = True
        query.message.reply_text("لطفا پیام خود را ارسال کنید ❤️‍🔥")

    elif query.data == "buy":
        keyboard = [
            [InlineKeyboardButton("5 گیگ - 80 هزار", callback_data="p1")],
            [InlineKeyboardButton("10 گیگ - 120 هزار", callback_data="p2")],
            [InlineKeyboardButton("20 گیگ - 200 هزار", callback_data="p3")]
        ]
        query.message.reply_text("پکیج‌ها:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "p1":
        query.message.reply_text("💰 80 هزار\nبه نام امیررضا هژبر\n6104338644728640")

    elif query.data == "p2":
        query.message.reply_text("💰 120 هزار\nبه نام امیررضا هژبر\n6104338644728640")

    elif query.data == "p3":
        query.message.reply_text("💰 200 هزار\nبه نام امیررضا هژبر\n6104338644728640")

def message(update: Update, context: CallbackContext):
    if context.user_data.get("support"):
        context.user_data["support"] = False
        update.message.reply_text("پیام شما ارسال شد 🌹")

        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 پشتیبانی:\n{update.message.text}"
        )

    elif update.message.photo:
        update.message.reply_text("رسید دریافت شد 🌹")

        context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption="📥 رسید جدید"
        )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo, message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
