# -*- coding: utf-8 -*-

import telegram

keyboard=[['minfin.com.ua'],['obmenka.kharkov.ua']]
keyboard_show=telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True,
                                            one_time_keyboard=True)
keyboard_hide=telegram.ReplyKeyboardRemove()
inline=telegram.InlineKeyboardButton('Rate', callback_data='/main')
keyboard_inline=telegram.InlineKeyboardMarkup([inline])
