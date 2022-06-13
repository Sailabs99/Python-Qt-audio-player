# encoding=utf8
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from settings import WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY, TELEGRAM_TOKEN
from time import localtime, strftime
from os.path import exists


updater = Updater(TELEGRAM_TOKEN)
dp = updater.dispatcher


def start(update, context):
    update.message.reply_text(WELCOME_MESSAGE)

    user_info = update.message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"Connected {user_info}.")


def forward_to_chat(update, context):
    forwarded = update.message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )

    log = f'[{update.message.chat.first_name} {update.message.chat.last_name}]: {update.message.text}'
    logger(log)


def forward_to_user(update, context):
    def form_txt():
        repl_frst_nme = update.message.to_dict()['from']['first_name']
        repl_lst_nme = update.message.to_dict()['from']['last_name']
        ask_frst_nme = update.message.reply_to_message.forward_from.first_name 
        ask_lst_nme = update.message.reply_to_message.forward_from.last_name
        text_ask = update.message.reply_to_message.text
        text_repl = update.message.text
        f = f'[{repl_frst_nme} {repl_lst_nme}]: {str(text_repl)}, [{ask_frst_nme} {ask_lst_nme}]: {str(text_ask)}'
        logger(f)

    if froze(update.message.chat.id) == froze(TELEGRAM_SUPPORT_CHAT_ID):
        user_id = update.message.reply_to_message.forward_from.id
        context.bot.copy_message(
        message_id=update.message.message_id,
        chat_id=user_id,
        from_chat_id=update.message.chat_id
        )
        form_txt()


def froze(n):
    return frozenset([i for i in str(n)])


def logger(text):
    r = 'a'
    tm = localtime()
    f_tm = strftime("%d/%m/%Y, %H:%M:%S", localtime())
    name = strftime("%d.%m.%Y", localtime()) + '.txt'
    if not exists('log/name'):
        r = 'w'
    with open(f'log/{name}', r) as f:
        f.write(f'{f_tm} | {text}\n')


dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
dp.add_handler(MessageHandler(Filters.update & Filters.reply, forward_to_user))

updater.start_polling()
updater.idle()

