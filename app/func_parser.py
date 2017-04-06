# -*- coding: utf-8 -*-
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode
from parser import minfin_get_html, minfin_parse, obmenka_parse
from keybord import keyboard_hide, keyboard_show, keyboard_inline

#HANDLERS
def start(bot,update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='_Я бот, предоставляющий актуальный Курс Валют в Украине._',
                    reply_markup=keyboard_show,
                    parse_mode=ParseMode.MARKDOWN
                    )
def message_disp(bot, update):
    if update.message.text==unicode('minfin.com.ua','utf-8'):
        minfin(bot=bot, update=update)
    elif update.message.text==unicode('obmenka.kharkov.ua','utf-8'):
        obmenka(bot=bot,update=update)
    else:
        unknown(bot=bot,update=update)

#the first rates' source
def obmenka(bot,update):
    (currencies,date)=obmenka_parse()
    text='''Курс валют  \n%s :\n\t
            *$ Доллар $*\n    _Покупка / Продажа_
          *%s* \t/\t *%s*\n
            *€ Евро €*\n    _Покупка / Продажа_
          *%s* \t/\t *%s*\n
            *₽ Рубль ₽*\n    _Покупка / Продажа_
          *%s* \t/\t *%s* \n

*€ Евро €* - *$ Доллар $*\n    _Покупка / Продажа_
          *%s* \t/\t *%s*\n
*$ Доллар $* - *₽ Рубль ₽*\n    _Покупка / Продажа_
          *%s* \t/\t *%s \n\n\t\t        Хорошего дня !*
        ''' %(str(date),
              str(currencies[0][2]),
              str(currencies[0][3]),
              str(currencies[1][2]),
              str(currencies[1][3]),
              str(currencies[2][2]),
              str(currencies[2][3]),
              str(currencies[3][2]),
              str(currencies[3][3]),
              str(currencies[4][2]),
              str(currencies[4][3])
              )
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard_show,
                    )

#the second rates' source
def minfin(bot,update):
    (html, success)=minfin_get_html()
    if success==True:
        (curr, month, date)=minfin_parse(html)
        text='''
                Курс валют  %s %s %s:\n\n\t    *НАЛИЧНЫЙ РЫНОК*
            *$ Доллар $*\n _Покупка / Продажа_
        *%s* \t/\t *%s*\n
            *€ Евро €*\n _Покупка / Продажа_
        *%s* \t/\t *%s*\n
            *₽ Рубль ₽*\n _Покупка / Продажа_
        *%s* \t/\t *%s* \n
        \t\t   *МЕЖБАНК*
            *$ Доллар $*\n _Покупка / Продажа_
        *%s* \t/\t *%s*\n
            *€ Евро €*\n _Покупка / Продажа_
        *%s* \t/\t *%s \n\n\t\t      Хорошего дня !*
                ''' %(str(date[0]),
                      month.encode('utf-8'),
                      str(date[1]),
                      str(curr[0][0]),
                      str(curr[0][1]),
                      str(curr[1][0]),
                      str(curr[1][1]),
                      str(curr[2][0]),
                      str(curr[2][1]),
                      str(curr[3][0]),
                      str(curr[3][1]),
                      str(curr[4][0]),
                      str(curr[4][1])
                      )
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=text,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=keyboard_show,
                        )
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=html,
                        reply_markup=keyboard_show,
                        )

def unknown(bot,update):
    bot.sendMessage(chat_id=update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        text=update.message.text+' *IS NOT VALID. Try again.*',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard_show,)


start_handler=CommandHandler('start', start)
main_handler=MessageHandler(Filters.text, message_disp)
unknown_handler=MessageHandler(Filters.command | Filters.text, unknown)
handlers=[start_handler,
         main_handler,
         unknown_handler]


#ERROR handlers
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut,
                            ChatMigrated, NetworkError)

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        pass# remove update.message.chat_id from conversation_list
    except BadRequest:
        pass# handle malformed requests - read more below!
    except TimedOut:
        pass# handle slow connection problems
    except NetworkError:
        pass# handle other connection problems
    except ChatMigrated as e:
        pass# the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass# handle all other telegram related errors
