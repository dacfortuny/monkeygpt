import random

from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from src.answers import AnswerPirate
from src.insult import Insult
from src.utils import get_telegram_api_key


class MonkeyBot:
    def __init__(self):
        self.API_KEY = get_telegram_api_key()

    @staticmethod
    async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Use /insult <insult> to throw an insult at me and "
            "I'll try my best to reply with a witty comeback!",
        )

    @staticmethod
    async def _insult(update: Update, context: ContextTypes.DEFAULT_TYPE):

        insult = Insult(" ".join(context.args))
        is_successful_answer = random.getrandbits(1)
        answer = AnswerPirate(insult, is_successful_answer)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=answer.answer
        )

        if not is_successful_answer:
            message = f"\n(Good job! You got one on me!)\n"
        else:
            message = f"\n(You'll have to do better next time!)\n"

        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    @staticmethod
    async def _unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, I don't understand that command. Use /help to see what I can do.",
        )

    def run(self):
        application = ApplicationBuilder().token(self.API_KEY).build()

        help_handler = CommandHandler("help", self._help)
        insult_handler = CommandHandler("insult", self._insult)
        unknown_handler = MessageHandler(filters.COMMAND, self._unknown)

        application.add_handler(help_handler)
        application.add_handler(insult_handler)
        application.add_handler(unknown_handler)

        application.run_polling()
