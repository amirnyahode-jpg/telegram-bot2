# test - ultimate stability version
import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
PORT = int(os.environ.get("PORT", 8000))

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def run_health_server():
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
        server.serve_forever()
    except Exception as e:
        print(f"Web server error: {e}")

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید", callback_data="buy")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی", callback_data="support")]
    ])

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("به ربات خوش آمدید 👇", reply_markup=get_main_menu())

async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "support":
        context.user_data["support"] = True
        await q.message.reply_text("پیام خود را همینجا ارسال کنید ❤️‍🔥")
    elif q.data == "buy":
        await q.message.reply_text(
            "💳 پکیج‌ها:\n\n1) 5 گیگ - 80 هزار\n2) 10 گیگ - 120 هزار\n3) 20 گیگ - 200 هزار\n\n📌 شماره کارت:\n6104338644728640\nبه نام امیررضا هژبر\n\nبعد از پرداخت رسید را ارسال کنید 🌹"
        )

async def global_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.message.chat_id

    if user_id == ADMIN_ID:
        if update.message.reply_to_message:
            try:
                target_text = update.message.reply_to_message.caption or update.message.reply_to_message.text
                if target_text and "User ID:" in target_text:
                    target_user_id = int(target_text.split("User ID:")[1].strip())
                    await context.bot.copy_message(
                        chat_id=target_user_id,
                        from_chat_id=ADMIN_ID,
                        message_id=update.message.message_id
                    )
                    await update.message.reply_text("✅ پیام شما با موفقیت به مشتری ارسال شد.")
                else:
                    await update.message.reply_text("❌ خطا: اطلاعات کاربر پیدا نشد.")
            except Exception as e:
                await update.message.reply_text(f"❌ خطا در ارسال: {e}")
        return

    if update.message.photo:
        await update.message.reply_text("🌹 رسید دریافت شد\nدر حال بررسی... ❤️‍🔥")
        if ADMIN_ID:
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
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📩 پیام پشتیبانی:\n{update.message.text}\n\nUser ID: {user_id}"
            )

async def start_bot():
    if not TOKEN:
        print("Error: TOKEN is missing!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document, global_message_handler))

    print("Telegram bot is starting...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    print(f"Web Health Check Server started on port {PORT}")
    
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
