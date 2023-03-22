import telegram

from telegram.ext import CommandHandler, CallbackQueryHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pymongo import MongoClient

import random

import os

# Set up the bot and database

bot_token = 'YOUR_BOT_TOKEN'

bot = telegram.Bot(token=bot_token)

mongo_client = MongoClient(os.getenv('MONGO_URI'))

db = mongo_client['birthday_bot_db']

videos_collection = db['birthday_videos']

# Define the command handler

def start(update, context):

    chat_id = update.effective_chat.id

    message = "🎉🎈 Happy birthday to you! 🎂🎁"

    bot.send_message(chat_id=chat_id, text=message)

    

    # Send a GIF of birthday candles

    gif_url = "https://media.giphy.com/media/3ohc1dY0HHh8WYFbrK/giphy.gif"

    bot.send_animation(chat_id=chat_id, animation=gif_url)

    

    # Send a message with options to open a card or a gift

    message = "What would you like to open first?"

    keyboard = [[InlineKeyboardButton("🎁 Open a Gift", callback_data='gift'),

                 InlineKeyboardButton("💌 Open a Card", callback_data='card')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

start_handler = CommandHandler('start', start)

# Define the callback query handler

def button(update, context):

    query = update.callback_query

    chat_id = query.message.chat_id

    message_id = query.message.message_id

    

    if query.data == 'gift':

        # Send a random video from the database

        video_count = videos_collection.count_documents({})

        if video_count > 0:

            random_video = videos_collection.aggregate([{ "$sample": { "size": 1 } }]).next()

            video_id = random_video['video_id']

            video_url = f"https://www.youtube.com/watch?v={video_id}"

            bot.send_message(chat_id=chat_id, text=f"🎁 Here's a birthday gift video for you! {video_url}")

        else:

            bot.send_message(chat_id=chat_id, text="🎁 Sorry, there are no birthday gift videos available right now.")

        

        # Update the database by incrementing the count of videos sent

        videos_collection.update_one({}, {"$inc": {"videos_sent": 1}}, upsert=True)

        

    elif query.data == 'card':

        # Send a random image

        image_urls = ["https://picsum.photos/300/200?random=1",

                      "https://picsum.photos/300/200?random=2",

                      "https://picsum.photos/300/200?random=3"]

        random_image_url = random.choice(image_urls)

        bot.send_photo(chat_id=chat_id, photo=random_image_url)

        

        # Send a message thanking the user for opening the card

        message = "💌 Thank you for opening the card! I wrote you a special message."

        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message)

button_handler = CallbackQueryHandler(button)

# Register the handlers with the dispatcher

def register_handlers(dispatcher):

    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(button_handler)

