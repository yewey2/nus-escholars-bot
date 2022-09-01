from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

# from telegram import ()

import db
from setup import setup
PLAYERS_ALL = setup()

import random
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')

LOGGING = False

updater = Updater(token=API_KEY, use_context=True)
dispatcher = updater.dispatcher

CHAT_IDS = db.get_chat_ids()

def update_chat_id(username, chat_id):
    CHAT_IDS[username] = chat_id
    db.update_chat_ids(username, chat_id)
    PLAYERS_ALL.get(username).set_chat_id(chat_id)

def start_command(update,context):
    """Initializes the bot"""
    username = update.message.from_user.username
    chat_id = update.effective_chat.id
    text =  'Hello '+(update.message.from_user.first_name or '@'+username )
    text+= '\n\nFollow this bot for more info on E-Scholars :)'
    context.bot.send_message(
        chat_id=chat_id,
        text=text)
    if chat_id > 0 and chat_id not in CHAT_IDS.keys():
        update_chat_id(username, chat_id)

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

def check_message(update,context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    if not player:
        context.bot.send_message(
            text="Sorry, you're not registered as a participant in Angel & Mortal. " + 
                 "If you believe this is a mistake, please contact the admin.",
            chat_id=update.effective_chat.id
        )
        return
    elif not player.get_chat_id():
        context.bot.send_message(
            text="Sorry, please /start me first!",
            chat_id=update.effective_chat.id
        )

    elif player.get_chat_with() == '':
        context.bot.send_message(
            text="Sorry, please select who to chat with first!",
            chat_id=update.effective_chat.id
        )
        return
    elif player.get_chat_with() == 'mortal':
        mortal_chat_id = player.get_mortal().get_chat_id()
        if not mortal_chat_id:
            context.bot.send_message(
                text="Sorry, your mortal has not started the chat yet... If this problem persists, please contact the admin.",
                chat_id=update.effective_chat.id
            )
        return mortal_chat_id
        # context.bot.send_message(
        #     text='Your angel says: ' + update.message.text,
        #     chat_id=mortal_chat_id
        # )
    elif player.get_chat_with() == 'angel':
        angel_chat_id = player.get_angel().get_chat_id()
        if not angel_chat_id:
            context.bot.send_message(
                text="Sorry, your angel has not started the chat yet... If this problem persists, please contact the admin.",
                chat_id=update.effective_chat.id
            )
        return angel_chat_id
        # context.bot.send_message(
        #     text='Your mortal says: ' + update.message.text,
        #     chat_id=angel_chat_id
        # )

def message_forward(update,context):
    forward_chat_id = check_message(update, context)
    if forward_chat_id:
        player = PLAYERS_ALL.get(update.effective_chat.username)
        forward_to = ('angel' if player.get_chat_with()=='mortal' else 
                    'mortal' if player.get_chat_with()=='angel' else 
                    None
                    )
        context.bot.send_message(
            text=f"Your {forward_to} says: {update.message.text}",
            chat_id=forward_chat_id
        )

def mortal_command(update,context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    player.set_chat_with('mortal')
    context.bot.send_message(
        text="You are now chatting with your mortal!",
        chat_id=update.effective_chat.id
    )

def angel_command(update,context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    player.set_chat_with('angel')
    context.bot.send_message(
        text="You are now chatting with your angel!",
        chat_id=update.effective_chat.id
    )

def who_command(update,context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    chat_with = player.get_chat_with()
    if chat_with:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"You are currently chatting with the {chat_with}."
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are currently not chatting with anyone."
        )

dispatcher.add_handler(MessageHandler(~Filters.command & Filters.text, message_forward))
dispatcher.add_handler(CommandHandler('angel', angel_command))
dispatcher.add_handler(CommandHandler('mortal', mortal_command))
dispatcher.add_handler(CommandHandler('who', who_command))

if __name__ == "__main__":
    print('Starting main!')
    updater.start_polling()
    updater.idle()
