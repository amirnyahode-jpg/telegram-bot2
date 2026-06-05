241”}
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application,
CommandHandler,
CallbackQueryHandler,
MessageHandler,
ContextTypes,
filters,
)

TOKEN = os.environ.get(“TOKEN”)
ADMIN_ID = 8688294225

نگهداری ارتباط پیام ادمین ↔ مشتری

support_messages = {}

def main_menu():
return InlineKeyboardMarkup([
[InlineKeyboardButton(“🛒 خرید”, callback_data=“buy”)],
[InlineKeyboardButton(“🧑‍💻 پشتیبانی”, callback_data=“support”)]
])

def vpn_menu():
return InlineKeyboardMarkup([
[InlineKeyboardButton(“5 گیگ”, callback_data=“vpn_5”)],
[InlineKeyboardButton(“10 گیگ”, callback_data=“vpn_10”)],
[InlineKeyboardButton(“20 گیگ”, callback_data=“vpn_20”)],
[InlineKeyboardButton(“🔙 بازگشت”, callback_data=“back”)]
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“به ربات خوش آمدید 👇”,
reply_markup=main_menu()
)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

if query.data == "buy":
    await query.message.reply_text(
        "پکیج مورد نظر را انتخاب کنید 👇",
        reply_markup=vpn_menu()
    )
elif query.data == "vpn_5":
    await query.message.reply_text(
        "📦 5 گیگ\n"
        "💰 80 هزار تومان\n\n"
        "💳 6104338644728640\n"
        "👤 امیررضا هژبر\n\n"
        "پس از پرداخت رسید را ارسال کنید 🌹"
    )
elif query.data == "vpn_10":
    await query.message.reply_text(
        "📦 10 گیگ\n"
        "💰 120 هزار تومان\n\n"
        "💳 6104338644728640\n"
        "👤 امیررضا هژبر\n\n"
        "پس از پرداخت رسید را ارسال کنید 🌹"
    )
elif query.data == "vpn_20":
    await query.message.reply_text(
        "📦 20 گیگ\n"
        "💰 200 هزار تومان\n\n"
        "💳 6104338644728640\n"
        "👤 امیررضا هژبر\n\n"
        "پس از پرداخت رسید را ارسال کنید 🌹"
    )
elif query.data == "back":
    await query.message.reply_text(
        "منوی اصلی 👇",
        reply_markup=main_menu()
    )
elif query.data == "support":
    context.user_data["support_mode"] = True
    await query.message.reply_text(
        "لطفا پیام خود را همینجا ارسال کنید ❤️‍🔥\n\nبا تشکر 🌹🌹"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

# پاسخ ادمین به مشتری
if update.effective_user.id == ADMIN_ID:
    if (
        update.message.reply_to_message
        and update.message.reply_to_message.message_id in support_messages
    ):
        target_user = support_messages[
            update.message.reply_to_message.message_id
        ]
        await context.bot.send_message(
            chat_id=target_user,
            text=f"📩 پاسخ پشتیبانی:\n\n{update.message.text}"
        )
        await update.message.reply_text("✅ پیام ارسال شد")
    return
# پشتیبانی
if context.user_data.get("support_mode"):
    context.user_data["support_mode"] = False
    sent = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📩 پیام پشتیبانی\n\n"
            f"نام: {update.effective_user.first_name}\n"
            f"آیدی: {update.effective_user.id}\n\n"
            f"{update.message.text}"
        )
    )
    support_messages[sent.message_id] = update.effective_user.id
    await update.message.reply_text(
        "پیام شما ارسال شد 🌹\nبا تشکر ❤️‍🔥"
    )
    return
# رسید
if update.message.photo:
    await update.message.reply_text(
        "🌹 با تشکر از اعتماد شما 🌹\n"
        "رسید دریافت شد.\n"
        "کمتر از ۲۰ دقیقه آینده بررسی خواهد شد ❤️‍🔥"
    )
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=(
            f"📥 رسید جدید\n\n"
            f"نام: {update.effective_user.first_name}\n"
            f"آیدی: {update.effective_user.id}"
        )
    )

def main():
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(
    MessageHandler(
        filters.TEXT | filters.PHOTO,
        handle_message
    )
)
app.run_polling()

if name == “__mai
