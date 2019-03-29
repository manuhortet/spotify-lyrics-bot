# TODO:
# Add automatic mode

import telegram
import time
import logging
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import run_async
from credentials.credentials import token
from bot.login import USERNAME, PASSWORD, username, password, start, cancel

live_lyrics = False

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telegram.Bot(token=token)


@run_async
def current_song(bot, update):
    from bot.login import user_spotify
    song = user_spotify.get_song()
    lyrics = user_spotify.get_lyrics()

    bot.sendMessage(chat_id=update.message.chat_id, text="\U0001F3B6 *Lyrics for*: " + song,
                    parse_mode=telegram.ParseMode.MARKDOWN)
    bot.sendMessage(chat_id=update.message.chat_id, text=lyrics)


@run_async
def lyrics(bot, update):
    from bot.login import user_spotify
    global live_lyrics
    live_lyrics = True
    song = ''

    while live_lyrics:
        start_time = time.time()
        new_song = user_spotify.get_song()
        if song != new_song:
            song = new_song
            lyrics = user_spotify.get_lyrics()
            bot.sendMessage(chat_id=update.message.chat_id, text="\U0001F3B6 *Lyrics for*: " + song,
                            parse_mode=telegram.ParseMode.MARKDOWN)
            bot.sendMessage(chat_id=update.message.chat_id, text=lyrics)
        time.sleep(15.0 - ((time.time() - start_time) % 15.0))


@run_async
def stop(bot, update):
    global live_lyrics
    bot.sendMessage(chat_id=update.message.chat_id, text="Ok... \U0001F636")
    live_lyrics = False
    return -1


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

    dispatcher.add_handler(CommandHandler('current_song', current_song))
    dispatcher.add_handler(CommandHandler('lyrics', lyrics))
    dispatcher.add_handler(CommandHandler('stop', stop))

    updater.start_polling()
    updater.idle()
