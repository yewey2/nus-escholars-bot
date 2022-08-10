from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

# from telegram import ()

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

if __name__ == "__main__":
    print('Starting main!')
    updater.start_polling()
    updater.idle()
