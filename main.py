import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
PORT = int(os.environ.get("PORT", 8080))

class FastHealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def start_server():
    server = HTTPServer(('0.0.0.0', PORT), FastHealthCheck)
    server.serve_forever()

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
            "💳 پکیج‌ها:\n\n1) 5 گیگ - 80 هزار\n2) 10 گیگ - 120 هزار\n3) 20 گیگ - 200 هزار\n\n📌 شماره کارت:\n6104338644728640\nبه نام امیررضا هژبر\n\nبعد از پرداخت رسید را ارسال کنید 🌹"
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    # --- بخش اول: اگر پیام از طرف ادمین باشد (پاسخ دادن به مشتری) ---
    if user_id == ADMIN_ID:
        # چک میکنیم آیا ادمین روی پیامی ریپلای کرده یا نه
        if update.message.reply_to_message:
            try:
                # پیدا کردن آیدی مشتری از روی متن یا کپشنی که قبلاً براش فرستاده شده بود
                target_text = update.message.reply_to_message.caption or update.message.reply_to_message.text
                if target_text and "User ID:" in target_text:
                    target_user_id = int(target_text.split("User ID:")[1].strip())
                    
                    # ارسال پاسخ ادمین (هر چیزی که فرستاده: متن، عکس، فایل و...) به مشتری
                    await context.bot.copy_message(
                        chat_id=target_user_id,
                        from_chat_id=ADMIN_ID,
                        message_id=update.message.message_id
                    )
                    await update.message.reply_text("✅ پیام شما با موفقیت به مشتری ارسال شد.")
                else:
                    await update.message.reply_text("❌ خطا: اطلاعات کاربر روی این پیام پیدا نشد. حتماً روی رسیدی که ربات فرستاده ریپلای کنید.")
            except Exception as e:
                await update.message.reply_text(f"❌ خطا در ارسال پیام: {e}")
        return

    # --- بخش دوم: اگر پیام از طرف مشتری باشد (ارسال رسید یا پیام پشتیبانی) ---
    if update.message.photo:
        await update.message.reply_text("🌹 رسید دریافت شد\nدر حال بررسی... ❤️‍🔥")
        if ADMIN_ID:
            # فرستادن عکس برای ادمین به همراه آیدی عددی مشتری در کپشن برای ریپلای کردن
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=update.message.photo[-1].file_id,
                caption=f"📥 رسید جدید از طرف کاربر\nUser ID: {user_id}"
            )
        return

    if context.user_data.get("support"):
        context.user_data["support"] = False
        await update.message.reply_text("پیام شما ارسال شد 🌹")
        if ADMIN_ID and update.message.text:
            # فرستادن متن پشتیبانی برای ادمین به همراه آیدی مشتری
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📩 پیام پشتیبانی:\n{update.message.text}\n\nUser ID: {user_id}"
            )

async def main():
    if not TOKEN:
        print("Error: TOKEN is missing!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document, message_handler))

    print("ربات با موفقیت روشن شد...")
    async with app:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    asyncio.run(main())
