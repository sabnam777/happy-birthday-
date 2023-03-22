import os

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from dotenv import load_dotenv

from bot import start_handler, candle_handler, open_card_handler, gift_handler, button_handler

load_dotenv()

def main():

    bot_token = os.environ.get("BOT_TOKEN")

    updater = Updater(bot_token, use_context=True)

    dispatcher = updater.dispatcher

    start_command_handler = CommandHandler("start", start_handler)

    dispatcher.add_handler(start_command_handler)

    candle_command_handler = CommandHandler("blowcandle", candle_handler)

    dispatcher.add_handler(candle_command_handler)

    open_card_command_handler = CommandHandler("opencard", open_card_handler)

    dispatcher.add_handler(open_card_command_handler)

    gift_command_handler = CommandHandler("birthdaygift", gift_handler)

    dispatcher.add_handler(gift_command_handler)

    button_callback_handler = CallbackQueryHandler(button_handler)

    dispatcher.add_handler(button_callback_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

