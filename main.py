import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید", callback_data="buy")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی", callback_data="support")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به ربات خوش آمدید 👇", reply_markup=main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "support":
        context.user_data["support_mode"] = True
        await q.message.reply_text("لطفا پیام خود را همینجا ارسال کنید ❤️‍🔥")

    elif q.data == "buy":
        await q.message.reply_text(
            "پکیج‌ها:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("5 گیگ - 80 هزار", callback_data="5g")],
                [InlineKeyboardButton("10 گیگ - 120 هزار", callback_data="10g")],
                [InlineKeyboardButton("20 گیگ - 200 هزار", callback_data="20g")]
            ])
        )

    elif q.data == "5g":
        await q.message.reply_text("💰 ۸۰ هزار\nبه نام امیررضا هژبر\nشماره کارت: 6104338644728640")

    elif q.data == "10g":
        await q.message.reply_text("💰 ۱۲۰ هزار\nبه نام امیررضا هژبر\nشماره کارت: 6104338644728640")

    elif q.data == "20g":
        await q.message.reply_text("💰 ۲۰۰ هزار\nبه نام امیررضا هژبر\nشماره کارت: 6104338644728640")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("support_mode"):
        context.user_data["support_mode"] = False

        await update.message.reply_text("پیام شما ارسال شد 🌹")

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 پشتیبانی:\n{update.message.text}"
        )

    elif update.message.photo:
        await update.message.reply_text("رسید دریافت شد، در حال بررسی... ❤️‍🔥")

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption="📥 رسید جدید"
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()