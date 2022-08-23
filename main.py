from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

# from telegram import ()

import db

import random
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')

LOGGING = False

updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

def start_command(update,context):
    """Initializes the bot"""
    text =  'Hello '+(update.message.from_user.first_name or '@'+update.message.from_user.username )
    text+= '\n\nFollow this bot for more info on E-Scholars :)'
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text)
    if update.effective_chat.id > 0:
        db.update_chat_id(update.effective_chat.username, update.effective_chat.id)

dispatcher.add_handler(CommandHandler('start', start_command))

def scheduler(job, updater, time):
    """Scheduler for reminder to be run"""
    # time = datetime.time(hour=hour, minute=minute)
    j = updater.job_queue
    j.run_daily(
        job,
        days=(0, 1, 2, 3, 4, 5, 6),
        time=time)

# TODO: Add in a database to manage E-Scholars pairings for Angel & Mortal
# TODO: Include functions for E-Scholars to chat with each other

def message_forward(update,context):
    user = db.get_user(update.effective_chat.username)
    if not user:
        context.bot.send_message(
            text="Sorry, you're not registered as a participant in Angel & Mortal",
            chat_id=update.effective_chat.id
        )
        return
    if not user.get('chat_with') == '':
        context.bot.send_message(
            text="Sorry, please select who to chat with first!",
            chat_id=update.effective_chat.id
        )
        return
    elif user.get('chat_with') == 'mortal':
        mortal_chat_id = db.get_chat_id(user.get('mortal_username'))
        if not mortal_chat_id:
            context.bot.send_message(
                text="Sorry, your mortal has not started the chat yet... ",
                chat_id=update.effective_chat.id
            )
        context.bot.send_message(
            text='Your angel says: ' + update.message.text,
            chat_id=mortal_chat_id
        )
    elif user.get('chat_with') == 'angel':
        angel_chat_id = db.get_chat_id(user.get('angel_username'))
        if not angel_chat_id:
            context.bot.send_message(
                text="Sorry, your angel has not started the chat yet... ",
                chat_id=update.effective_chat.id
            )
        context.bot.send_message(
            text='Your mortal says: ' + update.message.text,
            chat_id=angel_chat_id
        )

dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text, message_forward))

if __name__ == "__main__":
    print('Starting main!')
    updater.start_polling()
    updater.idle()
