import logging
from ai import get_response
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    filters
)
import os
import dotenv
dotenv.load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

memory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="I'm HCARB. I am here for you. Please tell me what's on your mind")

    if not os.path.exists(f"logs/{chat_id}.txt"):
        with open(f"logs/{chat_id}.txt") as f:
            f.write("")
            f.close()    


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    history = memory.get(chat_id, [])
    response, history = get_response(chat_id, text, history)
    memory[chat_id] = history

    await context.bot.send_message(chat_id=chat_id, text=response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).read_timeout(30).write_timeout(30).build()
    start_handler = CommandHandler('start', start)
    response_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), respond)
    application.add_handler(response_handler)
    application.add_handler(start_handler)
    application.run_polling()