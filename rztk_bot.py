"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

url = r"https://rozetka.com.ua/ua/playstation_5/p223588825/"


def get_gray(driver):
    try:
        element = driver.find_element_by_xpath("//p[@class='status-label status-label--gray ng-star-inserted']")
        print(element.text)
        return True
    except NoSuchElementException:
        return False


def get_green(driver):
    try:
        element = driver.find_element_by_xpath("//p[@class='status-label status-label--green ']")
        print(element.text)
        return True
    except NoSuchElementException:
        return False


def get_unclear(driver):
    try:
        element = driver.find_element_by_xpath("//product-main-info/ul[@class='product-statuses ng-star-inserted']")
        print(element.text)
        return True
    except NoSuchElementException:
        return False


def get_driver():
    options = Options()
    options.headless = True
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(r"C:\Users\TuG\Documents\chromedriver_win32\chromedriver.exe", chrome_options=options)
    return driver


def ps5_status():
    ret = ""
    loop = True
    count = 0
    driver = get_driver()
    driver.get(url)
    while loop:
        print("Performing availability check @" + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        count = count + 1
        if count == 12:
            count = 0
            driver.quit()
            driver = get_driver()
            driver.get(url)
        if get_gray(driver):
            time.sleep(60)
            driver.refresh()
            continue
        elif get_green(driver):
            return "Status changed!"
        elif get_unclear(driver):
            return "Check failed, please retry"

    return ret


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def start_monitor(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start_monitor is issued."""
    update.message.reply_text('Hi! Starting to check PS5 availability for you...')
    status = ps5_status()
    update.message.reply_text(status)
    update.message.reply_text(url)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


# def echo(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    updater = Updater("tkn", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("start_monitor", start_monitor))

    # on noncommand i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # ps5_status()
    main()
