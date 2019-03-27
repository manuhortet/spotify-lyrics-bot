import telegram
import logging
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import run_async
from credentials.credentials import token
from bot.login import USERNAME, PASSWORD, username, password, start, cancel

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telegram.Bot(token=token)


@run_async
def lyrics(bot, update):
    from bot.login import user_spotify
    song = user_spotify.get_song()
    lyrics = user_spotify.get_lyrics()

    bot.sendMessage(chat_id=update.message.chat_id, text="\U0001F3B6 *Lyrics for*: " + song,
                    parse_mode=telegram.ParseMode.MARKDOWN)
    bot.sendMessage(chat_id=update.message.chat_id, text=lyrics)


def main():
    logging.info("Bot running at @Spoti_lyrics_bot")
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            USERNAME: [MessageHandler(Filters.text, username)],
            PASSWORD: [MessageHandler(Filters.text, password)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]))

    dispatcher.add_handler(CommandHandler('lyrics', lyrics))

    updater.start_polling()
    updater.idle()
