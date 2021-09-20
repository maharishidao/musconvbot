
# from config import conf
#import telegram
#
# tg_token=conf['telegram_token']
# bot = telegram.Bot(token=tg_token)
# print(tg_token)
#
# #proxy list: https://50na50.net/ru/proxy/socks5list
#
# proxy_url='socks5://66.33.210.203:24475'
#
# pp = telegram.utils.request.Request(proxy_url=proxy_url)
# bot = telegram.Bot(token=tg_token, request=pp)
# print(bot.get_me())
#
# REQUEST_KWARGS={'proxy_url'=proxy_url}

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from config import conf
import logging


proxy_url='socks5://104.248.63.49:30588'
REQUEST_KWARGS={'proxy_url':proxy_url}
tg_token=conf['telegram_token']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


import os
server_url='https://hello-world-delete-234.nw.r.appspot.com/'

PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(tg_token, use_context=True, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
# add handlers

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=tg_token)

updater.bot.set_webhook("server_url" + tg_token)
updater.idle()


# updater = Updater(token=tg_token, use_context=True,request_kwargs=REQUEST_KWARGS)
# dispatcher = updater.dispatcher



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Просто кинь мне ссылку на трек, и я ее конвертирую!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# updater.start_polling()

