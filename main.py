import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# تغییر کوچک: اگر Import اول با حروف بزرگ بود به 'import' اصلاح شد
TOKEN = os.environ.get("TOKEN")

# نکته مهم: تلگرام آیدی عددی می‌خواهد، پس باید ADMIN_ID را به int تبدیل کنیم
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

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
    # بررسی ارسال رسید (عکس) - این شرط باید اول باشد تا اگر کاربر عکس فرستاد مستقیم اینجا بیاید
    if update.message.photo:
        await update.message.reply_text(
            "🌹 رسید دریافت شد\nدر حال بررسی... ❤️‍🔥"
        )
        if ADMIN_ID:
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=update.message.photo[-1].file_id,
                caption="📥 رسید جدید"
            )
        return # عملیات تمام شد و از تابع خارج می‌شویم

    # بررسی پیام پشتیبانی (متن)
    if context.user_data.get("support"):
        context.user_data["support"] = False

        await update.message.reply_text("پیام شما ارسال شد 🌹")

        if ADMIN_ID and update.message.text:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📩 پشتیبانی:\n{update.message.text}"
            )

def main():
    # بررسی وجود توکن
    if not TOKEN:
        print("خطا: توکن ربات (TOKEN) در Environment Variables تنظیم نشده است.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    
    # فیلترها اصلاح شد تا هم متن و هم عکس را به درستی هندل کند
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, message_handler))

    print("ربات با موفقیت روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
