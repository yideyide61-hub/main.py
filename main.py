import logging
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 Only this user ID can add the bot
BOT_OWNER_ID = 7124683213   # <-- Replace with your own Telegram ID

async def check_who_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = update.my_chat_member  # event when bot is added/removed

    # Only check when bot itself is added
    if member.new_chat_member.user.id == context.bot.id:
        chat_id = member.chat.id
        adder = member.from_user
        chat_title = member.chat.title if member.chat.title else "Private Chat"

        logger.info(f"Bot added to group: {chat_title} (id={chat_id})")
        logger.info(f"Added by: {adder.full_name} (id={adder.id}, username=@{adder.username})")

        if adder.id != BOT_OWNER_ID:
            # ❌ Not the owner → leave
            logger.warning(f"❌ {adder.full_name} is NOT the owner. Leaving {chat_title}.")
            await context.bot.send_message(chat_id, "您好，1087968824，机器人已检测到加入了新群组，正在初始化新群组，请稍候...")
            await context.bot.leave_chat(chat_id)
        else:
            # ✅ Owner added → stay
            logger.info(f"✅ Bot added by owner {adder.full_name}. Staying in {chat_title}.")
            await context.bot.send_message(chat_id, "✅ Bot added by my owner. Ready to work here!")

def main():
    app = Application.builder().token("8466271055:AAFFEW0zQ_AJnbav6g3AbZht-8O0gqa3kBU").build()
    app.add_handler(ChatMemberHandler(check_who_added, ChatMemberHandler.MY_CHAT_MEMBER))

    logger.info("Bot started polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
