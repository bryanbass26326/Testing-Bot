import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
BOT_TOKEN = "6889231286:AAGRv7fWmgetkwl3scLCMtJvuJ_1FavjOYs"

# Dictionary to store referral information
referral_data = {}

# Initialize the Telegram bot
updater = Updater("6889231286:AAGRv7fWmgetkwl3scLCMtJvuJ_1FavjOYs", use_context=True)
dispatcher = updater.dispatcher

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Start command handler
def start(update, context):
    user = update.effective_user
    context.user_data['referral_link'] = f't.me/{context.bot.username}?start=referral_{user.id}'
    update.message.reply_text(f'Welcome, {user.mention_markdown()}\nYour referral link: {context.user_data["referral_link"]}\nShare this link to refer new users!')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Callback query handler for tracking referrals
def referral(update, context):
    query = update.callback_query
    user = query.from_user

    if 'referral_' in query.data:
        referred_by = query.data.replace('referral_', '')
        referral_data[referred_by] = referral_data.get(referred_by, 0) + 1
        query.answer(text=f'Thanks for using a referral link from {referred_by}!')
        query.edit_message_text(f'You have been referred by {referred_by}.')
    else:
        query.answer(text='This referral link is invalid.')

referral_handler = CallbackQueryHandler(referral)
dispatcher.add_handler(referral_handler)

# Message handler for tracking referrals in text messages
def handle_text_message(update, context):
    message = update.message.text
    user = update.effective_user

    if message.startswith('/start referral_'):
        referred_by = message.replace('/start referral_', '')
        referral_data[referred_by] = referral_data.get(referred_by, 0) + 1
        update.message.reply_text(f'Thanks for using a referral link from {referred_by}!')
        update.message.reply_text(f'You have been referred by {referred_by}.')

text_message_handler = MessageHandler(Filters.text & (~Filters.command), handle_text_message)
dispatcher.add_handler(text_message_handler)

# Start the bot
updater.start_polling()
updater.idle()






























