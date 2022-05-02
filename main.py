import os
from datetime import datetime, timedelta

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from dotenv import load_dotenv

from db_func import (create_db,
                     write_expense,
                     show_spendings,
                     show_spendings_for_month)

load_dotenv()
create_db()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

TODAY = datetime.today().strftime('%Y-%m-%d')
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
CURRENT_MONTH = datetime.today().strftime('%Y-%m')
BUTTONS = ReplyKeyboardMarkup([
    ['/spend_it_anyway'],
    ['/do_not_spend'],
    ['/show_spendings'],
    ['/show_yesterday_spendings'],
    ['/show_current_mont_spendings']
],
    resize_keyboard=True
)


def send_message(update, context, date):
    chat = update.effective_chat
    name = update.message.chat.first_name
    day = 'Сегодня'
    if date == YESTERDAY:
        day = 'Вчера'
    if date == CURRENT_MONTH:
        day = 'В этом месяце'
        dat = show_spendings_for_month(date, name)
    else:
        dat = show_spendings(date, name)
    text = f'{day} ты просрал кучу бабла:'
    sum_expensive = 0
    button = BUTTONS
    if len(dat) != 0:
        for row in dat:
            text += f'\n {row[4]} на {row[3]}'
            sum_expensive += row[4]
        text += f'\n Итого.. {sum_expensive}'
        context.bot.send_message(
            chat_id=chat.id,
            text=text,
            reply_markup=button
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=(f'Итого {sum_expensive} \n'
                  f'Ты еще ничего не потратил? Я сплю?'),
            reply_markup=button
        )


def wake_up(update, context):
    """Старт бота."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([
        ['/spend_money']
    ],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Еще один транжира??',
        reply_markup=button
    )


def spend_money(update, context):
    """Начать тратить деньги."""
    chat = update.effective_chat
    buttons = BUTTONS
    context.bot.send_message(
        chat_id=chat.id,
        text='ТЫ ОБАЛДЕЛ???',
        reply_markup=buttons
    )
    context.bot.send_photo(chat.id,
                           photo=('https://cs8.pikabu.ru/post_img/big/'
                                  '2016/09/10/4/1473483762167431656.jpg'))


def do_not_spend(update, context):
    """Не тратить деньги."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([
        ['/spend_money'],
        ['/show_spendings'],
        ['/show_yesterday_spendings'],
        ['/show_current_mont_spendings']
    ],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Умница',
        reply_markup=button
    )
    context.bot.send_photo(chat.id,
                           photo=('https://www.vokrug.tv/pic/product/5/5/1/'
                                  'c/551c8eedadfae9a67121fe71a5032d95.jpeg'))


def spend_it_anyway(update, context):
    """Все равно потратить деньги."""
    chat = update.effective_chat
    button = BUTTONS
    context.bot.send_message(
        chat_id=chat.id,
        text='Эхх... Сколько на этот раз?',
        reply_markup=button
    )


def create_expensive(update, context):
    """Записать трату."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    message = update.message.text
    values = message.split(' ')
    write_expense(TODAY,
                  name, values[1],
                  int(values[0]))
    button = BUTTONS
    context.bot.send_message(
        chat_id=chat.id,
        text='Да ты столько не зарабатываешь',
        reply_markup=button
    )


def send_today_spendings(update, context):
    """Отправить в чат сегодняшние траты."""
    send_message(update, context, TODAY)


def send_yesterday_spendings(update, context):
    """Отправить в чат вчерашние траты."""
    send_message(update, context, YESTERDAY)


def send_current_mont_spendings(update, context):
    """Отправить в чат траты за текущий месяц"""
    send_message(update, context, CURRENT_MONTH)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('spend_money',
                                                  spend_money))
    updater.dispatcher.add_handler(CommandHandler('do_not_spend',
                                                  do_not_spend))
    updater.dispatcher.add_handler(CommandHandler('spend_it_anyway',
                                                  spend_it_anyway))
    updater.dispatcher.add_handler(CommandHandler('show_spendings',
                                                  send_today_spendings))
    updater.dispatcher.add_handler(CommandHandler('show_yesterday_spendings',
                                                  send_yesterday_spendings))
    updater.dispatcher.add_handler(CommandHandler('show_current_mont_spendings',
                                                  send_current_mont_spendings))
    updater.dispatcher.add_handler(MessageHandler(Filters.text,
                                                  create_expensive))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
