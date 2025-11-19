from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Gán token trực tiếp
BOT_TOKEN = "7873715180:AAHxTzeDloMAy4i2YW136F48mGz1mKP-boA"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:  # Tránh lỗi nếu không có tin nhắn
        return

    message_text = update.message.text.strip()
    print(f"📩 Tin nhắn nhận được: {message_text}")  # Debug

    # Lấy username bot
    bot_username = (await context.bot.get_me()).username.lower()

    # Kiểm tra lệnh !id hoặc tag bot
    if message_text.lower() == "!id" or f"@{bot_username}" in message_text.lower():
        chat = update.effective_chat
        user = update.effective_user
        if chat.type in ["group", "supergroup"]:
            reply_text = (
                f"🆔 ID Group: {chat.id}\n"
                f"👤 ID Người gửi: {user.id} ({user.first_name})"
            )
            await update.message.reply_text(reply_text)
        else:
            await update.message.reply_text("⚠️ Đây không phải group, bot chỉ trả ID group thôi.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
