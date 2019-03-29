from telegram.ext.dispatcher import run_async
from bot.spotify import Spotify

USERNAME, PASSWORD = range(2)

user_nick = ''
user_pass = ''
user_spotify = None


@run_async
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hey there {}! \U0001F601".format(update.effective_user.first_name))
    bot.sendMessage(chat_id=update.message.chat_id, text="Will need your Spotify credentials to start sending those sick lyrics. \U0001F60E\U0001F3B8")
    bot.sendMessage(chat_id=update.message.chat_id, text="Tell me your username or email:")
    return USERNAME


@run_async
def username(bot, update):
    global user_nick
    user_nick = update.message.text.lower()
    bot.sendMessage(chat_id=update.message.chat_id, text="Password:")
    return PASSWORD


@run_async
def password(bot, update):
    user_pass = update.message.text.lower()
    global user_spotify
    try:
        user_spotify = Spotify(user_nick, user_pass)
        bot.sendMessage(chat_id=update.message.chat_id, text="It worked! \U0001F389 Now use /lyrics for me to sing \U0001F525\U0001F602\U0001F44C")
    except:
        bot.sendMessage(chat_id=update.message.chat_id, text="Bad credentials, I couldn't connect.")
    return -1


@run_async
def cancel(bot, update):
    user_id = update.message.chat_id
    bot.sendMessage(chat_id=user_id, text="Canceled! \U0001F46E")
    return -1
